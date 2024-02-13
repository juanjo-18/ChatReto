import streamlit as st
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from pinecone import Pinecone
import openai

OPENAI_API_KEY = "4fdaeb2a8fda4d9a9c4d2f95a5f52b54"
OPENAI_API_BASE = "https://acc-alejandria-core-openaimagesound-pro.openai.azure.com"
OPENAI_API_SECOND = "4fdaeb2a8fda4d9a9c4d2f95a5f52b54"
OPENAI_API_VERSION = "2023-07-01-preview"
OPENAI_API_TYPE = "azure"

PINECONE_API_KEY = "9f03d0db-e331-4f64-9a47-6e7eacc857ce"
PINECONE_ENV = "eastus-azure"


# Configuración de Azure Text Analytics
text_analytics_client = TextAnalyticsClient(endpoint=OPENAI_API_BASE, credential=AzureKeyCredential(OPENAI_API_KEY))

# Configuración de Pinecone
pinecone = Pinecone(api_key=PINECONE_API_KEY)

# Configuración de OpenAI GPT-4
openai.api_key = 'TU_CLAVE_OPENAI'

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
        # Llamada a la API de GPT-4 para obtener respuestas basadas en el texto del PDF
        response = openai.Completion.create(
            engine="gpt-4",  # Reemplaza con el nombre del modelo GPT-4
            prompt=f"{text_to_analyze}\n{question}",
            max_tokens=150,
            n=1,
        )

        # Mostrar la respuesta generada por GPT-4
        st.text(f"Respuesta del modelo GPT-4: {response.choices[0].text}")
