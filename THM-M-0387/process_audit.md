# THM-M-0387 证明过程审计

本文件聚焦：

> 已 machine-checked 的这些分支，证明过程各自是怎么走的？

## statement / reduction 过程表

| 步骤 | 形式化对象 | 数学作用 | 结果 |
|---|---|---|---|
| 1 | `FermatLastTheoremWith` / `FermatLastTheoremFor` / `FermatLastTheorem` | 固定总陈述与固定指数陈述 | 获得统一 statement layer |
| 2 | `fermatLastTheoremFor_iff_int` / `fermatLastTheoremFor_iff_rat` | 在 `ℕ/ℤ/ℚ` 版本间切换 | 可选最适合的证明域 |
| 3 | `fermatLastTheoremWith_of_fermatLastTheoremWith_coprime` | 约化到 primitive solution | 排除缩放冗余 |
| 4 | `FermatLastTheoremWith.mono` / `FermatLastTheoremFor.mono` | 若 `m ∣ n`，由指数 `m` 推指数 `n` | 合数指数被归入约化层 |
| 5 | `FermatLastTheorem.of_odd_primes` | 由 `n = 4` 与所有奇素数指数拼回总 FLT | 顶层拼装完成 |
| 6 | composite exponent split | 解释 `n > 4` 的非素数为何不单列：若 `4 ∣ n` 则归入 `n = 4`；否则某个奇素数 `p ∣ n`，归入奇素数指数分支 | `6, 8, 9, 10, 12, ...` 都被吸收 |

#### repository-local machine boundary note

`n = 4` 的 repo-local theorem-level closure 通过 mathlib import 与 wrapper theorem
`flt4Path` 记录；`n = 3` 的 repo-local theorem-level closure 通过 mathlib import 与
wrapper theorem `flt3Path` 记录。`flt4IntPath` 是从 mathlib 的自然数 / 整数版本等价
派生出的 repo-local wrapper；`flt8ViaFlt4Path` 是用 `FermatLastTheoremFor.mono`
与 `4 ∣ 8` 的指数整除单调性派生出的 repo-local wrapper。完整 `FermatLastTheorem`
不是本仓库 repo-local machine-checked theorem；regular primes theorem closure 属于上游
`flt-regular`，本仓库不 vendoring 证明本体，只保留 anchor-only statement/module/theorem-name 记录。

Local process ledgers and upstream theorem closure are separate layers:
本文件记录本仓库公开过程审计与 proof-step budget；regular primes 的 theorem closure
仍只来自上游 `flt-regular`，不由这些 local process ledgers 重新闭合。

## `n = 4` 过程表

| 步骤 | 形式化对象 | 数学作用 | 结果 |
|---|---|---|---|
| 1 | `Fermat42` | 改写成 `a^4 + b^4 = c^2` | 建立下降入口 |
| 2 | `exists_minimal` | 取最小反例 | 获得最小性不变量 |
| 3 | `coprime_of_minimal` | 最小反例互素 | 排除缩放冗余 |
| 4 | `exists_pos_odd_minimal` | 规整到奇 + 正 | 为分类准备 |
| 5 | `not_minimal` 前半 | 对 `(a^2,b^2,c)` 做 primitive triple 分类 | 得到第一组参数 |
| 6 | `not_minimal` 中段 | 对 `(a,n,m)` 再做 triple 分类 | 抽出平方/四次方结构 |
| 7 | `not_minimal` 后半 | 构造更小反例 | 与最小性矛盾 |
| 8 | `not_fermat_42` | 关掉 bridge problem | 得到无解 |
| 9 | `fermatLastTheoremFour` | 回到原方程 | branch 完闭 |

#### `n = 4` process-tree closure note

`Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/FLT4Path.lean`
在本仓库共享源码树里导入 `Mathlib.NumberTheory.FLT.Four`，并用 wrapper theorem
`flt4Path : FermatLastTheoremFor 4 := fermatLastTheoremFour` 记录 `n = 4`
这条 branch 的 repo-local theorem-level closure；证明实质来自 mathlib import。
在本文件覆盖的过程审计层级内，
`n = 4` 这条 branch 的 canonical package、canonical high-risk leaf，
以及此前单列的 package-level subitem 都已完成独立 `<=100` proof-step ledger 整合。

### `n = 4` 下一层机器节点

| 节点包 | 对应 formal hook | 数学作用 | 备注 |
|---|---|---|---|
| bridge packaging | `Fermat42`, `not_fermat_42`, `fermatLastTheoremFour` | FLT(4) 与桥梁方程之间来回切换 | 外层包裹层 |
| minimal normalization | `exists_minimal`, `coprime_of_minimal`, `exists_pos_odd_minimal` | 取得最小反例并规整到标准形态 | 下降前准备 |
| first triple classification | `PythagoreanTriple.coprime_classification'` | 从 `(a^2, b^2, c)` 取出第一组参数 `(m,n)` | 第一层参数化 |
| second triple classification | `PythagoreanTriple.coprime_classification'` | 从 `(a, n, m)` 取出第二组参数 `(r,s)` | 第二层参数化 |
| coprimality bridge | `Int.isCoprime_of_sq_sum` / `Int.isCoprime_of_sq_sum'` | 为 `b'^2 = m*(r*s)` 的平方提取建立互素接口 | 最容易漏掉的桥接层 |
| square extraction and sign cleanup | `Int.sq_of_gcd_eq_one`, `Or.resolve_right` | 把乘积为平方拆成因子为平方，并排除负平方假分支 | 最高负载 package；canonical high-risk leaf 继续以下游表为准 |
| smaller-solution construction and size comparison | `hh`, `hic`, `hic'` in `Fermat42.not_minimal` | 打包新解并证明它严格更小 | descent 收束 |

