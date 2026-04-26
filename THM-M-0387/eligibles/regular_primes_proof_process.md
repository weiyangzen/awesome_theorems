# THM-M-0387 regular primes 证明过程展开稿

## 1. 范围

这里解释的是：

> 对任意奇 regular prime `p`，费马大定理指数 `p` 的情形成立。

也就是 formal 结果：

- `caseI`
- `caseII`
- `flt_regular`

这部分不是 `mathlib` 主库里的一个小特例，
而是 `flt-regular` 项目的主体成果。

## 2. 这条分支到底证明了什么

它证明的不是“全部 FLT”，而是：

> 当指数是一个奇 regular prime 时，`a^p + b^p = c^p` 没有非平凡整数解。

形式化终点是：

- `flt_regular {p} ... : FermatLastTheoremFor p`

因此它是一个中间 generalization：

- 比 `n = 3`、`n = 4` 强得多；
- 但仍然远小于完整的 Wiles / Taylor-Wiles 总证明。

## 3. 对应的 formal 入口

本分支中最关键的对象和定理是：

- `IsRegularPrime`
- `isPrincipal_of_isPrincipal_pow_of_coprime`
- `MayAssume.coprime`
- `a_not_cong_b`
- `caseI`
- `caseII`
- `flt_regular`

如果按证明流程看，可以分成三层：

1. regularity 的代数数论引擎
2. Case I：`p ∤ abc`
3. Case II：`p | abc`

最后再把 Case I / II 合并。

## 4. 第一层：regular prime 到底在这里起什么作用

formal definition 是：

- `IsRegularNumber`
- `IsRegularPrime`

其内容是：

> `p` 与 `p` 次分圆域整数环的 class group 基数互素。

从证明角度看，regularity 真正承担的角色不是“标签”，而是下面这条 principalization engine：

- `isPrincipal_of_isPrincipal_pow_of_coprime`

它的含义可以概括成：

> 如果一个 ideal 的 `p` 次幂是 principal，且 `p` 与 class group 阶互素，
> 那么这个 ideal 本身就已经 principal。

这一步非常关键，因为 Kummer 路线的核心结构就是：

1. 先把某个理想证明成 `p` 次幂；
2. 再用 regularity 把它“降回” principal。

如果没有这条引擎，后面的 ideal-level factorization 无法回到 element-level。

## 5. 第二层之前的统一规整：primitive solution

无论是 Case I 还是 Case II，formal proof 都不会直接对任意整数解开打。

它先把任意候选解规整成 primitive solution。

这一步对应：

- `MayAssume.coprime`

在数学上它做的是：

1. 去掉公共因子；
2. 保留非零性；
3. 保留原方程的本质矛盾结构。

这样之后讨论的对象都满足：

- `gcd(a, b, c) = 1`

这是后面“`p` 最多整除三者之一”以及分支讨论的前提。

## 6. 总体拆分：Case I 与 Case II

对于指数为奇素数 `p` 的 FLT，经典上就分成：

- Case I：`p ∤ abc`
- Case II：`p | abc`

formal 结果也完全按这个结构组织：

- `caseI`
- `caseII`

最后由：

- `flt_regular`

合并成

`FermatLastTheoremFor p`

这意味着：

> `flt_regular` 不是一个黑箱 theorem，
> 它只是把两条已经闭合的分支拼起来。

## 7. Case I 的人类可读证明过程

### 7.1 目标

Case I 要排除的是：

- `a^p + b^p = c^p`
- `p ∤ abc`

对应 formal theorem：

- `caseI`

### 7.2 进入 `p` 次分圆域

令 `K = ℚ(ζ_p)`，其整数环记作 `O_K`。

在这里，方程分解成：

`a^p + b^p = ∏_{η ∈ μ_p} (a + η b)`

其中 `μ_p` 是所有 `p` 次单位根。

这和 `n = 3` 分支很像，但这里的单位根个数是 `p` 个，不是 `3` 个。

### 7.3 排除坏同余形态

formal proof 里有一个专门的规整结果：

- `a_not_cong_b`

它的作用是排除 Case I 中某种坏同余配置，
使得后续对这些因子 `(a + ηb)` 的 ideal 讨论更干净。

粗略地说，这一步是在确保：

> 各个线性因子之间除了唯一可能的上方素理想外，不会发生额外的公共因子纠缠。

### 7.4 从元素分解切到 ideal 分解

由于

`∏ (a + η b) = c^p`

在 ideal 层面上可以看出：

- 每个 `(a + ηb)` 生成的 principal ideal，
  在去掉 ramification 噪声后，都应表现得像一个 `p` 次幂 ideal。

formal proof 里和这一层对应的结果包括：

- `exists_ideal`
- `is_principal`

逻辑是：

1. 先从乘积是 `p` 次幂出发，
   说明各个因子理想本身也是 `p` 次幂理想。
2. 再利用 regularity，
   把“`I^p` principal”反推出 “`I` principal”。

这正是上一节讲的 principalization engine 真正发力的地方。

### 7.5 从 principal ideal 回到元素

一旦知道各相关 ideal 都是 principal，
就可以为它们选生成元，
把每个线性因子写成：

> 单位 × `p` 次幂

这一步在纸面证明里往往写得很快，
但 formalization 里其实需要大量单位、范数、共轭、整除结构的辅助引理。

从人类视角看，它的含义是：

> 你终于把 ideal-level 的 `p` 次幂信息，
> 拉回到了 element-level 的 `p` 次幂信息。

### 7.6 最后的矛盾来自哪里

当你把

`a + ζ_p b`

写成“单位 × `p` 次幂”之后，
再配合 Case I 的假设 `p ∤ abc` 与排好的同余条件，
就能推出不可能成立的局部同余结论。

formal proof 在这里用若干“更容易版”的中间命题分层收束，
典型名字包括：

- `CaseI.SlightlyEasier`
- `CaseI.Statement`
- `caseI_easier`
- `caseI`

对人类读者来说，可以把这一段理解成：

> regularity 让理想变 principal，
> principal 让线性因子变成单位乘 `p` 次幂，
> 而单位与同余的约束最终与 `p ∤ abc` 冲突。

于是 Case I 关闭。

## 8. Case II 的人类可读证明过程

### 8.1 目标

Case II 要排除的是：

- `a^p + b^p = c^p`
- `gcd(a,b,c)=1`
- `p | abc`

对应 formal theorem：

- `caseII`

### 8.2 为什么可假设 `p` 只整除一项

因为我们已经做了 primitive reduction，
所以 `p` 不可能整除三者中的两项或更多。

再利用方程的对称性，可以规整到：

- `p | z`
- `p ∤ y`

formal paper summary里也把这步单列成一个更方便的中间 statement：

- `not_exists_Int_solution`

也就是说，Case II 的实际入口不是“任意 `p|abc`”，而是更精细的：

> `p | z`，`p ∤ y`，且解非平凡。

### 8.3 从整数整除转到分圆域中 `π = ζ - 1` 的整除

在 `O_K` 中，`p` 与

`π^(p-1)`

只差一个单位。

因此：

- `p | n` 在整数里成立，
- 等价于 `π | n` 在 `O_K` 中成立。

这一步的意义是：

> 把 Case II 中“被 `p` 整除”的信息，
> 全部改写成“被唯一 ramified 元 `π` 整除”的信息。

从此以后，下降量不再记“`p` 进阶数”，而记“`π` 的幂次”。

### 8.4 把方程进一步一般化

写

`z = p^k z0`

并把这件事翻译到 `π` 的语言里以后，
要排除的不是单一方程

`x^p + y^p = z^p`

而是一族更一般的方程：

`x^p + y^p = ε * π^{p(m+1)} * z0^p`

其中：

- `m ≥ 0`
- `ε` 是单位
- `π ∤ y`
- `π ∤ z0`

这一步和 `n = 3` 的 generalized equation 很像。

理由也一样：

> 若不显式记住单位与 `π` 幂次，
> 下降构造无法闭合。

### 8.5 下降量是什么

Case II 里下降的量不是一个绝对值，而是上式中的参数 `m`。

换句话说，proof 的目标变成：

> 若存在某个 `m+1` 级别的解，
> 就构造出某个 `m` 级别的解。

于是只要有一个最小 `m` 的解，就会立刻矛盾。

### 8.6 为什么能从 `m+1` 下降到 `m`

这是 Case II 的技术核心。

假设有：

`x^p + y^p = ε * (π^(m+1) z)^p`

其中 `π ∤ y` 且 `π ∤ z`。

接着在 ideal 层分解：

`∏_{η ∈ μ_p} (x + ηy) = π^{p(m+1)} z^p`

由此看出每个因子都带有一个 `π`，
再除去这批 `π` 之后，
经过一系列 ideal / unit / 共轭分析，
可以构造出一个新方程：

`u1 * x'^p + y'^p = u2 * (π^m z')^p`

这就是 paper 中标出的核心下降 statement：

- `exists_solution′`

也就是：

> 从 level `m+1` 的解造出 level `m` 的解。

### 8.7 Kummer 引理在这里做什么

这一段证明里最关键的外部理论输入就是 Kummer's lemma。

它的作用不是直接证明 FLT，
而是帮你消掉下降过程中出现的某个坏单位 `u1`。

逻辑是：

1. 经过整理后，你得到一个单位 `u1`。
2. 你能证明 `u1` 同余于某个整数模 `p`。
3. Kummer 引理说：
   对 odd regular prime，这样的单位实际上就是一个 `p` 次幂单位。
4. 于是 `u1` 可以被吸收入 `x'^p` 这一项。

这样，下降后的新方程仍保持“与原方程同型”的结构，
不会因额外单位而失控。

也就是说：

> Kummer 引理不是用来开始证明，
> 而是用来保证下降后的方程仍在同一个封闭类里。

### 8.8 为什么最终能导出矛盾

一旦已经有“`m+1 → m`”的下降定理，
那么：

1. 假设存在 Case II 解；
2. 取 `m` 最小的那一个；
3. 由下降再造出一个更小的；
4. 矛盾。

因此 generalized Case II 方程无解，
从而原始 Case II 无解。

这就是：

- `not_exists_solution`
- `caseII`

这条线的收束方式。

## 9. 最后一步：把 Case I 与 Case II 合并

有了：

- `caseI`
- `caseII`

之后，`flt_regular` 做的事情就很直接：

1. 任意 primitive 解只能落在 Case I 或 Case II 之一；
2. 两边都已排除；
3. 故 `FermatLastTheoremFor p` 成立。

所以 `flt_regular` 的数学内容并不神秘；
真正的重活都在前面两条分支里。

## 10. 这条分支与 `n = 3`、`n = 4` 的本质差异

如果把三条已闭合分支并排看：

- `n = 4`
  是“最小反例 + 双重勾股数参数化”的初等递降；
- `n = 3`
  是“Eisenstein 整数 + `λ`-重数下降”；
- `regular primes`
  则是“分圆域 ideal 分解 + regularity principalization + Kummer 引理 + `π`-幂次下降”。

因此，`regular primes` 不是单纯把 `n = 3` 的论证做大一号，
而是把：

- class group
- principal ideal
- ramification
- cyclotomic units
- Kummer lemma

这些真正的代数数论基础设施都调动起来了。

## 11. 与 formal theorem 的一一对应

| 数学步骤 | 对应 formal 对象 |
|---|---|
| regularity 定义 | `IsRegularPrime` |
| `I^p` principal 推 `I` principal | `isPrincipal_of_isPrincipal_pow_of_coprime` |
| primitive reduction | `MayAssume.coprime` |
| Case I 坏同余规整 | `a_not_cong_b` |
| 第一分支关闭 | `caseI` |
| 第二分支入口 | `caseII` |
| 两分支合并 | `flt_regular` |

## 12. 阅读建议

如果你要按“人类可读”顺序啃这部分，建议这样走：

1. 先读本稿，把整体 proof graph 建起来。
2. 再回到 [`../process_audit.md`](../process_audit.md) 看 regular primes 过程表。
3. 再读 [`../full_study.md`](../full_study.md) 里 regular primes 的 machine-checked 拆解。
4. 最后再对照 `flt-regular` 项目和 2025 年 AFM 论文。

因为这条线的真正难点，不在 statement，而在：

> 你必须同时看见 element-level equation、ideal-level factorization、以及 class-group-level principalization 三层之间是怎么对接的。

## 13. 资料锚点

本稿对应的上游资料主锚点是：

1. `flt-regular` 项目中的 `CaseI`、`CaseII`、`MayAssume` 与主入口 `flt_regular`。
2. 2025 年 AFM 论文
   “A complete formalization of Fermat's Last Theorem for regular primes in Lean”。

本稿不是逐行 Lean 代码翻译，
而是把上述 formal proof 所体现的数学骨架，改写成人类连续可读的过程稿。

## 14. regular primes 定理树

如果要把 regular primes 这条线继续往叶子压实，
最自然的拆法不是直接从 `flt_regular` 一路往下展开，
而是先按 `MayAssume / Case I / Case II` 三大块切开。

截至 `2026-04-24`，这条分支已经固定成 `11` 个 package。

```text
regular primes branch
├── Root: flt_regular
├── Setup layer
│   ├── IsRegularPrime
│   ├── principalization engine
│   └── primitive reduction (MayAssume)
├── Case I: p ∤ abc
│   ├── bad congruence elimination
│   ├── cyclotomic factorization
│   ├── ideal p-th power extraction
│   ├── principalization via regularity
│   ├── principal ideal → element-level p-th power
│   └── local congruence contradiction
├── Case II: p ∣ abc
│   ├── normalize to p | z and p ∤ y
│   ├── translate p-divisibility to π-divisibility
│   ├── generalized equation family
│   ├── descent step m+1 → m
│   ├── Kummer lemma absorbs bad unit
│   └── minimal-m contradiction
└── Final merge
    ├── primitive solution lies in Case I or Case II
    └── both branches closed
```

和 `n = 4` 相比，这里真正重的地方有三块：

1. `ideal p-th power extraction`
2. `principalization via regularity`
3. `descent step m+1 → m`

所以后续如果只做“能做掉的先做掉”，
就应该先围绕这三块继续细拆，
而不是在已经很清楚的外层重复写摘要。

### 14.1 与机器节点包的对齐

为了保证 `machine_checked_audit`、`process_audit`、本稿三层口径一致，
下面把人类可读树和机器节点包直接对齐。

| 机器节点包 | 本稿中的可读层 | 说明 |
|---|---|---|
| setup | Setup layer | regularity 定义与 principalization engine |
| MayAssume | primitive reduction (MayAssume) | primitive solution 与入口规整 |
| Case I outer statement | Case I: p ∤ abc 的入口层 | 固定带附加假设的陈述并消去附加假设 |
| Case I ideal extraction | cyclotomic factorization / ideal p-th power extraction | 从线性因子进入 ideal-level `p` 次幂结构 |
| Case I principalization | principalization via regularity | 用 regularity 把 `I^p` principal 拉回 `I` principal |
| Case I element recovery / close | principal ideal → element-level p-th power / local congruence contradiction | 把 ideal-level 信息拉回 element-level 并收束矛盾 |
| Case II π-language | translate p-divisibility to π-divisibility / generalized equation family | 把整数整除改写成 `π`-language |
| Case II ideal-factor layer | Case II 中的 ideal 结构层 | 建立 `𝔠 η` 与 `𝔞 η` 的 ideal-level结构 |
| Case II distinguished root | distinguished root / local control | 锁定 `η₀` 并控制 `𝔭`-整除 |
| Case II descent core | descent step m+1 → m | 真正的下降核心 |
| Case II close / merge | minimal-m contradiction / Final merge | 取最小 `m` 收束并与 Case I 合并 |

本节中的 `Setup layer`、`primitive reduction (MayAssume)`、
`descent step m+1 → m`、`minimal-m contradiction / Final merge` 等标签
只作为 reader-facing aliases（读者导向别名）使用；它们不是第二套 competing machine-tree node 名，
也不形成第二套 canonical node system；跨文件同步时仍以上表左列 canonical package 名为准。
本稿与 `machine_checked_audit.md`、`process_audit.md` 共用同一组 regular-primes canonical package 名：
`setup`、`MayAssume`、`Case I outer statement`、`Case I ideal extraction`、
`Case I principalization`、`Case I element recovery / close`、
`Case II π-language`、`Case II ideal-factor layer`、
`Case II distinguished root`、`Case II descent core`、`Case II close / merge`。

### 14.2 每个 package 再拆一层

以下 package / `one-more-depth` 子包与 `machine_checked_audit.md`、`process_audit.md`
保持同名同步；截至 `2026-04-24`，这些展开项都已拥有独立 `<=100` proof-step ledger，
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

### 14.2A-14.2K 独立 ledger 集成摘要

Source anchor:
`https://github.com/leanprover-community/flt-regular/blob/master/FltRegular/MayAssume/Lemmas.lean`

| package | total proof steps | descendant closure carried by the same ledger |
|---|---:|---|
| `setup` | `13` | no extra canonical descendant beyond the package itself |
| `MayAssume` | `37` | no extra canonical descendant beyond the package itself |
| `Case I outer statement` | `16` | no extra canonical descendant beyond the package itself |
| `Case I ideal extraction` | `21` | closes former package-level unresolved `exists_ideal pairwise ideal coprimality interface` |
| `Case I principalization` | `13` | no extra canonical descendant beyond the package itself |
| `Case I element recovery / close` | `25` | closes former package-level unresolved `caseI_easier / aux-index exclusion` |
| `Case II π-language` | `18` | no extra canonical descendant beyond the package itself |
| `Case II ideal-factor layer` | `25` | closes `Case II ideal-factor layer / global product to local p-th powers` |
| `Case II distinguished root` | `20` | closes `Case II distinguished root / p_pow_dvd_c_eta_zero` |
| `Case II descent core` | `35` | closes `Case II descent core / three-root formula and raw descent` |
| `Case II close / merge` | `34` | closes `Case II close / merge / not_exists_solution'` |

