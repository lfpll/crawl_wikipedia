import pytest
import logging
from crawler.crawler import Worker,UrlModel,UniqueQueue
from queue import Queue
import responses
import pathlib
import os

CURRENT_PATH = os.path.dirname(__file__)
DATA_PATH    = CURRENT_PATH + '/data'
LOGGER = logging.getLogger(__name__)
INCREMENTAL_ENDPOINT = "http://incremental.com"

FILES = ['parent.html',
         'child1.html',
         'child2.html',
         'child3.html']


@pytest.fixture
def mock_requests():
    # Mocking Paths
    for file in FILES:
        url = 'http://test.com/%s'%file
        responses.add(responses.GET,url=url,
                        status=200,
                        body=open('%s/%s'%(DATA_PATH,file)).read())
        responses.add(responses.PUT,
                        url='%s/%s'%(INCREMENTAL_ENDPOINT,url))

                        
class TestCrawler:
    incremental_endpoint = INCREMENTAL_ENDPOINT

    def __start_queue(self,queue):
        while queue.qsize() > 0:
            queue.get()
        queue.add(UrlModel(url='http://test.com/parent.html'))
    
    @responses.activate
    def test_incremental(self,monkeypatch,mock_requests):
        urls_output = []
        queue = UniqueQueue() 
        self.__start_queue(queue)
        crawler = Worker(worker_id=1,max_depth=4,queue=queue,incremental_endpoint=self.incremental_endpoint,sleep_time=0,workers_size=1)  
        monkeypatch.setattr(crawler,'send_incremental',lambda child_urls: urls_output.extend(child_urls))
        
        # Trigger first url
        crawler.run()
        assert sorted([url.url for url in urls_output]) == ['http://test.com/child1.html', 'http://test.com/child2.html', 'http://test.com/child3.html','http://test.com/parent.html']


    def test_max_retries(self,caplog):
        with caplog.at_level(logging.WARNING):
            queue = UniqueQueue() 
            self.__start_queue(queue)
            crawler = Worker(worker_id=1,max_depth=1,queue=queue,incremental_endpoint=self.incremental_endpoint,sleep_time=0,max_retries=0,workers_size=1)
            crawler.run(retries=0)
            assert 'Worker 1 stopped, no urls on queue' in  caplog.text
