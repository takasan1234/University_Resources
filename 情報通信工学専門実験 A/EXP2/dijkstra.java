import java.io.File;
import java.io.FileNotFoundException;
import java.util.Random;
import java.util.Scanner;

public class dijkstra {
    /* 定数定義 */
    static final int NODE_NUM = 10;   /* 総ノード数 */
    static final int MAX = 9999;      /* 無限大に相当する数 */
    static final int FLAG = 0;        /* Dijkstraのテストの場合は0に、シミュレーション評価を行う場合は1にする */

    public static void main(String[] args) {
        /* Dijkstraのアルゴリズム部分で必要な変数 */
        int[][] graph = new int[NODE_NUM][NODE_NUM];    /* 距離行列 */
        int[] path   = new int[NODE_NUM];               /* 前ノード表 */
        int[] dist   = new int[NODE_NUM];               /* 距離を格納 */
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
            new Random(System.currentTimeMillis()); /* 乱数の初期化 */
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
                    // bandwidth[i][j] = link[i][j];
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

                /*
                 * 初期化
                 */
                for (i = 0; i < NODE_NUM; i++) { /* 何も確定していない状態にする */
                    dist[i] = MAX;
                    chk[i]  = 0;
                    path[i] = NODE_NUM;
                }
                path[src] = src;   /* 始点ノードへの経路上の前ノードはそれ自身とする */
                dist[src] = 0;     /* 始点ノード自身への距離は0である */
                chk[src]  = 1;     /* 始点ノードへの最短距離は確定 */
                tmp_node = src;    /* 始点ノードから探索を始める */
                fin      = 0;

                /*
                 * 経路探索
                 */

                /* 2. 送信ノードに接続されている全てのノードについて、接続リンクの長さを送信ノードからの長さとする */
                /* 3. 最短の距離をもつノードを確定とする */

                while (fin == 0) { /* finフラグが立つまで繰り返す */
                    /* 4. 更新処理 */
                    /* 5. 次の最短距離ノードを確定 */

                    if (chk[dest] == 1) fin = 1; /* 終点ノードへの最短距離が確定したら終了 */
                }

                /* 結果出力(Dijkstra作成時のみ実行する) */
                if (FLAG == 0) {
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
            }
        }

        /*
         * シミュレーション評価の結果出力
         */
        System.out.printf("\naverage = %f\n", sum_success / 1000.0); /* 平均を表示 */
    }
}
