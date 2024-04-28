from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "sberbank-ai/rugpt3small_based_on_gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


def generate_text(prompt: str, max_length: int = 50, temperature: float = 0.9):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    output = model.generate(input_ids, max_length=max_length, temperature=temperature)
    decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)

    return decoded_output


def get_feedback(prompt: str) -> str:
    generated_text = generate_text(prompt, max_length=300, temperature=0.9)

    return generated_text
