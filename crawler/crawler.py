from threading import Thread
from queue import Queue
import logging 

from pydantic import HttpUrl,BaseModel
from pydantic.typing import List,Optional
from bs4 import BeautifulSoup,SoupStrainer

import requests
import grequests

class UrlModel(BaseModel):
    url: HttpUrl
    depth: int = 0
    past_urls: List[HttpUrl] = []

class Worker(Thread):

    def __init__(self,worker_id:int,max_depth:int,
                    queue:Queue,incremental_endpoint:HttpUrl):
        super().__init__()
        self.worker_id     = worker_id
        self.max_depth     = max_depth
        self.queue         = queue
        self.incremental_endpoint = incremental_endpoint
    
    # Capture the urls from the current webpage
    def __capture_urls(self,page:str) -> List[HttpUrl]:
        urls = []
        # Avoid smart code (compressed loop)
        for link in BeautifulSoup(page,parse_only=SoupStrainer('a')):
            if link.has_attr('href'):
                urls.append(link['href'])
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
            logging.error('Worker %s stopped because of %s'%(self.worker_id,str(error)))
            raise error
        return response.content

  
    def run(self):
        logging.info('Worker %s spawed'%worker_id)
        while not Queue.empty():
            # If multiple async workers the while condition may not be enough
            father_obj : Optional[UrlModel]  = self.__pull_url()
            if not father_obj:
                logging.info('Worker %s stoped, no more urls'%self.worker_id)
                break
            
            # Case where the depth is already on max
            if father_url.depth + 1 > self.max_depth:
                logging.info('Max depth reached on  %s with %s'%(father.url,self.worker_id))
                continue

            content: bytes = self.__get_page(father_obj.url)
            child_urls: List[HttpUrl] = self.__capture_urls(content)

            # TODO separate this to another worker
            # Adding appearances values using the incremental api
            http_session = requests.Session()
            retries = Retry(total=5, backoff_factor=0.2, status_forcelist=[500, 502, 503, 504], raise_on_redirect=True,
                    raise_on_status=True)
            http_session.mount('http://', HTTPAdapter(max_retries=retries))
            http_session.mount('https://', HTTPAdapter(max_retries=retries))
            grequests.map([grequests.put('%s/%s'%(self.incremental_endpoint,url),
                                        session=http_session)
                             for url in child_urls])
            
            # Creating the list of pastUrls
            past_urls: List[HttpUrl] = [father_obj.past_urls,father_obj.url]

            # Transforming the urls into  url objects
            urls_objs: List[UrlModel] =  [UrlModel(url=url,
                                            depth=father_obj.depth +1,
                                            past_urls=past_urls) 
                                            for url in child_urls
                                            if url not in past_urls]
            
            self.__send_urls(urls_objs)
            
            
            