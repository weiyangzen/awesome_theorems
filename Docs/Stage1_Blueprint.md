# Stage1 Blueprint

## 定位

- 本文件是 Stage1 的 Lean 4-only 数学高难度 proof blueprint。
- 本文件是生成的候选队列，不是 theorem completion 或 live execution-state authority。
- 每个条目的规范 authority 是 `Docs/Stage1_Blueprint_rev-5.6.md`；仓库级选取规则服从 `Docs/Blueprint_Guidelines.md`。
- `THM-M-0387` 是历史兼容 fixture，不是允许硬编码定理、路径、指标、公理或状态的模板。
- rev-5.6 的规范 cover 是 `Docs/Stage1_Blueprint_Applicable_Theorems.md` 中且仅其中的 `1546` 个目标 ID；全部统一为 `L0 / rework_required`。
- 本文件保留的 `300` 个旧 slot 只用于发现历史文件和安排返工；不提供更高 assurance、proof credit 或门禁豁免，其余 `1246` 个目标同样按完整标准执行。
- 非数学条目、非 Lean4 路线、纯实验/模型检验路线、以及当前主命题仍为 open / independent / refuted / undecidable 的条目不进入本 Stage1 主队列。
- Stage1 入选只表示进入 Lean 4 proof execution queue，不表示该 theorem 已 repo-local machine-checked。

## 仓库级债务规则

- `mathematical_debt`: 允许存在，用于组织未来猜想或 open-problem 研究；但本 Stage1 主队列默认排除主命题未闭合的条目。
- `formalization_debt`: 允许存在，是本 Stage1 的主要工作对象；含义是人类证明已知但 Lean 4 kernel closure 尚未完成。
- `repo_local_integration_debt`: 不允许作为完成态存在；若外部 Lean 4 机器证明存在，必须 pin/import/check 或列为 integration blocker。
- 完成态只允许 `local_proof_body`、`local_wrapper_upstream_mathlib`、`external_upstream_pinned`；anchor-only URL/theorem name 不计完成。

## 选择算法

- Stage0 去重后总条目: `3262`；去重移除: `76`。
- Stage0 数学条目: `1601`。
- Stage1 eligible 数学条目: `1546`。
- Stage1 selected 数学条目: `300`。
- 排除的数学债/非主队列 bucket: `{'open': 25, 'refuted': 3, 'undecidable': 1, 'independent': 4}`。
- 排除的 conjecture-named / 声称证明条目: `45`。
- 难度分由领域权重、形式化状态、命名关键词、陈述复杂度与 M0387 flagship override 合成；同一子类设置 soft cap，避免单一领域挤满 300 个 slot。
- 本选择算法是 execution triage，不是数学价值排名；后续执行可因 primary-source audit 结果调整 lane。

## Stage1 Lane 统计

| lane | count |
|---|---:|
| `hard_mathlib_anchor_and_wrapper` | 259 |
| `frontier_deep_formalization_debt` | 28 |
| `known_partial_branch_deepening` | 8 |
| `hard_statement_first_partial_verification` | 4 |
| `flagship_deep_formalization_debt` | 1 |

## 入选子类统计

| 子类 | count |
|---|---:|
| 几何学 / 代数几何 | 36 |
| 数论 / 代数数论 | 36 |
| 微分方程 / 偏微分方程 | 36 |
| 其他重要领域 / 数学物理 | 36 |
| 概率论与随机过程 / 随机过程 | 36 |
| 概率论与随机过程 / 概率论基础 | 36 |
| 数论 / 丢番图方程 | 21 |
| 拓扑学 / 代数拓扑 | 16 |
| 几何学 / 微分几何 | 12 |
| 代数学 / 同调代数 | 11 |
| 代数学 / 范畴论 | 8 |
| 拓扑学 / 微分拓扑 | 5 |
| 分析学 / 泛函分析 | 3 |
| 数论 / 解析数论 | 3 |
| 数理逻辑 / 模型论 | 3 |
| 代数学 / 域论 | 1 |
| 其他重要领域 / 动力系统 | 1 |

## Completion Gate

此生成文件中的 `[ ]` 是候选队列标记。条目只有在独立的结构化 instance/state/evidence bundle 中通过下列门禁后，才可在对应 authority 中升级；不得直接编辑本生成文件制造完成态：

1. canonical Lean 4 target 已 elaboration/fingerprint，等价形式有 checked transport。
2. obligation universe 在观察状态前冻结，typed proof/refinement/provenance/trust/workflow graphs 通过验证。
3. wrapper、terminal body、axiom/TCB 与全传递依赖来源已解析；unique coverage 不受 alias/refactor 影响。
4. structured node recipes 在 immutable clean snapshot 中执行，生成 content-addressed receipts。
5. clean empty-cache cold build、network-denied offline replay、dependency cleanliness/SBOM/license 门禁通过。
6. 每个 leaf 有 substantive semantic ledger；`<=100` 只决定是否继续拆分。
7. required H/R 节点有 pinpoint source crosswalk、unique readable anchor 和独立 review。
8. 第二个独立 runner 和 independently implemented minimal verifier 同意结果。
9. deterministic evidence bundle 生成 README/meta/audit/status；audit 与 theorem completion 分开决定。

## Selected Theorems

## 数论 / 丢番图方程

