from crawler import Worker,UrlModel,UniqueQueue
from queue import Queue
from time import sleep
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    queue= UniqueQueue()
    queue.put(UrlModel(url="https://pt.wikipedia.org/w/index.php?title=Plan_B&oldid=61288281"))
    for x in range(1):
        crawler = Worker(x,max_depth=4,queue=queue,
            count_endpoint="http://127.0.0.1:80/url/increment",sleep_time=5,workers_size=4)
        
        crawler.daemon = True
        crawler.start()
    queue.join()

