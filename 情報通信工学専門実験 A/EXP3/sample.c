#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

/*
 * マクロ定義
 */
#define min(A, B) ((A)<(B) ? (A) : (B))
#define max(A, B) ((A)>(B) ? (A) : (B))

/*
 * 画像構造体の定義
 */
typedef struct
{
    int width;              /* 画像の横方向の画素数 */
    int height;             /* 画像の縦方向の画素数 */
    int maxValue;           /* 画素の値(明るさ)の最大値 */
    unsigned char *data;    /* 画像の画素値データを格納する領域を指す */
                            /* ポインタ */
} image_t;

// 関数の前方宣言を追加
int calclateThreshold(image_t *resultImage, image_t *originalImage);

/*======================================================================
 * このプログラムに与えられた引数の解析
 *======================================================================
 */
void
parseArg(int argc, char **argv, FILE **infp, FILE **outfp, char **mode)
{     
    FILE *fp;

    /* 引数の個数をチェック */
    if (argc!=4)
    {
        goto usage;
    }

    /* モードを設定 */
    *mode = argv[1];

    *infp = fopen(argv[2], "rb"); /* 入力画像ファイルをバイナリモードで */
                                /* オープン */

    if (*infp==NULL)		/* オープンできない時はエラー */
    {
        fputs("Opening the input file was failend\n", stderr);
        goto usage;
    }

    *outfp = fopen(argv[3], "wb"); /* 出力画像ファイルをバイナリモードで */
                                /* オープン */

    if (*outfp==NULL)		/* オープンできない時はエラー */
    {
        fputs("Opening the output file was failend\n", stderr);
        goto usage;
    }

    return;

/* このプログラムの使い方の説明 */
usage:
    fprintf(stderr, "usage : %s <mode> <input pgm file> <output pgm file>\n", argv[0]);
    fprintf(stderr, "mode:\n");
    fprintf(stderr, "  edge    - エッジ強調のみ\n");
    fprintf(stderr, "  binary  - 二値化のみ\n");
    fprintf(stderr, "  both    - エッジ強調→二値化\n");
    exit(1);
}


/*======================================================================
 * 画像構造体の初期化
 *======================================================================
 * 画像構造体 image_t *ptImage の画素数(width × height)、階調数
 * (maxValue)を設定し、画素値データを格納するのに必要なメモリ領域を確
 * 保する。 
 */
void
initImage(image_t *ptImage, int width, int height, int maxValue)
{
    ptImage->width = width;
    ptImage->height = height;
    ptImage->maxValue = maxValue;

    /* メモリ領域の確保 */
    ptImage->data = (unsigned char *)malloc((size_t)(width * height));

    if (ptImage->data==NULL)    /* メモリ確保ができなかった時はエラー */
    {
        fputs("out of memory\n", stderr);
        exit(1);
    }
}


/*======================================================================
 * 文字列一行読み込み関数
 *======================================================================
 *   FILE *fp から、改行文字'\n'が表れるまで文字を読み込んで、char型の
 * メモリ領域 char *buf に格納する。1行の長さが n 文字以上の場合は、先
 * 頭から n-1 文字だけを読み込む。
 *   読み込んだ文字列の先頭が '#' の場合は、さらに次の行を読み込む。
 *   正常に読み込まれた場合は、ポインタ buf を返し、エラーや EOF (End
 * Of File) の場合は NULL を返す。
 */
char *
readOneLine(char *buf, int n, FILE *fp)
{
    char *fgetsResult;

    do
    {
        fgetsResult = fgets(buf, n, fp);
    } while(fgetsResult!=NULL && buf[0]=='#');
            /* エラーや EOF ではなく、かつ、先頭が '#' の時は、次の行 */
            /* を読み込む */

    return fgetsResult;
}   


/*======================================================================
 * PGM-RAW フォーマットのヘッダ部分の読み込みと画像構造体の初期化
 *======================================================================
 *   PGM-RAW フォーマットの画像データファイル FILE *fp から、ヘッダ部
 * 分を読み込んで、その画像の画素数、階調数を調べ、その情報に従って、
 * 画像構造体 image_t *ptImage を初期化する。
 *   画素値データを格納するメモリ領域も確保し、この領域の先頭を指すポ
 * インタを ptImage->data に格納する。
 *
 * !! 注意 !!
 *   この関数は、ほとんどの場合、正しく動作するが、PGM-RAWフォーマット
 * の正確な定義には従っておらず、正しいPGM-RAWフォーマットのファイルに
 * 対して、不正な動作をする可能性がある。なるべく、本関数をそのまま使
 * 用するのではなく、正しく書き直して利用せよ。
 */
