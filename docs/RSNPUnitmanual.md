# 遠隔操作用RSNPユニット利用マニュアル

<h4> 芝浦工業大学 知能機械システム研究室　加藤宏一朗，松日楽　信人</h4>

~~~text  
連絡先：  
芝浦工業大学 機械機能工学科 知能機械システム研究室  
〒135-8548 東京都江東区豊洲3-7-5  
機械工学専攻 修士2年 加藤宏一朗 Koichiro Kato
TEL:03-5859-8073
E-mail:md20024@shibaura-it.ac.jp  
~~~  

<div style="page-break-before:always"></div>

## 1.はじめに  

汎用ユニット(以下，「RSNPユニット」と記載)を，多種多様なロボットやデバイスに外付けで接続することで，取得したデータをRSNP(Robot Serivice Networking Protocol)通信でインターネット経由でサーバにアップロードして蓄積し，Webブラウザ等のGUI上で各ロボットの状態を管理，監視するシステムを開発してきました．今回は，双方向の通信を実現し，以下の図のようにRSNPユニットをロボットやデバイスに接続してインターネット経由で遠隔操作することができます．  

<img src="https://user-images.githubusercontent.com/46204057/104468815-3c321700-55fb-11eb-9f7b-5befc4f6a554.png"  width="60%">


### 1.1 使用するRSNPユニット
1月のロボットフォーラムで使用いただいたRSNPユニットと同様です．  
RSNPクライアント×2, MQTTブローカーがインストールされています．  

<img src="https://user-images.githubusercontent.com/46204057/125299828-77bc5c80-e364-11eb-9b48-d885cadc77ea.png" width=50%> 

## 2. ユニット使用方法  

