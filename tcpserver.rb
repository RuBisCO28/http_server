require 'socket'

server = TCPServer.new('0.0.0.0', 8080)

while true
  p "Wating connection from client"
  socket = server.accept
  p "Connection is established"

  p socket.peeraddr

  while buffer = socket.gets
    puts "RECV : #{buffer}"

    socket.puts "SERVER received '#{buffer}' from CLIENT."
  end

  socket.close
end

server.close
