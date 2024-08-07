from q1_memory import main as q1_memory
from q1_time import main as q1_time

from q2_memory import main as q2_memory
from q2_time import main as q2_time

from q3_memory import main as q3_memory
from q3_time import main as q3_time

import gc

def main(request):
    gc.collect()
    request_json = request.get_json()
    if not request_json or 'message' not in request_json:
        return 'Please, insert parameters'

    function = request_json['message']
    file_path = request_json.get('file_path')

    options = {
        'q1_memory': q1_memory,
        'q1_time': q1_time,

        'q2_memory': q2_memory,
        'q2_time': q2_time,

        'q3_memory': q3_memory,
        'q3_time': q3_time        
    }

    process = options.get(function)
    if process:
        return process(file_path)
    return f"No valid process for {function}"

if __name__ == "__main__":
    print("Starting Function")
    main()
