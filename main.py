import time

from download import DataDownloader

if __name__ == '__main__':
    dd = DataDownloader()
    #dd.download_data()
    #dd.parse_region_data('PLK')
    #exit()
    starttime = time.time()
    dict = dd.get_dict()

    print("TIME ", time.time() - starttime)

    print(dict)