#### `n = 4` package 再拆一层

以下 package / `one-more-depth` 子包与 `machine_checked_audit.md`、`eligibles/n4_proof_process.md`
保持同名同步；这些展开项已拥有独立 `<=100` proof-step ledger，
因此下表统一记为 `checked`。

| package | one-more-depth items | status |
|---|---|---|
| `bridge packaging` | `Fermat42 bridge predicate`; `not_fermat_42: normalized witness acquisition`; `not_fermat_42: minimal contradiction handoff`; `not_fermat_42: bridge impossibility closure`; `fermatLastTheoremFour: ℕ ↔ ℤ transport`; `fermatLastTheoremFour: quartic-to-square final closure` | `checked` |
| `minimal normalization` | `minimal witness selection`; `primitive reduction by common-prime descent`; `odd-first-coordinate normalization`; `positive-c normalization` | `checked` |
| `first triple classification` | `ht : PythagoreanTriple (a^2) (b^2) c packaging`; `h2 : Int.gcd (a^2) (b^2) = 1 primitive certificate`; `ha22 : a^2 % 2 = 1 odd-leg certificate`; `raw coprime triple classification`; `PythagoreanTriple.coprime_classification' normal-form pruning` | `checked` |
| `second triple classification` | `PythagoreanTriple a n m packaging`; `Int.gcd a n = 1 transfer`; `0 < m upgrade`; `second PythagoreanTriple.coprime_classification' call`; `r,s output interface` | `checked` |
| `coprimality bridge` | `seed import from second classification`; `single-factor lift via Int.isCoprime_of_sq_sum`; `symmetric single-factor lift`; `product lift via Int.isCoprime_of_sq_sum'`; `API handoff to Int.sq_of_gcd_eq_one` | `checked` |
| `square extraction and sign cleanup` | `even-halving normalization to b'^2 = m * (r*s)`; `square extraction for m`; `square extraction for r*s with sign cleanup`; `split d^2 across coprime r and s`; `square away the residual signs` | `checked` |
| `smaller-solution construction and size comparison` | `sign-normalized fourth-power witnesses`; `new witness equation hh`; `minimality re-instantiation hic'`; `strict natAbs descent hic`; `final contradiction` | `checked` |

#### `n = 4` accepted ledger: `bridge packaging`

`bridge packaging` 的独立 ledger 如下；
总计 `14` 步，满足 `<=100` 约束。

| subitem | step range | status |
|---|---|---|
| `Fermat42 bridge predicate` | `1-2` | `checked` |
| `not_fermat_42: normalized witness acquisition` | `3-6` | `checked` |
| `not_fermat_42: minimal contradiction handoff` | `7-8` | `checked` |
| `not_fermat_42: bridge impossibility closure` | `9` | `checked` |
| `fermatLastTheoremFour: ℕ ↔ ℤ transport` | `10-11` | `checked` |
| `fermatLastTheoremFour: quartic-to-square final closure` | `12-14` | `checked` |

1. `Fermat42` 先把 bridge predicate 定义成 `a ≠ 0 ∧ b ≠ 0 ∧ a ^ 4 + b ^ 4 = c ^ 2`。
2. 因而整条桥梁层的第一步只是把“两个非零条件 + quartic-to-square 方程”打包成单个下降入口。
3. 在 `not_fermat_42` 中，先假设 `h : a ^ 4 + b ^ 4 = c ^ 2`。
4. 用 `And.intro ha (And.intro hb h)` 把 `ha`、`hb`、`h` 组装成 `Fermat42 a b c` witness。
5. 对这个 witness 调用 `Fermat42.exists_pos_odd_minimal`。
6. 得到 `a0 b0 c0` 与 `hf : Minimal a0 b0 c0`、`h2 : a0 % 2 = 1`、`hp : 0 < c0`；这就完成了 normalized witness acquisition。
7. 把 `hf`、`h2`、`hp` 直接交给 `Fermat42.not_minimal`。
8. 该 theorem 立刻给出 `False`，即规范化后的最小反例不可能存在。
9. 因而起始 bridge 方程被排除，收束为 `a ^ 4 + b ^ 4 ≠ c ^ 2`。
10. 在 `fermatLastTheoremFour` 中先用 `rw [fermatLastTheoremFor_iff_int]`，把自然数版本转成整数版本。
11. 于是过程上只需处理整数 `a b c` 与非零假设 `ha hb _`、方程 `heq : a ^ 4 + b ^ 4 = c ^ 4`。
12. 调用 `@not_fermat_42 _ _ (c ^ 2) ha hb`，把桥梁命题的右端实例化成 `c ^ 2`。
13. 用 `rw [heq]; ring` 把输入方程改写成 `a ^ 4 + b ^ 4 = (c ^ 2) ^ 2`。
14. 因而 `not_fermat_42` 与 `heq` 矛盾，最终完成 `FermatLastTheoremFor 4` 的 closure。

#### `n = 4` accepted ledger: `minimal normalization`

`minimal normalization` 的独立 ledger 如下；
总计 `18` 步，满足 `<=100` 约束。

| subitem | step range | status |
|---|---|---|
| `minimal witness selection` | `1-6` | `checked` |
| `primitive reduction by common-prime descent` | `7-12` | `checked` |
| `odd-first-coordinate normalization` | `13-16` | `checked` |
| `positive-c normalization` | `17-18` | `checked` |

1. Start from `h : Fermat42 a b c` and define
   `S := {n : ℕ | ∃ s : ℤ × ℤ × ℤ, Fermat42 s.1 s.2.1 s.2.2 ∧ n = Int.natAbs s.2.2}`.
