# BTtoMQTT_python
マイコンから受信したBTのメッセージをMQTTに変換するスクリプト  
ブローカーのIPアドレスおよびポートはjsonファイルに記載
python3でないと動かないので注意

## BT関係コマンドメモ

### スキャンをして繋ぎたいBT機器のマックアドレスを特定
    hcitool scan

### /dev/rfcomm1を読むことでBTの出力が得られるようになる
    sudo rfcomm bind /dev/rfcomm1 マックアドレス

## その他メモ

### nvm関係
    source ~/.nvm/nvm.sh

### foreverでデーモン化
    forever start -c python3 hoge.py

### foreverでデーモン化されたか確認
    forever list

### foreverで起動しているスクリプトを停止
    foreve stop hoge.py

### foreverで起動しているスクリプトを再起動
    forever restart hoge.py


