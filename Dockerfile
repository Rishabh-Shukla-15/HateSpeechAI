FROM python:3.10-slim

WORKDIR /app

ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_FILE_WATCHER_TYPE=none
ENV STREAMLIT_SERVER_RUN_ON_SAVE=false

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

EXPOSE 7860

CMD ["sh", "-c", "streamlit run src/streamlit_app.py --server.port=7860 --server.address=0.0.0.0"]
