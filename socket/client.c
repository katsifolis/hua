#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <signal.h>

#define BUFFER_SIZE 2048

/* COLORS */
#define printb(...)	printf("\033[32m" __VA_ARGS__)
#define printr(...)	printf("\033[31m" __VA_ARGS__)
#define printm(...)	printf("\033[36m" __VA_ARGS__)
#define COLOR_RESET	printf("\033[0m")

void
error(const char *msg)
{
	perror(msg);
	exit(0);
}

void 
signalhandler(int signum) 
{ 
	printf("\nCaught signal %d \n",signum);
	exit(signum);
}


int 
main(int argc, char *argv[])
{
	/* Initializations */
	int clientSocket,result,portno;
	struct sockaddr_in serverAddr;
	char buffer[BUFFER_SIZE];
	int readbytes;

	signal(SIGINT,signalhandler); 
	
	/* Guard */
	if (argc < 3)
	{
		fprintf(stderr, "usage %s ip-address port\n", argv[0]);
		exit(0);
	}

	portno = atoi(argv[2]);
	
	clientSocket = socket(AF_INET, SOCK_STREAM, 0);
	if (clientSocket < 0) {
		error("ERROR opening socket");
	}
	printf("Client socket is created.\n");
	

	memset(&serverAddr, '\0', sizeof(serverAddr));
	serverAddr.sin_family = AF_INET;
	serverAddr.sin_addr.s_addr=inet_addr(argv[1]);
	serverAddr.sin_port = htons(portno);

	result = connect(clientSocket, (struct sockaddr *) &serverAddr, sizeof(serverAddr));
	if (result < 0) {
		error("ERROR connecting");
	}

	printm("Connected to server with ip address: \n");
	COLOR_RESET;
	

	while (1) { 
		printr("%s:>",argv[1]);
		COLOR_RESET;
		memset(buffer, '\0', BUFFER_SIZE);
		fgets(buffer, BUFFER_SIZE - 1, stdin); 
		send(clientSocket, buffer, strlen(buffer), 0);

		if (strcmp(buffer, "quit\n") == 0) { 
			close(clientSocket);
			printf("Disconnected from server %s \n",argv[1]);
			break;
		} else if (strcmp(buffer, "\n") == 0) { /* ignoring the \r */
			continue;
		}

		readbytes=recv(clientSocket,buffer,7000,0);
		if (readbytes < 0) {
			printf("Error in receiving message \n");
		} else if (readbytes==-1) {
			close(clientSocket);
			printf("Disconnected from server \n");
			break;
		} else {
			buffer[readbytes-1]='\0'; 
			printf("Server:\n%s\n", buffer);
		}
	}
	return 0;
}