### 14.3 高风险 leaf 再拆一层

跨文件统一的 canonical high-risk leaf 名称保持不变：

1. `Case II ideal-factor layer / global product to local p-th powers`
2. `Case II distinguished root / p_pow_dvd_c_eta_zero`
3. `Case II descent core / three-root formula and raw descent`
4. `Case II close / merge / not_exists_solution'`

这些高风险 leaf 及其 `one-more-depth` 子包截至 `2026-04-24` 都已由 matching package ledger 关闭。
上述 canonical high-risk leaf 名与 `machine_checked_audit.md`、`process_audit.md`
以及本稿中的 ledger 行保持逐字一致；reader-facing 解释句不提升为新的 leaf 名。

| leaf | one-more-depth items | status |
|---|---|---|
| `Case II ideal-factor layer / global product to local p-th powers` | `exists_ideal_pow_eq_c_aux / RHS normalization`; `prod_c / cyclotomic product expansion`; `prod_c / factorwise 𝔪·𝔠η·𝔭 substitution`; `prod_c / common-factor cancellation`; `exists_ideal_pow_eq_c / pairwise-coprime local extraction`; `root_div_zeta_sub_one_dvd_gcd / witness packaging` | `checked` |
| `Case II distinguished root / p_pow_dvd_c_eta_zero` | `η₀ divisibility criterion import`; `off-root product coprimality`; `gcd-product pivot`; `distinguished factor reinsertion into total product`; `visible 𝔭^(m*p) extraction from global p-th power` | `checked` |
| `Case II descent core / three-root formula and raw descent` | `three-root orbit selection`; `root-difference as unit·π`; `three-root cancellation identity`; `raw descended triple packaging`; `raw nondivisibility certification` | `checked` |
| `Case II close / merge / not_exists_solution'` | `generalized-family minimal-m closure`; `π-adic normalization of z`; `integer transport`; `primitive gcd cleanup`; `caseII permutation close`; `final merge` | `checked` |

### 14.3A 高风险 leaf 的 process-level wording

这些 proof chunk 的命名保持不变，但截至 `2026-04-24` 都已从 process-budget 角度完成闭合：

| leaf | process-level wording | status |
|---|---|---|
| `Case II ideal-factor layer / global product to local p-th powers` | 先把 `𝔷 = 𝔪 * 𝔷'` 代回并整理出全局等式 `∏η 𝔠 η = (𝔷' * 𝔭^m)^p`，再用 pairwise coprimality 与 `Finset.exists_eq_pow_of_mul_eq_pow_of_coprime` 逐个抽出 `(𝔞 η)^p = 𝔠 η`。 | `checked` |
| `Case II distinguished root / p_pow_dvd_c_eta_zero` | 先用 `p_dvd_c_iff` 排除所有 off-root 的 `𝔭`-整除，再把它升级成 `gcd (𝔭^(m*p), ∏_{η ≠ η₀} 𝔠 η) = 1`，最后借 `prod_c` 把全部 `𝔭^(m*p)` 压到 `𝔠 η₀`。 | `checked` |
| `Case II descent core / three-root formula and raw descent` | 先取轨道 `η₀, η₀ζ, η₀ζ²`，把三条 root difference 统一改写成 `π` 的 unit 倍，再由 `formula` 做三根消元，并在 `exists_solution` 中打包成 level-`m` 的 raw descended equation。 | `checked` |
| `Case II close / merge / not_exists_solution'` | 先从 `π ∣ z` 的解中抽出最大 `π`-幂，落到 generalized level-`m` 方程族，再经整数 transport、primitive cleanup、Case II 置换归约，最后与 Case I 合并。 | `checked` |

## 15. 截至 2026-04-24 的机器兼容完成度判断

下面这 `11` 个 canonical package 的 one-more-depth expansion
均已拥有独立 `<=100` proof-step ledger：

| package | one-more-depth status |
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

### 15.1 regular primes status ledger

顶层 theorem-flow 行继续描述 theorem-level 的 machine-checked 事实；
下表只审计 process-tree 的 `<=100` leaf-budget closure。
这里的 process-tree `checked`
不改变 theorem-level 的 upstream closure /
repo-local anchor-only 边界，也不把已完成的 canonical naming sync
扩张成“本仓库已 vendoring 上游 `flt_regular` 证明本体”的断言。

截至 `2026-04-24`，`11` 个 canonical package、`4` 个 canonical high-risk leaf，
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

此前曾单列的
`exists_ideal pairwise ideal coprimality interface`
与 `caseI_easier / aux-index exclusion`
也已随 matching package ledger 一并关闭；
它们不并入 canonical high-risk leaf 集，但截至 `2026-04-24` 也都已处于闭合状态。

### 15.2 regular primes closure status snapshot

| question | answer |
|---|---|
| theorem-boundary wording closure | yes |
| repo-local anchor-only statement/module/theorem-name record closure | yes |
| human-readable narrative closure | yes |
| canonical package naming closure | yes |
| canonical high-risk leaf naming closure | yes |
| package-level unresolved-subitem naming closure | yes |
| explicit `unchecked` exposure | n/a; as of `2026-04-24`, this surface is all checked |
| `<=100`-step leaf-proof closure | yes; all expanded surfaces are checked |

因此，regular primes 这条线已经达到：

- theorem-boundary wording closure: yes
- boundary sentence fixed as:
  `upstream theorem closure: yes / repo-local vendored theorem closure: no, anchor-only / repo-local anchor-only statement/module/theorem-name record: yes`
- human-readable narrative closure: yes
- theorem vendoring closure remains:
  `no`; 截至 `2026-04-24`，本仓库的人类可读 closure 与 machine-tree 对齐，
  但不表示本仓库已经 vendoring `flt_regular` 的证明本体
- machine-compatible package naming closure: yes
- machine-compatible high-risk leaf naming closure: yes
- `<=100`-step leaf-proof closure: yes; all expanded surfaces are checked

<!-- HR18_REGULAR_MERGED_START -->
## 附录：regular primes 的 11 个 execution unit 公开归档

下列 `11` 个 unit 的稳定公开说明统一归档在本主稿内，不再需要另设公开子稿。
`FLT-HR-008` 到 `FLT-HR-018` 的唯一公开说明目标就是本文件；`human_steps/`、`.cron/results/*` 与自动化工作副本路径都不是公开归档目标。

### `FLT-HR-008` `regular primes / setup and regularity engine`

Scope boundary: this unit is limited to the canonical package `setup`; it records the regularity engine and anchor-only theorem boundary, and does not prove `MayAssume`, Case I, Case II, or repo-local vendored theorem closure.

#### Human-Readable Expansion
##### 1. 本 unit 的边界

在 `regular primes` 这条路线里，`setup` 是外层代数数论引擎。它不处理 primitive reduction，也不进入 `Case I: p ∤ abc` 或 `Case II: p ∣ abc` 的具体反证；它只负责把“regular prime”这个输入条件变成后续可复用的 principalization engine。

按本仓库三层材料统一后的 canonical naming，本 unit 只认下面两个 formal hook：

- `IsRegularPrime`
- `isPrincipal_of_isPrincipal_pow_of_coprime`

这里的 reader-facing 标题 `setup and regularity engine` 只是说明用语；canonical package 名仍然是 `setup`。

##### 2. `IsRegularPrime` 在这里表达什么

这一路线中的 regularity 不是单纯的标签，而是 class-group coprimality 条件。统一口径是：

> `p` 与 `p` 次分圆域整数环的 class group 基数互素。

因此，人类读这一步时要抓住的不是 Bernoulli 数的背景判据，而是后续证明真正消费的是“`p` 不会在相应 class group 中留下无法杀掉的 torsion 障碍”这件事。`IsRegularNumber / IsRegularPrime interface` 这一子项的作用，就是把这条 regularity 条件组织成后续 theorem 可直接调用的 formal 入口，而分支实际对外使用的名字是 `IsRegularPrime`。

##### 3. principalization engine 的局部逻辑链

`isPrincipal_of_isPrincipal_pow_of_coprime` 是整个 setup 层的核心。它把“`I^p` 已 principal”转换为“`I` 本身 principal”，从而把 ideal-level 信息拉回 element-level。其局部逻辑可以按下面五步理解：

1. 先把 `I = 0` 的平凡情形单独剥离，这就是 `I = 0 base case`。
2. 对非零 ideal，用 `ClassGroup.mk0_eq_one_iff bridge` 把“`I` 在 class group 中的类是单位元”改写成“`I` principal”。
3. 若 `(I^p).IsPrincipal`，则在 class group 中有 `[I]^p = 1`；这就是 `p-power to class-group torsion`，也就是把 principality of the `p`-th power 翻译成 `p`-torsion 信息。
4. regular prime 条件给出 `p` 与 class group 的基数互素，因此 class group 中任何同时受 `p`-torsion 约束又受群阶约束的元素，其 `orderOf` 只能是 `1`；这正是 `orderOf coprimality kill step`。
5. 一旦 `[I] = 1`，就回到第 2 步的桥，推出 `I` principal。

这条链条就是本 unit 所谓的 regularity engine：它不是额外的装饰，而是后续 Kummer 路线从 ideal factorization 回到元素生成元、单位和同余控制的必要桥梁。

##### 4. 为什么这一步是整条 branch 的入口引擎

Case I 会先把某个线性因子对应的 ideal 证明成 `p` 次幂结构，再在下游 `Case I principalization` 包中真正调用这里的引擎，把 ideal principalize 掉。Case II 里的某些 quotient / principal bridge 也沿用同一思想，只是包装不同。换句话说：

- 没有 `IsRegularPrime`，后续就没有可以杀掉 class-group obstruction 的条件。
- 没有 `isPrincipal_of_isPrincipal_pow_of_coprime`，后续 ideal-level factorization 不能稳定返回 element-level。
- 因此 `setup` 不是背景章节，而是整个 `flt_regular` 路线的 algebraic engine。

##### 5. 本 unit 的 theorem-boundary 说明

本 unit 必须保留下面这句边界口径：

`upstream theorem closure: yes / repo-local vendored theorem closure: no, anchor-only / repo-local anchor-only statement/module/theorem-name record: yes`

它的含义是：

- `IsRegularPrime` 与 `isPrincipal_of_isPrincipal_pow_of_coprime` 的 machine-checked closure 来自上游 `flt-regular`。
- 本仓库本地的 `Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/RegularPrimesPath.lean` 只记录 `regularPrimesStatementShape`、上游模块路径和终端 theorem 名 `flt_regular`。
- 因而本文件可以稳定解释 proof architecture，但不能把“anchor 已记录”说成“上游证明本体已经 vendored 到本仓库”。

##### 6. 本 unit 与下游单元的交接

本 unit 在这里结束于“regularity 条件已经被组织成 principalization engine”。再往后：

- `FLT-HR-009` 负责 `MayAssume`，把任意整数解规整到 primitive solution。
- `FLT-HR-010` 到 `FLT-HR-013` 才真正展开 Case I。
- `FLT-HR-014` 到 `FLT-HR-018` 处理 Case II 与最终合并。

所以本 unit 的完成标准不是“已经证明了 regular primes 的 FLT”，而是“已经把整条路线最外层的 regularity / class-group / principalization 接口讲清楚，并给出局部 budget closure”。

#### Local Budget Ledger
局部 canonical package：`setup`

局部 budget cap：`13`

closure 口径：下表里的 `checked` 只表示本 unit 的人类可读闭包已经写定；它不改变上游 theorem closure / 本地 anchor-only 的边界。

| step | canonical subitem | local closure note | status |
|---|---|---|---|
| 1 | package boundary | 固定本 ledger 只关闭 `setup`，不前跳 `MayAssume`、Case I、Case II | `checked` |
| 2 | `IsRegularNumber / IsRegularPrime interface` | 记录 setup 层的 formal 入口对象集合 | `checked` |
| 3 | `IsRegularNumber / IsRegularPrime interface` | 指明分支实际对外使用的 predicate 名为 `IsRegularPrime` | `checked` |
| 4 | `IsRegularNumber / IsRegularPrime interface` | 把 regular prime 解释为 class-group coprimality 条件 | `checked` |
| 5 | `I = 0 base case` | 把零 ideal 作为平凡 principal 情形单列 | `checked` |
| 6 | `ClassGroup.mk0_eq_one_iff bridge` | 把 class-group 单位元条件改写成 principal 性 | `checked` |
| 7 | `p-power to class-group torsion` | 从 `(I^p).IsPrincipal` 提取 `[I]^p = 1` | `checked` |
| 8 | `p-power to class-group torsion` | 把上一步读成 class group 中的 `p`-torsion 信息 | `checked` |
| 9 | `orderOf coprimality kill step` | 用 regularity 提供 `p` 与 class group 阶互素 | `checked` |
| 10 | `orderOf coprimality kill step` | 用 `orderOf` 同时受 `p` 与群阶约束，杀掉非平凡 ideal class | `checked` |
| 11 | `ClassGroup.mk0_eq_one_iff bridge` | 由 `[I] = 1` 回推 `I` principal | `checked` |
| 12 | package closure | 记录 `isPrincipal_of_isPrincipal_pow_of_coprime` 是 setup 的 algebraic engine | `checked` |
| 13 | handoff boundary | 把下游交接给 `MayAssume` / Case I / Case II，并保留 anchor-only theorem boundary | `checked` |

Total local proof steps: `13`

局部 closure 汇总：`13 / 13` steps checked，满足本 unit 的独立 `<=100` 步预算约束。

### `FLT-HR-009` `regular primes / MayAssume primitive reduction`

Scope boundary: this unit is limited to the canonical package `MayAssume`; it proves only the primitive-reduction interface and does not prove Case I, Case II, or repo-local vendored theorem closure.

#### Human-Readable Expansion
##### 1. 这个 unit 只负责什么

这个 unit 不进入 `Case I` 的分圆域 ideal 分解，也不进入 `Case II` 的 `pi = zeta - 1` 下降。

它只做两件前置规整：

1. 把任意非平凡整数解规整成 primitive solution。
2. 把 primitive solution 整理成两个分支都能直接使用的统一接口。

从 `RegularPrimesPath.lean` 记录的模块顺序看，
`FltRegular/MayAssume/Lemmas.lean`
正好位于
`FltRegular/CaseI/Statement.lean`
与
`FltRegular/CaseII/Statement.lean`
之前；
因此这里的作用不是“证明某个 branch”，而是把 branch 入口清理干净。

对后续流程来说，这个接口层的输出是：

- 一个保持原方程的 primitive 非零三元组；
- 一个可供 `Case I` 使用的“坏同余已规整”版本；
- 一个专门用于消去坏同余的局部整除引理。

##### 2. `MayAssume.coprime`：先把公共因子除掉

`MayAssume.coprime` 的核心不是抽象地说“可设互素”，
而是显式构造一个除以三元组公共 gcd 之后的新解。

做法是固定
`s := ({a, b, c} : Finset ℤ)`，
再令
`d := s.gcd id`。

然后它完成三件事：

1. 证明 `d != 0`，否则 `{a,b,c}` 全部为零，和非平凡性矛盾。
2. 用 `d | a`、`d | b`、`d | c` 把原方程写成
   `a = d * na`、`b = d * nb`、`c = d * nc` 的形式，
   再把等式整体按 `d^n` 约去。
3. 证明新三元组
   `(a / d, b / d, c / d)`
   既满足同一个指数方程，又满足 gcd 为 `1`，且非零性仍然保留。

所以这里的 primitive reduction 不是“换个记号”，
而是完成了真正的方程 transport：

- 原方程 `a^n + b^n = c^n` 被搬运到约去公共因子后的新三元组；
- 非零性被搬运；
- primitive 条件被直接产出。

这正是后续分支讨论所需的最小正规形。
没有这一步，就不能稳定地区分 `p ∤ abc` 与 `p | abc`，
也不能安全使用“`p` 不会同时整除多个坐标”的 primitive 推论。

##### 3. `p_dvd_c_of_ab_of_anegc`：坏同余消去所需的局部引理

`MayAssume` 里还有一个很局部但很关键的接口引理：
`p_dvd_c_of_ab_of_anegc`。

它处理的输入不是整个 `Case I`，而是如下同余组合：

- `a ≡ b [ZMOD p]`
- `b ≡ -c [ZMOD p]`
- `a^p + b^p = c^p`

在 `ZMod p` 中把原方程取模，
再利用 `p` 为素数时的 `p` 次幂简化，
就可以把方程压缩成一个只剩 residue class 的关系。

把上面的两个同余代回去之后，
式子会走到一个二分：

- 要么 `c = 0 mod p`；
- 要么 `3 = 0 mod p`。

后者只会在 `p = 3` 时发生。
而 regular-primes 路线在真正进入两大分支时已经带有小素数 cutoff，
所以这里能排掉 `p = 3`，
从而只留下
`p | c`。

这个引理的角色要说清楚：

- 它本身不是 branch split；
- 它是 `a_not_cong_b` 内部用来打掉坏同余配置的“局部模 `p` 反击”。

也就是说，
它把“两个不良同余一起成立”转成“`p` 整除某个坐标”，
再由 `Case I` 的 `p ∤ abc` 假设完成矛盾。

##### 4. `a_not_cong_b`：把 Case I 入口规整成无坏同余的版本

`Case I` 不仅要有 primitive solution，
还要避免一个会污染线性因子 coprimality 的坏同余形态。
`a_not_cong_b` 的任务就是把这一点做成标准入口。

它的逻辑分成两步。

第一步，检查原三元组是否已经满足
`¬ a ≡ b [ZMOD p]`。

- 如果是，那么直接保留原三元组；
- 如果不是，就对三元组做一次符号与坐标规整。

第二步，在坏同余真的发生时，换成
`(x, y, z) := (a, -c, -b)`。

之所以可以这么换，是因为此时 `p` 为奇素数，
所以奇次幂会把负号保留下来。
原方程
`a^p + b^p = c^p`
可改写成
`a^p + (-c)^p = (-b)^p`，
因此换元后的三元组仍是同一个指数方程的解。

