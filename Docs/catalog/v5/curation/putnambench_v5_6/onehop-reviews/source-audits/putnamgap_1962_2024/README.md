# PutnamGAP 1962–2024 一度关系源审计

本目录物化了固定在 PutnamGAP commit `aee05407afc7e621e8d9c7f909f4f25ccb8131c0` 的 1962–2024 年 756 道 canonical solution 的关系审计。范围严格为每年 A1–A6、B1–B6。

## 计数与含义边界

- 共保存 910 条审计/发现记录。
- 47 条为逐 span 人工审阅后接受的**源内直接关系**：36 条非猜想关系，11 条显式猜想关系；后者按源内状态分为 4 条开放、7 条在源内已解决。
- 860 条由词法或结构扫描发现，全部是 `candidate_pending_human_review`，`credit_eligible=false`；它们没有定理、猜想或一度闭包的入库 credit。
- 另有 2 条 pending 和 1 条因仅是主题联系而 rejected 的记录。

这里的 `accepted_human_reviewed` 只表示“审阅者确认 pinned source span 确实表达了该直接关系”。它**不等于**：

- 已建立独立的 catalog theorem/conjecture identity；
- 已通过 catalog 收录、去重、状态或来源权威性门；
- 已成为 PutnamBench 一度闭包中的正式 edge；
- 已证明与现有 catalog claim 等价或不存在重复。

因此，下游必须另做 identity normalization、独立来源核验、去重和 catalog acceptance。不得把 47 直接加到正式定理库存，更不得把 860 个自动 candidate 当成已补定理。

## 版权边界

本目录不转载 Putnam 原题或 canonical solution 原文。关系文件只保存：

- 独立改写的 target/evidence 摘要；
- pinned repository path、commit、Git blob SHA-1、文件 SHA-256；
- decoded `solution` 字符偏移及 span SHA-256。

PutnamGAP 的项目原创变体和工具适用 CC BY 4.0；原 Putnam 题目与 canonical solutions 仍属于 MAA，不能据此视为 CC BY 4.0 内容。详情以 pinned upstream `LICENSE` 为准。

## 文件与校验

- `putnamgap_1962_2024_onehop_relations.json`：最终关系审计 artifact。
- `receipt.json`：artifact、checker、source tree 和计数回执。
- `check_relations.py`：不导入生成器的只读独立 checker。

Checker 默认使用本次审计冻结时的只读源镜像：

- tree：`/tmp/putnamgap-tree.json`
- dataset：`/tmp/putnamgap-audit.uYDPao/dataset`

也可分别通过 `PUTNAMGAP_TREE_SNAPSHOT` 与 `PUTNAMGAP_DATASET_ROOT` 指向内容相同的镜像。运行：

```bash
python3 Docs/catalog/v5/curation/putnambench_v5_6/onehop-reviews/source-audits/putnamgap_1962_2024/check_relations.py
```

Checker 会独立重建 756 题分母，并验证全部 910 条记录的 source file SHA-256、Git blob SHA-1、decoded-solution offset/span SHA-256、disposition credit gate、artifact/receipt 计数和文件哈希。
