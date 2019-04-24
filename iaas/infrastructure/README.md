## はじめに

- いくつかの変数値が未設定のため、そのままでは利用できない
- 1つの参照としての活用推奨

## 前提条件

- terraformがインストールされていること
    - 動作確認バージョンは `Terraform v0.11.13`
- GCPサービスアカウントのJSONがローカルにあること
- SSL/TLS証明書を作成し、ローカルで利用可能にしておくこと
- AppおよびBenchmarkerのイメージは別途作成しておくこと

## 構築・削除

```
// 必要な環境設定
$ export GOOGLE_CLOUD_KEYFILE_JSON=/{適当なPATH}/GCPServiceAccount.json
$ export TF_VAR_path_to_private_key=/{適当なPATH}/hoge.key
$ export TF_VAR_path_to_private_cert=/{適当なPATH}/hoge.crt

// 構築
$ terraform apply

// 構築
$ terraform destroy
```