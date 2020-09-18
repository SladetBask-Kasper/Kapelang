#include <thread>
#define PORT 8080
#define MAX_SPAM 5

bool run = true;

void listen_(int sock, char buffer[]) {
    using namespace std;
    string last = "";
    int same = 0;
    while (run) {
        int valread = read( sock , buffer, 1024);
        if (strcmp(buffer, last.c_str()) == 0) {
            same++;
            cout << "SPAM: " << same << endl;
            if (same >= MAX_SPAM) {
                cout << "ERROR: Connection lost. Press enter to exit." << endl;
                run = false;
            }
        } else {
            same = 0;
        }
        last = buffer;
        printf("\nThem: %s\n",buffer );
    }
}
void talk_(int sock) {
    using namespace std;
    cout << "Enter messages freely below: " << endl;
    while (run) {
        string msg;
        cin >> msg;

        send(sock , msg.c_str() , msg.length() , 0 );
        cout << "You: " << msg << endl;
    }
}