### S1-M-001 / THM-M-0387 费马大定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 丢番图方程`
- 源文档形式化状态: `部分验证（n=3、n=4 与 regular primes 已 machine-checked；全证明进行中）`；Stage0 bucket: `partial`
- 难度分: `279`；Stage1 lane: `flagship_deep_formalization_debt`；profile: `arithmetic_geometry_number_theory`
- 定理内容: x^n+y^n=z^n (n>2)无正整数解
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: regular primes 的 `repo_local_integration_debt` 已还清；完整 Wiles/Taylor-Wiles 主线保留 `formalization_debt`；无 active repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-002 / THM-M-0392 莫德尔方程

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 丢番图方程`
- 源文档形式化状态: `部分解决`；Stage0 bucket: `partial`
- 难度分: `173`；Stage1 lane: `known_partial_branch_deepening`；profile: `arithmetic_geometry_number_theory`
- 定理内容: y²=x³+k的整数解
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 允许存在 `formalization_debt` 或局部分支数学债；若发现外部 Lean 4 机器证明，必须立即 pin/import/check，不能留下 `repo_local_integration_debt`。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-003 / THM-M-0388 佩尔方程

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 丢番图方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: x²-Dy²=1的整数解
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-004 / THM-M-0390 卡塔兰猜想

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 丢番图方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 8和9是唯一的连续幂
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-005 / THM-M-0391 米哈伊列斯库定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 丢番图方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 卡塔兰猜想的证明
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-006 / THM-M-0393 图埃定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 丢番图方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 某些丢番图方程的有限解
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-007 / THM-M-0394 西格尔定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 丢番图方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 曲线上整点的有限性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-008 / THM-M-0395 法尔廷斯定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 丢番图方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 曲线上有理点的有限性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-009 / THM-M-0396 贝克定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 丢番图方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 对数线性形式的下界
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-010 / THM-M-0397 贝克方法

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 丢番图方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 丢番图方程的有效解法
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-011 / THM-M-0398 图埃-西格尔-罗特定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 丢番图方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 代数数的逼近
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-012 / THM-M-0399 罗特定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 丢番图方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 代数数的有理逼近
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-013 / THM-M-0400 子空间定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 丢番图方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 联立逼近的子空间界
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-014 / THM-M-0401 施密特定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 丢番图方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 代数数的联立逼近
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-015 / THM-M-0402 Evertse定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 丢番图方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: S-单位方程的解数
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-016 / THM-M-0403 舒利克维-埃弗特斯定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 丢番图方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 线性递推序列的零点
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-017 / THM-M-0404 Skolem-Mahler-Lech定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 丢番图方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 线性递推序列的零点
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-018 / THM-M-0405 比拉斯基定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 丢番图方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 线性递推序列的素因子
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-019 / THM-M-0406 科利特-埃弗特斯定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 丢番图方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 曲线上整点的退化性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-020 / THM-M-0389 马尔可夫方程

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 丢番图方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `148`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: x²+y²+z²=3xyz的整数解
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-021 / THM-M-0412 皮尔斯猜想

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 丢番图方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `148`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 某些三次曲线的整数点
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

## 几何学 / 代数几何

### S1-M-022 / THM-M-0133 怀尔斯定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `进行中（作为 FLT 全证明链，公开完整 machine-checked 版本尚未完成）`；Stage0 bucket: `partial`
- 难度分: `223`；Stage1 lane: `known_partial_branch_deepening`；profile: `algebraic_geometry`
- 定理内容: 费马大定理的证明
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 允许存在 `formalization_debt` 或局部分支数学债；若发现外部 Lean 4 机器证明，必须立即 pin/import/check，不能留下 `repo_local_integration_debt`。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-023 / THM-M-0115 格罗滕迪克黎曼-罗赫定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `200`；Stage1 lane: `frontier_deep_formalization_debt`；profile: `algebraic_geometry`
- 定理内容: 概形的黎曼-罗赫公式
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-024 / THM-M-0111 小平嵌入定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `186`；Stage1 lane: `frontier_deep_formalization_debt`；profile: `algebraic_geometry`
- 定理内容: Hodge流形的射影性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-025 / THM-M-0113 霍奇分解定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `179`；Stage1 lane: `frontier_deep_formalization_debt`；profile: `algebraic_geometry`
- 定理内容: Kähler流形的上同调分解
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-026 / THM-M-0130 志村簇

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `179`；Stage1 lane: `frontier_deep_formalization_debt`；profile: `algebraic_geometry`
- 定理内容: Hodge型志田簇的构造
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-027 / THM-M-0105 黎曼-罗赫定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `178`；Stage1 lane: `frontier_deep_formalization_debt`；profile: `algebraic_geometry`
- 定理内容: 代数曲线的除子理论
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-028 / THM-M-0148 森重文极小模型纲领

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `部分完成`；Stage0 bucket: `partial`
- 难度分: `171`；Stage1 lane: `known_partial_branch_deepening`；profile: `algebraic_geometry`
- 定理内容: 高维代数簇的双有理分类
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 允许存在 `formalization_debt` 或局部分支数学债；若发现外部 Lean 4 机器证明，必须立即 pin/import/check，不能留下 `repo_local_integration_debt`。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-029 / THM-M-0104 贝祖定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: 代数曲线交点个数的上界
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-030 / THM-M-0106 诺特正规化引理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: 仿射簇到仿射空间的有限态射
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-031 / THM-M-0107 扎里斯基主定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: 双有理态射的性质
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-032 / THM-M-0108 周炜良定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: 射影簇的代数性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-033 / THM-M-0109 周炜良引理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: 代数簇的坐标环性质
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-034 / THM-M-0110 小平消没定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: 正线丛的上同调消没
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-035 / THM-M-0112 莱夫谢茨超平面定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: 超平面截面的拓扑性质
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-036 / THM-M-0116 塞韦里群有限生成定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: 代数曲面的Néron-Severi群有限生成
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-037 / THM-M-0117 莫爱泽松定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: Moisezon流形的代数性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-038 / THM-M-0119 川又消没定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: 对数典范奇点的消没定理
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-039 / THM-M-0120 森重文锥定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: 代数簇锥的有限生成性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-040 / THM-M-0121 森重文有理性定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: Fano簇的有理性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-041 / THM-M-0122 法尔廷斯定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: Mordell猜想的证明
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-042 / THM-M-0123 莫德尔猜想

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: 代数曲线有理点的有限性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-043 / THM-M-0124 马宁-德林费尔德定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: 椭圆曲线上Heegner点的性质
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-044 / THM-M-0125 格罗斯-扎吉尔公式

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: 椭圆曲线导数的公式
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-045 / THM-M-0126 志村曲线定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: 四元数代数上的模曲线
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-046 / THM-M-0128 志村互反律

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: CM域的类域论
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-047 / THM-M-0129 志村提升定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: 模形式的提升
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-048 / THM-M-0131 志村对应

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: 椭圆曲线与模形式的对应
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-049 / THM-M-0132 谷山-志村猜想

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: 椭圆曲线与模形式的对应
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-050 / THM-M-0134 布灵-约克定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: 对称群表示论
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-051 / THM-M-0135 麦克唐纳恒等式

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: 仿射根系上的恒等式
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-052 / THM-M-0136 卡茨-穆迪代数

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: 无穷维李代数的分类
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-053 / THM-M-0137 卡茨-彼得森特征标公式

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: 仿射李代数的特征标
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-054 / THM-M-0138 贝林森-伯恩斯坦局部化

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: D-模与表示论的对应
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-055 / THM-M-0139 卡日丹-卢斯蒂格猜想

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: 表示论中Kazhdan-Lusztig多项式
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-056 / THM-M-0140 卡日丹-卢斯蒂格基

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: Hecke代数的典范基
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-057 / THM-M-0141 卢斯蒂格典范基

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 代数几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `algebraic_geometry`
- 定理内容: 量子群的典范基
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 scheme、sheaf、category theory、commutative algebra、topology API。
- Stage1 partial verification scope: 先验证 statement shape、核心对象定义、局部性质稳定性、特殊 base/ring 情形，以及可由 mathlib import 直接检查的 wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 对象/态射定义 -> 局部化/覆盖 -> sheaf/cohomology 层 -> base change / descent -> 主定理 branch。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: scheme/cohomology/descent API 深，许多论文级标准事实需要拆成可命名 lemma；优先锁定已在 mathlib 存在的局部结构。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

## 数论 / 代数数论

### S1-M-058 / THM-M-0430 朗兰兹互反律

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `部分证明`；Stage0 bucket: `partial`
- 难度分: `201`；Stage1 lane: `known_partial_branch_deepening`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 伽罗瓦表示与自守表示的对应
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 允许存在 `formalization_debt` 或局部分支数学债；若发现外部 Lean 4 机器证明，必须立即 pin/import/check，不能留下 `repo_local_integration_debt`。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-059 / THM-M-0431 局部朗兰兹对应

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `184`；Stage1 lane: `frontier_deep_formalization_debt`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 局部域的朗兰兹对应
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-060 / THM-M-0432 函数域朗兰兹对应

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `184`；Stage1 lane: `frontier_deep_formalization_debt`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 函数域的朗兰兹对应
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-061 / THM-M-0433 洛朗·拉福格定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `184`；Stage1 lane: `frontier_deep_formalization_debt`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 函数域GL_n的朗兰兹对应
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-062 / THM-M-0448 哈里斯-泰勒定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `184`；Stage1 lane: `frontier_deep_formalization_debt`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 局部朗兰兹对应
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-063 / THM-M-0449 海涅曼-洛基塔斯基定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `184`；Stage1 lane: `frontier_deep_formalization_debt`；profile: `arithmetic_geometry_number_theory`
- 定理内容: p-adic群的局部朗兰兹对应
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-064 / THM-M-0446 怀尔斯-泰勒定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `182`；Stage1 lane: `frontier_deep_formalization_debt`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 模性提升
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-065 / THM-M-0447 泰勒-怀尔斯方法

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `182`；Stage1 lane: `frontier_deep_formalization_debt`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 伽罗瓦表示的模性提升
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-066 / THM-M-0437 志田簇

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `181`；Stage1 lane: `frontier_deep_formalization_debt`；profile: `arithmetic_geometry_number_theory`
- 定理内容: Hodge型志田簇的构造
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-067 / THM-M-0423 哈塞原理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `174`；Stage1 lane: `frontier_deep_formalization_debt`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 局部-整体原理
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-068 / THM-M-0413 代数整数环

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 数域的整数环是Dedekind整环
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-069 / THM-M-0414 理想唯一分解定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: Dedekind整环中理想的唯一分解
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-070 / THM-M-0415 理想类群有限性

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 数域的理想类群有限
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-071 / THM-M-0416 狄利克雷单位定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 数域单位群的结构
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-072 / THM-M-0417 闵可夫斯基定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 格点与凸体的关系
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-073 / THM-M-0418 闵可夫斯基界

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 理想类群生成元的界
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-074 / THM-M-0419 克罗内克-韦伯定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 有理数域的有限阿贝尔扩张
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-075 / THM-M-0420 希尔伯特类域

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 数域的最大非分歧阿贝尔扩张
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-076 / THM-M-0421 局部类域论

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 局部域的阿贝尔扩张
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-077 / THM-M-0422 整体类域论

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 数域的阿贝尔扩张
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-078 / THM-M-0424 布饶尔群

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 中心单代数的分类
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-079 / THM-M-0425 赫克L-函数

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 赫克特征的L-函数
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-080 / THM-M-0426 赫克特征标的函数方程

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 赫克L-函数的函数方程
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-081 / THM-M-0427 阿廷L-函数

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 伽罗瓦表示的L-函数
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-082 / THM-M-0429 布饶尔定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 阿廷L-函数的亚纯性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-083 / THM-M-0434 吴宝珠基本引理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 基本引理的证明
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-084 / THM-M-0435 志村曲线

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 四元数代数上的模曲线
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-085 / THM-M-0436 志村提升

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 模形式的提升
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-086 / THM-M-0438 志田周期

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 志田簇上的周期积分
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-087 / THM-M-0441 皮拉-约克定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: o-极小结构中的有理点
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-088 / THM-M-0442 马苏尔定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 椭圆曲线上有理挠点的分类
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-089 / THM-M-0443 马祖尔-泰特定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 椭圆曲线的p-adic L-函数
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-090 / THM-M-0444 科利瓦金欧拉系

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 欧拉系的构造
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-091 / THM-M-0445 鲁宾-科利瓦金定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 椭圆曲线的BSD
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-092 / THM-M-0450 莫德尔-韦伊定理

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 椭圆曲线有理点构成有限生成群
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-093 / THM-M-0451 奈隆-泰特高度

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 代数数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `arithmetic_geometry_number_theory`
- 定理内容: 椭圆曲线上点的高度
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 `NumberTheory`、commutative algebra、field/ring/ideal/class-group API；必要时允许 pinned external Lean 4 dependency。
- Stage1 partial verification scope: 优先 formalize statement、关键 reduction、低维/特殊情形、mathlib 已有 theorem wrapper、以及外部 Lean 4 项目的 pinned dependency wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 局部/整体约化 -> 代数结构层 -> 核心引理族 -> terminal theorem / partial theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 数域、理想类群、局部域、椭圆曲线、L-function 或 Galois representation API 可能不完整；需先识别可 repo-local check 的已完成 branch。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

## 代数学 / 同调代数

### S1-M-094 / THM-M-0007 格罗滕迪克谱序列定理

- Stage1 状态: `[ ] open`
- 来源分类: `代数学 / 同调代数`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `194`；Stage1 lane: `frontier_deep_formalization_debt`；profile: `homological_category_theory`
- 定理内容: 导出函子的复合
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 category theory、abelian category、chain complex、homological algebra API。
- Stage1 partial verification scope: 先做 category-level statement、自然性 square、短正合/长正合子结果、已存在 API 的 wrapper 与 theorem-tree ledger。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 范畴/函子前提 -> exactness / derived object -> naturality square -> spectral/long exact sequence branch -> terminal statement。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: universe、simp-normal-form、自然变换与 exactness API 容易导致证明项复杂；必须保持 theorem names 与 mathlib API 对齐。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-095 / THM-M-0006 导出函子定理

- Stage1 状态: `[ ] open`
- 来源分类: `代数学 / 同调代数`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `160`；Stage1 lane: `frontier_deep_formalization_debt`；profile: `homological_category_theory`
- 定理内容: 左/右导出函子的存在性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 category theory、abelian category、chain complex、homological algebra API。
- Stage1 partial verification scope: 先做 category-level statement、自然性 square、短正合/长正合子结果、已存在 API 的 wrapper 与 theorem-tree ledger。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 范畴/函子前提 -> exactness / derived object -> naturality square -> spectral/long exact sequence branch -> terminal statement。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: universe、simp-normal-form、自然变换与 exactness API 容易导致证明项复杂；必须保持 theorem names 与 mathlib API 对齐。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-096 / THM-M-0001 长正合序列定理

- Stage1 状态: `[ ] open`
- 来源分类: `代数学 / 同调代数`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `150`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `homological_category_theory`
- 定理内容: 短正合列诱导长正合同调序列
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 category theory、abelian category、chain complex、homological algebra API。
- Stage1 partial verification scope: 先做 category-level statement、自然性 square、短正合/长正合子结果、已存在 API 的 wrapper 与 theorem-tree ledger。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 范畴/函子前提 -> exactness / derived object -> naturality square -> spectral/long exact sequence branch -> terminal statement。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: universe、simp-normal-form、自然变换与 exactness API 容易导致证明项复杂；必须保持 theorem names 与 mathlib API 对齐。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-097 / THM-M-0002 五引理

- Stage1 状态: `[ ] open`
- 来源分类: `代数学 / 同调代数`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `150`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `homological_category_theory`
- 定理内容: 交换图中同态的同构性质
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 category theory、abelian category、chain complex、homological algebra API。
- Stage1 partial verification scope: 先做 category-level statement、自然性 square、短正合/长正合子结果、已存在 API 的 wrapper 与 theorem-tree ledger。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 范畴/函子前提 -> exactness / derived object -> naturality square -> spectral/long exact sequence branch -> terminal statement。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: universe、simp-normal-form、自然变换与 exactness API 容易导致证明项复杂；必须保持 theorem names 与 mathlib API 对齐。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-098 / THM-M-0003 蛇引理

- Stage1 状态: `[ ] open`
- 来源分类: `代数学 / 同调代数`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `150`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `homological_category_theory`
- 定理内容: 短正合列诱导的长正合序列
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 category theory、abelian category、chain complex、homological algebra API。
- Stage1 partial verification scope: 先做 category-level statement、自然性 square、短正合/长正合子结果、已存在 API 的 wrapper 与 theorem-tree ledger。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 范畴/函子前提 -> exactness / derived object -> naturality square -> spectral/long exact sequence branch -> terminal statement。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: universe、simp-normal-form、自然变换与 exactness API 容易导致证明项复杂；必须保持 theorem names 与 mathlib API 对齐。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-099 / THM-M-0004 万有系数定理

- Stage1 状态: `[ ] open`
- 来源分类: `代数学 / 同调代数`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `150`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `homological_category_theory`
- 定理内容: 同调群与张量积/同态群的关系
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 category theory、abelian category、chain complex、homological algebra API。
- Stage1 partial verification scope: 先做 category-level statement、自然性 square、短正合/长正合子结果、已存在 API 的 wrapper 与 theorem-tree ledger。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 范畴/函子前提 -> exactness / derived object -> naturality square -> spectral/long exact sequence branch -> terminal statement。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: universe、simp-normal-form、自然变换与 exactness API 容易导致证明项复杂；必须保持 theorem names 与 mathlib API 对齐。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-100 / THM-M-0005 库奈斯公式

- Stage1 状态: `[ ] open`
- 来源分类: `代数学 / 同调代数`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `150`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `homological_category_theory`
- 定理内容: 乘积空间的同调群计算
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 category theory、abelian category、chain complex、homological algebra API。
- Stage1 partial verification scope: 先做 category-level statement、自然性 square、短正合/长正合子结果、已存在 API 的 wrapper 与 theorem-tree ledger。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 范畴/函子前提 -> exactness / derived object -> naturality square -> spectral/long exact sequence branch -> terminal statement。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: universe、simp-normal-form、自然变换与 exactness API 容易导致证明项复杂；必须保持 theorem names 与 mathlib API 对齐。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-101 / THM-M-0008 托雷定理

- Stage1 状态: `[ ] open`
- 来源分类: `代数学 / 同调代数`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `150`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `homological_category_theory`
- 定理内容: Tor函子的性质
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 category theory、abelian category、chain complex、homological algebra API。
- Stage1 partial verification scope: 先做 category-level statement、自然性 square、短正合/长正合子结果、已存在 API 的 wrapper 与 theorem-tree ledger。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 范畴/函子前提 -> exactness / derived object -> naturality square -> spectral/long exact sequence branch -> terminal statement。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: universe、simp-normal-form、自然变换与 exactness API 容易导致证明项复杂；必须保持 theorem names 与 mathlib API 对齐。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-102 / THM-M-0009 Ext长正合序列

- Stage1 状态: `[ ] open`
- 来源分类: `代数学 / 同调代数`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `150`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `homological_category_theory`
- 定理内容: Ext函子的长正合序列
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 category theory、abelian category、chain complex、homological algebra API。
- Stage1 partial verification scope: 先做 category-level statement、自然性 square、短正合/长正合子结果、已存在 API 的 wrapper 与 theorem-tree ledger。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 范畴/函子前提 -> exactness / derived object -> naturality square -> spectral/long exact sequence branch -> terminal statement。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: universe、simp-normal-form、自然变换与 exactness API 容易导致证明项复杂；必须保持 theorem names 与 mathlib API 对齐。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-103 / THM-M-0010 阿廷-里斯引理

- Stage1 状态: `[ ] open`
- 来源分类: `代数学 / 同调代数`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `150`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `homological_category_theory`
- 定理内容: 关于滤过模的性质
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 category theory、abelian category、chain complex、homological algebra API。
- Stage1 partial verification scope: 先做 category-level statement、自然性 square、短正合/长正合子结果、已存在 API 的 wrapper 与 theorem-tree ledger。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 范畴/函子前提 -> exactness / derived object -> naturality square -> spectral/long exact sequence branch -> terminal statement。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: universe、simp-normal-form、自然变换与 exactness API 容易导致证明项复杂；必须保持 theorem names 与 mathlib API 对齐。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-104 / THM-M-0011 平坦下降定理

- Stage1 状态: `[ ] open`
- 来源分类: `代数学 / 同调代数`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `150`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `homological_category_theory`
- 定理内容: 平坦基变换下的下降理论
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 category theory、abelian category、chain complex、homological algebra API。
- Stage1 partial verification scope: 先做 category-level statement、自然性 square、短正合/长正合子结果、已存在 API 的 wrapper 与 theorem-tree ledger。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 范畴/函子前提 -> exactness / derived object -> naturality square -> spectral/long exact sequence branch -> terminal statement。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: universe、simp-normal-form、自然变换与 exactness API 容易导致证明项复杂；必须保持 theorem names 与 mathlib API 对齐。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

## 拓扑学 / 代数拓扑

### S1-M-105 / THM-M-0545 霍奇分解定理

- Stage1 状态: `[ ] open`
- 来源分类: `拓扑学 / 代数拓扑`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `182`；Stage1 lane: `frontier_deep_formalization_debt`；profile: `topology_algebraic_differential`
- 定理内容: 微分形式的Hodge分解
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 topology、homotopy-adjacent API、manifold、homology/cohomology 相关结构。
- Stage1 partial verification scope: 先验证空间/流形对象、基本不变量、functoriality、低维/简单空间特例、已存在 mathlib theorem wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 空间/流形前提 -> 不变量定义 -> functoriality/naturality -> exact sequence / obstruction branch -> 主定理。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 同伦、谱序列、transversality、cobordism 等基础设施可能缺失；需优先做可检查的不变量与特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-106 / THM-M-0554 阿蒂亚-希策布鲁赫谱序列

- Stage1 状态: `[ ] open`
- 来源分类: `拓扑学 / 代数拓扑`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `175`；Stage1 lane: `frontier_deep_formalization_debt`；profile: `topology_algebraic_differential`
- 定理内容: 广义上同调论的谱序列
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 topology、homotopy-adjacent API、manifold、homology/cohomology 相关结构。
- Stage1 partial verification scope: 先验证空间/流形对象、基本不变量、functoriality、低维/简单空间特例、已存在 mathlib theorem wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 空间/流形前提 -> 不变量定义 -> functoriality/naturality -> exact sequence / obstruction branch -> 主定理。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 同伦、谱序列、transversality、cobordism 等基础设施可能缺失；需优先做可检查的不变量与特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-107 / THM-M-0546 庞加莱对偶

- Stage1 状态: `[ ] open`
- 来源分类: `拓扑学 / 代数拓扑`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `160`；Stage1 lane: `frontier_deep_formalization_debt`；profile: `topology_algebraic_differential`
- 定理内容: 流形的同调对偶
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 topology、homotopy-adjacent API、manifold、homology/cohomology 相关结构。
- Stage1 partial verification scope: 先验证空间/流形对象、基本不变量、functoriality、低维/简单空间特例、已存在 mathlib theorem wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 空间/流形前提 -> 不变量定义 -> functoriality/naturality -> exact sequence / obstruction branch -> 主定理。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 同伦、谱序列、transversality、cobordism 等基础设施可能缺失；需优先做可检查的不变量与特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-108 / THM-M-0576 阿蒂亚-博特不动点定理

- Stage1 状态: `[ ] open`
- 来源分类: `拓扑学 / 代数拓扑`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `159`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `topology_algebraic_differential`
- 定理内容: 等变椭圆算子的不动点公式
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 topology、homotopy-adjacent API、manifold、homology/cohomology 相关结构。
- Stage1 partial verification scope: 先验证空间/流形对象、基本不变量、functoriality、低维/简单空间特例、已存在 mathlib theorem wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 空间/流形前提 -> 不变量定义 -> functoriality/naturality -> exact sequence / obstruction branch -> 主定理。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 同伦、谱序列、transversality、cobordism 等基础设施可能缺失；需优先做可检查的不变量与特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-109 / THM-M-0544 霍奇理论

- Stage1 状态: `[ ] open`
- 来源分类: `拓扑学 / 代数拓扑`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `157`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `topology_algebraic_differential`
- 定理内容: 调和形式与上同调
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 topology、homotopy-adjacent API、manifold、homology/cohomology 相关结构。
- Stage1 partial verification scope: 先验证空间/流形对象、基本不变量、functoriality、低维/简单空间特例、已存在 mathlib theorem wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 空间/流形前提 -> 不变量定义 -> functoriality/naturality -> exact sequence / obstruction branch -> 主定理。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 同伦、谱序列、transversality、cobordism 等基础设施可能缺失；需优先做可检查的不变量与特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-110 / THM-M-0553 亚当斯谱序列

- Stage1 状态: `[ ] open`
- 来源分类: `拓扑学 / 代数拓扑`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `topology_algebraic_differential`
- 定理内容: 稳定同伦群的计算
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 topology、homotopy-adjacent API、manifold、homology/cohomology 相关结构。
- Stage1 partial verification scope: 先验证空间/流形对象、基本不变量、functoriality、低维/简单空间特例、已存在 mathlib theorem wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 空间/流形前提 -> 不变量定义 -> functoriality/naturality -> exact sequence / obstruction branch -> 主定理。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 同伦、谱序列、transversality、cobordism 等基础设施可能缺失；需优先做可检查的不变量与特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-111 / THM-M-0555 塞尔谱序列

- Stage1 状态: `[ ] open`
- 来源分类: `拓扑学 / 代数拓扑`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `topology_algebraic_differential`
- 定理内容: 纤维化的同调谱序列
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 topology、homotopy-adjacent API、manifold、homology/cohomology 相关结构。
- Stage1 partial verification scope: 先验证空间/流形对象、基本不变量、functoriality、低维/简单空间特例、已存在 mathlib theorem wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 空间/流形前提 -> 不变量定义 -> functoriality/naturality -> exact sequence / obstruction branch -> 主定理。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 同伦、谱序列、transversality、cobordism 等基础设施可能缺失；需优先做可检查的不变量与特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-112 / THM-M-0556 勒雷-塞尔谱序列

- Stage1 状态: `[ ] open`
- 来源分类: `拓扑学 / 代数拓扑`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `topology_algebraic_differential`
- 定理内容: 纤维化的谱序列
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 topology、homotopy-adjacent API、manifold、homology/cohomology 相关结构。
- Stage1 partial verification scope: 先验证空间/流形对象、基本不变量、functoriality、低维/简单空间特例、已存在 mathlib theorem wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 空间/流形前提 -> 不变量定义 -> functoriality/naturality -> exact sequence / obstruction branch -> 主定理。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 同伦、谱序列、transversality、cobordism 等基础设施可能缺失；需优先做可检查的不变量与特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-113 / THM-M-0570 指标定理的热核证明

- Stage1 状态: `[ ] open`
- 来源分类: `拓扑学 / 代数拓扑`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `153`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `topology_algebraic_differential`
- 定理内容: 阿蒂亚-辛格定理的热核方法
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 topology、homotopy-adjacent API、manifold、homology/cohomology 相关结构。
- Stage1 partial verification scope: 先验证空间/流形对象、基本不变量、functoriality、低维/简单空间特例、已存在 mathlib theorem wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 空间/流形前提 -> 不变量定义 -> functoriality/naturality -> exact sequence / obstruction branch -> 主定理。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 同伦、谱序列、transversality、cobordism 等基础设施可能缺失；需优先做可检查的不变量与特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-114 / THM-M-0579 庞加莱猜想

- Stage1 状态: `[ ] open`
- 来源分类: `拓扑学 / 代数拓扑`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `topology_algebraic_differential`
- 定理内容: 单连通闭三维流形同胚于球面
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 topology、homotopy-adjacent API、manifold、homology/cohomology 相关结构。
- Stage1 partial verification scope: 先验证空间/流形对象、基本不变量、functoriality、低维/简单空间特例、已存在 mathlib theorem wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 空间/流形前提 -> 不变量定义 -> functoriality/naturality -> exact sequence / obstruction branch -> 主定理。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 同伦、谱序列、transversality、cobordism 等基础设施可能缺失；需优先做可检查的不变量与特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-115 / THM-M-0580 佩雷尔曼定理

- Stage1 状态: `[ ] open`
- 来源分类: `拓扑学 / 代数拓扑`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `topology_algebraic_differential`
- 定理内容: 庞加莱猜想的证明
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 topology、homotopy-adjacent API、manifold、homology/cohomology 相关结构。
- Stage1 partial verification scope: 先验证空间/流形对象、基本不变量、functoriality、低维/简单空间特例、已存在 mathlib theorem wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 空间/流形前提 -> 不变量定义 -> functoriality/naturality -> exact sequence / obstruction branch -> 主定理。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 同伦、谱序列、transversality、cobordism 等基础设施可能缺失；需优先做可检查的不变量与特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-116 / THM-M-0583 四维庞加莱猜想

- Stage1 状态: `[ ] open`
- 来源分类: `拓扑学 / 代数拓扑`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `topology_algebraic_differential`
- 定理内容: 四维拓扑庞加莱猜想
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 topology、homotopy-adjacent API、manifold、homology/cohomology 相关结构。
- Stage1 partial verification scope: 先验证空间/流形对象、基本不变量、functoriality、低维/简单空间特例、已存在 mathlib theorem wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 空间/流形前提 -> 不变量定义 -> functoriality/naturality -> exact sequence / obstruction branch -> 主定理。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 同伦、谱序列、transversality、cobordism 等基础设施可能缺失；需优先做可检查的不变量与特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-117 / THM-M-0586 高维庞加莱猜想

- Stage1 状态: `[ ] open`
- 来源分类: `拓扑学 / 代数拓扑`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `topology_algebraic_differential`
- 定理内容: n≥5维庞加莱猜想
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 topology、homotopy-adjacent API、manifold、homology/cohomology 相关结构。
- Stage1 partial verification scope: 先验证空间/流形对象、基本不变量、functoriality、低维/简单空间特例、已存在 mathlib theorem wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 空间/流形前提 -> 不变量定义 -> functoriality/naturality -> exact sequence / obstruction branch -> 主定理。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 同伦、谱序列、transversality、cobordism 等基础设施可能缺失；需优先做可检查的不变量与特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-118 / THM-M-0571 局部指标定理

- Stage1 状态: `[ ] open`
- 来源分类: `拓扑学 / 代数拓扑`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `144`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `topology_algebraic_differential`
- 定理内容: 指标密度的局部公式
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 topology、homotopy-adjacent API、manifold、homology/cohomology 相关结构。
- Stage1 partial verification scope: 先验证空间/流形对象、基本不变量、functoriality、低维/简单空间特例、已存在 mathlib theorem wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 空间/流形前提 -> 不变量定义 -> functoriality/naturality -> exact sequence / obstruction branch -> 主定理。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 同伦、谱序列、transversality、cobordism 等基础设施可能缺失；需优先做可检查的不变量与特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-119 / THM-M-0547 莱夫谢茨对偶

- Stage1 状态: `[ ] open`
- 来源分类: `拓扑学 / 代数拓扑`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `140`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `topology_algebraic_differential`
- 定理内容: 带边流形的对偶定理
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 topology、homotopy-adjacent API、manifold、homology/cohomology 相关结构。
- Stage1 partial verification scope: 先验证空间/流形对象、基本不变量、functoriality、低维/简单空间特例、已存在 mathlib theorem wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 空间/流形前提 -> 不变量定义 -> functoriality/naturality -> exact sequence / obstruction branch -> 主定理。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 同伦、谱序列、transversality、cobordism 等基础设施可能缺失；需优先做可检查的不变量与特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-120 / THM-M-0548 亚历山大对偶

- Stage1 状态: `[ ] open`
- 来源分类: `拓扑学 / 代数拓扑`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `140`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `topology_algebraic_differential`
- 定理内容: 球面中子空间的对偶
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 topology、homotopy-adjacent API、manifold、homology/cohomology 相关结构。
- Stage1 partial verification scope: 先验证空间/流形对象、基本不变量、functoriality、低维/简单空间特例、已存在 mathlib theorem wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 空间/流形前提 -> 不变量定义 -> functoriality/naturality -> exact sequence / obstruction branch -> 主定理。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 同伦、谱序列、transversality、cobordism 等基础设施可能缺失；需优先做可检查的不变量与特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

## 几何学 / 微分几何

### S1-M-121 / THM-M-0177 格罗滕迪克-黎曼-罗赫定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 微分几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `176`；Stage1 lane: `frontier_deep_formalization_debt`；profile: `differential_geometry`
- 定理内容: 态射的黎曼-罗赫定理
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 manifold、smooth map、tensor/calculus、topology、analysis API。
- Stage1 partial verification scope: 先验证 statement、局部坐标 lemma、基础曲率/张量恒等式、低维或紧流形特殊情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 流形/丛/联络定义 -> 曲率或张量恒等式 -> 局部坐标 branch -> 全局化/compactness -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 坐标计算、smoothness automation、tensor notation 和 global/local bridge 是主要 formalization_debt。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-122 / THM-M-0166 霍普夫-里诺定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 微分几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `164`；Stage1 lane: `frontier_deep_formalization_debt`；profile: `differential_geometry`
- 定理内容: 完备黎曼流形的测地线存在性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 manifold、smooth map、tensor/calculus、topology、analysis API。
- Stage1 partial verification scope: 先验证 statement、局部坐标 lemma、基础曲率/张量恒等式、低维或紧流形特殊情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 流形/丛/联络定义 -> 曲率或张量恒等式 -> 局部坐标 branch -> 全局化/compactness -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 坐标计算、smoothness automation、tensor notation 和 global/local bridge 是主要 formalization_debt。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-123 / THM-M-0170 纳什嵌入定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 微分几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `161`；Stage1 lane: `frontier_deep_formalization_debt`；profile: `differential_geometry`
- 定理内容: 黎曼流形可等距嵌入欧氏空间
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 manifold、smooth map、tensor/calculus、topology、analysis API。
- Stage1 partial verification scope: 先验证 statement、局部坐标 lemma、基础曲率/张量恒等式、低维或紧流形特殊情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 流形/丛/联络定义 -> 曲率或张量恒等式 -> 局部坐标 branch -> 全局化/compactness -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 坐标计算、smoothness automation、tensor notation 和 global/local bridge 是主要 formalization_debt。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-124 / THM-M-0175 黎曼-罗赫定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 微分几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `differential_geometry`
- 定理内容: 代数曲线上的除子维数公式
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 manifold、smooth map、tensor/calculus、topology、analysis API。
- Stage1 partial verification scope: 先验证 statement、局部坐标 lemma、基础曲率/张量恒等式、低维或紧流形特殊情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 流形/丛/联络定义 -> 曲率或张量恒等式 -> 局部坐标 branch -> 全局化/compactness -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 坐标计算、smoothness automation、tensor notation 和 global/local bridge 是主要 formalization_debt。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-125 / THM-M-0176 希策布鲁赫-黎曼-罗赫定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 微分几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `154`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `differential_geometry`
- 定理内容: 高维代数簇的黎曼-罗赫定理
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 manifold、smooth map、tensor/calculus、topology、analysis API。
- Stage1 partial verification scope: 先验证 statement、局部坐标 lemma、基础曲率/张量恒等式、低维或紧流形特殊情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 流形/丛/联络定义 -> 曲率或张量恒等式 -> 局部坐标 branch -> 全局化/compactness -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 坐标计算、smoothness automation、tensor notation 和 global/local bridge 是主要 formalization_debt。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-126 / THM-M-0165 莫尔斯指数定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 微分几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `151`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `differential_geometry`
- 定理内容: 测地线变分的临界点指标
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 manifold、smooth map、tensor/calculus、topology、analysis API。
- Stage1 partial verification scope: 先验证 statement、局部坐标 lemma、基础曲率/张量恒等式、低维或紧流形特殊情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 流形/丛/联络定义 -> 曲率或张量恒等式 -> 局部坐标 branch -> 全局化/compactness -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 坐标计算、smoothness automation、tensor notation 和 global/local bridge 是主要 formalization_debt。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-127 / THM-M-0173 阿蒂亚-辛格指标定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 微分几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `151`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `differential_geometry`
- 定理内容: 椭圆算子的解析指标与拓扑指标相等
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 manifold、smooth map、tensor/calculus、topology、analysis API。
- Stage1 partial verification scope: 先验证 statement、局部坐标 lemma、基础曲率/张量恒等式、低维或紧流形特殊情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 流形/丛/联络定义 -> 曲率或张量恒等式 -> 局部坐标 branch -> 全局化/compactness -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 坐标计算、smoothness automation、tensor notation 和 global/local bridge 是主要 formalization_debt。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-128 / THM-M-0182 佩雷尔曼定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 微分几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `150`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `differential_geometry`
- 定理内容: 庞加莱猜想与几何化猜想的证明
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 manifold、smooth map、tensor/calculus、topology、analysis API。
- Stage1 partial verification scope: 先验证 statement、局部坐标 lemma、基础曲率/张量恒等式、低维或紧流形特殊情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 流形/丛/联络定义 -> 曲率或张量恒等式 -> 局部坐标 branch -> 全局化/compactness -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 坐标计算、smoothness automation、tensor notation 和 global/local bridge 是主要 formalization_debt。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-129 / THM-M-0181 汉密尔顿里奇流定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 微分几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `140`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `differential_geometry`
- 定理内容: 里奇流的短期存在性与唯一性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 manifold、smooth map、tensor/calculus、topology、analysis API。
- Stage1 partial verification scope: 先验证 statement、局部坐标 lemma、基础曲率/张量恒等式、低维或紧流形特殊情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 流形/丛/联络定义 -> 曲率或张量恒等式 -> 局部坐标 branch -> 全局化/compactness -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 坐标计算、smoothness automation、tensor notation 和 global/local bridge 是主要 formalization_debt。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-130 / THM-M-0183 丘成桐卡拉比猜想

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 微分几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `140`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `differential_geometry`
- 定理内容: 紧Kähler流形上Ricci平坦度量的存在性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 manifold、smooth map、tensor/calculus、topology、analysis API。
- Stage1 partial verification scope: 先验证 statement、局部坐标 lemma、基础曲率/张量恒等式、低维或紧流形特殊情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 流形/丛/联络定义 -> 曲率或张量恒等式 -> 局部坐标 branch -> 全局化/compactness -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 坐标计算、smoothness automation、tensor notation 和 global/local bridge 是主要 formalization_debt。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-131 / THM-M-0184 唐纳森定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 微分几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `differential_geometry`
- 定理内容: 四维流形上反自对偶联络的模空间
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 manifold、smooth map、tensor/calculus、topology、analysis API。
- Stage1 partial verification scope: 先验证 statement、局部坐标 lemma、基础曲率/张量恒等式、低维或紧流形特殊情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 流形/丛/联络定义 -> 曲率或张量恒等式 -> 局部坐标 branch -> 全局化/compactness -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 坐标计算、smoothness automation、tensor notation 和 global/local bridge 是主要 formalization_debt。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-132 / THM-M-0171 格罗莫夫嵌入定理

- Stage1 状态: `[ ] open`
- 来源分类: `几何学 / 微分几何`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `137`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `differential_geometry`
- 定理内容: 度量空间嵌入的充要条件
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 manifold、smooth map、tensor/calculus、topology、analysis API。
- Stage1 partial verification scope: 先验证 statement、局部坐标 lemma、基础曲率/张量恒等式、低维或紧流形特殊情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 流形/丛/联络定义 -> 曲率或张量恒等式 -> 局部坐标 branch -> 全局化/compactness -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 坐标计算、smoothness automation、tensor notation 和 global/local bridge 是主要 formalization_debt。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

## 代数学 / 范畴论

### S1-M-133 / THM-M-0087 加布里埃尔-波珀斯库定理

- Stage1 状态: `[ ] open`
- 来源分类: `代数学 / 范畴论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `172`；Stage1 lane: `frontier_deep_formalization_debt`；profile: `homological_category_theory`
- 定理内容: Grothendieck范畴的刻画
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 category theory、abelian category、chain complex、homological algebra API。
- Stage1 partial verification scope: 先做 category-level statement、自然性 square、短正合/长正合子结果、已存在 API 的 wrapper 与 theorem-tree ledger。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 范畴/函子前提 -> exactness / derived object -> naturality square -> spectral/long exact sequence branch -> terminal statement。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: universe、simp-normal-form、自然变换与 exactness API 容易导致证明项复杂；必须保持 theorem names 与 mathlib API 对齐。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-134 / THM-M-0086 弗雷德定理

