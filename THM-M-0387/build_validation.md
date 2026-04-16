# THM-M-0387 构建与验证记录

## 已通过的本地验证

以下命令已经通过：

```bash
cd Formalizations/Lean
LAKE_NUM_JOBS=1 lake build \
  +AwesomeTheorems.NumberTheory.THM_M_0387.FLT4Path \
  +AwesomeTheorems.NumberTheory.THM_M_0387.FLT3Path \
  +AwesomeTheorems.NumberTheory.THM_M_0387.RegularPrimesPath \
  +AwesomeTheorems.NumberTheory.THM_M_0387.Sample
lake env lean ../../THM-M-0387/FermatLastTheorem_Sample.lean
```

其中：

1. 在 `Formalizations/Lean` 下执行
   `LAKE_NUM_JOBS=1 lake build +AwesomeTheorems.NumberTheory.THM_M_0387.FLT4Path +AwesomeTheorems.NumberTheory.THM_M_0387.FLT3Path +AwesomeTheorems.NumberTheory.THM_M_0387.RegularPrimesPath +AwesomeTheorems.NumberTheory.THM_M_0387.Sample`
   已成功，收尾信息为 `Build completed successfully (3448 jobs).`
2. 在 `Formalizations/Lean` 下执行
   `lake env lean ../../THM-M-0387/FermatLastTheorem_Sample.lean`
   已成功，退出码为 `0`。

其中被 `lake build` 直接编译的模块体现在位于：

- [`Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/FLT4Path.lean`](../Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/FLT4Path.lean)
- [`Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/FLT3Path.lean`](../Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/FLT3Path.lean)
- [`Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/RegularPrimesPath.lean`](../Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/RegularPrimesPath.lean)
- [`Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/Sample.lean`](../Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/Sample.lean)

而 `THM-M-0387/` 目录现在只承担 theorem dossier 角色；
共享 Lean 源码树已经迁到仓库级目录 `Formalizations/Lean/`。

这组命令也被固化到：

- [`run_local_validation.sh`](./run_local_validation.sh)

## 本地工具链状态

本地工具链为 `awesome-theorems-local`，有效状态为：

- `lean --version` 返回 `Lean 4.29.0`
- `lean --print-libdir` 指向本地 `stage1/lib/lean`

这说明当前不是只装了 `elan` 外壳，而是已经切到了可用的本地 Lean `stage1` 工具链。

## 边界

本文件只记录已经真实跑通的验证，不额外夸大。

当前可以严格声称的是：

1. 本仓库已存在 repo-level 共享 Lean 工程。
2. `AwesomeTheorems.NumberTheory.THM_M_0387.FLT4Path`、`FLT3Path`、`RegularPrimesPath` 与 `Sample` 已 build 通过。
3. `THM-M-0387/FermatLastTheorem_Sample.lean` 作为 dossier-local 入口已 file-check 通过。
