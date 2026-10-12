package oblig1;

import java.io.*;

class Teque {

    Teque(int size) {
    }

    void pushBack(int x) {
    }

    void pushFront(int x) {
    }

    void pushMiddle(int x) {
    }

    int get(int i) {
        return -1;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int N = Integer.parseInt(br.readLine());
        Teque teque = new Teque(N);

        for (int i = 0; i < N; i++) {
            String[] line = br.readLine().split(" ");
            String cmd = line[0];
            int num = Integer.parseInt(line[1]);

            if (cmd.equals("push_back")) {
                teque.pushBack(num);
            } else if (cmd.equals("push_front")) {
                teque.pushFront(num);
            } else if (cmd.equals("push_middle")) {
                teque.pushMiddle(num);
            } else if (cmd.equals("get")) {
                System.out.println(teque.get(num));
            }
        }
    }
}