这里必须额外保住三种不变量：

1. gcd 不变。
   对 `a`、`-b`、`-c` 取 gcd 时，
   符号变化不会改变 `natAbs`，
   因而 primitive 条件可原样转移。
2. 非零积不变。
   `a * (-c) * (-b) = a * b * c`，
   所以原来的非平凡性直接继承。
3. `Case I` 假设不变。
   同一个乘积恒等式也保证
   `¬ p | a*b*c`
   能传到新三元组。

接下来还要证明新三元组确实摆脱了坏同余。

若仍有
`a ≡ -c [ZMOD p]`，
再结合最开始的坏同余
`a ≡ b [ZMOD p]`，
就落入上一节的 `p_dvd_c_of_ab_of_anegc`。
于是得到 `p | c`，
进而 `p | a*b*c`，
和 `Case I` 的入口条件矛盾。

因此 `a_not_cong_b` 的真正输出不是一个“更漂亮”的三元组，
而是一个同时携带以下数据的 witness package：

- 方程仍成立；
- primitive 条件仍成立；
- 非零性仍成立；
- `Case I` 假设仍成立；
- 新三元组满足 `¬ x ≡ y [ZMOD p]`。

##### 5. 这就是 Case I / Case II 分叉前的完整接口

这个 unit 结束时，后续分支所需的数据已经全部就位。

对 `Case I`：

- 输入来自 primitive solution；
- 再额外带上 `a_not_cong_b` 产出的坏同余消去版本；
- 因而可以直接进入 `CaseI.Statement` 及后续分圆域 ideal 层。

对 `Case II`：

- 输入同样来自 primitive solution；
- 不需要 `a_not_cong_b` 的非同余包装，
  但会用到这里已经建立好的 primitive 入口，
  使 `p | abc` 的讨论落在“最多整除一个坐标”的标准背景里。

因此 `MayAssume` 的地位可以精确概括为：

> 它不负责关闭任一分支，
> 只负责把任意非平凡解整理成两个主分支都认可的标准入口，
> 并把 Case I 额外需要的坏同余规整提前完成。

##### 6. 按 formal hook 看，这里到底向下游交什么

若按 `MayAssume` 文件里的接口顺序读，这个 unit 实际向下游交出三类对象：

1. `MayAssume.coprime`
   给出除以公共 gcd 之后的 transported equation，
   同时把 primitive 条件与非零性一起打包；
   这是 Case I / Case II 共用的入口。
2. `MayAssume.p_dvd_c_of_ab_of_anegc`
   给出一个局部模 `p` 反击器：
   当 `a ≡ b` 与 `b ≡ -c` 同时出现时，
   它把坏同余压成 `p | c`。
   这不是独立 branch theorem，
   而是供 `a_not_cong_b` 内部调用的局部接口。
3. `a_not_cong_b`
   在保留方程、primitive、非零积和 `Case I` 假设的同时，
   必要时通过符号与坐标替换，把 witness 规整到
   `¬ x ≡ y [ZMOD p]` 的 Case I 可用形态。

所以本 unit 的真正终点不是“已经开始证明 Case I / Case II”，
而是：

- 对外层总流程，已经把任意解压缩成 primitive 接口；
- 对 `Case I outer statement`，已经准备好无坏同余的输入包；
- 对 `Case II`，已经准备好不含公共 gcd 的 primitive 输入包。

再往后的事情都属于下一层 package，
不在本 ledger 的职责边界内。

#### Local Budget Ledger
##### Ledger Summary

| canonical subitem | step range | status |
|---|---|---|
| `MayAssume.coprime / divide-by-gcd equation transport` | `1-10` | `checked` |
| `MayAssume.coprime / primitive output` | `11-12` | `checked` |
| `MayAssume.coprime / nonzero output` | `13-16` | `checked` |
| `p_dvd_c_of_ab_of_anegc / ZMod divisibility extraction` | `17-25` | `checked` |
| `a_not_cong_b / sign-swap invariants` | `26-32` | `checked` |
| `a_not_cong_b / bad-congruence elimination` | `33-37` | `checked` |

Total local proof steps: `37`

总计 `37` 步，满足本 unit 的独立 `<=100` 步预算约束。

##### Detailed Local Ledger

1. 在 `MayAssume.coprime` 中固定 `s := ({a, b, c} : Finset ℤ)` 与 `d := s.gcd id`。
2. 由 `hprod : a * b * c != 0` 先抽出 `ha : a != 0`。
3. 对 `{a,b,c}` 的三个成员分别使用 `gcd_dvd`，得到 `d | a`、`d | b`、`d | c`。
4. 证明 `d != 0`；若 `d = 0`，则 `Finset.gcd_eq_zero_iff` 迫使 `{a,b,c}` 全为零，与 `ha` 矛盾。
5. 由 `d != 0` 推出 `d^n != 0`。
6. 为方程 transport 选取见证 `na`、`nb`、`nc`，使 `a = d * na`、`b = d * nb`、`c = d * nc`。
7. 将目标等式整体左乘 `d^n`，并用 `mul_left_inj'` 把问题化为对同一非零因子 `d^n` 的约去。
8. 用 `mul_pow`、第 3 步的整除见证以及 `Int.mul_ediv_cancel_left`，把 `d^n * (a / d)^n`、`d^n * (b / d)^n`、`d^n * (c / d)^n` 全部改写回原变量。
9. 改写后，transport 后的目标恰好恢复成原方程 `a^n + b^n = c^n`。
10. 用原假设 `H` 关闭 `divide-by-gcd equation transport` 分支。
11. 在 primitive 输出分支，对非零成员 `a ∈ {a,b,c}` 应用 `Finset.gcd_div_id_eq_one`。
12. 再经 `gcd_eq_gcd_image` 与 `d` 的命名改写，得到 `({a / d, b / d, c / d} : Finset ℤ).gcd id = 1`。
13. 在非零输出分支，反设 `(a / d) * (b / d) * (c / d) = 0`。
14. 用 `mul_eq_zero` 拆成三种情形：`a / d = 0`、`b / d = 0`、`c / d = 0`。
15. 每一支都用 `Int.eq_zero_of_ediv_eq_zero` 把“约后为零”拉回原坐标为零。
16. 每个原坐标为零都与 `hprod` 矛盾，因此 `(a / d) * (b / d) * (c / d) != 0`。
17. 在 `p_dvd_c_of_ab_of_anegc` 中装入 `Fact p.Prime`，使 `ZMod.pow_card` 型简化可用。
18. 对等式 `h : a^p + b^p = c^p` 施加 `congr_arg (fun n : ℤ => (n : ZMod p))`。
19. 用 `Int.cast_add`、`Int.cast_pow` 与 `ZMod.pow_card` 简化投到 `ZMod p` 后的方程，使各个 `p` 次幂塌缩到相应 residue class。
20. 把 `hab` 与 `hbc` 这两个 `Int.ModEq` 条件改写成 `ZMod p` 里的等式。
21. 用 `a = b` 与 `b = -c` 的 `ZMod p` 版本重写投模后的方程。
22. 经整理后把结论压成一个二分：要么 `c = 0 mod p`，要么 `3 = 0 mod p`。
23. 把 `c = 0 mod p` 用 `ZMod.intCast_zmod_eq_zero_iff_dvd` 拉回成 `p | c`。
24. 对异常支 `3 = 0 mod p` 使用 `ZMod.natCast_eq_zero_iff` 与 `Nat.dvd_prime Nat.prime_three`，得到只可能 `p = 1` 或 `p = 3`。
25. 再用 `hpri.ne_one` 与小素数 cutoff `hp : p != 3` 排掉异常支，只剩 `p | c`。
26. 在 `a_not_cong_b` 中，对 `H : a ≡ b [ZMOD p]` 分情形讨论。
27. 若 `H` 为假，就直接返回原三元组及其现有数据包。
28. 若 `H` 为真，就定义符号交换后的三元组 `(x,y,z) := (a, -c, -b)`。
29. 由 `hp5 : 5 <= p` 得 `p != 2`，再由素数奇偶分解推出 `p` 为奇数。
30. 用奇数次幂对负号的保留，把 `(-c)^p` 改写成 `-c^p`，把 `(-b)^p` 改写成 `-b^p`。
31. 结合原方程 `h` 重排可得 `a^p + (-c)^p = (-b)^p`，即新三元组仍满足同一类方程。
32. 对新三元组的 gcd 做符号不变性整理：把 `{a,-c,-b}` 改写成与 `{a,b,c}` 同 `natAbs` 的形式，从而把 primitive 条件传过去。
33. 为证明新三元组摆脱坏同余，反设 `habs : a ≡ -c [ZMOD p]`。
34. 由 `p >= 5` 再推出 `p != 3`，并把 `H` 与 `habs` 都转成 `p_dvd_c_of_ab_of_anegc` 需要的 `ZMod p` 等式格式。
35. 套用 `p_dvd_c_of_ab_of_anegc` 得到 `p | c`，于是可推出 `p | a*b*c`。
36. 这与 `Case I` 的输入假设 `¬ p | a*b*c` 矛盾，所以新三元组必须满足 `¬ x ≡ y [ZMOD p]`；同时 `a * (-c) * (-b) = a * b * c` 保证非零积不变。
37. 同一个乘积恒等式也把 `Case I` 假设从原三元组传到新三元组，完成 `a_not_cong_b` 的 witness package。

### `FLT-HR-010` `regular primes / Case I outer statement`

Scope boundary: this unit is limited to the canonical package `Case I outer statement`; it states and routes the Case I interface and does not prove ideal extraction, principalization, element recovery, Case II, or repo-local vendored theorem closure.

#### Human-Readable Expansion
##### 1. Canonical node 对齐

本 unit 对应 `process_audit.md` 里的 package
`Case I outer statement`，
canonical hook 是：

- `CaseI.SlightlyEasier`
- `CaseI.Statement`
- `CaseI.may_assume`

它的职责不是直接完成 Case I 的全部矛盾，
而是把“原始整数解 + Case I 分支条件”整理成一个适合下游分圆域论证的标准入口。

从本仓库的锚点模块
`Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/RegularPrimesPath.lean`
看，regular primes 路线只在本地记录了 upstream module anchor；
因此这里的人类可读展开必须以 `process_audit.md` 与
`regular_primes_proof_process.md` 给出的 canonical 名称为准，
把外层骨架先写清，再把 heavier 的 ideal-level 论证留给后续 unit。

##### 2. 本单元到底要固定什么

Case I 的外层目标是排除下面这种情形：

- `a^p + b^p = c^p`
- `p` 是 odd regular prime
- `p ∤ abc`

其中 `p ∤ abc` 是这条分支的定义性条件。
因为 `p` 是素数，所以这句话等价于：

- `p ∤ a`
- `p ∤ b`
- `p ∤ c`

也就是说，Case I 的核心不是“有一个坐标被 `p` 整除”，
而恰恰是“`p` 不整除任何一个坐标”。
这会把证明与 Case II 的 `π = ζ - 1` 下降机制分开，
并告诉我们接下来应走的是分圆分解加 ideal factorization 的路线。

##### 3. 为什么这里先做外层规整，而不是直接做 ideal 提取

`process_audit.md` 把本 unit 继续细拆成五个 one-more-depth 子项：

- `SlightlyEasier / Statement interface`
- `small-prime cutoff (hodd / hprod / hp5)`
- `Case I divisibility transport across gcd quotient`
- `primitive normalization via MayAssume.coprime`
- `noncongruence normalization and dispatch`

这说明本单元要处理的不是“理想怎样变成 `p` 次幂”，
而是“什么样的三元组才有资格被送进那个理想论证”。

换句话说，这一层的产出是一个**标准化的 Case I 输入包**：

- 方程仍是 `a^p + b^p = c^p`
- 三元组已经规整成 primitive solution
- Case I 分支条件 `p ∤ abc` 仍然保留
- 还会额外安排一个方便后续线性因子分析的非同余条件

只有当这些入口条件都被稳定安装后，
后面的 unit 才能在分圆域 `K = ℚ(ζ_p)` 的整数环里谈
`a + η b` 这些线性因子生成的 ideal。

##### 4. `CaseI.SlightlyEasier → CaseI.Statement → CaseI.may_assume` 的层次

从人类角度看，这三个名字表达的是同一个骨架的三层包装。

`CaseI.SlightlyEasier`：
它是一个更强、也更干净的入口版陈述。
在这一层里，证明已经假定了足够好的外部条件，
例如 primitive 性、Case I 分支条件、以及坏同余已经被排掉，
所以可以直接把注意力转向分圆分解。

`CaseI.Statement`：
它把公共读者真正关心的 Case I 陈述，
压缩到 `CaseI.SlightlyEasier` 可用的输入格式。
也就是说，它负责把“公共接口上的 Case I”桥接到“技术接口上的 Case I”。

`CaseI.may_assume`：
它再往外包一层，
调用 `MayAssume.coprime` 和 `a_not_cong_b`，
把任意候选解替换成一个等价的、适合 Case I 技术论证的标准三元组。

所以这个单元的核心信息不是某个神秘的新引理，
而是一个清晰的工作流：

原始整数解  
`→` primitive normalization  
`→` Case I 非同余 normalization  
`→` `CaseI.SlightlyEasier` 的 clean input  
`→` 进入下游分圆因子论证

##### 5. small-prime cutoff 在这里的作用

审计表明确把 `small-prime cutoff (hodd / hprod / hp5)` 记为本 unit 的组成部分，
这表示 Case I 的 outer statement 不是对所有奇素数都用完全相同的入口包装。

在这个 regular primes 分支里，
`p = 3` 已经由仓库中另一条机器验证路线单独处理；
因此这里真正需要的技术入口是 `p ≥ 5` 的情形。

这个 cutoff 的作用主要有两点：

1. 它保证 sign-swap / noncongruence normalization 不会落进 `p = 2` 或 `p = 3` 的退化算术。
2. 它保证后面在 `ZMod p` 中做坏同余排除时，有足够空间把例外分支彻底剪掉。

因此，small-prime cutoff 不是旁枝细节，
而是 Case I outer statement 能够顺利接上 `a_not_cong_b` 的前提。

##### 6. `p ∤ abc` 如何跨过 primitive quotient 运输

`Case I divisibility transport across gcd quotient` 和
`primitive normalization via MayAssume.coprime`
必须一起看。

`MayAssume.coprime` 做的是：

- 把原始三元组按公共 gcd 约掉
- 保留方程形状
- 保留非零性
- 输出 primitive solution

而本单元额外要确认的是：
这个“除以 gcd”的操作不会把 Case I 分支条件弄丢。

本地要点可以概括成一句话：

> 如果原始三元组落在 Case I，即 `p ∤ abc`，
> 那么约去公共 gcd 后得到的 primitive triple 仍然落在 Case I，
> 因为这一步只是去掉公共可约部分，并没有制造新的 `p`-整除。

于是 `CaseI.Statement` 之后讨论的对象，
可以安全地从“任意整数候选解”收缩为“primitive 的 Case I 候选解”。

##### 7. 非同余规整为什么属于 outer statement

`a_not_cong_b` 已经在上一个 package `MayAssume` 中被审计为完成，
但它的使用位置正是本 unit。

原因是：
Case I 后续要把

`a^p + b^p = c^p`

送进分圆域中的分解

`a^p + b^p = ∏_{η ∈ μ_p} (a + η b)`。

为了让这些线性因子在 ideal 层面表现得足够“分离”，
需要先排除一个坏的同余构型；
`a_not_cong_b` 正是把原始 primitive Case I triple
变成一个满足

- `a \not\equiv b [ZMOD p]`

的等价三元组。

这里的“等价”不是松散口语，
而是指下面几件对 Case I 外层骨架至关重要的事实都被保留下来：

- 方程仍成立
- gcd 条件仍成立
- 非零积仍成立
- `p ∤ abc` 仍成立

因此在 `CaseI.may_assume` 的视角里，
`a_not_cong_b` 不是附带修饰，
而是进入分圆因子分析前的最后一个 outer normalization。

##### 8. 本单元的终点：只到分圆分解入口，不越过它

完成上述规整之后，
本单元能合法交给下游 unit 的输入是：

- `p` 是 odd regular prime，且已进入 `p ≥ 5` 的技术分支
- `(a,b,c)` 是 primitive solution
- `a^p + b^p = c^p`
- `p ∤ abc`
- `a \not\equiv b [ZMOD p]`

在这个标准入口上，
下一单元 `Case I ideal extraction` 才开始真正使用

`a^p + b^p = ∏_{η ∈ μ_p} (a + η b)`

以及对应的 ideal factorization，
去证明每个线性因子在去掉 ramified 噪声后都表现成 `p` 次幂 ideal。

所以本文件的收口句应该是：

> `FLT-HR-010` 已经把 Case I 的原始分支陈述，
> 规整成“primitive + noncongruence-normalized + still in Case I”的标准输入；
> 这正是外层 route 进入 cyclotomic factorization 的地方，
> 但还没有进入 ideal extraction、本原化 principalization 或最终矛盾。

#### Local Budget Ledger
本 unit 的局部预算与 `machine_checked_audit.md` / `process_audit.md`
保持一致，总计 `16` 步，满足 `<=100` 约束。

| subitem | step range | status |
|---|---|---|
| `SlightlyEasier / Statement interface` | `1-3` | `checked` |
| `small-prime cutoff (hodd / hprod / hp5)` | `4-6` | `checked` |
| `Case I divisibility transport across gcd quotient` | `7-9` | `checked` |
| `primitive normalization via MayAssume.coprime` | `10-12` | `checked` |
| `noncongruence normalization and dispatch` | `13-16` | `checked` |

