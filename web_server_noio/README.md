## Request concurrency test:

 - start up a Web server
 - for each GET request, do some CPU work

This is to simulate when each request has no I/O dependency.

## Result:
|         | Median           | p90%  | p99% |
| ------------- |:-------------:| -----:| -----:|
| go | 112 | 166 | 238 |
| python/tornado | 1854 | 3314  | 11197 |