2. `S` is nonempty by the original witness `(a, b, c)` with `n = Int.natAbs c`.
3. Let `m := Nat.find S_nonempty`; by `Nat.find_spec`, choose `s0 = (a0, b0, c0)` with `hs0 : Fermat42 a0 b0 c0` and `m = Int.natAbs c0`.
4. For any other solution `(a1, b1, c1)` with `h1 : Fermat42 a1 b1 c1`, `Nat.find_min'` gives `m ≤ Int.natAbs c1`.
5. Rewrite by `m = Int.natAbs c0`; this yields `Fermat42 a0 b0 c0` together with `∀ a1 b1 c1, Fermat42 a1 b1 c1 → Int.natAbs c0 ≤ Int.natAbs c1`.
6. Therefore `Minimal a0 b0 c0` holds, so `exists_minimal` closes `minimal witness selection`.
7. For `coprime_of_minimal`, rewrite the goal with `Int.isCoprime_iff_gcd_eq_one`; assume the minimal witness is not coprime.
8. `Nat.Prime.not_coprime_iff_dvd` produces a prime `p` with `p ∣ a` and `p ∣ b`.
9. Use `Int.natCast_dvd` to write `a = (p : ℤ) * a1` and `b = (p : ℤ) * b1`.
10. Substitute these into `a ^ 4 + b ^ 4 = c ^ 2`; `Int.pow_dvd_pow_iff` then gives `(p : ℤ) ^ 2 ∣ c`.
11. Write `c = (p : ℤ) ^ 2 * c1`; then `Fermat42.mul` with multiplier `p` turns the original witness into `hf : Fermat42 a1 b1 c1`.
12. Minimality gives `Int.natAbs c ≤ Int.natAbs c1`, but `Int.natAbs c = p ^ 2 * Int.natAbs c1` and `p ^ 2 > 1`, while `c1 ≠ 0` by `Fermat42.ne_zero hf`; contradiction. Hence `IsCoprime a b`, closing `primitive reduction by common-prime descent`.
13. For odd normalization, start from the minimal witness supplied by steps `1-6` and split on `Int.emod_two_eq_zero_or_one a0`.
14. If `a0 % 2 = 1`, keep `(a0, b0, c0)`; the first coordinate is already odd.
15. If `a0 % 2 = 0`, split on `Int.emod_two_eq_zero_or_one b0`.
16. The branch `b0 % 2 = 0` implies `2 ∣ Int.gcd a0 b0` via `Int.dvd_coe_gcd`, contradicting step `12`; the surviving branch `b0 % 2 = 1` uses `minimal_comm` to swap the legs and preserve minimality. This yields `exists_odd_minimal` and closes `odd-first-coordinate normalization`.
17. For sign normalization, start from the odd minimal witness and apply `lt_trichotomy 0 c0`.
18. If `0 < c0`, keep it; if `c0 = 0`, contradict `Fermat42.ne_zero`; if `c0 < 0`, replace `c0` by `-c0` using `neg_of_minimal`, which preserves minimality and oddness, and `neg_pos.mpr` gives positivity. This yields `exists_pos_odd_minimal` and closes `positive-c normalization`.

跨文件统一的 canonical high-risk leaf 集中在：

1. `raw coprime triple classification`
2. `square extraction for r*s with sign cleanup`
3. `strict natAbs descent hic`

`Int.gcd a n = 1 transfer`
不提升为跨文件统一的 high-risk leaf 名；
它已由 `second triple classification` 的独立 ledger 一并关闭。

#### `n = 4` 选定高风险 leaf 再拆一层

以下高风险 leaf 及其 `one-more-depth` 子包都已由 matching package ledger 关闭；
审计口径仍保持不变，但状态统一记为 `checked`。

| leaf | process-level wording | status |
|---|---|---|
| `raw coprime triple classification` | 先做 `positive-z reduction` 与 `odd-leg dispatch by symmetry`，再进入 `circleEquivGen` 驱动的 `unit-circle rational parameter extraction`，随后通过 parity 分支筛掉不合法 `(m,n)` 形态，最后把 witness 打包回 `coprime_classification` 的原始输出。 | `checked` |
| `square extraction for r*s with sign cleanup` | 先把 `hs` 与 `hcp` 通过 `mul_comm` / `Int.gcd_comm` 改成 `Int.sq_of_gcd_eq_one` 的输入形状，得到 `r*s = d^2 ∨ r*s = -d^2`；再用 `m > 0` 和 `b' ≠ 0` 排除负分支，收束到 `r*s = d^2`。 | `checked` |
| `strict natAbs descent hic` | 先把目标改写成正整数 `c` 上的整数不等式，再沿 `natAbs i ≤ i^2 = m ≤ m^2 < m^2 + n^2 = c` 这条链条收束，其中唯一提供严格性的输入是 `hn : n ≠ 0`。 | `checked` |

| leaf | one-more-depth items | status |
|---|---|---|
| `raw coprime triple classification` | `positive-z reduction`; `odd-leg dispatch by symmetry`; `zero-left degenerate branch`; `unit-circle rational parameter extraction`; `mixed-parity admissible reconstruction`; `forbidden parity branch elimination`; `raw tuple packaging` | `checked` |
| `square extraction for r*s with sign cleanup` | `API orientation for extracting the second factor`; `raw signed-square witness for r*s`; `negative-branch rewrite to a nonpositive RHS`; `strict positivity of the square side`; `sign cleanup to a clean square equation` | `checked` |
| `strict natAbs descent hic` | `natAbs target recast`; `left witness square bound`; `new-witness substitution`; `old-c expansion`; `strict gap from the residual square`; `transitive close` | `checked` |

#### `n = 4` status ledger

顶层 theorem-flow 行继续描述 theorem-level 的 machine-checked 事实；
下表只审计 process-tree 的 `<=100` leaf-budget closure。