- Stage1 状态: `[ ] open`
- 来源分类: `代数学 / 范畴论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `167`；Stage1 lane: `frontier_deep_formalization_debt`；profile: `homological_category_theory`
- 定理内容: 嵌入定理与生成元存在性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 category theory、abelian category、chain complex、homological algebra API。
- Stage1 partial verification scope: 先做 category-level statement、自然性 square、短正合/长正合子结果、已存在 API 的 wrapper 与 theorem-tree ledger。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 范畴/函子前提 -> exactness / derived object -> naturality square -> spectral/long exact sequence branch -> terminal statement。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: universe、simp-normal-form、自然变换与 exactness API 容易导致证明项复杂；必须保持 theorem names 与 mathlib API 对齐。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-135 / THM-M-0082 伴随函子定理

- Stage1 状态: `[ ] open`
- 来源分类: `代数学 / 范畴论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `160`；Stage1 lane: `frontier_deep_formalization_debt`；profile: `homological_category_theory`
- 定理内容: 伴随函子的存在性条件
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 category theory、abelian category、chain complex、homological algebra API。
- Stage1 partial verification scope: 先做 category-level statement、自然性 square、短正合/长正合子结果、已存在 API 的 wrapper 与 theorem-tree ledger。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 范畴/函子前提 -> exactness / derived object -> naturality square -> spectral/long exact sequence branch -> terminal statement。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: universe、simp-normal-form、自然变换与 exactness API 容易导致证明项复杂；必须保持 theorem names 与 mathlib API 对齐。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-136 / THM-M-0084 极限与余极限定理

