# スコアを競ってみよう！

## レギュレーション
- 合格条件
    ```
    Gatling で負荷をかけて、全部通れば終わりです。
    ```
- 確認方法
    ```
    cli の gatling 実行結果
    dashboard
    ```
- 触っていいもの・いけないもの
    ```
    触っていいもの:
      自分が serverless framework でデプロイしたコンポーネント
      (API Gateway, Lambda, DynamoDB, CloudWatch)
      gatling の ターゲットURL の指定
    触ってはいけないもの:
      IAMの設定,
      EC2の設定,
      他人のコンポーネント（壊すと楽しいよ）,
      他のリージョン（たまにオハイオ好きな人いるよね）,
      gatling の設定（ターゲットURLを除く以外）
    ```

## 実施手順
- 各自のec2インスタンスにログイン

- 試験ツールの整備 (講師が環境を用意している場合はスキップ)
    ```sh
    # gatling-charts-highcharts-bundle-2.3.0 をダウンロード
    $ cd ~
    $ curl -O https://repo1.maven.org/maven2/io/gatling/highcharts/gatling-charts-highcharts-bundle/2.3.0/gatling-charts-highcharts-bundle-2.3.0-bundle.zip
    $ unzip gatling-charts-highcharts-bundle-2.3.0-bundle.zip

    # 本repositoryにあるスクリプトをコピー
    $ cp ~/2019-sw-training/faas/application/bench/gatling-charts-highcharts-bundle-2.3.0/bin/* ~/gatling-charts-highcharts-bundle-2.3.0/bin/
    $ cp ~/2019-sw-training/faas/application/bench/gatling-charts-highcharts-bundle-2.3.0/user-files/simulations/* ~/gatling-charts-highcharts-bundle-2.3.0/user-files/simulations/

    # ホスト名とstage名を揃える (sls deploy した APIGW の URL と gatling のアクセス先を揃えるため。変なアプローチなので handson.scala をいじってくれてもOK)
    hostname <stage名>
    ```

- 試験ツールのディレクトリに移動
    ```sh
    $ cd ~/gatling-charts-highcharts-bundle-2.3.0  # 環境により異なる場合がございます
    ```

- `gatling-charts-highcharts-bundle-2.3.0/user-files/simulations/handson.scala` の以下の部分を編集し、試験の向け先を **「sls で作成した自分の API」** に修正する
    ```scala
    val httpConf = http
       .baseURL("https://hogehoge.execute-api.ap-southeast-1.amazonaws.com/")  // ここを sls で作成した自分の API に修正する
    ```

- 試験ツール実行
    - `bash bin/gatling.sh -s HandsOnRequest`

## 試験結果の例
- 出力サンプル: 以下のような標準出力から OK そうか確認してください。 (web server からレポートも確認できるが、いまはNW的に許可していない。手元に html file を scp して見てもらっても構わない)
    ```
    ================================================================================
    2019-04-08 01:54:33                                          61s elapsed
    ---- Requests ------------------------------------------------------------------
    > Global                                                   (OK=1201   KO=0     )
    > request get list                                         (OK=1200   KO=0     )
    > request post                                             (OK=1      KO=0     )

    ---- request get list ----------------------------------------------------------
    [##########################################################################]100%
            waiting: 0      / active: 0      / done:1200
    ---- request post --------------------------------------------------------------
    [##########################################################################]100%
            waiting: 0      / active: 0      / done:1
    ================================================================================

    Simulation computerdatabase.HandsOnRequest completed in 60 seconds
    Parsing log file(s)...
    Parsing log file(s) done
    Generating reports...

    ================================================================================
    ---- Global Information --------------------------------------------------------
    > request count                                       1201 (OK=1201   KO=0     )
    > min response time                                     46 (OK=46     KO=-     )
    > max response time                                    324 (OK=324    KO=-     )
    > mean response time                                    69 (OK=69     KO=-     )
    > std deviation                                         22 (OK=22     KO=-     )
    > response time 50th percentile                         66 (OK=66     KO=-     )
    > response time 75th percentile                         73 (OK=73     KO=-     )
    > response time 95th percentile                         88 (OK=88     KO=-     )
    > response time 99th percentile                        148 (OK=148    KO=-     )
    > mean requests/sec                                 20.017 (OK=20.017 KO=-     )
    ---- Response Time Distribution ------------------------------------------------
    > t < 800 ms                                          1201 (100%)
    > 800 ms < t < 1200 ms                                   0 (  0%)
    > t > 1200 ms                                            0 (  0%)
    > failed                                                 0 (  0%)
    ================================================================================

    Reports generated in 1s.
    Please open the following file: /home/ec2-user/gatling-charts-highcharts-bundle-2.3.0/results/handsonrequest-1554688411952/index.html

    ----ここから下に合格・不合格が出る
    ```
