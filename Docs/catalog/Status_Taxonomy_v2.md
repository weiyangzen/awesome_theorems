# Catalog Status Taxonomy v2

> 规范版本：`status-taxonomy/2.0`
>
> 审计基准日期：`2026-08-10`
>
> 对应 schema：[`Claim_Record_Schema_v2.json`](./Claim_Record_Schema_v2.json)

## 1. 目的与边界

本规范把源目录中的一个“形式化状态”拆成互不替代的语义轴。它适用于四层 catalog record：

```text
ATO  source occurrence：不可丢失的源记录
ATF  family：别名、等价式、共同 proof/dependency 泄漏组件
ATS  sense：同名对象消歧后的语义
ATV  variant：具有精确 scope 的可陈述变体
```

`ATO/ATF/ATS/ATV` 是身份层次，不是质量等级。只有 ATV 才可能成为原子 benchmark task 的
直接来源；ATF 共属只约束 split/leakage，不授予真值、证明或形式化 credit。

本规范不宣称现有占位目录已经有逐条 citation。迁移时宁可保留 `unknown`、`missing`、
`unreviewed` 或 `blocked`，也不得生成看似具体但无法定位的来源、日期、证明或 replay receipt。

## 2. 不可折叠的状态轴

| 轴 | 回答的问题 | 明确不能推出什么 |
|---|---|---|
| `source_status_raw` | 源文件原样写了什么 | 不能直接推出任何 current status |
| `claim_kind` | 当前记录究竟是 theorem、conjecture、model、algorithm、non-claim 等哪类对象 | 名称含“定理/猜想/问题”不构成裁决 |
| `statuses.human_truth` | 对冻结 exact claim，人类数学/理论证据目前支持什么 | 不推出经验支持、机器证明或本仓闭包 |
| `statuses.empirical` | 在冻结 regime、observable、数据与误差模型下，经验状态如何 | `observed` 不等于普适数学定理已证 |
| `statuses.external_formalization` | 仓库外是否有可定位 formal artifact | 不推出本仓已经 pin、import 或 replay |
| `statuses.repo_integration` | 本仓当前 revision 实际走到了哪一级 | 文件存在不等于 declaration/type/axiom/replay 已核验 |
| `provenance` | 来源是否从线索升级为 pinned primary evidence 并经过复核 | 通用书目不认证某一 exact statement/status |
| `benchmark_eligibility` | 该 record 是否具备派生 task 的先决条件 | 不等于 task、split、scorer 或 benchmark release 已存在 |

任何 UI、导出表或统计不得重新把这些轴压成一个“已验证”。

## 3. 身份、kind 与 exact statement

### 3.1 身份不随状态漂移

- ID 由 append-only registry 分配，不编码学科、名称、claim kind、真值或 mutable text hash。
- 更正名称、status、statement、domain、regime 或 source locator 不改变既有 ID。
- legacy `THM-*` 永久保留为 alias；不得把旧 alias 重新绑定到另一个后代。
- aggregate split 后，旧 ATV 标为 `split` 并返回全部 current children；不得偷偷选择其中一个。
- confirmed merge 使用一跳 redirect；证据必须逐个检查适用性，不能仅因 merge 自动继承。

### 3.2 名称不是分类器

历史名称可以保留在 `identity.labels[role=historical]`，但不能决定
`claim_kind.current_kind` 或 `statuses.human_truth.status`：

- “塞尔猜想”“莫德尔猜想”“庞加莱猜想”等历史名称可以对应 current theorem/proved；
- “选择公理”是 axiom，不是因为源表写“已验证”就变成 theorem；
- Church–Turing 是 thesis；可证明的模型等价结果应另建 theorem variant；
- 方程、模型、器件、方法、数据集和 proof event 可以进入 catalog，但不是 theorem denominator；
- 名称含“问题”的判定问题可能已有正解、负解或复杂度上界，不能一律标 open。

词法规则只允许产生 `classification_review.status=machine_triage`，不得自动 merge、delete、
upgrade truth 或赋予 benchmark eligibility。

### 3.3 exact statement 完整度

`exact_statement.completeness` 的顺序只表达结构完整度：

```text
missing
not_applicable
source_prose
normalized_prose
exact_structured
exact_formal
```

`exact_structured` 至少冻结 ordered binders、domain、quantifier、全部 hypotheses、conclusion
与 scope。学科 scope 还应包含：