- Stage1 状态: `[ ] open`
- 来源分类: `代数学 / 范畴论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `160`；Stage1 lane: `frontier_deep_formalization_debt`；profile: `homological_category_theory`
- 定理内容: 范畴中极限的存在性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 category theory、abelian category、chain complex、homological algebra API。
- Stage1 partial verification scope: 先做 category-level statement、自然性 square、短正合/长正合子结果、已存在 API 的 wrapper 与 theorem-tree ledger。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 范畴/函子前提 -> exactness / derived object -> naturality square -> spectral/long exact sequence branch -> terminal statement。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: universe、simp-normal-form、自然变换与 exactness API 容易导致证明项复杂；必须保持 theorem names 与 mathlib API 对齐。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-137 / THM-M-0088 米田嵌入

- Stage1 状态: `[ ] open`
- 来源分类: `代数学 / 范畴论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `157`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `homological_category_theory`
- 定理内容: 范畴可嵌入其预层范畴
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 category theory、abelian category、chain complex、homological algebra API。
- Stage1 partial verification scope: 先做 category-level statement、自然性 square、短正合/长正合子结果、已存在 API 的 wrapper 与 theorem-tree ledger。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 范畴/函子前提 -> exactness / derived object -> naturality square -> spectral/long exact sequence branch -> terminal statement。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: universe、simp-normal-form、自然变换与 exactness API 容易导致证明项复杂；必须保持 theorem names 与 mathlib API 对齐。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-138 / THM-M-0081 米田引理

