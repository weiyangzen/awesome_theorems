# 费马大定理形式化验证研究

> 蓝图编号: `THM-M-0387`
> 学科 / 子分类: `数学 / 数论 / 丢番图方程`
> 研究日期: `2026-04-16`

配套物料目录：

- [`README.md`](./README.md)
- [`machine_checked_audit.md`](./machine_checked_audit.md)
- [`process_audit.md`](./process_audit.md)
- [`build_validation.md`](./build_validation.md)
- [`FermatLastTheorem_Sample.lean`](./FermatLastTheorem_Sample.lean)
- [`run_local_validation.sh`](./run_local_validation.sh)
- [`meta.json`](./meta.json)
- [`Formalizations/Lean/AwesomeTheorems.lean`](../Formalizations/Lean/AwesomeTheorems.lean)
- [`Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/FLT4Path.lean`](../Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/FLT4Path.lean)
- [`Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/FLT3Path.lean`](../Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/FLT3Path.lean)
- [`Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/RegularPrimesPath.lean`](../Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/RegularPrimesPath.lean)
- [`Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/Sample.lean`](../Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/Sample.lean)

本文档按照仓库 `README.md` 与 `Docs/Stage0_Blueprint.md` 对单个定理的字段要求，
对“费马大定理”做一次完整的形式化验证研究，并给出一个贴近 `2026-04-24` 的 `Lean 4 + mathlib`
生态的最小样例。

## Machine-Checked Boundary Snapshot

截至 `2026-04-24`，本仓库的 machine-checked 边界如下：

Source evidence: local Lean dependency metadata pins source project
`leanprover-community/mathlib4` at revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` in
`Formalizations/Lean/lake-manifest.json` and `Formalizations/Lean/lakefile.lean`.
The exact mathlib module for `FermatLastTheoremFor`, `FermatLastTheorem`, and
the reduction lemmas is `Mathlib.NumberTheory.FLT.Basic`; `n = 4` uses
`Mathlib.NumberTheory.FLT.Four`; `n = 3` uses `Mathlib.NumberTheory.FLT.Three`.
Regular primes theorem closure is upstream-only in source project
`leanprover-community/flt-regular`; this repository records only the
anchor module `AwesomeTheorems.NumberTheory.THM_M_0387.RegularPrimesPath`.

- `n = 4` repo-local theorem-level closure 通过 `Mathlib.NumberTheory.FLT.Four` import
  与 wrapper theorem `flt4Path` 记录。
- `n = 3` repo-local theorem-level closure 通过 `Mathlib.NumberTheory.FLT.Three` import
  与 wrapper theorem `flt3Path` 记录。
- `flt4IntPath` 是由 mathlib 的 `fermatLastTheoremFor_iff_int` 等价推出的 repo-local 派生 wrapper。
- `flt8ViaFlt4Path` 是由 `FermatLastTheoremFor.mono` 与 `4 ∣ 8` 的指数整除单调性推出的 repo-local 派生 wrapper。
- 完整 `FermatLastTheorem` 不是本仓库 repo-local machine-checked theorem；样例只展示 statement/reduction API 与特例 wrapper。
- regular primes theorem closure 来自上游 `flt-regular`，本仓库不 vendoring 证明本体；这里只保留 anchor-only statement/module/theorem-name 记录。

## Cross-File Naming Consistency Record

截至 `2026-04-24`，跨文件名称比对结果如下；本节只记录公开材料之间的
canonical name / reader-facing alias 对齐关系，不改变 theorem-level 边界。

### `n = 4` package names

`full_study.md`、`machine_checked_audit.md`、`process_audit.md`、
`eligibles/n4_proof_process.md` 共同使用以下 `7` 个 package 名；
`full_study.md` 与 eligible 主稿在标题中保留 `n = 4 /` 前缀，
审计表在 package 列中使用去前缀后的同名短名：

1. `n = 4 / bridge packaging`
2. `n = 4 / minimal normalization`
3. `n = 4 / first triple classification`
4. `n = 4 / second triple classification`
5. `n = 4 / coprimality bridge`
6. `n = 4 / square extraction and sign cleanup`
7. `n = 4 / smaller-solution construction and size comparison`

### `regular primes` package names

`full_study.md` 与 `eligibles/regular_primes_proof_process.md` 使用完整 reader-facing
标题；`machine_checked_audit.md` 与 `process_audit.md` 的 package ledger 使用较短的
formal-flow alias。二者的 canonical 对应关系固定为：

| canonical public heading | audit ledger alias |
|---|---|
| `regular primes / setup and regularity engine` | `setup` |
| `regular primes / MayAssume primitive reduction` | `MayAssume` |
| `regular primes / Case I outer statement` | `Case I outer statement` |
| `regular primes / Case I ideal extraction` | `Case I ideal extraction` |
| `regular primes / Case I principalization` | `Case I principalization` |
| `regular primes / Case I element recovery and close` | `Case I element recovery / close` |
| `regular primes / Case II pi-language reduction` | `Case II π-language` |
| `regular primes / Case II ideal-factor layer` | `Case II ideal-factor layer` |
| `regular primes / Case II distinguished root` | `Case II distinguished root` |
| `regular primes / Case II descent core` | `Case II descent core` |
| `regular primes / Case II close and merge` | `Case II close / merge` |

Regular primes boundary is recorded explicitly:
upstream theorem closure: yes / repo-local vendored theorem closure: no, anchor-only / repo-local anchor-only statement/module/theorem-name record: yes.

### canonical high-risk leaf names

`Docs/Blueprint_Guidelines.md` fixes the cross-file high-risk set at `7` leaves.
The `n = 4` leaves appear in `machine_checked_audit.md`, `process_audit.md`,
and `eligibles/n4_proof_process.md`; the regular-primes leaves appear in
`machine_checked_audit.md`, `process_audit.md`, and
`eligibles/regular_primes_proof_process.md`:

1. `raw coprime triple classification`
2. `square extraction for r*s with sign cleanup`
3. `strict natAbs descent hic`
4. `Case II ideal-factor layer / global product to local p-th powers`
5. `Case II distinguished root / p_pow_dvd_c_eta_zero`
6. `Case II descent core / three-root formula and raw descent`
7. `Case II close / merge / not_exists_solution'`

The intentionally non-canonical package-level subitems remain excluded from this set:
`Int.gcd a n = 1 transfer`、`exists_ideal pairwise ideal coprimality interface`、
`caseI_easier / aux-index exclusion`。

### `n = 3` proof-process scope

`Docs/Blueprint_Guidelines.md` says `n = 3` should not be over-expanded into
trivial arithmetic leaves such as elementary coprimality or divisibility propagation.
The public `eligibles/n3_proof_process.md` follows that boundary: it keeps the
readable proof architecture at the level of mod `9` Case 1、Eisenstein integers、
generalized equation、typed solution objects、and `λ`-adic multiplicity descent,
while explicitly declining tutorial-style expansion of routine arithmetic preliminaries.

## Human-Readable Supervision

截至 `2026-04-24`，本节只追踪 `n = 4` 与 `regular primes` 的人类可读展开进度。

- 唯一 authoritative progress source 是下方 `Execution Checklist`。
- 这 `18` 个 execution unit 已经直接拆到最小公开归档粒度，因此不再对这 `18` 项自动二次拆分。
- 最终对外归档面只有 [`eligibles/n4_proof_process.md`](./eligibles/n4_proof_process.md)
  与 [`eligibles/regular_primes_proof_process.md`](./eligibles/regular_primes_proof_process.md) 这两份主稿；
  蓝图勾选只能根据对应公开归档面与 `Completion Gate` 的真实状态回写，不能手工抢跑。
- 以后更新 `Execution Checklist` 时，每个 execution unit 都必须同时保留公开归档面
  与 ``2026-04-24` 状态` / `Completion Gate`；若二者任一缺失，不得更新总进度或勾选状态。

<!-- EXECUTION_PROGRESS_SUMMARY_START -->
- 总进度: `18/18`
- `n = 4`: `7/7`
- `regular primes`: `11/11`
- 监工规则: 只有当对应公开归档面同时写明 `completed` 与 `Completion Gate = passed`，蓝图才允许从 `[ ]` 改为 `[x]`。
- 这 `18` 个 unit 已经是最细公开执行层；不再对这 `18` 项自动二次拆分。
<!-- EXECUTION_PROGRESS_SUMMARY_END -->

## Execution Checklist

<!-- EXECUTION_CHECKLIST_START -->
- [x] `FLT-HR-001` `n = 4 / bridge packaging`
  归档面: `THM-M-0387/eligibles/n4_proof_process.md :: n = 4 / bridge packaging`
  `2026-04-24` 状态: `completed` / `Completion Gate = passed`
