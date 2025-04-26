import threading
import multiprocessing
import requests
import time
import matplotlib.pyplot as plt

picture_url = "https://disneyparksblog.com/app/uploads/2025/03/DX_SXSW-2025_Falcon-scaled.jpg"
def request_url():
    request = requests.get(picture_url)

if __name__ == "__main__":
    start1 = time.time()

    threads = []

    for i in range(2):
        thread = threading.Thread(target=request_url)
        threads.append(thread)
        thread.start()

    for i in threads:
        i.join()

    end1 = time.time()
    print("Time spent on multithreading: ", end1 - start1)


    start2 = time.time()
    processes = []

    for i in range(2):
        process = multiprocessing.Process(target=request_url)
        processes.append(process)
        process.start()

    for i in processes:
        i.join()

    end2 = time.time()
    print("Time spent on multiprocessing: ", end2 - start2)

    thread_time = end1 - start1
    process_time = end2 - start2

    times = [thread_time, process_time]
    labels = ["Threads", "Processes"]

    plt.bar(labels, times, color="blue", align="center", width=0.6)
    plt.show()