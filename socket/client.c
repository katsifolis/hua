#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/time.h>
#include <time.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <signal.h>
#include <errno.h>
#include <fcntl.h>

#define BUFFER_SIZE 2048
#define GAME_COUNTER 20

/* Macros */

#define COLOR_RESET	printf("\033[0m")
#define printb(...)	printf("\033[32m" __VA_ARGS__)
#define printr(...)	printf("\033[31m" __VA_ARGS__)
#define printm(...)	printf("\033[36m" __VA_ARGS__)

/* Function Declarations */
void error(const char *);
void sig_int(int);
void check_server(int);
int * game(int);


/* Globals */
int client_socket;
int game_counter;
	
void
error(const char *msg)
{
	fprintf(stderr, msg);
	exit(0);
}

void 
sig_int(int signum) 
{ 
	printf("\nCaught signal %d \n",signum);
		
	exit(signum);
}

void
check_server(int signum)
{
	char tmp[100];
	memset(tmp, '\0', sizeof(tmp));
	if (recv(client_socket, tmp, 100, MSG_DONTWAIT) == 0) {
			close(client_socket);
			error("Server Shutdown\n");
			exit(1);
	}
	return;
}

int *
game(int counter)
{
	int i;
	char tmp;
	char *game_vec = malloc(sizeof(1000));
	printf("Please pick a number from 0 - 20 %d times\n", counter);
	for (i = 0; i < counter; i++) {
		printf("Pick your number: "); 
		scanf("%c", &tmp);
		game_vec[i] = tmp;
	}
	return game_vec;

}

int 
main(int argc, char *argv[])
{
	/* Initializations */
	srand(time(NULL));
	int result,portno;
	struct sockaddr_in serverAddr;
	char buffer[BUFFER_SIZE];
	char game_vec[GAME_COUNTER];
	int readbytes;
	char tmp[100];

	signal(SIGINT, sig_int); 
	signal(SIGALRM, check_server); 

	/*
	 * Sets an alarm
	 * to check every (interval)
	 * if the server has shut-down
	 */
	struct itimerval timer;
	/* First expiration */
	timer.it_value.tv_sec = 0;
	timer.it_value.tv_usec = 500000;
	/* Interval (every then) */
	timer.it_interval.tv_sec = 0;
	timer.it_interval.tv_usec = 50000; /* in ms */
	setitimer (ITIMER_REAL, &timer, NULL);	

	/* Guard */
	if (argc < 3)
	{
		fprintf(stderr, "usage %s ip-address port\n", argv[0]);
		exit(0);
	}

	portno = atoi(argv[2]);
	/* Creates the socket */
	client_socket = socket(AF_INET, SOCK_STREAM, 0);
	if (client_socket < 0) {
		error("ERROR opening socket");
	}
	printb("Client socket is created.\n");
	COLOR_RESET;
	
	memset(&serverAddr, '\0', sizeof(serverAddr));

	/* Populating the serverAddr struct */
	serverAddr.sin_family = AF_INET;
	serverAddr.sin_addr.s_addr=inet_addr(argv[1]);
	serverAddr.sin_port = htons(portno);

	/* Finally conect to the server */
	result = connect(client_socket, (struct sockaddr *) &serverAddr, sizeof(serverAddr));
	if (result < 0) {
		error("ERROR connecting");
	}

	printb("Connected to server with ip address: \n");
	COLOR_RESET;

	/* main loop for the client */
	for (;;) { 
		printm("%s:>",argv[1]);
		COLOR_RESET;
		memset(buffer, '\0', BUFFER_SIZE); /* fill the buffer with 0 */
		fgets(buffer, BUFFER_SIZE - 1, stdin); /* get input */
		if (strcmp(buffer, "END\n") == 0) {
			char *game_vec = game(game_counter);
			printf("%d", game_vec);
			send(client_socket, game_vec, sizeof(game_vec), 0);
			close(client_socket);
		}
		send(client_socket, buffer, strlen(buffer), 0);
		if (strcmp(buffer, "END\n") == 0) {
			close(client_socket);
			printf("Disconnected from server %s \n",argv[1]);
			break;
		}
		if (strcmp(buffer, "\n") == 0) continue;
		
		/* blocks until a response comes from the server */
		readbytes = recv(client_socket, buffer, 7000, 0); 
		if (readbytes == 0) {
			close(client_socket);
			error("Server Shutdown\n");
			break;
		} else {
			game_counter++; /* Incrementing for each successful command */
			buffer[readbytes-1]='\0';  
			printr("Server:\n%s%d\n", buffer, game_counter);
			COLOR_RESET;
		}
	}
	return 0;
}
