from google.cloud import storage
import utils.config as config

def download_file_from_gcs(file_path: str) -> str:
    """
    Descarga el contenido de un archivo desde un bucket de Google Cloud Storage.

    Args:
        file_path (str): La ruta al archivo dentro del bucket.

    Returns:
        str: El contenido del archivo como una cadena de texto.
    """
    try:
        # Inicializar el cliente de GCS
        client = storage.Client()
        bucket = client.bucket(config.BUCKET_NAME)
        blob = bucket.blob(file_path)
        
        # Descargar el contenido del archivo
        content = blob.download_as_text(encoding='utf-8')
        return content
    except Exception as e:
        print(f"Error al descargar el archivo desde GCS: {e}")
        return ""