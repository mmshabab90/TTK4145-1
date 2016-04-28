package main

import (
	"fmt"
	"runtime"
	"time"
)

var i int = 0

func increment(sema chan int, finished chan bool){
	for j := 0; j < 1000000; j++ {
		local := <-sema
		local++
		i = local
		sema <- local
    	}
	finished <- true	
}

func decrement(sema chan int, finished chan bool){
	for j := 0; j < 1000000; j++ {
		local := <- sema
		local--
    		i = local
		sema <- local
    	}
	finished <- true
}

func main() {
	runtime.GOMAXPROCS(runtime.NumCPU())
	
	sema := make(chan int, 1)
	sema <- i
	
	finished := make(chan bool, 1)
	
	go increment(sema, finished)
	go decrement(sema, finished)

	<-finished
	<-finished
	
	time.Sleep(100*time.Millisecond)
	fmt.Printf("i: %d\n", i)

}
