FROM python:3.9
# Copia solo el archivo requirements.txt primero
COPY requirements.txt /app/requirements.txt
# Instala las dependencias (pandas, scikit-learn, etc.) desde requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
# Luego, instala o actualiza OpenAI
RUN pip install --no-cache-dir openai --upgrade
# Copia el resto de la aplicación
COPY src/* /app/
COPY model/hotel_model.pkl /app/model/hotel_model.pkl
# Establece el directorio de trabajo
WORKDIR /app
# Define el punto de entrada para tu aplicación
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
