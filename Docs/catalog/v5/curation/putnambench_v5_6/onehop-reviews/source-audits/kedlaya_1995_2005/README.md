# Kedlaya Putnam 1995–2005 一度关系源审计

本目录物化了 1995–2005 年 Putnam A1–A6、B1–B6 共 132 道题的逐题 source-review。每题只保留一个经人工逐 span 确认、在标准解答中直接使用的 proposition-level claim target。

## 硬计数与 credit 边界

- accepted source-review relation edges：132
- covered problems：132/132
- accepted theorem-claim targets：132
- candidate / pending / rejected：0 / 0 / 0
- catalog credit：0
- theorem identity credit：0
- conjecture claim targets：0

这里的 `accepted_edge` 只表示“审阅者确认独立撰写的 proposition 确实在所指 source span 中作为直接证明步骤使用”。它不表示新增了 132 条 catalog 定理，也不建立 theorem identity、父版本 exact join 或 release entry。每行均明确设置 `catalog_credit=0`、`theorem_identity_credit=0`、`grants_release_entry=false`。

## 二次语义审计

132/132 行完成 summary-vs-span 二审：85 行直接通过，47 行因过泛、仅为方法标签或与 span 命题不够精确而重写，未审为 0。完整 CHANGE problem ID、最终 statement SHA-256 和 source-span SHA-256 绑定保存在 `receipt.json`，独立 checker 会逐行验证。

## 来源与版权边界

Kedlaya Putnam archive 在这里仅作 link-only 的非官方二手解答来源。本目录不 vendoring `.tex` 源文件，不保存解答原文、snippet、quote、可逆 trigger 或 source-text reconstruction material。Artifact 只保存：

- upstream URL 和相对文件名；
- 精确行区间、文件 SHA-256、span SHA-256；
- 独立撰写的 proposition statement；
- 零 identity/release credit 的审核结论。

## 文件与验证

- `kedlaya_1995_2005_onehop_relations.json`：132 条最终关系审计记录。
- `receipt.json`：artifact/checker/source hashes、计数、二审决策绑定与 CHANGE IDs。
- `check_kedlaya_1995_2005_onehop.py`：不导入生成器的只读独立 checker。

Checker 默认读取本轮冻结的只读外部快照 `/tmp/putnam-kedlaya-solutions-1995-2025`；也可用 `KEDLAYA_SOURCE_ROOT` 指向包含相同 `1995s.tex`–`2005s.tex` 与 `SHA256SUMS` 的快照：

```bash
python3 Docs/catalog/v5/curation/putnambench_v5_6/onehop-reviews/source-audits/kedlaya_1995_2005/check_kedlaya_1995_2005_onehop.py
```

Checker 会独立验证完整 11×12 题目分母、全部字段与 row hashes、source file/span hashes、problem-section 行边界、计数、版权/credit gates，以及 132 条 semantic-audit receipt bindings。
