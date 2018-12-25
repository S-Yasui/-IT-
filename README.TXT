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
MyForm.py         メインのファイルです。これを実行すると動きます。（コマンド　python MyForm.py）
Sample.ui         メインウィンドウのデザイナファイルです。（Qt Creatorで作成）
Sample.py         メインウィンドウのpyファイルです。上記デザイナファイルを更新したら，uiファイルをpyファイルに変換する作業が必要になります。
MyFaceAPI.py      FaceAPIを利用するクラスです。
MyCosmosDB.py     DB処理を行うクラスです。AzureのCosmosDBを利用しています。
const.py          定数定義を利用できるようにするクラスです。
PersonalIcon.py   アイコン画像の上に名前を表示できるようにQLabelクラスを拡張したクラスです。
MySearchDialog.py 検索ダイアログボックスのクラスです。
config.ini        デスクIDとフロアIDをこの設定ファイルから取得するようにしました。
		  ※デスクIDの上1桁が'0'：オフィス、'1'：サテライトオフィス、'2'：テレワークとしています。

◆その他
・実行前に、MyForm.pyと同階層に「image」という名前のフォルダを作成してください。カメラから取得した画像の一時保存場所なのですが，バグで先にフォルダを作っておかないと動きません。（後で直しておきます・・・）
  ↑修正しました（EC安井　2018/12/06）
・sonota_sampleフォルダに、OpenCV（画像処理用ライブラリ）やpyAudio（音声処理用ライブラリ）などのサンプルプログラムもおいています。
・iconファイル内には実際に表示するアイコンを格納しています。
・コマンド.txtにAnacondaで使えるコマンドをメモしています。（exe化はかなり重いです）

◆Face Storageへの写真登録手順
「sonota_sample」に格納されているサンプルソースをそのまま使って登録します。

１．人物情報を作成する
	(1)faceAPI_createPerson_test.py の17行目，18行目の値を変更して実行する。
		17 personName = '安井誠良'	←顔を登録する人の名前に変更
		18 userData = 'S7223'		←ユーザID（仮にエネコム：S+数字4桁，SST：A+数字4桁としています）

	(2)実行結果としてpersonIDがコンソール出力されるので，そのIDを控えておく。

２．作成した人物情報に顔写真を登録する
	(1)faceAPI_addPersonPic_test.py の17行目，18行目の値を変更して実行する。
		17 personId = '1e1ae1a8-c384-4143-b26f-9ffa1ae1bea4'									←１．(2)で控えたpersonIDに変更
		18 image_file_path = 'C:/Users/user/Desktop/2社合同IT研究会/IT研究会資料/sonota_sample/img/faceOnly/image06.png'	←顔写真のファイルパスに変更
    ※写真は，一応撮影の角度を変えて2枚登録します。
    ※できるだけ画像いっぱいに顔が映ったものを登録してください。

３．人物情報のトレーニングを行う
	(1)faceAPI_trainPerson_test.py を実行する。（特にソースを変える部分はありません）

４．顔認識機能を確認する
	(1)MyForm.py を実行し，webカメラを接続してメニューの更新を押す。
	(2)「ユーザ１」の向かい側に名前とアイコンが表示されれば成功。
