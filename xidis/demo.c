#include "threads.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static unsigned count;
static int test= 2;

#define NUM_OF_THREADS 8

static void *
job1
(void *arg)
{
	if (((unsigned long) arg % 2) == 0) {
		return arg;
	} else { count += 1; }
}

int
main
(int argc, char * argv[])
{

	delay(200);
	printf("\tA user level thread library using ucontext..\n");
	delay(200);

	int threads[NUM_OF_THREADS];

	// Creating the threads //
	for (int i = 0; i < NUM_OF_THREADS; ++i) {
		void *arg = (void *) i;

		threads[i] = threads_create(job1, arg);
		if (threads[i] == -1 ) {
			perror("threads_create");
			exit(EXIT_FAILURE);
		}

	}

	for (unsigned long i = 0; i<NUM_OF_THREADS; ++i) {
		int id = threads[i];

	// Joining the threads // 
		while (1) {
			void *res;
			if (threads_join(id, &res) > 0) {
				printf("\tjoined thread %d with result %d\n", id, res);
				break;
			} 
		}
	}
	printf("\tglobal count var: %d\n", count);
}
