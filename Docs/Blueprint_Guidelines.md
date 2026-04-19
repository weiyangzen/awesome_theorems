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
    `upstream theorem closure: yes / repo-local vendored theorem closure: no, anchor-only / repo-local anchor-only statement/module/theorem-name record: yes`；
    其中最后一段只表示本仓库的 anchor-only statement/module/theorem-name 记录已到位，
    不表示本仓库已经 vendoring 上游 `flt_regular` 证明本体。
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

## 执行建议

后续若继续补强其他条目，推荐工作顺序是：

1. 先查 primary sources。
2. 若已有 machine-checked branch，先补 `machine_checked_audit` 与 `process_audit` 的机器节点留痕。
3. 再把主定理拆成定理树，至少展开到引理节点或分情况节点。
4. 检查所有叶子节点是否都在 `100` 步以内；若否，继续拆。
5. 再更新专题文档或研究文档。
6. 最后再补 `eligibles` 的人类可读稿、README 入口或 repo structure。
