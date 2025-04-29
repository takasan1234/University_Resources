// 変換元 C コードと同じ処理を C# で実装
using System;
using System.IO;
using System.Linq;


enum PointType {
    Core,
    Border,
    Noise
}

class Point {
    public double[,] data;  // [1,2]を[,]に修正
    public PointType type;
    public bool is_visited;
    public int cluster_id;

    public Point(double[,] data){  // [1,2]を[,]に修正
        this.data = data;
        this.type = PointType.Noise;
        this.is_visited = false;
        this.cluster_id = -1;
    }
    public void set_core(double[,] data){  // [1,2]を[,]に修正
        this.data = data;
    }
    public void set_visited(bool is_visited){
        this.is_visited = is_visited;
    }
    public void set_cluster_id(int cluster_id){
        this.cluster_id = cluster_id;
    }
}


class Program
{
    // データ自体の情報
    public static double[,] data = new double[200, 2];   // データ (最大 200 行×2 列)
    public static int[]    label = new int[200];         // ラベル (未使用。元コードと同じく初期化のみ)


    // DBSCANに必要なパラメータ
    public static double epsilon = 0.3;   // 半径   
    public static int min_points = 2;   // 最小点数
    public static Point[] points = new Point[200];   // 点群
    public static int cluster_id = 1;   // クラスタID


    static void Main(string[] args)
    {
        if (args.Length < 2)
        {
            Console.WriteLine("使い方: Program <input-file> <output-file>");
            return;
        }

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

        // データをPoint型に変換
        for (int i = 0; i < 200; i++){
            points[i] = new Point(new double[1, 2] { { data[i, 0], data[i, 1] } });
        }

        Console.WriteLine("==========クラスタリング開始==========");
        for (int i = 0; i < 200; i++){
            if (points[i].is_visited) continue;
            if (checkAndExpandCluster(points[i])){
                cluster_id++;
            }
        }

        // cluster_idをlabel配列にコピー
        for (int i = 0; i < 200; i++) {
            label[i] = points[i].cluster_id;
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


    private static double calc_distance(double[,] A, double[,] B){  // double[]をdouble[,]に修正
        return Math.Sqrt(Math.Pow(A[0,0] - B[0,0], 2) +
                         Math.Pow(A[0,1] - B[0,1], 2));
    }

    private static bool checkAndExpandCluster(Point point){
        if (point.is_visited) return false;
        point.is_visited = true;
        Point[] neighbors = epsilonNeighborhood(point);
        int neighborCount = neighbors.Count(n => n != null);  // 実際の近傍点数を計算
        if (neighborCount >= min_points){
            point.cluster_id = cluster_id;
            point.type = PointType.Core;
            for (int j = 0; j < neighborCount; j++){
                if (neighbors[j] != null) {
                    neighbors[j].cluster_id = cluster_id;
                    neighbors[j].type = PointType.Border;
                    checkAndExpandCluster(neighbors[j]);
                }
            }
            return true;
        }
        return false;
    }

    // 純粋にepsilon以内にある点を返す
    private static Point[] epsilonNeighborhood(Point point){
        Point[] neighbors = new Point[200];
        int neighbor_count = 0;

        for (int i = 0; i < points.Length; i++){
            if (calc_distance(point.data, points[i].data) <= epsilon){
                neighbors[neighbor_count] = points[i];
                neighbor_count++;
            }
        }
        return neighbors;
    }
}