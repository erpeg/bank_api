# Fill Allocation API

## Summary

This Microservice app consists of 4 apps:

* Fill Server - responsible for sending information what stocks should be bought in what amount
    * Servers are sending information in random time intervals (for presentation purposes I have done 0-10 s range)
    * Number of running servers at the same time can be specified in /fill_server/main.py file
* AUM Server - responsible for sending informaiton how stocks should be distributed
    * Server is sending information every 30 s
* Controller Server - responsible for receiving information from Fill Servers and AUM Servers
    * Whole logic is applied in this app
    * Controller Server decides what stock should be bought by what account, to minimize variance of stocks held by each account, to converge to distribution provided by AUM Server
    * Every 10 seconds Controller Server is sending current state of stocks to Position Server
* Position Server - server responsible for printing out to standard output results coming from Controller Server

## Requirements

Application has been built based on FastAPI and Uvicorn

## Setup

Docker image has not been setup yet - it is in future plans as next implementation.

Currently to setup file below commands need to be run, each app should be run in separate cmd/terminal window with activatet venv:

### Windows
```
python.exe -m venv -venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```
CMD window #1 - Position Server
```
uvicorn position_server.main:app --reload
```

CMD window #2 - Controller Server
```
uvicorn controller.main:app --reload
```

CMD window #3 - AUM Server
```
python.exe .\aum_server\main.py
```

CMD window #4 - Fill Server
```
python.exe .\fill_server\main.py
```


### Linux
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Terminal window #1 - Position Server
```
uvicorn position_server.main:app --reload
```

Terminal window #2 - Controller Server
```
uvicorn controller.main:app --reload
```

Terminal window #3 - AUM Server
```
python3 ./aum_server/main.py
```

Terminal window #4 - Fill Server
```
python.exe ./fill_server/main.py
```

After turning all applications, in Position Server terminal, we should have printed out data of splitted stocks.

## Splitting Algorithm and Heurestics - My assumptions

In order to implement multiple servers sending requests to Controller Server, Multithreading has been applied.

I was considering taking two approaches in matter of deciding how new fill ticks should be processed.

Algorithm that has been applied here is processing each stock synchronically. For each new fill request that is processed, quantity of stocks is iterated and decision which account should be incremented by one is tested during every iteration. In order to derive what account should be granted new stock, normalizaiton of data has been used.

Advantages of this approach:
* The most up-to-date state is sent to Position Server
* Quantity is distributed in the most fair way
* In the future it is easier to implement Celery

Disadvantages:
* In situation of higher values of quantities, iteration one by one can slow down processing of newly added tasks to queue

Second approach I was considering was to merge all fill requests coming to the queue every ~ 9 seconds (1 second prior sending information to Position Server) and performing calculations splitting all stocks fairly.

Advantages of this approach:
* Less computing demanding

Disadvantages:
* In case computation takes longer than 1 minute, information to Position Server can be outdated
* New fill tasks coming to Contoller after 9th second won't be processed in this sending batch to Position server

I have decided to take 1st approach due to futer possibility of applyingg RabbitMQ/Redis with Celery worker, since Celery relies on queueing services.