- 数学：base theory、axioms、regularity、initial/boundary conditions；
- 物理：model、regime、units/normalization、approximations、IC/BC、frame/gauge、observable、error；
- CS：computation model、encoding、resource、case semantics、randomness、adversary、fault、security parameter。

`exact_formal` 只说明有一份 content-bound formal surface；它不自动表示 proof 已 kernel-check。

## 4. 来源与日期合同

### 4.1 空缺必须诚实

若没有逐条来源：

```text
provenance.status = missing
provenance.evidence_refs = []
license.status = unknown
license.spdx_expression = null
license.evidence_refs = []
human_truth.status = unknown
external_formalization.status = unknown
repo_integration.status = unknown 或经本仓全量 inventory 证明后的 absent
benchmark_eligibility.status = blocked/not_evaluated
benchmark_eligibility.blocking_reasons 包含 rights_unresolved
```

不得为了通过 schema 填入百科首页、搜索结果页、无法定位到 theorem/status 的通用教材，或虚构的
DOI、页码、revision、访问日期。`unknown` 是迁移成功状态，不是需要掩盖的失败。

### 4.2 material status 的最小证据

下列 human status 一旦被主动赋值，必须同时具有完整 `as_of` 日期和至少一条可解析
`source_refs`：

```text
proved, refuted, open, partial, independent, conditional, disputed
```

其中来源必须能定位到 exact scope，而不只是出现相同名称。优先顺序是：

1. primary proof/counterexample/consistency paper 或官方 status page；
2. 权威机构、标准或项目的 revision-pinned 页面；
3. 独立 scholarly review，用于确认 current/disputed status；
4. bibliographic lead 只能保留为 lead，不能单独触发 status upgrade。

每个 evidence reference 至少有 URI、DOI、arXiv ID、ISBN+页码、repository+revision，或
local path+Git blob 中的一种定位方式。网页应记录 `accessed_at`；仓库/形式化结论应 pin revision，
需要重放或逐字认证时还应保存 content hash。

Schema 能检查 nonempty reference ID，不能检查 ID 是否确实存在或适用。catalog validator 还必须检查：

- 所有 `source_refs` 唯一解析到本 record 的 `provenance.evidence_refs`；
- source kind 与被支持的 status 相容；
- locator/revision/hash 可读取且没有悄悄漂移；
- 引文的 scope、前提和结论确实覆盖当前 ATV。

### 4.3 日期语义

- `as_of` 是 current status 的审查截止日，必须为 `YYYY-MM-DD`；
- `proposed_at/resolved_at` 使用证据允许的最早诚实精度：年、月或日；
- 不得把提出时间、预印本时间、正式发表时间、证明完成时间与本仓 replay 时间混为一列；
- 不知道日/月时保留年精度，不得自动补 `01-01`；
- status change 只追加 `status_history` event，不重写或删除旧事件。

## 5. Human-truth taxonomy

| 值 | 规范含义 |
|---|---|
| `unknown` | 尚无足够证据完成 current scope 裁决；默认迁移值 |
| `proved` | exact claim 有满足政策的证明证据；可有 affirmative 或 negative answer polarity |
| `refuted` | exact proposition 为假，并有具体 counterexample/witness/否证链 |
| `open` | exact scoped proposition 截至 `as_of` 仍未解决，且有 current-status source |
| `partial` | 已冻结哪些子 scope/方向闭合、哪些仍开放；不能只写“有进展” |
| `independent` | 相对指定 base theory，正反方向及 consistency assumptions 均有证据 |
| `conditional` | 当前 conclusion 只在列出的 assumptions 下成立；assumption status 不得省略 |
| `disputed` | 存在 proof claim，但尚未通过项目规定的独立接受政策 |
| `not_applicable` | 该 record 不是 truth-apt claim；须由 kind review 支持 |

`unknown` 与 `open` 不同：`unknown` 表示 catalog 尚未审清，`open` 是有日期、有 exact scope、
有 status source 的正面学术判断。

## 6. 历史猜想与已解决问题

历史名称和 current status 分开保存：

```text
claim_kind.historical_kind = conjecture/hypothesis/open_problem
historical_status.classification = historical_...
claim_kind.current_kind = theorem（若 exact claim 已证）
human_truth.status = proved/refuted/independent/...
```

已解决历史猜想至少需要：

