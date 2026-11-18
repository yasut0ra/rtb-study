# 第7章 プライバシーと識別子

> **この章のゴール**: RTB で「人」を識別する仕組みと、それがプライバシー規制でどう変わってきたかを理解する。

## 7.1 「同じ人」をどうやって見分ける？

RTB で「昨日スニーカーを見た人」に広告を出すには、**別々のサイトにいる同じ人を結びつける** 必要があります。そのために使われてきたのが **識別子（ID）** です。

| 識別子 | 使われる場所 | 仕組み |
|-------|-----------|-------|
| **サードパーティ Cookie** | Web ブラウザ | アドテク企業のドメインで発行され、どのサイトでも読める ID |
| **ファーストパーティ Cookie** | Web ブラウザ | 訪問したサイト自身が発行する ID（そのサイト内でのみ有効） |
| **広告 ID**（IDFA / GAID） | スマホアプリ | OS が発行する端末ごとの ID（iOS: IDFA、Android: GAID） |
| **共通 ID**（UID2, ID5 など） | Web / アプリ / CTV | メールアドレスのハッシュなどから作る、業界で共有される ID |

## 7.2 Cookie Sync（クッキーシンク）

SSP と DSP は、それぞれ **別の Cookie ID** でユーザーを管理しています。
同じユーザーだと分かるように、**ID の対応表** を作る仕組みが Cookie Sync です。

```mermaid
sequenceDiagram
    participant B as ブラウザ
    participant S as SSP（ssp.example）
    participant D as DSP（dsp.example）
    B->>S: 広告リクエスト（Cookie: ssp_uid=ABC）
    S-->>B: 同期用ピクセル<br/>「dsp.example/sync?ssp_uid=ABC を読み込んで」
    B->>D: GET /sync?ssp_uid=ABC（Cookie: dsp_uid=XYZ）
    Note over D: 対応表に記録<br/>SSP の ABC = 自社の XYZ
    D-->>B: 302 → ssp.example/sync?buyeruid=XYZ（逆方向の同期）
    B->>S: GET /sync?buyeruid=XYZ
    Note over S: 次回から Bid Request の<br/>user.buyeruid に XYZ を入れる
```

これで DSP は Bid Request の `user.buyeruid = XYZ` を見て、「**うちのサイトに来たことがある、あの人だ！**」と分かります。

## 7.3 リターゲティングの仕組み

```mermaid
flowchart LR
    subgraph day1["📅 1日目"]
        U1["👤 ユーザー"] --> EC["👟 スニーカーECサイト<br/>（DSPのタグが設置）"]
        EC --> T["DSP に記録<br/>dsp_uid=XYZ は<br/>スニーカーに興味あり"]
    end
    subgraph day2["📅 2日目"]
        U2["👤 同じユーザー"] --> NEWS["📰 ニュースサイト"]
        NEWS --> BR["Bid Request<br/>buyeruid=XYZ"]
        BR --> DSP{"DSP:<br/>XYZ だ！<br/>高く入札しよう"}
        DSP --> AD["👟 スニーカーの広告"]
    end
    day1 --> day2
```

## 7.4 プライバシー規制の流れ

サードパーティ Cookie は便利な反面、**本人の知らないうちにサイトをまたいで行動を追跡** できてしまうため、各国の規制やブラウザ・OS の対応が進みました。

```mermaid
timeline
    title プライバシー保護の主な出来事
    2017 : Safari ITP（サードパーティ Cookie 制限の始まり）
    2018 : EU で GDPR 施行
    2019 : Firefox がトラッキング Cookie を標準でブロック
    2020 : 米カリフォルニア州 CCPA 施行
    2021 : iOS 14.5 で ATT 導入（IDFA の利用に許諾が必要に）
    2022 : 日本 改正個人情報保護法（個人関連情報の規制）
    2023 : 日本 改正電気通信事業法（外部送信規律）
    2024-2025 : Chrome がサードパーティ Cookie 廃止方針を撤回・Privacy Sandbox 縮小
```

### ブラウザ・OS の状況

| 環境 | サードパーティ Cookie / 広告 ID |
|-----|------------------------------|
| Safari（iPhone の標準ブラウザ） | 標準でブロック |
| Firefox | 標準でブロック |
| Chrome | **現在も利用可能**（廃止方針は撤回された） |
| iOS アプリ | IDFA は ATT で **ユーザーが許可した場合のみ** |
| Android アプリ | GAID は利用可能（ユーザーが削除・無効化可能） |

> ⚠️ Chrome は長年サードパーティ Cookie の段階的廃止と、その代替となる **Privacy Sandbox**（Topics API、Protected Audience API など）を進めていましたが、2024〜2025年に方針を転換し、廃止を見送りました。Privacy Sandbox の多くの API も縮小・廃止の方向と発表されています。
> この分野は変化が激しいので、**最新の公式発表を確認** してください。

## 7.5 同意管理（Consent）

GDPR などでは、広告目的でデータを使うには **ユーザーの同意** が必要です。
サイトでよく見る「Cookie を受け入れますか？」のバナーは **CMP**（Consent Management Platform）が表示しています。

```mermaid
flowchart LR
    U["👤 ユーザー"] -- "同意する / 拒否する" --> CMP["🍪 CMP<br/>（同意バナー）"]
    CMP --> STR["同意情報を文字列に変換<br/>（TCF / GPP 形式）"]
    STR --> SSP["SSP"]
    SSP -- "Bid Request の<br/>regs.gpp / user.consent" --> DSP["DSP"]
    DSP --> J{"このベンダーに<br/>同意がある？"}
    J -- Yes --> OK["パーソナライズ広告 OK"]
    J -- No --> NG["個人データを使わずに入札<br/>or 入札しない"]
```

| 仕組み | 地域 | 内容 |
|-------|-----|------|
| **TCF**（Transparency & Consent Framework） | 欧州 | IAB Europe の同意情報フォーマット |
| **GPP**（Global Privacy Platform） | 米国ほか | 複数地域の規制を1つの形式で扱える IAB Tech Lab の仕様 |

## 7.6 Cookie に頼らない広告手法

```mermaid
mindmap
  root((Cookieに頼らない手法))
    コンテキスト広告
      ページの内容で判断
      サッカー記事にスポーツ用品
    ファーストパーティデータ
      媒体社のログイン情報
      広告主の会員データ
    共通ID
      UID2
      ID5
      メールアドレスのハッシュ
    データクリーンルーム
      生データを渡さずに突き合わせ
    セラー定義オーディエンス
      媒体社が作ったセグメントを渡す
```

**コンテキスト広告** は「誰が」ではなく「**何を見ているか**」で広告を決めるため、個人を追跡しません。
AI による文章・画像の理解が進んだことで、近年あらためて注目されています。

---

⬅️ 前へ: [第6章 取引形態](06-deals.md) ｜ ➡️ 次へ: [第8章 透明性・品質・不正対策](08-quality-fraud.md)
