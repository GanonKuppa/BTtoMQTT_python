# BTtoMQTT_python
マイコンから受信したBTのメッセージをMQTTに変換するスクリプト.ブローカーのIPアドレスおよびポートはjsonファイルに記載
## BT関係コマンドメモ

### BT機器のスキャン
    hcitool scan                                  　

### /dev/rfcomm1を読むことでBTの出力が得られるようになる
    sudo rfcomm bind /dev/rfcomm1 マックアドレス

