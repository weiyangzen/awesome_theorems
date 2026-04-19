# THM-M-0387 费马大定理

本目录是 `THM-M-0387` 的旗舰物料目录。

目标不是只保存一篇长文，而是把“形式化验证 + 机器证明完整验证（可证明部分）”条目可直接复用的结构固定下来。

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
  三个已闭合分支的人类可读展开稿。
  本轮 `n = 4` 与 `regular primes` 的 `18` 个 execution unit 现已直接并回现有主稿，
  不再单独占用 `eligibles/` 子目录。
- `build_validation.md`
  本仓库本地 Lean 工程验证记录。
- `FermatLastTheorem_Sample.lean`
  本条定理 dossier-local Lean 入口。
- `run_local_validation.sh`
  统一本地验证脚本。
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

## 当前定位

这个目录现在承担两个角色：

1. `THM-M-0387` 的专属材料包。
2. 其他旗舰定理条目的标准范式。

因此，这个目录的结构本身就是模板，不只是内容模板。

`Docs/case_studies/fermat_last_theorem_formalization_study.md` 若保留，只作为兼容跳转入口；
本条目的权威正文与审计材料以当前目录为准。

当前仓库已经把 Lean 正式源码树提升为 repo-level 共享目录 `Formalizations/Lean/`；
`THM-M-0387/` 本身只承担 dossier、审计、研究与验证入口角色。

本次新增的人类可读衍生展开稿统一收在 `THM-M-0387/eligibles/` 的现有两份主稿中。
若要看本轮 `0/18` 到 `18/18` 的真实执行进度，则以 `full_study.md` 的 `Execution Checklist`
为准；公开材料包不再额外列出独立 `human_steps/` 目录。
