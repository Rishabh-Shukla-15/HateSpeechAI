FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY README.md .

EXPOSE 7860

CMD ["sh", "-c", "streamlit run app.py --server.port=7860 --server.address=0.0.0.0"]
