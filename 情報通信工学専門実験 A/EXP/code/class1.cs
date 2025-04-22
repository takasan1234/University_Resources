// 変換元 C コードと同じ処理を C# で実装
using System;
using System.IO;

class Program
{
    static void Main(string[] args)
    {
        if (args.Length < 2)
        {
            Console.WriteLine("使い方: Program <input-file> <output-file>");
            return;
        }

        // データの初期化(データはまだ格納されてない)
        double[,] data = new double[200, 2];   // データ (最大 200 行×2 列)
        int[]    label = new int[200];         // ラベル (未使用。元コードと同じく初期化のみ)
        int count = 0;

        // データの読み込み
        try
        {
            using (var fp_in = new StreamReader(args[0]))
            {
                string line;
                while (count < 200 && (line = fp_in.ReadLine()) != null)
                {
                    var parts = line.Split(',');
                    if (parts.Length != 2) continue; // 不正行をスキップ

                    if (double.TryParse(parts[0], out double x) &&
                        double.TryParse(parts[1], out double y))
                    {
                        data[count, 0] = x;
                        data[count, 1] = y;
                        count++;
                    }
                }
            }
        }
        catch (IOException)
        {
            Console.WriteLine("fail: cannot open the input-file. Change the name of input-file.");
            return;
        }

        // 外れ値検出のパラメータ設定
        int k_neighbors = 10; // k-近傍の数

        // 各データポイントのLOF値を計算
        double[] lof_values = new double[count];
        Console.WriteLine("各データポイントのLOF値:");
        for (int i = 0; i < count; i++)
        {
            double[] current_point = new double[] { data[i, 0], data[i, 1] };
            lof_values[i] = local_outlier_factor(data, label, k_neighbors, current_point);
            Console.WriteLine($"データポイント ({data[i, 0]}, {data[i, 1]}) の LOF値: {lof_values[i]}");
        }

        // LOFの値に基づいて外れ値を判定する閾値（例）
        double threshold = 1.5;
        Console.WriteLine("\n外れ値判定結果:");
        for (int i = 0; i < count; i++)
        {
            if (lof_values[i] > threshold)
            {
                Console.WriteLine($"データポイント ({data[i, 0]}, {data[i, 1]}) は外れ値です。LOF値: {lof_values[i]}");
            }
        }

        // int k = int.Parse(args[2]);
        int k = 3;
        double[,] centroid = new double[k, 2];

        // 重心の初期化
        Random rand = new Random();
        for (int i = 0; i < k; i++)
        {
            // 純粋にランダムに選択した場合、全てdataのラベルが同じになる可能性があるため
            int r = rand.Next(count);
            centroid[i, 0] = data[r, 0];
            centroid[i, 1] = data[r, 1];
        }

        // 重心の表示(デバッグ用：あとで消す。)
        Console.WriteLine("重心の初期化:");
        for (int i = 0; i < k; i++)
        {
            Console.WriteLine($"重心 {i}: ({centroid[i, 0]}, {centroid[i, 1]})");
        }

        // クラスタリング
        for(int iteration = 0; iteration < 1000; iteration++) {
            for (int i = 0; i < 200; i++)
            {
                double min_dist = double.MaxValue;
                int min_cluster = -1;

                for (int j = 0; j < k; j++)
                {
                    // データ(i番目)と重心(j番目)の距離を計算
                    double dist = Math.Sqrt(Math.Pow(data[i, 0] - centroid[j, 0], 2) +
                                            Math.Pow(data[i, 1] - centroid[j, 1], 2));
                    if (dist < min_dist)
                    {
                        min_dist = dist;
                        min_cluster = j;
                    }
                }

                // データ(i番目)をクラスタ(min_cluster番目)に割り当て
                label[i] = min_cluster;
            }

            // 重心の更新
            for (int j = 0; j < k; j++)
            {
                centroid[j, 0] = calc_centroid(data, label, j)[0];
                centroid[j, 1] = calc_centroid(data, label, j)[1];
            }
        }


        // 出力ファイルの作成
        try
        {
            using (var fp_out = new StreamWriter(args[1], false))
            {
                for (int i = 0; i < 200; i++)
                {
                    fp_out.WriteLine($"{data[i,0]},{data[i,1]},{label[i]}");
                }
            }
        }
        catch (IOException)
        {
            Console.WriteLine("fail: cannot open the output-file. Change the name of output-file.");
            return;
        }
    }