- [x] `FLT-HR-002` `n = 4 / minimal normalization`
  归档面: `THM-M-0387/eligibles/n4_proof_process.md :: n = 4 / minimal normalization`
  `2026-04-24` 状态: `completed` / `Completion Gate = passed`
- [x] `FLT-HR-003` `n = 4 / first triple classification`
  归档面: `THM-M-0387/eligibles/n4_proof_process.md :: n = 4 / first triple classification`
  `2026-04-24` 状态: `completed` / `Completion Gate = passed`
- [x] `FLT-HR-004` `n = 4 / second triple classification`
  归档面: `THM-M-0387/eligibles/n4_proof_process.md :: n = 4 / second triple classification`
  `2026-04-24` 状态: `completed` / `Completion Gate = passed`
- [x] `FLT-HR-005` `n = 4 / coprimality bridge`
  归档面: `THM-M-0387/eligibles/n4_proof_process.md :: n = 4 / coprimality bridge`
  `2026-04-24` 状态: `completed` / `Completion Gate = passed`
- [x] `FLT-HR-006` `n = 4 / square extraction and sign cleanup`
  归档面: `THM-M-0387/eligibles/n4_proof_process.md :: n = 4 / square extraction and sign cleanup`
  `2026-04-24` 状态: `completed` / `Completion Gate = passed`
- [x] `FLT-HR-007` `n = 4 / smaller-solution construction and size comparison`
  归档面: `THM-M-0387/eligibles/n4_proof_process.md :: n = 4 / smaller-solution construction and size comparison`
  `2026-04-24` 状态: `completed` / `Completion Gate = passed`
- [x] `FLT-HR-008` `regular primes / setup and regularity engine`
  归档面: `THM-M-0387/eligibles/regular_primes_proof_process.md :: regular primes / setup and regularity engine`
  `2026-04-24` 状态: `completed` / `Completion Gate = passed`
- [x] `FLT-HR-009` `regular primes / MayAssume primitive reduction`
  归档面: `THM-M-0387/eligibles/regular_primes_proof_process.md :: regular primes / MayAssume primitive reduction`
  `2026-04-24` 状态: `completed` / `Completion Gate = passed`
- [x] `FLT-HR-010` `regular primes / Case I outer statement`
  归档面: `THM-M-0387/eligibles/regular_primes_proof_process.md :: regular primes / Case I outer statement`
  `2026-04-24` 状态: `completed` / `Completion Gate = passed`
- [x] `FLT-HR-011` `regular primes / Case I ideal extraction`
  归档面: `THM-M-0387/eligibles/regular_primes_proof_process.md :: regular primes / Case I ideal extraction`
  `2026-04-24` 状态: `completed` / `Completion Gate = passed`
- [x] `FLT-HR-012` `regular primes / Case I principalization`
  归档面: `THM-M-0387/eligibles/regular_primes_proof_process.md :: regular primes / Case I principalization`
  `2026-04-24` 状态: `completed` / `Completion Gate = passed`
- [x] `FLT-HR-013` `regular primes / Case I element recovery and close`
  归档面: `THM-M-0387/eligibles/regular_primes_proof_process.md :: regular primes / Case I element recovery and close`
  `2026-04-24` 状态: `completed` / `Completion Gate = passed`
- [x] `FLT-HR-014` `regular primes / Case II pi-language reduction`
  归档面: `THM-M-0387/eligibles/regular_primes_proof_process.md :: regular primes / Case II pi-language reduction`
  `2026-04-24` 状态: `completed` / `Completion Gate = passed`
- [x] `FLT-HR-015` `regular primes / Case II ideal-factor layer`
  归档面: `THM-M-0387/eligibles/regular_primes_proof_process.md :: regular primes / Case II ideal-factor layer`
  `2026-04-24` 状态: `completed` / `Completion Gate = passed`
- [x] `FLT-HR-016` `regular primes / Case II distinguished root`
  归档面: `THM-M-0387/eligibles/regular_primes_proof_process.md :: regular primes / Case II distinguished root`
  `2026-04-24` 状态: `completed` / `Completion Gate = passed`
- [x] `FLT-HR-017` `regular primes / Case II descent core`
  归档面: `THM-M-0387/eligibles/regular_primes_proof_process.md :: regular primes / Case II descent core`
  `2026-04-24` 状态: `completed` / `Completion Gate = passed`
- [x] `FLT-HR-018` `regular primes / Case II close and merge`
  归档面: `THM-M-0387/eligibles/regular_primes_proof_process.md :: regular primes / Case II close and merge`
  `2026-04-24` 状态: `completed` / `Completion Gate = passed`
<!-- EXECUTION_CHECKLIST_END -->

## Unit Inventory

截至 `2026-04-24`，`18` 个 execution unit 的公开归档面固定如下：

- `FLT-HR-001` 到 `FLT-HR-007`: [`eligibles/n4_proof_process.md`](./eligibles/n4_proof_process.md)
- `FLT-HR-008` 到 `FLT-HR-018`: [`eligibles/regular_primes_proof_process.md`](./eligibles/regular_primes_proof_process.md)
- 每个 unit 的完成信号来自对应公开归档面与 `Completion Gate`；`full_study.md` 只负责同步显示。
- 若公开归档面在 `2026-04-24` 处于 `missing`、`open`、`not passed` 等非完成态，蓝图必须保持 `[ ]`。

### Evidence Cross-Check for Completed Execution Units

截至 `2026-04-24`，`full_study.md` 把 `FLT-HR-001` 到 `FLT-HR-018` 计为 completed。
这些 completed unit 的证据命名口径如下：

- machine anchor evidence: `machine_checked_audit.md` 的 `n = 4` package 表覆盖 `FLT-HR-001` 到 `FLT-HR-007`，`regular primes` package 表覆盖 `FLT-HR-008` 到 `FLT-HR-018`；其中 `FLT-HR-017` 明名 hooks `exists_solution` 与 `exists_solution'`，`FLT-HR-018` 明名 hooks `not_exists_solution`、`not_exists_solution'`、`not_exists_Int_solution`、`not_exists_Int_solution'`、`caseII`、`flt_regular`。
- public merge target evidence: `FLT-HR-001` 到 `FLT-HR-007` 的唯一公开合并目标是 `THM-M-0387/eligibles/n4_proof_process.md`，`FLT-HR-008` 到 `FLT-HR-018` 的唯一公开合并目标是 `THM-M-0387/eligibles/regular_primes_proof_process.md`。
- independent `<=100` local ledger evidence: `THM-M-0387/eligibles/n4_proof_process.md` 已为 `FLT-HR-001` 到 `FLT-HR-007` 各自命名 local ledger；`THM-M-0387/eligibles/regular_primes_proof_process.md` 已为 `FLT-HR-008` 到 `FLT-HR-018` 各自命名 local ledger，且 `FLT-HR-017` 的 ledger 总计 `35` 步，`FLT-HR-018` 的 ledger 总计 `34` 步。
- boundary wording evidence: regular primes 在 `2026-04-24` 保持 `upstream theorem closure: yes / repo-local vendored theorem closure: no, anchor-only / repo-local anchor-only statement/module/theorem-name record: yes` 的边界口径；`FLT-HR-018` 的完成只表示公开人类可读展开与本地预算账本已经补齐。

需要先明确一个事实：截至 `2026-04-16`，费马大定理的**完整**机器检验证明应归类为
`部分验证 / 截至 2026-04-16 未完成完整 repo-local machine-check`，而不是简单的全局 `已验证`。原因是：

1. `mathlib` 已经给出 `n = 3` 与 `n = 4` 的 machine-checked 证明。
2. Lean 社区已经公开发表了 regular primes 情形的完整形式化结果。
3. 但截至 `2026-04-24`，完整的 Taylor-Wiles / Wiles 主证明链尚未形成可由本仓库 repo-local 验证的 Lean 证明，因此不能保守地声称“全定理已完成 machine-checked”。

## 一、按 README / Blueprint 字段完整填写

### 定理内容

费马大定理的标准陈述是：

> 对任意整数 `n > 2`，方程 `x^n + y^n = z^n` 没有非零整数解。
> 等价地，对任意正整数 `n > 2`，方程 `x^n + y^n = z^n` 没有正整数解。

在 `mathlib` 中，对固定指数 `n` 的陈述被编码为：

- `FermatLastTheoremFor n`
- `FermatLastTheoremWith R n`
- `FermatLastTheorem`

其中：

- `FermatLastTheoremFor n` 表示自然数上的固定指数版本；
- `FermatLastTheoremWith R n` 表示任意半环 `R` 上的固定指数版本；
- `FermatLastTheorem` 表示“对所有 `n >= 3` 都成立”的总陈述。

### 命题类型

`数学定理 / 不存在性命题 / 丢番图方程结果 / 数论核心定理`

更精细地说，它是一类关于整数点不存在性的全称命题，其现代证明高度依赖：

