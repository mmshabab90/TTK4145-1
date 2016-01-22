from threading import Thread, Lock

i=0



def thread_1(lock):
        global i
        for p in range(1000000):
		lock.acquire(True)                
		i += 1
		lock.release()

def thread_2(lock):
        global i
        for p in range(1000000):
                lock.acquire(True)
		i -= 1
		lock.release()



def main():
	lock = Lock()
	inc = Thread(target = thread_1, args = (lock,))
	dec = Thread(target = thread_2, args = (lock,))
	inc.start()
	dec.start()
	inc.join()
	dec.join()
	print(i)
	
main()
