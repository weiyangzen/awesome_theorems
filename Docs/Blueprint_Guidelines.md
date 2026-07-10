# Blueprint Guidelines

本文件用于保存蓝图编写与升级时的质量要求，尤其是用户已经明确提出、后续不应丢失的要求。

## 目标

当仓库为某个定理补充 blueprint 条目、case study、或形式化验证研究时，输出不应停留在“有无验证”的粗粒度标签，而要尽可能达到可追踪、可核查、可继续执行的状态。

## M0387 基准门槛

`THM-M-0387` 是后续 3000+ 个定理 blueprint 的旗舰样本，而不是一次性特例。凡是从 `THM-M-0387` 中沉淀出的更高标准，必须先同步进本文件，再生成或再生成任何批量 blueprint。

具体顺序固定为：

1. 先在 `THM-M-0387` 中把数学边界、machine-check 边界、人类可读展开、proof-unit 状态与本地验证记录校准到同一事实。
2. 再把可泛化规则写入 `Docs/Blueprint_Guidelines.md`，包括状态口径、债务分类、定理树粒度、执行门槛、公开/私有 surface 边界。
3. 最后才允许运行 blueprint generator，使 `Docs/Stage0_Blueprint.md` 或其他批量蓝图继承这些规则。

若发现某条规则只存在于 `THM-M-0387` 文档、生成器 override、或某个已生成蓝图中，而没有进入本 guideline，则该规则还不能视为仓库级标准；下一次批量生成前必须补回本文件。

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
9. 对每个定理，都必须按“定理树”而不是平铺 prose 的方式组织 proof blueprint。
10. 所谓“定理树”，至少要把主定理展开到：
   - 被直接调用的引理节点
   - 或者 proof 中不可再忽略的分情况讨论节点
11. 若一个节点仍然依赖其他 theorem / lemma / case split，它就不能被视为叶子节点。
12. 最终叶子节点的证明过程必须控制在 `100` 步以内；若超过 `100` 步，必须继续拆成更细的引理或 case 节点。
13. `证明路径上的定理或其他引例引理` 与 `依赖图与关键引理` 不能只写线性摘要，必须能支撑这棵定理树继续向下展开。
14. 若使用 cron / 并行 worker 自动补强 proof tree，必须把“私有 runtime ledger”和“公开归档面”分开：
   - worker 的中间账本、slot 草稿、临时分段稿应放在 `.cron/results/`、`.ops/` 或同类私有路径下
   - 这些 runtime 文件不能直接成为 blueprint 的公开 completion surface
15. 自动展开 `eligibles` 时，默认只能增补现有的公开主稿，不应为了执行方便在公开材料包下再平行新建第二套长期目录结构。
   - 例如已有 `eligibles/n4_proof_process.md`、`eligibles/regular_primes_proof_process.md` 时，应优先把新内容 merge 回这些主稿
   - 只有用户明确要求拆成新的公开子目录时，才允许保留额外公开 surface
16. 每个 execution unit 必须同时有：
   - 一个私有 runtime ledger，用于并行执行与局部 budget closure
   - 一个稳定的公开 merge target，用于最终材料归档
   blueprint / todo / README 只能引用稳定的公开 merge target，不能引用 `.cron/automation_repo*`、私有 runtime ledger、或临时绝对路径。
17. 自动执行场景下，平行 worker 不得直接并发编辑同一个公开 tracked 文档。
   - worker 应只写自己独占的私有 runtime ledger
   - supervisor / integrator 再串行 merge 回公开主稿
   - blueprint 勾选与 todo 回写只能发生在 merge-back 之后
18. 一个 unit 只有在以下条件同时满足后，才允许从 `open` 变成 `checked/completed`：
   - machine side 的 theorem / module / theorem-name anchor 已核实
   - 对“本仓库本地编译验证”与“仅记录上游 closure”之间的边界已如实写清
   - 对应的人类可读展开已经 merge 回公开 surface
   - 该 unit 自身已具备独立的 `<=100` 步 local budget ledger
