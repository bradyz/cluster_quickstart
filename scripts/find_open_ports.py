import random
import socket

result = list()

for i in range(8000, 9000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(('127.0.0.1', i)) != 0:
            result.append(i)

print(random.choice(result))
