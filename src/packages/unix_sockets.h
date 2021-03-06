#pragma once
#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>
#include <sstream>
#include <iostream>

#ifndef MAX_SPAM
#define MAX_SPAM 5
#endif

class Tcp {
protected:
    int portn, sock, valread;
    char buffer[1024] = {0};
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    int server_fd;

public:
    Tcp() {
        if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
        {
            printf("\n Socket creation error \n");
            exit(1);
        }
    }
    ~Tcp() {
        //setRun(false);
    }

    bool connectTo(std::string ip = "127.0.0.1", int port = 80) {
        address.sin_family = AF_INET;
        address.sin_port = htons(port);
        if(inet_pton(AF_INET, ip.c_str(), &address.sin_addr)<=0)
        {
            printf("\nInvalid address/ Address not supported \n");
            return false;
        }
        if (connect(sock, (struct sockaddr *)&address, sizeof(address)) < 0)
        {
            printf("\nConnection Failed \n");
            return false;
        }
    }

    bool listenOn(int port) {
        // Creating socket file descriptor
        if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0)
        {
            perror("socket failed");
            return false;
        }

        // Forcefully attaching socket to the port 8080
        if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT,
                                                      &opt, sizeof(opt)))
        {
            perror("setsockopt");
            return false;
        }
        address.sin_family = AF_INET;
        address.sin_addr.s_addr = INADDR_ANY;
        address.sin_port = htons( port );

        // Forcefully attaching socket to the port 8080
        if (bind(server_fd, (struct sockaddr *)&address,
                                     sizeof(address))<0)
        {
            perror("bind failed");
            return false;
        }
        if (listen(server_fd, 3) < 0)
        {
            perror("listen");
            return false;
        }
        if ((sock = accept(server_fd, (struct sockaddr *)&address,
                           (socklen_t*)&addrlen))<0)
        {
            perror("accept");
            return false;
        }
    }
    //void setRun(bool value) { run = value; }
    int getSock() { return sock; }
    char* getBuffer() { return buffer; }
    void sends(std::string msg) {
        send(sock , msg.c_str() , msg.length() , 0 );
    }
    int readToBuffer() {
        return read(sock , buffer, 1024);
    }
};
