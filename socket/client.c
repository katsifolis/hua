#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <time.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <signal.h>
#include <errno.h>

#define BUFFER_SIZE 2048

/* Macros */
#define COLOR_RESET	printf("\033[0m")
#define printb(...)	printf("\033[32m" __VA_ARGS__)
#define printr(...)	printf("\033[31m" __VA_ARGS__)
#define printm(...)	printf("\033[36m" __VA_ARGS__)

void
error(const char *msg)
{
	fprintf(stderr, msg);
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
	srand(time(NULL));
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
	printb("Client socket is created.\n");
	COLOR_RESET;
	

	memset(&serverAddr, '\0', sizeof(serverAddr));
	serverAddr.sin_family = AF_INET;
	serverAddr.sin_addr.s_addr=inet_addr(argv[1]);
	serverAddr.sin_port = htons(portno);

	result = connect(clientSocket, (struct sockaddr *) &serverAddr, sizeof(serverAddr));
	if (result < 0) {
		error("ERROR connecting");
	}

	printb("Connected to server with ip address: \n");
	COLOR_RESET;
	

	while (1) { 
		int flag;
		printm("%s:>",argv[1]);
		COLOR_RESET;
		memset(buffer, '\0', BUFFER_SIZE);
		fgets(buffer, BUFFER_SIZE - 1, stdin); 
		flag = write(clientSocket, buffer, strlen(buffer));
		//send(clientSocket, buffer, strlen(buffer), MSG_NOSIGNAL);
		printf("%d\n", flag);
		printf("%d\n", errno);
		if (strcmp(buffer, "END\n") == 0) {
			close(clientSocket);
			printf("Disconnected from server %s \n",argv[1]);
			break;
		}
	   	if (strcmp(buffer, "\n") == 0) continue;
	   	
		readbytes = recv(clientSocket, buffer, 7000, 0);
		if (readbytes == 0) {
			close(clientSocket);
			error("Server Shutdown\n");
			break;
		} else {
			buffer[readbytes-1]='\0'; 
			printr("Server:\n%s\n", buffer);
			COLOR_RESET;
		}
	}
	return 0;
}
