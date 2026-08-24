# THM 列表六视角 Benchmark 锐评

> 审计日期：2026-08-10
>
> 审计对象：`Docs/researches/{math,physics,cs}_theorems.md`、生成后的
> `Docs/Stage0_Blueprint.md`、Stage1 target/instance surfaces 与相关生成器
>
> 基线：`main` 起始提交 `9c299dbabd34878a420db46ca66d687886fe2b04`
>
> 文档性质：六名独立 reviewer 的只读审计汇总；不是数据集 release、proof receipt、
> blueprint 游标或对任何单条命题的真值认证。

## 结论

当前三份 THM 列表是有价值的广覆盖研究目录，但不是 PutnamBench 意义上的 theorem
benchmark，也不是可直接评分的科学 benchmark。最严重的问题不是“条目还不够多”，而是
目录行、可判定 claim、文献事实、形式化工件、benchmark task 和执行状态被压进了同一层。

可复现盘点得到 3,338 条原始记录；Stage0 以六个字符串字段做严格去重后剩 3,262 条。
其中 2,808 条（86.08%）仍显示原始标签“已验证”，但 3,262/3,262 没有逐条 primary
citation，3,261/3,262 没有精确 statement，也有 3,261/3,262 没有 Stage0 machine-artifact
链。当前最准确的发布标签是：

```text
catalog_research_value = high
claim_identity_frozen = false
machine_evidence_complete = false
benchmark_ready = false
```

任何 pass rate 若直接把“已验证”、Stage1 target 或存在 `.lean` 文件当分母/成功标准，都会
混淆人类数学真值、经验支持、形式化可行性、外部 formal proof 与本仓库 replay 事实。

## 六个独立视角

| 一级 reviewer task | 视角 | 独立审查面 |
|---|---|---|
| `/root/bench_math` | 数学 | PutnamBench、miniF2F、ProofNet 对照；精确量词、前提、原子性、开放状态与数学重复 |
| `/root/bench_physics` | 物理 | law/model/effect/observation 分轨；regime、单位、近似、observable、误差与数值 oracle |
| `/root/bench_cs` | 计算机科学 | computation/adversary/fault model、encoding、resource、probability、correctness 与 executable oracle |
| `/root/bench_schema` | benchmark schema | task unit、release pin、family split、visibility、scorer、metrics、license 与 contamination |
| `/root/bench_status` | 状态与证据 | human truth、empirical、external formal、repo integration、provenance 的错误折叠与升级门 |
| `/root/bench_sampling` | 分层抽样 | 跨三域的重复、别名、粒度、难度/年代/类别覆盖和抽样外推边界 |

六名 reviewer 均只读工作；审查时未改动三份源表、Stage0 或其生成器。
这里的 task name 是本轮一级分工身份，不是外部个人身份；本汇总保存各自结论，不把协作
thread transcript 冒充仓库内六份独立签名 attestation。

## Benchmark 一手资料定位

以下定位是 reviewer 在 2026-08-10 使用的比较入口。论文计数与仓库主分支计数可能随时间
不同，因此本报告只把论文/数据集版本数字当作带来源的观察，不把未固定的 `main` 当 release。

| 资源 | 一手入口 |
|---|---|
| PutnamBench | paper: <https://arxiv.org/abs/2407.11214>; repository: <https://github.com/trishullab/PutnamBench> |
| miniF2F | paper: <https://arxiv.org/abs/2109.00110>; repository: <https://github.com/facebookresearch/miniF2F> |
| ProofNet | paper: <https://arxiv.org/abs/2302.12433>; repository: <https://github.com/zhangir-azerbayev/ProofNet> |
| LeanDojo | paper: <https://arxiv.org/abs/2306.15626>; Lean 4 benchmark DOI: <https://doi.org/10.5281/zenodo.8040109> |
| Lean Workbook | paper: <https://arxiv.org/abs/2406.03847>; data: <https://huggingface.co/datasets/InternLM/Lean-Workbook> |
| TheoremQA | paper: <https://arxiv.org/abs/2305.12524>; repository: <https://github.com/TIGER-AI-Lab/TheoremQA> |
| SciBench | paper: <https://arxiv.org/abs/2307.10635>; repository: <https://github.com/mandyyyyii/scibench> |

## 可复现基线

生成器现有 parser 的全量计数如下：