- Stage1 状态: `[ ] open`
- 来源分类: `代数学 / 范畴论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `150`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `homological_category_theory`
- 定理内容: 对象由其表示函子唯一确定
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 category theory、abelian category、chain complex、homological algebra API。
- Stage1 partial verification scope: 先做 category-level statement、自然性 square、短正合/长正合子结果、已存在 API 的 wrapper 与 theorem-tree ledger。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 范畴/函子前提 -> exactness / derived object -> naturality square -> spectral/long exact sequence branch -> terminal statement。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: universe、simp-normal-form、自然变换与 exactness API 容易导致证明项复杂；必须保持 theorem names 与 mathlib API 对齐。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-139 / THM-M-0083 可表函子定理

- Stage1 状态: `[ ] open`
- 来源分类: `代数学 / 范畴论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `150`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `homological_category_theory`
- 定理内容: 函子可表的条件
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 category theory、abelian category、chain complex、homological algebra API。
- Stage1 partial verification scope: 先做 category-level statement、自然性 square、短正合/长正合子结果、已存在 API 的 wrapper 与 theorem-tree ledger。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 范畴/函子前提 -> exactness / derived object -> naturality square -> spectral/long exact sequence branch -> terminal statement。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: universe、simp-normal-form、自然变换与 exactness API 容易导致证明项复杂；必须保持 theorem names 与 mathlib API 对齐。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-140 / THM-M-0085 贝克单子性定理