19. 自动展开的人类可读稿必须继续服从 machine/process surface 的 canonical naming。
   - 可以给读者加 alias、标题化标签、budget alias
   - 但这些 alias 不能演变成第二套 competing canonical node system
20. 任何自动生成后准备进入公开主稿的材料，都应去掉过程性措辞，例如“本轮 worker”“slot 3”“下一轮继续”“当前 frontier”等，最后公开版只保留静态结论、状态表、budget ledger 与可复核内容。
21. 若同一 theorem folder 内存在 `full_study.md`、`machine_checked_audit.md`、`process_audit.md`、`eligibles/`、`README.md`、`meta.json` 等多层公开材料，必须指定一个 authoritative progress / status surface；其他文件只能解释它，不能与它产生 `checked` / `missing`、`completed` / `open`、`13/18` / `18/18` 这类冲突。
22. 公开 checklist 是 completion gate，不是叙事摘要。若 checklist 中某 unit 仍为 `missing`、`open` 或未勾选，则其他公开稿不得把同一 unit、同一 package、或同一 leaf 写成已经完全 `checked/completed`，除非同一 patch 同步更新 checklist 并给出公开 merge target 与 ledger anchor。
23. 反过来，若审计稿或人类可读稿已经声明某 unit 的 machine anchor、人类展开、`<=100` local ledger 均已闭合，则 authoritative checklist、README 摘要、`meta.json` 以及任何进度汇总必须同步更新；不得留下陈旧的 `missing`、`0/18`、`13/18` 等旧状态。
24. `meta.json`、README 入口、表格摘要里的 `status_detail` 必须保留与正文同等重要的边界信息。尤其当某分支只是“上游已 machine-checked、本仓库仅 anchor-only”时，不能在机器可读摘要里压缩成“本仓库已 machine-checked”。
25. `build_validation.md` 必须区分“历史上某日期通过”与“当前环境可复现通过”。若复跑失败，必须记录失败日期、命令、错误摘要与待修复条件；在复跑成功前，不得把当前状态继续写成“已通过”。
26. 本地验证脚本本身也属于验证 surface：必须说明推荐调用方式，并保证要么脚本具备可执行权限且 `./path/script.sh` 可运行，要么文档统一写成 `bash path/script.sh`。不能让 README 推荐一种当前会 `Permission denied` 的调用方式。
27. 若本地验证依赖自定义 toolchain、预编译 stage、缓存或外部下载，验证记录必须写明这些前置条件；若当前工具链只有 `lean` 但缺 `lake`，或会触发未完成下载，则不能声称当前 Lean 工程可复现 build 通过。

## 机器证明债分类

后续生成或升级具体 blueprint 时，必须把“还缺什么”按下面三类债务区分，不能只写成笼统的 `缺失`、`未完成` 或 `待补充`：

1. `mathematical_debt` / 数学债
   - 命题仍是 conjecture / open problem，或人类数学共同体尚无公认闭合证明。
   - 换言之，债务在数学本身：人类还没有证明。
   - 这类条目不能被写成“人类已证明，只差形式化”。
2. `formalization_debt` / 形式化债
   - 人类数学上已有证明，但还没有完整走完 proof assistant / kernel-checked 的机器证明渠道。
   - 公开项目若仍含 `sorry` / `admit` / axiom placeholder / 未闭合 blueprint，也属于这一类。
   - 这类条目的正确状态是“数学已知，机器形式化未闭合”，不能写成数学债。
3. `repo_local_integration_debt` / repo-local 整合债
   - 外部 Lean / Coq / Isabelle / HOL 工程已有可检查的机器证明，但本仓库尚未 pin/import/check，或只有 URL / theorem name / source note。
   - 换言之，机器证明已经存在，债务在本仓库没有把它纳入验证闭包。
   - 这类债务在本仓库标准下不允许长期存在：发现后必须通过 pinned dependency、vendored proof body、或 repo-local wrapper theorem 还清；还清后状态可升级为 `external_upstream_pinned` 或 `local_wrapper_upstream_*`，但仍需说明 proof body 是否 vendored。
   - 若短期内因为工具链不兼容、license、依赖冲突等原因无法整合，不能把该条目标成 completed；必须显式列入 blocker，并给出下一步整合条件。

