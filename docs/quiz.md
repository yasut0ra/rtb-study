# 確認問題

各問題の「答えを見る」をクリックすると解答と解説が表示されます。

## 基本編

### Q1. 登場人物
次のうち、**広告主側（買い手側）** のツールはどれ？

1. SSP
2. DSP
3. アドサーバー（媒体社用）

<details markdown="1">
<summary>答えを見る</summary>

**2. DSP**（Demand-Side Platform）

SSP とアドサーバーは媒体社側（売り手側）のツールです。「Demand（需要）= 買いたい側」「Supply（供給）= 売りたい側」と覚えましょう。→ [第1章](01-overview.md)
</details>

### Q2. No Bid
DSP が入札しないとき、一般的に返す HTTP ステータスコードは？

<details markdown="1">
<summary>答えを見る</summary>

**204 No Content**

本文なしで返すことで、通信量を減らせます。→ [第3章](03-openrtb.md)
</details>

### Q3. tmax
Bid Request の `tmax: 120` は何を意味する？

<details markdown="1">
<summary>答えを見る</summary>

**120 ミリ秒以内に Bid Response を返してほしい** という締め切り。間に合わない入札は無視されます。→ [第2章](02-rtb-flow.md)
</details>

## 計算編

### Q4. セカンドプライス
フロア 100円、入札が A: 400円 / B: 250円 / C: 90円 のとき、セカンドプライス（+1円）で **勝者と支払額** は？

<details markdown="1">
<summary>答えを見る</summary>

**勝者 A、支払額 251円**

C はフロア未満なので失格。2位は B の 250円 なので、250 + 1 = 251円。
ファーストプライスなら A は 400円 を支払います。→ [第4章](04-auction.md)
</details>

### Q5. 入札額の計算
目標 CPA = 2,000円、pCTR = 0.4%、pCVR = 5% のとき、入札額（CPM）は？

<details markdown="1">
<summary>答えを見る</summary>

**400円**

$$
0.004 \times 0.05 \times 2000 \times 1000 = 400
$$

→ [第5章](05-dsp-bidding.md)
</details>

### Q6. 指標の計算
広告費 30万円、表示 600,000回、クリック 1,800回、購入 36件 のとき、**CPM・CTR・CPC・CPA** は？

<details markdown="1">
<summary>答えを見る</summary>

| 指標 | 計算 | 答え |
|-----|------|-----|
| CPM | 300,000 ÷ 600,000 × 1,000 | **500円** |
| CTR | 1,800 ÷ 600,000 | **0.3%** |
| CPC | 300,000 ÷ 1,800 | **約167円** |
| CPA | 300,000 ÷ 36 | **約8,333円** |

→ [第9章](09-metrics.md)
</details>

## 応用編

### Q7. ビッドシェーディング
ファーストプライスオークションで、DSP が評価額をそのまま入札すると何が問題になる？

<details markdown="1">
<summary>答えを見る</summary>

**払いすぎ（勝ったときの利益がゼロ）になる。**

評価額 = 支払額なので、勝っても得がありません。そこで勝率と利益のバランスを取り、期待利益が最大になる金額まで入札を下げます（ビッドシェーディング）。→ [第4章](04-auction.md)
</details>

### Q8. ads.txt
`famous-news.jp/ads.txt` に `ssp-a.example, 12345, DIRECT` だけが書かれている。
`site.domain = famous-news.jp`、SSP = `ssp-b.example` の Bid Request が来た。DSP はどうすべき？

<details markdown="1">
<summary>答えを見る</summary>

**入札を見送るべき。**

ssp-b.example は famous-news.jp が認めた販売者ではないため、ドメイン偽装（スプーフィング）の可能性があります。→ [第8章](08-quality-fraud.md)
</details>

### Q9. 取引形態
「在庫と価格を事前に保証し、オークションを行わない」取引形態は？

<details markdown="1">
<summary>答えを見る</summary>

**プログラマティック保証型（PG: Programmatic Guaranteed）**

優先取引（Preferred Deal）も価格は固定ですが、在庫の保証はなく、買い手は買わないこともできます。→ [第6章](06-deals.md)
</details>

### Q10. 考えてみよう
サードパーティ Cookie が使えない Safari のユーザーに対して、広告主が効果的に広告を届ける方法を2つ挙げてみよう。

<details markdown="1">
<summary>解答例を見る</summary>

- **コンテキスト広告**: ページの内容（例: ランニング記事）に合わせて広告を出す
- **共通 ID（UID2 など）**: ログインユーザーのメールアドレスのハッシュを使って識別する
- **媒体社のファーストパーティデータ**: PMP で媒体社が持つ会員セグメントを使う
- **データクリーンルーム**: 広告主と媒体社のデータを安全に突き合わせる

→ [第7章](07-privacy.md)
</details>
