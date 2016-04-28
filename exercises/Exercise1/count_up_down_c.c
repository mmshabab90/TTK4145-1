

#include <pthread.h>
#include <stdio.h>

int i = 0;


void* increment(){
  for(int j = 0; j < 1000000; j++){
    i++;
  }
  return NULL;
} 

void* decrement(){
  for (int j = 0; j < 1000000; j++){
    i--;
  }
  return NULL;
}

int main(){
  pthread_t inc;
  pthread_t dec;

  pthread_create(&inc, NULL, increment, NULL);
  pthread_create(&dec, NULL, decrement, NULL);

  pthread_join(inc, NULL);
  pthread_join(dec, NULL);
  printf("i: %d\n", i);
  return 0;
}

