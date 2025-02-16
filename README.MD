# Readme

### Download and run Ollama without root access
```shell
curl -L https://ollama.com/download/ollama-linux-amd64 -o ./ollama
sudo chmod +x /usr/bin/ollama
/usr/bin/ollama serve
/usr/bin/ollama run llama3
```

### Switch to GPU partition
```shell
 sinfo
 sinfo --Node  --partition=gpu
 sinfo --partition=gpu --format="%P %t %D %C %G"
 squeue
 srun --partition=gpu --gres=gpu:1 --pty $SHELL
 srun --partition=gpu --gres=gpu:v100_32:1 --pty $SHELL
 srun --partition=cpu --pty $SHELL
```

### CRAG benchmark
```shell
git clone https://github.com/facebookresearch/CRAG.git
cd CRAG
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install auto-gptq --no-build-isolation
# pip install auto-gptq --no-build-isolation --extra-index-url https://huggingface.github.io/autogptq-index/whl/cu118/
pip install "vllm==0.4.2"
pip install "debugpy==1.8.0"

# bzcat  crag_task_3_dev_v4.tar.bz2.part* | bzip2 >crag_task_3_dev_v4_merged.tar.bz2
cat data/crag_task_3_dev_v4.tar.bz2.part* > data/crag_task_3_dev_v4.tar.bz2

pip install huggingface_hub[hf_transfer]
huggingface-cli login
HF_HUB_ENABLE_HF_TRANSFER=1 huggingface-cli download \
    meta-llama/Meta-Llama-3-8B-Instruct \
    --local-dir-use-symlinks False \
    --local-dir models/meta-llama/Meta-Llama-3-8B-Instruct \
    --exclude *.pth # These are alternates to the safetensors hence not needed

# for local testing only
HF_HUB_ENABLE_HF_TRANSFER=1 huggingface-cli download \
    meta-llama/Llama-3.2-3B-Instruct \
    --local-dir-use-symlinks False \
    --local-dir models/meta-llama/Llama-3.2-3B-Instruct \
    --exclude *.pth # These are alternates to the safetensors hence not needed
    
HF_HUB_ENABLE_HF_TRANSFER=1 huggingface-cli download \
   sentence-transformers/all-MiniLM-L6-v2 \
    --local-dir-use-symlinks False \
    --local-dir models/sentence-transformers/all-MiniLM-L6-v2 \
    --exclude *.bin *.h5 *.ot # These are alternates to the safetensors hence not needed
    
HF_HUB_ENABLE_HF_TRANSFER=1 huggingface-cli download   intfloat/e5-base-v2   --local-dir-use-symlinks False     --local-dir models/intfloat/e5-base-v2     --exclude *.pth

# python local_evaluation.py
python local_evaluation.py --dataset-path data/crag_task_1_and_2_dev_v4.jsonl.bz2

cd mock_api
# python3 -m venv .venv
# source .venv/bin/activate
pip install -r requirements.txt
pip install "numpy<2.0.0"
uvicorn server:app --reload


```

### FlashRAG benchmark
```shell
HF_HUB_ENABLE_HF_TRANSFER=1 huggingface-cli download     meta-llama/Meta-Llama-3-8B-Instruct     --local-dir-use-symlinks False     --local-dir models/meta-llama/Meta-Llama-3-8B-Instruct     --exclude *.pth # These are alternates to the safetensors hence not needed

HF_HUB_ENABLE_HF_TRANSFER=1 huggingface-cli download     meta-llama/Llama-3.2-3B-Instruct     --local-dir-use-symlinks False     --local-dir models/meta-llama/Llama-3.2-3B-Instruct     --exclude *.pth

HF_HUB_ENABLE_HF_TRANSFER=1 huggingface-cli download RUC-NLPIR/FlashRAG_datasets   --local-dir-use-symlinks False     --local-dir datasets/FlashRAG_datasets     --exclude *.pth --repo-type dataset

python -m flashrag.retriever.index_builder   --retrieval_method e5   --model_path ~/models/intfloat/e5-base-v2/   --corpus_path ~/datasets/FlashRAG_datasets/retrieval-corpus/domainrag_text_corpus.jsonl   --save_dir ~/indexes/   --use_fp16   --max_length 512   --batch_size 256   --pooling_method mean   --sentence_transformer   --faiss_type Flat

python run_exp.py --method_name 'naive'                   --split 'test'                   --dataset_name 'nq'                   --gpu_id '0'
```


```shell
 ssh -NfL localhost:9999:localhost:9999  kucerj56@cluster.in.fit.cvut.cz
 ssh -NfL localhost:9999:localhost:9999 kucerj56@cf-prod-node-031
```