对应的机器状态口径固定如下：

| 状态 | 含义 | 可计入 repo-local completed |
|---|---|---|
| `local_proof_body` | 证明本体在本仓库并通过本地验证 | yes |
| `local_wrapper_upstream_mathlib` | 本仓库有 wrapper，证明本体来自 pinned mathlib 并本地检查 | yes |
| `external_upstream_pinned` | 外部 formal 工程已作为 pinned dependency / vendored dependency 进入本仓库验证闭包并通过检查 | yes |
| `external_upstream_anchor_only` | 只记录外部 URL、commit、module 或 theorem name，未进入本仓库验证闭包 | no |
| `not_repo_local_closed` | 没有 repo-local theorem / dependency closure 闭合目标 | no |

生成具体蓝图时，`形式化阻塞点`、`现有 machine-checked 状态`、`依赖图与关键引理` 至少要回答：

- 人类数学证明是否已知？
- 是否已有公开机器检验证明？
- 若有外部机器证明，本仓库是否已经 pin/import/check？
- 若仍未闭合，债务类型是 `mathematical_debt`、`formalization_debt` 还是 `repo_local_integration_debt`？
- 哪个具体 theorem family / branch / API 参数仍缺失？

例如 `THM-M-0387` 中，regular primes 原先属于 `repo_local_integration_debt`，在 pin `flt-regular` 并检查 `regularPrimesPath` 后已还清；完整 Wiles/Taylor-Wiles 主线属于 `formalization_debt`，因为人类数学证明已知，但公开 Lean kernel-checked 完整链仍未闭合。

仓库级 acceptance 规则固定为：`repo_local_integration_debt` 不允许作为完成态残留；`mathematical_debt` 与 `formalization_debt` 可以存在，因为它们分别用于组织未来的新数学证明与新机器形式化工作。

## Stage1 Lean 4 队列

`Stage1_Blueprint.md` 只服务 Lean 4 theorem proving 执行队列，不再覆盖所有可形式化工具路线。生成 Stage1 前必须已经完成本 guideline 的同步，且 Stage1 生成器必须把下面规则写入生成结果：

`Docs/Stage1_Blueprint_rev-5.6.md` 是每个 Stage1 定理实例的规范 assurance standard；
`Stage1_Blueprint.md` 只是由生成器产生的 300 条候选队列，不再兼任 live execution-state、
evidence 或 theorem-completion authority。`THM-M-0387` 是历史兼容 fixture，不是允许把定理 ID、
路径、指标、公理集合或状态硬编码进通用 validator 的模板。

rev-5.6 在本仓库的目标集合必须冻结为
`Docs/Stage1_Blueprint_Applicable_Theorems.md` 中且仅其中的 `1546` 个 Lean 4 metadata-screened
候选。Stage0 的 `1601` 个去重数学记录不是 Stage1 cover 数；其余 `55` 个不得出现在目标表、
不得取得 Stage1 lane/slot/conformance 状态，也不得计入覆盖率。目标表不得再以历史 300-slot
文件的存在区分 assurance level。全部 `1546` 个目标统一从 `L0 / rework_required` 开始；旧 slot、
旧 wrapper、旧 statement、旧 build result 和旧 source label 只能作为 discovery input，不提供
proof credit、accepted state 或门禁豁免。任何历史证据都必须按当前 rev-5.6 的 exact scope、
provenance、trust、freshness 和 receipt 规则重新接纳。

目标集合发生增删时，必须发布 exact ID delta、eligibility 理由并重新运行结构检查；不能通过
手工向生成 Markdown 添行来扩大标准范围。