void
readPgmRawHeader(FILE *fp, image_t *ptImage)
{
    int width, height, maxValue;
    char buf[128];
    char *commentPos;

    /* マジックナンバー(P5) の確認 */
    if(readOneLine(buf, 128, fp)==NULL)
    {
        goto error;
    }
    /* 行内コメントを除去 */
    commentPos = strchr(buf, '#');
    if (commentPos != NULL) {
        *commentPos = '\0';
    }
    if (buf[0]!='P' || buf[1]!='5')
    {
        goto error;
    }

    /* 画像サイズの読み込み */
    if (readOneLine(buf, 128, fp)==NULL)
    {
        goto error;
    }
    /* 行内コメントを除去 */
    commentPos = strchr(buf, '#');
    if (commentPos != NULL) {
        *commentPos = '\0';
    }
    if (sscanf(buf, "%d %d", &width, &height) != 2)
    {
        goto error;
    }
    if ( width<=0 || height<=0)
    {
        goto error;
    }

    /* 最大画素値の読み込み */
    if (readOneLine(buf, 128, fp)==NULL)
    {
        goto error;
    }
    /* 行内コメントを除去 */
    commentPos = strchr(buf, '#');
    if (commentPos != NULL) {
        *commentPos = '\0';
    }
    if (sscanf(buf, "%d", &maxValue) != 1)
    {
        goto error;
    }
    if ( maxValue<=0 || maxValue>=256 )
    {
        goto error;
    }

    /* 画像構造体の初期化 */
    initImage(ptImage, width, height, maxValue);

    return;

/* エラー処理 */
error:
    fputs("Reading PGM-RAW header was failed\n", stderr);
    exit(1);
}
     

/*======================================================================
 * PGM-RAWフォーマットの画素値データの読み込み
 *======================================================================
 *   入力ファイル FILE *fp から総画素数分の画素値データを読み込んで、
 * 画像構造体 image_t *ptImage の data メンバーが指す領域に格納する
 */
void
readPgmRawBitmapData(FILE *fp, image_t *ptImage)
{
    if( fread(ptImage->data, sizeof(unsigned char),
            ptImage->width * ptImage->height, fp)
            != ptImage->width * ptImage->height )
    {
        /* エラー */
        fputs("Reading PGM-RAW bitmap data was failed\n", stderr);
        exit(1);
    }
}


/*======================================================================
 * フィルタリング(ネガポジ反転)
 *======================================================================
 *   画像構造体 image_t *originalImage の画像をフィルタリング(ネガポジ
 * 反転)して、image_t *resultImage に格納する
 */
void
filteringImage(image_t *resultImage, image_t *originalImage)
{
    int     x, y;
    int     width, height;

    /* originalImage と resultImage のサイズが違う場合は、共通部分のみ */
    /* を処理する。*/
    width = min(originalImage->width, resultImage->width);
    height = min(originalImage->height, resultImage->height);

    for(y=0; y<height; y++)
    {
        for(x=0; x<width; x++)
        {
            resultImage->data[x+resultImage->width*y]
                    = ( originalImage->maxValue
                    -originalImage->data[x+originalImage->width*y] )
                    *resultImage->maxValue/originalImage->maxValue;
        }
    }
}

/*======================================================================
 * フィルタリング(Prewittフィルタ)
 *======================================================================
 *   画像構造体 image_t *originalImage の画像をフィルタリング(Prewittフィルタ)
 * して、image_t *resultImage に格納する
 */
void
filteringImageByPrewittWithSquareRoot(image_t *resultImage, image_t *originalImage)
{
    int     x, y;
    int     width, height;

    /* originalImage と resultImage のサイズが違う場合は、共通部分のみ */
    /* を処理する。*/
    width = min(originalImage->width, resultImage->width);
    height = min(originalImage->height, resultImage->height);

    int x_filter[3][3] = {
        {-1, 0, 1},
        {-1, 0, 1},
        {-1, 0, 1}
    };
    int y_filter[3][3] = {
        {-1, -1, -1},
        {0, 0, 0},
        {1, 1, 1}
    };
    
    for(y=0; y<height-2; y++)
    {
        for(x=0; x<width-2; x++)
        {
            int x_sum = 0;
            int y_sum = 0;
            for(int i=0; i<3; i++)
            {
                for(int j=0; j<3; j++)
                {
                    x_sum += originalImage->data[x+i+originalImage->width*(y+j)] * x_filter[i][j];
                    y_sum += originalImage->data[x+i+originalImage->width*(y+j)] * y_filter[i][j];
                }
            }
            int result =  sqrt(x_sum*x_sum + y_sum*y_sum);
            if(result > 255)
            {
                result = 255;
            }
            resultImage->data[x+resultImage->width*y] = result;
        }
    }
}

