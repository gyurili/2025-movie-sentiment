import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


DEFAULT_MODEL_NAME = 'jeonghyeon97/koBERT-Senti5'

tokenizer = AutoTokenizer.from_pretrained('monologg/kobert', trust_remote_code=True)
model = AutoModelForSequenceClassification.from_pretrained(DEFAULT_MODEL_NAME)

def analyze_sentiment(text: str, model_name: str = DEFAULT_MODEL_NAME):
    if model_name != DEFAULT_MODEL_NAME:
        _model = AutoModelForSequenceClassification.from_pretrained(model_name)
    else:
        _model = model

    inputs = tokenizer([text], return_tensors='pt', padding=True, truncation=True)
    outputs = _model(**inputs)
    prediction = torch.argmax(outputs.logits, dim=1).item()

    sentiment_map = {
        0: ("Angry", 1),
        1: ("Fear", 3),
        2: ("Happy", 5),
        3: ("Tender", 4),
        4: ("Sad", 2)
    }
    label, score = sentiment_map.get(prediction, ("Unknown", 0))
    return {"sentiment": label, "score": score}