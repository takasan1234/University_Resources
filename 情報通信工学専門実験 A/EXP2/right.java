import java.io.*;
import java.util.*;

public class right {
    // 定数
    static final int NODE_NUM = 10; // ノード数
    static final int MAX = 9999; // 無限大を表す数
    static final int FLAG = 0; // Dijkstraのテストの場合は0に、シミュレーション評価を行う場合は1にする

    public static void main(String[] args) {
        // Dijkstraのアルゴリズム実行で必要な変数
        int[][] graph = new int[NODE_NUM][NODE_NUM]; // 距離行列
        int[] path = new int[NODE_NUM]; // 前ノード表
        int[] dist = new int[NODE_NUM]; // 距離を格納
        int[] chk = new int[NODE_NUM]; // 最短距離確定のフラグ
        int src = 0, dest = 0; // 始点・終点ノード
        int tmp_node, fin; // 注目しているノードと未確定ノードが残っているかどうかのフラグ

        // シミュレーション評価の部分で必要な変数
        int[][] link = new int[NODE_NUM][NODE_NUM]; // リンク容量
        int[][] bandwidth = new int[NODE_NUM][NODE_NUM]; // リンクの空き容量(逐次更新される)
        int miss; // 再送を表すフラグ
        int success; // 確保できた通信数
        int sum_success = 0; // 確保できた通信数の合計

        // 距離行列の作成
        for (int i = 0; i < NODE_NUM; i++) {
            for (int j = 0; j < NODE_NUM; j++) {
                graph[i][j] = MAX; // 接続されていないノード間の距離をMAXにする
                link[i][j] = -1; // 接続されていないノード間のリンク容量を-1にする
                if (i == j) {
                    graph[i][j] = 0; // 同じノード自身への距離は0とし
                    link[i][j] = -1; // リンク容量は-1とする
                }
            }
        }

        // ファイルから距離情報を読み込む
        try {
            BufferedReader br = new BufferedReader(new FileReader("./distance.txt"));
            String line;
            while ((line = br.readLine()) != null) {
                String[] values = line.trim().split("\\s+");
                if (values.length == 4) {
                    int a = Integer.parseInt(values[0]);
                    int b = Integer.parseInt(values[1]);
                    int c = Integer.parseInt(values[2]);
                    int d = Integer.parseInt(values[3]);
                    graph[a][b] = c; // 接続されているノード間の距離を設定
                    graph[b][a] = c; // 逆方向も同じ距離と仮定
                    link[a][b] = d; // 接続されているノード間のリンクを設定
                    link[b][a] = d; // 逆方向も同じ容量と仮定
                }
            }
            br.close();
        } catch (IOException e) {
            System.out.println("distance.txtファイルが見つかりません");
            e.printStackTrace();
            return;
        }

        // 始点・終点ノードをユーザー入力から得る (評価の場合は、実行しない)
        if (FLAG == 0) {
            Scanner scanner = new Scanner(System.in);
            System.out.printf("Source Node?(0-%d)", NODE_NUM - 1);
            src = scanner.nextInt();
            System.out.printf("Destination Node?(0-%d)", NODE_NUM - 1);
            dest = scanner.nextInt();
            scanner.close();
        }

        if (FLAG == 1) {
            Random random = new Random(); // 乱数の初期化
        }

        // シミュレーション評価開始
        success = 0;
        sum_success = 0; // 評価指標を初期化

        for (int sim_time = 0; sim_time < 1000; sim_time++) {
            miss = 0; // 空きリンクが存在しない場合のフラグをOFFにする
            success = 0; // 確保できた通信数を初期化する

            // 全リンクの空き容量を初期状態に戻す
            for (int i = 0; i < NODE_NUM; i++) {
                for (int j = 0; j < NODE_NUM; j++) {
                    if (link[i][j] > 0) {
                        bandwidth[i][j] = link[i][j];
                    }
                }
            }

            while (miss == 0) { // 再送が発生するまで繰り返す
                // 評価の場合、送受信ノードをランダムに選ぶ
                if (FLAG == 1) {
                    // ランダムに送受信ノードを選択
                    Random random = new Random();
                    src = random.nextInt(NODE_NUM);
                    dest = random.nextInt(NODE_NUM);

                    System.out.printf("src=%d, dest=%d\n", src, dest); // 送受信ノードを表示
                    if (src == dest) {
                        System.out.println("送受信ノードが一致している");
                    }
                }

                // Dijkstraのアルゴリズム
                // 初期化
                for (int i = 0; i < NODE_NUM; i++) { // 距離を未確定にする
                    dist[i] = MAX;
                    chk[i] = 0;
                    path[i] = NODE_NUM;
                }

                path[src] = src; // 始点ノードへの経路の前ノードはそれ自身とする
                dist[src] = 0; // 始点ノード自身への距離は0である
                chk[src] = 1; // 始点ノードへの最短距離は確定
                tmp_node = src; // 始点ノードから探索を始める
                fin = 0;

                // 経路探索
                while (fin == 0) { // finフラグが立つまで繰り返す
                    // 確定したノードに接続している全てのノードについて
                    for (int i = 0; i < NODE_NUM; i++) {
                        if (graph[tmp_node][i] < MAX && chk[i] == 0) {
                            // 現在の距離よりも短い距離が見つかった場合に更新
                            if (dist[i] > dist[tmp_node] + graph[tmp_node][i]) {
                                dist[i] = dist[tmp_node] + graph[tmp_node][i];
                                path[i] = tmp_node;
                            }
                        }
                    }

                    // まだ確定していないノードの中で、始点ノードからの距離が最短のノードを確定とする
                    int min_dist = MAX;
                    int min_node = -1;
                    for (int i = 0; i < NODE_NUM; i++) {
                        if (chk[i] == 0 && dist[i] < min_dist) {
                            min_dist = dist[i];
                            min_node = i;
                        }
                    }

                    if (min_node != -1) {
                        chk[min_node] = 1;
                        tmp_node = min_node;
                    } else {
                        fin = 1; // 探索終了
                    }

                    if (chk[dest] == 1) {
                        fin = 1; // 終点ノードへの最短距離が確定したら終了
                    }
                }

                // 結果出力(Dijkstra作成時のみ実行する)
                if (FLAG == 0) {
                    if (dist[dest] >= MAX) {
                        System.out.printf("No path from node%d to node%d.\n", src, dest);
                    } else {
                        System.out.printf("Shortest path from node%d to node%d is as follows.\n", src, dest);
                        System.out.printf("%d", dest);
                        int i = dest;
                        while (path[i] != src) {
                            i = path[i];
                            System.out.printf(" <- %d", i);
                        }
                        System.out.printf(" <- %d\n", src);
                        System.out.printf("Shortest distance is %d.\n", dist[dest]);
                    }
                    return;
                }

                // 以下、Dijkstraで確定した経路を評価するためのプログラム
                if (FLAG == 1) {
                    // 経路が存在するかチェック
                    if (dist[dest] < MAX) {
                        // 経路を再構築
                        ArrayList<Integer> route = new ArrayList<>();
                        int i = dest;
                        while (i != src) {
                            route.add(i);
                            i = path[i];
                        }
                        route.add(src);
                        Collections.reverse(route); // 始点から終点へ順に並べる

                        // 経路上の全リンクに空き容量があるか確認
                        boolean can_allocate = true;
                        for (i = 0; i < route.size() - 1; i++) {
                            if (bandwidth[route.get(i)][route.get(i + 1)] <= 0) {
                                can_allocate = false;
                                break;
                            }
                        }

                        if (can_allocate) {
                            // 2-(a) 全リンクに空き容量がある場合、各リンクから1Mbps分帯域を確保し、
                            // 「確保できた通信数」を1増やす
                            for (i = 0; i < route.size() - 1; i++) {
                                bandwidth[route.get(i)][route.get(i + 1)] -= 1;
                                bandwidth[route.get(i + 1)][route.get(i)] -= 1; // 双方向リンクの場合
                            }

                            success += 1;
                        } else {
                            // 2-(b) 空き容量のないリンクが存在する場合、再送とし、
                            // この時点までの「確保できた通信数」をsum_successに加算して、whileからbreak
                            miss = 1;
                            sum_success += success;
                            break;
                        }
                    } else {
                        // 経路がない場合
                        miss = 1;
                        sum_success += success;
                        break;
                    }
                }
            }
        }

        // シミュレーション評価の結果出力
        if (FLAG == 1) {
            System.out.printf("\naverage = %.6f\n", (double) sum_success / 1000.0); // 平均値を表示
        }
    }
}
