## Serverless Architecture 事例

---

### A. 従来システムのサーバーレス化

+++

#### 事例A-1 典型的な Web API の置き換え

##### 一般的なCRUD API

<img src="faas/presentation/assets/img/web_api.jpg" width="60%">

##### source: [サーバーレスアーキテクチャのパターン別ユースケース](https://yoshidashingo.hatenablog.com/entry/serverlss-usecases-2017)

+++

#### 事例A-2 SPA

##### S3にhtml/jsを格納して、lambdaを発火

<img src="faas/presentation/assets/img/spa.jpg" width="80%">

##### source: [サーバーレスアーキテクチャのパターン別ユースケース](https://yoshidashingo.hatenablog.com/entry/serverlss-usecases-2017)

---

### B. FaaS ならではの事例

+++

#### 事例 B-1 非同期ジョブ

- 画像アップロード→リサイズや切り出し

<img src="faas/presentation/assets/img/nikkei.jpg" width="60%">

##### source: [紙面ビューアーを支えるサーバレスアーキテクチャ](https://speakerdeck.com/ikait/serverless-architecture-supports-nikkeis-paper-viewer)

+++

#### 事例 B-2 Webサイト監視

##### 定期的なトリガーでヘルスチェックを実行

<img src="faas/presentation/assets/img/monitoring.jpg" width="60%">

##### source: [サーバーレスアーキテクチャのパターン別ユースケース](https://yoshidashingo.hatenablog.com/entry/serverlss-usecases-2017)

+++

#### 事例 B-3 オンコールシステム

##### アラートをトリガーに電話を鳴らす

<img src="faas/presentation/assets/img/on_call.jpg" width="80%">

##### source: [サーバーレスアーキテクチャのパターン別ユースケース](https://yoshidashingo.hatenablog.com/entry/serverlss-usecases-2017)

+++

#### 事例 B-4 aibo

##### aiboはすべてサーバレス

<img src="faas/presentation/assets/img/aibo.jpg" width="60%">

##### source: [aiboクラウドサービスを支えるサーバレス技術](https://speakerdeck.com/ryoheimorimoto/serverlessconf-tokyo-2018-aibo)
