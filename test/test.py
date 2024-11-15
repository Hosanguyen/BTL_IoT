import time

print(time.time())
cur = time.time() 
time.sleep(10)

print(time.time() - cur)