`7` 个 canonical package 都已拥有独立 `<=100` proof-step ledger，
因此本节对应的 process-tree `unchecked` surface 已经收束为 `0`。

| canonical package | status |
|---|---|
| `bridge packaging` | `checked` |
| `minimal normalization` | `checked` |
| `first triple classification` | `checked` |
| `second triple classification` | `checked` |
| `coprimality bridge` | `checked` |
| `square extraction and sign cleanup` | `checked` |
| `smaller-solution construction and size comparison` | `checked` |

canonical high-risk leaf set 使用 `Docs/Blueprint_Guidelines.md` 固化的名称；
三项 leaf 均已随 matching package ledger 关闭，不再作为 package row 重复计数。

| canonical high-risk leaf | status |
|---|---|
| `raw coprime triple classification` | `checked` |
| `square extraction for r*s with sign cleanup` | `checked` |
| `strict natAbs descent hic` | `checked` |

本节 `one-more-depth items` 表中列出的全部子项现都继承各自 parent row 的 `checked` 状态。
`n = 4` 过程审计表中已无剩余 package-level unresolved subitem。

## `n = 3` 过程表

默认读者基线是“有大学水平的初等数论能力”。
因此这里不再把 `互素`、`整除传播`、基础模算术逐步拆到教学化碎片层；
过程表只保留真正承担证明工作的节点。

| 步骤 | 形式化对象 | 数学作用 | 结果 |
|---|---|---|---|
| 1 | `fermatLastTheoremThree_case_1` | mod `9` 处理 `3 ∤ abc` | 完成 Case 1 |
| 2 | `fermatLastTheoremThree_of_three_dvd_only_c` | 整数层规整到 `3 ∣ c` | 统一 Case 2 入口 |
| 3 | `FermatLastTheoremForThreeGen` | 引入 `a^3+b^3=u*c^3` | 单位因子显式化 |
| 4 | `Solution'` / `Solution` | 记录下降约束 | 下降对象类型化 |
| 5 | `exists_Solution_of_Solution'` | 转到适于下降的对象 | 保持重数 |
| 6 | `Solution'.multiplicity` | 记录 `λ = ζ₃-1` 的重数 | 获得下降量 |
| 7 | `Solution.exists_minimal` | 在重数上取最小解 | 获得最小性 |
| 8 | `Solution'_descent` | 构造新解 | 下降映射 |
| 9 | `exists_Solution_multiplicity_lt` | 严格下降 | 与最小性矛盾 |
| 10 | `fermatLastTheoremThree` | 回到原方程 | branch 完闭 |

#### `n = 3` process-tree closure note

`Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/FLT3Path.lean`
在本仓库共享源码树里导入 `Mathlib.NumberTheory.FLT.Three`，并用 wrapper theorem
`flt3Path : FermatLastTheoremFor 3 := fermatLastTheoremThree` 记录 `n = 3`
这条 branch 的 repo-local theorem-level closure；证明实质来自 mathlib import。

## regular primes 过程表

| 步骤 | 形式化对象 | 数学作用 | 结果 |
|---|---|---|---|
| 1 | `IsRegularPrime` | class group 视角定义 regularity | Kummer 条件 |
| 2 | `isPrincipal_of_isPrincipal_pow_of_coprime` | `I^p` principal 推 `I` principal | principalization engine |
| 3 | `MayAssume.coprime` | 任意解规整到 primitive solution | 规整层 |
| 4 | `a_not_cong_b` | 排除 Case I 坏同余 | 规整层 |
| 5 | `caseI` | 处理 `p ∤ abc` | Case I 完闭 |
| 6 | `not_exists_solution` 等 | 在分圆域中做 `ζ-1` 幂次下降 | Case II 核心 |
| 7 | `caseII` | 处理 `p ∣ abc` | Case II 完闭 |
| 8 | `flt_regular` | 合并两分支 | generalization 完闭 |

#### regular primes process-tree closure note

本节只审计 regular primes 路线的 process-tree closure。
theorem-level 结果仍以上游 `flt-regular` 为准；本仓库内的
`Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/RegularPrimesPath.lean`
只是 statement shape / upstream module / terminal theorem 的锚点模块，
不是 vendored 证明本体。

因此这里需要同时保留三层口径：

- upstream theorem closure: yes
- repo-local vendored theorem closure: no, anchor-only
- repo-local anchor-only statement/module/theorem-name record: yes

Boundary sentence fixed as:
`upstream theorem closure: yes / repo-local vendored theorem closure: no, anchor-only / repo-local anchor-only statement/module/theorem-name record: yes`

其中最后一段只表示锚点 statement/module/theorem-name 记录已到位，
不表示本仓库已 vendoring 上游 `flt_regular` 证明本体。
本文件后续 `checked` / local ledger 行只审计本仓库的人类可读 process ledger 与 proof-step budget，
不把这些 process ledger 重新解释为 repo-local theorem closure。
因此 local process ledgers 与 upstream theorem closure 是两个分离层级：前者记录本仓库公开过程审计是否补齐，后者仍只来自上游 `flt-regular`。

上游 theorem closure 与 repo-local anchor-only 边界已经固定；
在本文件覆盖的过程审计层级内，
regular primes 路线的 canonical package、canonical high-risk leaf，
以及此前单列的 package-level subitem 都已完成独立 `<=100` proof-step ledger 整合。

### regular primes 下一层机器节点