1. 固定 odd regular prime `p`，以及一个候选整数解 `a^p + b^p = c^p`，并把本分支条件写成 `p ∤ abc`。
2. 记住本 unit 的 canonical hook 是 `CaseI.SlightlyEasier`、`CaseI.Statement`、`CaseI.may_assume`；它们共同承担的是 Case I 外层入口，而不是 ideal extraction 或收束矛盾。
3. 因而本 unit 的局部目标是：把原始 Case I 候选解整理成下游分圆分解可以直接接手的标准输入包。
4. 从 odd-prime 情形中抽出 small-prime cutoff；在本分支里真正进入技术论证的是 `p ≥ 5`，而不是已经被独立处理掉的 `p = 3`。
5. 这一 cutoff 保证 `a_not_cong_b` 里的 sign-swap 与 `ZMod p` 论证不会退化到 `p = 2` 或 `p = 3` 的例外算术。
6. 因此 `CaseI.SlightlyEasier` 所依赖的“clean arithmetic environment”之一，就是已经安装好的 `hp5` 级别下界。
7. 把 `p ∤ abc` 读成 Case I 的精确分支谓词：因为 `p` 是素数，这等价于 `p` 不整除 `a,b,c` 中任一项。
8. 这个分支谓词把本情形和 Case II 的 `p ∣ abc` 完全分开，并说明后续不应走 `π = ζ - 1` 的下降路线，而应走分圆因子分解路线。
9. 所以 `CaseI.Statement` 的公共接口，核心上就是“在 `p ∤ abc` 的条件下，把 Case I 交给更强的技术版陈述”。
10. 调用 `MayAssume.coprime`，把原始三元组除以公共 gcd，得到满足 primitive 条件的新三元组。
11. 该规整保持指数方程和非零积，因此并没有损坏 Case I 外层需要保留的结构信息。
12. 同时，`p ∤ abc` 会沿着这一步被运输到 primitive triple 上，于是之后可以只对 primitive 的 Case I 解工作。
13. 在 primitive Case I triple 上调用 `a_not_cong_b`，检查是否已经有 `a \not\equiv b [ZMOD p]`。
14. 若已经满足该非同余条件，则保持原三元组；否则做 sign / permutation normalization，换到一个等价三元组 `(x,y,z)`。
15. 这个替换保持方程、gcd、非零积和 `p ∤ xyz`，同时强制得到 `x \not\equiv y [ZMOD p]`，从而去掉后续线性因子分析中的坏同余构型。
16. 至此完成 `CaseI.may_assume` 的 outer dispatch：下游 unit 可以在 primitive、Case I、且已做非同余规整的标准三元组上进入 `a^p + b^p = ∏_{η∈μ_p}(a + η b)` 的 cyclotomic factorization。

Checklist verification: this public section is headed `regular primes / Case I outer statement`, names hooks `CaseI.SlightlyEasier`, `CaseI.Statement`, and `CaseI.may_assume`, and carries an independent local ledger of `16` steps.

### `FLT-HR-011` `regular primes / Case I ideal extraction`

Scope boundary: this unit is limited to the canonical package `Case I ideal extraction`; it does not prove Case I principalization, element recovery, Case II, or repo-local vendored theorem closure.

#### Human-Readable Expansion
##### 1. 本单元的精确任务

本单元只处理 Case I 中的 ideal 提取层，不负责后面的 principalization，也不负责最终同余矛盾。

局部输入是：

- `p` 为奇素数，且在本 Case I 包里已经有 `5 ≤ p`。
- `a ^ p + b ^ p = c ^ p`。
- `({a, b, c} : Finset ℤ).gcd id = 1`，即 primitive 条件。
- `caseI : ¬↑p ∣ a * b * c`。
- 固定 `K := CyclotomicField p ℚ`，`R := 𝓞 K`，再选定一个 `ζ ∈ nthRootsFinset p 1`。

局部输出不是元素级的
`a + ζ * b = unit × α ^ p`，
而只是 ideal 级的
`span ({a + ζ * b} : Set R) = I ^ p`。

这正是 `Case I principalization` 的输入边界。
值得强调的是：这一层还没有使用 `IsRegularPrime`。
regularity 真正开始发力，是下一单元的 `is_principal_aux / is_principal`。

##### 2. `ab_coprime core`：先把整数层的互素接口补齐

`exists_ideal` 要调用 `fltIdeals_coprime`，
而后者需要一个很干净的整数层输入：`a` 与 `b` 互素。
因此源码先证明
`ab_coprime`：

> 若 `a ^ p + b ^ p = c ^ p` 且 `({a,b,c}).gcd id = 1`，则 `IsCoprime a b`。

理由非常直接，但这是后面 ideal 互素接口的硬前提：

- 若 `gcd(a,b) ≠ 1`，取素数 `q` 整除它。
- 则 `q ∣ a` 且 `q ∣ b`，于是 `q ∣ a ^ p + b ^ p`。
- 由 `a ^ p + b ^ p = c ^ p` 可知 `q ∣ c ^ p`，再由素数整除幂推出 `q ∣ c`。
- 于是 `q` 同时整除 `a,b,c`，与 primitive 条件冲突。

所以 `ab_coprime` 的作用不是额外结论，而是把 primitive 信息从
`gcd(a,b,c)=1`
收缩成后续 cyclotomic factorization 真正要用的二元互素接口
`IsCoprime a b`。

##### 3. `exists_ideal cyclotomic product rewrite`：把元素等式改写成 ideal 等式

接下来进入分圆域整数环 `R = 𝓞(ℚ(ζ_p))`。
先把整数等式
`a ^ p + b ^ p = c ^ p`
强制 cast 到 `R`。

随后使用分圆恒等式
`pow_add_pow_eq_prod_add_mul`，
把左边改写成所有 `p` 次单位根对应线性因子的乘积：

`a ^ p + b ^ p = ∏_{η ∈ nthRootsFinset p 1} (a + η * b)`。

然后对这个元素等式施加 `span ({·} : Set R)`。
Lean 里这一步通过

- `prod_span_singleton`
- `span_singleton_pow`

把“元素乘积等式”变成“principal ideals 的乘积等式”：

`∏_{η} span ({a + η * b} : Set R) = (span ({c} : Set R)) ^ p`。

这一步是本单元的主桥：
它把原始的费马方程变成了一个
“有限个 principal ideal 的乘积是一个 `p` 次幂 ideal”
的全局结构式。

##### 4. `exists_ideal pairwise ideal coprimality interface`：把全局乘积拆成逐因子结构

只有全局乘积等式还不够；
若要从
`∏ J_η = L ^ p`
推出某个单独的 `J_ζ` 也是 `p` 次幂，
必须先知道这些 `J_η` 两两互素。

这正是源码里
`fltIdeals_coprime`
提供的接口。
在这里，

- `fltIdeals p a b hη = Ideal.span ({a + η * b} : Set R)`；
- `ab_coprime` 提供整数层的 `IsCoprime a b`；
- `caseI : ¬↑p ∣ a * b * c` 排除了坏的 ramification 纠缠；
- `η₁ ≠ η₂` 保证比较的是两个不同线性因子。

于是对于任意两个不同的 `η₁, η₂ ∈ nthRootsFinset p 1`，
`exists_ideal` 都能调用
`fltIdeals_coprime`
得到：

`IsCoprime (span ({a + η₁ * b} : Set R)) (span ({a + η₂ * b} : Set R))`。

这一步正是审计表里原先曾单列的
`exists_ideal pairwise ideal coprimality interface`。
它的地位非常关键：
没有这层 pairwise coprimality，
全局 `p` 次幂结构不能安全地下钻到单个因子。

##### 5. `exists_ideal single-factor p-th power extraction`：从全局乘积抽出单个 `p` 次幂 ideal

有了上面的两块数据：

- 全局乘积等式
  `∏_{η} span ({a + η * b} : Set R) = (span ({c} : Set R)) ^ p`；
- 各因子两两互素；

就可以调用
`exists_eq_pow_of_mul_eq_pow_of_coprime`
这类有限乘积抽根引理。

Lean 中的做法是：

- 把全体线性因子 ideal 看成一个有限族；
- 用 pairwise coprimality 验证引理的互素前提；
- 以所选的 `ζ` 为目标因子；
- 从全局 `p` 次幂乘积中抽出一个 ideal `I`，满足
  `span ({a + ζ * b} : Set R) = I ^ p`。

这就是 `exists_ideal` 的最终输出。

请注意这个输出的粒度：

- 已知的是“该 principal ideal 等于某个 ideal 的 `p` 次幂”；
- 还不知道这个 `I` 本身 principal；
- 也还没有选出元素 `α` 使 `a + ζ * b = unit × α ^ p`。

换句话说，本单元只把
`cyclotomic factorization`
推进到了
`ideal-level p-th power structure`，
故意停在这里，等待下一单元用 regularity 做 principalization。

##### 6. `f / auxf' / auxf zero-coefficient witness`：本 package 顺带交给下一层的稀疏系数接口

按数学内容说，`f / auxf' / auxf` 已经开始靠近后续的 element-level 收束；
但在源码分层里，它们和 `exists_ideal` 同处一个 Case I 文件，
并且审计表把它们一并记在本 package 下，
因此这里需要把这个接口也交代清楚。

定义稀疏函数
`f (a b : ℤ) (k₁ k₂ : ℕ) : ℕ → ℤ`，
其支撑只落在四个位置：

- `0` 处系数是 `a`；
- `1` 处系数是 `b`；
- `k₁` 处系数是 `-a`；
- `k₂` 处系数是 `-b`；
- 其他位置系数全为 `0`。

`auxf'` 与 `auxf` 的内容是：

- 因为 `p ≥ 5`，而这个支撑至多只有四个点，
  所以 `range p` 中一定还能找到一个索引 `i`
  不在这四个点里；
- 因而 `f a b k₁ k₂ i = 0`；
- `auxf'` 先给出 `i ∈ range p` 的版本，
  `auxf` 再把它打包成 `Fin p` 版本。

这一步本身不再抽 ideal，
但它给后面的 `dvd_coeff_cycl_integer` 提供了一个
“至少有一个系数为零”的可调用见证。
因此在 package 边界上，
它扮演的是一个向下一层输出的技术接口。

##### 7. 本单元与前后单元的边界

本单元接收上一单元 `Case I outer statement` 已经规整好的输入：

- primitive 条件；
- `p ∤ abc`；
- 非坏同余配置已经由外层 route 准备妥当。

本单元输出给下一单元 `Case I principalization` 的核心对象只有一个：

- `∃ I, span ({a + ζ * b} : Set R) = I ^ p`。

因此本单元的逻辑定位可以压缩成一句话：

> 用分圆分解得到全局 ideal 乘积，再借 pairwise coprimality 把它逐因子地抽成 `p` 次幂 ideal。

#### Local Budget Ledger
本 unit 的局部 ledger 总计 `21` 步，满足 `<=100` 约束。

| subitem | step range | status |
|---|---|---|
| `ab_coprime core` | `1-4` | `completed` |
| `exists_ideal cyclotomic product rewrite` | `5-9` | `completed` |
| `exists_ideal pairwise ideal coprimality interface` | `10-14` | `completed` |
| `exists_ideal single-factor p-th power extraction` | `15-18` | `completed` |
| `f / auxf' / auxf zero-coefficient witness` | `19-21` | `completed` |

1. 假设 `gcd(a,b) ≠ 1`，取素数 `q` 整除这个 gcd。
2. 由 `q ∣ a` 与 `q ∣ b`，得到 `q ∣ a ^ p + b ^ p`；再借 `a ^ p + b ^ p = c ^ p` 得 `q ∣ c ^ p`，从而 `q ∣ c`。
3. 因此 `q` 同时整除 `a,b,c`，于是 `q` 整除 `({a,b,c} : Finset ℤ).gcd id`。
4. 这与 primitive 条件冲突，故 `IsCoprime a b`；这一步就是 `ab_coprime`。
5. 进入 `K = ℚ(ζ_p)` 与其整数环 `R = 𝓞 K`，把 `a ^ p + b ^ p = c ^ p` cast 到 `R`。
6. 用 `pow_add_pow_eq_prod_add_mul` 把 `a ^ p + b ^ p` 重写成 `∏_{η ∈ nthRootsFinset p 1} (a + η * b)`。
7. 对该等式施加 `span ({·} : Set R)`，把元素乘积等式转换成 principal ideal 的乘积等式。
8. 用 `prod_span_singleton` 与 `span_singleton_pow` 把右边整理成 `(span ({c} : Set R)) ^ p`。
9. 得到全局 ideal 等式：所有线性因子生成的 principal ideals 的乘积是一个 `p` 次幂 ideal。
10. 固定两个不同的根 `η₁ ≠ η₂`，目标是证明对应 ideal 两两互素。
11. 把第 `4` 步得到的 `IsCoprime a b` 输入 `fltIdeals_coprime` 的整数层前提。
12. 把 `caseI : ¬↑p ∣ a * b * c` 输入 `fltIdeals_coprime` 的 Case I 前提，排除坏公共因子。
13. 对任意 `η₁ ≠ η₂`，推出 `span ({a + η₁ * b} : Set R)` 与 `span ({a + η₂ * b} : Set R)` 互素。
14. 这就关闭了 `exists_ideal pairwise ideal coprimality interface` 这个局部接口缺口。
15. 将第 `9` 步的全局乘积等式和第 `13` 步的 pairwise coprimality 一起送入 `exists_eq_pow_of_mul_eq_pow_of_coprime`。
16. 选择固定的目标根 `ζ ∈ nthRootsFinset p 1` 作为要抽出的单个因子。
17. 从全局 `p` 次幂乘积中提取出一个 ideal `I`，满足 `span ({a + ζ * b} : Set R) = I ^ p`。
18. 这就是 `exists_ideal` 的精确输出，也是下一单元 `Case I principalization` 的输入。
19. 另外定义稀疏系数函数 `f a b k₁ k₂`，其支撑只可能落在 `0,1,k₁,k₂` 四个位置。
20. 因为 `p ≥ 5`，`range p` 不会被这至多四个支撑点填满，所以 `auxf'`、`auxf` 能构造出一个索引 `i` 使 `f a b k₁ k₂ i = 0`。
21. 这个零系数见证随后供 `dvd_coeff_cycl_integer` 使用，作为本 package 输出给下一层的技术接口。

Checklist verification: this public section is headed `regular primes / Case I ideal extraction`, names hooks `ab_coprime`, `auxf'`, `auxf`, and `exists_ideal`, and carries an independent local ledger of `21` steps.

### `FLT-HR-012` `regular primes / Case I principalization`

Scope boundary: this unit is limited to the canonical package `Case I principalization`; it does not prove Case I element recovery, Case II, or repo-local vendored theorem closure.

#### Human-Readable Expansion
##### 1. 本单元承接什么，目标又是什么

在 Case I 中，上一单元 `Case I ideal extraction` 已经把选定的线性因子

`x := a + η b`

对应到分圆整数环 `O_K` 里的某个 ideal `I`，并给出标准形：

`span {x} = I^p`

这里左边天然是 principal ideal，因为它就是由单个元素 `x` 生成的 ideal。
所以本单元真正要做的事只有三步：

1. 先把上一单元交出的 `span {x} = I^p` 改写成“`I^p` 是 principal ideal”。
2. 再把 regular prime 假设真正消耗掉，用它推出 `I` 本身已经 principal。
3. 最后把这个 principal ideal 重新翻回元素陈述，得到
   `x = ε * α^p`，其中 `ε` 是单位、`α ∈ O_K`。

这就是审计表里 `Case I principalization` 的精确位置：
它既不负责抽 ideal，也不负责完成最终矛盾，
而是负责把“ideal-level 的 `p` 次幂信息”桥接回“元素层的 `unit × p` 次幂控制”。

##### 2. 为什么 regularity 正好能完成 principalization

这里真正消耗的 formal hook 是 setup 层的 principalization engine：

- `isPrincipal_of_isPrincipal_pow_of_coprime`

它的数学含义很直接。把 `I` 放到 class group 里看，记其类为 `[I]`。
若 `I^p` 是 principal，那么在 class group 中就有

`[I]^p = [I^p] = 1`

另一方面，`[I]` 的阶一定整除 class group 的基数。
而 `regular prime` 的定义正是要求 `p` 与这个 class-number 互素。
因此，一个阶整除 `h_K` 的群元素如果又被 `p` 杀死，
在 `gcd(p, h_K) = 1` 的条件下只能是平凡元。
于是 `[I] = 1`，也就是 `I` 本身 principal。

所以 regularity 在 Case I 里不是装饰性标签，
而是恰好把

`I^p principal`

降回

`I principal`

的关键输入。没有这一步，就只能停留在 ideal-level，
根本无法回到后续需要的元素级表达式。

##### 3. `is_principal_aux` 的局部证明动作

`is_principal_aux` 的工作可以按审计命名拆成五段。

第一段是

- `is_principal_aux: certify (I^p).IsPrincipal`

这一步只用上一单元交出的等式 `span {x} = I^p`。
因为 `span {x}` 本来就是主理想，所以把等式反向改写以后，
立刻得到 `(I^p).IsPrincipal`。

第二段是

- `is_principal_aux: apply regularity`

这一步把上面的 principality 见证和 regularity 提供的 coprimality
一起送入 `isPrincipal_of_isPrincipal_pow_of_coprime`，
从而输出 `I.IsPrincipal`。
到这里为止，证明仍然只在 ideal 层面移动。

第三段是

- `is_principal_aux: raise to p-th powers and normalize spans`

既然 `I` principal，就可选 `α` 使 `I = span {α}`。
把这个等式升到 `p` 次幂，可得

`I^p = (span {α})^p = span {α^p}`

再与最初的 `span {x} = I^p` 拼接，就得到

`span {x} = span {α^p}`

这一步很关键，因为它把“某个抽象 ideal principal”重新落回“具体元素 `x` 与 `α^p` 生成同一 principal ideal”。

第四段是

- `is_principal_aux: unit extraction and final witness`

两个单生成 principal ideals 相等，等价于它们的生成元互为 associate。
于是存在单位 `ε`，使得

`x = ε * α^p`

这就是本单元真正要交给下一单元的输出：
不是最终矛盾，而是一个已经经过 regularity 消毒的、可直接用于元素运算的 witness。