/*======================================================================
 * フィルタリング(Prewittフィルタ)
 *======================================================================
 *   画像構造体 image_t *originalImage の画像をフィルタリング(Prewittフィルタ)
 * して、image_t *resultImage に格納する
 */
void
filteringImageByPrewittWithAbsolute(image_t *resultImage, image_t *originalImage)
{
    int     x, y;
    int     width, height;

    /* originalImage と resultImage のサイズが違う場合は、共通部分のみ */
    /* を処理する。*/
    width = min(originalImage->width, resultImage->width);
    height = min(originalImage->height, resultImage->height);

    int x_filter[3][3] = {
        {-1, 0, 1},
        {-1, 0, 1},
        {-1, 0, 1}
    };
    int y_filter[3][3] = {
        {-1, -1, -1},
        {0, 0, 0},
        {1, 1, 1}
    };
    
    for(y=0; y<height-2; y++)
    {
        for(x=0; x<width-2; x++)
        {
            int x_sum = 0;
            int y_sum = 0;
            for(int i=0; i<3; i++)
            {
                for(int j=0; j<3; j++)
                {
                    x_sum += originalImage->data[x+i+originalImage->width*(y+j)] * x_filter[i][j];
                    y_sum += originalImage->data[x+i+originalImage->width*(y+j)] * y_filter[i][j];
                }
            }
            int result = abs(x_sum) + abs(y_sum);
            if(result > 255)
            {
                result = 255;
            }
            resultImage->data[x+resultImage->width*y] = result;
        }
    }
}

/*======================================================================
 * 二値化
 *======================================================================
 *   画像構造体 image_t *originalImage の画像を二値化して、image_t *resultImage に格納する
 */
void
binarizationWithThreshold(image_t *resultImage, image_t *originalImage)
{
    int     x, y;
    int     width, height;

    /* originalImage と resultImage のサイズが違う場合は、共通部分のみ */
    /* を処理する。*/
    width = min(originalImage->width, resultImage->width);
    height = min(originalImage->height, resultImage->height);

    int threshold = calclateThreshold(resultImage, originalImage);
    printf("threshold: %d\n", threshold);

    for(y=0; y<height; y++)
    {
        for(x=0; x<width; x++)
        {
            if(originalImage->data[x+originalImage->width*y] > threshold)
            {
                resultImage->data[x+resultImage->width*y] = 255;
            }
            else
            {
                resultImage->data[x+resultImage->width*y] = 0;
            }
        }
    }
}

// 関数の戻り値の型をintに修正
int
calclateThreshold(image_t *resultImage, image_t *originalImage)
{
    int x, y;
    int width, height;
    
    width = min(originalImage->width, resultImage->width);
    height = min(originalImage->height, resultImage->height);

    int N = width * height;  // N = 全画素数
    int ni[256] = {0};      // ni = 階調値iである画素の数
    double pi[256] = {0.0}; // pi = ni/N
    int L = 256;            // L = 階調値の最大値+1
    
    // niの計算：各階調値の出現回数をカウント
    for(y = 0; y < height; y++) {
        for(x = 0; x < width; x++) {
            ni[originalImage->data[x + originalImage->width * y]]++;
        }
    }

    // piの計算：pi = ni/N
    for(int i = 0; i < L; i++) {
        pi[i] = (double)ni[i] / N;
    }

    // μTの計算：μT = Σ(i*pi)
    double mu_T = 0.0;
    for(int i = 0; i < L; i++) {
        mu_T += i * pi[i];
    }

    // クラス間分散の計算とその最大値を求める
    double max_sigma_B = 0.0;
    int optimal_k = 0;
    
    // 1 ≤ k ≤ L-1 の範囲で探索
    for(int k = 1; k < L; k++) {
        // ω0の計算：ω0 = Σ(pi) [i=0からk]
        double omega_0 = 0.0;
        for(int i = 0; i <= k; i++) {
            omega_0 += pi[i];
        }
        
        // ω1の計算：ω1 = Σ(pi) [i=k+1からL-1]
        double omega_1 = 1.0 - omega_0;  // ω0 + ω1 = 1 なので
        
        // μ0の計算：μ0 = Σ(i*pi)/ω0 [i=0からk]
        double mu_0 = 0.0;
        for(int i = 0; i <= k; i++) {
            mu_0 += i * pi[i];
        }
        mu_0 = omega_0 > 0 ? mu_0 / omega_0 : 0;
        
        // μ1の計算：μ1 = Σ(i*pi)/ω1 [i=k+1からL-1]
        double mu_1 = 0.0;
        for(int i = k + 1; i < L; i++) {
            mu_1 += i * pi[i];
        }
        mu_1 = omega_1 > 0 ? mu_1 / omega_1 : 0;
        
        // クラス間分散σB²(k)の計算
        double sigma_B = omega_0 * (mu_0 - mu_T) * (mu_0 - mu_T) + 
                        omega_1 * (mu_1 - mu_T) * (mu_1 - mu_T);
        
        // 最大値の更新
        if(sigma_B > max_sigma_B) {
            max_sigma_B = sigma_B;
            optimal_k = k;
        }
    }
    return optimal_k;  // 最適な閾値を返す
}

