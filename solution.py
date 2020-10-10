from socket import *


def smtp_client(port=1025, mailserver='127.0.0.1'):
    msg = "\r\n My message"
    endmsg = "\r\n.\r\n"

    # Choose a mail server (e.g. Google mail server) if you want to verify the script beyond GradeScope

    # Create socket called clientSocket and establish a TCP connection with mailserver and port

    # Fill in start
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((mailserver, port))
    # Fill in end

    # Send HELO command and print server response.
    heloCommand = 'HELO Alice\r\n'
    clientSocket.send(heloCommand.encode())
    recv1 = clientSocket.recv(1024).decode()

    # Send MAIL FROM command and print server response.
    # Fill in start
    sendFrom = 'MAIL FROM: <vb2110@nyu.edu> \r\n'
    clientSocket.send(sendFrom.encode())
    recv2 = clientSocket.recv(1024).decode()
    # Fill in end

    # Send RCPT TO command and print server response.
    # Fill in start
    sendRcpt = 'RCPT TO: <vb2110@nyu.edu> \r\n'
    clientSocket.send(sendRcpt.encode())
    recv3 = clientSocket.recv(1024).decode()
    # Fill in end

    # Send DATA command and print server response.
    # Fill in start
    sendData = "DATA \r\n"
    clientSocket.send(sendData.encode())
    recv4 = clientSocket.recv(1024).decode()
    # print(sending + received)
    # Fill in end

    # Send message data.
    # Fill in start
    #sending = "Subject: Hello SMTP lab \r\n bye bye\r\n"
    clientSocket.send(msg.encode())
    # print(sending)
    # Fill in end

    # Message ends with a single period.
    # Fill in start
    clientSocket.send(endmsg.encode())
    # recv5 = clientSocket.recv(1024).decode()
    # print(sending + received)
    # Fill in end

    # Send QUIT command and get server response.
    # Fill in start
    sendQuit = "QUIT \r\n"
    clientSocket.send(sendQuit.encode())
    # received = clientSocket.recv(1024).decode()
    # print(sending + received)
    clientSocket.close()
    # Fill in end

if __name__ == '__main__':
    smtp_client(1025, '127.0.0.1')
