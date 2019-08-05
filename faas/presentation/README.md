## FaaS Lecture and presentation
- First, check out `https://gitpitch.com/nttcom/2019-sw-training?p=faas/presentation#/` (presentation with markdown rendered by GitPitch)
- if the above link is broken, find by yourself based on below pattern:
    ```
    https://gitpitch.com/$user/$repo/$branch?p=$dir/$subdir
    ```

---

## 当日のタイムライン
- 0900 opening
- 0910 講義開始
- 10min 休憩
- 1010-1140: ハンズオン Part1 (web) 1.5h
- 1140-1240: 昼休み
- 1240−1340: ハンズオン Part2 (infra as code)
- 10min 休憩
- 1350-1600: ハンズオン Part3 (challenge) (10min 休憩含む)
- 1600-1630: 解説、業務紹介
- 1630-1730: 振り返り or 終了

## 講義内容
- 自己紹介
- サーバーレス、FaaSとは
- オンプレからSaaSまでの比較
- 代表的なサービス事例: lambda, azurefunction, gcf
- 事例 (外部イベントとかで見てきた事例など)

## ハンズオン内容
- 1. Webコンソールから作る
    - lambda 作成
    - apigw は指示通り作ってもらう
    - dynamodb も指示通り
    - 動作確認

- 2. Serverless Framework から作る
    - webコンソールで作ったものにプラスする（test-driven development）
    - sls が動作する踏み台サーバを人数分用意
    - ポチっとデプロイ
    - 動作確認

- 3. 負荷をかけてみる
    - 負荷試験の話 (gatling) スライドを挟もう
    - gatlingで負荷かてみる
    - 何が悪いか考えてみてくれ