| 集合 | 数学 | 物理 | 计算机科学 | 合计 |
|---|---:|---:|---:|---:|
| 原始 source records | 1,666 | 1,272 | 400 | 3,338 |
| Stage0 严格去重后 | 1,601 | 1,263 | 398 | 3,262 |
| 被静默折叠的 source occurrences | 65 | 9 | 2 | 76 |
| Stage0 “已验证” | 1,531 | 1,099 | 178 | 2,808 |

最小复现入口：

```bash
python3 - <<'PY'
from Docs.tools.generate_stage0_blueprint import (
    LIST_STYLE_SOURCES, TABLE_STYLE_SOURCE, parse_list_style_source,
    parse_table_style_source, dedupe_items,
)
items = []
for s in LIST_STYLE_SOURCES:
    items += parse_list_style_source(s["path"], s["discipline"], s["ignore_h2"])
s = TABLE_STYLE_SOURCE
items += parse_table_style_source(s["path"], s["discipline"], s["ignore_h2"])
print(len(items), len(dedupe_items(items)[0]), dedupe_items(items)[1])
PY
```

证据缺失率：

| 缺口 | 数量 | 解释 |
|---|---:|---|
| 逐条可定位 citation 缺失 | 3,262/3,262 | 通用书目不能认证某一 statement/status |
| exact statement 缺失 | 3,261/3,262 | 只有 M0387 的 Stage0 override 非占位 |
| Stage0 machine-artifact 链缺失 | 3,261/3,262 | 文件存在也不能替代 declaration/type/axiom/replay receipt |
| Stage1 authoritative completion | 1,546/1,546 targets 未完成 | membership 全部 `theorem_complete=false` |

此外，1,546 个 Stage1 targets 只有 1,506 个 instance 目录、1,180 个 `instance.json`、336 个
`statement.json`、217 个标准名 `proof-receipt.json` 和 253 个 `release-decision.json`；
`instance.json` 至少有八种 schema 表达。它们是执行资产，不是一个冻结的 benchmark release。

## 与同类 benchmark 的直接差距

| Benchmark | 已核查的核心合同 | 当前列表缺口 |
|---|---|---|
| PutnamBench | 区分源问题与跨语言 formalization；factored-answer 题分为 given-answer proof 与 answer+proof；结果须绑定 release/commit | source occurrence、canonical claim、formal variant 和 evaluation task 未分层；无 answer visibility |
| miniF2F | 488 statements，固定 244 valid/244 test；按 commit/date 报告并限制公开 proof 污染 | 无 immutable split、release pin 或 proof-visibility policy |
| ProofNet | NL statement、formal statement、NL proof 三元组；formal proving/autoformalization 分轨；typecheck 不等于语义正确 | prose、statement、proof 和 task 混在目录项；无语义 equivalence scorer |
| LeanDojo | random 与 novel-premises split；报告 R@k/MRR/Pass@1 并绑定十分钟预算 | 无 dependency/family holdout、attempt 定义或资源绑定 metric |
| TheoremQA | theorem application QA，固定 answer/answer_type/picture 等任务字段 | “定理名录”被误当应用题；没有 answer-type scorer |
| SciBench | 数值答案、单位、LaTeX、详细解答；数值 tolerance 或 rubric 按任务冻结 | 物理条目缺单位、容差、数据、误差预算和可执行 oracle |
| APPS/竞赛数据 | 完整 I/O、输入约束、隐藏测试、时间/内存限制 | 算法名或复杂度摘要没有 candidate contract 与测试 |

PutnamBench 论文中的 640 source problems/1,692 formalizations 与其当前主分支的 1,724
formalizations/672 Lean 4 items 已不同，这本身证明：未 pin 的“当前数量”不能用于跨论文比较。

## P0：跨域阻断项

### P0-1：顺序 ID 会漂移，去重会擦除身份

`generate_stage0_blueprint.py` 先按六个原始字符串字段去重，再按出现顺序生成
`THM-{M|P|C}-NNNN`。在前方插入一行会改变后续全部 ID；跨域完全相同的行按
`数学 > 物理 > 计算机科学` 保留，来源 occurrence 与学科标签被丢弃。

已确认例子包括：CS Hamming 界被数学 occurrence 折叠而没有 THM-C ID；第二个 Huffman
occurrence 被删除；措辞不同的 BWT 却同时保留为 C-0109/C-0395；M-0023/M-0517 都是岩泽
主猜想；M-1133/M-1188 是热方程极值/极大值原理的同族表述。

