## Request concurrency test:

 - start up a Web server
 - for each GET request, fetch 3 urls

This is to simulate when each request has heavy I/O dependency.

## Result:

*100 connections with 20 concurrency: `ab -n 100 -c 20 http://localhost:8080/`*

|         | Median           | p90%  | p99% |
| ------------- |:-------------:| -----:| -----:|
| Async | 4013 | 4521 | 4945 |
| Sync | 8085 | 8390 | 8683 |
| Sync + Coroutine | 30422 | 31565 | 32665 |


*500 connections with 50 concurrency: `ab -n 500 -c 50 http://localhost:8080/`*

| | Median           | p90%  | p99% |
| ------------- |:-------------:| -----:| -----:|
| Async | 9131 | 9381 | 9894 |
| Sync | 21510 | 22215 | 22833 |
| Sync + Coroutine | 77701 | 79787 | 81497 |
