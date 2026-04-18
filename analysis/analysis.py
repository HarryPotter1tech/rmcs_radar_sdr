import zmq

context = zmq.Context()
print("Connecting to gnu radio receiver server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
print("Connected to gnu radio receiver server.")
print("Requesting data from gnu radio receiver server…")
buffer: bytes = b""
while True:
    buffer += socket.recv()