- 椭圆曲线
- 模形式
- 伽罗瓦表示
- 降层与模性提升

### 形式化可验证性

建议在本仓库中标注为：

`部分验证 / 截至 2026-04-24 未完成完整 repo-local machine-check（`n = 3`、`n = 4` 由 mathlib import 与 repo-local wrapper 记录；regular primes theorem closure 来自上游 `flt-regular` 且本仓库 anchor-only）`

原因如下：

- `n = 4` 的无限递降证明已经在 `mathlib` 中完成，本仓库用 `flt4Path` 作为 repo-local wrapper 记录闭合点。
- `n = 3` 的 Eisenstein 整数 / 三次分圆域路线已经在 `mathlib` 中完成，本仓库用 `flt3Path` 作为 repo-local wrapper 记录闭合点。
- `regular primes` 情形已有公开发表的 Lean 4 完整形式化结果；本仓库只保留 anchor-only statement/module/theorem-name 记录，不 vendoring `flt-regular` 证明本体。
- 但截至 `2026-04-24`，完整的 Wiles / Taylor-Wiles 主线尚未形成可由本仓库 repo-local 验证的 Lean 证明。

### 目标形式系统

首选目标形式系统应为：

- `Lean 4 + mathlib`

原因：

- 截至 `2026-04-24`，最活跃的公开 FLT 总证明项目就在 Lean 生态中推进。
- `mathlib` 已经为 `n = 3`、`n = 4`、代数数论、分圆域、PID、ideal、valuation、gcd、coprimality 等组件提供了可复用基础设施。
- 截至 `2026-04-24`，本仓库没有 Coq / Isabelle 的本地工程骨架，因此以 Lean 样例最贴合本项目状态。

备选系统：

- `Isabelle/HOL`
- `Coq / Rocq + MathComp`

但若要与 `2026-04-24` 的社区产出直接对接，Lean 是第一选择。

### 逻辑基础/形式系统

若以 Lean 路线为准，逻辑基础可描述为：

- `依赖类型论`
- `Prop` 中的定理证明
- `classical` 推理按需开启
- 商类型、理想、代数数论对象通过 `mathlib` 现有抽象层表达

若迁移到 Isabelle/HOL，则逻辑基础会变成：

- `经典高阶逻辑 (HOL)`

对 FLT 而言，真正的难点不在陈述层，而在于：

- 代数数论对象的组织
- 模形式与伽罗瓦表示的 API 设计
- 从 paper proof 到可组合 lemma graph 的拆分

### 提出假说时间

`1637`

### 提出背景

费马在阅读丢番图《算术》时于页边写下注记，声称已经找到了一个“真正惊人的证明”，说明当 `n > 2` 时方程 `x^n + y^n = z^n` 没有正整数解，但页边空白放不下。

从形式化研究视角看，背景应拆成两个层次：

1. 历史背景：17 世纪整数方程与古典数论问题。
2. 现代证明背景：20 世纪下半叶形成的“椭圆曲线 - 模形式 - 伽罗瓦表示”路线。

后者才是截至 `2026-04-24` 可执行的主形式化路线。

### 精确定义与前提条件

建议将正式版本写成如下精确形式：

1. 变量域：`x, y, z : ℕ` 或 `ℤ`
2. 非平凡性：`x ≠ 0 ∧ y ≠ 0 ∧ z ≠ 0`
3. 指数范围：`n : ℕ` 且 `n ≥ 3`
4. 方程：`x ^ n + y ^ n = z ^ n`
5. 目标：推出矛盾

在形式化中，还常用以下等价化简：

1. 从任意 `n ≥ 3` 约化到 `n = 4` 与“奇素数指数 `p`”。
2. 从自然数版本转到整数版本或有理数版本。
3. 只考虑互素的 primitive solution。

`mathlib` 已经显式提供：

- `fermatLastTheoremFor_iff_int`
- `fermatLastTheoremFor_iff_rat`
- `FermatLastTheorem.of_odd_primes`

因此“陈述规范化”这一步在 Lean 里已经有成熟入口。

这里还需要把一个常见疑问提前说清楚：

> 为什么没有把 `4` 以上的非素数指数单独列成 branch？

原因不是遗漏，而是它们已经被指数整除约化吸收了。

1. 若 `n > 2` 且 `4 ∣ n`，那么只要 `n = 4` 成立，`FermatLastTheoremFor.mono` 就把结论上推到该 `n`。
2. 若 `n > 2` 是合数但 `4 ∤ n`，那么 `n` 必有奇素数因子 `p`；一旦指数 `p` 成立，同样由 `FermatLastTheoremFor.mono` 推出指数 `n`。

因此，`6, 8, 9, 10, 12, ...` 不是一条被漏掉的新 branch，
而是 statement / reduction 层已经处理掉的派生指数。

### 被证明的过程

从研究与形式化双重视角，费马大定理的证明过程最好拆成“一个前置约化层 + 三个主闭环”。

#### 前置层：合数指数约化

- 假说内容：存在非零整数解满足 `a^n + b^n = c^n`，其中 `n > 2` 为合数
- 中间转化：
  - 若 `4 ∣ n`，把问题压回 `n = 4`
  - 若 `4 ∤ n`，选取奇素数因子 `p ∣ n`，把问题压回指数 `p`
- 核心工具：`FermatLastTheoremFor.mono`
- 结论：`4` 以上非素数指数不需要单独形成新 branch

这一步已经在 `mathlib` 的 reduction layer 中 machine-check。

#### 闭环 A：指数 `4`

- 假说内容：存在非零整数 `a, b, c` 使得 `a^4 + b^4 = c^4`
- 中间转化：只需证明 `a^4 + b^4 = c^2` 无非零整数解
- 核心工具：勾股数分类 + 无限递降
- 结论：矛盾，故 `n = 4` 成立

这一路线已经在 `mathlib` 中完整 machine-check。

#### 闭环 B：指数 `3`

- 假说内容：存在非零整数 `a, b, c` 使得 `a^3 + b^3 = c^3`
- 中间转化：转入 `ℤ[ζ₃]`，研究 `a^3 + b^3 = u * c^3`
- 核心工具：三次分圆域、单位、`λ = ζ₃ - 1` 的重数下降、Kummer 型引理
- 结论：通过 descent 得出矛盾

这一路线也已经在 `mathlib` 中完整 machine-check。

在写作粒度上，这一分支默认读者已经掌握大学水平的初等数论，
因此不会把 `互素`、`整除` 这类显然准备动作拆成过度琐碎的小节点；
真正展开的是 mod `9`、generalized equation、`λ = ζ₃ - 1` 的重数下降这些承担证明工作的节点。

#### 闭环 C：一般奇素数指数 `p`

- 假说内容：存在 primitive 非平凡解 `a^p + b^p = c^p`
- 构造：Frey 椭圆曲线
- 关键桥梁：Serre 观点、Ribet 降层、Wiles/Taylor-Wiles 模性提升
- 终局：该曲线既必须来自某模形式，又因降层落到不存在的低层空间，得到矛盾

这一路线是完整 FLT 形式化的主战场，截至 `2026-04-24` 为推进中。

### 被证明年代或时间

完整数学证明的历史时间点建议写为：

- `1994`：Andrew Wiles 公布证明
- `1995`：Wiles 与 Taylor-Wiles 的正式修正与发表完成

如果需要在仓库中更严格地区分，可写为：

- `1994-1995`

### 被证明的意义

费马大定理的重要性不只在于“一个著名难题被解决”，更在于它是现代数论结构化的交汇点：

1. 它把整数方程问题与椭圆曲线、模形式联系起来。
2. 它推动了模性与伽罗瓦表示技术的发展。
3. 它是 proof assistant 社区测试“能否形式化现代高阶数论”的标志性 benchmark。
4. 它适合作为仓库中的“长证明链 formalization case study”，因为从陈述层到库工程层都有代表性。

### 证明路径上的定理或其他引例引理

建议按“已经 machine-checked / `2026-04-24` 推进中 / 截至 `2026-04-24` 是难点”三层来组织：

#### 已经 machine-checked

- `FermatLastTheoremFor 4`
- `FermatLastTheoremFor 3`
- `FermatLastTheorem.of_odd_primes`
- `fermatLastTheoremFor_iff_int`
- `fermatLastTheoremFor_iff_rat`
- 勾股数组件、coprime 与 gcd 基础
- 三次分圆域与相关 algebraic number theory 基础

#### 已有公开阶段性完整结果

- regular primes 情形的 FLT 完整 Lean 形式化
- Kummer's lemma 的 Lean 形式化
- Hilbert 90-94 在该路线中的可形式化改写

#### 完整总证明待打通

- Frey 曲线构造的系统化 API
- 模形式空间与 Hecke 代数的形式化基础设施
- Galois representation 与 deformation theory 的统一接口
- Ribet 降层与 Taylor-Wiles patching 主链

