import time
from threading import Condition, Thread
import concurrent.futures
from multiprocessing import cpu_count


def factorize(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors


def factorize_list_sync(numbers):
    result = []
    condition = Condition()

    def worker(num):
        with condition:
            factors = factorize(num)
            result.append(factors)
            condition.notify()

    threads = []
    for num in numbers:
        thread = Thread(target=worker, args=(num,))
        threads.append(thread)
        thread.start()

    with condition:
        condition.wait_for(lambda: len(result) == len(numbers))

    return result


def factorize_list_parallel(numbers):
    num_cores = cpu_count()
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_cores) as execut:
        result = list(execut.map(factorize, numbers))
    return result

if __name__ == '__main__':
    numbers_to_factorize = [128, 255, 99999, 10651060]

    start_time = time.time()
    result_sync = factorize_list_sync(numbers_to_factorize)
    end_time = time.time()
    execution_time_sync = end_time - start_time
    print("Синхронний час виконання:", execution_time_sync, "секунд")
    print("Результат синхронного виконання:")
    for result in result_sync:
        print(result)

    start_time = time.time()
    result_parallel = factorize_list_parallel(numbers_to_factorize)
    end_time = time.time()
    execution_time_parallel = end_time - start_time
    print("Паралельний час виконання:", execution_time_parallel, "секунд")
    print("Результат паралельного виконання:")
    for result in result_parallel:
        print(result)
