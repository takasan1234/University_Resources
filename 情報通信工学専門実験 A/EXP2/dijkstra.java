import java.io.File;
import java.io.FileNotFoundException;
import java.util.Random;
import java.util.Scanner;

public class dijkstra {
    /* 定数定義 */
    static final int NODE_NUM = 10;   /* 総ノード数 */
    static final int MAX = 9999;      /* 無限大に相当する数 */
    static final int FLAG = 0;        /* Dijkstraのテストの場合は0に、シミュレーション評価を行う場合は1にする */
    static final int ROUTE_TYPE = 1;  /* 経路選択方法：0=最短路、1=最大路 */

    /* Dijkstraアルゴリズムによる最短路の計算 */
    public static void findShortestPath(int[][] graph, int[] path, int[] dist, int[] chk, int src, int dest) {
        int i, tmp_node, tmp_dist, fin;
        
        /* 初期化 */
        for (i = 0; i < NODE_NUM; i++) {
            dist[i] = MAX;
            chk[i]  = 0;
            path[i] = NODE_NUM;
        }
        path[src] = src;   /* 始点ノードへの経路上の前ノードはそれ自身とする */
        dist[src] = 0;     /* 始点ノード自身への距離は0である */
        chk[src]  = 1;     /* 始点ノードへの最短距離は確定 */
        tmp_node = src;    /* 始点ノードから探索を始める */
        fin      = 0;

        /* 経路探索 */
        while (fin == 0) { /* finフラグが立つまで繰り返す */
            /* 更新処理 */
            for (i = 0; i < NODE_NUM; i++) {
                if (graph[tmp_node][i] < MAX && chk[i] == 0) {
                    /* 未確定ノードへの距離を更新 */
                    if (dist[i] > dist[tmp_node] + graph[tmp_node][i]) {
                        dist[i] = dist[tmp_node] + graph[tmp_node][i];
                        path[i] = tmp_node;  /* 前ノードを記録 */
                    }
                }
            }

            /* 次の最短距離ノードを確定 */
            tmp_dist = MAX;
            for (i = 0; i < NODE_NUM; i++) {
                if (chk[i] == 0 && dist[i] < tmp_dist) {
                    tmp_dist = dist[i];
                    tmp_node = i;
                }
            }

            // 未確定ノードが存在しない、または到達不能な場合 ループを抜ける
            if (tmp_dist == MAX) {
                fin = 1;
            } else {
                chk[tmp_node] = 1;  /* 最短距離ノードを確定 */
            }

            if (chk[dest] == 1) fin = 1; /* 終点ノードへの最短距離が確定したら終了 */
        }
    }

    /* 最大路の計算（ボトルネックリンクが最大の経路を求める） */
    public static void findMaximumPath(int[][] graph, int[][] link, int[] path, int[] bottleneck, int[] chk, int src, int dest) {
        int i, j, tmp_node, tmp_bottleneck, fin;
        int[][] capacityGraph = new int[NODE_NUM][NODE_NUM]; // ボトルネック容量用のグラフ
        
        /* 容量グラフの初期化 */
        for (i = 0; i < NODE_NUM; i++) {
            for (j = 0; j < NODE_NUM; j++) {
                if (graph[i][j] < MAX) { // リンクが存在する場合
                    capacityGraph[i][j] = link[i][j]; // リンク容量を使用
                } else {
                    capacityGraph[i][j] = 0; // リンクがない場合は容量0
                }
            }
        }
        
        /* 初期化 */
        for (i = 0; i < NODE_NUM; i++) {
            bottleneck[i] = 0; // ボトルネック容量を0で初期化
            chk[i] = 0;
            path[i] = NODE_NUM;
        }
        
        path[src] = src;   // 始点ノードへの経路上の前ノードはそれ自身
        bottleneck[src] = MAX; // 始点ノード自身へのボトルネック容量は最大
        chk[src] = 1;      // 始点ノードは確定
        tmp_node = src;    // 始点ノードから探索開始
        fin = 0;
        
        /* 経路探索 */
        while (fin == 0) {
            /* 更新処理 */
            for (i = 0; i < NODE_NUM; i++) {
                if (capacityGraph[tmp_node][i] > 0 && chk[i] == 0) {
                    // 経路上のボトルネック容量は、これまでの最小容量と新しいリンク容量の小さい方
                    int newBottleneck = Math.min(bottleneck[tmp_node], capacityGraph[tmp_node][i]);
                    
                    // より大きなボトルネック容量を持つ経路が見つかった場合、更新
                    if (bottleneck[i] < newBottleneck) {
                        bottleneck[i] = newBottleneck;
                        path[i] = tmp_node;
                    }
                }
            }
            
            /* 次に確定するノードを選択（未確定ノードの中でボトルネック容量が最大のもの） */
            tmp_bottleneck = 0;
            tmp_node = -1;
            for (i = 0; i < NODE_NUM; i++) {
                if (chk[i] == 0 && bottleneck[i] > tmp_bottleneck) {
                    tmp_bottleneck = bottleneck[i];
                    tmp_node = i;
                }
            }
            
            // 未確定ノードが存在しない、または到達不能な場合
            if (tmp_node == -1) {
                fin = 1;
            } else {
                chk[tmp_node] = 1; // ノードを確定
            }
            
            if (chk[dest] == 1) fin = 1; // 終点ノードが確定したら終了
        }
    }