修订门：冻结全部 3,338 source occurrences；用内容绑定、与排序无关的 canonical ID；旧
THM ID 永久作为 alias；duplicate/alias/refinement/same-name-different-claim 都必须是显式关系，
不得再次 destructive renumber/dedupe。

### P0-2：一个“形式化状态”混合至少六个正交轴

当前 22 种原始状态同时表达“人类已证明”“问题得到否定答案”“经验上受支持”“原则上可
形式化”“已有外部机器证明”“本仓库已有进度”和算法复杂度。生成器又把“已验证/已证明/
已解决/准多项式时间解决”压成一个 `closed` bucket。

默认迁移必须保守：原始 `已验证` 只保留在 `source_status_raw`；没有逐条 evidence 时，
`human_truth=unknown`、`external_formalization=none`、`repo_integration=absent`。任何轴只能由
自己的证据升级，不能相互推断。

### P0-3：绝大多数行还不是可判定 proposition

数学中 1,470/1,601 被兜底为“数学定理/命题”；物理中 988/1,263 被兜底为“物理命题/
结果”；CS 398/398 的 proof 文本被模板称为“假说内容”。对象、学科、框架、设备、方程、
算法、问题和历史 proof artifact 因而进入同一个 theorem 表面。

修订门：先完成 `claim_kind` 和 atomicity gate，再允许 statement/proof 工作。非 truth-valued
ontology entries 可以保留在 catalog，但不得进入 theorem pass-rate。

### P0-4：没有独立 benchmark task、split 或 scorer SSOT

Stage0 是目录快照；Stage1 是强 provenance/validation 的执行系统。两者都没有稳定的
`source problem x statement variant x task type x visibility x environment` task unit，也没有
冻结 family split、public/private pack、candidate surface、统一 metric 和 scorer conformance
tests。公开 proof 的 sibling family 可轻易污染所谓 held-out 测试。

修订门：canonical catalog 与 benchmark release 必须分层；aliases、同义 statement、同一
source solution、proof-template 和 dependency family 的连通分量只能落入一个 split。

### P0-5：license、provenance 与 release pin 不足

三份 source list 无逐条 source locator/hash/license，仓库根也没有统一 LICENSE。即便某一
命题是公共知识，其原文、翻译、证明、图片、代码和数据仍有不同版权/再分发边界。

修订门：每个分发 byte 绑定 source、content hash、rights scope 与允许用途；citation-only
资产显式标出；release 绑定 Git tree、文件 digest、toolchain、dependency 与 scorer identity。

## 数学抽查：statement、原子性与状态

| ID | 当前问题 | 最低修订 |
|---|---|---|
| M-0004 万有系数定理 | 同调与上同调多个版本混成一句 | 分拆 tensor/Tor exact sequence 与 Hom/Ext 版本；注明分裂非自然 |
| M-0016 Hilbert 第十二问题 | 虚二次已解范围与一般数域开放范围混杂 | solved special case 与 general-open 两项，分别给 status source |
| M-0023/M-0517 岩泽主猜想 | 重复且版本/角色分量不明 | 一个 family；冻结 `p`、扩张、Iwasawa algebra、characteristic ideal 和 p-adic L-function |
| M-0043/M-0313 谱定理 | 同名但矩阵/算子命题不同 | namespaced canonical names；各自精确 domain 与 conclusion |
| M-0114 Hodge 猜想 | 开放命题只有名词摘要 | 精确量化 Hodge classes；只进入 statement/open-challenge 轨 |
| M-0122/M-0123/M-0395 Mordell/Faltings | 历史猜想、证明事件和定理重复计数 | 一个 canonical claim family，历史名称与 source occurrence 作 alias |
| M-0183 Calabi 猜想 | “任意紧 Kähler 都 Ricci-flat”过强 | 使用 prescribed Ricci form 定理；Ricci-flat 推论增加 `c1=0` |
| M-0191 Weil 猜想 | 四个独立命题包成一项 | 拆 rationality、functional equation、Betti interpretation、RH/weights |
| M-0241/M-0242 Riemann-Hilbert | unrestricted 版本有反例，正结果范围混杂 | positive theorem、restricted theorem、counterexample 分项 |
| M-0285 Borel-Cantelli | 第一/第二引理前提不同却合并 | 收敛和发散+独立两项分别评分 |
| M-0387 FLT | 人类已证与本仓 machine partial 必须分轴 | exact root；`human=proved`、`formal=partial`，开放 root 不进普通 pass-rate |
| M-0583 四维 Poincare | topological solved 与 smooth open 混合 | 两个 scope、两个状态、两个 source chain |
| M-0706 Church-Turing | 方法论 thesis 错标 theorem | 可证明的模型等价与不可由数学证明的 thesis 分开 |
| M-0769 选择公理 | 公理错标定理 | `claim_kind=axiom`，记录 ZF/ZFC 环境与实际 axiom dependency |
| M-1001 鞅收敛 | “所有鞅 a.s. 收敛”是假 | 分别加入 nonnegative/L1 bounded/uniform-integrability/Lp 前提 |
| M-1226/M-1231 Navier-Stokes | 方程/model 与真正开放正则性题重复 | model record 与 CMI open proposition 分开 |

