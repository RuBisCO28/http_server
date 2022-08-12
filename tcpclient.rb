require 'socket'

socket = TCPSocket.open("localhost", 8080)

while line = $stdin.gets
  socket.puts line
  socket.flush

  puts socket.gets
end

socket.close
