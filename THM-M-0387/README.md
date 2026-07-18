# THM-M-0387 费马大定理

本目录是 `THM-M-0387` 的旗舰物料目录。

目标不是只保存一篇长文，而是把“形式化验证 + 机器证明边界记录（可证明部分）”条目可直接复用的结构固定下来。

截至 `2026-07-10`，本目录是历史 theorem dossier。唯一 requirements、排序和执行进度权威是
`Docs/Stage1_Blueprint_v2.md`；旧 assurance 文档只作为 Git 历史 provenance，
`proof_units.json` 是可重算的历史 proof-tree/debt manifest，而 `full_study.md`
中的旧 checklist 仅是历史 readability inventory。
`bash THM-M-0387/run_local_validation.sh` 是本地统一验证入口；
但该验证只覆盖本仓库中实际纳入 Lean 工程的 wrappers、pinned dependencies 与样例入口，不表示完整 FLT
已经在本仓库完成 repo-local formal closure。
总体状态仍是 `部分验证`，而不是全局 `已验证`。

历史 dossier 的最终可重算覆盖率为：tree classification `132/132 (100%)`，
machine closure `29/93 (31.18%)`，readable closure `132/132 (100%)`，
human-source `H0` closure `0/113 (0%)`。最后一项为零并不否定 FLT 的历史证明；
它表示本轮没有把 primary-paper 的精确 section/theorem/page 与每个需要审计的 node
完成逐项 statement/assumption crosswalk，因此全部节点保守保留 `H1`。exact root
仍是 `[H1, M2, R0]`，`root_machine_closed = false`。

Lean 4-only rule: this dossier treats a branch as completed only when it has a
Lean 4 theorem/module/check path in this repository validation closure, a
pinned mathlib Lean 4 theorem wrapped and checked locally, or a pinned external
Lean 4 dependency checked through a repo-local wrapper. External Lean 4 URLs or
theorem names alone are not an acceptable completed state; if such a branch is
found, it is a repo-local integration blocker until pinned/imported/checked.

