from typing import List, Tuple
import json
from collections import Counter
from emoji import emoji_list
import cProfile
import pstats
from memory_profiler import memory_usage

def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    """
    Encuentra los top 10 emojis más usados con su respectivo conteo.
    
    Args:
        file_path (str): La ruta al archivo JSON que contiene los tweets.
    
    Returns:
        List[Tuple[str, int]]: Una lista de tuplas, cada una con un emoji y el número de veces que fue usado.
    """
    emoji_counter = Counter()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    tweet_content = json.loads(line)['content']
                    
                    # Se obtienen los emojis de la línea analizada
                    tweet_emojis = [emoji['emoji'] for emoji in emoji_list(tweet_content)]
                    
                    # Se actualiza el contador externo con los emojis encontrados en esta línea.
                    emoji_counter.update(tweet_emojis)
                
                except json.JSONDecodeError:
                    print("Error: No se pudo decodificar una línea del archivo JSON.")
                except KeyError:
                    print("Error: Una línea del archivo JSON no contiene las claves esperadas.")
        
        # Se devuelven los 10 emojis más presentes en todo el archivo.
        return emoji_counter.most_common(10)
    
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no se encontró.")
        return []
    except Exception as e:
        print(f"Error inesperado: {e}")
        return []

def main():
    """
    Función principal que ejecuta el análisis de los tweets, midiendo el tiempo de ejecución y el uso de memoria.
    """
    file_path = 'farmers-protest-tweets-2021-2-4.json'

    # Medir el tiempo de ejecución con cProfile
    profiler = cProfile.Profile()
    profiler.enable()

    result = q2_memory(file_path)

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats()

    # Medir el uso de memoria
    mem_usage = memory_usage((q2_memory, (file_path,)), interval=1, timeout=None)
    print(f"Memoria utilizada: {max(mem_usage)} MB \nRESULTADO:")

    return result


"""
if __name__ == "__main__":
    response = main()
    print(response)
"""