    // k番目の重心を計算するメソッド k=2ならlabel[0]とlabel[1]の重心を計算する
    private static double[] calc_centroid(double[,] data, int[] label, int k)
    {
        double[] centroid = new double[2];
        double[] sum = new double[2];
        int valid_count = 0;

        for (int i = 0; i < 200; i++)
        {
            if (label[i] == k){
                sum[0] += data[i, 0];
                sum[1] += data[i, 1];
                valid_count++;
            }
        }
        centroid[0] = sum[0] / valid_count;
        centroid[1] = sum[1] / valid_count;
        return centroid;
    }

    // LOF(外れ値の検知)の計算
    private static double local_outlier_factor(double[,] data, int[] label, int k_neighbors, double[] A){
        double lrd = local_reachability_density(data, label, k_neighbors, A);
        double k_dist = k_distance(data, label, k_neighbors, A);
        double[,] nearest_neighbors = FindKNearestNeighbors(data, label, k_neighbors, A);

        double lof = 0;
        double bunshi = 0;
        for(int i=0; i<k_neighbors; i++){
            double[] neighbor = new double[] { nearest_neighbors[i, 0], nearest_neighbors[i, 1] };
            bunshi += local_reachability_density(data, label, k_neighbors, neighbor) / k_neighbors;
        }
        lof = bunshi / lrd;
        return lof;
    }

    // lrd(局所到達可能性密度)の計算
    private static double local_reachability_density(double[,] data, int[] label, int k_neighbors, double[] A){
        double[,] nearest_neighbors = FindKNearestNeighbors(data, label, k_neighbors, A);
        double reach_dist_sum = 0;
        for(int i=0; i<k_neighbors; i++){
            double[] neighbor = new double[] { nearest_neighbors[i, 0], nearest_neighbors[i, 1] };
            reach_dist_sum += reach_dist_k(data, label, k_neighbors, A, neighbor);
        }
        return k_neighbors / reach_dist_sum;
    }

    // k_distanceの計算
    private static double k_distance(double[,] data, int[] label, int k_neighbors, double[] A){
        double[,] k_nearest_neighbors = FindKNearestNeighbors(data, label, k_neighbors, A);
        double[] last_neighbor = new double[] { k_nearest_neighbors[k_neighbors-1, 0], k_nearest_neighbors[k_neighbors-1, 1] };
        double distance = calc_distance(A, last_neighbor);
        return distance;
    }

    // 1〜k番目の最近傍点を求める。戻り値は、k_nearest_neighbors[k, 2]の配列で、距離が小さい順に格納している
    private static double[,] FindKNearestNeighbors(double[,] data, int[] label, int k_neighbors, double[] A){
        double[] distances = new double[200];
        double[,] k_nearest_neighbors = new double[k_neighbors, 2];
        for (int i = 0; i < 200; i++){
            distances[i] = Math.Sqrt(Math.Pow(data[i, 0] - A[0], 2) +
                                     Math.Pow(data[i, 1] - A[1], 2));
        }
        for (int i = 0; i < k_neighbors; i++){
            double min_distance = double.MaxValue;
            int min_index = -1;
            for (int j = 0; j < 200; j++){
                if (distances[j] < min_distance){
                    min_distance = distances[j];
                    min_index = j;
                }
            }
            distances[min_index] = double.MaxValue;
            k_nearest_neighbors[i, 0] = data[min_index, 0];
            k_nearest_neighbors[i, 1] = data[min_index, 1];
        }
        return k_nearest_neighbors;
    }

    private static double calc_distance(double[] A, double[] B){
        return Math.Sqrt(Math.Pow(A[0] - B[0], 2) +
                         Math.Pow(A[1] - B[1], 2));
    }

    private static double reach_dist_k(double[,] data, int[] label, int k_neighbors, double[] A, double[] B){
        return Math.Max(calc_distance(A, B), k_distance(data, label, k_neighbors, B));
    }
}