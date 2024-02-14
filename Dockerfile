FROM python:3.9
RUN pip install pandas scikit-learn==1.2.2 streamlit numpy azure-ai-textanalytics pinecone-client openai pypdf langchain langchain-community
COPY requirements.txt /app/requirements.txt
COPY src/* /app/
COPY model/hotel_model.pkl /app/model/hotel_model.pkl
WORKDIR /app
ENTRYPOINT [ "streamlit","run","app.py","--server.port=8501","--server.address=0.0.0.0"]
