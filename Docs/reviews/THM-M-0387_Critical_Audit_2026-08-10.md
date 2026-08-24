# THM-M-0387 六视角锐评与修订门

> 审计日期：2026-08-10
>
> 审计对象：当前 `main`（起始提交 `9c299dbabd34878a420db46ca66d687886fe2b04`）
>
> 文档性质：非权威、只读审计报告；不是 blueprint、任务游标或完成 receipt。

## 结论

`THM-M-0387` 对自己的根边界总体诚实：本仓库已通过 pinned Lean 依赖封闭
`n = 3`、`n = 4`、small exponents 和 regular primes 等分支，但没有封闭无条件
`FermatLastTheorem`。条件组装边
`OddPrimeExponentClosure -> FermatLastTheorem` 也没有被冒充为根证明。

不过，它目前还不能承担“已独立验收的旗舰 benchmark”这一更强角色。六个独立审查
视角共同发现三类硬缺口：

1. Wiles/Taylor-Wiles 人类数学 DAG 中存在会阻断链条的变量混型、局部正规化缺口和
   case split 漏项；
2. Lean/provenance gate 的覆盖比公开文字弱，若干所谓 direct probe、逐节点命令和
   statement transport 并未按宣称执行；
3. 当前验证事实、历史 receipt、Stage1 投影与 benchmark 状态没有统一到一个可重放、
   带快照身份的证据模型。

因此当前最准确的公开标签是：

```text
flagship formalization dossier + public FLT open challenge
root_machine_closed = false
benchmark_ready = false
```

## 六个独立审查视角

| 视角 | 核心审查面 |
|---|---|
| 数学事实核查 | `n=3`、`n=4`、regular primes、Frey/Ribet/Wiles/Taylor-Wiles 链 |
| Lean 语义核查 | theorem 类型、条件根、public declarations、axiom probe、上游 proof-body 链 |
| 跨文件一致性 | README、manifest、audit、Stage1 registry、receipt、指标分母和快照身份 |
| 本机可复现性 | elan/toolchain、Lake manifest、fresh clone、缓存/网络、验证入口 |
| benchmark 对照 | PutnamBench、miniF2F、ProofNet、LeanDojo、Lean Workbook 的任务/评分合同 |
| 敌对审稿 | 尝试推翻 checked/complete/coverage/flagship 等暗示，并复核潜在误报 |

## P0：必须先修的阻断项

### P0-1：FLT 指数与模性提升残余特征混型

[`wiles_taylor_wiles_process.md`](../../THM-M-0387/readable/wiles_taylor_wiles_process.md)
在 W03/W04/W05 间混用了 FLT 指数 `pF` 与 Wiles 半稳定模性证明所用的残余特征
`r in {3, 5}`。代表位置为该文件的 294--310、388--406、542--549、635--640、
833--850 行，以及 `proof_units.json` 约 8842 行。

Frey 曲线的 `E[pF]` 用于 Ribet 降层；Wiles 的 residual modularity/lifting 分支则处理
`E[3]` 或 `E[5]`。二者不是同一个类型参数。Taylor-Wiles 素数条件也应是
`q = 1 mod r^n`，不能沿用 `pF^n`。

修订门：W04 不得再依赖 W03.5；所有 deformation/Hecke/patching 对象显式参数化
`r`；W05 才重新消费 `rho_bar(E, pF)`。

### P0-2：2-adic 正规化不足

同一文档 95--117、218--264、881--902 行只固定“某项为偶”，不足以推出所使用的
2-adic 最小模型、半稳定性和最终 level `2`。至少需要固定 pairwise-coprime 解并记录

```text
a^p + b^p = c^p,  b = 0 (mod 2),  a = -1 (mod 4),
```

再给出 2 处适用的整模型，证明系数整性、2-极小性、`v2(c4)=0` 和
`v2(Delta_min)=2*p*v2(b)-8 > 0`。从 raw Frey model 到该模型是产生整模型的有理变量
替换，不能笼统称作可逆的 integral change of variables。

### P0-3：3--5 trick 的 residual case split 不穷尽

[`wiles_taylor_wiles_process.md`](../../THM-M-0387/readable/wiles_taylor_wiles_process.md)
513--540、833--850 行把 `E[3]` 可约后 `E[5]` 不可约当成自动事实，漏掉二者同时
可约的情形。

修订门：W04.9 必须列出三个互斥且穷尽的分支：`E[3]` 不可约；`E[3]` 可约且
`E[5]` 不可约；二者均可约。第三支要给精确 Wiles/Mazur theorem signature 和全部前提。

