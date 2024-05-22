import argparse
from transformers import T5Tokenizer, T5ForConditionalGeneration
import random
from tqdm import tqdm
import re
import os
import json

import torch
import torchvision

from question_answering import T5_Question_Answering
from retriever import PyseriniRetriever

def parse_args():
    parser = argparse.ArgumentParser()
    # dataset args
    parser.add_argument('--dataset_name', type=str)
    parser.add_argument('--FV_data_path', type=str)
    parser.add_argument('--setting', help='[gold | open-book | close-book]', type=str)
    parser.add_argument('--num_eval_samples', default=2000, type=int)
    parser.add_argument('--program_dir', type=str)
    parser.add_argument('--program_file_name', type=str)
    parser.add_argument('--output_dir', type=str)
    # fact checker args
    parser.add_argument("--model_name", default = 'google/flan-t5-xl', type=str)
    parser.add_argument("--cache_dir", type=str)
    parser.add_argument('--corpus_index_path', default=None, type=str)
    parser.add_argument('--num_retrieved', default=5, type=int)
    parser.add_argument('--max_evidence_length', default=3000, help = 'to avoid exceeding GPU memory', type=int)
    args = parser.parse_args()
    return args

class Program_Execution:
    def __init__(self, args) -> None:
        # load model
        self.args = args
        CACHE_DIR = args.cache_dir
        self.model_name = args.model_name
        self.dataset_name = args.dataset_name
        print(f"Loading model {self.model_name}...")
        self.tokenizer = T5Tokenizer.from_pretrained(self.model_name, cache_dir= CACHE_DIR)
        self.model = T5ForConditionalGeneration.from_pretrained(self.model_name, cache_dir= CACHE_DIR)
        self.model.parallelize()
        print(f"Model {self.model_name} loaded.")

        self.QA_module = T5_Question_Answering(self.model, self.tokenizer)

        # load retriever
        if self.args.setting == 'open-book':
            self.searcher = PyseriniRetriever(self.args.corpus_index_path, use_bm25=True, k1=0.9, b=0.4)
        else:
            self.searcher = None

        # load dataset
        with open(os.path.join(args.FV_data_path, args.dataset_name, 'claims', f'dev.json'), 'r') as f:
            dataset = json.load(f)
        self.gold_evidence_map = {sample['id']:sample['evidence'] for sample in dataset}

    def parse_question_command(self, command, variable_map):
        return_var, tmp = command.split('= Question')
        return_var = return_var.strip()

        p1 = re.compile(f'Question\([f]?\"(.*)\"\)', re.S)
        matching = re.findall(p1, command)
        question = matching[0] if len(matching)>0 else tmp

        # replace variable
        for variable_name, variable_value in variable_map.items():
            replace_var = "{" + str(variable_name) + "}"
            if question.find(replace_var) >=0:
                question = question.replace(replace_var, variable_value)

        return return_var, question

    def retrieve_evidence(self, query):
        hits = self.searcher.retrieve(query, self.args.num_retrieved)
        evidence = '\n'.join([hit['text'].strip() for hit in hits])
        # cut overlong evidence
        if len(evidence.split()) > self.args.max_evidence_length:
            print('evidence is too long, cut it to max_evidence_length')
            evidence = ' '.join(evidence.split()[:self.args.max_evidence_length])
        
        # save retrieval results (can comment out if not needed)
        retrieved_results = []
        for hit in hits:
            retrieved_results.append({'id': hit['doc_id'], 'score': hit['score'], 'query': query})
        
        return evidence, retrieved_results
    
    def get_query_result(self, ID, program, evidence,claim):
        variable_map = {}
        claim_only = True if self.args.setting == 'close-book' else False
        retrieved_evidence = []

        question_pattern = re.compile(r'.*=\s*Question.*')
        question_commands = []
        for line in program:
            if(question_pattern.match(line)):
               question_commands.append(line)

        for command in question_commands:
            try:
                return_var, question = self.parse_question_command(command, variable_map)
                # if open-book setting, then retrieve evidence from the corpus
                if self.args.setting == 'open-book':
                    evidence, retrieved_results = self.retrieve_evidence(question)
                    retrieved_evidence += retrieved_results
                    #check if the answer exist
                check_res=self.QA_module.check_question(question,claim)
                # print(check_res['answer_text'])
                if check_res['answer_text'] == "Yes" :
                   evidence = claim
                answer = self.QA_module.answer_question_directly(question, evidence, claim_only)['answer_text']
                variable_map[return_var] = answer
            except:
                print('Error in executing questions for example: ', ID)
        
        return variable_map,retrieved_evidence

    def execute_on_dataset(self):
        # load generated program
        with open(os.path.join(self.args.program_dir, self.args.program_file_name), 'r') as f:
            dataset = json.load(f)
        dataset = dataset if self.args.num_eval_samples < 0 else dataset[:self.args.num_eval_samples]

        results = []
        for sample in tqdm(dataset):
            evidence = self.gold_evidence_map[sample['id']] if self.args.setting == 'gold' else None
            
            variable_map , retrieved_evidence = self.get_query_result(sample['id'], sample['questions'], evidence, sample['claim'])
                        
            final_claims = []
            extracted_claims = []
            try:
                for raw_text in sample['questions']:
                    match = re.search(r'claims_to_verify\s*=\s*\[.*\]', raw_text)
                    if match:
                        match_text = re.split(r',', raw_text)
                        for part in match_text:
                            pattern = r'"(.*?)"'
                            matches = re.findall(pattern, part)
                            longest_match = max(matches, key=len)
                            extracted_claims.append(longest_match)
                for claim in extracted_claims:
                   for return_var, answer in variable_map.items():
                       replace_var = "{" + str(return_var) + "}"
                       if claim.find(replace_var) >=0:
                           claim = claim.replace(replace_var, answer)
                   final_claims.append(claim)
            except:
                final_claims.append(sample['claim'])


            # execute program            
            results.append({'idx': sample['idx'],
                            'id': sample['id'], 
                            'claim': sample['claim'],
                            'gold': sample['gold'],
                            'divided_claims': sample['divided_claims'],
                            'questions': sample['questions'],
                            'logic': sample['logic'], 
                            'claims': final_claims})
        

        # save results to file
        output_path = os.path.join(self.args.output_dir, '{}_{}'.format(self.model_name.split('/')[-1], self.args.setting))
        if not os.path.exists(output_path):
            os.makedirs(output_path)
       
        output_file_name = f'{self.args.dataset_name}_final_claims.json'
        
        with open(os.path.join(output_path, output_file_name), 'w') as f:
           f.write(json.dumps(results, indent = 2))


if __name__ == "__main__":
    args = parse_args()
    program_executor = Program_Execution(args)
    program_executor.execute_on_dataset()