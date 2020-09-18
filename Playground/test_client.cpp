#include "unix_sockets.h"

int main(int argc, char const *argv[]) {
    using namespace std;

    Tcp sock;
    sock.connectTo("127.0.0.1",8080);
    // once we get a connection:
    communicate(sock);

    return 0;
}
