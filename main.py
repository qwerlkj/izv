import time

from download import DataDownloader

if __name__ == '__main__':
    dd = DataDownloader()
    starttime = time.time()
    data = dd.get_dict(["JHM", "MSK"])