- Stage1 状态: `[ ] open`
- 来源分类: `代数学 / 范畴论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `150`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `homological_category_theory`
- 定理内容: 单子与伴随的等价
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 category theory、abelian category、chain complex、homological algebra API。
- Stage1 partial verification scope: 先做 category-level statement、自然性 square、短正合/长正合子结果、已存在 API 的 wrapper 与 theorem-tree ledger。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 范畴/函子前提 -> exactness / derived object -> naturality square -> spectral/long exact sequence branch -> terminal statement。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: universe、simp-normal-form、自然变换与 exactness API 容易导致证明项复杂；必须保持 theorem names 与 mathlib API 对齐。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

## 微分方程 / 偏微分方程

### S1-M-141 / THM-M-1315 Riemannian Penrose不等式

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `166`；Stage1 lane: `frontier_deep_formalization_debt`；profile: `partial_differential_equations`
- 定理内容: Huisken-Ilmanen/Bray的证明
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-142 / THM-M-1314 Penrose不等式

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `部分证明`；Stage0 bucket: `partial`
- 难度分: `159`；Stage1 lane: `known_partial_branch_deepening`；profile: `partial_differential_equations`
- 定理内容: 黑洞质量的上下界
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 允许存在 `formalization_debt` 或局部分支数学债；若发现外部 Lean 4 机器证明，必须立即 pin/import/check，不能留下 `repo_local_integration_debt`。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-143 / THM-M-1153 Wiener准则

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: 边界点的正则性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-144 / THM-M-1154 正则边界点

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: Dirichlet问题解的存在性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-145 / THM-M-1168 内部估计

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: 解在内部的正则性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-146 / THM-M-1169 边界估计

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: 解在边界的正则性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-147 / THM-M-1172 W^{2,p}正则性

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: 解的二阶导数的L^p可积性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-148 / THM-M-1180 Caffarelli正则性理论

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: Monge-Ampère方程的正则性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-149 / THM-M-1181 Caffarelli定理

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: 凸解的内部正则性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-150 / THM-M-1182 Caffarelli边界正则性

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: 严格凸区域的边界正则性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-151 / THM-M-1186 McCann定理

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: 最优传输的存在性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-152 / THM-M-1189 热方程的Schauder估计

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: 抛物型方程的正则性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-153 / THM-M-1214 Cazenave-Weissler定理

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: NLS的临界正则性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-154 / THM-M-1216 Kenig-Ponce-Vega定理

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: 色散方程的低正则性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-155 / THM-M-1224 Grillakis定理

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: NLW的正则性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-156 / THM-M-1228 Caffarelli-Kohn-Nirenberg定理

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: 弱解的部分正则性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-157 / THM-M-1229 Serrin准则

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: 弱解的正则性条件
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-158 / THM-M-1234 Yudovich定理

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: 二维Euler方程的整体存在性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-159 / THM-M-1235 Wolibner定理

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: 二维Euler方程的整体存在性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-160 / THM-M-1255 Malgrange-Ehrenpreis定理

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: 常系数PDE基本解的存在性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-161 / THM-M-1259 Hörmander定理(次椭圆)

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: 次椭圆算子的正则性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-162 / THM-M-1266 Tonelli定理

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: 变分问题的存在性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-163 / THM-M-1270 Ekeland变分原理

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: 近似极小点的存在性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-164 / THM-M-1271 山路引理

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: 临界点存在性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-165 / THM-M-1272 喷泉定理

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: 多临界点的存在性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-166 / THM-M-1307 Klainerman定理

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: 零条件与整体存在性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-167 / THM-M-1311 Choquet-Bruhat定理

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: Einstein方程的局部存在性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-168 / THM-M-1312 Choquet-Bruhat-Geroch定理

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `152`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: Einstein方程的整体存在性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-169 / THM-M-1184 Kantorovich对偶

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `150`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: 最优传输的对偶问题
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-170 / THM-M-1205 compensated 紧性

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `150`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: 守恒律方程的紧性方法
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-171 / THM-M-1251 缓增分布

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `150`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: Schwartz空间的对偶
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-172 / THM-M-1292 Struwe紧性引理

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `150`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: Palais-Smale条件的替代
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-173 / THM-M-1293 Lions集中紧性原理

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `150`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: 临界增长问题的紧性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-174 / THM-M-1294 全局紧性

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `150`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: 非紧问题的紧化
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-175 / THM-M-1237 Sobolev嵌入定理

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `149`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: Sobolev空间到连续函数空间的嵌入
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-176 / THM-M-1238 Rellich-Kondrachov定理

- Stage1 状态: `[ ] open`
- 来源分类: `微分方程 / 偏微分方程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `149`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `partial_differential_equations`
- 定理内容: Sobolev空间的紧嵌入
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、normed spaces、measure/integration、weak derivative 或 distribution-adjacent definitions。
- Stage1 partial verification scope: 优先验证精确定义、弱形式陈述、基础估计、ODE/有限维近似、已在 analysis API 中可表达的 compactness/continuity 子引理。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 函数空间与边界条件 -> weak/classical formulation bridge -> energy estimate / compactness -> regularity / existence branch -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: PDE 基础设施在 Lean 4 中通常是 formalization_debt；必须把可验证范围限制到 statement、functional-analytic lemma、energy estimate 或特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

## 其他重要领域 / 数学物理

### S1-M-177 / THM-M-1535 AdS/CFT对偶

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `部分验证`；Stage0 bucket: `partial`
- 难度分: `161`；Stage1 lane: `known_partial_branch_deepening`；profile: `mathematical_physics`
- 定理内容: 引力与量子场论的对偶
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 允许存在 `formalization_debt` 或局部分支数学债；若发现外部 Lean 4 机器证明，必须立即 pin/import/check，不能留下 `repo_local_integration_debt`。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-178 / THM-M-1559 Riemann-Hilbert问题

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `160`；Stage1 lane: `frontier_deep_formalization_debt`；profile: `mathematical_physics`
- 定理内容: 可积系统的解析问题
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-179 / THM-M-1543 Atiyah-Ward对应

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `157`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 瞬子与代数几何
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-180 / THM-M-1521 庞加莱回归定理

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `156`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 有界系统的回归性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-181 / THM-M-1536 全息原理

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `部分验证`；Stage0 bucket: `partial`
- 难度分: `153`；Stage1 lane: `known_partial_branch_deepening`；profile: `mathematical_physics`
- 定理内容: 量子引力与边界理论
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 允许存在 `formalization_debt` 或局部分支数学债；若发现外部 Lean 4 机器证明，必须立即 pin/import/check，不能留下 `repo_local_integration_debt`。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-182 / THM-M-1566 Gubinelli-Imkeller-Perkowski理论

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `146`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 抛物型SPDE的正则性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-183 / THM-M-1542 Ward对应

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `144`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 扭量与自对偶Yang-Mills
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-184 / THM-M-1515 诺特定理

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 对称性与守恒量的对应
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-185 / THM-M-1516 哈密顿力学

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 经典力学的哈密顿形式
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-186 / THM-M-1517 拉格朗日力学

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 经典力学的拉格朗日形式
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-187 / THM-M-1518 最小作用量原理

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 物理系统的变分原理
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-188 / THM-M-1519 泊松括号

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 经典力学的代数结构
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-189 / THM-M-1520 刘维尔定理

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 相空间体积守恒
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-190 / THM-M-1522 遍历理论

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 时间平均等于空间平均
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-191 / THM-M-1523 量子力学的数学基础

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 希尔伯特空间形式
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-192 / THM-M-1524 海森堡不确定性原理

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 共轭变量的不确定性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-193 / THM-M-1525 薛定谔方程

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 量子力学的基本方程
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-194 / THM-M-1526 狄拉克方程

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 相对论性量子力学
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-195 / THM-M-1527 麦克斯韦方程组

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 电磁学的基本方程
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-196 / THM-M-1528 爱因斯坦场方程

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 广义相对论的基本方程
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-197 / THM-M-1529 杨-米尔斯理论

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 非阿贝尔规范场论
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-198 / THM-M-1531 Higgs机制

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 规范对称性自发破缺
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-199 / THM-M-1532 标准模型

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 粒子物理的标准模型
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-200 / THM-M-1537 黑洞熵

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 黑洞的热力学熵
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-201 / THM-M-1540 彭罗斯扭量理论

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 时空的扭量描述
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-202 / THM-M-1541 twistor 理论

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 复几何与物理
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-203 / THM-M-1544 ADHM构造

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 瞬子的代数几何构造
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-204 / THM-M-1545 Nahm 变换

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 单极子的构造
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-205 / THM-M-1546 Hitchin 系统

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 代数可积系统
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-206 / THM-M-1547 可积系统

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 完全可积的哈密顿系统
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-207 / THM-M-1548 Korteweg-de Vries方程

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 非线性波动方程
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-208 / THM-M-1549 逆散射变换

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: KdV方程的解法
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-209 / THM-M-1550 Lax对

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 可积系统的表示
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-210 / THM-M-1551 零曲率表示

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 可积系统的规范理论
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-211 / THM-M-1552 tau函数

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 可积系统的tau函数
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-212 / THM-M-1553 Hirota双线性方法

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 数学物理`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `136`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `mathematical_physics`
- 定理内容: 可积系统的双线性方法
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 analysis、linear operators、Hilbert spaces、measure theory、PDE/geometry 接口。
- Stage1 partial verification scope: 先验证公理化 statement、算子/空间定义、谱或变分子引理、特殊参数情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 公理化模型 -> 函数空间/算子前提 -> 谱/能量/变分结构 -> 关键估计 -> theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 必须把物理语言重写成数学命题；非公理化实验事实不进入 proof slot。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

## 分析学 / 泛函分析

### S1-M-213 / THM-M-0328 格罗滕迪克对偶性

- Stage1 状态: `[ ] open`
- 来源分类: `分析学 / 泛函分析`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `150`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `functional_harmonic_analysis`
- 定理内容: 核空间的拓扑张量积
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 normed spaces、measure/integration、topology、operator theory API。
- Stage1 partial verification scope: 先验证 normed-space statement、bounded linear map lemma、积分/极限交换条件、特殊空间情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 空间/算子前提 -> boundedness/compactness -> convergence/duality -> main estimate / representation theorem。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: Bochner/Pettis integral、distribution、Fourier analysis、operator spectrum 等 API 可能不完整。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-214 / THM-M-0325 格罗滕迪克不等式

- Stage1 状态: `[ ] open`
- 来源分类: `分析学 / 泛函分析`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `142`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `functional_harmonic_analysis`
- 定理内容: 张量积的范数不等式
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 normed spaces、measure/integration、topology、operator theory API。
- Stage1 partial verification scope: 先验证 normed-space statement、bounded linear map lemma、积分/极限交换条件、特殊空间情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 空间/算子前提 -> boundedness/compactness -> convergence/duality -> main estimate / representation theorem。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: Bochner/Pettis integral、distribution、Fourier analysis、operator spectrum 等 API 可能不完整。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-215 / THM-M-0326 格罗滕迪克定理

- Stage1 状态: `[ ] open`
- 来源分类: `分析学 / 泛函分析`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `142`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `functional_harmonic_analysis`
- 定理内容: 核空间与逼近性质
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 normed spaces、measure/integration、topology、operator theory API。
- Stage1 partial verification scope: 先验证 normed-space statement、bounded linear map lemma、积分/极限交换条件、特殊空间情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 空间/算子前提 -> boundedness/compactness -> convergence/duality -> main estimate / representation theorem。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: Bochner/Pettis integral、distribution、Fourier analysis、operator spectrum 等 API 可能不完整。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

## 概率论与随机过程 / 随机过程

### S1-M-216 / THM-M-1092 Kolmogorov前向/后向方程

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `150`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 转移密度的微分方程
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-217 / THM-M-1093 Fokker-Planck方程

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `150`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 概率密度的演化方程
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-218 / THM-M-1027 维纳过程的存在性

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `148`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 布朗运动的数学构造
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-219 / THM-M-1052 Krylov-Bogolyubov定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `148`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 不变测度的存在性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-220 / THM-M-1064 Skorokhod嵌入

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `145`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 随机游走的嵌入
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-221 / THM-M-1028 维纳过程的性质

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 布朗运动的连续性与不可微性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-222 / THM-M-1029 Lévy鞅刻画

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 布朗运动的鞅刻画
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-223 / THM-M-1030 Dubins-Schwarz定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 连续局部鞅的时间变换
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-224 / THM-M-1031 鞅表示定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 布朗鞅的随机积分表示
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-225 / THM-M-1032 伊藤公式

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 随机过程的链式法则
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-226 / THM-M-1033 伊藤等距

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 随机积分的等距性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-227 / THM-M-1034 随机积分的定义

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 伊藤积分的构造
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-228 / THM-M-1035 Stratonovich积分

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 另一种随机积分定义
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-229 / THM-M-1036 随机微分方程的存在唯一性

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: SDE的解的存在唯一性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-230 / THM-M-1037 强解与弱解

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: SDE解的不同概念
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-231 / THM-M-1038 Yamada-Watanabe定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: SDE强解的唯一性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-232 / THM-M-1039 随机微分方程的马尔可夫性

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: SDE解的马尔可夫性质
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-233 / THM-M-1040 Feller过程

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: Feller半群与马尔可夫过程
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-234 / THM-M-1041 Hille-Yosida定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 生成元的刻画
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-235 / THM-M-1042 Dynkin公式

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 马尔可夫过程的生成元
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-236 / THM-M-1043 Feynman-Kac公式

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 偏微分方程的概率表示
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-237 / THM-M-1044 Girsanov定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 测度变换与鞅
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-238 / THM-M-1045 Cameron-Martin定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: Wiener空间的平移
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-239 / THM-M-1046 Novikov条件

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 指数鞅的鞅性条件
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-240 / THM-M-1047 Kazamaki条件

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 指数鞅的鞅性条件
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-241 / THM-M-1048 鞅问题

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 马尔可夫过程的鞅刻画
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-242 / THM-M-1049 Stroock-Varadhan鞅问题

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 扩散过程的鞅刻画
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-243 / THM-M-1050 Krylov估计

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 扩散过程的矩估计
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-244 / THM-M-1051 Krylov-Safonov估计

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 非散度型方程的Harnack不等式
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-245 / THM-M-1053 遍历定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 时间平均等于空间平均
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-246 / THM-M-1054 von Neumann遍历定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: L^2遍历定理
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-247 / THM-M-1055 Birkhoff遍历定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 几乎必然遍历定理
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-248 / THM-M-1056 Oseledets乘法遍历定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 随机矩阵的Lyapunov指数
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-249 / THM-M-1057 Kingman次可加遍历定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 次可加过程的遍历定理
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-250 / THM-M-1058 大偏差原理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 稀有事件的概率衰减速率
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-251 / THM-M-1059 Cramér定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 随机过程`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 独立随机变量和的大偏差
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

