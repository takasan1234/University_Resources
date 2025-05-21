import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;
import java.util.Scanner;
import java.util.ArrayList;
import java.util.List;
import java.util.Collections;
import java.util.Arrays;

public class dijkstra {
    /* 定数定義 */
    static final int NODE_NUM = 10;   /* 総ノード数 */
    static final int MAX = Integer.MAX_VALUE;      /* 無限大に相当する数 */
    static final int FLAG = 1;        /* Dijkstraのテストの場合は0に、シミュレーション評価を行う場合は1にする */
    static final int ROUTE_TYPE = 1;  /* 経路選択方法：0=最短路、1=最大路、2=要求時最短路、3=要求時最大路、4=空き容量逆数、5=最短最大路 */
    static final int SIM_COUNT = 10000; /* シミュレーション回数 */
    static final int[] PARAM_N = {5, 6, 7, 8, 9, 10, 20, 50, 100}; /* テストするパラメータnの値 */
    static final double[] LAMBDA_VALUES = {0.0001, 0.001, 0.01, 0.1, 1.0}; /* 複数の指数分布のレート（λ）パラメータ */
    static final int TIME_MODEL = 1;  /* 時間モデル：0=指数分布、1=単純なn回前リソース解放 */
    static final String[] ROUTE_TYPE_NAMES = {
        "最小ホップ経路を用いた固定経路",
        "最大路を用いた固定経路",
        "最小ホップを用いた要求時経路",
        "最大路を用いた要求時経路",
        "空き容量の逆数を考慮した経路",
        "最短最大路（Shortest Widest Path）"
    };
    static final String[] TIME_MODEL_NAMES = {
        "指数分布モデル",
        "単純なn回前リソース解放モデル"
    };

    /* 指数分布に基づく乱数生成メソッド */
    private static double generateExponentialRandom(Random random, double lambda) {
        // 指数分布の逆関数法を使用
        return -Math.log(1.0 - random.nextDouble()) / lambda;
    }

    /* 通信履歴を管理するクラス */
    static class Communication {
        int src;           // 送信元ノード
        int dest;          // 宛先ノード
        List<Integer> path; // 経路上のノード
        boolean established; // 通信が確立したかどうか
        double arrivalTime; // 通信の到着時間
        double holdingTime; // 通信の保持時間

        public Communication(int src, int dest) {
            this.src = src;
            this.dest = dest;
            this.path = new ArrayList<>();
            this.established = false;
            this.arrivalTime = 0.0;
            this.holdingTime = 0.0;
        }

