import logging 
import grequests
import requests
from threading import Thread
from queue import Queue
from time import sleep
from urllib.parse import urljoin

from pydantic import HttpUrl,BaseModel
from pydantic.typing import List,Optional,Union
from bs4 import BeautifulSoup,SoupStrainer


class UrlModel(BaseModel):
    url: str
    depth: Optional[int] = 0
    past_urls: Optional[List] = []

class Worker(Thread):

    def __init__(self,worker_id:int,max_depth:int,
                    queue:Queue,incremental_endpoint:HttpUrl,max_retries:int=5,sleep_time:float=2.0):
        super().__init__()
        self.worker_id     = worker_id
        self.max_depth     = max_depth
        self.queue         = queue
        self.incremental_endpoint = incremental_endpoint
        self.max_retries  = max_retries
        self.sleep_time   = sleep_time
        
    
    # Capture the urls from the current webpage
    def capture_urls(self,page:str,father_url:HttpUrl) -> List[HttpUrl]:
        urls: List[HttpUrl] = []
        # Avoid smart code (compressed loop)
        for link in BeautifulSoup(page,parse_only=SoupStrainer('a')):
            # Removing non link urls
            if link.has_attr('href') and link['href'].find('/') -1:
                if link['href'].startswith('http'):
                    urls.append(link['href'])
                else:
                    urls.append(urljoin(father_url,link['href']))
        return urls
    
    # Pull the next url obj from the queue
    def __pull_url_obj(self) -> Optional[UrlModel]:
        if not self.queue.empty():
            return self.queue.get()
        return None
    
    def __send_urls(self,urls: List[UrlModel]):
        for url_obj in urls:
            self.queue.put(url_obj)

    def __get_page(self,url:HttpUrl) -> bytes:
        try:
            response = requests.get(url)
            response.raise_for_status()
        except Exception as error:
            logging.error('Worker %s stopped on %s because of %s'%
                                    (self.worker_id,url,str(error)))
            raise error
        return response.content

    def send_incremental(self,child_urls):
        # TODO separate this to another worker
        # Adding appearances values using the incremental api
        urls_calls = ['%s/%s'%(self.incremental_endpoint,url) for url in child_urls]
        grequests.map([grequests.put(url) for url in urls_calls])
  
    def run(self,retries = 0):
        logging.info('Worker %s spawed'%self.worker_id)
        i = 0
        while True:
            
            # Checking if there is urls in queue
            father_obj : Optional[UrlModel]  = self.__pull_url_obj()
            if not father_obj:
                retries = retries + 1
                logging.warning('Retry Happening')
                if retries > self.max_retries:
                    logging.warning('Worker %s stopped, no urls on queue'%self.worker_id)
                    break
                sleep(self.sleep_time)
                continue

            logging.info('Crawling %s'%father_obj.url)
            # Case where the depth is already on max
            if father_obj.depth + 1 > self.max_depth:
                logging.info('Max depth reached on worker %s with %s'%(father_obj.url,self.worker_id))
                continue

            content: bytes = self.__get_page(father_obj.url)
            child_urls: List[HttpUrl] = list(set(self.capture_urls(content,father_obj.url)))
            if child_urls:
                # Creating the list of pastUrls
                father_obj.past_urls.append(father_obj.url)
                # Transforming the urls into  url objects
                urls_objs =  [UrlModel(url=url,depth=father_obj.depth + 1, past_urls=list(set(father_obj.past_urls)))
                                                for url in child_urls
                                                if url not in father_obj.past_urls and url.find('http') > - 1]
                self.__send_urls(urls_objs)
                # Update appearances count
                # self.send_incremental(child_urls=child_urls)
                logging.info('go next')
            retries = 0
        self.queue.task_done()
        