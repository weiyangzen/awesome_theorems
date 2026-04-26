# THM-M-0387 费马大定理

本目录是 `THM-M-0387` 的旗舰物料目录。

目标不是只保存一篇长文，而是把“形式化验证 + 机器证明边界记录（可证明部分）”条目可直接复用的结构固定下来。

截至 `2026-04-24 13:31:15 CST (+0800)`，本目录是 blueprint-first / status-first 的 theorem dossier：
`full_study.md` 的 `Execution Checklist` 是权威进度面；除非 `2026-04-24` 之后的公开验证记录证明完整 repo-local formal closure，
本文档不声称完整 FLT 已在本仓库本地闭合。
总体状态固定为 `部分验证 / 截至 2026-04-24 未完成完整 repo-local machine-check`，而不是全局 `已验证`。

Machine-checked boundary: `n = 4` 通过 `Mathlib.NumberTheory.FLT.Four` import 与 wrapper theorem
`flt4Path` 记录 repo-local theorem-level closure；`n = 3` 通过 `Mathlib.NumberTheory.FLT.Three`
import 与 wrapper theorem `flt3Path` 记录 repo-local theorem-level closure；`flt4IntPath` 是由
mathlib `fermatLastTheoremFor_iff_int` 等价推出的 repo-local 派生 wrapper；`flt8ViaFlt4Path` 是由
`FermatLastTheoremFor.mono` 与 `4 ∣ 8` 的指数整除单调性推出的 repo-local 派生 wrapper。
本地 Lean 工程 pin `leanprover-community/mathlib4` revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`；`FermatLastTheoremFor`、
`FermatLastTheorem` 与 reduction lemmas 的 exact module 是
`Mathlib.NumberTheory.FLT.Basic`。
完整 `FermatLastTheorem` 不是本仓库 repo-local machine-checked theorem；regular primes theorem closure
来自上游 `flt-regular`，本仓库不 vendoring 证明本体，只保留 anchor-only statement/module/theorem-name 记录。
`RegularPrimesPath.lean` 是 statement-shape 与 upstream-anchor 代码，不是本仓库对 `flt_regular` 的本地证明。

## 目录内容

- `README.md`
  入口与导航。
- `full_study.md`
  权威总研究正文。
- `machine_checked_audit.md`
  theorem-level 机器证明审计。
- `process_audit.md`
  branch-wise 证明过程审计。
- `eligibles/`
  三个分支的人类可读展开稿；regular primes 的定理闭合来自上游 `flt-regular`，本仓库只保留 anchor-only 记录。
  截至 `2026-04-24`，`n = 4` 与 `regular primes` 的 execution unit 已有 `18/18` 个公开归档面达到 `completed` / `Completion Gate = passed`；
  但这只是公开人类可读展开与本地预算账本完成，不改变完整 FLT 在本仓库 repo-local machine-check 未闭合的边界。
- `build_validation.md`
  本仓库本地 Lean 工程验证记录。
- `FermatLastTheorem_Sample.lean`
  本条定理 dossier-local Lean 入口。
- `run_local_validation.sh`
  统一本地验证脚本；规范调用方式是从仓库根目录执行 `bash THM-M-0387/run_local_validation.sh`。
- `meta.json`
  机器可读元数据。

## 导航

- [总研究文档](./full_study.md)
- [机器证明审计](./machine_checked_audit.md)
- [过程审计](./process_audit.md)
- [Eligible Derivatives](./eligibles/README.md)
- [构建与验证记录](./build_validation.md)
- [Lean 样例](./FermatLastTheorem_Sample.lean)
- [共享 Lean 库根模块](../Formalizations/Lean/AwesomeTheorems.lean)
- [共享 Lean 聚合模块](../Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/Sample.lean)
- [共享 Lean `n = 4` 路径模块](../Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/FLT4Path.lean)
- [共享 Lean `n = 3` 路径模块](../Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/FLT3Path.lean)
- [共享 Lean regular primes 路径模块](../Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/RegularPrimesPath.lean)
- [本地验证脚本](./run_local_validation.sh)
- [元数据](./meta.json)

## 2026-04-24 定位

截至 `2026-04-24`，这个目录承担两个角色：

1. `THM-M-0387` 的专属材料包。
2. 其他旗舰定理条目的标准范式。

因此，这个目录的结构本身就是模板，不只是内容模板。

`Docs/case_studies/fermat_last_theorem_formalization_study.md` 若保留，只作为兼容跳转入口；
本条目的权威正文与审计材料以 `THM-M-0387/` 目录为准。

截至 `2026-04-24`，本仓库已经把 Lean 正式源码树提升为 repo-level 共享目录 `Formalizations/Lean/`；
`THM-M-0387/` 本身只承担 dossier、审计、研究与验证入口角色。

截至 `2026-04-24`，人类可读衍生展开稿统一收在 `THM-M-0387/eligibles/` 的现有两份主稿中；
execution unit 状态只使用 `completed` / `Completion Gate = passed` 或 `missing/open` / `Completion Gate = missing/not passed`。
若要看截至 `2026-04-24` 的执行进度，则以 `full_study.md` 的 `Execution Checklist` 为准；公开材料包不再额外列出独立
`human_steps/` 目录。

## 本地验证

本地验证状态以 [`build_validation.md`](./build_validation.md) 为准。
`2026-04-24 21:50:30 CST (+0800)` 的本地重跑命令是：

```bash
bash THM-M-0387/run_local_validation.sh
```

该重跑失败，退出码为 `1`，原因是本地 `awesome-theorems-local` 工具链缺少
`/Users/wangweiyang/.elan/toolchains/awesome-theorems-local/bin/lake`。
因此，本 README 不声称 `2026-04-24 21:50:30 CST (+0800)` 环境可复现通过；
`build_validation.md` 中早于 `2026-04-24 21:50:30 CST (+0800)` 的成功 build、Lean version、toolchain name、模块清单和 file-check 只作为历史通过记录。
脚本文件在 `2026-04-24` 文档约定中不要求可执行位，所有文档统一使用 `bash THM-M-0387/run_local_validation.sh` 调用。

本地验证前提是 `Formalizations/Lean/lean-toolchain` 选择的自定义工具链 `awesome-theorems-local`
必须提供可用的 `lake` 与 `lean` 二进制；只存在 `elan` 外壳不足以完成验证。
`.lake/`、Lake build outputs、elan/toolchain downloads、dependency caches 与其他本机缓存不是 tracked artifacts，
公开证据以 `build_validation.md` 中记录的命令、结果、版本和边界说明为准。