数学源表 1,666 条中 1,590 条（95.4%）写“已验证”；Stage0 数学 1,601 条中仍有
1,531 条（95.6%）。这不是 formal coverage 统计。至少还需 ordered binders、变量域、量词、
全部前提、边界/退化情形、primary theorem locator 和 exact formal declaration。

## 物理抽查：模型、regime 与证据

1,263/1,263 条物理记录的 regime、近似阶、observable、单位/归一化、误差/数值方案及
EFT/RG 依赖全部仍是占位；1,099 条却显示“已验证”。代表缺口：

| ID | 当前问题 | 应有类别/最低闭包 |
|---|---|---|
| P-0008 单电子晶体管 | 器件不是 theorem | device；结电容、充电能、温度、偏压与 I-V oracle |
| P-0040 摩尔定律 | 历史产业趋势冒充普适定律 | empirical trend；时间窗、工艺/计数口径、拟合与 CI |
| P-0323 RANS | 平均方程与 closure family 未分 | averaged identity + model family；平均算子与 closure |
| P-0343 Hagen-Poiseuille | 公式缺几何与流动假设 | exact model consequence；稳态、层流、不可压、刚性圆管、无滑移 |
| P-0377/P-0857 van der Waals | 摩尔/广延写法重复 | 一个 claim family；EOS convention、相区、参数标定与误差 |
| P-0529 CMB anisotropy | observable/data product 不是单一结论 | dataset/observable；release、频段、mask、foreground、covariance |
| P-0534 NANOGrav | 合作组名称被当命题 | time-stamped observational result；data release、HD correlation、Bayes factor |
| P-0685 AdS/CFT | 研究纲领/猜想被写成已验证 | conjectural duality family；具体 pair、dictionary、large-N/coupling regime |
| P-0748 最小作用量 | “最小”通常应为驻值 | variational stationarity；端点、可微性、约束与 boundary terms |
| P-0763 三体不可积 | “没有解析解”过强 | 固定 Hamiltonian 与 integral class 的 non-integrability theorem |
| P-0853 Stefan-Boltzmann | 把 radiant exitance 与 energy density 混淆 | 区分 `J=sigma T^4` 与 `u=aT^4`；黑体/发射率/SI |
| P-0955 Zeno/anti-Zeno | 相反机制合在一项 | 拆两个 IDs；measurement interval、spectral density、survival probability |
| P-1062 QKD security | “无条件安全”缺协议与对手 | security theorem；设备/信道、finite key、composable epsilon |
| P-1262 confinement | gauge-dependent 口号且 continuum 问题开放 | experiment/model/open-hypothesis 分轨；Wilson criterion 与 mass gap 不混同 |
| P-1263 area law | 与 entanglement area law 同名异义 | namespaced Wilson-loop claim；group、维数、loop family、limits |

物理条目必须把“模型内部可推导”“现实实验/观测支持”“形式系统机器检查”设为三个正交轴。
缺 identity、physical closure 或 track-specific oracle 时，状态只能是 `not_scorable`。

## 计算机科学抽查：模型、资源与对手

398/398 条 CS 记录的 computation model、resource、adversary/security parameter、case
semantics、executable spec、exact statement、evidence 与 target system 全为空。代表硬错：

