# Readme

### Download and run Ollama without root access
```shell
sudo curl -L https://ollama.com/download/ollama-linux-amd64 -o /usr/bin/ollama
sudo chmod +x /usr/bin/ollama
/usr/bin/ollama serve
/usr/bin/ollama run llama3
```

### Switch to GPU partition
```shell
 srun --partition=gpu --gres=gpu:1 --pty $SHELL
```