1. Lean 4 优先
   - 能在 Lean 4 / mathlib 中表达为定理、结构定理、模型定理、算法正确性定理或复杂度命题的条目，才进入 Stage1。
   - 已知更适合 TLA+ / SPIN / NuSMV / 专用模型检验、或只应作为实验数据 pipeline 的条目，不进入 Stage1。
2. 太难先延后
   - 若条目本身仍是 open problem、独立性命题、已否证命题、不可形式化命题，或当前连数学陈述与 formal target 都无法稳定，则不得进入 Stage1 主执行队列。
   - 人类数学证明已知但 Lean 4 基础设施明显未闭合的条目可以进入 Stage1，但必须标为 `deep_formalization_debt` 或更高难度 lane，不能伪装成短 proof task。
3. 太简单不占主队列
   - 若条目只是定义展开、低重要性事实、或不具备作为后续样本的 proof-tree 价值，应进入 `deferred_too_simple`，而不是占用 Stage1 主队列。
4. 物理条目口径
   - 物理条目只有在被重写为“给定公理化模型 / 方程 / regime / 单位约定后的数学结论”时，才算 Lean 4 theorem proving 任务。
   - Stage1 不把实验事实、材料性质、或现象描述本身写成 Lean 4 已证明定理。
5. 每个 Stage1 入选条目至少要带有：
   - Stage0 原 UID 与来源学科/子类。
   - Lean 4 陈述规范化任务。
   - mathlib / external upstream anchor 搜索任务。
   - theorem-tree / proof-package 拆分任务。
   - repo-local wrapper / pinned dependency / local proof body 三选一的闭合目标。
   - `<=100` 叶子证明步数预算要求。
   - 机器证明债分类与当前 lane。

`Stage1_Blueprint.md` 的 300 条数学高难度队列还必须额外满足：

- 只从 Stage0 的数学条目中选取，保留 Stage0 原 UID。
- 只纳入 Lean 4 / mathlib 可以承担部分验证任务的条目；非 Lean4 路线不进入 Stage1。
- 排除当前主命题仍为 open problem、独立性命题、已否证命题或不可形式化命题的条目；这些可以进入后续 conjecture / barrier 队列，但不占 Stage1 的 300 个 Lean 4 proof slots。
- 排除只有 `声称证明`、`部分解决`、`部分证明` 的 conjecture-named 条目；除非源文档明确写作 `已验证` / `已证明` / `已解决`，否则 `猜想` 条目不占 Stage1 theorem proof slot。
- 难度排序优先级应偏向现代数论、代数几何、同调代数、偏微分方程、随机过程、数学物理、微分/代数拓扑、微分几何、证明论/模型论/集合论等深依赖图领域。
- 对每一条，即使源文档写作 `已验证`，Stage1 也不得直接把它计为 repo-local completed；必须先完成 mathlib / external Lean 4 anchor 搜索、wrapper / dependency 整合、本地 build validation、`<=100` leaf budget ledger 与公开 merge target。
- 若 Stage1 执行时发现外部 Lean 4 证明已经存在，不能留下 `repo_local_integration_debt`；必须 pin/import/check 或显式标为 integration blocker，不能勾选完成。

每个 Stage1 实例还必须满足 rev-5.6 通用 assurance 门槛：