### P0-4：regular Case II 的 residue map 与 `eta_0` 写错

[`regular_primes_proof_process.md`](../../THM-M-0387/eligibles/regular_primes_proof_process.md)
2046--2058、2134--2138、2377--2384、2523--2525 行使用了错误的
`(eta-1)/(zeta-1)` residue map，并从未正规化的 `x+eta*y` 选择 `eta_0`。

固定 upstream 实际使用 `(x+y*eta)/(zeta-1)`；它覆盖包含零在内的全部 residue
classes，`eta_0` 是零类的唯一逆像。未正规化的 `x+eta*y` 已全部被 `pi` 整除，不能
区分该根。

修订门：四处逐字同步到 pinned `InductionStep.lean` 的 map、值域和唯一性前提。

### P0-5：当前复现事实不能由历史 pass 代替

审计开始时，规范命令

```bash
bash THM-M-0387/run_local_validation.sh
```

在当时的 [`run_local_validation.sh`](../../THM-M-0387/run_local_validation.sh) 的
pinned-Lake guard 失败。该机器后来已补装 exact toolchain，因此这个历史失败不再是
当前可复现的 blocker；仍可直接复现的缺口是 [`meta.json`](../../THM-M-0387/meta.json)
46--55 行与
[`build_validation.md`](../../THM-M-0387/build_validation.md) 仍只展示 2026-07-10 的
`pass/0`。更关键的是，相关 Lean、manifest、验证文档和 lint 在 7 月 11--18 日继续变化，
旧记录未绑定当前 Git tree，审计时也没有 `THM-M-0387/receipts/current-validation.json`。

这不否定历史运行，只否定“它证明当前快照可重放”。

修订门：拆分 `historical_result` 与 `current_reproduction`；每次运行生成 append-only
receipt，绑定 HEAD/tree/dirty、argv、toolchain、dependency SHAs、exit code、stdout/stderr
摘要和证据 manifest 摘要。

### P0-6：Stage1 的 PASS/exit-code 语义不可信

`Stage1_Instances/THM-M-0387/check_intake.py` 仍读取已经删除的 rev-5.6 文件；它能输出
`repair_required`/`status=failed` 却返回进程 exit `0`。`check_validation.py` 又只核对
JSON/hash/字符串，没有执行 `validation-spec.json` 中声明的 Lean recipes，却打印
`PASS validation handoff`。

修订门：任何 semantic failure 必须非零退出；validation checker 必须真实执行冻结的
`cwd + argv` recipe，并为正 fixture、错误 statement、`axiom`、`sorry`、forbidden import、
timeout 和 receipt tamper 提供负测试。

### P0-7：当前没有可评分的 benchmark task/scorer

M0387 同时混合了 statement autoformalization、已有 branch retrieval/wrapper、132-node
dossier audit 和开放的 FLT root proof。已有分支答案公开在同仓库，根任务又没有 accepted
gold；二者都不能直接进入普通 pass-rate。

修订门：新增唯一 task manifest，将 `statement_autoformalization`、
`partial_proof_or_retrieval`、`root_open_challenge`、`dossier_audit` 分轨；逐轨冻结输入、
allowed imports、candidate entrypoint、资源预算和 metric。M0387 必须标成 public/contaminated
development challenge，root 在 accepted closure 出现前不得进入 aggregate score。

## P1：高优先级质量缺口

### Lean 与 provenance

- `Stage1_Instances/THM-M-0387/Statement.lean` 只 import `Init`，对两个本地重复 Prop 做
  `Iff.rfl`，没有直接绑定 pinned mathlib 的真实 `FermatLastTheorem`。
- M0387 本地目录约有 32 个 theorem 声明；现有 manifest 的 29 个 closed-node probes 只
  对应 23 个 distinct declaration names，至少 9 个公开 theorem 未进入 exact-type/axiom
  probe。29 是节点数，不应被读成 29 份独立证明。
- 文档声称直接 probe `fermatLastTheoremThree`、`fermatLastTheoremFour`、`FLT_small`、
  `flt_regular`；实际 linter 强制 probe repo-local wrapper，未单独验证上游 terminal 的
  exact type、source location 与 wrapper-to-terminal link。
- `proof_units.json` 中 23 条逐节点命令先 `cd Formalizations/Lean`，又传入
  `Formalizations/Lean/...`，路径前缀重复；lint 只检查字符串非空，不执行命令。
- 31 个 provenance ref 指向当前 checkout 不存在的
  `Docs/Stage1_Assurance_Standard_rev-5.6.md`。