### 依赖图与关键引理

下面给出一个适合仓库在 `2026-04-24` 以后拆分的依赖图：

```text
费马大定理
├── 陈述规范化
│   ├── 自然数 / 整数 / 有理数版本等价
│   ├── primitive solution 化简
│   └── 约化到 n = 4 与奇素数指数
├── 合数指数吸收层
│   ├── 4 | n 归入 n = 4
│   └── odd prime p | n 归入奇素数指数
├── 特殊指数机器检验
│   ├── n = 4
│   │   ├── 勾股数分类
│   │   ├── 最小反例规整
│   │   └── 无限递降
│   └── n = 3
│       ├── 三次分圆域
│       ├── generalized equation
│       ├── λ-进重数
│       └── descent
└── 一般奇素数指数
    ├── primitive solution reduction
    ├── Frey curve
    ├── semistability
    ├── mod p Galois representation
    ├── Ribet level lowering
    ├── semistable modularity
    └── contradiction
```

### 证据类型

该条目应标记为复合型证据：

- `解析证明 / 代数证明`
- `无限递降`
- `代数数论证明`
- `现代模性证明`
- `机器检验（局部完整 + 截至 2026-04-24 总体 repo-local machine-check 未完成）`

换句话说，它不是“单一风格”的 theorem item，而是一个跨多个证明范式的大型证明簇。

### 形式化阻塞点

费马大定理在形式化上的主要阻塞点，不是 statement 太难，而是 proof stack 太深：

1. `库工程阻塞`
   需要大量代数数论、模形式、椭圆曲线、Hecke 代数与伽罗瓦表示基础设施。

2. `证明分解阻塞`
   论文中的许多步骤对人类读者是“标准事实”，但对 proof assistant 必须拆成细粒度 lemma。

3. `对象表示阻塞`
   同一个数学对象在 paper 中可能切换多个视角，但在 formal system 里需要稳定 API。

4. `经典数学依赖阻塞`
   理想、Noether 性、局部化、完备化、表示理论等部分往往涉及 noncomputable/classical 工具。

5. `长链协同阻塞`
   完整路线不是一个人几周能封闭的证明，而是多年协作项目。

因此，仓库对该条目最合理的执行策略不是“一步到位”，而是分层推进：

- statement layer
- reduction layer
- special exponent layer
- algebraic number theory layer
- modularity / Galois layer

### 提出者/来源

- `提出者`: Pierre de Fermat
- `现代证明核心作者`: Andrew Wiles，Richard Taylor

### 等价表述

在本仓库中建议显式记录以下等价表述：

1. 自然数版本与整数版本等价。
2. 自然数版本与有理数版本等价。
3. 只需考虑 primitive solution。
4. 只需证明 `n = 4` 与所有奇素数指数。

其中第 4 点对 formalization 尤其重要，因为它直接决定任务拆分边界。

### 所需公理

若仅就 statement 而言，需要的只是通常的算术与代数结构。

若就 `2026-04-24` 的主流形式化路线而言，建议在仓库中写得更实务化：

- 自然数、整数、有理数的标准代数公理
- 唯一分解 / PID / gcd 相关结构
- 理想、商环、分圆域、整闭包等代数数论对象
- 完整总证明阶段可能需要更强的经典数学基础设施

### 经典逻辑/选择公理依赖

建议在仓库中写成下面这种“分层判断”，而不是简单地写“需要”或“不需要”：

1. `n = 4` 的数学思想本身偏初等，可较少依赖高阶选择原理。
2. `n = 3` 与 regular primes 路线已经进入代数数论对象层，Lean 实现中存在 `noncomputable` 与 classical 组织方式。
3. 完整 Wiles/Taylor-Wiles 路线大概率会广泛使用现代经典数学库，因此在工程上应按“经典逻辑 + 局部选择”准备。

### 现有 machine-checked 状态

截至 `2026-04-16`，可保守记录为：

| 范围 | 状态 | 说明 |
|---|---|---|
| statement / reduction 层 | 已验证 | `mathlib` 中已给出 FLT 的标准陈述、指数整除约化、`ℕ/ℤ/ℚ` 版本等价、primitive solution 化简入口 |
| `n = 4` | repo-local wrapper 已记录 | `mathlib` 中的 `fermatLastTheoremFour`，本仓库通过 import 与 `flt4Path` 记录 theorem-level closure；证明链并非一句 theorem，而是最小解 + 互素化 + 勾股数分类 + 无限递降 |
| `n = 3` | repo-local wrapper 已记录 | `mathlib` 中的 `fermatLastTheoremThree`，本仓库通过 import 与 `flt3Path` 记录 theorem-level closure；证明链包含 mod `9` 的 Case 1、三次分圆域中的 generalized equation、`λ = ζ₃ - 1` 的 multiplicity descent |
| regular primes | upstream closure / repo-local anchor-only | `flt-regular` 项目与 2025 年论文给出 `FermatLastTheoremFor p` 的完整 Lean 4 证明；本仓库不 vendoring 证明本体，只记录 statement shape、module anchors 与 terminal theorem name `flt_regular` |
| 完整 FLT | 未完成 repo-local machine-check | 截至 `2026-04-24`，完整 `FermatLastTheorem` 不是本仓库 repo-local machine-checked theorem |

因此，最稳妥的总体状态不是 `已验证`，而是：

`部分验证 / 截至 2026-04-24 未完成完整主证明 repo-local machine-check（special exponents + regular primes 已有可追踪结果）`

### 现有工件链接

- `mathlib` 对 FLT statement 的定义：
  <https://leanprover-community.github.io/mathlib4_docs/Mathlib/NumberTheory/FLT/Basic.html>
- `mathlib` 对 `n = 4` 的完整证明：
  <https://leanprover-community.github.io/mathlib4_docs/Mathlib/NumberTheory/FLT/Four.html>
  exact Lean module: `Mathlib.NumberTheory.FLT.Four`; terminal theorem:
  `fermatLastTheoremFour`.
- `mathlib` 对 `n = 3` 的完整证明：
  <https://leanprover-community.github.io/mathlib4_docs/Mathlib/NumberTheory/FLT/Three.html>
  exact Lean module: `Mathlib.NumberTheory.FLT.Three`; terminal theorem:
  `fermatLastTheoremThree`.
- `flt-regular` 主 theorem `flt_regular`：
  <https://github.com/leanprover-community/flt-regular/blob/master/FltRegular/FltRegular.lean>
  source repository: <https://github.com/leanprover-community/flt-regular>;
  `2026-04-24` source-identification command
  `git ls-remote https://github.com/leanprover-community/flt-regular.git HEAD refs/heads/master`
  returned `0ba4fc22e1742623c3923c5a7a1eb7df36d01b10` for `HEAD` and
  `refs/heads/master`.  This is an upstream source anchor only; this repository
  does not vendor the `flt-regular` proof body.
- `flt-regular` 中 regular primes 的定义：
  <https://github.com/leanprover-community/flt-regular/blob/master/FltRegular/NumberTheory/RegularPrimes.lean>
  exact upstream module for setup: `FltRegular.NumberTheory.RegularPrimes`;
  declaration anchors: `IsRegularNumber`, `IsRegularPrime`,
  `isPrincipal_of_isPrincipal_pow_of_coprime`.
- `flt-regular` 中 primitive solution 规整：
  <https://github.com/leanprover-community/flt-regular/blob/master/FltRegular/MayAssume/Lemmas.lean>
  exact upstream module for MayAssume: `FltRegular.MayAssume.Lemmas`;
  declaration anchors: `MayAssume.coprime`,
  `MayAssume.p_dvd_c_of_ab_of_anegc`, `a_not_cong_b`.
- `flt-regular` 的 Case I 主文件：
  <https://github.com/leanprover-community/flt-regular/blob/master/FltRegular/CaseI/Statement.lean>
  exact upstream Case I modules: `FltRegular.CaseI.Statement` and supporting
  `FltRegular.CaseI.AuxLemmas`; declaration anchors: `CaseI.SlightlyEasier`,
  `CaseI.Statement`, `CaseI.may_assume`, `CaseI.ab_coprime`,
  `CaseI.exists_ideal`, `CaseI.is_principal`, `CaseI.caseI_easier`, `CaseI.caseI`.
- `flt-regular` 的 Case II 主文件：
  <https://github.com/leanprover-community/flt-regular/blob/master/FltRegular/CaseII/Statement.lean>
  exact upstream Case II terminal module: `FltRegular.CaseII.Statement`;
  declaration anchors: `not_exists_solution`, `not_exists_solution'`,
  `not_exists_Int_solution`, `not_exists_Int_solution'`, and `caseII`.