1. 对 canonical Lean target 做 elaboration、environment fingerprint 与等价形式 checked transport。
2. 在观察机器闭合状态前冻结 canonical obligation registry、eligibility、exclusion 与 denominator。
3. 分开 proof、refinement、provenance、evidence、trust、documentation 与 workflow typed graph。
4. 对非叶节点检查精确 child-to-parent composition certificate；alias/wrapper/transport 不得重复计 proof-body credit。
5. 解析真实 terminal declaration/body、全传递 declaration/依赖 closure、foundation/axiom profile 与完整 TCB。
6. validation recipe 必须是结构化 `cwd/argv/env/timeout/network/covered_ids`，并按原记录执行。
7. release evidence 必须绑定 immutable clean source snapshot、content-addressed receipts、SBOM/license、cold build 与 offline replay。
8. `R0` 必须是 unique anchored structured reconstruction 加独立 review；`<=100` 只是 leaf split threshold。
9. `H0` 必须有 primary source edition/theorem/page/assumption/errata crosswalk 与独立 review。
10. root、unique leaf、distinct body、interface、source-boundary、critical path/cut set 分开报告；百分比不能替代根闭合。
11. audit completion 与 theorem completion 必须是两个终点；open root 可以完成 audit，不能完成 theorem。
12. 高保证 release 必须经过独立 clean runner、independently implemented minimal verifier、mutation/metamorphic fixtures 和 deterministic evidence bundle。
13. evidence 必须有 owner、review due、invalidation、revocation、archive 与 tool/dependency upgrade differential policy。

## 定理树要求

后续对任意 theorem 条目做补强时，必须同时满足下面这套树形约束：

1. 根节点
   - 根节点就是条目本身的主定理或主命题。
2. 中间节点
   - 中间节点必须是“真正承担证明工作的依赖块”，包括引理、构造、归约、normalization、case split、induction step、descent step、bridge theorem。
3. 分叉节点
   - 如果 proof 依赖 `Case I / Case II`、奇偶拆分、边界条件拆分、局部/整体拆分、primitive/non-primitive 拆分，这些都必须显式写成分叉节点。
4. 叶子节点
   - 叶子节点必须是不再引用其他 theorem / lemma 的最小证明单元。
   - 每个叶子节点的“证明过程”上限是 `100` 步。
5. 超步数处理
   - 若某叶子节点超过 `100` 步，后续 checklist 不得标记为收敛，必须继续拆分。
6. 审计要求
   - 对已 machine-checked 的部分，要优先按上游源码里的 theorem / lemma / case structure 对齐。
   - 对尚未 machine-checked 的部分，可以先给出树形占位，但不能跳过分叉节点。
7. 执行优先级
   - 若某个 proof branch 已 machine-check，到下一轮补强时，必须优先扩充 `machine_checked_audit` 与 `process_audit` 中的机器节点留痕。
   - `eligibles/` 中的人类可读展开稿只能作为第二优先级跟进，不得先于机器留痕层无限外扩。
8. 粒度控制
   - 默认读者基线按“大学水平、具备相关学科基础”处理，而不是按完全零基础处理。
   - 对 `互素`、`整除`、基础模算术、线性代换等显然背景动作，不应为了凑叶子节点而过度教学化细拆。
   - 只有当这些动作本身决定了 proof flow 或 branch split 时，才值得进入定理树节点。

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
7. `theorem tree` 层
   必须明确写出主定理如何展开到引理节点或 case split 节点，并说明叶子节点是否已经压到 `100` 步以内。
8. 若某个 package / leaf 已经展开到下一层，但尚未逐条验证为 `<= 100` 步的 leaf proof，
   必须把该展开状态字面标为 `unchecked`，不能只写“待继续细化”或“后续再拆”。
9. 若 machine-proof 自动审计与 human-readable 自动展开同时进行，则 closure 顺序必须固定为：
   - 先核 machine anchor / theorem-level audit
   - 再核 process-tree / package-level ledger
   - 最后 merge 回 `eligibles` 的公开人类可读主稿
   不允许反过来先把公开 `eligibles` 写满，再倒逼 machine/process surface 跟上。

## 对 `eligibles` 人类可读展开的通用要求

`eligibles/` 的定位不是 machine audit 的复读层，也不是零基础教材层，
而是“对已经存在的 machine/process 结构做 reader-facing proof-flow translation”的公开主稿层。

后续对任意定理的人类可读展开，必须同时满足下面这组通用约束：

