from typing import List, Tuple
from datetime import datetime
import json
from collections import defaultdict, Counter
import cProfile
import pstats
from memory_profiler import memory_usage

def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    """
    Encuentra las top 10 fechas con mas tweets y menciona el usuario con mas publicaciones en cada una de esas fechas.
    
    Args:
        file_path (str): La ruta al archivo JSON que contiene los tweets.
    
    Returns:
        List[Tuple[datetime.date, str]]: Una lista de tuplas, cada una con una fecha y el usuario que mas tweets publico en esa fecha.
    """
    try:
        # Se usa un solo diccionario para mantener el conteo de tweets por usuario y fecha.
        dates_dict = defaultdict(Counter)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            # Se analiza linea por linea para optimizar el uso de memoria.
            for line in f:
                tweet = json.loads(line)
                tweet_date = tweet['date'].split('T')[0]
                username = tweet['user']['username']
                
                # Se actualiza el contador de tweets escritos por un usuario en un dia.
                dates_dict[tweet_date][username] += 1
        
        # Se ordenan las fechas segun el numero de tweets que se publicaron ese dia.
        top_dates = sorted(dates_dict.keys(), key=lambda x: sum(dates_dict[x].values()), reverse=True)[:10]
        
        # Se obtiene el usuario con mayor cantidad de tweets para cada fecha segun el numero registrado en el contador.
        top_users = [max(dates_dict[date], key=dates_dict[date].get) for date in top_dates]
        
        # Se pasan todas las fechas a formato datetime.date()
        top_dates = [datetime.strptime(date_str, "%Y-%m-%d").date() for date_str in top_dates]
        
        return list(zip(top_dates, top_users))
    
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no se encontro.")
        return []
    except json.JSONDecodeError:
        print("Error: No se pudo decodificar el archivo JSON.")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def main():
    """
    Funcion principal que ejecuta el analisis de los tweets, midiendo el tiempo de ejecucion y el uso de memoria.
    """
    file_path = 'farmers-protest-tweets-2021-2-4.json'

    # Medir el tiempo de ejecucion con cProfile
    profiler = cProfile.Profile()
    profiler.enable()

    result = q1_time(file_path)

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats()

    # Medir el uso de memoria
    mem_usage = memory_usage((q1_time, (file_path,)), interval=1, timeout=None)
    print(f"Memoria utilizada: {max(mem_usage)} MB \nRESULTADO:")

    return result

"""
if __name__ == "__main__":
    response = main()
    print(response)
"""