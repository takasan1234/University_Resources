// 相関ルールマイニング (Aprioriアルゴリズム) の実装
using System;
using System.IO;
using System.Linq;
using System.Text;
using System.Collections.Generic;

namespace AssociationRuleMining
{
    class Program
    {
        // 最小支持度と最小信頼度の閾値
        private const double MIN_SUPPORT = 0.1;     // 10%
        private const double MIN_CONFIDENCE = 0.5;  // 50%
        private const double MIN_LIFT = 1.0;        // リフト値の最小値

        static void Main(string[] args)
        {
            // コマンドライン引数のチェック
            if (args.Length < 2)
            {
                Console.WriteLine("使用方法: assoc-rule-mining.exe <入力ファイル> <出力ファイル>");
                return;
            }

            string inputFile = args[0];
            string outputFile = args[1];

            try
            {
                // トランザクションデータの読み込み
                List<HashSet<string>> transactions = ReadTransactions(inputFile);
                int totalTransactions = transactions.Count;

                Console.WriteLine($"トランザクション数: {totalTransactions}");
                
                // 頻出アイテム集合の抽出（Aprioriアルゴリズム）
                Dictionary<string, int> frequentItemsets = FindFrequentItemsets(transactions);
                
                // 相関ルールの生成
                List<AssociationRule> rules = GenerateRules(frequentItemsets, totalTransactions);
                
                // 結果の出力
                SaveResults(rules, outputFile);
                
                Console.WriteLine($"抽出された頻出アイテム集合数: {frequentItemsets.Count}");
                Console.WriteLine($"生成された相関ルール数: {rules.Count}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"エラーが発生しました: {ex.Message}");
                Console.WriteLine($"スタックトレース: {ex.StackTrace}");
            }
        }

        // CSVファイルからトランザクションデータを読み込む
        static List<HashSet<string>> ReadTransactions(string filePath)
        {
            List<HashSet<string>> transactions = new List<HashSet<string>>();
            
            using (StreamReader reader = new StreamReader(filePath))
            {
                string line;
                while ((line = reader.ReadLine()) != null)
                {
                    if (string.IsNullOrWhiteSpace(line)) continue;
                    
                    // カンマで区切られたアイテムをHashSetに格納
                    HashSet<string> transaction = new HashSet<string>(
                        line.Split(',')
                            .Select(item => item.Trim())
                            .Where(item => !string.IsNullOrWhiteSpace(item))
                    );
                    
                    if (transaction.Count > 0)
                    {
                        transactions.Add(transaction);
                    }
                }
            }
            
            return transactions;
        }

        // Aprioriアルゴリズムによる頻出アイテム集合の抽出
        static Dictionary<string, int> FindFrequentItemsets(List<HashSet<string>> transactions)
        {
            int totalTransactions = transactions.Count;
            int minSupportCount = (int)Math.Ceiling(MIN_SUPPORT * totalTransactions);

            Console.WriteLine($"最小支持度カウント: {minSupportCount}");

            // すべてのユニークアイテムの取得
            HashSet<string> allItems = new HashSet<string>();
            foreach (var transaction in transactions)
            {
                foreach (var item in transaction)
                {
                    allItems.Add(item);
                }
            }

            // 最終的な頻出アイテム集合の格納先（HashSetをソートしたキー文字列として保存）
            Dictionary<string, int> frequentItemsets = new Dictionary<string, int>();
            Dictionary<string, HashSet<string>> itemsetMap = new Dictionary<string, HashSet<string>>();

            // 頻出1-アイテム集合（L1）の生成
            Dictionary<string, int> L1 = new Dictionary<string, int>();
            foreach (var item in allItems)
            {
                HashSet<string> itemset = new HashSet<string> { item };
                int count = CountSupport(itemset, transactions);
                
                if (count >= minSupportCount)
                {
                    string key = GetItemsetKey(itemset);
                    L1.Add(key, count);
                    frequentItemsets.Add(key, count);
                    itemsetMap[key] = itemset;
                }
            }

            Console.WriteLine($"頻出1-アイテム集合数: {L1.Count}");

            // L(k-1)からL(k)を生成
            Dictionary<string, int> Lk = L1;
            Dictionary<string, HashSet<string>> LkMap = new Dictionary<string, HashSet<string>>(itemsetMap);
            int k = 2;

            while (Lk.Count > 0)
            {
                // 候補生成: L(k-1)からCkを生成
                Dictionary<string, HashSet<string>> candidates = GenerateCandidates(LkMap, k);
                
                // 支持度カウント
                Dictionary<string, int> nextLk = new Dictionary<string, int>();
                Dictionary<string, HashSet<string>> nextLkMap = new Dictionary<string, HashSet<string>>();
                
                foreach (var candidateEntry in candidates)
                {
                    string key = candidateEntry.Key;
                    HashSet<string> candidate = candidateEntry.Value;
                    
                    int count = CountSupport(candidate, transactions);
                    
                    if (count >= minSupportCount)
                    {
                        nextLk.Add(key, count);
                        frequentItemsets.Add(key, count);
                        nextLkMap[key] = candidate;
                        itemsetMap[key] = candidate;
                    }
                }
                
                Lk = nextLk;
                LkMap = nextLkMap;
                Console.WriteLine($"頻出{k}-アイテム集合数: {Lk.Count}");
                k++;
                
                // 候補がなくなったら終了
                if (Lk.Count == 0) break;
            }
            
            return frequentItemsets;
        }

        // 候補生成 (L(k-1)からCkを生成)
        static Dictionary<string, HashSet<string>> GenerateCandidates(Dictionary<string, HashSet<string>> Lk, int k)
        {
            Dictionary<string, HashSet<string>> candidates = new Dictionary<string, HashSet<string>>();
            
            // L(k-1)のアイテム集合のリスト
            List<HashSet<string>> itemsets = Lk.Values.ToList();
            
            for (int i = 0; i < itemsets.Count; i++)
            {
                for (int j = i + 1; j < itemsets.Count; j++)
                {
                    HashSet<string> set1 = itemsets[i];
                    HashSet<string> set2 = itemsets[j];
                    
                    // 最初のk-2要素が同じ集合のみ結合する
                    if (SharesFirstKMinus2Elements(set1, set2, k))
                    {
                        // 新しいk-アイテム集合を生成
                        HashSet<string> candidate = new HashSet<string>(set1);
                        foreach (var item in set2)
                        {
                            candidate.Add(item);
                        }
                        
                        // 候補アイテム集合のサイズがkであれば追加
                        if (candidate.Count == k)
                        {
                            // プルーニング: すべての部分集合が頻出である必要がある
                            bool allSubsetsFrequent = true;
                            foreach (var subset in GetAllSubsets(candidate, k - 1))
                            {
                                string subsetKey = GetItemsetKey(subset);
                                if (!Lk.ContainsKey(subsetKey))
                                {
                                    allSubsetsFrequent = false;
                                    break;
                                }
                            }
                            
                            if (allSubsetsFrequent)
                            {
                                string key = GetItemsetKey(candidate);
                                if (!candidates.ContainsKey(key))
                                {
                                    candidates.Add(key, candidate);
                                }
                            }
                        }
                    }
                }
            }
            
            return candidates;
        }

        // 最初のk-2要素が同じか確認
        static bool SharesFirstKMinus2Elements(HashSet<string> set1, HashSet<string> set2, int k)
        {
            if (k <= 2) return true; // k=2の場合は常にtrue
            
            // k-1アイテム集合の要素数がk-1であることを確認
            if (set1.Count != k - 1 || set2.Count != k - 1) return false;
            
            // 最初のk-2要素が同じかどうかをチェック
            HashSet<string> intersection = new HashSet<string>(set1);
            intersection.IntersectWith(set2);
            
            return intersection.Count == k - 2;
        }

        // サイズkのすべての部分集合を生成
        static List<HashSet<string>> GetAllSubsets(HashSet<string> itemset, int k)
        {
            List<HashSet<string>> subsets = new List<HashSet<string>>();
            GetSubsets(itemset.ToList(), k, 0, new List<string>(), subsets);
            return subsets;
        }

        // 再帰的に部分集合を生成
        static void GetSubsets(List<string> items, int k, int start, List<string> current, List<HashSet<string>> result)
        {
            if (current.Count == k)
            {
                result.Add(new HashSet<string>(current));
                return;
            }
            
            for (int i = start; i < items.Count; i++)
            {
                current.Add(items[i]);
                GetSubsets(items, k, i + 1, current, result);
                current.RemoveAt(current.Count - 1);
            }
        }

        // 支持度を計算（トランザクション中の出現回数）
        static int CountSupport(HashSet<string> itemset, List<HashSet<string>> transactions)
        {
            int count = 0;
            
            foreach (var transaction in transactions)
            {
                bool containsAll = true;
                
                foreach (var item in itemset)
                {
                    if (!transaction.Contains(item))
                    {
                        containsAll = false;
                        break;
                    }
                }
                
                if (containsAll)
                {
                    count++;
                }
            }
            
            return count;
        }

        // アイテム集合から一意のキーを生成
        static string GetItemsetKey(HashSet<string> itemset)
        {
            return string.Join(",", itemset.OrderBy(i => i));
        }

        // 相関ルールの生成
        static List<AssociationRule> GenerateRules(Dictionary<string, int> frequentItemsets, int totalTransactions)
        {
            List<AssociationRule> rules = new List<AssociationRule>();
            
            // アイテム集合をキーから復元
            Dictionary<string, HashSet<string>> itemsetMap = new Dictionary<string, HashSet<string>>();
            foreach (var key in frequentItemsets.Keys)
            {
                itemsetMap[key] = new HashSet<string>(key.Split(','));
            }
            
            // 2つ以上のアイテムを持つ頻出アイテム集合からルールを生成
            foreach (var entry in frequentItemsets)
            {
                string itemsetKey = entry.Key;
                int itemsetSupport = entry.Value;
                HashSet<string> itemset = itemsetMap[itemsetKey];
                
                if (itemset.Count >= 2)
                {
                    // すべての非空の真部分集合をantecedent（前提）として試す
                    List<HashSet<string>> allSubsets = new List<HashSet<string>>();
                    for (int i = 1; i < itemset.Count; i++)
                    {
                        GetSubsets(itemset.ToList(), i, 0, new List<string>(), allSubsets);
                    }
                    
                    foreach (var antecedent in allSubsets)
                    {
                        // 帰結部（consequent）の計算
                        HashSet<string> consequent = new HashSet<string>(itemset);
                        consequent.ExceptWith(antecedent);
                        
                        // 前提部の支持度を取得
                        string antecedentKey = GetItemsetKey(antecedent);
                        int antecedentSupport = 0;
                        if (frequentItemsets.ContainsKey(antecedentKey))
                        {
                            antecedentSupport = frequentItemsets[antecedentKey];
                        }
                        else
                        {
                            // 前提部がfrequentItemsetsに含まれていない場合はスキップ
                            continue;
                        }
                        
                        // 帰結部の支持度を取得
                        string consequentKey = GetItemsetKey(consequent);
                        int consequentSupport = 0;
                        if (frequentItemsets.ContainsKey(consequentKey))
                        {
                            consequentSupport = frequentItemsets[consequentKey];
                        }
                        else
                        {
                            // 帰結部がfrequentItemsetsに含まれていない場合はスキップ
                            continue;
                        }
                        
                        // 信頼度の計算 confidence = support(itemset) / support(antecedent)
                        double confidence = (double)itemsetSupport / antecedentSupport;
                        
                        // リフトの計算 lift = confidence / support(consequent)
                        double lift = confidence / ((double)consequentSupport / totalTransactions);
                        
                        // 最小信頼度とリフト値をチェック
                        if (confidence >= MIN_CONFIDENCE && lift >= MIN_LIFT)
                        {
                            // 相関ルールの作成
                            AssociationRule rule = new AssociationRule
                            {
                                Antecedent = antecedent,
                                Consequent = consequent,
                                Support = (double)itemsetSupport / totalTransactions,
                                Confidence = confidence,
                                Lift = lift
                            };
                            
                            rules.Add(rule);
                        }
                    }
                }
            }
            
            // 信頼度の降順でソート
            return rules.OrderByDescending(r => r.Confidence).ToList();
        }

        // 結果を出力ファイルに保存
        static void SaveResults(List<AssociationRule> rules, string outputFile)
        {
            using (StreamWriter writer = new StreamWriter(outputFile))
            {
                // ヘッダーの書き込み
                writer.WriteLine("Antecedent,Consequent,Support,Confidence,Lift");
                
                // 各ルールの書き込み
                foreach (var rule in rules)
                {
                    string antecedent = string.Join(" & ", rule.Antecedent);
                    string consequent = string.Join(" & ", rule.Consequent);
                    
                    writer.WriteLine($"{antecedent},{consequent},{rule.Support:F4},{rule.Confidence:F4},{rule.Lift:F4}");
                }
            }
            
            Console.WriteLine($"結果を {outputFile} に保存しました");
        }
    }

    // 相関ルールのクラス定義
    class AssociationRule
    {
        public HashSet<string> Antecedent { get; set; }  // 前提部
        public HashSet<string> Consequent { get; set; }  // 帰結部
        public double Support { get; set; }              // 支持度
        public double Confidence { get; set; }           // 信頼度
        public double Lift { get; set; }                 // リフト値
    }
}
