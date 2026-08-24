# THM 总目录、猜想状态与 ID 六视角审计

> 审计日期：2026-08-10
>
> 审计对象：3,338 条 source occurrences、3,262 条 Stage0 legacy projection、
> Stage1 identity/status surfaces 与现有生成器
>
> 基线：`main` 起始提交 `9c299dbabd34878a420db46ca66d687886fe2b04`
>
> 文档性质：第三轮恰好六名新 reviewer 的只读审计汇总；不是 truth certification、
> canonical registry release、benchmark release 或 blueprint 外的第二任务游标。

## 结论

现有 `THM-{M|P|C}-NNNN` 是一次去重后展示顺序，不是稳定 claim identity。目录目前也不能
被称为“3,262 个定理”：它混合 theorem、lemma、historical/open conjecture、hypothesis、
axiom、definition、equation、model、law、effect、algorithm、protocol、framework、proof event、
device、observation 与只有名词的 ontology entry。

六个独立视角共同支持以下迁移方向：

```text
3338 source occurrences (全部保留)
  -> family / disambiguated sense / atomic scoped variant
  -> zero or more formal statement variants
  -> zero or more versioned benchmark tasks
```

旧 THM ID 必须永久可解析，但不得再随源表重排而重新分配。分类和 truth status 都不能编码进
canonical ID，因为“猜想”可被证明、scope 可被拆分、学科 tag 也可多值。推荐 append-only 的
opaque registry：`ATO` 标 source occurrence，`ATF` 标 family，`ATS` 标 sense，`ATV` 标精确
variant；所有 ID 一经分配永不删除、复用或重算。

## 六个独立审查视角

| 一级 reviewer task | 审查面 |
|---|---|
| `/root/catalog_math_kind` | theorem/lemma/conjecture/axiom/definition/equation/algorithm/proof event/thesis 的全量 triage |
| `/root/catalog_physics_kind` | theorem/law/model/effect/observation/device/framework/open problem 与 regime/sense |
| `/root/catalog_cs_kind` | theorem/algorithm/protocol/definition/security game/framework/thesis 与 computation/adversary/fault model |
| `/root/catalog_open_status` | historical/open/refuted/independent/conditional、scope split、status source 与日期 |
| `/root/catalog_id_registry` | occurrence/family/sense/variant、legacy alias、split/merge/redirect、receipt migration 与 mutation tests |
| `/root/catalog_cross_domain` | taxonomy 失衡、同名/重复/粒度、经典结果缺口与 catalog/benchmark 分轨 |

六名 reviewer 均未修改仓库，也未再派生 subagent。
这里的“六名”指六个一级审查 task；本汇总保存角色与结论，但不把协作 thread transcript
冒充六份仓库内签名 attestation。随后同一批 reviewer 接受了互不重叠的 Catalog v2 实施任务，
不改变本节只读审查阶段的证据边界。

## 不可逆损失与身份漂移

| 层 | 数量/事实 |
|---|---:|
| 原始 source occurrences | 3,338 = M 1,666 + P 1,272 + C 400 |
| Stage0 legacy records | 3,262 = M 1,601 + P 1,263 + C 398 |
| 被六字段 exact 去重折叠 | 76 occurrences |
| exact duplicate clusters | 74：72 个二元簇、2 个三元簇 |
| 跨域 exact cluster | 仅 Hamming 界：数学与 CS occurrence |
| 去重后同名 clusters | 139 组、282 条；65 组跨域 |

现有 signature 包含会变化的 `importance/status`，却漏 discipline、subcategory、source path 和
CS source domain；它既会把 Hamming 的 CS provenance 删除，也无法合并不同措辞的 BWT。
`assign_ids()` 再按当前顺序计数：在数学列表最前插一项，旧 `THM-M-0387` 会漂成 0388，
而字符串 `THM-M-0387` 会静默指向原 M0386。这足以否定其作为 citation key、receipt join key
或 benchmark identity 的资格。

`THM-M-0133`/`THM-M-0387` 是更危险的语义碰撞：前者是“Wiles proof”事件，后者是 FLT root，
但 Stage1 把二者冻结成同一个 statement fingerprint。0133 必须重型为 proof event 或更精确
modularity claim，其错误工件不能让 FLT 被计算两次。

## 数学 kind 全量结果

Stage0 数学 1,601 项的现有实际分布是：generic theorem 1,470、formula/identity 38、
open aggregate 32、lemma 31、problem 29、M0387 override 1。分类器完全没有 axiom、definition、
equation、algorithm、method、model、proof artifact、thesis 或 historical-conjecture-name 分支。

强标题线索也被压成 generic：11/11 个“公理”、24/24 个“算法”、11/11 个“证明”、
64/64 个“理论”、34/36 个“方程”、35/55 个“猜想”。代表迁移：

