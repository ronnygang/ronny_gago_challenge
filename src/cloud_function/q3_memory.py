from typing import List, Tuple
import json
from collections import Counter
from emoji import emoji_list
import cProfile
import pstats
from memory_profiler import memory_usage
import utils.utils as helper

def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    """
    Encuentra los top 10 usuarios más mencionados en los tweets.
    
    Args:
        file_path (str): La ruta al archivo JSON que contiene los tweets.
    
    Returns:
        List[Tuple[str, int]]: Una lista de tuplas, cada una con un usuario y el número de veces que fue mencionado.
    """
    users_counter = Counter()
    
    try:
        # Descargar el contenido del archivo desde GCS
        content = helper.download_file_from_gcs(file_path)

        for line in content.splitlines():
            try:
                tweet = json.loads(line)
                mentioned_users = tweet.get('mentionedUsers', [])
                
                if not mentioned_users:
                    continue
                
                usernames = [user['username'] for user in mentioned_users]
                users_counter.update(usernames)
            
            except json.JSONDecodeError:
                print("Error: No se pudo decodificar una línea del archivo JSON.")
            except KeyError:
                print("Error: Una línea del archivo JSON no contiene las claves esperadas.")
        
        return users_counter.most_common(10)
    
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
        List[Tuple[str, int]]: Una lista de tuplas, cada una con un usuario y el número de veces que fue mencionado.
    """

    # Medir el tiempo de ejecución con cProfile
    profiler = cProfile.Profile()
    profiler.enable()

    result = q3_memory(file_path)

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats()

    # Medir el uso de memoria
    mem_usage = memory_usage((q3_memory, (file_path,)), interval=1, timeout=None)
    print(f"Memoria utilizada: {max(mem_usage)} MB \nRESULTADO:")

    return result

"""
if __name__ == "__main__":
    file_path = 'farmers-protest-tweets-2021-2-4.json'
    response = main(file_path)
    print(response)
"""