##### 4. `is_principal` wrapper 的作用与边界

审计表里还单列了

- `is_principal wrapper`

它不是新的数学核心，而是一个封装层。
上一单元交出的数据往往带着具体根 `η`、具体线性因子 `x`、
以及由 `exists_ideal` 构造出来的 ideal witness；
`is_principal_aux` 则更像一个抽象模板：
“只要给我 `span {x} = I^p`，再给 regularity，我就把它 principalize 并吐出 `unit × p` 次幂见证。”

因此 `is_principal` 的职责只是把上游的具体数据喂给这个模板，
并把模板的输出重新包装成 Case I 主线可继续消费的形式。

这也解释了本单元与相邻单元的边界：

- `FLT-HR-011` 负责把 cyclotomic factorization 变成 `I^p` 数据。
- 本单元负责把 `I^p` 数据经由 regularity 转成 `x = ε * α^p` 这类局部控制。
- `FLT-HR-013` 再利用这个 witness 做有限索引整理、单位管理与局部同余收口。

##### 5. 本单元在整条 Case I 链中的地位

从 proof pipeline 看，这一段是 Kummer 路线真正显出
“regular primes 与低指数特例不同” 的地方。
`n = 3` 或 `n = 4` 分支更多是直接在元素层做算术整理；
regular primes 则必须先进入 class-group / ideal 的世界，
再靠 regularity 把 ideal-level 结论拉回 element-level。

因此，本单元的价值不在于推出一个长公式，
而在于完成整个 Case I 最难替代的一次桥接：

`cyclotomic factorization`
`→ ideal p-th power extraction`
`→ principalization via regularity`
`→ 单位 × p` 次幂见证

只要这一步完成，后面的元素级整理就重新回到了可以计算、
可以比较系数、也可以制造模 `p` 矛盾的轨道上。

#### Local Budget Ledger
对齐信息：

- Canonical package: `Case I principalization`
- Formal hooks: `is_principal_aux`, `is_principal`
- Repo-local boundary: `RegularPrimesPath.lean` 仅锚定 statement shape / module path / terminal theorem；本 unit 的 formal hook 本体未在本仓库 vendored
- 审计预算: `13` 步，满足 `<=100` 约束
- Checklist verification: this public section is headed `regular primes / Case I principalization`, names hooks `is_principal_aux` and `is_principal`, and carries an independent local ledger of `13` steps.

| subitem | step range | status |
|---|---:|---|
| `is_principal wrapper` | `1-2` | `checked` |
| `is_principal_aux: certify (I^p).IsPrincipal` | `3-4` | `checked` |
| `is_principal_aux: apply regularity` | `5-7` | `checked` |
| `is_principal_aux: raise to p-th powers and normalize spans` | `8-10` | `checked` |
| `is_principal_aux: unit extraction and final witness` | `11-13` | `checked` |

1. 固定上一单元交出的具体线性因子 `x := a + η b` 与 ideal `I`，其接口数据是 `span {x} = I^p`。
2. 把要证的具体 Case I 结论先收缩到抽象模板 `is_principal_aux`；`is_principal` 只负责完成这层包装与解包。
3. 由 `x` 是单个元素，立即知道 `span {x}` 是 principal ideal。
4. 用第 1 步的等式改写第 3 步，得到 `(I^p).IsPrincipal`。
5. 调入 regular prime 假设提供的 class-number coprimality，使 principalization engine 的前提齐备。
6. 应用 `isPrincipal_of_isPrincipal_pow_of_coprime`，推出 `I.IsPrincipal`。
7. 选取 `α` 作为 `I` 的生成元，写成 `I = span {α}`。
8. 将第 7 步升到 `p` 次幂，得到 `I^p = (span {α})^p`。
9. 用 principal ideal 的幂次公式把右边标准化为 `span {α^p}`。
10. 联立第 1 步与第 9 步，得到 `span {x} = span {α^p}`。
11. 由两个单生成 principal ideals 相等，抽出一个单位 `ε`，满足 `x = ε * α^p`。
12. 把 `(ε, α)` 重新打包成 `is_principal_aux` 返回的局部 witness。
13. 将该 witness 交给下游 `Case I element recovery / close`，供其继续做有限索引整理与最终局部同余矛盾。

### `FLT-HR-013` `regular primes / Case I element recovery and close`

Scope boundary: this unit is limited to the canonical package `Case I element recovery / close`; it closes the Case I local interface and does not prove Case II or repo-local vendored theorem closure.

#### Human-Readable Expansion
##### Canonical Alignment

| canonical node | formal hook | 本 unit 的局部作用 |
|---|---|---|
| `Case I element recovery / close` | `ex_fin_div` | 把上一单元给出的 `unit × pth-power` 见证改写成一个四项稀疏和的 `p`-整除关系，并抽出 `k₁,k₂ : Fin p` |
| `Case I element recovery / close` | `caseI_easier` | 排除坏索引重合，把 divisibility of sparse sum 变成系数整除，从而推出 `p ∣ a` 并与 Case I 假设矛盾 |
| `Case I element recovery / close` | `caseI` | 把上一步的局部矛盾接回 outer statement 层，由 `CaseI.may_assume` 完成原始 Case I 结论 |

此前曾单列但未单独提升为跨文件 high-risk leaf 的
`caseI_easier / aux-index exclusion`
就在本 unit 内被吸收并关闭。

##### 输入与输出

本 unit 固定以下局部输入：

- `hreg : IsRegularPrime p`
- `hp5 : 5 ≤ p`
- `hgcd : ({a, b, c} : Finset ℤ).gcd id = 1`
- `hab : ¬a ≡ b [ZMOD p]`
- `caseI : ¬↑p ∣ a * b * c`
- `H : a ^ p + b ^ p = c ^ p`
- `hζ : IsPrimitiveRoot ζ p`

上一单元 `is_principal` 的输出是：

`∃ (u : Rˣ) (α : R), ↑u * α ^ p = ↑a + ζ * ↑b`

这里 `R` 是 `p` 次分圆域整数环。  
本 unit 的任务就是把这个元素级输出转写成一个能在系数层面直接制造矛盾的 sparse relation。

##### 一、`ex_fin_div`：从 `unit × pth-power` 到四项稀疏和

`ex_fin_div` 是本 unit 的第一段实质内容。它不再讨论 ideal，而是直接消费上一单元交来的元素式
`↑u * α ^ p = ↑a + ζ * ↑b`。

核心动作分成三步：

1. 先把 `ζ` 放到分圆域 `K` 中，并把 primitive root 结构同步过去。这样 `a + ζ b` 就处在 `exists_int_sum_eq_zero` 的标准输入形状里。
2. 再把 `a + ζ b = unit × pth-power` 交给 cyclotomic auxiliary theorem `exists_int_sum_eq_zero`。它返回某个整数 `k`，使
   `a + bζ - ζ^(2k) * (a + bζ^(-1))`
   落在 ideal `(p)` 中。
3. 最后把 `2k` 与 `2k - 1` 的模 `p` 剩余类分别打包成 `k₁, k₂ : Fin p`，并把 `ζ^(-1)` 统一改写成模 `p` 指数。这一步给出本 unit 真正要用的输出：
   `k₂ ≡ k₁ - 1 [ZMOD p]`
   且
   `↑p ∣ ↑a + ↑b * ζ - ↑a * ζ ^ (k₁ : ℕ) - ↑b * ζ ^ (k₂ : ℕ)`。

因此，`ex_fin_div` 完成的不是新的 principalization，而是把 principal generator witness 压缩成一个“只有四个系数可能非零”的 cyclotomic divisibility statement。

##### 二、`caseI_easier / aux-index exclusion`：排除所有会让稀疏和塌缩的坏索引

`caseI_easier` 先假设 `H : a ^ p + b ^ p = c ^ p`，然后调用 `ex_fin_div` 得到 `k₁,k₂,hcong,hdiv`。

接下来定义系数函数
`f a b k₁ k₂ : ℕ → ℤ`，
只在四个位置可能非零：

- `0 ↦ a`
- `1 ↦ b`
- `k₁ ↦ -a`
- `k₂ ↦ -b`

剩下的位置都送到 `0`。

这时真正危险的地方是：如果 `k₁` 或 `k₂` 跟 `0`、`1`、彼此本身重合，四项稀疏和就会塌缩，后面的系数提取不能直接使用。  
因此 `caseI_easier` 中间插入了一整组辅助排除：

- `aux0k₁` 排除 `k₁ = 0`
- `aux0k₂` 排除 `k₂ = 0`
- `aux1k₁` 排除 `k₁ = 1`
- `aux1k₂` 排除 `k₂ = 1`
- `auxk₁k₂` 排除 `k₁ = k₂`

这些引理的作用分工很清楚：

- `aux0k₁`、`aux0k₂`、`aux1k₂` 都把“索引碰撞”重新送进 `dvd_coeff_cycl_integer`，从而推出 `p ∣ a` 或 `p ∣ b`，再与 `caseI : ¬↑p ∣ a*b*c` 矛盾。
- `aux1k₁` 把碰撞改写成 `a ≡ b [ZMOD p]`，直接和 `hab` 冲突。
- `auxk₁k₂` 纯粹使用 `k₂ ≡ k₁ - 1 [ZMOD p]` 这条同余；若二者相等，就会得到 `1 ≡ 0 [ZMOD p]`，与素数模下的基本算术冲突。

所以，`caseI_easier / aux-index exclusion` 的数学意义是：

> 保证 `0, 1, k₁, k₂` 在 `range p` 中确实对应四个可区分的位置，
> 从而 `f` 真的是一个 support 只有四点的稀疏系数函数。

##### 三、`caseI_easier / sparse-sum coefficient close`：从稀疏和的 `p`-整除推出 `p ∣ a`

有了上面的排除之后，`caseI_easier` 才能把 `hdiv` 精确重写成

`↑(p : ℤ) ∣ ∑ j ∈ range p, f a b k₁ k₂ j • ζ ^ j`。

这一步把 `ex_fin_div` 产出的四项 relation 变成了一个标准的 cyclotomic integer sum。

之后 proof 的 closing move 有两层：

1. 用 `auxf hp5 a b k₁ k₂` 找到某个 `i : Fin p`，满足 `f a b k₁ k₂ (i : ℕ) = 0`。  
   这正是 `p ≥ 5` 的局部用途：`range p` 至少有五个位置，而 `f` 最多只有四个位置可能非零，所以一定能找到一个“空位”。
2. 把这个空位和前面的 `key` 一起交给 `dvd_coeff_cycl_integer`。  
   这个 theorem 的局部含义是：如果一条 cyclotomic 整数线性组合整体被 `p` 整除，而且我们能指定一个零系数位置作支点，那么其余系数也会继承 `p`-整除约束。

`caseI_easier` 最后请求的是索引 `0` 处的系数。  
按 `f` 的定义，索引 `0` 的系数正好是 `a`，所以机器上 `simpa [f]` 直接得到
`↑p ∣ a`。

一旦 `p ∣ a`，就立刻有 `p ∣ a*b*c`。这与 Case I 的分支假设 `¬↑p ∣ a*b*c` 矛盾，于是 `H` 被排除，得到
`a ^ p + b ^ p ≠ c ^ p`。

因此，本 unit 的真正 closing sentence 是：

> principalization 交出的 `unit × pth-power` 见证，
> 在 `ex_fin_div` 中变成一个四项 sparse divisibility；
> 这个 sparse divisibility 在 `caseI_easier` 中又被压回到单个系数 `a` 的 `p`-整除；
> 而 `p ∣ a` 与 Case I 假设正面冲突。

##### 四、`caseI`：把局部收口接回 outer statement

本 unit 的最后一个 theorem `caseI` 非常短，但它承担 statement-level closure：

- 它不再重复 primitive reduction、小素数 cutoff、或坏同余规整。
- 这些外层工作都由上一单元 `FLT-HR-010 / Case I outer statement` 中已经解释过的 `CaseI.may_assume` 处理。
- `caseI` 这里只是把 `caseI_easier` 作为 handler 交给 `CaseI.may_assume`。

所以本 unit 与 `FLT-HR-010` 的边界很清楚：

- `FLT-HR-010` 负责把任意 Case I 候选解规整到 `hgcd`、`hab`、`caseI` 这些“更容易版”输入。
- `FLT-HR-013` 负责在这些更容易版输入下，真正完成 element-level closure 并打出矛盾。

这也解释了为什么本 unit 的 canonical formal hook 恰好是
`ex_fin_div`、`caseI_easier`、`caseI`：

- `ex_fin_div` 是 element recovery；
- `caseI_easier` 是 local contradiction；
- `caseI` 是 branch closure。

#### Local Budget Ledger
本 unit 的独立 ledger 总计 `25` 步，满足 `<=100` 约束。

Checklist verification: this public section is headed `regular primes / Case I element recovery and close`, names hooks `ex_fin_div`, `caseI_easier`, and `caseI`, and carries an independent local ledger of `25` steps.

| subitem | step range | status |
|---|---|---|
| `ex_fin_div / principal-generator witness` | `1-6` | `checked` |
| `ex_fin_div / k₁,k₂ : Fin p packaging` | `7-10` | `checked` |
| `caseI_easier / aux-index exclusion` | `11-17` | `checked` |
| `caseI_easier / sparse-sum coefficient close` | `18-23` | `checked` |
| `caseI / may_assume wrapper` | `24-25` | `checked` |

1. 在 `ex_fin_div` 中把输入 primitive root `ζ : R` 强制上推到分圆域 `K`，记为 `ζ'`，并把 `hζ` 转成 `hζ' : IsPrimitiveRoot ζ' p`。
2. 调用上一单元已经关闭的 `is_principal hreg hp5 hgcd caseI H hζ`，得到 `u : Rˣ` 与 `α : R`，满足 `↑u * α ^ p = ↑a + ζ * ↑b`。
3. 用 canonical root `hζ'.unit'`、`pow_one` 与乘法交换，把上式改写成 `exists_int_sum_eq_zero` 的标准输入形状 `a + b * ζ = u * α^p`。
4. 由 `hp5 : 5 ≤ p` 立刻得到 `p ≠ 2`，因此满足 `exists_int_sum_eq_zero` 需要的 `2 < p`。
5. 对 `x = a`、`y = b`、`i = 1` 应用 `exists_int_sum_eq_zero hζ' a b 1 hu.symm`，得到某个整数 `k`，使
   `a + bζ - ζ^(2k) * (a + bζ^(-1))`
   落在 ideal `(p)` 中。
6. 把“落在 `(p)` 中”重新解释为 divisibility statement，得到一个 raw `p`-整除关系，准备进入模 `p` 指数整理。
7. 设 `k₁ := ((2 * k) % p).natAbs`，并把它连同范围证明一起打包成 `Fin p`。
8. 设 `k₂ := ((2 * k - 1) % p).natAbs`，同样打包成 `Fin p`。
9. 用 `emod_nonneg` 与 `emod_lt_of_pos` 证明这两个整数剩余类都落在 `0 ≤ r < p`，因此 `k₁`、`k₂` 的 `Fin p` 打包合法。
10. 用 `zpow_eq_one_iff_dvd`、`ZMod.intCast_zmod_eq_zero_iff_dvd` 和指数改写，把 step `5-6` 的 raw 关系整理成
    `k₂ ≡ k₁ - 1 [ZMOD p]`
    以及
    `↑p ∣ ↑a + ↑b * ζ - ↑a * ζ ^ (k₁ : ℕ) - ↑b * ζ ^ (k₂ : ℕ)`。
11. 在 `caseI_easier` 中反设 `H : a ^ p + b ^ p = c ^ p`，并调用 `ex_fin_div hp5 hreg hζ hgcd caseI H` 取得 `k₁,k₂,hcong,hdiv`。
12. 定义系数函数 `f a b k₁ k₂`：索引 `0` 处取 `a`，索引 `1` 处取 `b`，索引 `k₁` 处取 `-a`，索引 `k₂` 处取 `-b`，其余一律取 `0`。
13. 用 `aux0k₁` 排除 `k₁ = 0`；若发生这类碰撞，`dvd_coeff_cycl_integer` 会把 `hdiv` 压回到某个基本系数的 `p`-整除，进而推出 `p ∣ a*b*c`，与 `caseI` 冲突。
14. 用 `aux0k₂` 排除 `k₂ = 0`；这一分支会直接把矛盾压成 `p ∣ a`，从而再次违背 `caseI`。
15. 用 `aux1k₁` 排除 `k₁ = 1`；这一分支把 sparse relation 改写成 `a ≡ b [ZMOD p]`，直接和 `hab` 矛盾。
16. 用 `aux1k₂` 排除 `k₂ = 1`；这一分支同样会导出 Case I 禁止出现的 `p`-整除结论。
17. 用 `auxk₁k₂ hcong` 排除 `k₁ = k₂`；若二者相等，则 `k₂ ≡ k₁ - 1 [ZMOD p]` 退化成 `1 ≡ 0 [ZMOD p]`，与素数模算术矛盾。
18. 由 step `13-17` 的全部排除，把 `hdiv` 精确改写成
    `↑(p : ℤ) ∣ ∑ j ∈ range p, f a b k₁ k₂ j • ζ ^ j`，
    记为 cyclotomic sum 的全局整除关系 `key`。
