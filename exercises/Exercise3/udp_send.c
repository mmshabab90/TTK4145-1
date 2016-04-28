#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>

#define PORT "30000"

int main(void){
	int status;
	int sockfd;
	int yes = 1;
	struct addrinfo hints;
	struct addrinfo *servinfo;
	
	memset(&hints, 0, sizeof(hints));
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_DGRAM;
	hints.ai_flags = AI_PASSIVE;

	if ((status = getaddrinfo(NULL, PORT, &hints, &servinfo)) != 0) {
   		fprintf(stderr, "getaddrinfo error: %s\n", gai_strerror(status));
    		exit(1);
	}
	
	if (setsockopt(listener, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int)) == -1 {
		perror("setsockopt");
		exit(1);
	}

	sockfd = socket(servinfo->ai_family, servinfo->ai_socktype, servinfo -> ai_protocol);
	bind(sockfd, servinfo->ai_addr, servinfo->ai_protocol);

	printf("HEI\n");
	freeaddrinfo(servinfo);
} 
