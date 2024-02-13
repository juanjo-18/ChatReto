import streamlit as st
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from pinecone import Pinecone
import openai

openai.api_type = "azure"
openai.api_base = "https://acc-alejandria-core-openaimagesound-pro.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = ("4fdaeb2a8fda4d9a9c4d2f95a5f52b54")

pinecone.api_key = "9f03d0db-e331-4f64-9a47-6e7eacc857ce"
pinecone.environment= "eastus-azure"


# Configuración de Azure Text Analytics
text_analytics_client = TextAnalyticsClient(endpoint=openai.api_base, credential=AzureKeyCredential(openai.api_key))

# Configuración de Pinecone
pinecone = Pinecone(api_key=pinecone.api_key)

# Función para analizar texto con Azure Text Analytics
def analyze_text(text):
    response = text_analytics_client.analyze_sentiment(documents=[{"id": "1", "language": "es", "text": text}])
    return response[0].sentiment

# Función para indexar un documento en Pinecone
def index_document(document):
    pinecone.index(index_name=pinecone.environment, ids=[document["id"]], vectors=[document["vector"]])

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
