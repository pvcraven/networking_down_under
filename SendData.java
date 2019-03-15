import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;

public class SendData {

    public static void main(String[] args) throws Exception {
        InetAddress serverAddress = InetAddress.getByName("127.0.0.1");
        int serverPort =  10000;

        System.out.println("Connecting...");
        Socket socket = new Socket(serverAddress, serverPort);

        System.out.println("Connected, sending data...");

        String myData = "Hello world!";
        boolean autoFlush = true;
        PrintWriter out = new PrintWriter(socket.getOutputStream(), autoFlush);
        out.print(myData);
        out.flush();

        System.out.println("Done");
    }
}