import logging 
import grequests
import requests
from threading import Thread
from queue import Queue
from time import sleep
from urllib.parse import urljoin

from pydantic import HttpUrl,BaseModel
from pydantic.typing import List,Optional
from bs4 import BeautifulSoup,SoupStrainer


class UniqueQueue(Queue):
    
    def __init__(self):
        super().__init__()
        self.set = set()

    def add(self, url_obj):
        if not url_obj.url in self.set:
            self.put(url_obj)
            self.set.add(url_obj.url)


class UrlModel(BaseModel):
    url: str
    depth: Optional[int] = 0

class Worker(Thread):

    def __init__(self,worker_id:int,max_depth:int,
                    queue:UniqueQueue,count_endpoint:HttpUrl,workers_size:int,
                    max_retries:int=5,sleep_time:float=2.0):
        super().__init__()
        self.worker_id     = worker_id
        self.max_depth     = max_depth
        self.queue         = queue
        self.count_endpoint = count_endpoint
        self.max_retries  = max_retries
        self.sleep_time   = sleep_time
        self.workers_size = workers_size
    
    # Capture the urls from the current webpage
    def capture_urls(self,page:str,father_url:HttpUrl) -> List[str]:
        urls: List[str] = []
        # Avoid smart code (compressed loop)
        for link in BeautifulSoup(page,parse_only=SoupStrainer('a')):
            # Removing non link urls
            if link.has_attr('href') and link['href'].find('/') > -1:
                if link['href'].startswith('http'):
                    urls.append(link['href'])
                else:
                    urls.append(urljoin(father_url,link['href']))
        return list(set(urls))
    
    # Pull the next url obj from the queue
    def __pull_urls_obj(self) -> List[Optional[UrlModel]]:
        logging.info('Queue size %s',self.queue.qsize())
        size = min(int(self.queue.qsize()/self.workers_size)  + 1,500)
        return [self.queue.get() for _ in range(size) if self.queue.qsize() > 0]
    
    def __send_urls(self,urls: List[UrlModel]):
        for url_obj in urls:
            self.queue.add(url_obj)

    def __get_pages(self,urls:List[UrlModel]):
        responses = grequests.map([grequests.get(obj.url,timeout=3) for obj in urls])
        return [(rs.content,obj.depth,obj.url) for rs,obj in zip(responses,urls) if rs and rs.status_code == 200]

    def send_incremental(self,child_urls,n=100):
        # TODO separate this to another worker
        # Adding appearances values using the incremental api
        urls_calls = ['%s/%s'%(self.count_endpoint,url.url) for url in child_urls]
        size = 0
        for i in range(0, len(urls_calls), n):
            split_url = urls_calls[i:i + n]
            size = size + len(split_url)              
            with requests.Session() as s:
                grequests.map([grequests.put(url) for url in split_url])
                logging.info("Worker %s updated %s urls"%(self.worker_id,size))
  
  
    def run(self,retries = 0):
        logging.info('Worker %s spawed'%self.worker_id)
        i = 0
        while True:
            try:

                # Checking if there is urls in queue
                father_objs : List[UrlModel]  = self.__pull_urls_obj()
                logging.info("Worker %s Crawling %s urls",self.worker_id,len(father_objs))
                if not father_objs:
                    retries = retries + 1
                    logging.warning('Retry Happening for %s'%self.worker_id)
                    if retries > self.max_retries:
                        logging.warning('Worker %s stopped, no urls on queue'%self.worker_id)
                        break
                    sleep(self.sleep_time)
                    continue

                # Case where the depth is already on max
                father_objs = [obj for obj in father_objs if obj.depth + 1 < self.max_depth]
                if not father_objs:
                    continue

                contents = self.__get_pages(father_objs)
                child_urls = []
                for content,depth,father_url in contents:
                    tmp_urls = self.capture_urls(content,father_url)
                    child_urls.extend([UrlModel(url=url,depth=depth+1) for url in tmp_urls])

                if child_urls:
                    # Transforming the urls into  url objects avoiding bugs with http
                    self.__send_urls(child_urls)
                    # Update appearances count
                    self.send_incremental(child_urls=child_urls)
                retries = 0
            except Exception as error:
                logging.error(str(error))
        self.queue.task_done()