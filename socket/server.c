#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <signal.h>
#include <ctype.h>

#define BUFFER_SIZE 2048
#define QUIT 127

/* COLORS */
#define printb(...)	printf("\033[32m" __VA_ARGS__)
#define printr(...)	printf("\033[31m" __VA_ARGS__)
#define printm(...)	printf("\033[36m" __VA_ARGS__)
#define COLOR_RESET	printf("\033[0m")

void 
error(const char *msg)
{
	perror(msg);
	exit(1);
}

void
signalhandler(int signum)
{ 
	printf("\nCaught signal %d \n",signum);
	exit(signum);
}

void 
check_child_exit(int status)
{ 
	if(WIFEXITED(status)) {
		printf("Child ended normally. Exit code is %d\n",WEXITSTATUS(status));
	} else if (WIFSTOPPED(status)) {
		printf("Child ended because of an uncaught signal, signal = %d\n",WTERMSIG(status));
	} else if (WIFSTOPPED(status)) {
		printf("Child process has stopped, signal code = %d\n",WSTOPSIG(status));
	}
	exit(EXIT_SUCCESS);
}

/* Parses the command sent by the client */
char 
parse(char *vec[10], char *line)
{
	int i;
	char *pch = malloc(sizeof(line));
	if(strstr(line,"|")) {
		printf("Found pipe\n");
		pch = strtok(line, "|");
		i=0;
		while (pch != NULL) {
			vec[i]=pch;
			pch = strtok (NULL, "|");
			i++;
		}
	} else {

		pch = strtok (line," \n"); 
		i=0;
		while (pch != NULL) {
			vec[i]=pch;
			pch = strtok (NULL, " \n");
			i++;
		}
		
		vec[i]='\0';
	}
	printf("%s\n", vec);

	return 0;
}

void 
runpipe(int pfd[],int socket,char *typedcommand)
{  
	char* vec[10];
	char* comands[3];
	parse(comands,typedcommand); 
	int pid;
	switch(pid=fork()){
		/* child */
		case 0: 
			parse(vec,comands[1]); // ανάλυση για την εντολή 2
			dup2(pfd[0],0);
			dup2(socket,1);
			dup2(socket,2);
			close(pfd[1]);
			/*the child does not need this end of
				the pipe*/
			execvp(vec[0],vec);
			perror(vec[0]);
			exit(1);

		/* parent */
		default: 
			parse(vec,comands[0]); 
			dup2(pfd[1],1);
			close(pfd[0]);
			execvp(vec[0],vec);
			perror(vec[0]);
			exit(1);
		case -1:
			perror("fork");
			exit(1);
	}


}

int 
main(int argc, char *argv[])
{
	int sockfd, newsockfd, portno;
	socklen_t clilen;
	char buffer[BUFFER_SIZE]; 
	struct sockaddr_in serv_addr, cli_addr;
	int n;
	char str[INET_ADDRSTRLEN];
	pid_t childpid;
	int pid,status;
	char *vec[10];
	size_t bufsize = 32;
	size_t characters;

	/* Signal Contoller */
	signal(SIGINT,signalhandler); 

	if (argc < 2) {
		fprintf(stderr, "No port provided\n");
		exit(1);
	}

	/* Socket Creation */
	if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
		error("ERROR opening socket");
	}
	printf("Server socket is created.\n");


	memset((char *)&serv_addr, '\0', sizeof(serv_addr));
	portno = atoi(argv[1]);
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = INADDR_ANY;
	serv_addr.sin_port = htons(portno);

	/* Binding */
	if (bind(sockfd,(struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0) {
		error("ERROR on binding");
	}

	printf("Bind to port %d\n",portno);

	/* Listening */
	listen(sockfd, 5);
	printf("Listening for connections..\n");

	while (1) {


		/* Wait for incoming connections in a loop */

		clilen = sizeof(cli_addr);
		newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);

		if (newsockfd < 0) {
			error("ERROR on accept");
		}
		printf("Connection accepted\n");


		if (inet_ntop(AF_INET, &cli_addr.sin_addr, str, INET_ADDRSTRLEN) == NULL) {
			fprintf(stderr, "Could not convert byte to address\n");
			exit(1);
		}
		printf("The client address is :%s\n", str);


		if((childpid = fork()) == 0 ) { 
			while(1) { 
				printf("Client %s please enter a command\n",str);
		
				bzero(buffer, BUFFER_SIZE);
				n = recv(newsockfd, buffer, BUFFER_SIZE - 1, 0);
				if (n <= 0) {
					error("ERROR reading from socket");
				} 
				else if (n == '\n') {
					continue;
				}
			
				int pid=fork();
				if(pid==-1) {
					perror("fork");
					exit(1);
				}
				if(pid!=0) { 
					if(wait(&status)==-1) {
						perror("wait");
						check_child_exit(QUIT);
					}

					if(WEXITSTATUS(status)==QUIT) { 
							break;
				}

			} else {  
				   if(strcmp(buffer, "quit\n") == 0 || n < 0 ) {
					  fprintf(stdout,"Disconnected from client %s\n",str);
					  close(sockfd);
					  exit(QUIT);
					}
					printf("Executing Client's %s command:",str);


					 if(strstr(buffer,"|")) {

						int pid;
						int fd[2];
						pipe(fd);
						switch(pid=fork()){

							case 0:
								runpipe(fd,newsockfd,buffer);
							default:
								while((pid=wait(&status))!=-1)
								exit(0);
							case -1:
								perror("fork");
								exit(1);

						}

					 } else {
						parse(vec,buffer);
						dup2(newsockfd,1); 
						dup2(newsockfd,2);
						execvp(vec[0],vec);
						perror(vec[0]);
						exit(1);
					}

			   }
			}

		}

	}
	close(newsockfd);

	return 0;
}



