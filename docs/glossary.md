# 用語集

本書に登場する主な用語を、五十音順とアルファベット順にまとめます。「章」の列は、その用語を詳しく説明している章です。

## 五十音順

| 用語 | 説明 | 章 |
|-----|------|-------|
| **アドエクスチェンジ** | 広告枠の売り手と買い手が取引する市場。オークションを実行する | [1](01-overview.md) |
| **アドサーバー** | 予約型広告や RTB の広告などを比較し、表示する広告を最終的に決めて配信するシステム | [1](01-overview.md) |
| **アドテク税** | 広告費のうち、媒体社に届くまでに中間事業者の手数料として差し引かれる部分の俗称 | [9](09-metrics.md) |
| **アドフラウド** | ボットなどによる不正な表示やクリックで、広告費をだまし取る行為 | [8](08-quality-fraud.md) |
| **インプレッション** | 広告が 1 回表示されること | [1](01-overview.md) |
| **ウォーターフォール** | SSP に優先順位を付け、順番に問い合わせる従来の方式 | [4](04-auction.md) |
| **クッキーシンク** | SSP と DSP がそれぞれ付与した Cookie の ID を対応づける仕組み | [7](07-privacy.md) |
| **コンテキスト広告** | ページの内容に合わせて広告を出す手法。個人を追跡しない | [7](07-privacy.md) |
| **収益等価定理** | 一定の条件のもとで、オークションの方式が違っても売り手の期待収益が等しくなるという経済学の定理 | [4](04-auction.md) |
| **セカンドプライスオークション** | 落札者が「2 位の入札額＋最小単位」を支払う方式。OpenRTB では Second Price Plus と呼ぶ | [4](04-auction.md) |
| **データクリーンルーム** | 生のデータを互いに渡さずに、複数の企業のデータを安全に突き合わせる環境 | [7](07-privacy.md) |
| **ディール ID** | PMP や優先取引などの特別な取引を識別する ID | [6](06-deals.md) |
| **ビッドシェーディング** | ファーストプライスで払いすぎないよう、勝率を考慮して入札額を引き下げる技術 | [4](04-auction.md) |
| **ビューアビリティ** | 広告が実際にユーザーから見える状態で表示されたかどうか | [8](08-quality-fraud.md) |
| **ファーストプライスオークション** | 落札者が自分の入札額をそのまま支払う方式。現在の主流 | [4](04-auction.md) |
| **フィルレート** | 広告リクエストのうち、実際に広告が表示された割合 | [9](09-metrics.md) |
| **フリークエンシーキャップ** | 同じユーザーに広告を表示する回数の上限 | [5](05-dsp-bidding.md) |
| **フロアプライス** | 媒体社が設定する最低落札価格 | [4](04-auction.md) |
| **ブランドセーフティ** | 不適切なページに広告が表示されないようにすること | [8](08-quality-fraud.md) |
| **ヘッダービディング** | 複数の SSP に同時に入札を募り、最も高い入札を選ぶ方式 | [4](04-auction.md) |
| **ペーシング** | 予算を期間中に適切なペースで消化するための調整 | [5](05-dsp-bidding.md) |
| **優先取引** | 特定の買い手に固定価格で優先的に広告枠を提供する取引。Preferred Deal | [6](06-deals.md) |
| **予約型広告** | 広告枠を期間や表示回数を決めて事前に契約する広告。純広告とも呼ぶ | [1](01-overview.md) |
| **リターゲティング** | 過去に自社サイトを訪れた人に広告を出す手法 | [7](07-privacy.md) |

## アルファベット順

| 用語 | 正式名称 | 説明 | 章 |
|-----|---------|------|-------|
| **AdCOM** | Advertising Common Object Model | 広告・端末などの共通オブジェクトと列挙値を定める IAB Tech Lab の仕様 | [3](03-openrtb.md) |
| **ads.txt** | Authorized Digital Sellers | 媒体社が自社の広告枠の正規の販売者を公開するファイル | [8](08-quality-fraud.md) |
| **ATT** | App Tracking Transparency | iOS のアプリが IDFA を使う際に、ユーザーの許可を求める仕組み | [7](07-privacy.md) |
| **CMP** | Consent Management Platform | 同意バナーを表示し、同意情報を管理する仕組み | [7](07-privacy.md) |
| **CPA** | Cost Per Acquisition | 1 コンバージョンあたりの費用 | [9](09-metrics.md) |
| **CPC** | Cost Per Click | 1 クリックあたりの費用 | [9](09-metrics.md) |
| **CPM** | Cost Per Mille | 1,000 回表示あたりの費用 | [9](09-metrics.md) |
| **CTR** | Click-Through Rate | クリック率 | [9](09-metrics.md) |
| **CTV** | Connected TV | インターネットに接続したテレビ。動画広告の成長分野 | [1](01-overview.md) |
| **CVR** | Conversion Rate | コンバージョン率 | [9](09-metrics.md) |
| **DMP / CDP** | Data Management Platform / Customer Data Platform | ユーザーデータを管理・活用する基盤 | [1](01-overview.md) |
| **DSP** | Demand-Side Platform | 広告主側の入札システム | [1](01-overview.md) |
| **eCPM** | effective CPM | 1,000 回表示あたりの実質的な収益 | [9](09-metrics.md) |
| **GDPR** | General Data Protection Regulation | EU の一般データ保護規則 | [7](07-privacy.md) |
| **GPP** | Global Privacy Platform | 複数の地域の同意情報を 1 つの形式で扱う IAB Tech Lab の仕様 | [7](07-privacy.md) |
| **IDFA / GAID** | Identifier for Advertisers / Google Advertising ID | iOS と Android の広告 ID | [7](07-privacy.md) |
| **MRC** | Media Rating Council | 広告計測の基準を定める米国の団体 | [8](08-quality-fraud.md) |
| **OpenRTB** | — | IAB Tech Lab が策定する RTB の標準仕様 | [3](03-openrtb.md) |
| **PG** | Programmatic Guaranteed | 在庫と価格を保証するプログラマティック取引 | [6](06-deals.md) |
| **PMP** | Private Marketplace | 招待された買い手だけが参加できるオークション | [6](06-deals.md) |
| **QPS** | Queries Per Second | 1 秒あたりのリクエスト数 | [9](09-metrics.md) |
| **ROAS** | Return On Ad Spend | 広告費に対する売上の比率 | [9](09-metrics.md) |
| **RTB** | Real-Time Bidding | インプレッションごとにリアルタイムで行われるオークション | [2](02-rtb-flow.md) |
| **schain** | SupplyChain Object | 広告枠の販売経路を記録した、Bid Request 内の情報 | [8](08-quality-fraud.md) |
| **sellers.json** | — | 広告システムが、自社のアカウントと販売者の対応を公開するファイル | [8](08-quality-fraud.md) |
| **SPO** | Supply Path Optimization | 効率のよい販売経路だけを選んで買う取り組み | [8](08-quality-fraud.md) |
| **SSP** | Supply-Side Platform | 媒体社側の販売システム | [1](01-overview.md) |
| **TCF** | Transparency & Consent Framework | IAB Europe が定める、欧州向けの同意情報の形式 | [7](07-privacy.md) |
| **tmax** | — | Bid Request に対する応答の締め切り（ミリ秒） | [3](03-openrtb.md) |
| **UID2** | Unified ID 2.0 | メールアドレスのハッシュ値などをもとにした業界共通の ID | [7](07-privacy.md) |
| **VAST** | Video Ad Serving Template | 動画広告（4.1 以降は音声広告も）を配信するための XML 形式 | [3](03-openrtb.md) |
