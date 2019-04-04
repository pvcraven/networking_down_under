import java.util.Iterator;
import java.util.Set;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.ByteBuffer;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;

public class ReceiveMultipleMessages {

    public static void handleConnection() throws Exception {
        // Selector: multiplexor of SelectableChannel objects
        Selector selector = Selector.open(); // selector is open here

        // ServerSocketChannel: selectable channel for stream-oriented listening sockets
        ServerSocketChannel mySocket = ServerSocketChannel.open();
        InetSocketAddress myAddress = new InetSocketAddress("127.0.0.1", 10000);

        // Binds the channel's socket to a local address and configures the socket to listen for connections
        mySocket.bind(myAddress);

        // Adjusts this channel's blocking mode.
        mySocket.configureBlocking(false);

        int ops = mySocket.validOps();
        SelectionKey selectKy = mySocket.register(selector, ops, null);

        String fullMessage = "";
        boolean done = false;
        int chunks = 0;
        long startTime = System.currentTimeMillis();
        long endTime = 0L;

        System.out.println("\nStarting...");

        while(!done) {

            // Selects a set of keys whose corresponding channels are ready for I/O operations
            selector.select();

            // token representing the registration of a SelectableChannel with a Selector
            Set<SelectionKey> myKeys = selector.selectedKeys();
            Iterator<SelectionKey> keyIterator = myKeys.iterator();

            while (keyIterator.hasNext()) {
                SelectionKey myKey = keyIterator.next();

                // Tests whether this key's channel is ready to accept a new socket connection
                if (myKey.isAcceptable()) {
                    SocketChannel myClient = mySocket.accept();

                    // Adjusts this channel's blocking mode to false
                    myClient.configureBlocking(false);

                    // Operation-set bit for read operations
                    myClient.register(selector, SelectionKey.OP_READ);
                    System.out.println("Connection Accepted: " + myClient.getLocalAddress());

                    // Tests whether this key's channel is ready for reading
                } else if (myKey.isReadable()) {

                    SocketChannel myClient = (SocketChannel) myKey.channel();
                    ByteBuffer myBuffer = ByteBuffer.allocate(2048);
                    myClient.read(myBuffer);
                    String result = new String(myBuffer.array()).trim();
                    fullMessage = fullMessage + result;

                    // System.out.println("Message received: " + result);
                    chunks += 1;

                    if (result.endsWith("Z")) {
                        myClient.close();
                        mySocket.close();
                        selector.close();
                        done = true;
                        System.out.println("It's time to close connection as we got a Z");
                        endTime = System.currentTimeMillis();
                    }
                }
                keyIterator.remove();
            }
        }
        long totalTime = endTime - startTime;
        System.out.println("Done receiving " + fullMessage.length() + " in " + chunks + " chunks over " + totalTime + " ms.");
    }

    public static void main(String[] args) throws Exception {
        while(true)
            handleConnection();
    }
}