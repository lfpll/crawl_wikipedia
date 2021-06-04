# This s a test project for a job interview

The idea is to create a crawler that will craw until N depth from the initial URL and store in a database.
Then it will generate some features based on that url

## V0.1

### Components:

- [Crud Api](apis/crud/crud_api.py) 
    - Incremental number of appearances of url
    - Insert url
    - Create url
    - Update url with features on the database
    - Get Url

- [ML Api](apis/crud/model_api.py)
    - Get results of appearances

- [Crawler](crawler/crawler.py) - Worker using threads
    - Capture the information from the pages
    - Add new urls to the queue
    - Increment the url appearances
    - Single workers no multiple async requests

## Architectural decisions

###  Apis

Using fastapi  because of perfomance, also isolating the database from direct connections because of componentization.

### Crawler

Using simple python code, language easy to prototype with internal queues that can be replaced for other queues like redis unique queues

### How to run

This code users docker-compose to conteinerize everything, simply:

    docker-compose build

Besides building the code also trian ml_model api using the sample in the folder, start the containers:

    docker-compose up

Then you can access the docker container which runs the crawler with:

    docker exec -i -t  <<id of the container>>

Replace the id of the container with the one of the crawler, run:

    python main.py

This will start running the code and crawling the url in the [crawler/crawler.py](crawler/main.py), to check the data you can use the fast api docks in

[Crud Api Swagger](http://27.0.0.1:80/docs)

[ML Api Swagger](http://127.0.0.1:90/docs)

The get endpoints of both are able to check for the urls being in the database.

## Conclussions

The crawler is slow right now mostly because the crud api which became hiccup, some possible solutions would be:

- Multiple urls being sended with a single post request
    - replace the query as one single Upsert query
    - replacing with  redis using incremental function
- Direct connection

## Possible Future improvements

1. change to incremental function of  upserts and multiple urls on incremental.
2. Replace UniqueQueue with a redis instance enabling multicontainers with multiple workers
3. Creating an supervisor to check the workers health
4. Proxy rotator to avoid ip blockage

Besides a some of code improvements like the structure of the model_api and crud_api.

P.S: lambda + Pubsub was not considered because of requirements of the project, I believe that would be the fastest and ideal solution for a small project like this.

## Assumptions

- This is a MVP fast-paced solution, it's for tests and there will be bugs possibly .
- Containeraziation was required.
- It's better to do calculations in the apis that in the crawler (Ex: adding columns to the urls)

## About the ML Model

### Features

- is_file: if the url is a file
- percent_of_letters_path: percentage of letters in path 
- percent_of_numbers_path: percentage of numbers in path
- path_length: length of path
- last_path_length: length of last path example: /wiki/Pokemon -> Length(Pokemon)
- full_lengh: length of the whole url 
- is_arabic: if url has arabic digits
- number_of_subpaths: subpaths existent in path
- related_original_url: if it's related to the original url (It's on the model, in this case wikipedia)
- domain_length: Length of the domain


## Current Architecture

![Architecthure V0.1](/architecture.png)