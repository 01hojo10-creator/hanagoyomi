# はなごよみ

365日ぶんの誕生花を、やさしいメッセージと写真(またはイラスト)でとどける、スマホ向けの一枚HTMLアプリです。
コイン集め・ガチャ・ミニゲーム「おはなキャッチ」・お花畑コレクションなどのゲーム要素つき。

## 構成

```
hanagoyomi/
├─ index.html          アプリ本体(旧 はなごよみ.html)。単体で動作します
├─ credits.html         写真の出典・ライセンス一覧(index.html のフッターからリンク)
├─ data/
│   ├─ flowers.json         365(うるう年366)日ぶんの誕生花データ(日付→花名/花言葉/メッセージ/art情報/wiki記事名)。編集の元データ
│   ├─ credits_manifest.json 各写真の出典情報(作者・ライセンス・出典URL)。credits.html の生成元
│   └─ collect_summary.json  写真収集結果のログ(取得成功/画像なし/ライセンス不適合の内訳)
├─ images/              花の写真(images/MMDD.jpg、長辺640pxにリサイズ済み)
└─ scripts/             写真収集スクリプト(再収集・更新用)
```

`index.html` は `data/flowers.json` の内容をビルド時に埋め込んだ単一HTMLです。
`data/flowers.json` を編集した場合は、以下のコマンドで index.html に再度埋め込みなおしてください。

```bash
python scripts/embed_flowers.py
```

## データについて

- 花のデータ(`data/flowers.json`)は日付キー(`"07-08"`など)ごとに、花の名前・花言葉・ひとことメッセージ・イラスト生成用パラメータ・写真検索用のWikipedia記事名を保持しています。
- 写真は [Wikimedia Commons](https://commons.wikimedia.org/) のフリー素材から、パブリックドメイン / CC0 / CC BY / CC BY-SA のいずれかのライセンスの画像のみを収集しています。作者名・ライセンス・出典URLは `credits.html` に一覧表示されます。
- 写真が用意できなかった日(366日中29日)は、アプリ内で自動的にイラスト表示にフォールバックします。ユーザーは「📷 しゃしん / 🎨 イラスト」の切り替えボタンでいつでも手動で切り替えられます。

## 既存機能(変更していません)

- コイン・レベル・称号システム
- ガチャ(通常/レアカード、全84枚相当のコンテンツ)
- ミニゲーム「おはなキャッチ」
- お花畑コレクション(4シーン: よる/ひる/ゆうやけ/はるかぜ)
- localStorage キー: `hanagoyomi_v2` / `hanagoyomi_mode` / `hanagoyomi_scene`

## ローカルでの確認方法

`index.html` は写真を `images/` フォルダから相対パスで読み込むため、ブラウザで直接 `file://` を開いても動作しますが、
簡易サーバー経由での確認を推奨します。

```bash
cd hanagoyomi
python -m http.server 8000
# ブラウザで http://localhost:8000/ を開く
```

## GitHub Pages で公開する手順

1. このフォルダの内容をGitHubリポジトリにpushします(このフォルダ自体が既にgitリポジトリとして初期化されています)。
   ```bash
   git remote add origin <あなたのリポジトリURL>
   git push -u origin main
   ```
2. GitHubのリポジトリページで **Settings → Pages** を開きます。
3. "Source" を `Deploy from a branch` にし、ブランチを `main`、フォルダを `/ (root)` に設定して保存します。
4. しばらく待つと `https://<ユーザー名>.github.io/<リポジトリ名>/` でアプリが公開されます(`index.html` が自動的にトップページとして表示されます)。

## 写真データの再収集・更新について

`scripts/collect_photos.py` を実行すると、`data/flowers.json` の `wiki` フィールドをもとに Wikimedia Commons から
写真を再収集し、`images/` と `data/credits_manifest.json` を更新します。ライセンスが確認できない画像は自動的にスキップされます。

```bash
python -m pip install pillow
python scripts/collect_photos.py
```

再収集後は、以下の順で再生成してください。

```bash
python scripts/build_credits.py     # credits.html を再生成
python scripts/embed_flowers.py     # index.html にデータを再埋め込み(wikiフィールド等を変更した場合)
```
