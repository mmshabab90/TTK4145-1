
#include <pthread.h>
#include <stdio.h>

int i = 0;


void* increment(void* mutex){
	int j;
  	for(j = 0; j < 1000000; j++){
		pthread_mutex_lock(mutex);	
		i++;
		pthread_mutex_unlock(mutex);
  	}
  	return NULL;
} 

void* decrement(void* mutex){
	int j;
  	for (j = 0; j < 1000000; j++){
		pthread_mutex_lock(mutex);
		i--;
		pthread_mutex_unlock(mutex);
  	}
  	return NULL;
}

int main(){

	pthread_mutex_t mutex;
	pthread_mutex_init(&mutex, NULL);
  	pthread_t inc;
  	pthread_t dec;

  	pthread_create(&inc, NULL, increment, (void*) &mutex);
  	pthread_create(&dec, NULL, decrement, (void*) &mutex);

  	pthread_join(inc, NULL);
  	pthread_join(dec, NULL);
  	printf("i: %d\n", i);

	pthread_mutex_destroy(&mutex);

  	return 0;
}
