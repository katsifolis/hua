#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#define BUFFER_SIZE 4


int
main()
{
	char *test = malloc(sizeof(BUFFER_SIZE));
	memset(test, '1', BUFFER_SIZE);
	printf("%d", sizeof(test));

	int i = 0;
	while(test[i] != '\0') {
		printf("%c", test[i]);
		i++;
	}
			

	return 0;
}