19. 这一步的重写中，所有 `sum_ite`、`filter` 与 `range` 化简都已经由坏索引排除保障，因此不会再出现 support 碰撞导致的额外项。
20. 调用 `auxf hp5 a b k₁ k₂`，在 `range p` 里选出某个 `i : Fin p`，使 `f a b k₁ k₂ (i : ℕ) = 0`；其根本原因是 `p ≥ 5` 而 `f` 至多有四个非零位置。
21. 把这个“空位”与 `key` 一起送进 `dvd_coeff_cycl_integer`；该 theorem 允许从整个 cyclotomic sum 被 `p` 整除，回收到单个系数的 `p`-整除。
22. 在 `caseI_easier` 的最终调用中，请求的是索引 `0` 的系数；按 `f` 的定义，索引 `0` 的系数正好是 `a`。
23. 因而 `simpa [f]` 直接得到 `↑p ∣ a`，再乘上 `b*c` 推出 `↑p ∣ a*b*c`，与 `caseI` 矛盾，故 `a ^ p + b ^ p ≠ c ^ p`。
24. 在最终 theorem `caseI` 中，把 step `11-23` 已经建立的 `caseI_easier` 作为 handler 交给 `CaseI.may_assume`。
25. `CaseI.may_assume` 负责导入已关闭的 outer-layer 规整：small-prime cutoff、primitive normalization、坏同余规整；因此 step `23` 的局部矛盾自动提升成原始 Case I 结论，完成本 unit closure。

### `FLT-HR-014` `regular primes / Case II pi-language reduction`

Scope boundary: this unit is limited to the canonical package `Case II π-language`; it sets up the π-language interface and does not prove ideal-factor extraction, distinguished-root divisibility, descent core, close/merge, or repo-local vendored theorem closure.

#### Human-Readable Expansion
##### 1. 这个 package 在 Case II 里到底负责什么

Case II 的整数入口已经在上一层规整成：

- `x^p + y^p = z^p`
- `gcd(x,y,z) = 1`
- `p | z`
- `p ∤ y`

下文统一把 primitive triple 记成 `x,y,z`；若与上游 statement 中常见的 `a,b,c` 对照，只是字母替换。这里真正关键的不是记号，而是：

> 这一支的下降量不再由“整数绝对值”控制，
> 而由分圆域整数环里 `π = ζ - 1` 的幂次控制。

因此本 package 的职责不是做真正的下降，
也不是提取 `𝔠 η`、`𝔞 η` 这类 ideal 对象，
而是先把整数层的 `p`-整除语言，
完整改写成后续能持续使用的 `π`-language。

审计里这一步对应的 formal hook 是：

- `zeta_sub_one_dvd`
- `span_pow_add_pow_eq`
- `div_one_sub_zeta_mem`
- `div_zeta_sub_one_Bijective`

对应的 canonical 子项则固定为：

1. `global π-divisibility of the generalized equation`
2. `rootwise π-divisibility of linear factors`
3. `integral quotient packaging`
4. `residue-class injectivity`
5. `residue-class bijection`

##### 2. 为什么整数里的 `p | z` 要改写成 `π | z`

设 `K = Q(ζ)`，`O_K` 是 `p` 次分圆域的整数环，记

`π = ζ - 1`.

在 `O_K` 中，素数 `p` 的 ramification 完全集中在这一个方向上：

`p = unit * π^(p-1)`.

因此，对嵌入到 `O_K` 里的整数来说，
“被 `p` 整除”与“落到 `π` 上方的唯一 ramified 素方向里”是同一件事的两种写法。

人类读者真正要记住的是：

> Case II 不是继续在 `ℤ` 里追 `v_p`，
> 而是进入 `O_K` 后改追 `π = ζ - 1` 的整除层级。

这一步一旦完成，
后面的下降参数就不再写成“`z` 里含有多少个 `p`”，
而写成“方程右边含有多少块 `π^p`”。

##### 3. 为什么必须把原方程扩展成 generalized equation family

如果只盯着原始方程

`x^p + y^p = z^p`,

那么每做一次 cyclotomic 分解、除去一个公共 `π`、再整理单位，
方程的形状都会改变。

所以 formal proof 不直接在原始方程上下降，
而是先扩成一族封闭的 generalized Case II 方程：

`x^p + y^p = ε * π^(p*(m+1)) * z0^p`

也可以等价写成

`x^p + y^p = ε * (π^(m+1) * z0)^p`,

其中：

- `m ≥ 0`
- `ε` 是 `O_K` 的单位
- `π ∤ y`
- `π ∤ z0`

这里的核心不是“写得更复杂”，
而是把未来下降时一定会出现的两类噪声提前显式化：

1. 单位 `ε`
2. `π` 的可见幂次

只有把这两件事一开始就放进 statement，
后面的 `m+1 -> m` 才是同一类方程内部的下降，
而不是每降一步就换一个 theorem 目标。

##### 4. 从全局 `π`-整除到每个线性因子的 `π`-整除

在 `O_K` 中有熟悉的分解：

`x^p + y^p = ∏_{η ∈ μ_p} (x + η y)`.

一旦右边写成 generalized equation，
左边就带有显式的 `π^(p*(m+1))`。
由于在模 `π` 的意义下所有 `p` 次单位根都满足

`η ≡ 1 (mod π)`,

所以每个线性因子都有相同的一阶近似：

`x + η y ≡ x + y (mod π)`.

而 generalized equation 的全局 `π`-整除恰好逼出

`x + y ≡ 0 (mod π)`,

于是得到：

`π | (x + η y)` 对每个 `η ∈ μ_p` 都成立。

这就是 canonical 子项
`rootwise π-divisibility of linear factors`
的数学内容。

它的作用非常局部但非常关键：

> 后面并不是凭空定义 `𝔠 η`，
> 而是因为每个 `x + η y` 都已经显式含有一个公共 `π`，
> 才能把“除去一个 `π` 之后剩下什么”系统地包装起来。

这里 package 只负责把“每个因子都含 `π`”这件事说清楚；
真正把这些 quotient 组织成 ideal-level 对象，
是下一单元的职责。

##### 5. 为什么“除以 `π`”之后仍然留在整数环里

知道 `π | (x + η y)` 还不够，
因为后面真正要用的是“把这个 `π` 除掉以后仍然是一个合法的 `O_K` 元”。

这正是

- `div_one_sub_zeta_mem`

这类引理的角色。

它们控制的不是大范围 descent，
而是一个很基础但不能跳过的整性问题：

> 某些看起来像 `(1 - η) / (1 - ζ)`、
> 或“线性因子除以 `ζ - 1`”的表达式，
> 仍然属于 `O_K`，
> 因而可以在整数环内部继续做 ideal / residue-class 运算。

从人类视角看，
这一步是在把“可整除”升级成“可安全地取商并继续工作”。

如果没有这层 quotient packaging，
后面关于 `𝔠 η` 的定义就会悬空，
因为你根本还没有证明相应 quotient 是整数环里的对象。

##### 6. residue-class injectivity / bijection 为什么在这里出现

把公共 `π` 除掉以后，
不同 root 对应的 quotient 不能全部塌成一个 residue class。
否则后面你就无法区分各个因子，
也很难证明 pairwise coprimality。

这里 formal proof 利用的是一个经典现象：

`(η - 1) / (ζ - 1)`

在 `O_K` 中是整的，
而且它模 `π` 的剩余正好记录了 root 的 residue-class 信息。

于是得到两层结论：

1. `residue-class injectivity`
   不同 `η` 给出不同的归一化剩余类；
2. `residue-class bijection`
   这些归一化剩余类正好跑遍需要的非零 residue classes。

人类可读地说，
这意味着：

> 虽然每个 `x + η y` 都先共同含有一个 `π`，
> 但把这层公共 ramification 去掉以后，
> 各个 root 方向仍然是彼此可区分的，
> 不会在 mod-`π` 世界里混成同一个因子。

这一步还没有正式推出 pairwise coprimality，
但它正是下一单元开始做 ideal-factor layer 时所需的 residue-level 预处理。

##### 7. 本单元与下一单元的边界

本单元到这里就应当停止。

已经完成的内容是：

- 把整数 `p`-整除改写成 `π`-整除；
- 把原始 Case II 方程扩成 generalized equation family；
- 说明每个线性因子都显式含有一个 `π`；
- 证明除去该 `π` 的 quotient 仍在整数环里；
- 证明这些 quotient 的 residue-class 数据彼此可分辨并形成完整参数化。

仍然不在本单元内的内容是：

- 定义 `𝔠 η` 与 `𝔞 η`
- 把全局乘积改写成局部 `p` 次幂 ideal
- 从 residue 信息升级到 pairwise coprimality 与 distinguished root 分析

这些都属于后续 `FLT-HR-015` 与 `FLT-HR-016`。

所以，`FLT-HR-014` 的稳定人类结论可以压缩成一句话：

> Case II 的第一步不是直接下降，
> 而是先把整数解翻译成一个带单位、带 `π`-幂次、带 factorwise quotient 的 generalized cyclotomic language；
> 一旦这套语言准备好，后面的 ideal-factor layer、distinguished root 与 descent core 才有统一的工作平台。

#### Local Budget Ledger
Source anchors:

- repo-local anchor: `Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/RegularPrimesPath.lean`
- upstream module anchor: `FltRegular/CaseII/Statement.lean`
- upstream module anchor: `FltRegular/CaseII/AuxLemmas.lean`
- upstream module anchor: `FltRegular/CaseII/InductionStep.lean`

本 unit 的局部 proof budget 总计 `18` 步，
与 `machine_checked_audit.md` / `process_audit.md` / `regular_primes_proof_process.md`
中对 `Case II π-language` 的预算摘要一致，
并且不再额外派生新的 canonical descendant。

- Total local proof steps: `18`
- Budget status: `checked`
- Completion condition: satisfied (`18 <= 100`)

| subitem | step range | status |
|---|---|---|
| `global π-divisibility of the generalized equation` | `1-4` | `checked` |
| `rootwise π-divisibility of linear factors` | `5-8` | `checked` |
| `integral quotient packaging` | `9-12` | `checked` |
| `residue-class injectivity` | `13-15` | `checked` |
| `residue-class bijection` | `16-18` | `checked` |

1. 进入 `K = Q(ζ)` 与其整数环 `O_K`，固定 `π = ζ - 1` 作为唯一 ramified prime direction 的生成元。
2. 用 `p = unit * π^(p-1)` 这条 cyclotomic ramification 事实，把整数层的 `p | z` 解释成 `O_K` 中沿 `π` 方向的整除信息。
3. 说明仅用原始方程 `x^p + y^p = z^p` 不能形成封闭的下降 statement，因为每一步都会引入单位与 `π`-幂次。
4. 因而把目标统一扩成 generalized equation family：`x^p + y^p = ε * π^(p*(m+1)) * z0^p`，并显式保留 `π ∤ y`、`π ∤ z0`。
5. 对 generalized equation 应用 cyclotomic factorization：`x^p + y^p = ∏_{η ∈ μ_p} (x + η y)`。
6. 在模 `π` 的意义下使用 `η ≡ 1`，把每个线性因子的剩余类统一改写成 `x + y` 的剩余类。
7. 由全局右边含有显式 `π`-幂次，推出 `x + y ≡ 0 (mod π)`，从而得到每个 `x + η y` 都被 `π` 整除。
8. 把上一步整理成 factorwise 的 `π`-divisibility statement，为后续对每个 root 单独取商做准备。
9. 对每个 root 考虑“除以一个 `π` 之后的 quotient”，并指出这不是形式除法，而必须验证整性。
10. 用 `div_one_sub_zeta_mem`-型引理证明与 `(1-η)/(1-ζ)` 同型的 normalized quotient 仍属于 `O_K`。
11. 于是每个 root 的线性因子都能在整数环内部写成 `π * (integral quotient)` 的形式。
12. 这就完成了 `integral quotient packaging`：后续 ideal / residue 运算都可以对这些 quotient 本身进行，而不必再回到分式表达。
13. 固定归一化 residue 数据 `((η - 1) / (ζ - 1)) mod π`，把不同 root 的差异转成可比较的模 `π` 信息。
14. 证明若 `η ≠ η'`，则对应归一化 residue class 也不同；这就是 `residue-class injectivity`。
15. 因而去掉公共 `π` 以后，不同 root 的 quotient 不会在 mod-`π` 世界里塌缩成同一个方向。
16. 进一步证明这些归一化 residue class 恰好跑遍所需的非零 residue classes。
17. 这给出 `residue-class bijection`，说明 root 参数与局部 residue 参数之间没有缺口。
18. 至此，Case II 已从“整数里有 `p`-divisibility 的原始方程”完全翻译成“分圆域里带单位、带 `π`-幂次、带可区分 quotient 的 generalized equation family”，恰好停在下一单元 `Case II ideal-factor layer` 的入口。

### `FLT-HR-015` `regular primes / Case II ideal-factor layer`

Scope boundary: this unit is limited to the canonical package `Case II ideal-factor layer`; it does not prove the distinguished-root layer, descent core, close/merge, or repo-local vendored theorem closure.

#### Human-Readable Expansion
##### 1. 本 unit 的位置与输入

本 unit 处在 `Case II π-language` 之后、`Case II distinguished root` 之前。
上一 unit 已把整数层的 `p`-整除改写进分圆域的 `π = ζ - 1` 语言，
得到 generalized Case II 方程
`x^p + y^p = ε * (π^(m+1) z)^p`
以及每个线性因子
`L_η := (x + η y)`
至少都含有一份 ramified ideal `𝔭 = (π)`。

这一 unit 不负责选出 distinguished root `η₀`；
它只做更基础的一件事：
把“全部 `L_η` 的乘积是一个整体 `p` 次幂”转成
“每个 residual ideal `𝔠_η` 本身都是 ideal-level 的 `p` 次幂”。

##### 2. `𝔠 η residual-ideal extraction` 与 `𝔷 = 𝔪 * 𝔷' normalization`

记 `𝔷 := (z)` 为 `z` 生成的 ideal。
这一层先抽出两类“所有根都共有”的部分：

1. ramified 的公共一阶部分 `𝔭 = (π)`；
2. 由公共 gcd 型数据打包出来的公共 ideal `𝔪`。

把它们从每个线性因子里剥离后，定义 residual ideals `𝔠_η`，使
`L_η = 𝔪 * 𝔠_η * 𝔭`。

与此同时，把右侧的 `z`-ideal 也做对应的公共因子规整：
`𝔷 = 𝔪 * 𝔷'`。

这一改写的作用很直接：
`𝔪` 记录“不同根之间真正共享的部分”，
`𝔠_η` 记录“属于根 `η` 自己的部分”，
而 `𝔷'` 则是 `z` 一侧在剥离共享部分后的剩余 ideal。

审计表把这一步拆成
`𝔠 η residual-ideal extraction`
与
`𝔷 = 𝔪 * 𝔷' normalization`，
其中右侧正规化在 formal hook 上由 `exists_ideal_pow_eq_c_aux` 先行完成。

##### 3. `residual pairwise coprimality`

抽出公共 `𝔪` 与统一的一次 `𝔭` 之后，
剩余的 `𝔠_η` 必须两两互素。
人类可读的原因是：

- 如果某个素 ideal 同时整除 `𝔠_η` 与 `𝔠_θ`，
  那么把公共部分 `𝔪` 与 `𝔭` 乘回去，
  它就会同时整除两个不同的线性因子 `L_η` 与 `L_θ`；
- 但上一 unit 已经把不同根之间的公共因子控制到 `π`-language 可见的公共部分里；
- 既然这部分已经统一剥离，
  剩下的 `𝔠_η` 与 `𝔠_θ` 就不能再共享新的素 ideal。

这一步是后面从“乘积是 `p` 次幂”推到“每个因子都是 `p` 次幂”的关键，
因为没有 pairwise coprimality，就不能做逐因子抽取。

##### 4. `prod_c`: 从全局乘积到统一的 `p` 次幂公式

把所有根上的分解
`L_η = 𝔪 * 𝔠_η * 𝔭`
相乘，并与 generalized equation 右侧的 ideal 分解相比较。

左侧给出
`∏η L_η = 𝔪^p * (∏η 𝔠_η) * 𝔭^p`。

右侧则由
`x^p + y^p = ε * (π^(m+1) z)^p`
和
`𝔷 = 𝔪 * 𝔷'`
整理成
`∏η L_η = (𝔪 * 𝔷' * 𝔭^(m+1))^p`。

于是把左右两边共有的 `𝔪^p` 与那一层统一抽出的 `𝔭^p` 消去，
得到本 unit 的核心全局公式
`∏η 𝔠_η = (𝔷' * 𝔭^m)^p`。

这正是审计里
`prod_c / common-factor cancellation`
之后留下来的 canonical 目标：
剩余 product 已经是一个显式的 `p` 次幂 ideal。

这一层只说明“全部 `𝔠_η` 的乘积”是 `p` 次幂；
它还没有说明每个 `𝔠_η` individually 是 `p` 次幂。
从全局到局部，还差一次 pairwise-coprime extraction。

##### 5. `exists_ideal_pow_eq_c`: 从全局 `p` 次幂到每个 `𝔠_η` 的局部 `p` 次幂

有两条输入同时成立：

1. `∏η 𝔠_η = (𝔷' * 𝔭^m)^p`；
2. family `(𝔠_η)_η` 两两互素。

于是可以直接应用审计里点名的工具
`Finset.exists_eq_pow_of_mul_eq_pow_of_coprime`，
把一个“pairwise coprime ideals 的乘积是 `p` 次幂”的事实逐因子拆开。

结论是：对每个根 `η`，都存在 ideal `𝔞_η`，使
`(𝔞_η)^p = 𝔠_η`。

这一步才是真正的
`global product to local p-th powers`：
`p` 次幂信息不再留在整个乘积上，
而是被分配到每个 rootwise residual ideal 上。

到这里，这个 unit 的主任务已经完成。
后续 `Case II distinguished root`
不再需要重新做全局乘积分析，
只需研究这些已经局部 `p` 次幂化的 `𝔠_η` 中，
哪一个吸收了额外的 `𝔭^(m*p)`。

##### 6. `principal quotient bridge`: 为什么还要记录 `root_div_zeta_sub_one_dvd_gcd_spec` 与 `c_div_principal`

这一 unit 末尾还要把“局部 `p` 次幂 ideal”转换成下一 unit 能直接消费的 quotient witness。
原因是：后面的下降不是只看 `𝔠_η = (𝔞_η)^p` 这条裸等式，
还要比较不同根对应的 ideal，
进而把差值 `η - θ` 里的一次 `π`-divisibility
翻译成某个 quotient / fractional-ideal 的 principal 见证。

