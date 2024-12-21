<html lang="ja">
    <head>
        <meta charset="utf-8" />
    </head>
    <body>
        <h1><center>Homography</center></h1>
        <h2>なにものか？</h2>
        <p>
            画像内の４点を指定し、４点が矩形になるように射影変換した画像を出力します。<br>
            <img src="images/homography.svg"><br>
            <h3>適用例</h3>
            <img src="images/01.png"><br>
            <img src="images/02.png"><br>
            <img src="images/03.png"><br>
        </p>
        <h2>環境構築方法</h2>
        <p>
            pip install opencv-python<br>
        </p>
        <h2>使い方</h2>
        <p>
            python homography.py (画像ファイル名)<br>
            <br>
            画像の表示サイズは+キー押下/-キー押下で調整できます。<br>
            矩形になるべき点を４点クリックします。<br>
            ESCキーを押下するとプログラムが終了します。<br>
            結果は homography.png に保存されます。<br>
        </p>
    </body>