- `flt-regular` 的 Case II 下降步骤文件：
  <https://github.com/leanprover-community/flt-regular/blob/master/FltRegular/CaseII/InductionStep.lean>
  exact upstream Case II descent module: `FltRegular.CaseII.InductionStep`;
  supporting module: `FltRegular.CaseII.AuxLemmas`; declaration anchors include
  `zeta_sub_one_dvd`, `span_pow_add_pow_eq`, `div_one_sub_zeta_mem`,
  `div_zeta_sub_one_Bijective`, `prod_c`, `exists_ideal_pow_eq_c`,
  `root_div_zeta_sub_one_dvd_gcd_spec`, `c_div_principal`, `p_dvd_c_iff`,
  `p_dvd_a_iff`, `p_pow_dvd_c_eta_zero`, `p_pow_dvd_a_eta_zero`,
  `exists_solution`, and `exists_solution'`.
- `flt-regular` upstream terminal theorem declaration:
  exact module `FltRegular.FltRegular`; theorem header at upstream commit
  `0ba4fc22e1742623c3923c5a7a1eb7df36d01b10` is
  `theorem flt_regular {p : ℕ} [Fact p.Prime] (hreg : IsRegularPrime p) (hodd : p ≠ 2) : FermatLastTheoremFor p`.
  This repository records only the module-name source anchor plus the
  `2026-04-24` `git ls-remote` command result above; `flt-regular` is not
  pinned by vendored commit, release tag, or lockfile in this repository.
  TODO before stronger reproducibility claims: add a reproducible pin for
  `leanprover-community/flt-regular` by commit or release and record the
  matching dependency state.
- Imperial College London 的公开总项目：
  <https://github.com/ImperialCollegeLondon/FLT>
- 该项目的 blueprint：
  <https://imperialcollegelondon.github.io/FLT/blueprint/>
- regular primes 情形的公开论文页面：
  <https://afm.episciences.org/16046>

## 二、已 machine-checked 部分的详细拆解

这一节专门回答“哪些部分已经被机器证明，而且到底详细到了什么程度”。
重点不是“有一个 theorem 名字存在”，而是**已经 machine-check 的数学内容到底铺到了哪一层**。

### 1. statement / reduction 层已经 machine-check 到什么程度

这部分主要在 `mathlib` 的 `Mathlib/NumberTheory/FLT/Basic.lean` 中。

已经存在的核心对象与约化工具包括：

- `FermatLastTheoremWith`
  这是“任意半环 `R`、固定指数 `n`”版本的统一陈述层。
- `FermatLastTheoremFor`
  这是自然数版本的固定指数陈述。
- `FermatLastTheorem`
  这是完整 FLT 的总陈述：对所有 `n ≥ 3` 都成立。
- `FermatLastTheoremWith.mono` 与 `FermatLastTheoremFor.mono`
  这两个结果 formalize 了“若 `m | n`，则证明 `m` 指数版本即可推出 `n` 指数版本”。
  这一步非常关键，因为它把“完整 FLT”约化成“`n = 4` 与所有奇素数指数”。
- `FermatLastTheorem.of_odd_primes`
  这条把 “`n = 4` + 所有奇素数指数” 拼回总 FLT。
- `fermatLastTheoremWith_nat_int_rat_tfae`
  这是自然数 / 整数 / 有理数三种陈述之间的 TFAE。
- `fermatLastTheoremFor_iff_int`
  这条是最常用入口，把自然数版本切换到整数版本。
- `fermatLastTheoremFor_iff_rat`
  允许切换到有理数版本。
- `fermatLastTheoremWith_of_fermatLastTheoremWith_coprime`
  把一般非零解归约到 `gcd = 1` 的 primitive solution。
- `dvd_c_of_prime_of_dvd_a_of_dvd_b_of_FLT`
  这是 `2026-04-24` 以后拆分 special case 时会重复用到的 divisibility 工具。
- `isCoprime_of_gcd_eq_one_of_FLT`
  把 `gcd = 1` 明确转成互素性结论。

把上面这些 reduction 工具合起来，就得到一个在 blueprint 中必须写明的事实：

- `4` 以上非素数指数不是独立 branch。
- 它们全部被 divisibility reduction 吸收。
- 所以真正需要独立审计的主 branch 只有：
  - `n = 4`
  - `n = 3`
  - regular primes
  - 一般奇素数指数主链

结论是：`mathlib` 不是只放了一个总 statement，而是已经把 FLT 形式化工作中最重要的**陈述规范化层**和**指数约化层**做成了稳定基础设施。

### 2. `n = 4` 已经 machine-check 到什么程度

这部分在 `Mathlib/NumberTheory/FLT/Four.lean` 中，成熟度已经很高。

它的证明不是“直接一句 finishing theorem”，而是完整铺开成了一个无限递降脚手架：

- `Fermat42`
  先把目标改写成 `a^4 + b^4 = c^2` 的无解问题。
  这是 classical paper proof 里最常见的桥梁，在 Lean 中被明确单独命名。
- `Fermat42.exists_minimal`
  若存在解，则存在 `|c|` 最小的解。
  这一步把无限递降需要的“最小反例”对象形式化了。
- `Fermat42.coprime_of_minimal`
  证明最小反例必然互素。
  这不是修辞性说明，而是完整 machine-checked 的缩放论证。
- `Fermat42.exists_odd_minimal`
  证明可进一步假设最小反例中某个变量是奇数。
- `Fermat42.exists_pos_odd_minimal`
  将最小反例规范化到“奇 + 正”的形态。
- `Fermat42.not_minimal`
  这是整条 `n = 4` 证明的核心。
  证明思路是把 `(a^2, b^2, c)` 看成 primitive Pythagorean triple，先分解出 `(m, n)`，再对 `(a, n, m)` 再做一次 primitive triple 分类，最后构造出一个更小的反例，从而和最小性矛盾。
- `not_fermat_42`
  收束成 `a^4 + b^4 ≠ c^2`。
- `fermatLastTheoremFour`
  从上一步推出 `FermatLastTheoremFor 4`。
- `FermatLastTheorem.of_odd_primes`
  再把 `n = 4` 和“所有奇素数指数”拼成完整 FLT 的标准归约框架。

因此，`n = 4` 的 machine-check 不是一个“黑箱特例证明”，而是一条完整可审计的 descent proof。

### 3. `n = 3` 已经 machine-check 到什么程度

这部分在 `Mathlib/NumberTheory/FLT/Three.lean` 中，细节远多于“已经证明 `n=3`”这句话本身。

它的结构可以分成四层：

#### 第一层：Case 1 的初等同余论证

- `cube_of_castHom_ne_zero`
- `cube_of_not_dvd`
- `fermatLastTheoremThree_case_1`

这里 formalize 的是 paper proof 中著名的模 `9` 分析：
若 `3 ∤ abc`，则每个非零立方模 `9` 只能是 `1` 或 `8`，因此 `a^3 + b^3 = c^3` 不可能成立。

#### 第二层：把一般情形约化到“只有 `c` 被 `3` 整除”

- `three_dvd_b_of_dvd_a_of_gcd_eq_one_of_case2`
- `fermatLastTheoremThree_of_dvd_a_of_gcd_eq_one_of_case2`
- `fermatLastTheoremThree_of_three_dvd_only_c`

这一段的作用是把整数解的 divisibility 结构规整到一个更可控的形态，给分圆域中的 generalized equation 做准备。

#### 第三层：把方程推广到三次分圆域中的 generalized equation

- `FermatLastTheoremForThreeGen`

它考虑的不是直接的 `a^3 + b^3 = c^3`，而是：

- `a^3 + b^3 = u * c^3`

其中 `u` 是单位，工作环境是 `ℤ[ζ₃]`。
这一步对人类读者来说可能看似“技术性绕路”，但对形式化非常关键，因为 descent 构造过程中单位因子无法避免。

#### 第四层：把 generalized equation 组织成可下降的对象，并做 multiplicity descent

- `Solution'`
  记录 generalized equation 的一个解，附带 `¬ λ ∣ a`、`¬ λ ∣ b`、`λ ∣ c`、互素性等约束。
- `Solution`
  在 `Solution'` 基础上再要求 `λ^2 ∣ a + b`。
- `Solution'.multiplicity`
  把 `λ = ζ₃ - 1` 在 `c` 中的重数做成显式自然数。
- `Solution.exists_minimal`
  在重数意义下取最小解。
- `exists_Solution_of_Solution'`
  证明可把 `Solution'` 转换为 `Solution`，同时保持重数不变。
- `Solution'_descent`
  从一个 `Solution` 构造新的 `Solution'`。
- `Solution'_descent_multiplicity_lt`
  证明新构造的对象使 multiplicity 严格下降。
- `exists_Solution_multiplicity_lt`
  从任意 `Solution` 生成一个更小的 `Solution`，与最小性矛盾。
- `fermatLastTheoremThree`
  最终收束成 `FermatLastTheoremFor 3`。

