from fastapi import FastAPI
from pydantic import BaseModel
import torch
import os
from core.gpt import GPT, GPTConfig, generate_text
from tokenizers import Tokenizer

app = FastAPI()

# --- Config Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'core', 'best_model.pt')
TOKENIZER_PATH = os.path.join(BASE_DIR, 'core', 'tokenizer.json')

# --- Load Resources ---
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"⚙️ Loading model on {device}...")

try:
    # 1. Load Tokenizer
    tokenizer = Tokenizer.from_file(TOKENIZER_PATH)
    
    # 2. Load Model Architecture
    config = GPTConfig()
    model = GPT(config).to(device)
    
    # 3. Load Weights
    checkpoint = torch.load(MODEL_PATH, map_location=device, weights_only=False)
    # هندل کردن حالتی که فایل شامل دیکشنری کامل است یا فقط وزن‌ها
    if 'model' in checkpoint:
        state_dict = checkpoint['model']
    else:
        state_dict = checkpoint
        
    model.load_state_dict(state_dict)
    model.eval() # حتما روی حالت ارزیابی باشد
    print("✅ Model & Tokenizer Loaded Successfully!")
    
except FileNotFoundError as e:
    print(f"❌ CRITICAL ERROR: File not found -> {e}")
    print("Please make sure 'best_model.pt' and 'tokenizer.json' are in the 'core' folder.")
    model = None

class RequestData(BaseModel):
    text: str
    length: int = 100
    temp: float = 0.9

@app.post("/generate")
def gen_endpoint(data: RequestData):
    if model is None:
        return {"error": "Model failed to load. Check server logs."}
    
    result = generate_text(
        model, tokenizer, 
        prompt=data.text, 
        max_len=data.length, 
        device=device,
        temp=data.temp
    )
    return {"generated": result}