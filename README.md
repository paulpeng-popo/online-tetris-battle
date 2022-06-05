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

#### Socket 連線
* Concurrent Server
* Server-Client 一對二
* Waiting room
* Clients 間同步傳遞資訊
* 結束連線

#### 主遊戲
* Blocks 陣列
* 隨機亂數
* Time 無窮迴圈
* 方向鍵控制 (左、右、下)
* 消除判定
* 旋轉功能
* 空白鍵快速落下
* 方塊保留鍵
* 集氣條+對手生成灰色方塊
* 分數
* 計時
* 結束判定

#### GUI
* 主封面、進入遊戲介面
* 遊戲操作介紹
* 等待室介面、對手資訊
* 主遊戲介面框設計
* 結算畫面