| Legacy | 当前混型 | 建议 kind/relation |
|---|---|---|
| M-0023/M-0517 | 岩泽主猜想重复且 scope 不明 | historical conjecture -> proved theorem family；先固定 cyclotomic/character scope |
| M-0033/M-0034 | Serre 猜想与 Quillen-Suslin proof/result 分离 | canonical claim + historical alias + proof event |
| M-0114 | Hodge 只有开放名词摘要 | exact open conjecture；只进 open-challenge |
| M-0122/M-0123/M-0395 | Faltings/Mordell/proof event 重复 | 一个 family，claim 与历史/proof occurrences 分层 |
| M-0183 | Calabi statement 写强 | prescribed Ricci theorem；Ricci-flat corollary 加 `c1=0` |
| M-0191 | Weil 四个 claims 聚合 | rationality/FE/Betti/RH-weights 四 variants |
| M-0241/M-0242 | Riemann-Hilbert 正结果与反例混合 | unrestricted counterexample、restricted theorem 分项 |
| M-0285 | 第一/第二 Borel-Cantelli 合并 | 两个 lemmas，假设独立评分 |
| M-0485/M-0902 | 已否证历史猜想 | `historical_conjecture + refuted`，绑定 witness |
| M-0583 | topological 4D solved 与 smooth 4D open | 必须 split 两个 variants |
| M-0706 | Church-Turing 错标 theorem | thesis；模型等价 theorem 另项 |
| M-0712 | Hilbert 10 写“已否证” | decision problem 的 proven negative solution |
| M-0769 | choice 错标 theorem | axiom；ZF/ZFC 与 dependency 另轴 |
| M-0775/M-0776/M-0796/M-0802 | independence 与 axiom/claim 混合 | relative-independence records，明确 base theory |
| M-1034/M-1226/M-1525/M-1527 | integral/PDE/物理方程对象 | construction/equation/model；存在性等 claim 作 child |
| M-0133/M-0580/M-0836/M-0838 | proof 事件被算 theorem | `proof_event_for`，保存 artifact identity |
| M-0472/M-0823/M-0825/M-1571 | algorithm 对象被算 theorem | algorithm；correctness/termination/resource children |

## 物理 kind 与同名 sense

1,263 条物理项中 988 条仍是 generic，且 1,263/1,263 的 exact definition、六个 regime
字段、evidence/artifact 全为空。名称实际含 80 个“定理”，路由表却没有 theorem 分支；
公式、恒等式、方法、近似、猜想/假说、observation/device 也没有可信路由。

31 个同名 clusters/62 rows 的逐组判读得到约 17 个 merge candidates、9 个 family/variant
clusters、5 个硬同名 clusters。代表项：

| Legacy | 判定 |
|---|---|
| P-0010/P-0952、P-0011/P-0953 | weak localization/UCF 同 claim，多 occurrence |
| P-0094/P-1000 | topological-insulator 同实体但 raw status 冲突 |
| P-0141/P-1021 | Heisenberg model 的相反 `J` 号 convention；同 family、不同 sense |
| P-0311/P-0372 | fluid Euler equation 与 thermodynamic Euler identity；硬同名 |
| P-0377/P-0857 | van der Waals extensive/molar variants |
| P-0494/P-0668 | relativistic Doppler approaching/receding convention |
| P-0499/P-1099 | wave dispersion 与 scattering dispersion relation；硬同名 |
| P-0898/P-1263 | entanglement area law 与 Wilson-loop area law；绝不能 merge |
| P-1143/P-1262 | confinement observation/model/open rigorous claim 同 family分层 |
| P-0005/P-1015 | Aharonov-Bohm 的翻译 alias |

`P-0040` 应是 empirical trend，`P-0534` 是 time-stamped observation/dataset，`P-0685` 是
conjectural framework，`P-0701` 是 proposal/hypothesis，`P-0832` 是 molecular-chaos assumption，
`P-1040` 才是 scoped no-cloning theorem，`P-1070` 是依赖 noise model 的 theorem family，
`P-1161` 是 framework。它们不能共享一个 proved/formalized 状态。

## CS kind 与模型边界

CS source 400、Stage0 398。人工逐条主对象 triage 为：

| 建议主 kind | 数量 |
|---|---:|
| theorem candidate | 176 |
| algorithm | 69 |
| framework/method | 37 |
| protocol/scheme | 31 |
| aggregate/topic，必须拆 | 26 |
| definition | 25 |
| model/construction | 24 |
| conjecture | 4 |
| open programme | 3 |
| security definition/game | 2 |
| thesis | 1 |

至少 222/398 不是干净 theorem record，其中 81 条却显示 raw“已验证”。现有关键词分类对
algorithm 只命中 27/69、protocol 2/31，对 definition/conjecture/open/thesis 全部零命中。

