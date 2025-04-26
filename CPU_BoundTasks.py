import threading
from multiprocessing import shared_memory, Pool
import time
import numpy as np
import matplotlib.pyplot as plt

a1 = np.random.randint(100, size=(2000, 2000))
a2 = np.random.randint(100, size=(2000, 2000))

def multiply_thread(index, result, row):
    result[index] = row @ a2

def multiply_process(args):
    index, row, shm_name = args
    shm = shared_memory.SharedMemory(name=shm_name)
    a2_shared = np.ndarray((2000, 2000), dtype=np.int32, buffer=shm.buf)
    result = row @ a2_shared
    shm.close()
    return (index, result)

if __name__ == "__main__":
    start1 = time.time()
    results_t = [None] * 2000
    threads = []

    for i in range(2000):
        arow = a1[i]
        thread = threading.Thread(target=multiply_thread, args=(i, results_t, arow))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end1 = time.time()
    print("Time spent on multithreading: ", end1 - start1)

    shm = shared_memory.SharedMemory(create=True, size=a2.nbytes)
    shm_array = np.ndarray((2000, 2000), dtype=np.int32, buffer=shm.buf)
    shm_array[:] = a2

    start2 = time.time()
    args_list = [(i, a1[i], shm.name) for i in range(2000)]

    with Pool() as pool:
        results = pool.map(multiply_process, args_list)

    results_p = [None] * 2000
    for index, value in results:
        results_p[index] = value

    end2 = time.time()
    print("Time spent on multiprocessing (pool):", end2 - start2)

    thread_time = end1 - start1
    process_time = end2 - start2

    times = [thread_time, process_time]
    labels = ["Threads", "Processes"]

    plt.bar(labels, times, color="gray", align="center", width=0.6)
    plt.show()

    shm.close()
    shm.unlink()