这说明 `n = 3` 的 machine-check 已经达到“完整 descent architecture”的程度，而不是只 formalize 了一个缩略 proof sketch。

### 4. regular primes 已经 machine-check 到什么程度

这部分不是 `mathlib` 主库里的一两个 theorem，而是一个独立项目 `flt-regular`，并且已经有公开发表的 2025 年论文。

它的 machine-checked 范围，至少包括以下四层：

#### 第一层：regular prime 的定义与基础

文件：

- `FltRegular/NumberTheory/RegularPrimes.lean`

核心对象：

- `IsRegularNumber`
- `IsRegularPrime`
- `isPrincipal_of_isPrincipal_pow_of_coprime`

这一步不是背景知识而已。
regular prime 的核心形式化意义在于：若 `p` 与 class group 的基数互素，则“某个 ideal 的 `p` 次幂为 principal”能推出“该 ideal 本身 principal”。
这正是 Kummer 路线能 formalize 下去的 algebraic engine。

#### 第二层：把任意非平凡整数解先规整到 primitive solution

文件：

- `FltRegular/MayAssume/Lemmas.lean`

核心结果：

- `MayAssume.coprime`
- `a_not_cong_b`

它们负责把原始方程归整到：

- `gcd = 1`
- 非零性保持
- 在 Case I 中还要进一步规避 `a ≡ b (mod p)` 的坏情形

这一步解决的是“paper proof 中默认可以 assume 的条件，在 Lean 里必须显式证明”的工程问题。

#### 第三层：Case I 的完整 machine-check

文件：

- `FltRegular/CaseI/Statement.lean`
- `FltRegular/CaseI/AuxLemmas.lean`

主线结果：

- `CaseI.SlightlyEasier`
- `CaseI.Statement`
- `CaseI.may_assume`
- `exists_ideal`
- `is_principal`
- `ex_fin_div`
- `caseI_easier`
- `caseI`

这一条线的数学内容大意是：

1. 先把 `a^p + b^p = c^p` 写进 `p` 次分圆域的整数环中。
2. 对 `a + ζb` 生成的 ideal 做 `p` 次幂分解。
3. 用 regular prime 条件把“`I^p` principal”反推成 “`I` principal”。
4. 从 principal 化得到一个更强的 cyclotomic divisibility 结论。
5. 再通过有限和 / 系数整除等手段回到整数层，制造矛盾。

这不是“只验证了 Case I 的 statement”，而是已经 machine-check 到 principal ideal、ideal factorization、有限和整除的具体桥接环节。

#### 第四层：Case II 的完整 machine-check

文件：

- `FltRegular/CaseII/Statement.lean`
- `FltRegular/CaseII/InductionStep.lean`
- `FltRegular/CaseII/AuxLemmas.lean`

主线结果：

- `not_exists_solution`
- `not_exists_solution'`
- `not_exists_Int_solution`
- `not_exists_Int_solution'`
- `caseII`

这一条线 formalize 的是 Kummer 路线中更技术性的 infinite descent：

1. 在分圆域整数环里考虑 `ζ - 1` 的整除层级。
2. 从 `z = (ζ - 1)^m z'` 出发构造更小的解。
3. 用归纳或 well-founded 下降证明这样的解链不可能无限存在。
4. 再把结论拉回到整数方程层，排除 `p ∣ abc` 的情形。

因此，regular primes 这部分也不是“抽象地证明了一个 case”，而是已经有可逐文件审计的 Case I / Case II 完整机器证明。

### 5. 这些 machine-checked 部分合起来到底意味着什么

把上面四层合起来，截至 `2026-04-24` 已经被机器证明的内容远比“`n = 3`、`n = 4`、`regular primes`”这句摘要更扎实：

1. FLT 的陈述层与关键归约层已经在 `mathlib` 中稳定存在。
2. `n = 4` 不是黑箱，而是完整无限递降 proof。
3. `n = 3` 不是黑箱，而是带 generalized equation 和 multiplicity descent 的完整 proof architecture。
4. regular primes 不是概念性声明，而是分成 `MayAssume + Case I + Case II + main theorem flt_regular` 的完整工程。

因此，`THM-M-0387` 在本仓库里不应只用一句“部分验证”笼统概括，而应明确表述成：

> statement / reduction 层、`n = 4`、`n = 3`、`regular primes` 已有实质性且可追踪的 machine-checked 结果；缺失的是完整 Taylor-Wiles / Wiles 主证明链的公开完工版本。

### 6. 本次核查使用的主要资料

本次补充优先使用了 primary sources：

- `mathlib` 文档与源码：
  - <https://leanprover-community.github.io/mathlib4_docs/Mathlib/NumberTheory/FLT/Basic.html>
  - <https://leanprover-community.github.io/mathlib4_docs/Mathlib/NumberTheory/FLT/Four.html>
  - <https://leanprover-community.github.io/mathlib4_docs/Mathlib/NumberTheory/FLT/Three.html>
- `flt-regular` 项目源码与 README：
  - <https://github.com/leanprover-community/flt-regular/blob/master/README.md>
  - <https://github.com/leanprover-community/flt-regular/blob/master/FltRegular/FltRegular.lean>
  - <https://github.com/leanprover-community/flt-regular/blob/master/FltRegular/NumberTheory/RegularPrimes.lean>
  - <https://github.com/leanprover-community/flt-regular/blob/master/FltRegular/MayAssume/Lemmas.lean>
  - <https://github.com/leanprover-community/flt-regular/blob/master/FltRegular/CaseI/Statement.lean>
  - <https://github.com/leanprover-community/flt-regular/blob/master/FltRegular/CaseII/Statement.lean>
  - <https://github.com/leanprover-community/flt-regular/blob/master/FltRegular/CaseII/InductionStep.lean>
- 公开项目状态页与论文页：
  - <https://github.com/ImperialCollegeLondon/FLT>
  - <https://imperialcollegelondon.github.io/FLT/blueprint/>
  - <https://afm.episciences.org/16046>

### 7. theorem-level 机器证明审计表

下面这张表专门回答一个更严格的问题：

> 已 machine-checked 的，到底是“某个名字存在”，还是“整条证明链已经被拆成可追踪 theorem/lemma graph”？

