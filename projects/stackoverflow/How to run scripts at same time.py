from time import sleep
import multiprocessing as mp

cpu_count = mp.cpu_count()
print(cpu_count)


def bot1(num):
    sleep(2)
    print(f'This is bot1, num: {num}')


def bot2():
    sleep(2)
    print('This is bot2')


if __name__ == '__main__':
    process_list = []
    for i in range(5):
        process_list.append(mp.Process(target=bot1, args=(i,)))
    process_list.append(mp.Process(target=bot2))

    for p in process_list:
        p.start()
    for p in process_list:
        p.join()
