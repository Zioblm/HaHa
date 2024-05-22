import argparse
from transformers import T5Tokenizer, T5ForConditionalGeneration
import random
from tqdm import tqdm
import re
import os
import json

import torch
torch.cuda.current_device()
import torchvision

from question_answering import T5_Question_Answering
from retriever import PyseriniRetriever
from evaluate import print_evaluation_results

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

    def map_direct_answer_to_label(self, predict):
        predict = predict.lower().strip()
        label_map = {'true': True, 'false': False, 'yes': True, 'no': False, "it's impossible to say": False}
        if predict in label_map:
            return label_map[predict]
        else:
            print(f"Alert!!! wrong answer mapping: {predict}")
            return random.sample([True, False], 1)[0]

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
    
    def get_verify_result(self, ID, claim,  evidence):
        claim_only = True if self.args.setting == 'close-book' else False
        retrieved_evidence = []
        final_answer = None
        
        if self.args.setting == 'open-book':
            evidence, retrieved_results = self.retrieve_evidence(claim)
            retrieved_evidence += retrieved_results
        
        answer = self.QA_module.answer_verify_question(claim, evidence, claim_only)['answer_text']
        final_answer = self.map_direct_answer_to_label(answer)
                  
        return final_answer, retrieved_evidence

    def execute_on_dataset(self):
        # load generated program
        with open(os.path.join(self.args.program_dir, self.args.program_file_name), 'r') as f:
            dataset = json.load(f)
        dataset = dataset if self.args.num_eval_samples < 0 else dataset[:self.args.num_eval_samples]

        gt_labels, predictions = [], []
        results = []
        for sample in tqdm(dataset):
            claims = sample['claims']
            gt_labels.append(sample['gold'])
            # get evidence
            evidence = self.gold_evidence_map[sample['id']] if self.args.setting == 'gold' else None
            
            # execute program
            sample_predictions = []
            if len(claims) == 0:
                claims.append(sample['claim'])
            for claim in claims:
                try:
                    single_prediction, retrieved_evidence = self.get_verify_result(sample['id'], claim, evidence)
                except Exception as e:
                    print(f"Alert!!! execution error: {sample['id']}")
                    single_prediction = random.sample([True, False], 1)[0]
                sample_predictions.append(single_prediction)

            if sample['logic']=="OR" or sample['logic']=="NOR":
                final_prediction = False
                for pred in sample_predictions:
                    final_prediction = final_prediction or pred 
                if sample['logic']=="NOR":
                    final_prediction = not final_prediction

            else:
                final_prediction = True
                for pred in sample_predictions:
                    final_prediction = final_prediction and pred 
                if sample['logic']=="NAND":
                    final_prediction = not final_prediction

            predictions.append('supports' if final_prediction == True else 'refutes')
            results.append({'id': sample['id'], 
                            'claim': sample['claim'],
                            'gold': sample['gold'], 
                            'prediction': 'supports' if final_prediction == True else 'refutes'})
        
        # evaluate
        self.evaluation(predictions, gt_labels)

        # save results to file
        output_path = os.path.join(self.args.output_dir, '{}_{}'.format(self.model_name.split('/')[-1], self.args.setting))
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        output_file_name = f'{self.args.dataset_name}_result.json'
        with open(os.path.join(output_path, output_file_name), 'w') as f:
           f.write(json.dumps(results, indent = 2))

    def evaluation(self, predictions, gt_labels):
        print_evaluation_results(predictions, gt_labels, num_of_classes=2)

if __name__ == "__main__":
    args = parse_args()
    program_executor = Program_Execution(args)
    program_executor.execute_on_dataset()