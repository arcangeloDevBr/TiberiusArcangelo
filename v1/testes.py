from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

token = "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"  # coloque seu Hugging Face token aqui

pipe = pipeline("text-generation", model=model_id, tokenizer=model_id, 
                model_kwargs={"torch_dtype": torch.float16, "device_map": "auto"}, 
                use_auth_token=token)

pergunta = "Who are you?"
resposta = pipe(pergunta, max_new_tokens=100, do_sample=True, temperature=0.7)[0]["generated_text"]
print(resposta)