    public static void main(String[] args) {
        /* Dijkstraのアルゴリズム部分で必要な変数 */
        int[][] graph = new int[NODE_NUM][NODE_NUM];    /* 距離行列 */
        int[] path   = new int[NODE_NUM];               /* 前ノード表 */
        int[] dist   = new int[NODE_NUM];               /* 距離を格納 */
        int[] bottleneck = new int[NODE_NUM];           /* ボトルネック容量を格納 */
        int[] chk    = new int[NODE_NUM];               /* 最短距離確定のフラグ */
        int tmp_node, tmp_dist;                         /* 注目しているノードとそこまでの最短距離 */
        int src = 0, dest = 0;                          /* 始点・終点ノード */
        int a = 0, b = 0, c = 0, d = 0, i = 0, j = 0;
        int fin;                                        /* 未確定ノードが残っているかどうかのフラグ */
        Scanner stdin;

        /* シミュレーション評価の部分で必要な変数 */
        int[][] link      = new int[NODE_NUM][NODE_NUM]; /* リンク容量 */
        int[][] bandwidth = new int[NODE_NUM][NODE_NUM]; /* リンクの空き容量 */
        int miss;                                       /* 呼損を表すフラグ */
        int success;                                    /* 確立できた通信回数 */
        int sum_success;                                /* 確立できた通信回数の合計 */
        int sim_time;                                   /* 評価の回数をカウント */

        /*
         * 距離行列の作成
         */
        for (i = 0; i < NODE_NUM; i++) {
            for (j = 0; j < NODE_NUM; j++) {
                graph[i][j] = MAX;    /* 接続されていないノード間の距離をMAXにする */
                link[i][j]  = -1;     /* 接続されていないノード間のリンク容量を-1にする */
                if (i == j) {
                    graph[i][j] = 0;
                    link[i][j]  = -1;
                } /* そのノード自身への距離は0とし、リンク容量は-1とする */
            }
        }

        /* ファイル読み込み */
        try {
            Scanner scanner = new Scanner(new File("./distance.txt"));
            while (scanner.hasNextInt()) { /* EOFまで4つ組を読み込む */
                a = scanner.nextInt();
                b = scanner.nextInt();
                c = scanner.nextInt();
                d = scanner.nextInt();
                graph[a][b] = c; /* 接続されているノード間の距離を設定 */
                graph[b][a] = c; /* 逆方向も等距離と仮定 */
                link[a][b]  = d; /* 接続されているノード間のリンクを設定 */
                link[b][a]  = d; /* 逆方向も同じ容量と仮定 */
            }
            scanner.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
            return;
        }

        /*
         * 始点・終点ノードを標準入力から得る (評価の場合は、実行しない)
         */
        if (FLAG == 0) {
            stdin = new Scanner(System.in);
            System.out.printf("Source Node?(0-%d)", NODE_NUM - 1);
            src = stdin.nextInt();
            System.out.printf("Destination Node?(0-%d)", NODE_NUM - 1);
            dest = stdin.nextInt();
            // stdin.close();
        }

        if (FLAG == 1) {
            Random rand = new Random(System.currentTimeMillis()); /* 乱数の初期化 */
            do {
                src = rand.nextInt(NODE_NUM);  // 0からNODE_NUM-1までの乱数を生成
                dest = rand.nextInt(NODE_NUM);
            } while (src == dest);  // 送信元と送信先が同じ場合は再抽選
        }

        /****************************/
        /* シミュレーション評価開始 */
        /****************************/
        success     = 0;
        sum_success = 0; /* 評価指標を初期化 */
        for (sim_time = 0; sim_time < 1000; sim_time++) {
            miss    = 0; /* 空きリンクが存在しない場合のフラグをOFFにする */
            success = 0; /* 確立できた通信回数を初期化する */

            for (i = 0; i < NODE_NUM; i++) { /* 全リンクの空き容量を初期状態に戻す */
                for (j = 0; j < NODE_NUM; j++) {
                    bandwidth[i][j] = link[i][j];  // リンク容量を初期状態にコピー
                }
            }

            while (miss == 0) { /* 呼損が発生するまで繰り返す */
                /* 評価の場合、送受信ノードをランダムに決定 */
                if (FLAG == 1) {
                    /* ランダムに送受信ノードを決定 */
                    System.out.printf("src=%d, dest=%d\n", src, dest); /* 送受信ノードを表示 */
                    if (src == dest) System.out.println("送受信ノードが一致している");
                }

                /****************************************/
                /* ここからdijkstraのアルゴリズムを記述 */
                /****************************************/

                if (ROUTE_TYPE == 0) {
                    // 最短路の計算
                    findShortestPath(graph, path, dist, chk, src, dest);
                } else {
                    // 最大路の計算
                    findMaximumPath(graph, link, path, bottleneck, chk, src, dest);
                }

                /* 結果出力(Dijkstra作成時のみ実行する) */
                if (FLAG == 0) {
                    if (ROUTE_TYPE == 0) {
                        // 最短路の結果出力
                        if (dist[dest] >= MAX) {
                            System.out.printf("No path from node%d to node%d.\n", src, dest);
                        } else {
                            System.out.printf("Shortest path from node%d to node%d is as follows.\n", src, dest);
                            System.out.printf("%d <- ", dest);
                            i = dest;
                            for (i = path[i]; i != src; i = path[i]) { /* 前ノード表を辿る */
                                System.out.printf("%d <- ", i);
                            }
                            System.out.printf("%d\n", src);
                            System.out.printf("Shortest distance is %d.\n", dist[dest]);
                        }
                    } else {
                        // 最大路の結果出力
                        if (bottleneck[dest] <= 0) {
                            System.out.printf("No path from node%d to node%d.\n", src, dest);
                        } else {
                            System.out.printf("Maximum bottleneck path from node%d to node%d is as follows.\n", src, dest);
                            System.out.printf("%d <- ", dest);
                            i = dest;
                            for (i = path[i]; i != src; i = path[i]) { /* 前ノード表を辿る */
                                System.out.printf("%d <- ", i);
                            }
                            System.out.printf("%d\n", src);
                            System.out.printf("Maximum bottleneck capacity is %d.\n", bottleneck[dest]);
                        }
                    }
                    return; /* Dijkstra作成時は結果を出力したら終了 */
                }

                /************************************/
                /* ここまでがdijkstraのアルゴリズム */
                /************************************/

                /**********************************************************************/
                /* この下にdijkstraで決定した経路を評価するためのプログラムを記述 */
                /**********************************************************************/
                /*
                 * 2-(a) 空き容量がある場合の処理
                 * 2-(b) 呼損が発生した場合の処理
                 */
                int miss_flag = 0;
                
                // 経路上の全リンクの空き容量を確認
                i = dest;
                int temp = dest;
                for (i = path[i]; i != src; i = path[i]) {
                    if (bandwidth[temp][i] < 1) {  // 空き容量が1Mbps未満の場合
                        miss_flag = 1;
                        break;
                    }
                    temp = i;
                }

                if (miss_flag == 0) {  // 経路上の全リンクに十分な空き容量がある場合
                    // 経路上の全リンクの空き容量を1Mbps減少
                    i = dest;
                    temp = dest;
                    for (i = path[i]; i != src; i = path[i]) {
                        bandwidth[temp][i]--;
                        bandwidth[i][temp]--;  // 双方向に容量を減少
                        temp = i;
                    }
                    success++;
                } else {
                    miss++;
                }
                System.out.printf("success = %d, miss = %d\n", success, miss);
                return;
                
            }
        }

        /*
         * シミュレーション評価の結果出力
         */
        System.out.printf("\naverage = %f\n", sum_success / 1000.0); /* 平均を表示 */
    }
}