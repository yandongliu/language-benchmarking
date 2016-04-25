package main

import (
	"fmt"
	"net/http"
	"time"
)

func DoWork(num int, c chan int) {
	sum := 0
	for i := 1; i < num; i++ {
		sum += i
	}
	c <- sum
}

func statusHandler(w http.ResponseWriter, r *http.Request) {
	var nums = []int{
		10000,
		100000,
		1000000,
	}
	var c = make(chan int, len(nums))
	for _, num := range nums {
		go DoWork(num, c)
	}
	var count = 0
	for {
		select {
		case r := <-c:
			fmt.Fprintf(w, "%d", r)
			count++
			if count == len(nums) {
				return
			}
		case <-time.After(50 * time.Millisecond):
			fmt.Printf(".")
		}
	}

}

func main() {
	http.HandleFunc("/", statusHandler)
	http.ListenAndServe(":8080", nil)
}
