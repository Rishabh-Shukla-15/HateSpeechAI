import os
os.environ["TRANSFORMERS_NO_TF"] = "1"

import streamlit as st
import torch
from transformers import BertTokenizer, BertForSequenceClassification

# ---------------- CONFIG ----------------
MODEL_PATH = "shuklaRishabh/hate-speech-bert"   # 🔥 Hugging Face model repo
LABELS = ["Hate Speech", "Offensive", "Neutral"]

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)
    model = BertForSequenceClassification.from_pretrained(MODEL_PATH)
    model.to(DEVICE)
    model.eval()
    return tokenizer, model

tokenizer, model = load_model()

# ---------------- UI ----------------
st.set_page_config(
    page_title="Hate Speech Detection",
    page_icon="🚨",
    layout="centered"
)

st.title("🚨 Hate Speech Detection System")
st.markdown(
    """
    This application uses a **BERT-based NLP model** to classify text into:
    - **Hate Speech**
    - **Offensive Language**
    - **Neutral Content**
    """
)

text = st.text_area(
    "✍️ Enter text below",
    height=160,
    placeholder="Type or paste text here..."
)

# ---------------- PREDICTION ----------------
if st.button("🔍 Analyze Text"):
    if not text.strip():
        st.warning("⚠️ Please enter some text.")
    else:
        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128
        )

        inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1)[0]
            prediction = torch.argmax(probs).item()

        st.success(f"### 🧠 Prediction: **{LABELS[prediction]}**")

        st.subheader("📊 Confidence Scores")
        for i, label in enumerate(LABELS):
            st.progress(float(probs[i]))
            st.write(f"{label}: **{probs[i] * 100:.2f}%**")
