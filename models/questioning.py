import argparse
import os
import json
from tqdm import tqdm
import time

from prompt import Prompt_Loader
from utils import OpenAIModel

class Reasoning_Program_Generator:
    def __init__(self, args):
        self.args = args
        self.program_dir = args.program_dir
        self.program_file_name = args.program_file_name
        self.dataset_name = args.dataset_name
        self.model_name = args.model_name
        self.save_path = args.save_path

        self.openai_api = OpenAIModel(args.api_key, args.model_name, args.stop_words, args.max_new_tokens)
        self.prompt_loader = Prompt_Loader()

    def update_results(self, sample, generated_text):
        result_list = [operation.strip() for operation in generated_text.split('\n')]
        self.result_dict[sample['id']]['questions'] = result_list
        
    def batch_generate_programs(self, batch_size = 10):
        # create output_dir
        self.result_dict = []
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

        with open(os.path.join(self.args.program_dir, self.args.program_file_name), 'r') as f:
            dataset = json.load(f)
        dataset = dataset if self.args.num_eval_samples < 0 else dataset[:self.args.num_eval_samples]

        print(f"Loaded {len(dataset)} claims from {self.program_file_name}.")

        # generate programs
        temperature = 0.0
        outputs = []
        # split dataset into chunks
        dataset_chunks = [dataset[i:i + batch_size] for i in range(0, len(dataset), batch_size)]
        
        # initialize empty results
        result_dict = {}
        for idx, sample in enumerate(dataset):
            result = {'idx': idx,
                        'id': sample['id'], 
                        'claim': sample['claim'],
                        'gold': sample['gold'],
                        'questions': [],
                        'logic': sample['logic'],
                        'divided_claims': sample['divided_claims']}
            result_dict[sample['id']] = result
        self.result_dict = result_dict

        print(f"Begin generating questions...")
        # for each chunk
        for chunk in tqdm(dataset_chunks):
            # create prompt
            full_prompts = [self.prompt_loader.prompt_construction_a(example['divided_claims'], self.dataset_name) for example in chunk]
            try:
                batch_outputs = self.openai_api.batch_generate(full_prompts,temperature)
                # create output
                for sample, output in zip(chunk, batch_outputs):
                  self.update_results(sample, output)
                outputs.clear()    
                for key in result_dict:
                    outputs.append(result_dict[key])
                sorted_outputs = sorted(outputs, key=lambda x: x['idx'])
                with open(os.path.join(self.save_path, f'{self.dataset_name}_{self.model_name}_programs.json'), 'w') as f:
                    json.dump(sorted_outputs, f, indent=2, ensure_ascii=False)
            except:
                # generate one by one if batch generation fails
                for sample, full_prompt in zip(chunk, full_prompts):
                  if self.result_dict[sample['id']]['idx']>-1:
                    try:
                        output = self.openai_api.generate(full_prompt, temperature)
                        # time.sleep(3)
                        print('g')
                        self.update_results(sample, output)
                    except:
                        print('Error in generating reasoning programs for example: ', sample['id'])
                  outputs.clear()
                  for key in result_dict:
                      outputs.append(result_dict[key])
                  sorted_outputs = sorted(outputs, key=lambda x: x['idx'])
                  with open(os.path.join(self.save_path, f'{self.dataset_name}_{self.model_name}_programs.json'), 'w') as f:
                      json.dump(sorted_outputs, f, indent=2, ensure_ascii=False)


        print(f"Generated {len(result_dict)} examples.")


def parse_args():
    parser = argparse.ArgumentParser()
    # dataset args
    parser.add_argument('--dataset_name', default='HOVER', type=str)
    parser.add_argument('--program_dir', type=str)
    parser.add_argument('--program_file_name', type=str)
    parser.add_argument('--num_eval_samples', default=-1, type=int)
    parser.add_argument('--save_path', default = './results/programs', type=str)
    parser.add_argument('--api_key', type=str)
    parser.add_argument('--model_name', type=str, default='text-davinci-003')
    parser.add_argument('--stop_words', type=str, default='# The claim is')
    parser.add_argument('--max_new_tokens', type=int, default=1024)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_args()
    generator = Reasoning_Program_Generator(args)
    generator.batch_generate_programs()