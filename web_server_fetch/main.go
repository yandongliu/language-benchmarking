package main

import (
	"fmt"
	"net/http"
	"time"
)

func checkStatus(url string, c chan int) {
	resp, err := http.Get(url)
	defer resp.Body.Close()
	if err != nil {
		c <- 400
	} else {
		c <- resp.StatusCode
	}
}

var requestCnt int

func statusHandler(w http.ResponseWriter, r *http.Request) {
	requestCnt++
	fmt.Printf("%d: %s\n", requestCnt, r.RemoteAddr)
	var urls = []string{
		"http://google.com",
		"http://wikipedia.org",
		"http://amazon.com",
	}
	var c = make(chan int, len(urls))
	for _, url := range urls {
		go checkStatus(url, c)
	}
	var count = 0
	for {
		select {
		case r := <-c:
			fmt.Fprintf(w, "%d", r)
			count++
			if count == len(urls) {
				return
			}
		case <-time.After(50 * time.Millisecond):
			fmt.Printf(".")
		}
	}

}

func main() {
	requestCnt = 0
	http.HandleFunc("/", statusHandler)
	http.ListenAndServe(":8080", nil)
}
