import argparse
import os
import re
import json
from tqdm import tqdm
import time


from myprompt import Prompt_Loader
from utils import OpenAIModel

def get_res(text):
    lines = text.split('\n')
    if lines:
        raw_claims = '\n'.join(lines[:-1])
        raw_logic = lines[-1]
        claims = re.findall(r':\s*"(.*?)\."', raw_claims)
        T1 = ".\n".join(claims) + "."
        T2 = raw_logic.split(":")[1]
        return T1,T2

class Reasoning_Program_Generator:
    def __init__(self, args):
        self.args = args
        self.data_path = args.data_path
        self.dataset_name = args.dataset_name
        self.model_name = args.model_name
        self.save_path = args.save_path

        self.openai_api = OpenAIModel(args.api_key, args.model_name, args.stop_words, args.max_new_tokens)
        self.prompt_loader = Prompt_Loader()


    def batch_generate_programs(self, batch_size = 10):
        # create output_dir
        self.result_dict = []
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

        # load dataset
        with open(os.path.join(self.data_path, self.dataset_name, 'claims', 'dev.json'), 'r') as f:
            raw_dataset = json.load(f)
        
        raw_dataset = raw_dataset if self.args.num_eval_samples < 0 else raw_dataset[:self.args.num_eval_samples]
        print(f"Loaded {len(raw_dataset)} examples from {self.dataset_name} dev set.")

        # generate programs
        temperature = 0.0
        outputs = []
        # split dataset into chunks
        dataset_chunks = [raw_dataset[i:i + batch_size] for i in range(0, len(raw_dataset), batch_size)]
        
        # initialize empty results
        result_dict = {}
        for idx, sample in enumerate(raw_dataset):
            result = {'idx': idx,
                        'id': sample['id'], 
                        'claim': sample['claim'],
                        'gold': sample['label'], 
                        'divided_claims': "Error in generating simple claims for this example",
                        'logic': "NULL"}
            result_dict[sample['id']] = result
        self.result_dict = result_dict

        print(f"Begin generating simple claims...")
        # for each chunk
        for chunk in tqdm(dataset_chunks):
            # create prompt
            full_prompts = [self.prompt_loader.prompt_construction(example['claim'], self.dataset_name) for example in chunk]
            try:
                batch_outputs = self.openai_api.batch_generate(full_prompts,temperature)
                # create output
                for sample, raw_output in zip(chunk, batch_outputs):
                    res_claims , res_logic=extract_res(raw_output)
                    self.result_dict[sample['id']]['divided_claims']=res_claims
                    self.result_dict[sample['id']]['logic']=res_logic
                outputs.clear()    
                for key in result_dict:
                    outputs.append(result_dict[key])
                sorted_outputs = sorted(outputs, key=lambda x: x['idx'])
                with open(os.path.join(self.save_path, f'{self.dataset_name}_{self.model_name}_claims.json'), 'w') as f:
                    json.dump(sorted_outputs, f, indent=2, ensure_ascii=False)
            except:
                # generate one by one if batch generation fails
                for sample, full_prompt in zip(chunk, full_prompts):
                  if self.result_dict[sample['id']]['idx']>-1:
                    try:
                        raw_output = self.openai_api.generate(full_prompt, temperature)
                        res_claims , res_logic = get_res(raw_output)
                        self.result_dict[sample['id']]['divided_claims']=res_claims
                        self.result_dict[sample['id']]['logic']=res_logic
                        time.sleep(1)
                        print("s")
                    except:
                        print('Error in generating reasoning programs for example: ', sample['id'])
                  outputs.clear()
                  for key in result_dict:
                      outputs.append(result_dict[key])
                  sorted_outputs = sorted(outputs, key=lambda x: x['idx'])
                  with open(os.path.join(self.save_path, f'{self.dataset_name}_{self.model_name}_claims.json'), 'w') as f:
                      json.dump(sorted_outputs, f, indent=2, ensure_ascii=False)


        print(f"Generated {len(result_dict)} examples.")


def parse_args():
    parser = argparse.ArgumentParser()
    # dataset args
    parser.add_argument('--dataset_name', default='HOVER', type=str)
    parser.add_argument('--data_path', type=str)
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