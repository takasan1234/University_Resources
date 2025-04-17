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

        double[,] data = new double[200, 2];   // データ (最大 200 行×2 列)
        int[]    label = new int[200];         // ラベル (未使用。元コードと同じく初期化のみ)
        int count = 0;

        

        /* -------- Input -------- */
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

        /* -------- k-means -------- */
        // ここにクラスタリング処理を実装する
        // （元コードでは未実装のため、空のまま保持）

        /* -------- Output -------- */
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
}
