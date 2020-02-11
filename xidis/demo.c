#include "threads.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void *magic = NULL;
static unsigned count;
static int test;

static void *thread0(void *arg)
{
    for (;;) {
		if (magic != arg) {
			printf("Hello, this is thread %lu with count %u.\n", (unsigned long) arg, count);
			magic = arg;
			count += 1;
		}
    }

    return NULL;
}

static void *thread1(void *arg)
{
    if ((unsigned long) arg % 2 == 0) {
		return arg;
    } else { for (;;) { } }

}

void j(int a) {

	int test;

	for (int i = 0; i < 1000; i++) {
		test = test + i + (test % 2 * i);
	}

	return;
}

void print_menu(char *arg) {

	char *buffer;
	int length;
	FILE *f = fopen(arg, "r");
	char * line = NULL;
    size_t len = 0;
    ssize_t read;
	void (*j_ptr)(int) = &j;
	int arg1;

	
	if (f == NULL) {
		printf("Can't find file\n");
		exit(EXIT_FAILURE);
	}
	
	fseek (f, 0, SEEK_END);
	length = ftell(f);
	fseek (f, 0, SEEK_SET);
	buffer = malloc (length);

	while ( (read = getline(&line, &len, f)) != -1) {
		char *str = strtok(line, " ");
		printf("%s\n", str);
		while (str != NULL) {
			if ((strcmp(str, "j")) == 0) {
				str = strtok(NULL, " ");
				printf("%s\n", str);
				arg1 = atoi(str);
				printf("%d\n", arg1);
			} else {
				str = strtok(NULL, " ");
			}
		}
		str = NULL;
	}
 	fclose (f);
}

int main(int argc, char * argv[])
{
    if (argc < 2) {
		printf("file not given\n");
		exit(1);
	}
    puts("Hello, this is main().");

    char buff[10] = {0};
   	strcpy(buff, argv[1]);

    print_menu(buff);

	for (unsigned long i = 0; i < 12; ++i) {
		void *arg = (void *) i;

		if (threads_create(thread0, arg) == -1) {
			perror("threads_create");
			exit(EXIT_FAILURE);
		}
	}

    for (;;) {
		if (magic != 0x0) {
			puts("Hello, this is main().");
			magic = 0x0;
		}
    }

    int threads[12];

    for (unsigned long i = 0; i < 12; ++i) {
		void *arg = (void *) i;

		if ((threads[i] = threads_create(thread1, arg)) == -1) {
			perror("threads_create");
			exit(EXIT_FAILURE);
		}
    }
/*
    for (int i = 0; i < 8; ++i) {
		int id = threads[i];

		while (1) {
			void *res;

			if (threads_join(id, &res) > 0) {
				printf("joined thread %d with result %p\n", id, res);
				break;
			}
			printf("joined thread %d with result %p\n", id, res);
		}
    }
	*/
}