代表迁移包括：C-0002 thesis；C-0011 definition；C-0035 Berman-Hartmanis open conjecture；
C-0076 algorithm 与 approximation theorem 分层；C-0171 拆 `OWF => P!=NP` theorem 和 converse
open claim；C-0181 security definition/game；C-0185 Fiat-Shamir heuristic transform，按 ROM/
QROM variant；C-0202 ElGamal algebraic correctness 与 DDH security 分开；C-0242 compiler
correctness theorem schema；C-0300 open programme；C-0311 linearizability definition；C-0338
HHL algorithm；C-0392 若要进 theorem 轨，应改成 prefix-machine invariance theorem。

CS source footer 自己也已漂移：实际 importance 为 310/88/2，文档写 280/100/20；实际
status 为 180/211/8/1，文档写 200/180/20 且漏“不可形式化”。40/40 category 还有 `. `
前缀清洗 bug。

## 开放、历史、反例、独立与条件状态

名称含猜想/假设/假说/问题/悖论/Millennium 的候选共 135：数学 98、物理 22、CS 15；其中
71 项显示 closed 类状态。另有 55 个 open/partial 候选和 8 个 refuted/independent/
undecidable 候选被生成成普通命题。`infer_proposition_type()` 漏掉 `部分证明/部分进展/待研究/
声称证明/独立于ZFC/已否证/不可判定`，而 CS 仅因名称含“问题”产生的七个 open 标签又全是假阳性。

必须分开的语义：

- historical conjecture 已解决：保留历史名，current claim 标 theorem/proved，proof paper 另作 event；
- open：有 exact scope、`status_as_of` 与近期权威 status source；
- refuted：具体 counterexample/witness；
- negative solution：一个 decision/existence problem 被证明无算法/无对象，不等于 claim 被 refuted；
- independent：正反相对一致性方向、base theory 与 consistency assumptions；
- conditional theorem：implication 可 proved，但 conclusion 不继承 proved；
- claimed/disputed proof：primary claim 与独立评述未满足 policy 前保持 unresolved。

截至 2026-08-10 的优先 scope audit 包括六个未解决 Clay families、ABC disputed status、
André-Oort full-generality preprint claim、Zimmer programme 的已证精确版本、三维 Kakeya set 的
2025/2026 proof claims与不同 Kakeya maximal claim、cosmic censorship weak/strong variants、
Navier-Stokes equation/object 与 regularity problem、graph-isomorphism quasipolynomial upper bound
与仍开放的 complexity classification。

每个 current-status change 必须 append-only 记录：`historical_kind`、`current_claim_kind`、
`truth_status`、`scope`、`as_of`、`resolved_at`、`conditional_on[]`、`base_theory`、
`consistency_assumptions[]`、evidence/formal/repo axes 与 source locator。

## 推荐 append-only ID registry

### 层次

```text
ATO-00000001  source occurrence
ATF-00000001  family / proof-leakage component
ATS-00000001  disambiguated sense
ATV-00000001  exact scoped variant; public canonical catalog ID
TASK-...       versioned benchmark task derived later
```

ID 只编码实体层次，不编码学科、kind、truth 或文本 hash。内容 hash 绑定 revision；identity 由
append-only registry 保存。Bootstrap 可将当前 3,338 occurrences 与 3,262 legacy variants
按冻结快照顺序一次性分配；之后任何新对象只领取 `next_serial`。分配由单写者以 registry
前置 SHA 和 idempotency request digest 做 compare-and-swap；允许编号空洞，禁止复用。

不存在合法的 discipline-offset 迁移公式。ATV bootstrap 按全部 3,338 个 source occurrences
分配，legacy THM IDs 却只覆盖 3,262 个 Stage0 survivors；每个 alias 因而必须由内容绑定的
3,262-entry migration map 解析。例如当前映射是：

```text
THM-M-1601 -> ATV-00001666
THM-P-0001 -> ATV-00001667
THM-C-0001 -> ATV-00002939
```

任何由 `THM-{domain}-ordinal` 算术推导 ATV 的实现都必须失败。旧 alias 永久解析到其冻结
历史 ATV。若 aggregate 以后 split，旧 ATV 标 `split` 并返回多个 current children，不能偷偷
挑一个；历史 proof/receipt 不自动继承。若 confirmed duplicate merge，较晚 record 一跳
redirect 到 survivor，但 artifacts 仍逐项审 applicability。

### 关系

最低枚举：

```text
legacy_exact_duplicate
same_claim
checked_equivalent
specializes / generalizes / refines
historical_name_of / translation_of
same_name_different_claim
proof_event_for
```