- historical name 与 source；
- proposed date（按可证精度）；
- exact current scope；
- `resolved_at` 与 resolution source；
- `resolution_kind`；
- proof event 与 claim 本身分离，使用 `proof_event_for` relation。

名称仍含“猜想”不会让它回到 open。反过来，某一 family 的特殊情形已证，也不能把更一般的
同名 family 全部标 proved。若不同版本混在一句中，先拆 ATV：solved special case 与 general-open
variant 分别维护 status。

典型迁移模式包括：

- Quillen–Suslin/Serre、Faltings/Mordell、Mihăilescu/Catalan、Perelman/Poincaré 等：
  historical claim 与 proof event 建 relation，不重复计入两个独立 theorem successes；
- 四维 Poincaré：topological solved 与 smooth open 必须是两个 scope；
- Riemann–Hilbert：positive restricted theorem、unrestricted counterexample 与不同现代 sense 分开；
- André–Oort、Zimmer、Kakeya 等带有多个版本和近期 proof claims 的 family：以 exact theorem
  scope 和独立评审政策裁决，不能按标题整体升级。

## 7. Open 与 partial

`open` record 必须满足：

1. exact binders/domain/hypotheses/conclusion；
2. scope 不混合 equation/object、special case、general family 与 proof programme；
3. `as_of` 为本轮审查日期；
4. 至少一条近期权威 status source；
5. known special cases、equivalences 与 barrier results 通过 relation 或独立 ATV 表达；
6. benchmark 只能进入独立 `open_challenge` 或 audit 轨，不进入 ordinary proof pass-rate。

`partial` 不能是模糊的“部分证明/部分进展”。它必须列出已闭合和未闭合的各个 scope；若做不到，
保守降为 `unknown` 并加入 `scope_incomplete`/`missing_status_source` blocker。

Clay family、ABC disputed claim、cosmic censorship、Navier–Stokes regularity、P vs NP、VP vs VNP、
UG/quantum PCP 等都必须按上述门逐条审查。源表的 `未解决/待研究/待证明` 只形成 triage candidate。

## 8. Refuted、negative solution 与 undecidability

三者不可混淆：

- `refuted`：原命题为假，必须提供具体 counterexample/witness。例如一个“所有对象都满足 P”
  被对象 `x` 否定；`human_truth.answer_polarity` 通常不是 negative solution。
- `negative solution`：一个“是否存在/是否可判定”的问题得到否定答案，但相应 impossibility/
  undecidability theorem 是 `proved`，并设 `answer_polarity=negative`。
- `undecidability_result`：是 current claim kind；它可以是 proved theorem，而不是 human status
  `refuted` 或 catalog 不可判定。

因此，Hilbert 第十问题的不可算法判定结论、停机问题不可判定性等应记录为 proved negative
solution；Euler/费马素数等普遍性猜想若有反例，则记录 refuted 并保存 witness。经验数据与某模型
不符时先用 `empirical=falsified_in_scope`；除非 exact mathematical proposition 也被否证，不能同步
写 `human_truth=refuted`。

## 9. Independence

`independent` 必须显式记录：

- `base_theory`，例如 ZF、ZFC 或另一固定形式系统；
- positive direction 的相对一致性/不可证证据；
- negative direction 的相对一致性/不可否证证据；
- 所有 consistency assumptions；
- 两个方向各自适用的 exact formulation 与 source。

“独立于 ZFC”不是“尚未找到证明”，也不是“在更强公理下没有真值”。CH、GCH、Suslin 等
record 不能共享一段笼统独立性文字；每一项必须绑定自己的 exact statement、base theory 和双向链。
公理（如 `V=L`）本身的 kind 也不能因独立性结果而被改写成 theorem。

## 10. Conditional claims

条件命题有两种不同 catalog 表达：

1. 若 exact claim 本身是 `A -> B` 且该 implication 已证：
   `human_truth=proved`，`conditionality.mode=implication_is_exact_claim`。这不授予 `A` 或 `B`
   单独的 proved status。
2. 若 record 的 conclusion 是 `B`，目前只知在 `A` 下成立：
   `human_truth=conditional`，`conditionality.mode=conclusion_under_assumptions`，并列出 A 的
   exact statement、status 与 source。

Ladner、Karp–Lipton 等 implication theorem 可属于第一类；不能由此声称 `P != NP` 或其 consequent
无条件成立。密码学安全归约必须列出计算模型、security parameter、adversary 与 hardness
assumption。物理模型推导必须列出 regime/approximation；“模型内条件推导成立”不自动升级现实宇宙
中的 empirical status。