| 节点包 | 对应 formal hook | 数学作用 | 备注 |
|---|---|---|---|
| setup | `IsRegularPrime`, `isPrincipal_of_isPrincipal_pow_of_coprime` | 定义 regularity 与 principalization engine | 外层代数数论引擎 |
| MayAssume | `MayAssume.coprime`, `MayAssume.p_dvd_c_of_ab_of_anegc`, `a_not_cong_b` | 规整 primitive solution，并固定 Case I / Case II 入口 | 两个主分支共同入口 |
| Case I outer statement | `CaseI.SlightlyEasier`, `CaseI.Statement`, `CaseI.may_assume` | 固定带附加假设的陈述，再消去附加假设 | Case I 外层骨架 |
| Case I ideal extraction | `ab_coprime`, `auxf'`, `auxf`, `exists_ideal` | 线性因子 ideal 表现为 `p` 次幂 | 高负载 package；canonical high-risk leaf 继续以下游表为准 |
| Case I principalization | `is_principal_aux`, `is_principal` | 用 regularity 从 ideal-level 回到 element-level | regular primes 的核心特色 |
| Case I element recovery / close | `ex_fin_div`, `caseI_easier`, `caseI` | 选择生成元、整理单位与同余并收束矛盾 | Case I 最终收口 |
| Case II π-language | `zeta_sub_one_dvd`, `span_pow_add_pow_eq`, `div_one_sub_zeta_mem`, `div_zeta_sub_one_Bijective` | 建立 `π = ζ - 1` 框架和 ideal 分解 | 下降准备 |
| Case II ideal-factor layer | `prod_c`, `exists_ideal_pow_eq_c`, `root_div_zeta_sub_one_dvd_gcd_spec`, `c_div_principal` | 建立 `𝔠 η` 与 `𝔞 η` 的 ideal-level `p` 次幂结构 | 下降前半 |
| Case II distinguished root | `p_dvd_c_iff`, `p_dvd_a_iff`, `p_pow_dvd_c_eta_zero`, `p_pow_dvd_a_eta_zero` | 锁定唯一 ramified root `η₀` | 下降前的局部控制 |
| Case II descent core | `exists_solution`, `exists_solution'` | 从 level `m+1` 下降到 level `m` | 最高负载 package；canonical high-risk leaf 继续以下游表为准 |
| Case II close / merge | `not_exists_solution`, `not_exists_solution'`, `not_exists_Int_solution`, `not_exists_Int_solution'`, `caseII`, `flt_regular` | 最小 `m` 矛盾并合并 Case I / II | 外层收口 |

#### regular primes package 再拆一层

以下 package / `one-more-depth` 子包与 `machine_checked_audit.md`、`eligibles/regular_primes_proof_process.md`
保持同名同步；这些展开项已拥有独立 `<=100` proof-step ledger，
因此下表统一记为 `checked`。

| package | one-more-depth items | status |
|---|---|---|
| `setup` | `IsRegularNumber / IsRegularPrime interface`; `I = 0 base case`; `ClassGroup.mk0_eq_one_iff bridge`; `p-power to class-group torsion`; `orderOf coprimality kill step` | `checked` |
| `MayAssume` | `MayAssume.coprime / divide-by-gcd equation transport`; `MayAssume.coprime / primitive output`; `MayAssume.coprime / nonzero output`; `p_dvd_c_of_ab_of_anegc / ZMod divisibility extraction`; `a_not_cong_b / sign-swap invariants`; `a_not_cong_b / bad-congruence elimination` | `checked` |
| `Case I outer statement` | `SlightlyEasier / Statement interface`; `small-prime cutoff (hodd / hprod / hp5)`; `Case I divisibility transport across gcd quotient`; `primitive normalization via MayAssume.coprime`; `noncongruence normalization and dispatch` | `checked` |
| `Case I ideal extraction` | `ab_coprime core`; `exists_ideal cyclotomic product rewrite`; `exists_ideal pairwise ideal coprimality interface`; `exists_ideal single-factor p-th power extraction`; `f / auxf' / auxf zero-coefficient witness` | `checked` |
| `Case I principalization` | `is_principal wrapper`; `is_principal_aux: certify (I^p).IsPrincipal`; `is_principal_aux: apply regularity`; `is_principal_aux: raise to p-th powers and normalize spans`; `is_principal_aux: unit extraction and final witness` | `checked` |
| `Case I element recovery / close` | `ex_fin_div / principal-generator witness`; `ex_fin_div / k₁,k₂ : Fin p packaging`; `caseI_easier / aux-index exclusion`; `caseI_easier / sparse-sum coefficient close`; `caseI / may_assume wrapper` | `checked` |
| `Case II π-language` | `global π-divisibility of the generalized equation`; `rootwise π-divisibility of linear factors`; `integral quotient packaging`; `residue-class injectivity`; `residue-class bijection` | `checked` |
| `Case II ideal-factor layer` | `𝔠 η residual-ideal extraction`; `residual pairwise coprimality`; `𝔷 = 𝔪 * 𝔷' normalization`; `global product to local p-th powers`; `principal quotient bridge` | `checked` |
| `Case II distinguished root` | `zeta_sub_one_dvd_root selection`; `p_dvd_c_iff local divisibility criterion`; `p_pow_dvd_c_eta_zero_aux off-root coprimality`; `p_pow_dvd_c_eta_zero concentration on the distinguished 𝔠 η₀`; `p_dvd_a_iff / p_pow_dvd_a_eta_zero transfer from 𝔠 to 𝔞` | `checked` |
| `Case II descent core` | `η₀-ideal split`; `quotient principalization`; `α/β representative extraction`; `ideal-to-element balance around η₀`; `three-root formula and raw descent`; `Kummer normalization` | `checked` |
| `Case II close / merge` | `not_exists_solution: generalized-family minimal-m closure`; `not_exists_solution': π-adic normalization of z`; `not_exists_Int_solution: transport from cyclotomic divisibility back to integer divisibility`; `not_exists_Int_solution': primitive gcd cleanup`; `caseII: sign/permutation normalization of the primitive Case II branch`; `flt_regular: final branch merge` | `checked` |