| ID | 当前问题 | 最低修订 |
|---|---|---|
| C-0004 Rice | “任何程序行为性质”错误包含语法性质 | 固定 acceptable numbering；非平凡、extensional partial-function property |
| C-0037 Impagliazzo-Wigderson | 当前蕴含式不是该定理 | 固定 E 的 exponential circuit lower bound implies BPP=P |
| C-0043 NTIME hierarchy | `f(n)` 与 `f(n+1)` 版本一般为假 | time-constructible 与 `t1(n+1)=o(t2(n))` |
| C-0064 LFKN | `#P subset IP` 函数类/语言类类型错 | 用 #SAT claimed-count interactive protocol 的 completeness/soundness |
| C-0069 Kabanets-Impagliazzo | 当前方向错 | PIT in P implies NEXP circuit lower bound or permanent arithmetic lower bound |
| C-0074 Hastad | 3SAT 判定问题不可谈近似比 | E3-CNF gap：1 与 `7/8+epsilon` 的 NP-hard distinction |
| C-0080 CSP dichotomy | “有限域”误写对象 | 固定 finite domain/constraint language Gamma；P 或 NP-complete |
| C-0084 hash O(1) | 掩盖最坏线性 | hash family/load/randomness 与 expected/worst case 分轴 |
| C-0171 P!=NP 与 OWF | `P!=NP => OWF` 仍开放 | 已知 `OWF => P!=NP` 与 converse-open 两条 |
| C-0214 type safety | preservation 被当完整 safety | preservation 与 progress 分项，再给 not-stuck corollary |
| C-0291 FLP | 模型、故障数、termination 量词缺失 | asynchronous reliable channels、one crash、deterministic/admissible execution |
| C-0294 Byzantine `3f+1` | oral/signed model 混合 | synchronous oral messages 下 `n>3f`；signed variant 另项 |
| C-0338 HHL | 暗示输出全部经典解/polylog 总成本 | sparse access、kappa、epsilon 与 quantum-state output |
| C-0362/C-0363 Shannon | 实质重复 | 一个 DMC capacity family，achievability/converse/strong converse 分项 |
| C-0392 Kolmogorov | “算法信息论基础”不是 proposition | 改为 prefix-machine invariance theorem |

算法、定义、协议、framework 可以保留，但 `kind`、encoding、correctness contract、resource
vector、probability/adversary/fault model 与 executable oracle 必须按类别填写，不能统一走
theorem proof scorer。

## 确定性分层抽样与外推边界

第六名 reviewer 以 `20260810 + stratum_index` 为固定 seed，对六个互斥高风险层各抽六项：
同名异 statement、statement 长度不超过六字、closed-status 对象名、名称/status 冲突、时间
缺失、跨学科同名。36/36 均需要 statement 或 schema 补强；这不是对全库错误率的无偏估计，
而是证明现有风险规则能稳定找到不可直接评分的条目。

全量静态结果进一步显示：

- 3,261/3,262 条仍含 `待补充`，Stage0 共出现 `待补充` 42,472 次；`待选` 6,522 次、
  `待判定` 3,261 次、`待分类` 3,261 次；
- statement 字符数中位数 10、P90 20、P95 24；1,636/3,262（50.15%）不超过十字；
- 使用宽松的中文/符号谓词线索，仍有 2,229/3,262（68.33%）没有 proposition signal；
- 74 个 exact-duplicate groups 贡献 76 个额外 occurrences；去重后仍有 139 个同名组、
  282 条记录，其中 125 组是同名异 statement；
- 65 个同名组跨学科，说明随机逐行 split 会同时遭遇 alias leakage 与不同 sense 误合并；
- 在学科开头插入一行会分别改变 1,601、1,263、398 个现有 ordinal IDs；让任意一条被折叠
  occurrence 重新分裂，漂移数中位数 376.5、最大 1,292；
- 所有 398 个 CS category 留有错误前缀 `. `：数字标题清洗正则只吃掉 `1` 而留下句点；
  category 因而也还不能直接作为 benchmark strata。

固定抽样的代表项包括：C-0004 Rice 缺 extensional/nontrivial/model；M-0580“佩雷尔曼
定理”只是 proof-event 标签；P-1049 量子过程层析是 method；M-1364 Lorenz 系统和 P-1050
Dicke 模型只是 model objects；P-0570 平坦性问题却显示 verified；C-0244 类型擦除正确性缺
源/目标语言；P-0772 Noether theorem 缺作用量、对称与边界；P-1070 threshold theorem 缺
噪声模型、码族和误差范数。

这些 lint 只可用于 triage：短 statement 未必错误（例如 `V=L`）；没有中文谓词会误报纯
符号公式；同名不必重复（三个“谱定理”可为不同 scope）；保留“猜想”的历史名称也不代表
当前仍开放。自动系统必须输出 `same_claim / alias / specialization / refinement / distinct_sense /
needs_review`，不能据 warning 自动 merge 或删除。

