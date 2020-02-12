#include "threads.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void *magic = NULL;
static unsigned count;
static int test= 2;

#define NUM_OF_THREADS 8

static void *
job1
(void *arg)
{
	if (((unsigned long) arg % 2) == 0) {
		return arg;
	} else { count = 1; }
}
/*
 * 1. Opens the files
 * 2. Searches for pending workloads
 * 3. Executes the jobs
 */

void 
init
(char *arg) {

	char *buffer			= NULL;
	char * line				= NULL;
	int length				= 0;
	int arg1				= 0;
	size_t len				= 0;
	ssize_t read			= 0;
	FILE *f					= fopen(arg, "r");
	void (*job_ptr)(int)	= &job1;

	
	if (f == NULL) {
		printf("Can't open the file\n");
		exit(EXIT_FAILURE);
	}
	
	// Determing file's size
	fseek (f, 0, SEEK_END);
	length = ftell(f);
	fseek (f, 0, SEEK_SET);
	buffer = malloc (length);

	// Getting the lines from the wordlist and running the jobs //
	while ((read = getline(&line, &len, f)) != -1) {
		char *str = strtok(line, " ");
		while (str != NULL) {
			if ((strcmp(str, "job")) == 0) {
				str = strtok(NULL, " ");
				arg1 = atoi(str);
			} else {
				str = strtok(NULL, " ");
			}
		}

		str = NULL;
	}

 	fclose (f);
}

int
main
(int argc, char * argv[])
{
	// Guard 
    if (argc < 2) {
		printf("file not given\n");
		exit(1);
	}

   	strcpy(buff, argv[1]);
    init(buff);
    char buff[10] = {0}; // filename buff

	int threads[NUM_OF_THREADS];

	// Creating the threads //
	for (int i = 0; i < 8; ++i) {
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
				printf("joined thread %d with result %d\n", id, res);
				break;
			} 
		}
	}
	printf("%lu \n", count);
}