1. 不能止步于“命名已经同步”。
   - 如果某条 branch 已经把 canonical package / leaf / package-level subitem 命名对齐，
     但 `eligibles` 里还只有摘要句、状态句、或表格标题，那么这不算合格的人类可读展开。
   - `eligibles` 至少要把每个公开 package 写到“读者能看懂这一步为什么存在、输入是什么、输出交给谁”的程度。
2. 也不能为了显得完整而过度教学化细拆。
   - 对互素、整除传播、基础模算术、简单符号改写、显然的 parity cleanup 等基础动作，
     若它们不决定 proof flow，就不应继续拆成面向零基础的长篇教程。
   - `eligibles` 的默认读者基线仍是“大学水平、具备相关学科基础”。
3. 合格的 `eligibles` package 展开，至少应同时回答四个问题：
   - 这一 package 在整条证明链中的局部职责是什么
   - 它接收哪些上游输入
   - 它产出哪些下游接口 / 结论
   - 它在 canonical naming 中对应哪个 package / leaf / subitem
4. 若某个 package 已拥有独立 `<=100` 步 local ledger，
   则 `eligibles` 不应继续停留在“后续可继续展开”的口气，
   而应把这份 closure 直接转译成稳定公开稿。
   - 公开稿里可以保留局部 ledger
   - 但不应继续用“当前 frontier”“下一轮再做”“本轮 slot”之类执行态措辞
5. 若某个 package 尚未拥有独立 `<=100` 步 local ledger，
   则 `eligibles` 必须明确写成 `unchecked` 或等价的 open 状态，
   不能用流畅 prose 掩盖它还没有真正闭合这一事实。
6. `eligibles` 的适度展开深度，默认以“package 级闭环 + 必要时补一层 high-risk leaf”作为目标。
   - 对 proof graph 比较浅的 branch，package 级闭环通常就够
   - 对 proof graph 很深且局部风险集中的 branch，必须继续把真正的高风险 leaf 再拆一层
   - 但不能把所有 package 都机械地下钻到同一深度
7. `eligibles` 应优先展开“承担证明推进的节点”，而不是“读起来顺手的节点”。
   - bridge theorem、minimal normalization、case split、descent core、principalization、local-to-global transport 这类节点优先
   - 纯背景知识、历史轶事、语义重复总结不应挤占 package 展开预算
8. 若机器层已经给出 package / leaf / one-more-depth inventory，
   则 `eligibles` 的成功展开至少要让读者能把 prose 段落逐段对回这套 inventory。
   - 可以有 reader-facing alias
   - 但不能写成一套无法映射回 machine/process surface 的新叙事树
9. `eligibles` 不应长期停留在“只有总叙事，没有 unit closure”的状态。
   - 对自动执行或大条目补强，建议把 package 级内容并回主稿的附录 / merged section
   - 这样既避免平行目录膨胀，也避免主稿永远只停在粗粒度 narrative
10. 判断 `eligibles` 是否“展开到位”的最低标准不是字数，而是可接续性。
    - 读者读完某个 package 后，应能明确知道下一步 proof obligation 是什么
    - 也应能看出为什么这个 package 已经闭合，或者为什么它还不能闭合
11. 常见失败模式应视为硬错误：
    - 只有 status ledger，没有真正的人类可读 proof-flow 解释
    - 只有一层大段 narrative summary，没有 package 级输入 / 输出边界
    - 为了“显得有内容”而把显然基础动作过度拆解
    - machine/process surface 已闭合，但 `eligibles` 仍长期停留在“未整合”的执行中间态
    - 为执行方便新开第二套公开 `eligibles` 文档树，导致主稿与附加稿长期并行漂移
