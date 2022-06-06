# Online Tetris Battle

### Network programing final term project

+ Prerequisite
    - python 3.9 (or above)
    - pygame 2.1.2

+ Install package
    ```sh
    pip install -r requirements.txt && cd src
    ```
+ Execute (Server side)
    ```sh
    python3 GameServer.py
    ```
+ Execute (Client side)
    ```sh
    python3 Tetris.py
    ```

### Game Introduction

#### Custom Ip Server

+ Just edit the ip address and port in [ip_port.txt](./src/game_data/ip_port.txt), then you can build your own servre
+ Support VPN connection

#### Socket 連線
* [x] Concurrent Server
* [x] Server-Client 一對二
* [x] Waiting room
* [x] Clients 間同步傳遞資訊
* [x] 結束連線

#### 主遊戲
* [x] Blocks 陣列
* [x] 隨機亂數
* [x] Time 無窮迴圈
* [x] 方向鍵控制 (左、右、下)
* [x] 消除判定
* [x] 旋轉功能
* [x] 空白鍵快速落下
* [x] 方塊保留鍵
* [x] 集氣條+對手生成灰色方塊
* [x] 分數
* [x] 計時
* [x] 結束判定

#### GUI
* [x] ~~主封面~~、進入遊戲介面
* [x] 遊戲操作介紹
* [x] 等待室介面、~~對手資訊~~
* [x] 主遊戲介面框設計
* [ ] ~~結算畫面~~
