import java.io.File;
import java.io.FileNotFoundException;
import java.util.Random;
import java.util.Scanner;
import java.util.ArrayList;
import java.util.List;

public class dijkstra {
    /* 定数定義 */
    static final int NODE_NUM = 10;   /* 総ノード数 */
    static final int MAX = 9999;      /* 無限大に相当する数 */
    static final int FLAG = 1;        /* Dijkstraのテストの場合は0に、シミュレーション評価を行う場合は1にする */
    static final int ROUTE_TYPE = 0;  /* 経路選択方法：0=最短路、1=最大路、2=要求時最短路、3=要求時最大路 */
    static final int SIM_COUNT = 10000; /* シミュレーション回数 */
    static final int[] PARAM_N = {5, 10, 20, 50, 100}; /* テストするパラメータnの値 */
    static final String[] ROUTE_TYPE_NAMES = {
        "最小ホップ経路を用いた固定経路",
        "最大路を用いた固定経路",
        "最小ホップを用いた要求時経路",
        "最大路を用いた要求時経路"
    };

    /* 通信履歴を管理するクラス */
    static class Communication {
        int src;           // 送信元ノード
        int dest;          // 宛先ノード
        List<Integer> path; // 経路上のノード
        boolean established; // 通信が確立したかどうか

        public Communication(int src, int dest) {
            this.src = src;
            this.dest = dest;
            this.path = new ArrayList<>();
            this.established = false;
        }

        // 経路情報を設定
        public void setPath(int[] nodePath) {
            this.path.clear();
            int current = this.dest;
            this.path.add(current);
            
            while (current != this.src && current < NODE_NUM) {
                current = nodePath[current];
                if (current >= NODE_NUM) {
                    // 経路が見つからなかった場合
                    this.path.clear();
                    break;
                }
                this.path.add(current);
            }
        }
    }

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

    /* 最小ホップを用いた要求時経路（空き容量のないリンクをグラフから取り除く） */
    public static void findOnDemandShortestPath(int[][] graph, int[][] bandwidth, int[] path, int[] dist, int[] chk, int src, int dest) {
        int i, j, tmp_node, tmp_dist, fin;
        int[][] availableGraph = new int[NODE_NUM][NODE_NUM]; // 利用可能なリンクのみのグラフ
        
        /* 利用可能なリンクのみのグラフを作成 */
        for (i = 0; i < NODE_NUM; i++) {
            for (j = 0; j < NODE_NUM; j++) {
                if (graph[i][j] < MAX && bandwidth[i][j] >= 1) {
                    // 空き容量が1Mbps以上あるリンクのみを使用
                    availableGraph[i][j] = graph[i][j];
                } else {
                    availableGraph[i][j] = MAX;
                }
            }
        }
        
        /* 最短路の計算（利用可能なリンクのみ） */
        for (i = 0; i < NODE_NUM; i++) {
            dist[i] = MAX;
            chk[i] = 0;
            path[i] = NODE_NUM;
        }
        
        path[src] = src;
        dist[src] = 0;
        chk[src] = 1;
        tmp_node = src;
        fin = 0;
        
        while (fin == 0) {
            for (i = 0; i < NODE_NUM; i++) {
                if (availableGraph[tmp_node][i] < MAX && chk[i] == 0) {
                    if (dist[i] > dist[tmp_node] + availableGraph[tmp_node][i]) {
                        dist[i] = dist[tmp_node] + availableGraph[tmp_node][i];
                        path[i] = tmp_node;
                    }
                }
            }
            
            tmp_dist = MAX;
            for (i = 0; i < NODE_NUM; i++) {
                if (chk[i] == 0 && dist[i] < tmp_dist) {
                    tmp_dist = dist[i];
                    tmp_node = i;
                }
            }
            
            if (tmp_dist == MAX) {
                fin = 1;
            } else {
                chk[tmp_node] = 1;
            }
            
            if (chk[dest] == 1) fin = 1;
        }
    }
    
