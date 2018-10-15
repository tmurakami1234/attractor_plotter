# attractor_plotter
## 概要
tkinter の練習で, ローレンツ方程式やレスラー方程式のような, 時間に依存する変数が3つの1回微分連立方程式のアトラクターを描くプログラムを制作しました. 時間発展の計算には4次のルンゲクッタ法を使いました. 次がプログラムの起動画面です.

![](https://raw.githubusercontent.com/tmurakami1234/attractor_plotter/feature/01/image.png)

次のコマンドでプログラムを起動します.

```bash
$ python3 attractor_plotter.py
```
ubuntu 18.04 bionic x86_64 では起動確認済みです.

## 仕様
* scale bar で設定されてる値のグラフをリアルタイムにプロットします.
* `keep=>` をクリックすることで, scale bar で設定している値を entry box に記録出来ます.
* `set<=` をクリックすると, entry box の値が scale bar に反映されます.
* `save` をクリックすると, その隣の entry box に書かれた名前で画像が保存されます.
    * 既にその名前の画像ファイルが存在する場合, `(NUM)`がファイル名に追記されます.
## 課題
* ソースを書き換えずに, 指定された方程式の数値計算結果がプロットされるようにしたい.
* 好きな変数を軸に指定してグラフを描けるようにUIを変更したい.