跨文件统一的 canonical high-risk leaf 集中在：

1. `Case II ideal-factor layer / global product to local p-th powers`
2. `Case II distinguished root / p_pow_dvd_c_eta_zero`
3. `Case II descent core / three-root formula and raw descent`
4. `Case II close / merge / not_exists_solution'`

`exists_ideal pairwise ideal coprimality interface` 与
`caseI_easier / aux-index exclusion`
虽然不提升为跨文件统一的 high-risk leaf 名，
但均已随 matching package ledger 一并转为 `checked`。

#### regular primes accepted ledger: `MayAssume`

Source anchor:
`https://github.com/leanprover-community/flt-regular/blob/master/FltRegular/MayAssume/Lemmas.lean`

`MayAssume` 的独立 ledger 如下；
总计 `37` 步，满足 `<=100` 约束。

| subitem | step range | status |
|---|---|---|
| `MayAssume.coprime / divide-by-gcd equation transport` | `1-10` | `checked` |
| `MayAssume.coprime / primitive output` | `11-12` | `checked` |
| `MayAssume.coprime / nonzero output` | `13-16` | `checked` |
| `p_dvd_c_of_ab_of_anegc / ZMod divisibility extraction` | `17-25` | `checked` |
| `a_not_cong_b / sign-swap invariants` | `26-32` | `checked` |
| `a_not_cong_b / bad-congruence elimination` | `33-37` | `checked` |

1. In `MayAssume.coprime`, fix `s := ({a, b, c} : Finset ℤ)` and `d := s.gcd id`.
2. From `hprod : a * b * c ≠ 0`, extract `ha : a ≠ 0`.
3. Use `gcd_dvd` on the three set-memberships to obtain `d ∣ a`, `d ∣ b`, and `d ∣ c`.
4. Show `d ≠ 0`: if `d = 0`, then `Finset.gcd_eq_zero_iff` forces every element of `{a,b,c}` to be zero, contradicting `ha`.
5. Deduce `d ^ n ≠ 0` from `d ≠ 0`.
6. For the transported equation, choose witnesses `na, nb, nc` with `a = d * na`, `b = d * nb`, and `c = d * nc`.
7. Multiply the target equation by `d ^ n`; `mul_left_inj' hdp` reduces the goal to equality after common left-multiplication by the nonzero factor `d^n`.
8. Rewrite `d^n * (a / d)^n`, `d^n * (b / d)^n`, and `d^n * (c / d)^n` using `mul_pow`, the divisibility witnesses, and `Int.mul_ediv_cancel_left _ hdzero`.
9. After those rewrites, the transported goal becomes exactly `a ^ n + b ^ n = c ^ n`.
10. Close that branch with the original hypothesis `H`.
11. For the primitive-output branch, apply `Finset.gcd_div_id_eq_one` to the nonzero member `a ∈ {a,b,c}`.
12. Rewrite by `gcd_eq_gcd_image` and the chosen name `d` to obtain `({a / d, b / d, c / d} : Finset ℤ).gcd id = 1`.
13. For the nonzero-output branch, assume `(a / d) * (b / d) * (c / d) = 0`.
14. Expand with `mul_eq_zero`; there are three cases: `a / d = 0`, `b / d = 0`, or `c / d = 0`.
15. In each branch, use `Int.eq_zero_of_ediv_eq_zero` to pull the zero back to the corresponding original factor.
16. Each pulled-back zero contradicts `hprod`, so `a / d * (b / d) * (c / d) ≠ 0`.
17. In `p_dvd_c_of_ab_of_anegc`, install `Fact p.Prime` so the `ZMod.pow_card` simplification is available.
18. Apply `congr_arg (fun n : ℤ => (n : ZMod p))` to `h : a ^ p + b ^ p = c ^ p`.
19. Simplify the cast equation with `Int.cast_add`, `Int.cast_pow`, and `ZMod.pow_card`; every `p`-th power collapses to the corresponding residue class.
20. Convert `hab` and `hbc` from `Int.ModEq` statements into equalities in `ZMod p`.
21. Rewrite the cast equation using `a = b` and `b = -c` in `ZMod p`.
22. Normalize the rewritten equation by subtraction and `ring_nf`; after simplifying casts and products, the proof reduces to the usual dichotomy “`c = 0` mod `p` or `3 = 0` mod `p`”.
23. Convert the desired branch `c = 0` in `ZMod p` back to divisibility with `ZMod.intCast_zmod_eq_zero_iff_dvd`.
24. Eliminate the exceptional branch `3 = 0` in `ZMod p` via `ZMod.natCast_eq_zero_iff`, then `Nat.dvd_prime Nat.prime_three`, producing only `p = 1` or `p = 3`.
25. Discharge those two possibilities by `hpri.ne_one` and `hp : p ≠ 3`, so the only surviving conclusion is `↑p ∣ c`.
26. In `a_not_cong_b`, split on `H : a ≡ b [ZMOD p]`.
27. If `H` is false, keep the original triple and return `⟨a, b, c, h, hgcd, H, hprod, caseI⟩`.
28. Assume that `H` is true; define the sign-swapped triple `(x,y,z) := (a, -c, -b)`.
29. From `hp5 : 5 ≤ p`, derive `p ≠ 2`, hence `p` is odd by `hpri.eq_two_or_odd'`.
30. Use `neg_pow` together with oddness to rewrite `(-c)^p = -c^p` and `(-b)^p = -b^p`.
31. Rearranging the signs and using `h`, conclude `a ^ p + (-c) ^ p = (-b) ^ p`.
32. Prove gcd-invariance for the swapped triple: rewrite `{a,-c,-b}` as `{a,-b,-c}`, simplify the inserted gcd expression across negatives with `gcd_insert`, `gcd_singleton`, `Int.gcd_eq_natAbs`, and `natAbs_neg`, then discharge the residual sign cases by the four `normUnit` possibilities to recover `hgcd`.
33. For the new noncongruence, assume toward contradiction `habs : a ≡ -c [ZMOD p]`.
34. Since `p ≥ 5`, derive `hp3 : p ≠ 3`; convert both `H` and `habs` to the `ZMod p` equalities expected by `p_dvd_c_of_ab_of_anegc`.
35. Apply `p_dvd_c_of_ab_of_anegc hpri hp3 h H habs` to obtain `↑p ∣ c`, write `c = p * n`, and therefore exhibit `↑p ∣ a * b * c` by rewriting `a * b * c = a * b * (p * n)`.
36. This contradicts `caseI : ¬↑p ∣ a * b * c`, so the swapped triple satisfies `¬x ≡ y [ZMOD p]`; moreover `a * (-c) * (-b) = a * b * c`, so `hprod` transfers to the new product.
37. The same sign-invariant product identity lets `grind` transfer `caseI` to `¬↑p ∣ x * y * z`, completing the witness package for `⟨a, -c, -b⟩`.

