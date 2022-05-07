package main

import (
	"fmt"
	"time"
)

func func_goroutine(id int, quit chan bool) {
	// fmt.Println("go routine")

	startTime := time.Now()
	fmt.Println(id, ",TS_Start,", startTime.UnixNano())
	for i := 0; i < 5; i++ {
		time.Sleep(100 * time.Millisecond)
	}
	endTime := time.Now()
	fmt.Println(id, ",TS_End,", endTime.UnixNano())
	quit <- true
}

func main() {
	quit := make(chan bool)
	for i := 0; i < 9; i++ {
		go func_goroutine(i, quit)
	}
	<-quit
	time.Sleep(1000 * time.Millisecond)
}
