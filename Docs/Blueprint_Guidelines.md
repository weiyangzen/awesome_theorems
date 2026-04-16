# Blueprint Guidelines

本文件用于保存蓝图编写与升级时的质量要求，尤其是用户已经明确提出、后续不应丢失的要求。

## 目标

当仓库为某个定理补充 blueprint 条目、case study、或形式化验证研究时，输出不应停留在“有无验证”的粗粒度标签，而要尽可能达到可追踪、可核查、可继续执行的状态。

## 通用要求

1. 对每个重点定理，必须满足 `README.md` 与 `Docs/Stage0_Blueprint.md` 中列出的字段要求，不能只补摘要。
2. 若定理处于 `部分验证` 或 `进行中` 状态，必须明确区分：
   - 已 machine-checked 的部分
   - 已公开发表但不等于全定理完成的部分
   - 仍在进行中的部分
3. 不能把“数学上已证明”与“公开机器检验证明已完成”混写为同一个状态。
4. 需要给出绝对日期，而不是只写“最近”“当前”“现在”。
5. 对 status 判断必须优先查阅 primary sources，而不是凭记忆填写。
6. 若条目声称“已证明 / 已验证 / 已 machine-checked”，则必须区分“数学上已有证明”和“本仓库或对应 formal 工程已实际编译通过”。
7. 对 Lean / Coq / Isabelle 等 proof assistant 工程，只有在以下条件满足后，才能把对应工件标成“已编译验证通过”：
   - 已配置完整工具链
   - 已配置项目文件，例如 `lean-toolchain`、`lakefile.lean` 或等价工程配置
   - 已实际运行 `lake build`、等价 build 命令，或逐文件编译命令并通过
8. 如果仓库当前只有文档、样例代码、或未纳入工程的片段，而没有真实编译通过，则只能写：
   - `样例`
   - `对齐上游 API 的示例`
   - `未在本仓库本地编译验证`
   不能直接写成“本仓库已证明/已验证”。

## 资料要求

1. 优先使用官方文档、正式论文、项目 README、源码入口文件、blueprint 页面。
2. 对技术性条目，尽量给出具体文件或 theorem 名称，而不是只给项目首页。
3. 若引用 machine-checked 结果，至少应能定位到：
   - 对应项目 / 库
   - 关键源码文件
   - 主 theorem 名称或结构名

## 对“已 machine-checked 部分”的展开要求

若一个定理的部分内容已经被机器证明，则必须至少展开到以下粒度：

1. `statement / reduction` 层
   说明陈述是否已经被编码、是否已有自然数/整数/有理数版本切换、是否已有 primitive solution 约化。
2. `special cases` 层
   明确写出已完成的特例，如 `n = 3`、`n = 4`，以及对应 theorem 名。
3. `intermediate general results` 层
   若已有 regular primes、semistable、case I / case II 等中间 generalization，必须单列说明。
4. `full theorem` 层
   明确说明完整总证明是否完成。
5. `theorem-level audit` 层
   至少给出一张“代码位置 / theorem 或 structure 名称 / 数学作用 / 当前闭合程度”的审计表。
6. `process audit` 层
   不能只写“某特例已验证”，还要说明 proof graph 中哪些步骤已经被机器化，例如最小反例、互素化、parity normalization、generalized equation、multiplicity descent、case split 完备性。

## 对旗舰条目的额外要求

对于像 `THM-M-0387 费马大定理` 这样的旗舰条目：

1. 必须保留独立完整研究文档，而不是只在大蓝图里写一行。
2. 必须给出“已 machine-checked 部分的详细拆解”。
3. 必须给出 theorem-level 审计表，而不是只给 narrative summary。
4. 必须把条目增强逻辑写进 blueprint 生成机制中，避免下次重新生成时丢失。
5. 若公开总项目仍在进行中，必须在条目中写清楚“哪部分完成，哪部分未完成”。
6. 若仓库内提供 Lean 样例或 proof artifact，必须额外说明：
   - 是否已经把仓库接成可编译工程
   - 是否已跑通 `lake build`
   - 哪些文件被实际编译
7. 旗舰条目应整理成独立 theorem folder，至少包含：
   - 位于仓库根目录，例如 `./THM-M-0387/`
   - `README.md`
   - `full_study.md`
   - `machine_checked_audit.md`
   - `process_audit.md`
   - `build_validation.md`
   - 一个本地 proof-assistant sample
   - 一个统一的本地验证脚本，例如 `run_local_validation.sh`
   - 一个机器可读 `meta.json`
8. 根目录 theorem folder 应是旗舰条目的权威材料包；若 `Docs/case_studies/` 下保留同名文档，只能作为 redirect stub，不应再承载正文。
9. 若 theorem 条目需要仓库内可编译的 Lean/Coq/Isabelle 源码，相关 theorem-specific 源文件也应尽量放在对应 theorem folder 内；应避免在仓库根目录再平行铺开只服务于该定理的 `Examples/`、`src/`、或同类专属目录。
10. 若仓库目标升级为“多定理共享一个正式 proof-assistant 工程”，则应把源码树提升为 repo-level 共享目录，例如 `Formalizations/Lean/`、`Formalizations/Coq/`、`Formalizations/Isabelle/`；此时 theorem folder 退回 dossier 角色，不再兼任共享源码根。
11. 在上述共享工程结构下，`AwesomeTheorems.lean` 这类库根模块应位于 assistant-specific 共享源码树根，而不是位于单个 theorem folder 中。

## 本仓库当前已固化的专项要求

### 针对 THM-M-0387

1. 不允许再把费马大定理整体写成简单的 `已验证`。
2. 必须明确写出：
   - `mathlib` 的 statement / reduction 层
   - `n = 4`
   - `n = 3`
   - `flt-regular` 的 regular primes
   - Imperial College London 公开 FLT 总项目仍在进行中
3. 需要在 case study、Stage0 blueprint override、以及 README 入口三处保持一致。
4. 若本仓库本地 Lean 工程尚未跑通，不允许把本仓库内样例文件表述成“已在本仓库完成验证”。
5. 必须补充 theorem-level 审计表与 process-level 审计，不得只保留“special cases/generalization/full theorem”这种摘要层。
6. 相关文本性质物料应集中到仓库根目录下的独立 theorem folder 中，供未来其他旗舰条目直接复用其目录结构。
7. 公用环境与本地验证流程应尽量集中到一个 `.sh` 中维护，而不是散落在聊天记录或零碎注释里。

## 执行建议

后续若继续补强其他条目，推荐工作顺序是：

1. 先查 primary sources。
2. 再更新专题文档或研究文档。
3. 再更新 Stage0 blueprint 及其生成器 override。
4. 最后补 README 入口或 repo structure。