`claimed proof` 不等于 conditional 或 proved。若 proof claim 尚未满足本项目的独立评述政策，使用
`human_truth=disputed`；只有 primary claim 而无独立 current-status source 时保持 `unknown`。

## 11. 物理状态的双轨与 scope

物理记录至少区分三种问题：

```text
human_truth：给定数学模型内的推导/定理是否成立
empirical：冻结 regime/observable/error 后，现实证据支持到什么程度
external/repo formalization：是否存在机器检查，以及本仓是否 replay
```

常见错误及修订规则：

- law/model/effect/observation/device 不能统一写 theorem；
- `observed/precision_tested/model_supported` 都必须绑定数据 release、observable、单位与误差；
- `unobserved` 只表示给定灵敏度和参数空间未观测，不等于理论被 refuted；
- effective law 的适用范围、近似阶与 normalization 是 statement 的组成部分；
- AdS/CFT、cosmic censorship、no-boundary、ergodic/ETH、confinement 等 family 必须拆 exact
  pair/variant/regime，不能用一个泛化 slogan 获得 `proved` 或 `verified`；
- 已解决的 solar/atmospheric-neutrino anomaly 是历史 observation/problem 与解释证据链，不能把
  “已解决”迁移成 universal theorem 或 repo proof credit。

经验轴的值不是单一线性等级。例如 `model_supported` 与 `precision_tested` 回答不同问题；聚合统计
必须按 track 和 observable 分层，不能把它们压成一个百分比。

## 12. External formalization 与 repo integration

### 12.1 External formalization

`kernel_checked` 至少需要：

- prover/system 与精确 toolchain；
- repository revision；
- file/module、declaration 与 exact type hash；
- imports/axiom report；
- placeholder-free 检查；
- 可定位 replay receipt。

论文说“formalized”、仓库 README、同名 theorem 或 wrapper 文件存在都不足以升级到
`kernel_checked`。只找到 statement 用 `statement_only`；只闭合部分 branches 用 `partial`；
没有做完整搜索时用 `unknown`，不要轻率声称 `no_artifact_identified`。

### 12.2 Repo integration

本仓轴只报告当前 pinned tree 的事实：

```text
unknown -> absent -> intake -> source_frozen -> statement_checked
        -> anchor_pinned/partial_proof_checked -> proof_checked -> release_accepted
```

这不是自动升级链：每一级都有自己的 evidence gate。`anchor_pinned` 只证明 exact external anchor
被 pin/check，不等于 proof body vendored；`proof_checked` 必须有当前 revision receipt；
`release_accepted` 还需要独立 master acceptance。receipt 漂移、dependency 漂移、placeholder 或
semantic validator 失败时追加 `invalidated` event，不删除旧成功记录。

## 13. Provenance、classification review 与 confidence

### 13.1 Provenance 等级

```text
missing
bibliographic_lead
primary_pinned
independently_reviewed
```

等级只描述 evidence closure。`bibliographic_lead` 可以帮助后续研究，但不能触发 material status。
`independently_reviewed` 要求 reviewer 检查 exact scope 与引用适用性，而不是只检查 URL 能打开。

顶层 `license` contract 与 `provenance` 分开。它独立记录 `status`、SPDX expression、
`redistribution_scope` 与 license-specific `evidence_refs`；不得把书目来源当成许可结论。即使命题事实
是公共知识，题面原文、翻译、证明、图片、代码和数据仍可能有不同许可。license 未清晰时 record
可以留在 catalog，但 `rights_unresolved` 必须保留，benchmark derivation 保持 blocked。

### 13.2 Review 与 confidence

`classification_review.status` 依次允许 machine triage、human review、domain-expert review 或
disputed。`confidence` 是 0--1 的审核元数据，不是概率真值，也不替代 source：

- lexical/heuristic confidence 再高也不能把“猜想”自动判 open/solved；
- human review 若无来源只能完成 kind/sense triage，不能升级 material status；
- disputed classification 必须保留双方 scope/rationale，不得用平均 confidence 消除争议；
- status upgrade 的 reviewer、时间、理由和 sources 进入 append-only history。

## 14. Benchmark eligibility

record-level 值为：

```text
not_evaluated
ineligible
blocked
eligible_catalog_only
eligible_for_task_derivation
```

