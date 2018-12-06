◆サンプルプログラム説明
FaceAPIを利用したサンプルプログラムです。

◆環境
Python 3.x（おそらく最新版で動くはずです）
以下のライブラリをインストールする必要があります。いずれもpipコマンドでインストールできるはずです。
ライブラリ             コマンド
-------------------------------------------------------------------
cognitive_face        pip install cognitive_face
OpenCV                pip install opencv-python
numpy                 pip install numpy
pyaudio               python -m pip install pyaudio
azure                 pip install azure
azure-cosmosdb-table  pip install azure-cosmosdb-table

◆主に使用するファイル
MyForm.py       メインのファイルです。これを実行すると動きます。（コマンド　python MyForm.py）
Sample.ui       メインウィンドウのデザイナファイルです。（Qt Creatorで作成）
Sample.py       メインウィンドウのpyファイルです。上記デザイナファイルを更新したら，uiファイルをpyファイルに変換する作業が必要になります。
MyFaceAPI.py    FaceAPIを利用するクラスです。
MyCosmosDB.py   DB処理を行うクラスです。AzureのCosmosDBを利用しています。
const.py        定数定義を利用できるようにするクラスです。
PersonalIcon.py アイコン画像の上に名前を表示できるようにQLabelクラスを拡張したクラスです。
config.ini      デスクIDとフロアIDをこの設定ファイルから取得するようにしました。

◆その他
・実行前に、MyForm.pyと同階層に「image」という名前のフォルダを作成してください。カメラから取得した画像の一時保存場所なのですが，バグで先にフォルダを作っておかないと動きません。（後で直しておきます・・・）
  ↑修正しました（EC安井　2018/12/06）
・sonota_sampleフォルダに、OpenCV（画像処理用ライブラリ）やpyAudio（音声処理用ライブラリ）などのサンプルプログラムもおいています。
・iconファイル内には実際に表示するアイコンを格納しています。
・コマンド.txtにAnacondaで使えるコマンドをメモしています。（exe化はかなり重いです）
