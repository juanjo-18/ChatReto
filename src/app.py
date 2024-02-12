import streamlit as st
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from pinecone import Pinecone

OPENAI_API_KEY = "4fdaeb2a8fda4d9a9c4d2f95a5f52b54"
OPENAI_API_BASE = "https://acc-alejandria-core-openaimagesound-pro.openai.azure.com"
OPENAI_API_SECOND = "4fdaeb2a8fda4d9a9c4d2f95a5f52b54"
OPENAI_API_VERSION = "2023-07-01-preview"
OPENAI_API_TYPE = "azure"

PINECONE_API_KEY = "1199e2a1-68b5-4641-a3b5-1eecfb9653ea"
PINECONE_ENV = "gcp-starter"


# Configuración de Azure Text Analytics
text_analytics_client = TextAnalyticsClient(endpoint=OPENAI_API_BASE, credential=AzureKeyCredential(OPENAI_API_KEY))

# Configuración de Pinecone
pinecone = Pinecone(api_key=pinecone_api_key)

# Función para analizar texto con Azure Text Analytics
def analyze_text(text):
    response = text_analytics_client.analyze_sentiment(documents=[{"id": "1", "language": "es", "text": text}])
    return response[0].sentiment

# Función para indexar un documento en Pinecone
def index_document(document):
    pinecone.index(index_name=PINECONE_ENV, ids=[document["id"]], vectors=[document["vector"]])

# Interfaz de usuario con Streamlit
st.title("Asistente de PDF Scanner")

uploaded_file = st.file_uploader("Sube un archivo PDF", type=["pdf"])

if uploaded_file is not None:
    st.text("Archivo cargado con éxito.")

    # Procesar el PDF y extraer texto (puedes usar bibliotecas como PyMuPDF para esto)
    # Luego, utiliza Azure Text Analytics para analizar el texto y Pinecone para indexar el documento.

    # Ejemplo de análisis de texto con Azure Text Analytics
    text_to_analyze = "Texto extraído del PDF"
    sentiment = analyze_text(text_to_analyze)
    st.text(f"Sentimiento del texto: {sentiment}")

    # Ejemplo de indexación con Pinecone
    document_to_index = {"id": "1", "vector": [0.1, 0.2, 0.3]}  # Reemplaza con tu propio vector
    index_document(document_to_index)

    # Preguntas al asistente
    question = st.text_input("Hazme una pregunta sobre el PDF:")
    if st.button("Obtener respuesta"):
        # Realiza la búsqueda en Pinecone utilizando la pregunta y muestra la respuesta.
        # También puedes utilizar el modelo de Azure OpenIA aquí para obtener respuestas basadas en el texto del PDF.
        st.text("Respuesta: Aquí debería estar la respuesta basada en el modelo y Pinecone.")
