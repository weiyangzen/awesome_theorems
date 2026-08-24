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

## 可复现的本机验证

仓库固定 `leanprover/lean4:v4.29.0`，并要求官方 `elan 4.2.3`、Lean
`4.29.0`（commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`）和 Lake
`5.0.0-src+98dc76e`。先运行只读环境检查：

```bash
python3 scripts/check_lean_environment.py
```

检查器始终输出一个 JSON 文档；toolchain、Lake lock 或已物化 package revision
不匹配时非零退出，并给出修复建议。它优先使用 `$ELAN_HOME/bin/elan`，否则使用
`PATH` 中的 `elan`，且通过 `elan run leanprover/lean4:v4.29.0` 运行工具，因而不受
用户默认 toolchain 影响。

完整的 THM-M-0387 本机验收仍是七阶段入口：

```bash
LAKE_NUM_JOBS=4 bash THM-M-0387/run_local_validation.sh
```

该入口先执行上述 preflight，再构建分支模块、集成 wrapper、样例、聚合库、完整
Lake target，最后编译并执行 dossier lint。它不会更新 `lake-manifest.json` 或切换
依赖 revision。注意 Lake 5 不提供 `LAKE_NUM_JOBS` 并发控制；上例中的值只作为调用方
资源提示被日志/receipt 记录，不应被解读为“四个 build jobs”的保证。

每个阶段默认有 7200 秒硬超时，并输出稳定的 `M0387_STAGE_BEGIN/ARGV/END` 标记；可用
正整数 `M0387_STAGE_TIMEOUT_SECONDS` 缩短该上限。入口会清除可重定向 toolchain 或
package 解析的 `ELAN_TOOLCHAIN`、`LAKE_OVERRIDE_LEAN`、`LEAN_SYSROOT`、`LEAN_PATH` 与
`LAKE_PKG_URL_MAP`，同时清除 `CDPATH`，保证记录的 cwd/argv 与实际执行一致。

## 原则

- theorem folder 保存研究、审计、验证记录与人类可读材料；
- 共享 Lean 模块统一进入本目录；
- 后续若增加更多定理，应继续扩充 `AwesomeTheorems/...` 模块树，而不是把 Lean 源码塞回各 theorem folder。