## 拓扑学 / 微分拓扑

### S1-M-252 / THM-M-0615 四维流形分类

- Stage1 状态: `[ ] open`
- 来源分类: `拓扑学 / 微分拓扑`
- 源文档形式化状态: `部分完成`；Stage0 bucket: `partial`
- 难度分: `149`；Stage1 lane: `known_partial_branch_deepening`；profile: `topology_algebraic_differential`
- 定理内容: 四维流形的拓扑与微分分类
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 topology、homotopy-adjacent API、manifold、homology/cohomology 相关结构。
- Stage1 partial verification scope: 先验证空间/流形对象、基本不变量、functoriality、低维/简单空间特例、已存在 mathlib theorem wrapper。
- 机器证明债分类: 允许存在 `formalization_debt` 或局部分支数学债；若发现外部 Lean 4 机器证明，必须立即 pin/import/check，不能留下 `repo_local_integration_debt`。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 空间/流形前提 -> 不变量定义 -> functoriality/naturality -> exact sequence / obstruction branch -> 主定理。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 同伦、谱序列、transversality、cobordism 等基础设施可能缺失；需优先做可检查的不变量与特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-253 / THM-M-0597 管状邻域定理

- Stage1 状态: `[ ] open`
- 来源分类: `拓扑学 / 微分拓扑`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `142`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `topology_algebraic_differential`
- 定理内容: 子流形的管状邻域存在性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 topology、homotopy-adjacent API、manifold、homology/cohomology 相关结构。
- Stage1 partial verification scope: 先验证空间/流形对象、基本不变量、functoriality、低维/简单空间特例、已存在 mathlib theorem wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 空间/流形前提 -> 不变量定义 -> functoriality/naturality -> exact sequence / obstruction branch -> 主定理。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 同伦、谱序列、transversality、cobordism 等基础设施可能缺失；需优先做可检查的不变量与特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-254 / THM-M-0607 光滑结构存在性

- Stage1 状态: `[ ] open`
- 来源分类: `拓扑学 / 微分拓扑`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `142`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `topology_algebraic_differential`
- 定理内容: 拓扑流形的光滑结构
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 topology、homotopy-adjacent API、manifold、homology/cohomology 相关结构。
- Stage1 partial verification scope: 先验证空间/流形对象、基本不变量、functoriality、低维/简单空间特例、已存在 mathlib theorem wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 空间/流形前提 -> 不变量定义 -> functoriality/naturality -> exact sequence / obstruction branch -> 主定理。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 同伦、谱序列、transversality、cobordism 等基础设施可能缺失；需优先做可检查的不变量与特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-255 / THM-M-0594 惠特尼嵌入定理

- Stage1 状态: `[ ] open`
- 来源分类: `拓扑学 / 微分拓扑`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `139`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `topology_algebraic_differential`
- 定理内容: 光滑流形可嵌入欧氏空间
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 topology、homotopy-adjacent API、manifold、homology/cohomology 相关结构。
- Stage1 partial verification scope: 先验证空间/流形对象、基本不变量、functoriality、低维/简单空间特例、已存在 mathlib theorem wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 空间/流形前提 -> 不变量定义 -> functoriality/naturality -> exact sequence / obstruction branch -> 主定理。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 同伦、谱序列、transversality、cobordism 等基础设施可能缺失；需优先做可检查的不变量与特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-256 / THM-M-0612 辛几何中的格罗莫夫定理

- Stage1 状态: `[ ] open`
- 来源分类: `拓扑学 / 微分拓扑`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `139`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `topology_algebraic_differential`
- 定理内容: 辛嵌入的不可压缩性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 topology、homotopy-adjacent API、manifold、homology/cohomology 相关结构。
- Stage1 partial verification scope: 先验证空间/流形对象、基本不变量、functoriality、低维/简单空间特例、已存在 mathlib theorem wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 空间/流形前提 -> 不变量定义 -> functoriality/naturality -> exact sequence / obstruction branch -> 主定理。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 同伦、谱序列、transversality、cobordism 等基础设施可能缺失；需优先做可检查的不变量与特殊情形。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

## 数论 / 解析数论

### S1-M-257 / THM-M-0517 岩泽主猜想

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 解析数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `146`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `analytic_number_theory`
- 定理内容: p-adic L-函数与类群的关系
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 number theory、analysis、asymptotics、series/integral API。
- Stage1 partial verification scope: 先验证 statement、基础算术函数、有限和恒等式、渐近符号接口与已知 mathlib wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 算术函数定义 -> analytic transform / estimate -> asymptotic branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 复杂分析、渐近估计、筛法、L-function API 是主要 formalization_debt。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-258 / THM-M-0498 黎曼-冯·曼戈尔特公式

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 解析数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `142`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `analytic_number_theory`
- 定理内容: 素数计数函数的显式公式
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 number theory、analysis、asymptotics、series/integral API。
- Stage1 partial verification scope: 先验证 statement、基础算术函数、有限和恒等式、渐近符号接口与已知 mathlib wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 算术函数定义 -> analytic transform / estimate -> asymptotic branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 复杂分析、渐近估计、筛法、L-function API 是主要 formalization_debt。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-259 / THM-M-0504 黎曼假设的推论

