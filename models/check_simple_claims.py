import argparse
import os
import json
from tqdm import tqdm
import torch
from transformers import pipeline
from coref import coref_resolution

def parse_args():
    parser = argparse.ArgumentParser()
    # dataset args
    parser.add_argument('--dataset_name', type=str)
    parser.add_argument('--save_path', type=str)
    parser.add_argument('--num_eval_samples', default=4000, type=int)
    parser.add_argument('--program_dir', type=str)
    parser.add_argument('--program_file_name', type=str)
    parser.add_argument('--model_name', type=str ,default='text-davinci-003')
    args = parser.parse_args()
    return args

class simple_check():
    def __init__(self, args) -> None:
        self.args = args

    def check_claims(self):
        classifier = pipeline('text-classification', model="FacebookAI/roberta-large-mnli")
        with open(os.path.join(self.args.program_dir, self.args.program_file_name), 'r') as f:
            dataset = json.load(f)
        dataset = dataset if self.args.num_eval_samples < 0 else dataset[:self.args.num_eval_samples]

        for sample in tqdm(dataset):
          if sample['idx']>-1:
            sequence_to_classify = sample['claim'] + '</s></s>'+ sample['divided_claims']
            try:
               result=classifier(sequence_to_classify)
               if result[0]['label']!="ENTAILMENT" and sample['logic']!="NAND" and sample['logic']!="NOR":
                   sample['divided_claims'] = sample['claim']
            except:
               print('Error in checking entaiment for example: ', sample['id'])

        for sample in tqdm(dataset):
          if sample['idx']>-1:
            try:
               sample['divided_claims']=coref_resolution(sample['divided_claims'])
            except:
               print('Error in checking coreference for example: ', sample['id'])

        sorted_outputs = sorted(dataset, key=lambda x: x['idx'])
        with open(os.path.join(self.args.save_path, f'{self.args.dataset_name}_{self.args.model_name}_checked_claims.json'), 'w') as f:
           json.dump(sorted_outputs, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    args = parse_args()
    program_checker = simple_check(args)
    program_checker.check_claims()