## 目标记录与状态模型

最小 canonical record 必须同时包含：

```json
{
  "canonical_id": "CLM-M-<content-bound-id>",
  "legacy_ids": ["THM-M-0023", "THM-M-0517"],
  "source_occurrences": [{"path": "...", "locator": "...", "sha256": "..."}],
  "claim_kind": "theorem|lemma|conjecture|open_problem|axiom|thesis|definition|equation|model|law|effect|algorithm|protocol|non_claim",
  "statement": {"binders": [], "hypotheses": [], "conclusion": null, "scope": null},
  "human_truth": {"status": "proved|refuted|open|partial|independent|conditional|not_applicable|unknown", "as_of": "2026-08-10", "source_refs": []},
  "empirical_status": {"status": "observed|precision_tested|model_supported|disfavored|unobserved|not_applicable|unknown"},
  "external_formalization": {"status": "none|statement_only|partial|kernel_checked"},
  "repo_integration": {"status": "absent|intake|statement_checked|anchor_pinned|proof_checked|release_accepted"},
  "provenance_status": "missing|bibliographic_lead|primary_pinned|independently_reviewed",
  "relations": [],
  "benchmark_tasks": []
}
```

历史名称中的“猜想”不决定 `claim_kind` 或当前 truth status：Quillen-Suslin/Faltings 等可保留
historical alias，同时标 `human_truth=proved`；Riemann hypothesis 等则是 open conjecture。
反之，名称不含“猜想”的 programme/slogan/problem 也不能被词法默认成 theorem。

## Benchmark 接纳门

1. **IDENTITY**：3,338 source occurrences 全保留；canonical/legacy ID 一对多关系可逆；重排和
   前方插入不改现有 canonical IDs。
2. **KIND/ATOMICITY**：封闭 enum；compound claim 拆分或显式 aggregate scorer；非 claim 不进
   theorem denominator。
3. **STATEMENT**：ordered binders、domain、quantifier、全部假设、conclusion、boundary/regime
   与一份可编译 formal surface；名词短语直接拒绝。
4. **STATUS**：human、empirical、formal、repo、provenance 分轴；裸“已验证”是非法可信值。
5. **EVIDENCE**：逐条 primary locator；formal credit 还需 prover/toolchain/revision/file/
   declaration/exact type/imports/axioms/no-placeholder/current replay receipt。
6. **PHYSICS**：变量/单位/模型/几何/frame/gauge/IC/BC/regime/approximation/observable/error/oracle
   缺任何适用关键项则 `not_scorable`。
7. **CS**：encoding/model/resource/case/reduction/randomness/adversary/fault/correctness 缺适用关键项
   则 `not_scorable`。
8. **TASK**：statement proving、given-answer proof、answer+proof、autoformalization、QA、numerical、
   audit 与 open challenge 分轨。
9. **SPLIT/VISIBILITY**：所有 identity/family 连通分量同 split；test pack 无 gold、proof import、
   private locator 或 sibling leakage。
10. **SCORER**：gold positive 通过；wrong theorem、removed hypothesis、changed domain、`sorry`、
    新 axiom、unsafe/oracle、自引用、额外 import、timeout 和 tamper 必须失败。
11. **RIGHTS/PIN**：每个分发资产有 hash/source/license；release、environment、scorer 和 denominator
    ID 集不可变且可离线重放。
12. **METRIC**：预注册 attempt、k、timeout、hardware、seed；同时报告 micro/macro、family/subject/
    difficulty breakdown 与置信区间。

## 当前可安全声称与不可声称

可以声称：本仓库拥有跨数学、物理、CS 的 3,338 条 source-occurrence 研究池；Stage0 对其中
3,262 条构造了历史执行模板；Stage1 对 1,546 个 targets 建立了不同深度的执行资产；M0387
具有局部 pinned Lean closure。

不可声称：2,808 条已经形式化验证；3,262 条是原子 theorem；1,546 targets 构成可比较的
benchmark；任何目录状态能替代 primary evidence；当前 ordinal ID 或字符串去重足以防 leakage。

满足上述接纳门后，目录才可以派生版本化 benchmark。此前它应公开标成 catalog/research
backlog，并把所有 pass-rate denominator 限制在真正有 task、scorer、split、rights 和 replay
证据的 records 上。
