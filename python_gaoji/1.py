import time

def timing(func):
    starttime = time.time()
    def count():
        func()
        endtime = time.time()
        print("elapse:", endtime - starttime)
    return count

@timing
def start():
    print("run...")
    time.sleep(1)

while True:
    start()
