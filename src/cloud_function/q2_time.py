from typing import List, Tuple
import json
from collections import Counter
from emoji import emoji_list
import cProfile
import pstats
from memory_profiler import memory_usage
import utils.utils as helper

def extract_emojis(text: str) -> List[str]:
    """
    Extrae todos los emojis de un texto.
    
    Args:
        text (str): El texto del cual extraer los emojis.
    
    Returns:
        List[str]: Una lista de emojis encontrados en el texto.
    """
    return [emoji['emoji'] for emoji in emoji_list(text)]

def q2_time(file_path: str) -> List[Tuple[str, int]]:
    """
    Encuentra los top 10 emojis más usados con su respectivo conteo.
    
    Args:
        file_path (str): La ruta al archivo JSON que contiene los tweets.
    
    Returns:
        List[Tuple[str, int]]: Una lista de tuplas, cada una con un emoji y el número de veces que fue usado.
    """
    emoji_counter = Counter()
    
    try:
        # Descargar el contenido del archivo desde GCS
        content = helper.download_file_from_gcs(file_path)

        for line in content.splitlines():
            try:
                tweet_content = json.loads(line)['content']
                
                # Extraer y contar los emojis directamente
                emojis = extract_emojis(tweet_content)
                emoji_counter.update(emojis)
            
            except json.JSONDecodeError:
                print("Error: No se pudo decodificar una línea del archivo JSON.")
            except KeyError:
                print("Error: Una línea del archivo JSON no contiene las claves esperadas.")
        
        # Devolver los 10 emojis más comunes
        return emoji_counter.most_common(10)
    
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no se encontró.")
        return []
    except Exception as e:
        print(f"Error inesperado: {e}")
        return []

def main(file_path: str) -> List[Tuple[str, int]]:
    """
    Función principal que ejecuta el análisis de los tweets, midiendo el tiempo de ejecución y el uso de memoria.
    
    Args:
        file_path (str): La ruta al archivo JSON que contiene los tweets.
    
    Returns:
        List[Tuple[str, int]]: Una lista de tuplas, cada una con un emoji y el número de veces que fue usado.
    """

    # Medir el tiempo de ejecución con cProfile
    profiler = cProfile.Profile()
    profiler.enable()

    result = q2_time(file_path)

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats()

    # Medir el uso de memoria
    mem_usage = memory_usage((q2_time, (file_path,)), interval=1, timeout=None)
    print(f"Memoria utilizada: {max(mem_usage)} MB \nRESULTADO:")

    return result

"""
if __name__ == "__main__":
    file_path = 'farmers-protest-tweets-2021-2-4.json'
    response = main(file_path)
    print(response)
"""
