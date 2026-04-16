# Formalizations / Lean

本目录是仓库级共享 Lean 源码树。

定位：

1. 不服务于单个 theorem folder。
2. 服务于整个仓库未来的多定理 Lean formalization。
3. 与 `THM-M-0387/` 这类 theorem dossier 分离。

## 当前内容

- `lakefile.lean`
- `lean-toolchain`
- `lake-manifest.json`
- `AwesomeTheorems.lean`
- `AwesomeTheorems/NumberTheory/THM_M_0387/Sample.lean`
- `AwesomeTheorems/NumberTheory/THM_M_0387/FLT4Path.lean`
- `AwesomeTheorems/NumberTheory/THM_M_0387/FLT3Path.lean`
- `AwesomeTheorems/NumberTheory/THM_M_0387/RegularPrimesPath.lean`

其中 `THM_M_0387` 已按三条分支路径拆开：

- `FLT4Path`
- `FLT3Path`
- `RegularPrimesPath`

`Sample.lean` 只保留为聚合入口。

依赖管理上，这棵共享 Lean 树现在通过 `lakefile.lean` + `lake-manifest.json`
固定 `mathlib` git revision；`.lake/` 与本地 vendored/cache 目录不进入 git。

## 原则

- theorem folder 保存研究、审计、验证记录与人类可读材料；
- 共享 Lean 模块统一进入本目录；
- 后续若增加更多定理，应继续扩充 `AwesomeTheorems/...` 模块树，而不是把 Lean 源码塞回各 theorem folder。
