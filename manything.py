import random

from multiprocessing import Pool
from time import time_ns


def is_prinme(num):
    flag = True
    for i in range(2,num//2):
        if num % i == 0:
            flag = False
    return flag

data = [random.randint(1000,1000000) for i in range(256)]

if __name__ == '__main__':
    start = time_ns()
    with Pool(3) as p:
        answers = p.imap(is_prinme, data)

    print(answers)
    end = time_ns()

    print((end - start) / 1000000000)