- Stage1 状态: `[ ] open`
- 来源分类: `数论 / 解析数论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `142`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `analytic_number_theory`
- 定理内容: 黎曼假设的等价命题
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 number theory、analysis、asymptotics、series/integral API。
- Stage1 partial verification scope: 先验证 statement、基础算术函数、有限和恒等式、渐近符号接口与已知 mathlib wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 算术函数定义 -> analytic transform / estimate -> asymptotic branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 复杂分析、渐近估计、筛法、L-function API 是主要 formalization_debt。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

## 概率论与随机过程 / 概率论基础

### S1-M-260 / THM-M-1011 Prohorov定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `146`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 概率测度族的紧性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-261 / THM-M-0981 柯尔莫哥洛夫公理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 概率论的公理化基础
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-262 / THM-M-0982 概率的连续性

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 概率测度的连续性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-263 / THM-M-0983 大数定律

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 频率收敛于概率
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-264 / THM-M-0984 强大数定律

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 几乎必然收敛
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-265 / THM-M-0985 柯尔莫哥洛夫强大数定律

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 独立同分布的强大数定律
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-266 / THM-M-0986 辛钦大数定律

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 弱大数定律
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-267 / THM-M-0987 中心极限定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 独立随机变量和的正态收敛
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-268 / THM-M-0988 林德伯格-列维中心极限定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 独立同分布的中心极限定理
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-269 / THM-M-0989 林德伯格-费勒中心极限定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 独立不同分布的中心极限定理
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-270 / THM-M-0990 李雅普诺夫中心极限定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 李雅普诺夫条件下的中心极限定理
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-271 / THM-M-0991 Berry-Esseen定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 中心极限定理的收敛速度
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-272 / THM-M-0992 切比雪夫不等式

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 偏离期望的概率上界
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-273 / THM-M-0993 切尔诺夫界

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 独立随机变量和的尾概率
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-274 / THM-M-0994 霍夫丁不等式

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 有界随机变量和的集中
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-275 / THM-M-0995 伯恩斯坦不等式

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 随机变量和的尾概率
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-276 / THM-M-0996 高斯集中不等式

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 高斯测度的等周不等式
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-277 / THM-M-0997 等周不等式

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 球面上集合的等周不等式
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-278 / THM-M-0998 Poincaré不等式

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 方差的上界
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-279 / THM-M-0999 对数Sobolev不等式

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 熵的上界
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-280 / THM-M-1000 transportation 不等式

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 最优传输的集中
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-281 / THM-M-1001 鞅收敛定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 鞅的几乎必然收敛
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-282 / THM-M-1002 Doob鞅收敛定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 上鞅和下鞅的收敛
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-283 / THM-M-1003 L^p鞅收敛定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: L^p有界鞅的收敛
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-284 / THM-M-1004 可选停时定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 鞅在停时的期望
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-285 / THM-M-1005 Doob不等式

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 鞅最大值的矩估计
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-286 / THM-M-1006 Burkholder-Davis-Gundy不等式

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 鞅的L^p范数等价
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-287 / THM-M-1007 柯尔莫哥洛夫三级数定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 独立随机变量级数收敛的条件
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-288 / THM-M-1008 Hewitt-Savage零一律

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 可交换事件的零一性质
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-289 / THM-M-1009 Erdős-Rényi第二引理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 波雷尔-坎泰利引理的推广
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-290 / THM-M-1010 Skorokhod表示定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 弱收敛的几乎必然表示
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-291 / THM-M-1012 Lévy连续性定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 特征函数的收敛
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-292 / THM-M-1013 Cramér-Wold定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 多维分布的收敛
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-293 / THM-M-1014 连续映射定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 连续映射保持弱收敛
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-294 / THM-M-1015 Slutsky定理

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 随机变量组合的收敛
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-295 / THM-M-1016 Delta方法

- Stage1 状态: `[ ] open`
- 来源分类: `概率论与随机过程 / 概率论基础`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `138`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `probability_stochastic_processes`
- 定理内容: 随机变量变换的渐近分布
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 measure theory、probability、filtration-like structures、integration、topology API。
- Stage1 partial verification scope: 先验证可测性、分布/期望陈述、独立性接口、基础收敛 lemma、有限状态或离散时间特例。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 概率空间 -> 随机变量/过程 -> 可测性与积分性 -> 收敛/鞅/Markov branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: filtration、stopping time、stochastic integral 等 API 可能需先自定义；不得把数学已知结果写成 repo-local completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

## 代数学 / 域论

### S1-M-296 / THM-M-0024 马祖尔-怀尔斯定理

- Stage1 状态: `[ ] open`
- 来源分类: `代数学 / 域论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `140`；Stage1 lane: `hard_mathlib_anchor_and_wrapper`；profile: `general_hard_mathematics`
- 定理内容: 岩泽主猜想的证明
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib；具体 API 需要 Stage1 anchor audit 后锁定。
- Stage1 partial verification scope: 先验证 statement、基础定义、可由 mathlib 直接表达的子引理、以及 repo-local wrapper skeleton。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 定义规整 -> 关键引理 -> case split / induction / compactness branch -> terminal theorem wrapper。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 需先完成 mathlib / external Lean 4 source audit，避免把源文档的 `已验证` 误当成本仓库 completed。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

## 其他重要领域 / 动力系统

### S1-M-297 / THM-M-1400 庞加莱-本迪克松定理

- Stage1 状态: `[ ] open`
- 来源分类: `其他重要领域 / 动力系统`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `134`；Stage1 lane: `hard_statement_first_partial_verification`；profile: `dynamical_systems`
- 定理内容: 二维系统的极限集
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 + mathlib 的 topology、measure theory、analysis、ODE-adjacent API。
- Stage1 partial verification scope: 先验证 map/flow definitions、invariance、固定点/周期点特例、有限或紧空间情形。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: phase space -> map/flow -> invariant/ergodic property -> stability/recurrence branch -> 主结论。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: ergodic theory、smooth flow、hyperbolicity API 需要大量基础设施；优先离散时间与 compact metric spaces。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

## 数理逻辑 / 模型论

### S1-M-298 / THM-M-0652 插值定理

- Stage1 状态: `[ ] open`
- 来源分类: `数理逻辑 / 模型论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `134`；Stage1 lane: `hard_statement_first_partial_verification`；profile: `logic_model_set_proof_theory`
- 定理内容: 插值公式的存在性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 可编码语法、证明系统、模型语义、集合论对象；mathlib 可支持 order/set/cardinal/model-theoretic fragments。
- Stage1 partial verification scope: 先验证语法与推导系统、soundness 子结论、有限 fragment、已形式化 meta-theory wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 语法编码 -> 语义/证明关系 -> soundness/completeness/cut/compactness branch -> 主结果。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 元理论编码、Gödel numbering、模型存在性与 universe 管理复杂；需要先定义可执行 syntax 与 proof relation。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-299 / THM-M-0660 主公式定理

- Stage1 状态: `[ ] open`
- 来源分类: `数理逻辑 / 模型论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `134`；Stage1 lane: `hard_statement_first_partial_verification`；profile: `logic_model_set_proof_theory`
- 定理内容: 稳定理论中主公式的存在性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 可编码语法、证明系统、模型语义、集合论对象；mathlib 可支持 order/set/cardinal/model-theoretic fragments。
- Stage1 partial verification scope: 先验证语法与推导系统、soundness 子结论、有限 fragment、已形式化 meta-theory wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 语法编码 -> 语义/证明关系 -> soundness/completeness/cut/compactness branch -> 主结果。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 元理论编码、Gödel numbering、模型存在性与 universe 管理复杂；需要先定义可执行 syntax 与 proof relation。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。

### S1-M-300 / THM-M-0674 饱和模型存在性

- Stage1 状态: `[ ] open`
- 来源分类: `数理逻辑 / 模型论`
- 源文档形式化状态: `已验证`；Stage0 bucket: `closed`
- 难度分: `134`；Stage1 lane: `hard_statement_first_partial_verification`；profile: `logic_model_set_proof_theory`
- 定理内容: 饱和模型的存在性
- 目标形式系统: `Lean 4 + mathlib` only；非 Lean4 路线不计入本 Stage1 slot。
- Lean 4 可部分验证依据: Lean 4 可编码语法、证明系统、模型语义、集合论对象；mathlib 可支持 order/set/cardinal/model-theoretic fragments。
- Stage1 partial verification scope: 先验证语法与推导系统、soundness 子结论、有限 fragment、已形式化 meta-theory wrapper。
- 机器证明债分类: 默认按 `formalization_debt` 处理，直到 primary-source audit 证明已有 Lean 4 机器证明；一旦发现外部 Lean 4 closure，必须转入 pinned dependency / wrapper 整合，不能作为 completed 留下 repo-local integration debt。
- repo-local 整合债规则: 若 anchor audit 发现外部 Lean 4 proof 已存在，本条不得保持 anchor-only；必须 pin/import/check 或显式列为 integration blocker，完成态不允许残留 `repo_local_integration_debt`。
- Lean 4 陈述规范化任务: 把源陈述改写成带显式 universe、变量域、前提条件、结论类型的 theorem statement；优先生成 `Stage1.<uid>.StatementShape : Prop` 或等价 namespace wrapper。
- mathlib / external anchor audit: 先查 mathlib module/theorem，再查公开 Lean 4 external project；记录 exact module、theorem name、commit/revision、是否能进入 Lake dependency closure。
- theorem-tree seed: 语法编码 -> 语义/证明关系 -> soundness/completeness/cut/compactness branch -> 主结果。
- proof-package 初始切分:
  1. statement normalization / notation freeze
  2. mathlib object model and imported theorem audit
  3. core reduction or bridge lemma package
  4. high-risk leaf discovery and `<=100` local ledger
  5. repo-local wrapper / pinned dependency / local proof-body closure gate
- 形式化阻塞点: 元理论编码、Gödel numbering、模型存在性与 universe 管理复杂；需要先定义可执行 syntax 与 proof relation。
- Stage1 assurance gate: 必须按 `Docs/Stage1_Blueprint_rev-5.6.md` 实例化 canonical statement fingerprint、frozen obligation registry、typed proof/provenance/workflow graphs、structured validation specs、content-addressed receipts、source-boundary/unique coverage、node-specific H/R review、hermetic Lean 4 replay 与独立验收；`<=100` 只作为 leaf split threshold。
- 当前完成判定: `not completed`; Stage1 selection 不是 proof completion。