#### regular primes 选定高风险 leaf 再拆一层

以下高风险 leaf 及其 `one-more-depth` 子包都已由 matching package ledger 关闭；
审计口径仍保持不变，但状态统一记为 `checked`。

| leaf | process-level wording | status |
|---|---|---|
| `Case II ideal-factor layer / global product to local p-th powers` | 先把 `𝔷 = 𝔪 * 𝔷'` 代回并整理出全局等式 `∏η 𝔠 η = (𝔷' * 𝔭^m)^p`，再用 pairwise coprimality 与 `Finset.exists_eq_pow_of_mul_eq_pow_of_coprime` 逐个抽出 `(𝔞 η)^p = 𝔠 η`。 | `checked` |
| `Case II distinguished root / p_pow_dvd_c_eta_zero` | 先用 `p_dvd_c_iff` 排除所有 off-root 的 `𝔭`-整除，再把它升级成 `gcd (𝔭^(m*p), ∏_{η ≠ η₀} 𝔠 η) = 1`，最后借 `prod_c` 把全部 `𝔭^(m*p)` 压到 `𝔠 η₀`。 | `checked` |
| `Case II descent core / three-root formula and raw descent` | 先取轨道 `η₀, η₀ζ, η₀ζ²`，把三条 root difference 统一改写成 `π` 的 unit 倍，再由 `formula` 做三根消元，并在 `exists_solution` 中打包成 level-`m` 的 raw descended equation。 | `checked` |
| `Case II close / merge / not_exists_solution'` | 先从 `π ∣ z` 的解中抽出最大 `π`-幂，落到 generalized level-`m` 方程族，再经整数 transport、primitive cleanup、Case II 置换归约，最后与 Case I 合并。 | `checked` |

| leaf | one-more-depth items | status |
|---|---|---|
| `Case II ideal-factor layer / global product to local p-th powers` | `exists_ideal_pow_eq_c_aux / RHS normalization`; `prod_c / cyclotomic product expansion`; `prod_c / factorwise 𝔪·𝔠η·𝔭 substitution`; `prod_c / common-factor cancellation`; `exists_ideal_pow_eq_c / pairwise-coprime local extraction`; `root_div_zeta_sub_one_dvd_gcd / witness packaging` | `checked` |
| `Case II distinguished root / p_pow_dvd_c_eta_zero` | `η₀ divisibility criterion import`; `off-root product coprimality`; `gcd-product pivot`; `distinguished factor reinsertion into total product`; `visible 𝔭^(m*p) extraction from global p-th power` | `checked` |
| `Case II descent core / three-root formula and raw descent` | `three-root orbit selection`; `root-difference as unit·π`; `three-root cancellation identity`; `raw descended triple packaging`; `raw nondivisibility certification` | `checked` |
| `Case II close / merge / not_exists_solution'` | `generalized-family minimal-m closure`; `π-adic normalization of z`; `integer transport`; `primitive gcd cleanup`; `caseII permutation close`; `final merge` | `checked` |

#### regular primes status ledger

顶层 theorem-flow 行继续描述 theorem-level 的 machine-checked 事实；
下表只审计 process-tree 的 `<=100` leaf-budget closure。

`11` 个 canonical package、`4` 个 canonical high-risk leaf，
以及此前单列的 `2` 个 package-level unresolved subitem
都已拥有独立 `<=100` proof-step ledger，
因此本节对应的 process-tree `unchecked` surface 已经收束为 `0`。

| node / leaf | status |
|---|---|
| `setup` | `checked` |
| `MayAssume` | `checked` |
| `Case I outer statement` | `checked` |
| `Case I ideal extraction` | `checked` |
| `Case I principalization` | `checked` |
| `Case I element recovery / close` | `checked` |
| `Case II π-language` | `checked` |
| `Case II ideal-factor layer` | `checked` |
| `Case II distinguished root` | `checked` |
| `Case II descent core` | `checked` |
| `Case II close / merge` | `checked` |
| `Case II ideal-factor layer / global product to local p-th powers` | `checked` |
| `Case II distinguished root / p_pow_dvd_c_eta_zero` | `checked` |
| `Case II descent core / three-root formula and raw descent` | `checked` |
| `Case II close / merge / not_exists_solution'` | `checked` |