六字段相同只能自动标 `legacy_exact_duplicate`，不能推断 semantic equality。只有冻结了数学
binders/domain/hypotheses/conclusion，物理 model/regime/units/observable，或 CS computation/
resource/adversary/probability 后，加人工裁决、primary identity 或 checked equivalence，才可
升级 `same_claim`。Family 共属只防 leakage，不授予 proof credit。

### Source locator

跨版本“byte-stable absolute offset”并不存在。每个 ATO 应保存不可变 birth locator
`(git blob, byte range, raw-block SHA)`，另保存当前 path/section/anchor/line hint。3,338 occurrences
包括 76 个历史上被折叠的成员，必须 100% 可逆。

Stage1 历史 receipt 不重写；给它增加绑定 legacy ID、canonical ID、registry revision 和 artifact
SHA 的 migration envelope。

## 覆盖缺口不是 benchmark task

对 MSC2020、APS PhySH、ACM CCS 与经典 family 的 bounded alias probe 找到 62 个零命中候选：
数学 24、物理 18、CS 20。其中包括 Jordan curve、Borsuk-Ulam、Serre duality、optional
stopping、Neyman-Pearson、Collatz/Jacobian/Schanuel；Kochen-Specker、Haag、Coleman-Mandula、
Lieb-Robinson、GR Birkhoff、quantum adiabatic；NP vs coNP、L vs NL、ETH/SETH、3SUM/OV/APSP、
LWE/SIS assumptions、MIP*=RE、PAC fundamental theorem 与 Sauer-Shelah。

这只证明在冻结 alias probe 下缺少 atomic record，不证明目录“逻辑不完整”，也不授权自动
新增 62 IDs。14 项是 open/hardness assumptions，只能做 catalog/open/conditional inputs；48 项
即使是已知 theorem，也要先有 exact statement、primary evidence、rights 与 relation review。
P vs NP 的 CS occurrence、Modularity theorem 与若干物理 parent theorem 应优先 crosswalk 到
已有 family，而不是重复 canonical claims。

目录 scope 必须先冻结。当前数学 37 类中 PDE+“其他”占 29.73%；物理 208 子类中 85 个只有
1--2 条；CS 38/40 类恰好十条，显示固定配额而非自然覆盖。若 CS 有意只覆盖 theory，明确写
`scope=theoretical_cs`；不要暗称完整 ACM computing catalog。

## 实施与验收门

1. **Occurrence conservation**：恰好 3,338 ATO；76 个折叠成员恢复；Hamming 同时保留 Math/CS provenance。
2. **Legacy resolution**：3,262 个 THM IDs 永久、唯一解析到历史 ATV；alias 不可重绑。
3. **ID stability**：源重排、前插、status/importance/category/kind/domain 修订均不改变已分配 ID。
4. **Kind/atomicity**：封闭 enum；family/entity/aggregate 不进 atomic theorem denominator。
5. **Sense review**：139 同名 clusters 显式裁决；硬同名禁止自动 merge，near duplicate 禁止自动 delete。
6. **Status source**：open/refuted/independent/disputed 无 exact scope、日期和 source 时 hard fail。
7. **Split/merge**：split 返回 multiple children 且不继承证据；merge redirect 一跳、无环、不复用 ID。
8. **Receipt migration**：历史 artifact hash 不改写，增加 pinned registry-revision envelope。
9. **Taxonomy**：多值 MSC/PhySH/ACM crosswalk；未覆盖需 `out_of_scope_reason`。
10. **Benchmark derivation**：仅 atomic statement + provenance/rights + environment + scorer + gold/replay 全过才生成 TASK。
11. **Open exclusion**：open/hypothesis/hardness assumption 不进普通 theorem-proof pass-rate。
12. **Family-safe split**：alias、variants、共享 proof/source/dependency family 的连通分量同 split。

最低 mutation suite 应覆盖：baseline 3338/3262/74/76；唯一跨域 exact Hamming；front insertion/
reorder/status edit 稳定；Unicode/punctuation 不重编号；same-name ambiguity；0133/0387 formal
fingerprint collision；legacy alias 不可重绑；split 无默认 child/无 evidence inheritance；merge
一跳无环；hash collision unequal payload fatal；allocator CAS/idempotency；tombstone 不复用；历史
receipt 按 pinned registry revision 解析；同输入再生 byte-deterministic。

## 安全公开口径

Stage0 是 3,262 条 legacy display records，不是 3,262 个 theorem。Catalog v2 发布时应同时报告：

```text
source_occurrence_count
legacy_projection_count
allocated_variant_count
active_atomic_claim_count
benchmark_task_count
```

这些计数不得互相替代。最优先工作不是扩表，而是先冻结 occurrence registry、修复 kind/status/
sense 与 36 类已知 identity collision；之后才审查缺失候选，最后只从过门的 atomic claims 派生
benchmark tasks。