12. 当 `eligibles` 已达到适度展开后，后续补强应继续优先投向：
    - 新闭合的 machine/process package
    - 仍未闭合的高风险 leaf
    而不是反复重写已经稳定闭合的低风险 prose 段落。

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
12. 若旗舰条目存在 `machine_checked_audit.md`、`process_audit.md` 与 `eligibles/` 三层材料，则优先级应固定为：
   - `machine_checked_audit.md`
   - `process_audit.md`
   - `full_study.md`
   - `eligibles/`
   后面的层只能解释前面的层，不能代替前面的层。

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
8. 费马大定理这种 proof graph 很深的条目，不能只给 narrative audit；必须持续把 statement/reduction、`n = 4`、`n = 3`、`regular primes`、以及一般奇素数指数主链拆成可继续细分的定理树。
9. 对已经闭合的 `n = 4`、`n = 3`、`regular primes` 等分支，后续补强顺序应是：
   - 先补 machine proof trace
   - 再补 process audit
   - 最后才补 `eligibles` 的人类可读详解
10. `n = 3` 这类已经有清晰下降骨架、且读者默认具备大学水平基础的分支，不必往“互素、整除传播”这种显然层继续过拆。
11. `n = 4` 与 regular primes 这类高负载 leaf package 集中的分支，应优先把机器节点继续拆到可独立审计的 ledger 粒度。
12. `THM-M-0387` 跨文件统一的 canonical deep-split high-risk set 固定为 `7` 个 leaf：
    `raw coprime triple classification`、`square extraction for r*s with sign cleanup`、`strict natAbs descent hic`、
    `Case II ideal-factor layer / global product to local p-th powers`、
    `Case II distinguished root / p_pow_dvd_c_eta_zero`、
    `Case II descent core / three-root formula and raw descent`、
    `Case II close / merge / not_exists_solution'`；
    `Int.gcd a n = 1 transfer`、`exists_ideal pairwise ideal coprimality interface`、
    `caseI_easier / aux-index exclusion` 不并入这套 canonical high-risk leaf 集；
    需要时可作为 package-level subitem 单列，但跨文件 canonical 名仍以上述 `7` 个 leaf 为准。
13. 若 `eligibles` 或专题稿为了讲解需要使用 reader-facing alias / budget alias，
    必须在同节明确写出它们只是 alias，不构成第二套 competing canonical node system；
    跨文件同步仍以上游 machine/process surface 的 canonical package / leaf 名为准。
14. 若 canonical package / high-risk leaf / package-level subitem 的 naming sync
    已完成，但这些节点还没有各自独立的 `<=100`-step ledger，则对应 checklist 项必须继续保持
    open，并明确写成“proof-budget closure 尚未完成”，不能回退成“命名尚未对齐”。
15. regular primes 的人类可读 closure 若显式固定边界句，应保留为：
    `upstream theorem closure: yes / repo-local checked dependency closure: yes / repo-local vendored proof-body copy: no`；
    其中第二段表示本仓库已经 pin `flt-regular` 并通过 `regularPrimesPath` 检查该分支，
    第三段表示证明本体仍位于外部 dependency 中，而不是复制进本仓库源码树。
16. 若当前 package / leaf / package-level subitem inventory 中没有任何节点拥有独立的
    `<=100`-step ledger，则必须明确写出“当前还没有可提升为 `checked` 的 leaf-budget closure”，并保持
    现有 canonical naming、boundary sentence 与 status ledger 原样同步。
17. 若某条路线已经完成 package / leaf / package-level subitem 的独立 `<=100`-step ledger，
    则最终稿应去掉过程性措辞，例如“本轮 worker”“当前 frontier”“下一轮继续”等，
    只保留静态结论、状态表与 ledger 本体。
18. `n = 4` 与 regular primes 的人类可读自动展开，默认应直接 merge 回
    `eligibles/n4_proof_process.md` 与 `eligibles/regular_primes_proof_process.md`，
    不应在 `eligibles/` 下长期保留第二套平行公开目录（例如 `human_steps/` 一类执行中间层）。
19. 若自动执行确实需要把 `18` 个 execution unit 拆成独立 runtime ledger，
    这些 ledger 必须放在私有路径（例如 `.cron/results/hr18/`）下；
    公开蓝图里只能显示它们最终 merge 回的主稿位置，而不能把私有 runtime 文件当成公开归档面。
