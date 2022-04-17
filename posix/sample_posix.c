#include <stdio.h>
#include <pthread.h>
#include <time.h>

static const int NUM_THREADS = 9;

static void func_thread(void) {
	pthread_t tid;
	struct timespec time;

	tid = pthread_self();

	clock_gettime(CLOCK_MONOTONIC, &time);
	/* printf is thread safe */
	/* printf("thread start: %x sec=%ld nsec=%ld\n", (unsigned int)tid, time.tv_sec,time.tv_nsec); */
	printf("%x,TS_Start,%ld\n", (unsigned int)tid,time.tv_nsec);

	/* for (int i = 0; i < 0xFFFF; i++) { } */

	clock_gettime(CLOCK_MONOTONIC, &time);
	/* printf("thread   end: %x sec=%ld nsec=%ld\n", (unsigned int)tid, time.tv_sec,time.tv_nsec); */
	printf("%x,TS_End,%ld\n", (unsigned int)tid,time.tv_nsec);
}

int main(void) {
	pthread_t thread[NUM_THREADS];
	int ret;
	int i;

	for (i = 0; i < NUM_THREADS; i++) {
		ret = pthread_create(&thread[i],NULL,(void *)func_thread,NULL);
		if (ret != 0) {
			printf("failed to create thread %d.\n", i);
		}
	}


	for (i = 0; i < NUM_THREADS; i++) {
		ret = pthread_join(thread[i], NULL);
		if (ret != 0) {
			printf("failed to join thread %d.\n", i);
		}
	}

	return 0;
}
