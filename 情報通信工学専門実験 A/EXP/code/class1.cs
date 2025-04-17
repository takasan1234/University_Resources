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

        // int k = int.Parse(args[2]);
        int k = 2;
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

        // 重心の表示(デバッグ用：あとで消す。)
        Console.WriteLine("重心の更新:");
        for (int i = 0; i < k; i++)
        {
            Console.WriteLine($"最終的な重心 {i}: ({centroid[i, 0]}, {centroid[i, 1]})");
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
    
}
