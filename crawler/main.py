from crawler import Worker,UrlModel,UniqueQueue
import logging
import os
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    end_point = os.environ["ENDPOINT_URL"]
    queue= UniqueQueue()
    queue.put(UrlModel(url="https://pt.wikipedia.org/w/index.php?title=Plan_B&oldid=61288281"))
    for x in range(1):
        crawler = Worker(x,max_depth=4,queue=queue,
            count_endpoint=end_point,sleep_time=5,workers_size=4)
        
        crawler.daemon = True
        crawler.start()
    queue.join()

