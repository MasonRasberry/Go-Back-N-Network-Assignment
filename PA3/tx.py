import socket
import argparse
from PA3.packet import Packet
from PA3.cQueue import CircularQueue
import logging

PAYLOAD_SIZE = 50
SEQNUM_SIZE = 10
WINDOW_SIZE = 5
logging.basicConfig(filename="Tx.log",level=logging.DEBUG)
packetList = list()


def reliablyTransfer(rx_ip, rx_port, filename):
    # Implement the UDP sender to reliably transfer the file
    # Create log files as well to log the events in the sender side
    # Set up socket
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Connect to server and send message
    print(f"client: connecting to {rx_ip}")
    with open(filename, "rb") as file:
        message = file.read(PAYLOAD_SIZE)
        mySocket.sendto(message, (rx_ip,rx_port))

    # Receive length
    dataLength, _ = mySocket.recvfrom(1)
    messageLength = int.from_bytes(dataLength, byteorder='big')

    # Receive message
    responseMessage, _ = mySocket.recvfrom(messageLength)
    print(f"client: received {messageLength} bytes")
    print(responseMessage.decode())
    mySocket.close()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDP Transmitter")
    parser.add_argument("-ip", metavar="IP address", default="127.0.0.1", type=str, help="Receiver IP address")
    parser.add_argument("-p", metavar="Port number", default=12345, type=int, help="Receiver port number")
    parser.add_argument("-f", metavar="File path", default="data/small.txt", type=str, help="Path to the file to send")

    args = parser.parse_args()

    reliablyTransfer(args.ip, args.p, args.f)