从人类角度看，逻辑是：

- 两个线性因子 `x + η y` 与 `x + θ y` 的差等于 `y(η - θ)`；
- 对不同根，`η - θ` 是 `π` 的 unit 倍；
- 因此前面由 gcd / divisibility 打包出的 witness
  可以控制相应 residual ideals 之间的 quotient；
- `root_div_zeta_sub_one_dvd_gcd_spec` 负责把这个 witness 正式封装出来；
- `c_div_principal` 再把“某个 quotient 被该 witness 控制”
  转成“该 quotient 是 principal fractional ideal”的结论。

审计表把这块叫做 `principal quotient bridge` 是准确的：
它不是重复做一次 principalization，
而是把已经得到的
`𝔠_η = (𝔞_η)^p`
接到下一层“比较不同根并锁定 distinguished root”的局部控制上。

##### 7. 本 unit 的输出接口

完成这一层后，可以把后续调用的输入压缩成三句话：

1. 对每个根 `η`，都有 residual ideal `𝔠_η`，并且 `L_η = 𝔪 * 𝔠_η * 𝔭`。
2. 它们满足全局公式 `∏η 𝔠_η = (𝔷' * 𝔭^m)^p`，且彼此两两互素。
3. 因而存在 `𝔞_η` 使 `(𝔞_η)^p = 𝔠_η`，并且不同根之间的 quotient principal witness 已被打包好。

这正好对应 canonical package `Case II ideal-factor layer`
里的五个 reader-facing subitems：

- `𝔠 η residual-ideal extraction`
- `residual pairwise coprimality`
- `𝔷 = 𝔪 * 𝔷' normalization`
- `global product to local p-th powers`
- `principal quotient bridge`

其中真正关闭 canonical high-risk leaf
`Case II ideal-factor layer / global product to local p-th powers`
的是第 4 节与第 5 节的组合：
先把乘积整理成显式 `p` 次幂，
再用 pairwise coprimality 逐根抽出 `(𝔞_η)^p = 𝔠_η`。

#### Local Budget Ledger
##### Budget Summary

- Canonical unit: `Case II ideal-factor layer / global product to local p-th powers`
- Formal hooks: `prod_c`, `exists_ideal_pow_eq_c`, `root_div_zeta_sub_one_dvd_gcd_spec`, `c_div_principal`
- Total local proof steps: `25`
- Budget status: `checked`
- Completion condition: satisfied (`25 <= 100`)

| subitem | step range | status |
|---|---|---|
| `exists_ideal_pow_eq_c_aux / RHS normalization` | `1-4` | `checked` |
| `prod_c / cyclotomic product expansion` | `5-8` | `checked` |
| `prod_c / factorwise 𝔪·𝔠η·𝔭 substitution` | `9-12` | `checked` |
| `prod_c / common-factor cancellation` | `13-15` | `checked` |
| `exists_ideal_pow_eq_c / pairwise-coprime local extraction` | `16-21` | `checked` |
| `root_div_zeta_sub_one_dvd_gcd / witness packaging` | `22-25` | `checked` |

##### Step Ledger

1. 固定上一 unit 给出的 generalized Case II 方程、`π = ζ - 1`、`𝔭 = (π)`，以及各线性因子 ideal `L_η := (x + η y)`。
2. 记 `𝔷 := (z)`，把右侧 `z` 生成的 ideal 纳入统一记号。
3. 抽出所有根都共有的 gcd 型公共 ideal `𝔪`，并引入 `𝔷'` 使 `𝔷 = 𝔪 * 𝔷'`。
4. 把右侧整理成适合比较的 `p` 次幂形式；这一步对应 `exists_ideal_pow_eq_c_aux / RHS normalization`。
5. 从 cyclotomic factorization 写出 `∏η L_η` 的 ideal-level 乘积。
6. 把 generalized equation 右侧的 `π^(m+1)` 与 `z` 一侧一起改写进该乘积公式。
7. 把左侧 product 与右侧 overall `p`-th-power ideal 放到同一个等式里比较。
8. 记录这就是 `prod_c / cyclotomic product expansion` 的全局起点。
9. 对每个 `η`，利用前一层已经得到的一次 `π`-divisibility，把 `L_η` 写成 `𝔪 * 𝔠_η * 𝔭`。
10. 把 `𝔠_η` 解释为除去统一公共部分后的 rootwise residual ideal。
11. 把这类分解同时代入所有根上的乘积。
12. 这一步完成 `prod_c / factorwise 𝔪·𝔠η·𝔭 substitution`。
13. 把左侧出现的 `𝔪^p` 与统一的一层 `𝔭^p` 从两边同时消去。
14. 用 `𝔷 = 𝔪 * 𝔷'` 把右侧剩余部分收束成 `(𝔷' * 𝔭^m)^p`。
15. 得到核心公式 `∏η 𝔠_η = (𝔷' * 𝔭^m)^p`；这一步完成 `prod_c / common-factor cancellation`。
16. 调用 residual pairwise coprimality：不同 `η` 的 `𝔠_η` 两两互素。
17. 观察右侧已经是显式的 `p` 次幂 ideal。
18. 把第 16 步与第 17 步一起喂给 `Finset.exists_eq_pow_of_mul_eq_pow_of_coprime`。
19. 对每个根 `η` 抽出 ideal `𝔞_η`，满足 `(𝔞_η)^p = 𝔠_η`。
20. 统一整理这些 witness，使它们成为整个根族上的 local data。
21. 这一步完成 `exists_ideal_pow_eq_c / pairwise-coprime local extraction`，也即 canonical leaf `global product to local p-th powers` 的主闭包。
22. 取两个不同根对应的线性因子，比较它们的差 `y(η - θ)`。
23. 用 `η - θ = unit * π` 的 root-difference 结构，把相应 gcd / divisibility witness 打包成 quotient 控制语句。
24. 把该 witness 转写成需要的 principal fractional-ideal 结论。
25. 将这一包装记录为 `root_div_zeta_sub_one_dvd_gcd_spec` / `c_div_principal` 的 bridge 输出，交给下一 unit 的 distinguished-root 局部控制。

### `FLT-HR-016` `regular primes / Case II distinguished root`

Scope boundary: this unit is limited to the canonical package `Case II distinguished root`; it does not prove the raw descent core, close/merge, or repo-local vendored theorem closure.

#### Human-Readable Expansion
本 unit 站在前一单元 `Case II ideal-factor layer` 的输出之上。
在那里已经得到两组本地对象：

- residual ideals `𝔠 η`，满足全局乘积公式
  `∏_η 𝔠 η = (𝔷' * 𝔭^m)^p`
- local `p` 次幂 root ideals `𝔞 η`，满足
  `(𝔞 η)^p = 𝔠 η`

这里 `𝔭` 是 `π = ζ - 1` 上方的唯一 ramified 素理想；
每个线性因子 `(x + ηy)` 都已经先抽走了一份“普遍存在的一次 `𝔭`”，
而本 unit 的任务是说明：

> 除了一个被唯一选中的 root `η₀` 之外，
> 其余 residual factor `𝔠 η` 都看不见任何额外的 `𝔭`；
> 因而全局右端显式出现的 `𝔭^(m*p)` 只能全部压到 `𝔠 η₀`，
> 再进一步转移成 `𝔞 η₀` 上的 `𝔭^m`。

这就是 canonical high-risk leaf
`Case II distinguished root / p_pow_dvd_c_eta_zero`
的本地数学含义。

##### 1. `η₀` 不是任意标签，而是由局部同余唯一选出的根

上一单元已经把 Case II 改写进 `π = ζ - 1` 的语言，并且保留了 `π ∤ y`。
因此在 `O_K / 𝔭` 里，
线性因子条件
`x + ηy ≡ 0`
可以唯一地解出一个 residue class 的 `η`。
再借前面已经建立好的 residue-class bijection，
这个 residue class 在全部 `p` 次单位根里对应唯一的实际 root，
记为 `η₀`。

所以 `η₀` 的角色不是“任选一个方便的根”，
而是“唯一可能承受额外 ramification 的根”。
这一步就是 package 表中的
`zeta_sub_one_dvd_root selection`。

##### 2. `p_dvd_c_iff` 把“额外 `𝔭`”精确锁到 `η₀`

对每个 root `η`，
`𝔠 η` 表示在 `(x + ηy)` 中抽去公共部分以后剩下的 residual ideal。
本 unit 的核心局部判别是：

> `𝔭 ∣ 𝔠 η` 当且仅当 `η = η₀`。

这就是 `p_dvd_c_iff` 的数学作用。
它告诉我们：

- `η = η₀` 时，`𝔠 η₀` 允许继续看到额外的 `𝔭`
- `η ≠ η₀` 时，`𝔠 η` 与 `𝔭` 局部互素

因此 distinguished root 的意义已经不是抽象命名，
而是一个真正的 local divisibility criterion。

##### 3. off-root 因子整体上与 `𝔭^(m*p)` 互素

一旦知道所有 `η ≠ η₀` 的 `𝔠 η` 都不被 `𝔭` 整除，
就可以把这种 factorwise 的“看不见 `𝔭`”升级为乘积级别的结论。
也就是说，

`∏_{η ≠ η₀} 𝔠 η`

与 `𝔭` 互素，
于是也与任意幂 `𝔭^(m*p)` 互素。
这正是 `p_pow_dvd_c_eta_zero_aux` 及其后续
`gcd-product pivot`
真正打包的内容：

> off-root product 不会吸收任何一部分可见的 `𝔭^(m*p)`。

这一点很关键，
因为后面全局乘积公式右侧明明写着一个显式的 `𝔭^(m*p)`；
若不先把 off-root product 从局部上清空，
就无法断言这些 `𝔭` 的幂到底落在哪一边。

##### 4. 全部显式 `𝔭^(m*p)` 都被压到 `𝔠 η₀`

回到上一单元给出的全局公式：

`𝔠 η₀ * ∏_{η ≠ η₀} 𝔠 η = ∏_η 𝔠 η = (𝔷' * 𝔭^m)^p`

而 `𝔷'` 的 normalization 已保证它与 `𝔭` 互素，
所以右边唯一“肉眼可见”的 `𝔭`-部分就是
`𝔭^(m*p)`。

由于第三步已经说明 off-root product 和 `𝔭^(m*p)` 互素，
右侧的这全部 `𝔭^(m*p)` 就不可能分散在其他因子里，
只能全部集中进 distinguished factor `𝔠 η₀`。
于是得到：

`𝔭^(m*p) ∣ 𝔠 η₀`

这就是 `p_pow_dvd_c_eta_zero`。

这一步给出的不是 `𝔠 η₀` 的完整结构，
而是下降真正需要的那部分 lower bound：
distinguished factor 至少包含足够多的 `𝔭`。

##### 5. 从 `𝔠 η₀` 再转移到 `𝔞 η₀`

descent core 下一步不会直接拿 `𝔠 η₀` 做 principalization，
而是要回到前一单元抽出的 `p` 次幂根 `𝔞 η₀`。
因此本 unit 还要完成最后一个局部传递：

- 由 `(𝔞 η)^p = 𝔠 η`
- 配合 `p_dvd_a_iff`
- 把 distinguished-root 的判别从 `𝔠` 层搬到 `𝔞` 层

于是从
`𝔭^(m*p) ∣ 𝔠 η₀ = (𝔞 η₀)^p`
得到

`𝔭^m ∣ 𝔞 η₀`

这就是 `p_pow_dvd_a_eta_zero`。

从 proof-flow 的角度看，
这一步的价值在于把“全部额外 ramification 集中在 `η₀`”
改写成“`η₀` 对应的 `p` 次幂根 ideal 已经显式带出 `𝔭^m`”，
这样下一单元就能直接围绕 `η₀` 做 ideal split、quotient principalization、
以及后面的元素级下降构造。

##### 6. 本 unit 的闭合输出

因此，`Case II distinguished root` 在局部上完成了四件事：

1. 选出唯一的 distinguished root `η₀`
2. 证明 off-root 的 residual factors 与 `𝔭` 全部互素
3. 由全局乘积公式推出 `𝔭^(m*p)` 全部集中在 `𝔠 η₀`
4. 再把这份集中性传给 `𝔞 η₀`

这就解释了为什么 process audit 会把本 package 的作用概括为：

> 先用 `p_dvd_c_iff` 排除所有 off-root 的 `𝔭`-整除，
> 再把它升级成
> `gcd (𝔭^(m*p), ∏_{η ≠ η₀} 𝔠 η) = 1`，
> 最后借 `prod_c` 把全部 `𝔭^(m*p)` 压到 `𝔠 η₀`。

而这份局部控制正是 descent core 的直接输入。

#### Local Budget Ledger
本 unit 的独立 ledger 总计 `20` 步，满足 `<=100` 约束。

##### Package-level ledger

| subitem | step range | status |
|---|---|---|
| `zeta_sub_one_dvd_root_spec distinguished-root selection` | `1-3` | `checked` |
| `p_dvd_c_iff local divisibility criterion` | `4-6` | `checked` |
| `p_pow_dvd_c_eta_zero_aux off-root coprimality` | `7-9` | `checked` |
| `p_pow_dvd_c_eta_zero concentration on the distinguished 𝔠 η₀` | `10-16` | `checked` |
| `p_dvd_a_iff / p_pow_dvd_a_eta_zero transfer from 𝔠 to 𝔞` | `17-20` | `checked` |

##### Descendant high-risk leaf carried by the same ledger

其中 steps `1-16` 同时关闭 canonical high-risk leaf
`Case II distinguished root / p_pow_dvd_c_eta_zero`；
它在本 ledger 中的局部拆分如下。

| leaf-local chunk | step range | status |
|---|---|---|
| `η₀ divisibility criterion import` | `1-6` | `checked` |
| `off-root product coprimality` | `7-9` | `checked` |
| `gcd-product pivot` | `10-11` | `checked` |
| `distinguished factor reinsertion into total product` | `12-13` | `checked` |
| `visible 𝔭^(m*p) extraction from global p-th power` | `14-16` | `checked` |

##### Step-by-step ledger

1. 从上一单元导入 `π ∤ y` 与 residue-class bijection：单位根 `η` 的模 `𝔭` residue class 可以被唯一追踪。
2. 在 `O_K / 𝔭` 中解局部同余 `x + ηy ≡ 0`，得到唯一候选 residue class。
3. 用 `zeta_sub_one_dvd_root_spec` 把这个唯一 residue class 提升成真正的 distinguished root `η₀`。
4. 对任意 root `η`，把“抽走基线那一份 `𝔭` 后是否还剩额外 `𝔭`”改写成 ideal 语言 `𝔭 ∣ 𝔠 η`。
5. 调用 `p_dvd_c_iff`，得到 `𝔭 ∣ 𝔠 η ↔ η = η₀`。
6. 因而所有 `η ≠ η₀` 的 off-root residual ideals 都满足 `𝔭 ∤ 𝔠 η`；额外 ramification 只可能留在 `𝔠 η₀`。
7. 把 step 6 的结论逐个因子地改写成 `𝔭` 与每个 off-root `𝔠 η` 的互素关系。
8. 将这些 factorwise 互素结论乘起来，得到 `∏_{η ≠ η₀} 𝔠 η` 仍与 `𝔭` 互素。
9. 这正是 `p_pow_dvd_c_eta_zero_aux` 的局部意义：off-root product 完整地看不见额外 `𝔭`。
10. 由 step 9 立即升级得到 `gcd (𝔭^(m*p), ∏_{η ≠ η₀} 𝔠 η) = 1`。
11. 于是任何显式出现的 `𝔭^(m*p)` 都不可能由 off-root product 吸收；这是整个 leaf 的 `gcd-product pivot`。
12. 把 distinguished factor 重新插回全局等式，写成
    `𝔠 η₀ * ∏_{η ≠ η₀} 𝔠 η = ∏_η 𝔠 η`。
13. 再用上一单元的 `prod_c` 结论把右侧改写成 `(𝔷' * 𝔭^m)^p`。
14. 展开右侧可见的 `𝔭`-部分，得到 `(𝔷')^p * 𝔭^(m*p)`；同时 `𝔷'` 的 normalization 保证它与 `𝔭` 互素。
15. 结合 step 10，右侧全部可见的 `𝔭^(m*p)` 只能落在左侧尚未排除的唯一因子 `𝔠 η₀`。
16. 因而推出 `𝔭^(m*p) ∣ 𝔠 η₀`；这就是 `p_pow_dvd_c_eta_zero`。
17. 回忆前一单元已经构造出 `(𝔞 η)^p = 𝔠 η`，所以 `𝔠 η₀` 是某个 local root ideal 的 `p` 次幂。
18. 用 `p_dvd_a_iff` 把 distinguished-root 的局部整除判别从 `𝔠` 层转移到 `𝔞` 层。
19. 由 step 16 与 step 17 把 `p` 次幂整除关系开根，得到 `𝔭^m ∣ 𝔞 η₀`；这就是 `p_pow_dvd_a_eta_zero`。
20. 至此，本 unit 为下一单元留下干净输入：全部额外 `𝔭`-贡献都集中在 `η₀`，并且已经在 `𝔞 η₀` 层显式可见。

### `FLT-HR-017` `regular primes / Case II descent core`

Scope boundary: this unit is limited to the canonical package `Case II descent core`; it packages the raw descent interface and does not prove the final minimal-`m` close/merge or repo-local vendored theorem closure.

#### Human-Readable Expansion
##### 1. 本 unit 的输入 / 输出接口

这一单元不重新建立 Case II 的整个环境，而是把前面三层已经获得的数据接过来：

1. 已经在 `π = ζ - 1` 的语言中工作。
2. 已经有 residual ideal 记号 `𝔠 η`，并且每个 `𝔠 η` 都已被写成某个 ideal 的 `p` 次幂。
3. 已经选定 distinguished root `η₀`，并把所有可见的 ramified `𝔭`-幂都压到了 `𝔠 η₀` 上。