本节 `one-more-depth items` 表中列出的全部子项现都继承各自 parent row 的 `checked` 状态。
此前曾单列的
`exists_ideal pairwise ideal coprimality interface`
与 `caseI_easier / aux-index exclusion`
也已随 matching package ledger 一并关闭；
regular primes 过程审计表中已无剩余 package-level unresolved subitem。

## v5.5 scheduler closeout evidence

- `K01`: `2026-04-26 11:15:45 CST (+0800)` ran `tmux list-sessions -F '#{session_name}'`; active sessions were `alphane-admin-frontend`, `alphane-backend`, `alphane-new-web`, and `awesome_theorems_thm_m_0387_v55_closeout_slot1`.
- `K01`: the active `THM-M-0387` v5.5 session was identified by `tmux display-message -p '#S'` as `awesome_theorems_thm_m_0387_v55_closeout_slot1`, i.e. the lead-reviewer closeout lane. The worker-session filter `tmux list-sessions -F '#{session_name}' | rg 'awesome_theorems_thm_m_0387_v55_(worker|slot[0-9]+)$|awesome_theorems_thm_m_0387_v55_worker|automation_repo_slot[0-9]+_worker'` returned no matches with exit code `1`, confirming no v5.5 worker tmux sessions were still running at that timestamp.
- `K02`: `2026-04-26 11:20:38 CST (+0800)` ran `ps -axo pid=,ppid=,stat=,command= | rg 'codex exec.*awesome_theorems/\.cron/automation_repo_slot[0-9]+'`; it still matched the active `codex exec` process for `/Users/wangweiyang/GitHub/awesome_theorems/.cron/automation_repo_slot1` (`PID 36542`, child `PID 36577`). Therefore K02 is not confirmed and remains unchecked in `fix_blueprint_v5_5.md`.
- `K02`: `2026-04-26 11:25:34 CST (+0800)` reran `ps -axo pid=,ppid=,stat=,command= | rg 'codex exec.*awesome_theorems/\.cron/automation_repo_slot[0-9]+'`; it still matched the active `codex exec` process for `/Users/wangweiyang/GitHub/awesome_theorems/.cron/automation_repo_slot1` (`PID 69593`, child `PID 69607`). Therefore K02 is not confirmed and remains unchecked in `fix_blueprint_v5_5.md`.
- `K02`: `2026-04-26 11:30:27 CST (+0800)` reran `ps -axo pid=,ppid=,stat=,command= | rg 'codex exec.*awesome_theorems/\.cron/automation_repo_slot[0-9]+'`; it still matched the active `codex exec` process for `/Users/wangweiyang/GitHub/awesome_theorems/.cron/automation_repo_slot1` (`PID 10891`, child `PID 10916`). Therefore K02 is not confirmed and remains unchecked in `fix_blueprint_v5_5.md`.
- `K02`: `2026-04-26 11:35:34 CST (+0800)` reran `ps -axo pid=,ppid=,stat=,command= | rg 'codex exec.*awesome_theorems/\.cron/automation_repo_slot[0-9]+' | rg -v "rg 'codex exec"`; it still matched the active `codex exec` process for `/Users/wangweiyang/GitHub/awesome_theorems/.cron/automation_repo_slot1` (`PID 43509`, child `PID 43510`). Therefore K02 is not confirmed and remains unchecked in `fix_blueprint_v5_5.md`.
- `K02`: `2026-04-26 11:40:22 CST (+0800)` reran `ps -axo pid=,ppid=,stat=,command= | rg 'codex exec.*awesome_theorems/\.cron/automation_repo_slot[0-9]+' | rg -v "rg 'codex exec"`; it still matched the active `codex exec` process for `/Users/wangweiyang/GitHub/awesome_theorems/.cron/automation_repo_slot1` (`PID 92567`, child `PID 92574`). Therefore K02 is not confirmed and remains unchecked in `fix_blueprint_v5_5.md`.
- `K02`: `2026-04-26 11:45:33 CST (+0800)` reran `ps -axo pid=,ppid=,stat=,command= | rg 'codex exec.*awesome_theorems/\.cron/automation_repo_slot[0-9]+' | rg -v "rg 'codex exec"`; it still matched the active `codex exec` process for `/Users/wangweiyang/GitHub/awesome_theorems/.cron/automation_repo_slot1` (`PID 64191`, child `PID 64194`). Therefore K02 is not confirmed and remains unchecked in `fix_blueprint_v5_5.md`.
- `K02`: `2026-04-26 11:50:29 CST (+0800)` reran `ps -axo pid=,ppid=,stat=,command= | rg 'codex exec.*awesome_theorems/\.cron/automation_repo_slot[0-9]+' | rg -v "rg 'codex exec"`; it still matched the active `codex exec` process for `/Users/wangweiyang/GitHub/awesome_theorems/.cron/automation_repo_slot1` (`PID 29077`, child `PID 29083`). Therefore K02 is not confirmed and remains unchecked in `fix_blueprint_v5_5.md`.
- `K02`: `2026-04-26 11:52:02 CST (+0800)` reran `ps -axo pid=,ppid=,stat=,command= | rg 'codex exec.*awesome_theorems/\.cron/automation_repo_slot[0-9]+' | rg -v "rg 'codex exec"`; it returned no matches with exit code `1`, confirming no `codex exec` process was still running inside `.cron/automation_repo_slot*` at that timestamp.
- `K03`: `2026-04-26 11:52:02 CST (+0800)` ran `git diff --cached --name-only`; it returned no paths, confirming no runtime state was staged before closeout staging. The same pass ran `git status --short --untracked-files=all`, which listed only `THM-M-0387/fix_blueprint_v5_5.md` and `THM-M-0387/process_audit.md`, and ran `git ls-files | rg '(^|/)(\.cron|\.ops|logs?|worker|automation_repo_slot)'`, which returned no tracked runtime paths with exit code `1`.