    /* 最大路を用いた要求時経路（経路選択時点での空き容量をリンクの重みとする） */
    public static void findOnDemandMaximumPath(int[][] graph, int[][] bandwidth, int[] path, int[] bottleneck, int[] chk, int src, int dest) {
        int i, j, tmp_node, tmp_bottleneck, fin;
        int[][] availableGraph = new int[NODE_NUM][NODE_NUM]; // 利用可能なリンクのみのグラフ
        
        /* 利用可能なリンクのみのグラフを作成（空き容量を重みとする） */
        for (i = 0; i < NODE_NUM; i++) {
            for (j = 0; j < NODE_NUM; j++) {
                if (graph[i][j] < MAX && bandwidth[i][j] >= 1) {
                    // 空き容量が1Mbps以上あるリンクのみを使用
                    availableGraph[i][j] = bandwidth[i][j]; // 空き容量をリンクの重みとする
                } else {
                    availableGraph[i][j] = 0;
                }
            }
        }
        
        /* 初期化 */
        for (i = 0; i < NODE_NUM; i++) {
            bottleneck[i] = 0;
            chk[i] = 0;
            path[i] = NODE_NUM;
        }
        
        path[src] = src;
        bottleneck[src] = MAX;
        chk[src] = 1;
        tmp_node = src;
        fin = 0;
        
        while (fin == 0) {
            for (i = 0; i < NODE_NUM; i++) {
                if (availableGraph[tmp_node][i] > 0 && chk[i] == 0) {
                    int newBottleneck = Math.min(bottleneck[tmp_node], availableGraph[tmp_node][i]);
                    
                    if (bottleneck[i] < newBottleneck) {
                        bottleneck[i] = newBottleneck;
                        path[i] = tmp_node;
                    }
                }
            }
            
            tmp_bottleneck = 0;
            tmp_node = -1;
            for (i = 0; i < NODE_NUM; i++) {
                if (chk[i] == 0 && bottleneck[i] > tmp_bottleneck) {
                    tmp_bottleneck = bottleneck[i];
                    tmp_node = i;
                }
            }
            
            if (tmp_node == -1) {
                fin = 1;
            } else {
                chk[tmp_node] = 1;
            }
            
            if (chk[dest] == 1) fin = 1;
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
        List<Communication> history = new ArrayList<>(); /* 通信履歴 */

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
            
            // 各経路選択方法でシミュレーションを実行
            for (int route_type = 0; route_type < 4; route_type++) {
                System.out.printf("\n=======================================\n");
                System.out.printf("経路選択方法: %s\n", ROUTE_TYPE_NAMES[route_type]);
                System.out.printf("=======================================\n");
                
                // パラメータnごとに実験を実施
                for (int param_n : PARAM_N) {
                    System.out.printf("\n===== パラメータn = %d の実験結果 =====\n", param_n);
                    
                    success = 0;
                    sum_success = 0; /* 評価指標を初期化 */
                    history.clear(); /* 通信履歴をクリア */
                    
                    // 初期化
                    for (i = 0; i < NODE_NUM; i++) {
                        for (j = 0; j < NODE_NUM; j++) {
                            bandwidth[i][j] = link[i][j];  // リンク容量を初期状態にコピー
                        }
                    }
                    
                    // SIM_COUNT回のシミュレーション
                    for (sim_time = 0; sim_time < SIM_COUNT; sim_time++) {
                        // ランダムに送受信ノードを決定
                        do {
                            src = rand.nextInt(NODE_NUM);
                            dest = rand.nextInt(NODE_NUM);
                        } while (src == dest);
                        
                        // 経路選択方法に応じた経路計算
                        switch (route_type) {
                            case 0: // 最小ホップ経路を用いた固定経路
                                findShortestPath(graph, path, dist, chk, src, dest);
                                break;
                            case 1: // 最大路を用いた固定経路
                                findMaximumPath(graph, link, path, bottleneck, chk, src, dest);
                                break;
                            case 2: // 最小ホップを用いた要求時経路
                                findOnDemandShortestPath(graph, bandwidth, path, dist, chk, src, dest);
                                break;
                            case 3: // 最大路を用いた要求時経路
                                findOnDemandMaximumPath(graph, bandwidth, path, bottleneck, chk, src, dest);
                                break;
                        }
                        
                        // 通信オブジェクトを作成
                        Communication comm = new Communication(src, dest);
                        comm.setPath(path); // 経路情報を設定
                        
                        // 経路が見つからなかった場合はスキップ
                        if (comm.path.isEmpty()) {
                            history.add(comm);
                            continue;
                        }
                        
                        // 経路上のリンク容量をチェック
                        boolean canEstablish = true;
                        for (int idx = 0; idx < comm.path.size() - 1; idx++) {
                            int node1 = comm.path.get(idx);
                            int node2 = comm.path.get(idx + 1);
                            if (bandwidth[node1][node2] < 1) {
                                canEstablish = false;
                                break;
                            }
                        }
                        
                        if (canEstablish) {
                            // 通信を確立できる場合、経路上のリンク容量を1Mbps減少
                            for (int idx = 0; idx < comm.path.size() - 1; idx++) {
                                int node1 = comm.path.get(idx);
                                int node2 = comm.path.get(idx + 1);
                                bandwidth[node1][node2]--;
                                bandwidth[node2][node1]--;
                            }
                            comm.established = true;
                            success++;
                        }
                        
                        // 通信履歴に追加
                        history.add(comm);
                        
                        // n回前の通信が終了した場合、リンク容量を増加
                        if (history.size() > param_n) {
                            Communication oldComm = history.get(history.size() - param_n - 1);
                            if (oldComm.established) {
                                // 経路上のリンク容量を1Mbps増加
                                for (int idx = 0; idx < oldComm.path.size() - 1; idx++) {
                                    int node1 = oldComm.path.get(idx);
                                    int node2 = oldComm.path.get(idx + 1);
                                    bandwidth[node1][node2]++;
                                    bandwidth[node2][node1]++;
                                }
                            }
                        }
                    }
                    
                    // 呼損率を計算
                    double blockingRate = (double)(SIM_COUNT - success) / SIM_COUNT;
                    System.out.printf("確立できた通信数: %d / %d\n", success, SIM_COUNT);
                    System.out.printf("呼損率: %.4f\n", blockingRate);
                }
            }
            
            return; // シミュレーション終了
        }

        /*
         * シミュレーション評価の結果出力
         */
        System.out.printf("\naverage = %f\n", sum_success / 1000.0); /* 平均を表示 */
    }
}