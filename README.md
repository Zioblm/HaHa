# HaHa
Code for FV model HaHa.

# Environment
We make experiment on Python 3.9, and you can install all other packages by 
```bash
pip install -r requirements.txt
```
## Dataset Preparation

The claims and corpus of **HOVER** can be prepared by:
```bash
bash prepare_hover_data.sh
```
Then you can begin the running of HaHa module.

Firstly it is complex claims decomposition. This will call openai-api so you should have an api-key.
```bash
python ./models/divider.py \
        --data_path ./datasets \
        --dataset_name "HOVER" \
        --model_name gpt-3.5-turbo \
        --num_eval_samples -1 \
        --api_key ...... \
        --save_path ./results/simple_claims
```

Then the entailment checking and coreference resolution module is packed in one file.
```bash
python ./models/check_simple_claims.py \
       --dataset_name HOVER  \
       --save_path ./results/checked_claims \
       --model_name gpt-3.5-turbo \
       --num_eval_samples -1  \
       --program_dir ./results/simple_claims  \
       --program_file_name HOVER_gpt-3.5-turbo_claims.json
```

Now come to the question generating, use openai-api again.
```bash
python ./models/questioning.py \
        --program_dir ./results/checked_claims \
        --program_file_name HOVER_gpt-3.5-turbo_checked_claims.json \
        --dataset_name "HOVER" \
        --model_name gpt-3.5-turbo \
        --num_eval_samples -1 \
        --api_key ...... \
        --save_path ./results/questions
```

Then answer the questions to complete the missing information. Here you can replace the setting with close-book or gold. Other model_name and your own cache_dir can be put in, too.
```bash
python ./models/question_for_information.py \
       --dataset_name HOVER \
       --setting open-book \
       --FV_data_path ./datasets \
       --program_dir ./results/questions \
       --program_file_name  HOVER_gpt-3.5-turbo_questions.json  \
       --corpus_index_path ./datasets/HOVER/corpus/index \
       --num_retrieved 5 \
       --max_evidence_length 512 \
       --num_eval_samples -1 \
       --output_dir ./results/final_claims  \
       --cache_dir ......
```
Finally verify them to get the result. Note that the file path will change if you use different evidence source setting.
```bash
python ./models/verify_for_result.py \
       --dataset_name HOVER \
       --setting open-book \
       --FV_data_path ./datasets \
       --program_dir ./results/final_claims/open-book  \
       --program_file_name HOVER_final_claims.json  \
       --corpus_index_path ./datasets/HOVER/corpus/index \
       --num_retrieved 5 \
       --max_evidence_length 512 \
       --num_eval_samples  -1 \
       --output_dir ./results/verify_result  \
       --cache_dir ......
```
You can further evaluate the result.
```bash
python ./models/evaluate.py \
       --dataset_name HOVER \
       --FV_data_path ./datasets \
       --result_file ./results/verify_result/open-book/HOVER_result.json