        public Communication(int src, int dest, double arrivalTime, double holdingTime) {
            this.src = src;
            this.dest = dest;
            this.path = new ArrayList<>();
            this.established = false;
            this.arrivalTime = arrivalTime;
            this.holdingTime = holdingTime;
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

    /* リンク情報を格納するクラス */
    static class Link implements Comparable<Link> {
        int node1;
        int node2;
        int capacity;

        public Link(int node1, int node2, int capacity) {
            this.node1 = node1;
            this.node2 = node2;
            this.capacity = capacity;
        }

        @Override
        public int compareTo(Link other) {
            // 容量の大きい順にソート
            return Integer.compare(other.capacity, this.capacity);
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

    /* 深さ優先探索で経路を探す */
    private static boolean dfs(int[][] graph, boolean[] visited, int[] path, int current, int dest) {
        if (current == dest) {
            return true;
        }

        visited[current] = true;

        for (int next = 0; next < NODE_NUM; next++) {
            if (graph[current][next] > 0 && !visited[next]) {
                path[next] = current;
                if (dfs(graph, visited, path, next, dest)) {
                    return true;
                }
            }
        }

        return false;
    }

    /* 最大路の計算（ボトルネックリンクが最大の経路を求める） */
    public static void findMaximumPath(int[][] graph, int[][] link, int[] path, int[] bottleneck, int[] chk, int src, int dest) {
        // リンクのリストを作成
        List<Link> links = new ArrayList<>();
        for (int i = 0; i < NODE_NUM; i++) {
            for (int j = i + 1; j < NODE_NUM; j++) {
                if (link[i][j] > 0) {
                    links.add(new Link(i, j, link[i][j]));
                }
            }
        }

        // リンクを容量の大きい順にソート
        Collections.sort(links);

        // 経路探索用の一時グラフ
        int[][] tempGraph = new int[NODE_NUM][NODE_NUM];
        boolean[] visited = new boolean[NODE_NUM];
        int currentBottleneck = 0;

        // 容量の大きいリンクから順にグラフを構築
        for (int i = 0; i < links.size(); i++) {
            // 現在のリンクの容量をボトルネック容量の候補とする
            currentBottleneck = links.get(i).capacity;

            // 同じ容量を持つリンクを全て追加
            while (i < links.size() && links.get(i).capacity == currentBottleneck) {
                Link currentLink = links.get(i);
                tempGraph[currentLink.node1][currentLink.node2] = 1;
                tempGraph[currentLink.node2][currentLink.node1] = 1;  // 無向グラフなので両方向に追加
                i++;
            }
            i--; // whileループで余分にインクリメントされた分を戻す

            // 経路探索
            Arrays.fill(visited, false);
            Arrays.fill(path, NODE_NUM);
            path[src] = src;

            if (dfs(tempGraph, visited, path, src, dest)) {
                // 経路が見つかった場合、この容量が最大ボトルネック容量
                for (int j = 0; j < NODE_NUM; j++) {
                    bottleneck[j] = currentBottleneck;
                }
                return;
            }
        }

        // 経路が見つからなかった場合
        Arrays.fill(bottleneck, 0);
        Arrays.fill(path, NODE_NUM);
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

    /* 空き容量の逆数を考慮した経路選択 */
    public static void findInverseCapacityPath(int[][] graph, int[][] bandwidth, int[] path, int[] dist, int[] chk, int src, int dest) {
        int i, tmp_node, tmp_dist, fin;
        double[][] inverseGraph = new double[NODE_NUM][NODE_NUM]; // 空き容量の逆数を格納するグラフ
        
        /* 空き容量の逆数でグラフを初期化 */
        for (i = 0; i < NODE_NUM; i++) {
            for (int j = 0; j < NODE_NUM; j++) {
                if (graph[i][j] < MAX && bandwidth[i][j] >= 1) {
                    // 空き容量が1Mbps以上あるリンクのみを使用
                    inverseGraph[i][j] = 1.0 / bandwidth[i][j]; // 空き容量の逆数を重みとする
                } else {
                    inverseGraph[i][j] = MAX; // 使用できないリンク
                }
            }
        }
        
        /* 初期化 */
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
        
        /* Dijkstraアルゴリズムで最小コスト経路を探索 */
        while (fin == 0) {
            for (i = 0; i < NODE_NUM; i++) {
                if (inverseGraph[tmp_node][i] < MAX && chk[i] == 0) {
                    int newDist = (int)(dist[tmp_node] + inverseGraph[tmp_node][i] * 1000); // 小数を整数に変換
                    if (dist[i] > newDist) {
                        dist[i] = newDist;
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

    /* 最短最大路（Shortest Widest Path）の計算 */
    public static void findShortestWidestPath(int[][] graph, int[][] bandwidth, int[] path, int[] dist, int[] chk, int src, int dest) {
        int i, j;
        int[] bottleneck = new int[NODE_NUM];
        int maxBottleneck;

        // Step 1: 最大帯域幅を持つ経路を見つける
        findOnDemandMaximumPath(graph, bandwidth, path, bottleneck, chk, src, dest);
        maxBottleneck = bottleneck[dest];

        // 経路が見つからない場合は終了
        if (maxBottleneck == 0) {
            Arrays.fill(path, NODE_NUM);
            Arrays.fill(dist, MAX);
            return;
        }

        // Step 2: 最大帯域幅以上の容量を持つリンクのみを使用して最短経路を計算
        int[][] filteredGraph = new int[NODE_NUM][NODE_NUM];
        for (i = 0; i < NODE_NUM; i++) {
            for (j = 0; j < NODE_NUM; j++) {
                if (graph[i][j] < MAX && bandwidth[i][j] >= maxBottleneck) {
                    // 最大帯域幅以上の容量を持つリンクのみを使用
                    filteredGraph[i][j] = graph[i][j];
                } else {
                    filteredGraph[i][j] = MAX;
                }
            }
        }

        // 最短経路を計算
        findShortestPath(filteredGraph, path, dist, chk, src, dest);
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
            Scanner stdin = new Scanner(System.in);
            System.out.printf("Source Node?(0-%d)", NODE_NUM - 1);
            src = stdin.nextInt();
            System.out.printf("Destination Node?(0-%d)", NODE_NUM - 1);
            dest = stdin.nextInt();
            // stdin.close();
        }

        if (FLAG == 1) {
            Random rand = new Random(System.currentTimeMillis()); /* 乱数の初期化 */
            
            // 時間モデルの表示
            System.out.printf("\n=======================================\n");
            System.out.printf("時間モデル: %s\n", TIME_MODEL_NAMES[TIME_MODEL]);
            System.out.printf("=======================================\n");
            
            // 各LAMBDAに対してシミュレーションを実行
            for (double currentLambda : LAMBDA_VALUES) {
                System.out.printf("\n=======================================\n");
                System.out.printf("λ = %.5f のシミュレーション\n", currentLambda);
                System.out.printf("=======================================\n");
                
                // CSVファイル出力の準備
                String lambdaStr = String.format("%.5f", currentLambda).replace(".", "_");
                String csvFileName = TIME_MODEL == 0 
                    ? "results_exponential_lambda_" + lambdaStr + ".csv" 
                    : "results_simple_lambda_" + lambdaStr + ".csv";
                
                StringBuilder csvContent = new StringBuilder();
                // CSVヘッダー
                csvContent.append("n,min_hop_fixed,max_path_fixed,min_hop_demand,max_path_demand,inverse_capacity,shortest_widest\n");
                
                // パラメータnの結果を格納する配列
                double[][] results = new double[PARAM_N.length][6]; // n値ごとに6種類の経路選択方法の結果を保存
                
                // 各経路選択方法でシミュレーションを実行
                for (int route_type = 0; route_type < 6; route_type++) {
                    System.out.printf("\n=======================================\n");
                    System.out.printf("経路選択方法: %s\n", ROUTE_TYPE_NAMES[route_type]);
                    System.out.printf("=======================================\n");
                    
                    // パラメータnごとに実験を実施
                    for (int n_idx = 0; n_idx < PARAM_N.length; n_idx++) {
                        int param_n = PARAM_N[n_idx];
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
                        
                        final double[] currentTime = {0.0}; // 現在時刻（指数分布用）
                        
                        // SIM_COUNT回のシミュレーション
                        for (sim_time = 0; sim_time < SIM_COUNT; sim_time++) {
                            // 時間モデルに応じたリソース解放処理
                            if (TIME_MODEL == 0) {
                                // 指数分布モデル：終了した通信のリンク容量を回復
                                List<Communication> endedCommunications = new ArrayList<>();
                                for (Communication oldComm : history) {
                                    if (oldComm.established && 
                                        oldComm.arrivalTime + oldComm.holdingTime <= currentTime[0]) {
                                        // 通信終了時刻が現在時刻以前なら終了
                                        for (int idx = 0; idx < oldComm.path.size() - 1; idx++) {
                                            int node1 = oldComm.path.get(idx);
                                            int node2 = oldComm.path.get(idx + 1);
                                            bandwidth[node1][node2]++;
                                            bandwidth[node2][node1]++;
                                        }
                                        endedCommunications.add(oldComm);
                                    }
                                }
                                // 終了した通信を履歴から削除
                                history.removeAll(endedCommunications);
                            } else {
                                // 単純なn回前リソース解放モデル
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
                            
                            // 時間モデルに応じた処理
                            if (TIME_MODEL == 0) {
                                // 指数分布モデル
                                // 到着間隔を指数分布に基づいて生成
                                double interArrivalTime = generateExponentialRandom(rand, currentLambda);
                                currentTime[0] += interArrivalTime;
                            }
                            
                            // ランダムに送受信ノードを決定
                            do {
                                src = rand.nextInt(NODE_NUM);
                                dest = rand.nextInt(NODE_NUM);
                            } while (src == dest);
                            
                            // 通信保持時間を決定（時間モデルに応じて）
                            double holdingTime = 0.0;
                            if (TIME_MODEL == 0) {
                                // 指数分布モデル
                                holdingTime = generateExponentialRandom(rand, 1.0 / param_n); // パラメータnに応じた平均保持時間
                            }
                            
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
                                case 4: // 空き容量の逆数を考慮した経路
                                    findInverseCapacityPath(graph, bandwidth, path, dist, chk, src, dest);
                                    break;
                                case 5: // 最短最大路（Shortest Widest Path）
                                    findShortestWidestPath(graph, bandwidth, path, dist, chk, src, dest);
                                    break;
                            }
                            
                            // 通信オブジェクトを作成
                            Communication comm;
                            if (TIME_MODEL == 0) {
                                // 指数分布モデル
                                comm = new Communication(src, dest, currentTime[0], holdingTime);
                            } else {
                                // 単純なn回前リソース解放モデル
                                comm = new Communication(src, dest);
                            }
                            comm.setPath(path); // 経路情報を設定
                            
                            // デフォルトでは確立失敗とマークし、条件を満たせば成功に変更
                            comm.established = false;
                            
                            // 経路が見つかった場合のみリンク容量チェックを行う
                            if (!comm.path.isEmpty()) {
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
                            }
                            
                            // 通信履歴に追加
                            history.add(comm);
                        }
                        
                        // 呼損率を計算
                        double blockingRate = (double)(SIM_COUNT - success) / SIM_COUNT;
                        System.out.printf("確立できた通信数: %d / %d\n", success, SIM_COUNT);
                        System.out.printf("呼損率: %.4f\n", blockingRate);
                        
                        // 結果を配列に保存
                        results[n_idx][route_type] = blockingRate;
                    }
                }
                
                // CSVファイルに結果を書き込む
                for (int n_idx = 0; n_idx < PARAM_N.length; n_idx++) {
                    csvContent.append(PARAM_N[n_idx]);
                    for (int route_type = 0; route_type < 6; route_type++) {
                        csvContent.append(",").append(String.format("%.6f", results[n_idx][route_type]));
                    }
                    csvContent.append("\n");
                }
                
                // CSVファイルに書き込み
                try (FileWriter writer = new FileWriter(csvFileName)) {
                    writer.write(csvContent.toString());
                    System.out.println("シミュレーション結果をCSVファイルに保存しました: " + csvFileName);
                    
                    // グラフ作成のためのPythonスクリプトを実行
                    System.out.println("グラフを生成しています...");
                    ProcessBuilder pb = new ProcessBuilder("python", "plot_graph.py", csvFileName);
                    pb.redirectErrorStream(true);
                    Process process = pb.start();
                    
                    // プロセスの出力を読み取る
                    Scanner scanner = new Scanner(process.getInputStream());
                    while (scanner.hasNextLine()) {
                        System.out.println(scanner.nextLine());
                    }
                    scanner.close();
                } catch (IOException e) {
                    System.err.println("CSVファイルの書き込み中にエラーが発生しました: " + e.getMessage());
                    e.printStackTrace();
                }
            }
            
            // すべてのCSVファイルを比較するグラフも作成
            System.out.println("すべてのλ値を比較するグラフを生成しています...");
            if (TIME_MODEL == 0) {
                ProcessBuilder pb = new ProcessBuilder("python", "plot_graph.py", "compare_lambdas");
                pb.redirectErrorStream(true);
                try {
                    Process process = pb.start();
                    
                    // プロセスの出力を読み取る
                    Scanner scanner = new Scanner(process.getInputStream());
                    while (scanner.hasNextLine()) {
                        System.out.println(scanner.nextLine());
                    }
                    scanner.close();
                } catch (IOException e) {
                    System.err.println("比較グラフ作成中にエラーが発生しました: " + e.getMessage());
                    e.printStackTrace();
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