void
PrewittAndBinarization(image_t *resultImage, image_t *originalImage)
{
    image_t tempImage;
    initImage(&tempImage, originalImage->width, originalImage->height, originalImage->maxValue);
    filteringImageByPrewittWithAbsolute(&tempImage, originalImage);
    binarizationWithThreshold(resultImage, &tempImage);
}


/*======================================================================
 * PGM-RAW フォーマットのヘッダ部分の書き込み
 *======================================================================
 *   画像構造体 image_t *ptImage の内容に従って、出力ファイル FILE *fp
 * に、PGM-RAW フォーマットのヘッダ部分を書き込む。
 */
void
writePgmRawHeader(FILE *fp, image_t *ptImage)
{
    /* マジックナンバー(P5) の書き込み */
    if(fputs("P5\n", fp)==EOF)
    {
        goto error;
    }

    /* 画像サイズの書き込み */
    if (fprintf(fp, "%d %d\n", ptImage->width, ptImage->height)==EOF)
    {
        goto error;
    }

    /* 画素値の最大値を書き込む */
    if (fprintf(fp, "%d\n", ptImage->maxValue)==EOF)
    {
        goto error;
    }

    return;

error:
    fputs("Writing PGM-RAW header was failed\n", stderr);
    exit(1);
}


/*======================================================================
 * PGM-RAWフォーマットの画素値データの書き込み
 *======================================================================
 *   画像構造体 image_t *ptImage の内容に従って、出力ファイル FILE *fp
 * に、PGM-RAW フォーマットの画素値データを書き込む
 */
void
writePgmRawBitmapData(FILE *fp, image_t *ptImage)
{
    if( fwrite(ptImage->data, sizeof(unsigned char),
            ptImage->width * ptImage->height, fp)
            != ptImage->width * ptImage->height )
    {
        /* エラー */
        fputs("Writing PGM-RAW bitmap data was failed\n", stderr);
        exit(1);
    }
}
 

/*
 * メイン
 */
int
main(int argc, char **argv)
{
    image_t originalImage, resultImage;
    FILE *infp, *outfp;
    char *mode;
  
    /* 引数の解析 */
    parseArg(argc, argv, &infp, &outfp, &mode);

    /* 元画像の画像ファイルのヘッダ部分を読み込み、画像構造体を初期化 */
    /* する */
    readPgmRawHeader(infp, &originalImage);

    /* 元画像の画像ファイルのビットマップデータを読み込む */
    readPgmRawBitmapData(infp, &originalImage);

    /* 結果画像の画像構造体を初期化する。画素数、階調数は元画像と同じ */
    initImage(&resultImage, originalImage.width, originalImage.height,
            originalImage.maxValue);

    /* 処理モードに応じたフィルタリング */
    if (strcmp(mode, "edge") == 0) {
        /* エッジ強調のみ（Prewitt + 絶対値） */
        filteringImageByPrewittWithAbsolute(&resultImage, &originalImage);
    } else if (strcmp(mode, "binary") == 0) {
        /* 二値化のみ */
        binarizationWithThreshold(&resultImage, &originalImage);
    } else if (strcmp(mode, "both") == 0) {
        /* エッジ強調→二値化 */
        PrewittAndBinarization(&resultImage, &originalImage);
    } else {
        fprintf(stderr, "Error: Invalid mode '%s'\n", mode);
        fprintf(stderr, "Valid modes: edge, binary, both\n");
        exit(1);
    }

    /* 画像ファイルのヘッダ部分の書き込み */
    writePgmRawHeader(outfp, &resultImage);

    /* 画像ファイルのビットマップデータの書き込み */
    writePgmRawBitmapData(outfp, &resultImage);

    return 0;
}
