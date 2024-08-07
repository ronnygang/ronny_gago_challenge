# Resolución Latam Challenge

**Dev:** Ronny Jhancarlo Gago Pizarro

## Requisitos on-premise:

1. **Descargar el dataset:**
   - Descargar el dataset dentro de la carpeta `src` en el siguiente [link](https://drive.usercontent.google.com/download?id=1ig2ngoXFTxP5Pa8muXo02mDTFexZzsis&export=download&authuser=0).

2. **Descomprimir el dataset:**
   ```bash
   unzip tweets.json.zip

3. **Crear entorno de desarrollo:**
   ```bash
   python3.9 -m venv venv

4. **Activar entorno de desarrollo:**
   ```bash
   source venv/scripts/activate

5. **Instalar librerías y paquetes utilizados:**
   ```bash
   pip install -r requirements.txt


## Requisitos GCP:
1. **Crear bucket en GCP:**
   ```bash
   PROJECT_ID=$(gcloud config get-value project)
   gsutil mb gs://$PROJECT_ID-challenge-latam

2. **Copiar dataset al bucket en GCP:**
   ```bash
   gsutil cp src/farmers-protest-tweets-2021-2-4.json gs://$PROJECT_ID-challenge-latam

3. **Desplegar cloud function:**
   ```bash
   gcloud functions deploy data-extract-test \
   --allow-unauthenticated \
   --region us-east1 \
   --timeout 540 \
   --runtime python39 \
   --project $PROJECT_ID \
   --trigger-http \
   --entry-point main \
   --memory=2048MB \
   --source ./