修订门：从 public API 自动枚举 declarations；对 wrapper 与 upstream terminal 分别运行
exact-type/axiom probe；验证 terminal 所在 source 与 proof-body link；命令改为结构化
`{cwd, argv}` 并逐条执行；所有本地/历史/外部 ref 使用可解引用的 typed locator。

### `n = 3`

- `n3_proof_process.md` 63、137、554 行把 Case-II reduction 写成无条件 canonical
  normalization；kernel 链实际是带入口假设 `H` 的条件定理，并依赖换号、循环置换、
  `Odd 3`、gcd 和整除传播。
- 565 行附近把 factor coprimality 和 cube-up-to-unit extraction 放在
  `Solution' -> Solution` 之前；实际二者发生在取得 `Solution` 之后，并依赖三次
  cyclotomic integer ring 的 PID/UFD。
- 580 行附近把 `formula3` 放在 `u4^2=1` 之前；597 行附近从 generalized witness 直接
  调用 `Solution.exists_minimal`，漏掉 `Solution' -> Solution`。

### `n = 4`

- `n4_proof_process.md` 的顶层摘要把 signed-square 结论写强。源码只推出
  `m=i^2`、`r=+/-j^2`、`s=+/-k^2`，随后由 `r^2=j^4`、`s^2=k^4` 消去符号。
- 整数互素性误写为 `Nat.Coprime`；`n!=0`、`rs!=0`、`b'!=0` 等侧条件缺少清晰的
  方程来源。`m>0` 则已在 961--979、1059--1062 行由 `ht6`、`b!=0` 与
  `b^2=2mn` 非循环地推出，不列为缺口。

### Wiles/Taylor-Wiles 余下链

- invariants/conductor 节诚实标成 H1/M4 planned/blocker；它的未完成接口仍没有冻结
  raw/minimal 两套 `Delta,c4` 公式，因此不能被后继节点当成已交付数据。
- Frey residual irreducibility 缺 Mazur 1978 rational-isogeny theorem 的精确引用和
  full rational 2-torsion/semistability 前提。
- W02.6、W05.2、W05.3 已在标题层分开 residual conductor 与 modular level；真正缺口是
  没有冻结能连接这些层的局部条件表，应分列 `q=2`、`q=pF`、奇 `q|abc, q!=pF`。
- Langlands--Tunnell、Taylor--Wiles prime、Ribet lowering 等叶的 primary references
  错配或缺 theorem/page/assumption crosswalk。
- 大量 “Apply the named source theorem / Verify intermediate condition” 模板句不能支撑
  独立的 R0/readability closure。

### 跨文件状态与指标

- 历史 `proof_units.json` 与 Stage1 registry 都有 132 nodes，却没有 `snapshot_id`、
  `lifecycle`、`claim_namespace` 和一一 crosswalk；裸 ID 不能跨快照直接比较。
- `readable closure 132/132` 的 numerator 来自自标 `R0`；132 个 readable targets 均无
  heading fragment，实际只落到 6 个文件，57 个节点共指向一篇 WTW 长文。应改名为
  `manifest readability annotation coverage`，不能称独立可读性验收。
- declaration 在顶层、`lean4` 与 composition edge 中重复保存，至少 6 个节点已分叉。
- M0133“怀尔斯定理”与 M0387 的 Stage1 Statement 冻结成同一个 FLT Prop；需要 alias 或
  exact target identity policy，不能把名称差异当成两项独立 benchmark。

## P2：精度、可维护性与审计轨迹

- `proof_units.json` 的 W08 输入遗漏 `p=3`/`flt3Path`，而 readable 文档已有正确二分；
  JSON 与人类投影必须由同一结构化 DAG 生成。
- `StatementAndReductionPath.lean` 的 `n=0` 分支是直接算术真，不应写成 vacuous truth；
  “只需 `n=4` 与所有奇素数”当前只检查充分方向，不能标成 checked equivalence。
- 历史日期应区分 1993 宣布、1994 修正突破与 1995 正式发表；“1995 路线”若使用现代
  `R_infinity/M_infinity` 语言，应标为现代等价重述并给 crosswalk。
- 当前 folder contract 会把新增 `receipts/current-validation.json` 视为 extra file；在发布
  current receipt 前，必须让 dossier contract 与 receipt 路径一致，并证明重复运行仍通过。
- 本汇总保存六个审查面及可复现证据，但没有把六份原始 subagent transcript 作为仓库资产。
  因而它可证明综合结论，不应被当作六份独立 attestation 的内容寻址归档。

