# ラベル「[システム]」のPull Request一覧

合計: 4件のPR

## PR一覧

| # | タイトル | 作成者 | 状態 | 作成日 | 更新日 |
|---|---------|--------|------|--------|--------|
| #1280 | [Add @yasuakikamoeka as code owner for education files](https://github.com/team-mirai/policy/pull/1280) | devin-ai-integration[bot] | closed | 2025-05-20 | 2025-05-20 |
| #1281 | [Add @i-tami-h as code owner for 50_国政のその他重要分野.md](https://github.com/team-mirai/policy/pull/1281) | devin-ai-integration[bot] | closed | 2025-05-20 | 2025-05-20 |
| #1964 | [Add files via upload　ステップ２デジタル民主主義を追加](https://github.com/team-mirai/policy/pull/1964) | tokshibata | closed | 2025-06-05 | 2025-06-11 |
| #2247 | [GitHubで行われているマニフェストのアップデートを、X(旧Twitter)でお知らせする機能の実装](https://github.com/team-mirai/policy/pull/2247) | yuki-snow1823 | open | 2025-06-12 | 2025-06-12 |

## PR詳細

### #1280: Add @yasuakikamoeka as code owner for education files

#### 説明

# Add @yasuakikamoeka as code owner for education files

This PR adds @yasuakikamoeka as a code owner for the education-related files according to the provided mapping table. This PR can be merged once the user is properly registered with write access to the repository.

## Files assigned to @yasuakikamoeka
- 11_ステップ１教育.md
- 21_ステップ２教育.md
- 32_ステップ３教育.md

Link to Devin run: https://app.devin.ai/sessions/77a31d64c6cb414fac1d686c62fdcbb3
Requested by: jujunjun110@gmail.com


#### 変更ファイル

- .github/CODEOWNERS

---

### #1281: Add @i-tami-h as code owner for 50_国政のその他重要分野.md

#### 説明

# Add @i-tami-h as code owner for 50_国政のその他重要分野.md

This PR adds @i-tami-h as a code owner for the file 50_国政のその他重要分野.md according to the provided mapping table. This PR can be merged once the user is properly registered with write access to the repository.

## Files assigned to @i-tami-h
- 50_国政のその他重要分野.md

Link to Devin run: https://app.devin.ai/sessions/77a31d64c6cb414fac1d686c62fdcbb3
Requested by: jujunjun110@gmail.com


#### 変更ファイル

- .github/CODEOWNERS

---

### #1964: Add files via upload　ステップ２デジタル民主主義を追加

#### 説明

v0.1時点で盛り込みが間に合わなかった部分について、公開しご意見をいただける段階まで来たので追加いたします

#### 変更ファイル

- .github/.linkspector.yml
- 15_ステップ１科学技術.md
- 22_ステップ２行政改革.md
- 25_ステップ２_デジタル民主主義.md

---

### #2247: GitHubで行われているマニフェストのアップデートを、X(旧Twitter)でお知らせする機能の実装

#### 説明

### 概要
チームみらいのSlackでやりとりされていた「GitHubで行われているマニフェストのアップデートを、Twitterでお知らせするbot」の企画のPR

### 背景
（エディさんの投稿を要約）
チームみらいのマニフェストリポジトリ( https://github.com/team-mirai/policy )で、変更提案の採用（マージ）が増えてきている。
マニフェストのアップデートは、チームみらいにとって最も本質的な進捗の一つなので、どのようなアップデートがあったかを有権者の方に知ってもらいたい。
知ってもらうために様々な方法はあるが、まずはXにその状況をリアルタイムに共有するようにしたい。

#### Xの投稿を見てユーザーに感じてほしいこと
- チームみらいの、この政策良いね！
- チームみらい、柔軟に意見を受け入れる姿勢があっていいね！

などなど...

### 変更内容

1. GitHub Actions ワークフロー（.github/workflows/post-to-x.yml）の追加
   - mainブランチへのPRがマージ（closed & merged）されたときに発火
   - Node.jsセットアップ後、`.github/scripts/post_to_x.ts` をTypeScriptでビルド・実行
   - Twitter（X）APIの認証情報はGitHub Secretsから取得

2. スクリプト（.github/scripts/post_to_x.ts）の追加
   - マージされたPRのタイトル・URL・作成者を取得し、X（旧Twitter）に自動投稿。
   - 投稿内容は「提案したPRがマージされました！」等の日本語メッセージ
   - エラー時は内容を出力して終了


### 主な変更点

- PRマージ時に自動でX（Twitter）へPR情報を投稿する仕組みを導入
- TypeScriptでX投稿用スクリプトを新規作成し、GitHub Actionsから実行する構成にした
- 認証情報やPR情報の受け渡しはGitHub Actionsの標準的な方法（Secretsやイベント情報）を利用


### 動作確認
個人のリポジトリで動作確認しました。

マージした際のActionsのログ
https://github.com/yuki-snow1823/pr-messenger-test/actions/runs/15611221825

マージしたPRのX投稿
https://x.com/mirai_manifesto/status/1933147520198152678

### 影響範囲
https://github.com/team-mirai/policy のmainブランチへのマージが行われると、Xに投稿されるようになります。

### 補足事項
土日のリリースを目標に最短で作成しました。改善点はチャンネルで話しているので、リリース後にまたブラッシュアップできればと思います🙌

本PRのマージ後は本番用のAPIキーなどをセットする必要があります。

### 今後の課題
- policyのリポジトリでの機能実装のPRも通知されてしまうので、何か対策がしたい
- 関連PRも取得するようにしたい
- AIを間に入れて文章に工夫をしたい...etc

#### 変更ファイル

- .github/scripts/post_to_x.ts
- .github/workflows/post-to-x.yml

---

