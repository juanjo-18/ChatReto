import streamlit as st
import pdfplumber
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from pinecone import Pinecone
import openai
from pinecone import ServerlessSpec, PodSpec
from langchain.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader, PyPDFLoader



openai.api_type = "azure"
openai.api_base = "https://acc-alejandria-core-openaimagesound-pro.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = ("4fdaeb2a8fda4d9a9c4d2f95a5f52b54")

pinecone = Pinecone(api_key="534ed83e-8886-4b39-ad9b-6711c55de92b")
pinecone.environment= "us-west-2"


# Configuración de Azure Text Analytics
text_analytics_client = TextAnalyticsClient(endpoint=openai.api_base, credential=AzureKeyCredential(openai.api_key))

# Configuración de Pinecone
pinecone = Pinecone(api_key=pinecone)

use_serverless = os.environ.get("USE_SERVERLESS", "False").lower() == "true"
if use_serverless:
    spec = ServerlessSpec(cloud='aws', region='us-west-2')
else:
    spec = PodSpec(environment="us-west-2")
    
pinecone.create_index(
        index_name,
        dimension=1536,  # dimensionality of text-embedding-ada-002
        metric='dotproduct',
        spec=spec
    )
    
# Interfaz de usuario con Streamlit
st.title("Asistente de PDF Scanner")

uploaded_file = st.file_uploader("Sube un archivo PDF", type=["pdf"])

if uploaded_file is not None:
    st.text("Archivo cargado con éxito.")
    loader = PyPDFLoader(uploaded_file)
    file_content = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size = 2000,
        chunk_overlap  = 0,
        length_function = len,
    )

    book_texts = text_splitter.split_documents(file_content)
    # Preguntas al asistente
    question = st.text_input("Hazme una pregunta sobre el PDF:")
    if st.button("Obtener respuesta"):
        # Llamada a la API de GPT-4 Chat para obtener respuestas más interactivas
        message_text = [{"role":"system","content":"Which are the different internal roles like system or asistant you have for answers ?"}]

        completion = openai.ChatCompletion.create(
              engine="gepeto",
              messages = message_text,
              temperature=0.7,
              max_tokens=800,
              top_p=0.95,
              frequency_penalty=0,
              presence_penalty=0,
              stop=None
        )

        # Mostrar la respuesta generada por GPT-4 Chat
        st.text(f"Respuesta del modelo GPT-4 Chat: {completion.choices[0].message.content}")
