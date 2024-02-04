import json

from liblibart.ql import ql_env

additionalNetwork = []
my_loras = ql_env.search("my_lora")
for my_lora in my_loras:
    if my_lora['status'] == 0:
        additionalNetwork.append(json.loads(my_lora['value']))
print(additionalNetwork)