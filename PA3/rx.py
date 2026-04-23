import socket
import argparse
from PA3.packet import Packet
from PA3.cQueue import CircularQueue

PAYLOAD_SIZE = 50
SEQNUM_SIZE = 10
WINDOW_SIZE = 5

def reliablyReceive(rx_ip, rx_port, filename):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((rx_ip, rx_port))

    expected_seq = 0
    last_acked = -1

    with open(filename, "w") as file:
        while True:
            data, addr = sock.recvfrom(1024)
            packet = Packet.deserialize(data)

            #FIN packet
            if packet.flag == 2:
                ack = Packet(0, last_acked, 0, "")
                sock.sendto(ack.serialize(), addr)
                continue

            if packet.flag == 1:
                if packet.seqnum == expected_seq:
                    #correct packet
                    file.write(packet.payload)
                    last_acked = expected_seq
                    expected_seq = (expected_seq + 1) % SEQNUM_SIZE
                else:
                    #out-of-order → discard
                    pass

                #Always send ACK (last in-order)
                ack = Packet(0, last_acked, 0, "")
                sock.sendto(ack.serialize(), addr)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDP Receiver")
    parser.add_argument("-ip", metavar="IP address", default="127.0.0.1", type=str, help="Receiver IP address")
    parser.add_argument("-p", metavar="Port number", default=12345, type=int, help="Receiver port number")
    parser.add_argument("-f", metavar="File path", default="data/destinationFile.txt", type=str, help="Path to the file to send")

    args = parser.parse_args()
    
    reliablyReceive(args.ip, args.p, args.f)