表中 `Mathlib/...` 行的 source project 均为 `leanprover-community/mathlib4`
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`；`FltRegular/...`
行的 source project 为上游 `leanprover-community/flt-regular`，不是本仓库 vendored proof。

| 分层 | 代码位置 | 关键 theorem / structure | 机器证明内容 | 备注 |
|---|---|---|---|---|
| statement | `Mathlib/NumberTheory/FLT/Basic.lean` | `FermatLastTheoremWith` | 一般半环上固定指数 FLT 陈述 | 统一 statement layer |
| statement | `Mathlib/NumberTheory/FLT/Basic.lean` | `FermatLastTheoremFor` | 自然数版本固定指数陈述 | 供特例直接调用 |
| statement | `Mathlib/NumberTheory/FLT/Basic.lean` | `FermatLastTheorem` | 全部 `n ≥ 3` 的总陈述 | 顶层目标 |
| reduction | `Mathlib/NumberTheory/FLT/Basic.lean` | `FermatLastTheoremWith.mono` | `m ∣ n` 时由指数 `m` 推指数 `n` | 全证明约化核心 |
| reduction | `Mathlib/NumberTheory/FLT/Basic.lean` | `fermatLastTheoremFor_iff_int` | `ℕ` 与 `ℤ` 版本切换 | 特例证明常走整数版 |
| reduction | `Mathlib/NumberTheory/FLT/Basic.lean` | `fermatLastTheoremFor_iff_rat` | `ℕ` 与 `ℚ` 版本切换 | 陈述等价层 |
| reduction | `Mathlib/NumberTheory/FLT/Basic.lean` | `fermatLastTheoremWith_of_fermatLastTheoremWith_coprime` | 约化到 primitive solution | 不是纸面省略，而是 formalized |
| reduction | `Mathlib/NumberTheory/FLT/Basic.lean` | `dvd_c_of_prime_of_dvd_a_of_dvd_b_of_FLT` | 素数整除传播 | 多个 special case 复用 |
| reduction | `Mathlib/NumberTheory/FLT/Basic.lean` | `isCoprime_of_gcd_eq_one_of_FLT` | `gcd = 1` 推互素 | primitive 入口 |
| special case | `Mathlib/NumberTheory/FLT/Four.lean` | `Fermat42` | 改写为 `a^4 + b^4 = c^2` 无解问题 | 无限递降桥梁 |
| special case | `Mathlib/NumberTheory/FLT/Four.lean` | `Fermat42.exists_minimal` | 取得最小反例 | descent 起点 |
| special case | `Mathlib/NumberTheory/FLT/Four.lean` | `Fermat42.coprime_of_minimal` | 最小反例互素 | 缩放论证已 formalized |
| special case | `Mathlib/NumberTheory/FLT/Four.lean` | `Fermat42.exists_pos_odd_minimal` | 规整到奇 + 正的最小反例 | 分类论证前提 |
| special case | `Mathlib/NumberTheory/FLT/Four.lean` | `Fermat42.not_minimal` | 构造更小反例并矛盾 | `n = 4` 核心证明 |
| special case | `Mathlib/NumberTheory/FLT/Four.lean` | `not_fermat_42` | 排除 `a^4 + b^4 = c^2` | 由核心步骤收束 |
| special case | `Mathlib/NumberTheory/FLT/Four.lean` | `fermatLastTheoremFour` | 得到 `FermatLastTheoremFor 4` | `n = 4` 最终结果 |
| special case | `Mathlib/NumberTheory/FLT/Three.lean` | `fermatLastTheoremThree_case_1` | `3 ∤ abc` 的 mod `9` 无解 | 初等分支 |
| special case | `Mathlib/NumberTheory/FLT/Three.lean` | `fermatLastTheoremThree_of_three_dvd_only_c` | 规整到只有 `c` 被 `3` 整除 | 进入分圆域前归整 |
| special case | `Mathlib/NumberTheory/FLT/Three.lean` | `FermatLastTheoremForThreeGen` | generalized equation 陈述 | 单位因子显式进入 |
| special case | `Mathlib/NumberTheory/FLT/Three.lean` | `Solution'` / `Solution` | 下降所需不变量打包 | formal descent 对象 |
| special case | `Mathlib/NumberTheory/FLT/Three.lean` | `exists_Solution_of_Solution'` | `Solution' → Solution` 且保持重数 | 下降准备 |
| special case | `Mathlib/NumberTheory/FLT/Three.lean` | `exists_Solution_multiplicity_lt` | multiplicity 严格下降 | `n = 3` 核心矛盾 |
| special case | `Mathlib/NumberTheory/FLT/Three.lean` | `fermatLastTheoremThree` | 得到 `FermatLastTheoremFor 3` | `n = 3` 最终结果 |
| generalization | `FltRegular/NumberTheory/RegularPrimes.lean` | `IsRegularPrime` | regular prime 的形式化定义 | class group 视角 |
| generalization | `FltRegular/NumberTheory/RegularPrimes.lean` | `isPrincipal_of_isPrincipal_pow_of_coprime` | principal ideal 反推引擎 | regular 路线关键 |
| generalization | `FltRegular/MayAssume/Lemmas.lean` | `MayAssume.coprime` | 任意解规整到 primitive solution | “可无损假设”的 formal version |
| generalization | `FltRegular/MayAssume/Lemmas.lean` | `a_not_cong_b` | Case I 中排除坏同余情形 | 进入 Case I 更强条件 |
| generalization | `FltRegular/CaseI/Statement.lean` | `CaseI.Statement` / `caseI` | 排除 `p ∤ abc` 的 regular primes 情形 | Kummer 路线 Case I |
| generalization | `FltRegular/CaseII/Statement.lean` | `not_exists_solution` / `caseII` | 排除 `p ∣ abc` 的 regular primes 情形 | Kummer 路线 Case II |
| generalization | `FltRegular/FltRegular.lean` | `flt_regular` | 合并 Case I / II 得 `FermatLastTheoremFor p` | regular primes 总结果 |

### 8. 机器证明“过程层”审计

如果只写“`n = 4` 已验证”，信息量也不够。
真正有用的是把“过程层”也审计清楚。

#### 8.1 `n = 4` 过程层

`Mathlib/NumberTheory/FLT/Four.lean` 的证明流水线大致是：

1. 用 `Fermat42` 重述问题。
2. 用 `exists_minimal` 构造最小反例。
3. 用 `coprime_of_minimal` 与 parity 规整把反例化到最利于分类的形态。
4. 用 primitive Pythagorean triple 分类拆出 `(m, n)`。
5. 再做第二轮 triple 分类，逐步抽出平方与四次方结构。
6. 构造严格更小的 `Fermat42` 反例。
7. 用 `not_minimal` 与最小性矛盾。
8. 收束到 `not_fermat_42`，再收束到 `fermatLastTheoremFour`。

如果按“机器证明留痕优先”的标准细分，
截至 `2026-04-24`，这条线最值得单列的下一层节点是：

1. `bridge packaging`
   也就是 `Fermat42`、`not_fermat_42`、`fermatLastTheoremFour` 之间的桥梁层。
2. `minimal normalization`
   也就是 `exists_minimal`、`coprime_of_minimal`、`exists_pos_odd_minimal` 这一组最小反例规整节点。
3. `PythagoreanTriple.coprime_classification'`
   第一轮和第二轮参数化共用的 formal 入口。
4. `Int.isCoprime_of_sq_sum` / `Int.isCoprime_of_sq_sum'`
   从和平方结构过渡到因子互素的桥接层。
5. `Int.sq_of_gcd_eq_one`
   从“互素乘积是平方”推回“各因子是平方”的核心抽取器。
6. `hic`, `hic'`
   新解严格更小的最终比较链。

也就是说，`n = 4` 截至 `2026-04-24` 已经不只是“`not_minimal` 很重要”，
而是已经能进一步定位到哪几个 formal hook 才是真正的高负载 leaf。

按 `2026-04-24` 仓库内的统一 package 口径，
`n = 4` 这一分支截至 `2026-04-24` 已拆成 `7` 个 package，
并且这 `7` 个 package 在：

- `machine_checked_audit.md`
- `process_audit.md`
- `eligibles/n4_proof_process.md`

三层材料里都已对齐命名。

#### 8.2 `n = 3` 过程层

`Mathlib/NumberTheory/FLT/Three.lean` 的证明流水线可以分成：

1. Case 1：mod `9` 排除 `3 ∤ abc`。
2. Case 2 整数层规整：把情形压缩到 `3 ∣ c` 而 `3 ∤ a,b`。
3. 进入 `ℤ[ζ₃]`，把方程泛化为 `a^3 + b^3 = u * c^3`。
4. 用 `Solution'` / `Solution` 明确记录 “`λ = ζ₃ - 1` 的整除 / 不整除 / 重数” 这些下降不变量。
5. 用 `exists_Solution_of_Solution'` 保证 generalized solution 可以转成适于下降的 solution。
6. 定义 multiplicity，并在其上取最小解。
7. 构造 `Solution'_descent`，证明 multiplicity 严格下降。
8. 用 `exists_Solution_multiplicity_lt` 和最小性矛盾。
9. 收束到 `fermatLastTheoremThree`。

在仓库写作粒度上，这一分支不再向“互素”“整除传播”那种大学初等数论基础层细拆；
默认读者可以把这些预备动作作为背景能力处理。

#### 8.3 regular primes 过程层

`flt-regular` 项目里的流水线则是：

1. `RegularPrimes.lean` 定义 regular prime，并给出 ideal principalization engine。
2. `MayAssume/Lemmas.lean` 把整数解规整成 primitive solution，并在 Case I 中进一步规整同余条件。
3. `CaseI/Statement.lean` 用分圆域 ideal factorization 与 principalization 排除 `p ∤ abc`。
4. `CaseII/Statement.lean` 与 `InductionStep.lean` 用 `ζ - 1` 的幂次下降排除 `p ∣ abc`。
5. `FltRegular.lean` 合并 Case I / II，得到 `flt_regular`。

按机器证明过程细分一层时，
截至 `2026-04-24` 最值得优先留痕的是：

1. `MayAssume.coprime`、`MayAssume.p_dvd_c_of_ab_of_anegc`、`a_not_cong_b`
   固定 primitive solution 与 Case I / Case II 的标准入口。
2. `exists_ideal`
   把 Case I 的线性因子 ideal 明确写成 `p` 次幂 ideal。
3. `is_principal_aux` / `is_principal`
   用 regularity 把 ideal-level 信息拉回 element-level。
4. `exists_solution` / `exists_solution'`
   把 Case II 的 level `m+1` 解下降到 level `m`。
5. `not_exists_solution` / `not_exists_Int_solution`
   取最小 `m` 并完成 Case II 收束。

也就是说，regular primes 这条线截至 `2026-04-24` 已经从“`caseI` / `caseII` 两个 theorem 名”推进到了：

- `MayAssume`
- `Case I ideal extraction`
- `Case I principalization`
- `Case II descent core`
- `Case II close / merge`

这套可细分的机器节点层。

按 `2026-04-24` 仓库内的统一 package 口径，
regular primes 这一分支截至 `2026-04-24` 已拆成 `11` 个 package；
其中 theorem/process audit 命名在：

- `machine_checked_audit.md`
- `process_audit.md`
- `eligibles/regular_primes_proof_process.md`

