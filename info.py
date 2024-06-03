import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the host and port
host = '127.0.0.1'  # Use your actual host IP or 'localhost'
port = 8080  # The port number you want to add

# Bind the socket to the host and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(1)

print(f"Server is listening on port {port}")

# Accept incoming connections
client_socket, client_address = server_socket.accept()

print(f"Connection from: {client_address}")

# Close the connection
client_socket.close()

API_ID       = "21518327"
API_HASH     = "e72f588b3e4763f01eecfc3c4aa7e8ac"
BOT_TOKEN    = "7369210557:AAHye9_YGxdQOJ9yuFU3i6WkDka4CzXB4-4"
SESSION      = "BQFIV_cAl0zQ4uSC_9SgbK4Ccx3c5hG8ppAk293kfgMetlpGh9BtSg_jxSDYOm8QYWpVjnXKHk0NdJp-KzBOc9S7hnM08XWf07HpnQakiB0EpkAfaMhT0sksPNpOO7vtNy6qmIfTuNgUfn5ROWSFZ0_nvV5t-W9WmMZ-oPZnfZSQChpHZapLjTAoblCISGCjrWDjDOFE1gl3PN_NndOYGJn9PNi7LLMSM8b8t8kDTcKehKYBB3JDCBkciqS-l8O3mesNdAtAIV4hAAshOWxp3SR5dU24cP5G5BZUxJNCI1zR0PiDW6DmbULNWmwGo0L_E2tJcNqYaHkAS9rPCATUmGrlfv0xJQAAAAFWPrmkAA"
DATABASE_URI = "mongodb+srv://vinayjaat4:vinayjaat4@postfinder.dns5ykq.mongodb.net/?retryWrites=true&w=majority&appName=postfinder"
LOG_CHANNEL  = -1001839965169
ADMIN        = 5741918628
CHANNEL      = "supremedevelopment"