20. `full_study.md` 一类 authoritative blueprint 若要显示进度，只能显示：
    - unit 名称
    - 公开 merge target
    - 当前 closure 状态
    不能把执行层的 slot 文件名、worker 临时目录、automation clone 路径暴露成长期公开接口。
21. 对 `eligibles` 的自动增补，推荐采用“附录式 merge-back”而不是“平行文件外溢”：
    - 原主稿保留总叙事与 canonical summary
    - 新增 execution unit 细化内容统一并入主稿的附录 / merged section
    - 这样既保留单文件可读性，也避免公开 surface 膨胀成多套 competing 文档树
22. 若自动执行已经成功把某批 unit merge 回现有 `eligibles` 主稿，
    后续 blueprint / README / case study 必须统一改口到新的公开归档面，
    不得继续引用已经废弃的执行中间层目录。
23. `THM-M-0387/full_study.md` 中的 `Execution Checklist` 是该条目的人类可读展开 authoritative progress surface。
    若它仍显示某个 `FLT-HR-*` 为 `missing`，则 `machine_checked_audit.md`、`process_audit.md`、`eligibles/*.md`、README 与 `meta.json`
    都不得把同一 execution unit 叙述为已经完成；若确已完成，必须在同一轮同步回写 `Execution Checklist`。
24. `THM-M-0387` 的 `regular primes` 分支必须始终保留三段边界：
    - upstream theorem closure: yes
    - repo-local checked dependency closure: yes
    - repo-local vendored proof-body copy: no
    任何入口摘要、机器可读元数据或 README 若写成“regular primes 已 machine-checked”，必须同时说明这是上游 closure，
    且已通过 pinned dependency 进入本仓库验证闭包，但不是本仓库源码树内 vendored proof body。
25. `THM-M-0387` 的本地 Lean 验证记录必须可复现。若 `run_local_validation.sh` 因权限、缺 `lake`、toolchain 缺失、或外部下载超时而失败，
    `build_validation.md` 必须降级为“历史通过记录 / 当前复现失败”，直到在当前环境重新跑通后才能恢复“当前已通过”。
26. `THM-M-0387` 的 `run_local_validation.sh` 必须与文档调用方式一致：
    - 若文档写 `./THM-M-0387/run_local_validation.sh`，脚本必须有 executable bit；
    - 若不保证 executable bit，则文档统一写 `bash THM-M-0387/run_local_validation.sh`。
27. `THM-M-0387` 若出现 `n = 4` / `regular primes` 的 package-level `checked` 声明，必须能追溯到：
    machine anchor、公开 merge target、独立 `<=100` local ledger、以及 authoritative checklist 同步勾选。
    任一项缺失时，状态必须保持 `open/missing` 或写成“审计稿已草拟，completion gate 未通过”。
28. `THM-M-0387` 必须明确写出当前 proof debt：
    - 已还清的 `repo_local_integration_debt`：`regularPrimesPath` 通过 pinned `flt-regular` dependency 检查 regular primes branch。
    - 仍未还清的 `formalization_debt`：完整 Wiles/Taylor-Wiles / Ribet / Frey curve / modularity 主线尚未形成可由本仓库验证的 Lean 4 完整证明。
    - 具体缺口 theorem family：`∀ p : ℕ, Nat.Prime p → Odd p → FermatLastTheoremFor p`，或直接 `FermatLastTheorem`。

## 执行建议

后续若继续补强其他条目，推荐工作顺序是：

1. 先查 primary sources。
2. 若已有 machine-checked branch，先补 `machine_checked_audit` 与 `process_audit` 的机器节点留痕。
3. 再把主定理拆成定理树，至少展开到引理节点或分情况节点。
4. 检查所有叶子节点是否都在 `100` 步以内；若否，继续拆。
5. 再更新专题文档或研究文档。
6. 最后再补 `eligibles` 的人类可读稿、README 入口或 repo structure。