`eligible_for_task_derivation` 只表示可以交给后续 TASK schema；不表示 benchmark task 已生成、
scorer 已通过、split 已冻结或 release 已发布。最小 gate 是：

1. ATV identity 与 family/sense 已审；
2. `atomicity=atomic` 且 `truth_apt=yes`；
3. exact structured/formal statement 与全部学科 scope 完整；
4. primary pinned provenance，必要时有独立 current-status review；
5. 顶层 `license` 明确；可再分发内容须有 SPDX expression，citation-only 必须冻结分发边界；
6. family split group 已给定；
7. classification 至少 human-reviewed；
8. blocking reasons 为空；
9. 选择与 status 相容的 track。

非 claim、aggregate、历史 proof event、method、device、dataset 不进入 theorem pass-rate。open claim
只能进入 `open_challenge`/audit 等不以证明闭合作普通成功的轨。physics numerical task 还需数据、
tolerance、unit/error oracle；CS task 还需 encoding、resource/adversary/fault model；proof task 还需
formal environment、scorer、negative fixtures 与 no-placeholder policy。

## 15. 保守迁移表

原始字符串永久原样写入 `source_status_raw`。下面只给默认迁移动作，不给 truth 映射：

| 原始例值 | 默认 current axes | 允许升级的附加证据 |
|---|---|---|
| `已验证/已证明/已解决` | human=`unknown`；external=`unknown`；repo=`unknown/absent` | exact claim + proof/status source；formal/repo 各自另过 gate |
| `可验证` | 所有实质轴 `unknown` | “原则上可形式化”不产生 formal credit |
| `未解决/待解决/待证明/待研究` | human=`unknown`，kind/status triage candidate | exact scope + dated current-status source 后才可 `open` |
| `部分证明/部分解决/部分进展` | human=`unknown` | 明确 solved/open scope split 后可 `partial` 或拆 ATV |
| `声称证明` | human=`unknown` 或政策确认后的 `disputed` | primary proof claim + 独立 status review |
| `独立于ZFC` | human=`unknown` | base theory、双方向、consistency assumptions 与 sources |
| `已否证` | human=`unknown` | exact counterexample/witness 与 resolution date/source |
| `不可判定` | human=`unknown` | 先判断它是 proved undecidability theorem，还是 catalog 未裁决 |
| `准多项式时间解决` | human=`unknown` | exact algorithmic upper bound 可 proved；更广 complexity classification 仍可 open |
| `不可形式化` | kind/status review candidate | thesis/non-claim 与可 formalize 的模型等价 theorem 分开 |

禁止以下自动映射：

```text
source 已验证 -> human proved
source 已验证 -> external kernel_checked
source 已验证 -> repo proof_checked
存在 .lean 文件 -> repo proof_checked
historical 名称含猜想 -> human open
问题得到否定答案 -> human refuted
实验观测 -> human proved
family 中一个 special case solved -> 整个 family solved
```

## 16. 升级、降级与验收门

### 16.1 升级

每次升级必须是 append-only event，绑定：axis、previous/new value、exact scope、`as_of`、reason、
reviewer 和 source refs。不得由另一轴的状态替代本轴证据。

### 16.2 纠错与失效

发现 scope 错误、proof gap、retraction、counterexample、artifact drift 或 replay failure 时：

- 不删除历史 event；
- 追加 corrected/invalidated event；
- 更新 current projection；
- 若 aggregate 需拆分，冻结旧 ID 并返回 children；
- 下游 TASK 自动失去 current eligibility，直到重新验证。

### 16.3 最低验收检查

- 每个 material source ref 可解析并适用于 exact ATV；
- open/refuted/independent/conditional/disputed 全有 `as_of` 和专属字段；
- historical resolution 有 proposed/resolved date（按诚实精度）与来源；
- negative solution 没有被写成 refuted；
- implication theorem 没有把 consequent 无条件升级；
- empirical、external formal、repo、benchmark 没有从 human truth 推断；
- missing evidence 保持空数组与 unknown，不含伪 citation；
- eligible record 满足 schema gate，但 release 状态仍由独立 TASK/release 契约管理。

结构语法检查：

```bash
python3 -m json.tool Docs/catalog/Claim_Record_Schema_v2.json >/dev/null
```

完整实现还应使用支持 JSON Schema Draft 2020-12 的 validator，并增加跨引用、append-only、
source applicability、ID stability 与 adversarial mutation tests；`json.tool` 只验证 JSON 语法。
