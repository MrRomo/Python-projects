from datetime import datetime

def excecution_time(func):
    def wraper(*args, **kwargs):
        start = datetime.now()
        func(*args, **kwargs)
        end = datetime.now()
        time_elapsed = end-start
        print(f'Tiempo de ejecucion: {time_elapsed.total_seconds()} (s)')
    return wraper

@excecution_time
def random_func():
    for _ in range(1, 1000000000):
        pass


if __name__ == '__main__':
    random_func()