from typing import List, Tuple
from datetime import datetime
import json
from collections import Counter
import cProfile
import pstats
from memory_profiler import memory_usage
import utils.utils as helper

def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    """
    Encuentra las top 10 fechas con más tweets y menciona el usuario con más publicaciones en cada una de esas fechas.
    
    Args:
        file_path (str): La ruta al archivo JSON que contiene los tweets.
    
    Returns:
        List[Tuple[datetime.date, str]]: Una lista de tuplas, cada una con una fecha y el usuario que más tweets publicó en esa fecha.
    """
    date_counter = Counter()
    user_counter_per_date = {}

    try:
        # Descargar el contenido del archivo desde GCS
        content = helper.download_file_from_gcs(file_path)

        # Leer y procesar cada línea una vez
        for line in content.splitlines():
            try:
                tweet = json.loads(line)
                tweet_date = tweet['date'].split('T')[0]
                username = tweet['user']['username']

                # Contar fechas
                date_counter[tweet_date] += 1

                # Contar usuarios por fecha
                if tweet_date not in user_counter_per_date:
                    user_counter_per_date[tweet_date] = Counter()
                user_counter_per_date[tweet_date][username] += 1
            except json.JSONDecodeError:
                print("Error: No se pudo decodificar una línea del archivo JSON.")
            except KeyError:
                print("Error: Una línea del archivo JSON no contiene las claves esperadas.")

        # Obtener las 10 fechas más comunes
        most_common_dates = date_counter.most_common(10)

        # Obtener el usuario más común por cada una de las fechas más comunes
        most_common_users = [user_counter_per_date[date[0]].most_common(1)[0][0] for date in most_common_dates]

        # Convertir las fechas a formato datetime.date y agrupar resultados
        return list(zip([datetime.strptime(date[0], "%Y-%m-%d").date() for date in most_common_dates], most_common_users))
    
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no se encontró.")
        return []
    except Exception as e:
        print(f"Error inesperado: {e}")
        return []

def main(file_path: str) -> List[Tuple[datetime.date, str]]:
    """
    Función principal que ejecuta el análisis de los tweets, midiendo el tiempo de ejecución y el uso de memoria.
    
    Args:
        file_path (str): La ruta al archivo JSON que contiene los tweets.

    Returns:
        List[Tuple[datetime.date, str]]: Una lista de tuplas, cada una con una fecha y el usuario que más tweets publicó en esa fecha.
    """    

    # Medir el tiempo de ejecución con cProfile
    profiler = cProfile.Profile()
    profiler.enable()

    result = q1_memory(file_path)

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats()

    # Medir el uso de memoria
    mem_usage = memory_usage((q1_memory, (file_path,)), interval=1, timeout=None)
    print(f"Memoria utilizada: {max(mem_usage)} MB \nRESULTADO:")

    return result

"""
if __name__ == "__main__":
    file_path = 'farmers-protest-tweets-2021-2-4.json'
    response = main(file_path)
    print(response)
"""