三层材料里已对齐命名。
公开完成状态以本文件的 `Execution Checklist` 为准；`FLT-HR-018` 的公开合并目标
`eligibles/regular_primes_proof_process.md` 已补齐 human expansion 与 local ledger，
所以它在 `2026-04-24` 公开状态中是 `completed` / `Completion Gate = passed`。

把这两条加起来，截至 `2026-04-24`，围绕 `THM-M-0387` 已细化并完成公开归档闸门的 package 总数是：

- `n = 4`：`7`
- `regular primes`：`11`
- 合计：`18`

需要按统一口径记录：
上述 `18` 个 canonical package 已经各自达到 `completed` / `Completion Gate = passed`，并拥有独立 `<=100` proof-step ledger；
`FLT-HR-018 / Case II close and merge` 的完成只表示公开人类可读展开与本地预算账本已经补齐，不表示本仓库 vendoring 上游 `flt_regular` 证明本体。

跨文件统一保持不变的 canonical high-risk leaf 名为：

- `n = 4`
  - `raw coprime triple classification`
  - `square extraction for r*s with sign cleanup`
  - `strict natAbs descent hic`
- regular primes
  - `Case II ideal-factor layer / global product to local p-th powers`
  - `Case II distinguished root / p_pow_dvd_c_eta_zero`
  - `Case II descent core / three-root formula and raw descent`
  - `Case II close / merge / not_exists_solution'`

先前曾单列但截至 `2026-04-24` 已随 package ledger 一并关闭的 package-level subitem 为：

- `Int.gcd a n = 1 transfer`
- `exists_ideal pairwise ideal coprimality interface`
- `caseI_easier / aux-index exclusion`

另外，`eligibles` 中面向读者的 layer label / budget alias 只作为讲解用 alias，
不构成第二套 canonical node 名；
`eligibles/n4_proof_process.md` 第 `16` 节的 budget alias 与
`eligibles/regular_primes_proof_process.md` 第 `14.1` 节的可读层标签，
都在 `2026-04-24` 口径下回映到上面这套 canonical package / high-risk leaf 名称。

其中：

- 截至 `2026-04-24`，`n = 4` 的三条 canonical high-risk leaf 都已由独立 ledger 完整关闭，
  且各自 one-more-depth 子层也随 parent ledger 一并纳入该 closed leaf 记录。
- regular primes 的四条 canonical high-risk leaf 都已由独立 ledger 完整关闭，
  其中 `Case II close / merge / not_exists_solution'` 由 `FLT-HR-018` 的 `34` 步 local ledger 关闭。
  theorem-boundary sentence 固定为
  `upstream theorem closure: yes / repo-local vendored theorem closure: no, anchor-only / repo-local anchor-only statement/module/theorem-name record: yes`。

因此，截至 `2026-04-24`，公开归档层闭合到 `18/18`；
`2026-04-24` 之后若增补，只属于解释层扩写，不改变 `2026-04-24` acceptance 结论。

## 三、形式化验证样例

### 样例目标

这个样例不试图伪装成“完整 FLT 已经在本仓库本地跑通”，因为 `THM-M-0387/` 目录在 `2026-04-24` 并不是一个 Lean 工程。
样例的目标是更严格也更有价值的：

1. 直接复用上游 `mathlib` 中已经真实存在的 theorem 名称。
2. 展示仓库如何把“陈述、约化、局部完成结果、总目标”拼成一个可执行研究对象。
3. 给 `2026-04-24` 以后把本仓库接成正式 Lean 项目时提供零歧义入口。

### Lean 样例文件

截至 `2026-04-24`，本条目采用“theorem dossier + repo-level Lean 共享源码树”的结构：

- `THM-M-0387/FermatLastTheorem_Sample.lean`
  本条目 dossier-local 的 Lean 入口。
- `Formalizations/Lean/AwesomeTheorems.lean`
  共享 Lean 库根模块。
- `Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/FLT4Path.lean`
  `n = 4` 路线模块。
- `Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/FLT3Path.lean`
  `n = 3` 路线模块。
- `Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/RegularPrimesPath.lean`
  regular primes 路线锚点模块。
- `Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/Sample.lean`
  聚合入口模块；本地验证时与三条路径模块一起被 build。

对应地，截至 `2026-04-24`，`lakefile.lean` 与 `lean-toolchain` 位于 `Formalizations/Lean/`，
不再让单个 theorem folder 兼任仓库级 Lean 源码根。

本地验证状态以 `THM-M-0387/build_validation.md` 为准。截至 `2026-04-24 22:10:48 CST (+0800)`，
规范重跑命令为 `bash THM-M-0387/run_local_validation.sh`，该重跑失败且退出码为 `1`，
失败原因是本地 `awesome-theorems-local` 工具链缺少
`/Users/wangweiyang/.elan/toolchains/awesome-theorems-local/bin/lake`。
因此，本节不声称 `2026-04-24 22:10:48 CST (+0800)` 环境可复现通过；早于该时间的成功 build、
Lean version、toolchain name、模块清单与 `FermatLastTheorem_Sample.lean` file-check 只作为历史通过记录。
脚本文件在 `2026-04-24` 文档约定中不要求可执行位，公开文档统一使用 `bash THM-M-0387/run_local_validation.sh` 调用。
本地验证前提是 `Formalizations/Lean/lean-toolchain` 选择的自定义工具链 `awesome-theorems-local`
同时提供可用的 `lake` 与 `lean` 二进制；只存在 `elan` 外壳不足以完成验证。
`.lake/`、Lake build outputs、elan/toolchain downloads、dependency caches 与其他本机缓存不是 tracked artifacts，
也不是公开稳定证据；公开验证证据以 `THM-M-0387/build_validation.md` 中记录的命令、结果、版本和边界说明为准。

内容如下：

```lean
import Mathlib.NumberTheory.FLT.Basic
import AwesomeTheorems.NumberTheory.THM_M_0387.FLT4Path
import AwesomeTheorems.NumberTheory.THM_M_0387.FLT3Path
import AwesomeTheorems.NumberTheory.THM_M_0387.RegularPrimesPath

open AwesomeTheorems.NumberTheory.THM_M_0387

example : FermatLastTheoremFor 4 := flt4Path

example : FermatLastTheoremFor 3 := flt3Path

example : FermatLastTheoremWith ℤ 4 := flt4IntPath

example : FermatLastTheoremFor 8 := flt8ViaFlt4Path

example
    (hodd : ∀ p : ℕ, Nat.Prime p → Odd p → FermatLastTheoremFor p) :
    FermatLastTheorem :=
  FermatLastTheorem.of_odd_primes hodd
```

这个样例说明了四个关键事实：

1. `n = 4` 与 `n = 3` 的 repo-local wrapper `flt4Path`、`flt3Path` 已经能被直接调用，证明实质来自 mathlib import。
2. `mathlib` 已经把自然数陈述和整数陈述打通，因此 `flt4IntPath` 可由 `fermatLastTheoremFor_iff_int` 作为 repo-local 派生 wrapper 给出。
3. 指数可通过整除关系上推，因此 `flt8ViaFlt4Path` 可由 `FermatLastTheoremFor.mono` 与 `4 | 8` 的指数整除单调性给出。
4. regular primes 路线在本仓库共享树里只有独立锚点模块，便于 `2026-04-24` 以后接入 `flt-regular`；theorem closure 属于上游，不是 repo-local vendored closure。Regular primes boundary: upstream theorem closure yes; repo-local vendored theorem closure no, anchor-only; repo-local anchor-only statement/module/theorem-name record yes。
5. `FermatLastTheorem.of_odd_primes` 展示“证明所有奇素数指数”加上 `n = 4` 即可推出完整 FLT 的任务分解；它不表示完整 FLT 已在本仓库 repo-local machine-check 闭合。

## 四、对本仓库的执行建议

如果把费马大定理作为本仓库的长期 formalization benchmark，建议按以下顺序推进：

1. 固化 `THM-M-0387` 的结构化字段，不再把总体状态写成 `已验证`。
2. 保留一个专题研究文档，避免把所有细节硬塞回大蓝图。
3. 把“样例代码”与“研究结论”分开：代码只展示真实已存在入口，研究文档负责证明链与阻塞点。
4. 截至 `2026-04-24` 的建议是把更多定理接入 `Formalizations/Lean/` 这棵共享源码树，而不是回退到 theorem-local 源码根。

## 五、结论

费马大定理非常适合做本仓库的“形式化验证研究样板条目”，因为它同时覆盖了：

- 简洁陈述
- 漫长历史
- 初等特例证明
- 现代高阶数论主证明
- 局部 machine-checked 成果
- 大型协作 formalization 项目

从仓库治理角度，最重要的不是把它误写成“已完成”，而是准确表达：

> 截至 `2026-04-24`，这是一个已经有坚实 machine-checked 前沿、但完整总证明尚未形成 repo-local machine-check 闭合的旗舰级形式化目标。