**配布したユニット以外のユニットを使用する場合，[こちら](https://github.com/IMS-Lab8073/RSNPUnitRemoteControl/blob/main/docs/RaspiSetup.md)から各種設定を済ませてください．**  

### 2.1 WiFiの設定  
電源投入から接続，WiFiの設定は[こちら](https://ims-lab8073.github.io/RSNPTutorial2020/Setting)に詳細な記載があります．**2.1から2.5まで**を参照ください．  

配布したユニットのホスト名，ユーザ名，パスワードは以下になります．  
| 項目 | 内容 |
|:-:|:-:|
| ホスト名 | rsnpunit |
| ユーザ名 | pi |
| パスワード | 8073 |

※ROSを実装したRSNPユニットは以下になります．  
| 項目 | 内容 |
|:-:|:-:|
| ホスト名 | ubuntu |
| ユーザ名 | ubuntu |
| パスワード | ubuntu |


以下，Raspberry Piの電源をいれ，Raspberry Pi上のコマンドで操作を行ってください．  
まず，接続するルータ等のSSIDとパスワードを調べます．  
次に，`wpa_supplicant.conf`ファイルをエディタで編集します．  

```shell
$ sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

※ファイルを編集するためのエディタとして今回は"nano"を使用していますが，好みのものを使用してください．以下，"nano"を使用します．

次のとおりに追記してください．  

~~~text
network={
     ssid="SSIDを記述"
     psk="パスワードを記述"
}
~~~

### 2.2 RSNP接続をする場合
RSNP接続をする場合，以下にしたがって下さい．RSNP接続を行わず，デバッグ用プログラムで動作を確認することもできます．  

#### 2.2.1 コンフィグレーションの設定
RSNPクライアントの実行のコンフィグレーションパラメータを設定しているファイルです．  
以下のコマンドで編集することができます．  

```shell
$ cd ~/RobotShowCase
$ sudo nano Config/Config.properties
```

デフォルトでは以下のようになっています．  
`robot_id`は各機関異なります．    

```
#Configuration
broker = localhost
subtopic = toUnit/Robotdata
pubtopic = fromServer/Velocity
# end_point = http://zmini.robo.meo.shibaura-it.ac.jp:8080/RemoteControlSystem/services
end_point = http://s01.sck.aim.aoyama.ac.jp/RemoteControlSystem/services
robot_id = Raspi1
password = null
debug = false
max_fps = 10
camera_no = -1
```

※各機関のロボットID
| 機関名 | 役割 | ID |
|:-:|:-:|:-:|
| 都産技 | ロボット搭載用 | libra_2021 |
| 都産技 | 俯瞰カメラ用 | libra_2021_sub |
| 会津大 | ロボット搭載用 | aizu_2021 |
| 会津大 | 俯瞰カメラ用 | aizu_2021_sub |

#### 2.2.2 カメラ用クライアントを立ち上げる
ロボット搭載用と俯瞰カメラ用どちらのユニットでも立ち上げてください．  
```
$ cd ~/RobotShowCase
```
```
$ java -jar RSNPCameraClient_Raspi.jar
```

以下の画像のように
```text
JavaCV TryLoad中・・・
JavaCV TryLoad終了
```
の表示が出れば起動成功です．  

<img src="https://user-images.githubusercontent.com/46204057/125301487-01205e80-e366-11eb-9a2a-3cde62d8c0da.png" width="80%">

#### 2.2.3 遠隔操作用クライアントを立ち上げる
ロボット搭載用のみで大丈夫です．  
新しいターミナルを開いてください．
```
$ cd ~/RobotShowCase
```
```
$ java -jar RSNPUnitRemoteControl.jar
```

### 2.3 RSNP通信を行わずに，動作を確認する(デバッグ用プログラムを使用する)  
RSNPユニット内にある，[デバッグ用プログラム](https://github.com/IMS-Lab8073/RSNPUnitRemoteControl/tree/main/debug)で動作を確認することができます．  
イメージは以下になります．  

<img src="https://user-images.githubusercontent.com/46204057/104475528-8d91d480-5602-11eb-8272-3760c6bd45a0.png" width="60%">

| Pub/Sub | ファイル名 |用途 |
|:-:|:-:|:-:|
| Pub | debug_publisher.py | サーバからくる文字列を送信(publish)します． |
| Sub | debug_subscriber.py | サーバへ送る文字列を受け取り(subscribe)，表示します．フォーマットが異なる場合，エラーとなります．  |

publisherとsubscriber，それぞれ，以下のコマンドで実行することができます．  
```shell
$ cd ~/RSNPUnitRemoteControl/debug
```

publisher  
```shell
$ python3 debug_publisher.py  
```

subscriber 
```shell
$ python3 debug_subscriber.py  
```


## 3. ユニット通信仕様  
ユニットとロボットとの通信方法を示します．通信方法はMQTTであり，MQTTブローカーおよびトピック名は2.2のコンフィグレーションに示す通りです．通信データ内容は[こちら](https://github.com/IMS-Lab8073/RSNPUnitRemoteControl/blob/main/docs/Specification.md)になります．  
デフォルトは以下になります．    

| 項目 | コンフィグレーション名 | デフォルト値 | 説明 |
|:-:|:-:|:-:|:-:|
| ブローカー | broker | localhost | RSNPユニット内部のブローカーです |
| トピック | subtopic | toUnit/Robotdata | 遠隔操作用クライアント**が**Subscribeする際に使うトピック名です | 
| トピック | pubtopic | fromServer/Velocity | 遠隔操作用クライアント**が**Publishする際に使うトピック名です |

## 4. 管理者画面/操作画面について
### 4.1 管理者画面からカメラを起動  
カメラを起動する管理者画面があります．  

http://s01.sck.aim.aoyama.ac.jp/RemoteControlSystem/RSNPServerState


カメラ用のクライアントは，以下のように
 - エンコードモード
 - 動画のサイズ
 - 動画のbitrate
 - 配信間隔
 - 動画のfps

を選択することができます．
基本的にはデフォルトの設定値で大丈夫です．  
<img src="https://user-images.githubusercontent.com/46204057/125300997-83f4e980-e365-11eb-93ac-e6ab8b73b3de.png">


開始ボタンを押すと，カメラ用クライアントから配信が始まります．  
`開く` のリンクからカメラ画像を確認することができます．  
<img src="https://user-images.githubusercontent.com/46204057/125303049-793b5400-e367-11eb-9aaa-1a88babd7ef3.png">


### 4.2 操作画面からロボットを操作する  
操作画面のURLは以下です．  
  
http://s01.sck.aim.aoyama.ac.jp/RemoteControlSystem/showcase-login    

ログイン画面からログインしてください．
<img src="https://user-images.githubusercontent.com/46204057/125303702-f5359c00-e367-11eb-862c-024b6dd5af49.png" width="80%">

ログイン後，以下の画面に遷移します．  
<img src="https://user-images.githubusercontent.com/46204057/125303770-01b9f480-e368-11eb-87cd-bf1dafcc8398.png" width="80%">

各操作画面には，画面下部のリンクから遷移できます．ログインIDに紐づいて遷移できる画面が決まっていて，自分の機関のページにのみ遷移できる設定になっています．  
操作画面に移動後，ロボット操作をオンにするとA~Eのボタンでの移動が可能になります．
※ロボット操作は，ロボットの状態が待機中(遠隔操作用クライアントが起動している状態)の場合のみONにできるので注意してください  
<img src="https://user-images.githubusercontent.com/46204057/125304426-8c9aef00-e368-11eb-8c19-b85a4989f1de.png" width="80%">