## 未被推翻的强项

1. README、meta、machine audit 与 Stage1 release 都明确根仍是 H1/M2，
   `root_machine_closed=false`。
2. 条件组装 theorem 明确保留 `OddPrimeExponentClosure` 前提。
3. `n=3`、`n=4`、regular-prime wrappers 的 terminal types 与 pinned upstream 相符；
   上述人类数学问题不反向推翻这些 terminal kernel facts。
4. Imperial full-FLT candidate 因 `sorryAx`/任意命题公理被保守拒绝。
5. `H0=0/113` 和 primary-source crosswalk debt 已公开披露。
6. Stage1 release 是 blocked 且 `theorem_complete=false`；不能把 intake `[x]` 误读成
   theorem completion。

## 统一修订合同

以下条件全部满足前，不应宣称 `benchmark_ready=true`：

1. 修复四个数学 P0，并把 WTW DAG 改为 exact typed dependencies。
2. 建立一个结构化 theorem-evidence manifest；所有 prose/registry/metrics 都是带输入摘要的
   生成投影。
3. 验证事实只来自绑定当前 Git tree 与环境的 append-only receipts。
4. canonical Statement 直接绑定真实 pinned mathlib declaration，Proof 只能 import 该
   Statement，不得复制第三份 target。
5. 自动枚举并 probe 全部公开 theorem；wrapper 和 upstream terminal 的类型、公理、
   source 和依赖边分别可重放。
6. 真正执行每条 validation recipe，并通过完整正负 fixtures。
7. 定义 benchmark tracks、split/family/leakage/answer-visibility/license/scoring contract；
   开放 root 不进入普通 aggregate。
8. 在 clean pinned 环境运行规范验证，保存 current receipt；该 receipt 只能证明它实际覆盖
   的 wrapper/kernel 边界，不能替代未形式化的人类数学链。

## 可执行复现与接受门

下列命令均从仓库根执行。`现状预期` 记录本审计快照，而不是把失败当作完成；修复后的
Master acceptance 要求相应命令达到“接受条件”。

| 审查面 | 命令 | 现状预期 | 接受条件 |
|---|---|---|---|
| exact toolchain 与 package pins | `python3 scripts/check_lean_environment.py` | 安装完成后应通过 | JSON `status=passed`，toolchain、Lean commit、Lake 与 11 个 manifest revisions 精确匹配 |
| 当前七阶段 replay | `LAKE_NUM_JOBS=4 bash THM-M-0387/run_local_validation.sh` | 审计开始时无 current receipt | exit 0；receipt 绑定 HEAD、输入 manifest、pins、argv、完整输出 hash，且重复运行仍通过 |
| dossier 静态/Lean probe | `python3 scripts/lint_theorem_dossier.py THM-M-0387` | 可重放历史合同，但覆盖边界有限 | exit 0，并额外枚举所有 public wrapper 与 consumed upstream terminal，而非只复用节点计数 |
| Stage1 intake 失败语义 | `python3 Stage1_Instances/THM-M-0387/check_intake.py` | 输出 failed/repair_required 仍 exit 0 | 任何 semantic failure 非零；修复后的正 fixture 才 exit 0 |
| Stage1 recipe 执行 | `python3 Stage1_Instances/THM-M-0387/check_validation.py` | 只做静态字符串/hash 检查 | 真正执行冻结 recipes；错误 statement、`axiom`、`sorry`、forbidden import、timeout 与 tamper fixtures 全部非零 |
| WTW 类型参数 | `rg -n 'pF|residual characteristic|Taylor.Wiles' THM-M-0387/readable/wiles_taylor_wiles_process.md` | 可定位混型处 | W04 只用显式 `r in {3,5}`，无 W03.5 依赖；W05 才重新消费 `pF` representation |
| regular Case II | `rg -n '\(eta-1\)|x\+eta\*y|eta_0' THM-M-0387/eligibles/regular_primes_proof_process.md` | 命中错误 map/未正规化选择 | 错误式零命中；四处统一为 `(x+y*eta)/(zeta-1)` 并与 pinned `InductionStep.lean` 对齐 |
| blueprint gates | `python3 Docs/tools/check_stage2_blueprint.py && python3 -m unittest scripts/test_stage2_blueprint.py` | 应通过 | 唯一 authority、DAG、依赖状态与 Gantt exact projection 的正负 fixtures 全通过 |

这些命令不能把 Wiles/Taylor--Wiles 的人类数学链升级为 kernel-checked；数学 P0 仍需要逐叶
primary theorem、完整假设和独立审阅。