因此本 unit 的真正输入是一个 `level m+1` 的 generalized Case II 解，形状可以读成：

```text
x^p + y^p = ε * (π^(m+1) z)^p,
π ∤ y,   π ∤ z.
```

这里的 `m` 不是额外装饰，而是整个无限递降真正下降的参数。

本 unit 的输出则不是“已经矛盾”，而只是：

```text
若 level m+1 有解，则 level m 也有同型解。
```

这正是 `exists_solution` / `exists_solution'` 在 process audit 里被标成
`Case II descent core` 的原因；最小 `m` 的矛盾留给下一单元
`Case II close / merge`。

##### 2. `η₀-ideal split` 到 `α/β representative extraction`

这一段的目标，是把上一单元停留在 ideal-level 的数据，压缩成足够具体的 element-level 代表元。

先看 distinguished root `η₀`。上一单元已经证明：

- off-root 分支对 `𝔭` 没有额外贡献；
- 所有可见的 `𝔭^(m*p)` 都集中在 `𝔠 η₀` 上。

所以在 descent core 的起点，`η₀` 分支被拆成：

```text
𝔠 η₀ = 𝔭^(m*p) * 𝔡
```

其中 `𝔡` 与 `𝔭` 互素。这个 split 的作用非常局部，但非常关键：
它把“哪个地方真正记录了参数 `m`”这件事隔离出来。此后任何真正的参数下降，
都必须体现为把这份 `𝔭`-贡献从 `m+1` 变成 `m`，而不是在别处分散地丢信息。

接着要做 `quotient principalization`。前一单元虽然已经把每个 `𝔠 η`
控制成 `p` 次幂 ideal，却还没有把 descent 需要的 quotient 真正拉回到元素层。
因此这里要把 `η₀` 支路及其 orbit 支路上的 quotient ideals principalize：

- 不是重新证明“regularity 蕴含 principalization engine”；
- 而是在已经建好的 engine 上，针对 descent 里真正出现的 quotient 局部调用一次。

这一步完成后，就可以选取生成元。canonical wording 用的是
`α/β representative extraction`，它表达的不是“只会出现两个根”，而是：

- 三根 orbit 中真正自由的生成元只需抓住两份；
- 第三份由 orbit 关系与共轭 / 比值关系回收；
- 因而人类可读层只把这份数据压缩记成 `α` / `β` 代表元。

这一步的输出不是最终方程，而是一组 element witnesses，
它们与前面的 ideals 对应，但只差一些单位。

##### 3. `ideal-to-element balance around η₀`

把 ideals 换成生成元以后，马上会遇到一个标准但不能跳过的事实：

> principal ideal 的生成元并不唯一，只唯一到单位。

所以从 ideal 等式转成 element 等式时，不可避免会出现若干单位。
descent core 不把这一层略去，而是显式保留它：

- `η₀` 支路上保留 `π^(m*p)` 的可见贡献；
- 其余 `p` 次幂部分都吸收到 `α`、`β` 与其 orbit mates；
- 所有“生成元不唯一”的误差统一收集成后面要处理的 `u1`、`u2`。

这就是 canonical 子节点 `ideal-to-element balance around η₀` 的准确含义：
它不是又一次 principalization，而是把“ideal-level 正确”平衡成
“element-level 正确，但带单位误差”的过渡层。

##### 4. `three-root formula and raw descent`

这是本 unit 的高风险叶子，也是用户指定的中心。

###### 4.1 为什么只取三根

这里并不需要所有 `p` 个根一起显式参与消元，而只取一个闭合 orbit：

```text
η₀,   η₀ζ,   η₀ζ².
```

原因是：

1. 它包含 distinguished root `η₀`；
2. 它在乘以 `ζ` 的操作下闭合；
3. 它已经足以制造需要的差分恒等式；
4. 它让 ramified `π` 的出现变成可精确计数，而不是在全体根里摊平。

这正对应 canonical leaf 的第一项 `three-root orbit selection`。

###### 4.2 root difference 为什么统一是 `unit · π`

三根之间的差分都落到同一个模板里：

```text
η₀ζ - η₀      = unit * (ζ - 1)
η₀ζ² - η₀ζ    = unit * (ζ - 1)
η₀ - η₀ζ²     = unit * (ζ - 1).
```

也就是每条 root difference 都是 `unit · π`。

这一步的意义不只是“算出来一个公式”，而是告诉你：

- 三根消元过程中出现的所有差分，`π`-adic 尺度完全统一；
- 不会有某条差分偷偷多带一个 `π`，也不会有某条差分完全不带 `π`；
- 因为还保留着 `π ∤ y` 的归一条件，所以这些 `π` 因子是真正可控的，
  不会被 `y` 的额外整除重新污染。

这正对应 canonical leaf 的第二项 `root-difference as unit·π`。

###### 4.3 三根公式到底做了什么

把上一步的差分表达式代回三根 orbit 的 element-level 平衡式，
再用 upstream 里的 `formula`-type identity 统一消元，
会得到一个“只剩下降变量”的新等式。

这里最容易误解的一点是：

> 三条差分都各带一个 `π`，并不意味着参数会一次掉三层。

原因在于 three-root formula 不是把三条差分机械相乘，
而是在 orbit 对称、分子分母配平与 `p` 次幂部分约掉以后，
净效果只留下“一层真正可见的 `π`-下降”。

所以原来是 `level m+1` 的数据，消元后只会变成 `level m`，
这正是想要的参数 drop：

```text
u1 * x'^p + y'^p = u2 * (π^m z')^p.
```

这里的 `parameter drop` 必须按字面理解成“恰好少一层 `π`”，
而不是模糊地说“某个 valuation 下降了”。输入端显式可见的是
`(π^(m+1) z)^p`，three-root cancellation 之后保留下来的规范形则是
`(π^m z')^p`；因此这一单元真正交给下一单元的，是一个已经被标准化成
`m+1 -> m` 的单层下降接口，而不是需要再猜测下降幅度的半成品。

这里的 `x'`、`y'`、`z'` 还只是 raw descended witnesses，
因此审计表把这一步叫作 `three-root formula and raw descent`。

对应 canonical leaf 的后三项分别是：

- `three-root cancellation identity`
- `raw descended triple packaging`
- `raw nondivisibility certification`

其中最后一项也很重要：若不能继续保证 `π ∤ y'`、`π ∤ z'`，
那么新方程就不再落在同一个 generalized Case II family 里，
后续最小 `m` 论证就无法接上。

##### 5. `Kummer normalization`

经过 raw descent 后，障碍已经不再是 ideal，也不再是 `η₀` 的局部 ramification，
而是单位。

具体说，下降后的方程带着 `u1`、`u2` 这类单位：

```text
u1 * x'^p + y'^p = u2 * (π^m z')^p.
```

如果停在这里，方程虽然“长得像”原方程，却还没有真正回到同一个封闭类，
因为左边多了一个讨厌的单位因子。

Kummer lemma 在这里承担的角色很窄，但不可替代：

1. 先证明这个坏单位在模 `p` 意义下同余于一个整数；
2. odd regular prime 的 Kummer 引理断言，这样的单位其实是 `p` 次幂单位；
3. 因而它可以被吸收到 `x'^p` 里；
4. 右边若还残留单位，也可做同样的归一；
5. 最终得到与原始 generalized Case II 方程同型的 level-`m` 解。

所以本 unit 的真正结论不是“已经没有解”，而是：

> `Case II descent core` 把 `m+1` 级解正规化地送到 `m` 级解，
> 并且在送下去的过程中没有丢失 `π ∤ y`、`π ∤ z` 这类闭包条件。

这就是 `exists_solution` / `exists_solution'` 在局部人类可读层上的准确职责。

#### Local Budget Ledger
##### Budget Summary

本 unit 的局部 ledger 总计 `35` 步，满足独立 `<=100` 步约束。

| canonical item | step range | status |
|---|---:|---|
| `η₀-ideal split` | `1-5` | `checked` |
| `quotient principalization` | `6-10` | `checked` |
| `α/β representative extraction` | `11-14` | `checked` |
| `ideal-to-element balance around η₀` | `15-19` | `checked` |
| `three-root formula and raw descent` | `20-30` | `checked` |
| `Kummer normalization` | `31-35` | `checked` |

其中 canonical high-risk leaf
`Case II descent core / three-root formula and raw descent`
在本地账本里细分如下：

| high-risk leaf item | step range | status |
|---|---:|---|
| `three-root orbit selection` | `20-21` | `checked` |
| `root-difference as unit·π` | `22-23` | `checked` |
| `three-root cancellation identity` | `24-25` | `checked` |
| `raw descended triple packaging` | `26-28` | `checked` |
| `raw nondivisibility certification` | `29-30` | `checked` |

##### Step Ledger

1. 从 `level m+1` 的 generalized Case II 解出发，固定方程
   `x^p + y^p = ε * (π^(m+1) z)^p`，并保留 `π ∤ y`、`π ∤ z`。
2. 导入前一单元已经给出的 distinguished root `η₀`。
3. 导入 residual ideals `𝔠 η` 与它们的 `p` 次幂表示。
4. 导入 off-root 分支对 `𝔭` 的互素性，以及所有可见 `𝔭`-幂都集中在 `𝔠 η₀` 上。
5. 把 `η₀` 分支写成 `𝔠 η₀ = 𝔭^(m*p) * 𝔡`，其中 `𝔡` 与 `𝔭` 互素；参数 `m` 从此被局部锁定在这一步。
6. 对 distinguished branch 上真正进入下降公式的 quotient ideal 调用 principal quotient bridge。
7. 因为 quotient ideal 在 ideal 层已经表现为 `p` 次幂对象且与 ramified 部分互素，regularity 允许把它 principalize。
8. 对与 `η₀` 同 orbit 的配对 quotient ideals 做同样的 principalization。
9. 这样一来，下降里出现的关键 ideals 都可由具体元素生成，而不再只是抽象 ideal 类。
10. 因此后续的消元可以完全转到 element level，并继续显式跟踪 `m`。
11. 为 distinguished branch 的 quotient 选取生成元 `α`。
12. 为配对 branch 的 quotient 选取生成元 `β`。
13. 用 orbit 关系与共轭 / 比值关系恢复第三个所需代表元，而不引入新的独立自由度。
14. 于是 descent 所需的 ideal 数据被压缩成 `α/β`-type 代表元包。
15. 把 principal ideals 的等式翻译成生成元的等式。
16. 显式记下“生成元只唯一到单位”，所以 element-level 等式必然伴随单位误差。
17. 把这些单位误差统一收集成后续记号 `u1`、`u2`。
18. 保留 `η₀` 分支上的 `π^(m*p)` 可见贡献，并把其余 `p` 次幂部分吸收到 `α`、`β` 及其 orbit mates。
19. 得到围绕 `η₀` 的平衡 element identity；这一步正是 ideal-to-element balance 的完成点。
20. 选择 orbit `η₀`、`η₀ζ`、`η₀ζ²`。
21. 选择这组三根，是因为它既包含 distinguished root，又在乘以 `ζ` 下闭合，并且已经足够驱动下降公式。
22. 计算 root differences：`η₀ζ-η₀`、`η₀ζ²-η₀ζ`、`η₀-η₀ζ²` 全都等于某个单位乘 `π = ζ-1`。
23. 结合 `π ∤ y`，确认这些差分给出的 `π` 因子是受控的，不会被 `y` 的额外整除掩盖。
24. 把步骤 `11-19` 的 element representatives 代回三根 orbit 的平衡式。
25. 调用 `formula`-type 的三根消元恒等式，约掉辅助 orbit 项，只保留下降真正需要的主项。
26. 将约掉后的 `p` 次幂部分重新打包为 `x'`、`y'`、`z'`。
27. 得到 raw descended equation：
    `u1 * x'^p + y'^p = u2 * (π^m z')^p`。
28. 这一步就是从 `level m+1` 到 `level m` 的原始参数下降；下降后的对象仍是同一 generalized family 的候选 witness。
29. 检查 `π ∤ y'`。
30. 检查 `π ∤ z'`；因此 raw descended triple 不只是形式重写，而是合格的下一层解。
31. 现阶段唯一还阻止它回到 canonical family 的障碍，是单位 `u1`（以及同类的单位归一问题）。
32. 证明这个坏单位在模 `p` 的意义下同余于某个整数。
33. 对 odd regular prime 应用 Kummer lemma，推出该单位其实是 `p` 次幂单位。
34. 把这个 `p` 次幂单位吸收到 `x'^p` 中，并对右端单位做同型归一。
35. 于是 `exists_solution` / `exists_solution'` 完成 `level m+1 -> level m` 的标准化下降接口；最小 `m` 的矛盾留给下一单元。

### `FLT-HR-018` `regular primes / Case II close / merge`

Scope boundary: this unit is limited to the canonical package `Case II close / merge` and canonical high-risk leaf `Case II close / merge / not_exists_solution'`; it does not prove repo-local vendored theorem closure, which remains anchor-only.

#### Human-Readable Expansion

This final regular-primes unit does not reopen the ideal-factor or raw-descent
machinery.  Its job is to close the minimal-`m` contradiction produced by the
Case II descent family and then merge Case II with Case I at the theorem entry.

The named upstream hooks for this close-and-merge surface are:

- `not_exists_solution`
- `not_exists_solution'`
- `not_exists_Int_solution`
- `not_exists_Int_solution'`
- `caseII`
- `flt_regular`

The first two hooks live at the generalized cyclotomic level.  The theorem
`not_exists_solution` packages the minimal-`m` contradiction: if a smallest
level in the generalized Case II family existed, the descent core would produce
a strictly smaller level of the same family.  The theorem `not_exists_solution'`
is the normalized version used when the visible divisibility is expressed by
the `π`-adic condition on `z`; it records the same contradiction after the
normalization needed by the final Case II statement.

The next pair transports that contradiction back to the integer-level Case II
surface.  `not_exists_Int_solution` is the bridge from the cyclotomic
divisibility statement to an integer triple with `p ∣ abc`, while
`not_exists_Int_solution'` performs the primitive-gcd cleanup needed before the
ordinary FLT statement can use the contradiction.  These hooks are transport
and cleanup layers, not new descent engines.

The hook `caseII` is the public Case II close.  It handles the sign and
permutation normalization of a primitive integer counterexample in the branch
`p ∣ abc`, sends it through the integer transport hooks above, and concludes
that this branch has no primitive solution for an odd regular prime.

Finally, `flt_regular` is the theorem-level merge.  It combines the already
closed Case I branch (`p ∤ abc`) with `caseII` (`p ∣ abc`) and yields the
regular-primes theorem `FermatLastTheoremFor p`.  This is upstream theorem
closure only: the repo-local boundary remains anchor-only, with a recorded
statement/module/theorem-name anchor for `flt_regular`, and does not claim that
this repository vendors the upstream proof body.

This section therefore closes the canonical high-risk leaf
`Case II close / merge / not_exists_solution'`, using the canonical name fixed
by `Docs/Blueprint_Guidelines.md`; it does not introduce a second leaf naming
system.

#### Local Budget Ledger

Total local proof steps: `34`

| canonical item | step range | status |
|---|---:|---|
| `generalized-family minimal-m closure` | `1-8` | `checked` |
| `π-adic normalization of z` | `9-13` | `checked` |
| `integer transport` | `14-19` | `checked` |
| `primitive gcd cleanup` | `20-24` | `checked` |
| `caseII permutation close` | `25-29` | `checked` |
| `final merge` | `30-34` | `checked` |

The local ledger has `34` steps, so it satisfies the independent `<=100`
proof-step budget for `FLT-HR-018`.

1. Start with a hypothetical generalized Case II solution at some level `m`.
2. Choose `m` minimal among all levels admitting such a solution.
3. Import the descent-core interface `exists_solution` / `exists_solution'` from
   the preceding unit.
4. Apply that interface to the minimal witness whenever the level is positive.
5. Obtain a new generalized Case II witness at level `m-1`.
6. Check that the descent preserves the defining nondivisibility conditions of
   the generalized family.
7. Contradict the minimality of `m`.
8. Package this contradiction as `not_exists_solution`.
9. Normalize the Case II input so the visible ramification is expressed through
   the `π`-adic condition on `z`.
10. Extract the maximal visible `π`-power from `z`.
11. Reindex the normalized witness as a level-`m` generalized-family solution.
12. Apply the minimal-`m` contradiction to the normalized witness.
13. Package this normalized contradiction as `not_exists_solution'`.
14. Begin with an integer-level primitive Case II triple.
15. Move the triple into the cyclotomic equation used by the generalized family.
16. Translate integer divisibility by `p` into the corresponding `π`-adic
    divisibility statement.
17. Preserve the coprimality and nonzero hypotheses required by the cyclotomic
    hooks.
18. Apply `not_exists_solution` / `not_exists_solution'` to rule out the
    transported cyclotomic witness.
19. Record the integer-level contradiction as `not_exists_Int_solution`.
20. Recheck primitivity for the original integer triple.
21. Remove common-factor artifacts introduced by sign or permutation choices.
22. Reestablish the exact gcd hypotheses expected by the public Case II theorem.
23. Reapply the integer transport contradiction under these cleaned hypotheses.
24. Record the cleaned integer contradiction as `not_exists_Int_solution'`.
25. Split the primitive integer branch by whether `p ∣ abc`.
26. In the Case II branch, choose the permutation placing the divisible factor in
    the expected argument position.
27. Normalize signs so the upstream Case II hooks see the canonical triple.
28. Apply `not_exists_Int_solution'` to the normalized Case II triple.
29. Close the public Case II theorem as `caseII`.
30. At the regular-primes theorem entry, import the closed Case I theorem.
31. Import the closed Case II theorem `caseII`.
32. Split an arbitrary primitive counterexample into the branches `p ∤ abc` and
    `p ∣ abc`.
33. Contradict the first branch by Case I and the second branch by Case II.
34. Merge the two branches into `flt_regular : FermatLastTheoremFor p`.
<!-- HR18_REGULAR_MERGED_END -->