Machine-checked boundary: `n = 4` 通过 `Mathlib.NumberTheory.FLT.Four` import 与 wrapper theorem
`flt4Path` 记录 repo-local theorem-level closure；`n = 3` 通过 `Mathlib.NumberTheory.FLT.Three`
import 与 wrapper theorem `flt3Path` 记录 repo-local theorem-level closure；`flt4IntPath` 是由
mathlib `fermatLastTheoremFor_iff_int` 等价推出的 repo-local 派生 wrapper；`flt8ViaFlt4Path` 是由
`FermatLastTheoremFor.mono` 与 `4 ∣ 8` 的指数整除单调性推出的 repo-local 派生 wrapper。
`regularPrimesPath` 是由 pinned `leanprover-community/flt-regular` dependency 的 terminal theorem
`flt_regular` 推出的 repo-local wrapper；该 dependency 固定在
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`，与本仓库 Lean `4.29.0` 和 mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` 对齐。
本地 Lean 工程 pin `leanprover-community/mathlib4` revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`；`FermatLastTheoremFor`、
`FermatLastTheorem` 与 transports/monotonicity lemmas 的 exact module 是
`Mathlib.NumberTheory.FLT.Basic`；conditional root assembly
`FermatLastTheorem.of_odd_primes` 位于 `Mathlib.NumberTheory.FLT.Four`。
完整 `FermatLastTheorem` 不是本仓库 repo-local machine-checked theorem；regular primes theorem closure
现在已经通过 pinned external dependency 纳入本仓库 validation closure，但这仍只覆盖 regular primes branch，
不补齐所有奇素数指数或 Wiles/Taylor-Wiles 主线。

## 目录内容

本节列出的 tracked 文件与目录是 `THM-M-0387` 的公开阅读面；`meta.json`
是机器可读 contract，`full_study.md` 是人类可读主线，审计、验证记录与 `eligibles/`
提供对应证据或 appendix-style 展开稿。
本目录不使用独立 `human_steps/`、result-log 目录、自动化工作副本、临时 closeout blueprint
或第二套进度文档作为公开材料面。

- `README.md`
  入口与导航。
- `proof_outline.md`
  Lean 4 anchored 短证明路线图；默认人类阅读入口。
- `proof_units.json`
  历史 schema-complete proof DAG、H/M/R ledger、证据边界与四项 coverage metrics。
- `full_study.md`
  special-branch expanded Lean 4 reconstruction study；不是进度权威。
- `machine_checked_audit.md`
  theorem-level 机器证明审计。
- `process_audit.md`
  branch-wise 证明过程审计。
- `readable/`
  Wiles/Taylor-Wiles 人类可读递归展开与外部候选/source ledger。
- `eligibles/`
  三个分支的人类可读长附录；regular primes 的定理闭合来自 pinned 上游 `flt-regular` dependency，
  并由本仓库 wrapper theorem `regularPrimesPath` 检查。
  `n = 4` 与 `regular primes` 的旧版 execution units 保留为公开展开材料；其 legacy
  completion wording 只说明旧版归档，不改变任何历史 H/M/R vector。
- `build_validation.md`
  本仓库本地 Lean 工程验证记录。
- `FermatLastTheorem_Sample.lean`
  本条定理 dossier-local Lean 入口。
- `run_local_validation.sh`
  统一本地验证脚本；规范调用方式是从仓库根目录执行 `bash THM-M-0387/run_local_validation.sh`。
- `meta.json`
  机器可读元数据、folder contract 与 per-branch formalization status。

## 导航

- [Lean 4 Proof Outline](./proof_outline.md)
- [Proof Units Manifest](./proof_units.json)
- [总研究文档](./full_study.md)
- [机器证明审计](./machine_checked_audit.md)
- [过程审计](./process_audit.md)
- [Machine-Closed Nodes](./readable/machine_closed_nodes.md)
- [Wiles/Taylor-Wiles Process](./readable/wiles_taylor_wiles_process.md)
- [External Candidate Ledger](./readable/external_candidate_ledger.md)
- [Eligible Derivatives](./eligibles/README.md)
- [构建与验证记录](./build_validation.md)
- [Lean 样例](./FermatLastTheorem_Sample.lean)
- [共享 Lean 库根模块](../Formalizations/Lean/AwesomeTheorems.lean)
- [共享 Lean 聚合模块](../Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/Sample.lean)
- [共享 Lean statement/reduction 路径模块](../Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/StatementAndReductionPath.lean)
- [共享 Lean `n = 4` 路径模块](../Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/FLT4Path.lean)
- [共享 Lean `n = 3` 路径模块](../Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/FLT3Path.lean)
- [共享 Lean regular primes 路径模块](../Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/RegularPrimesPath.lean)
- [共享 Lean small exponents 路径模块](../Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/SmallExponentsPath.lean)
- [Wiles/Taylor-Wiles 长路线](./readable/wiles_taylor_wiles_process.md)
- [外部候选账本](./readable/external_candidate_ledger.md)
- [本地验证脚本](./run_local_validation.sh)
- [Lean-aware lint 脚本](../scripts/lint_theorem_dossier.py)
- [元数据](./meta.json)

## 模板定位

截至 `2026-07-10`，这个目录承担两个角色：

1. `THM-M-0387` 的专属材料包。
2. 其他旗舰定理条目的标准范式。

因此，这个目录的结构本身就是模板，不只是内容模板。默认阅读路径保持轻量：
先读 `README.md`、`proof_outline.md` 与 `meta.json`，再读 `machine_checked_audit.md` 的边界表；
`full_study.md` 和 `eligibles/` 是需要展开数学过程时再进入的正文与长附录。

`Docs/case_studies/fermat_last_theorem_formalization_study.md` 若保留，只作为兼容跳转入口；
本条目的权威正文与审计材料以 `THM-M-0387/` 目录为准。

本仓库把 Lean 正式源码树放在 repo-level 共享目录 `Formalizations/Lean/`；
`THM-M-0387/` 本身只承担 dossier、审计、研究与验证入口角色。

Lean 4 anchored special-branch 展开稿收在 `THM-M-0387/eligibles/`；完整现代证明路线与
machine-open blocker 读法收在 `THM-M-0387/readable/`。旧 execution unit 状态不再作为
历史 cursor；蓝图 checklist 是唯一 cursor。

## 本地验证

本地验证状态以 [`build_validation.md`](./build_validation.md) 为准。规范命令是：

```bash
bash THM-M-0387/run_local_validation.sh
```

它构建所有 THM-M-0387 modules、Stage1 wrapper 与 aggregator，检查 dossier sample，
再执行 graph/type/axiom/placeholder/pin/body-location/public-surface lint。最新结果、版本与
精确输出记录在 `build_validation.md`；job count 不作为 coverage metric。

通过结果证明本仓库声明的 M0387 Lean wrappers、pinned dependency bodies、共享聚合模块和
`FermatLastTheorem_Sample.lean` 在本地工程中可复现检查；lint 从 `proof_units.json`
生成 exact-type 和 axiom probes，而不只检查 bare symbol existence。
它不改变完整
`FermatLastTheorem` 尚未 repo-local 闭合的边界。
`.lake/`、Lake build outputs、elan/toolchain downloads、dependency caches 与其他本机缓存不是 tracked artifacts，
公开证据以 `build_validation.md` 中记录的命令、结果、版本和边界说明为准。
