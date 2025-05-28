import numpy as np
import matplotlib.pyplot as plt
import time
from math import sqrt, pi


def classical_search(database, target):
    for i in range(len(database)):
        if database[i] == target:
            return i
    return -1


def grover_algorithm(database, target):
    n = len(database)
    if n == 0:
        return -1

    iterations = int((pi / 4) * sqrt(n))

    for _ in range(iterations):
        idx = classical_search(database, target)
        if idx != -1:
            return idx
    return -1


def timed_run(func, database, target, repeats=10):
    total_time = 0
    for _ in range(repeats):
        start = time.perf_counter()
        func(database, target)
        total_time += time.perf_counter() - start
    return total_time / repeats


def compare_performance(max_elements=10000, step=1000, repeats=10):
    classical_times = []
    quantum_times = []
    sizes = list(range(1, max_elements + 1, step))

    for size in sizes:
        database = np.random.randint(0, 100000, size)
        target = database[-1]  # همیشه عضو موجود انتخاب می‌کنیم

        # میانگین زمان اجرای جستجوی کلاسیک
        t_classic = timed_run(classical_search, database, target, repeats=repeats)
        classical_times.append(t_classic)

        # میانگین زمان اجرای شبیه‌سازی گروور
        t_grover = timed_run(grover_algorithm, database, target, repeats=repeats)
        quantum_times.append(t_grover)

    # رسم نمودار
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, classical_times, label='classic search', marker='o')
    plt.plot(sizes, quantum_times, label='Grover algorithm (شبیه‌سازی)', marker='s')
    plt.xlabel('size of DB')
    plt.ylabel('average runtime (sec)')
    plt.title('مقایسه عملکرد جستجوی کلاسیک و الگوریتم گروور (میانگین زمان)')
    plt.legend()
    plt.grid(True)
    plt.show()


# اجرای تابع
compare_performance(max_elements=10000, step=1000, repeats=20)
