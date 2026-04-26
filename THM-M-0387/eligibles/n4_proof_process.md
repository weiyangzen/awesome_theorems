# THM-M-0387 `n = 4` 证明过程展开稿

## 1. 目标

这里解释的是 `mathlib` 中 `fermatLastTheoremFour` 背后的证明过程。

本文件是 `FLT-HR-001` 到 `FLT-HR-007` 的唯一公开合并目标。
公开归档只指向本 tracked Markdown 主稿，不指向临时运行结果目录或自动化工作副本路径。

目标命题是：

> 不存在非零整数解满足 `a^4 + b^4 = c^4`。

在 formalization 里，实际先证明的是一个桥梁命题：

> 不存在非零整数解满足 `a^4 + b^4 = c^2`。

这就是 `Fermat42` 所编码的对象。

原因很简单：

- 如果 `a^4 + b^4 = c^4` 有非平凡解，
- 那么令 `C = c^2`，就得到 `a^4 + b^4 = C^2` 的非平凡解。

所以先排除 `a^4 + b^4 = c^2`，就自动排除了 `n = 4` 的 FLT。

## 2. 对应的 formal 入口

主要对象都在 `Mathlib/NumberTheory/FLT/Four.lean`：

- `Fermat42`
- `Fermat42.exists_minimal`
- `Fermat42.coprime_of_minimal`
- `Fermat42.exists_pos_odd_minimal`
- `Fermat42.not_minimal`
- `not_fermat_42`
- `fermatLastTheoremFour`

可以把它们理解成一条完整链：

1. 建桥
2. 取最小反例
3. 规范化
4. 两次勾股数组参数化
5. 构造更小反例
6. 矛盾
7. 回到原定理

## 3. 证明路线总览

这条证明的数学骨架，是经典的无限递降。

假设存在一个非平凡解：

`a^4 + b^4 = c^2`

那么就在所有解里选一个 `|c|` 最小的。

接着证明：

1. 这个最小解可以被规整成互素、正、并且 `a` 为奇数的形态。
2. 由方程
   `a^4 + b^4 = c^2`
   可把
   `(a^2, b^2, c)`
   看成 primitive Pythagorean triple。
3. 对这个 primitive triple 做一次标准参数化，得到新的参数 `m, n`。
4. 再由
   `a^2 = m^2 - n^2`
   把 `(a, n, m)` 看成第二个 primitive Pythagorean triple，
   再做一次参数化，得到新的参数 `r, s`。
5. 从
   `b^2 = 4 m r s`
   以及若干互素性结论推出：
   `m`、`r`、`s` 分别都是平方。
6. 于是构造出一个更小的解
   `j^4 + k^4 = i^2`。
7. 这和“原解的 `|c|` 最小”矛盾。

因此根本不存在起始反例。

## 4. 第一步：把问题转成最适合下降的桥梁方程

`Fermat42` 不是最终命题，而是最适合递降的版本：

`a ≠ 0 ∧ b ≠ 0 ∧ a^4 + b^4 = c^2`

它的优势在于：

- 左边两个四次方可以改写成两个平方的平方：
  `a^4 = (a^2)^2`, `b^4 = (b^2)^2`
- 因此整个方程天然进入勾股三元组框架：
  `(a^2)^2 + (b^2)^2 = c^2`

这就是为什么 formal proof 不是直接对 `a^4 + b^4 = c^4` 做递降，
而是先转成 `Fermat42`。

## 5. 第二步：取最小反例

`Fermat42.exists_minimal` 做的事情很标准：

- 假设某个解存在；
- 看所有解的 `|c|`；
- 因为这些值都是自然数，故存在最小的那个。

于是可以固定一个最小反例 `(a, b, c)`，满足：

- `a^4 + b^4 = c^2`
- `a ≠ 0`
- `b ≠ 0`
- 对任意其他解 `(a1, b1, c1)`，都有 `|c| ≤ |c1|`

这是整条递降证明的逻辑支点。

如果后面能从它造出一个更小的解，就立刻矛盾。

## 6. 第三步：最小反例的规范化

### 6.1 互素化

`Fermat42.coprime_of_minimal` 证明最小反例中的 `a` 与 `b` 必须互素。

理由是：

- 若 `a, b` 有共同素因子 `p`，
- 那么从方程
  `a^4 + b^4 = c^2`
  可以推出 `p^2 | c`，
- 进而把三者同时缩小，
- 得到一个更小的 `Fermat42` 解，
- 与最小性矛盾。

这一步把所有“纯粹来自公因子缩放”的伪复杂性剔除了。

### 6.2 奇偶规范化

`Fermat42.exists_odd_minimal` 和 `Fermat42.exists_pos_odd_minimal` 继续把解规整成：

- `a` 为奇数
- `c > 0`

这里做的不是新数学，而是为了让后面的 primitive Pythagorean triple 分类只剩一个标准分支。

这样一来，后面调用勾股数参数化定理时，奇偶和符号不会再分裂出多套并行讨论。

## 7. 第四步：第一次勾股数组参数化

由

`a^4 + b^4 = c^2`

可重写成

`(a^2)^2 + (b^2)^2 = c^2`

所以 `(a^2, b^2, c)` 是一个勾股三元组。

再利用：

- `a` 与 `b` 互素
- `a` 为奇数
- `c > 0`

可以调用 primitive Pythagorean triple 的标准分类，得到整数 `m, n`，使得：

- `a^2 = m^2 - n^2`
- `b^2 = 2mn`
- `c = m^2 + n^2`
- `m, n` 互素
- 奇偶性已经处于标准位置

这一步非常关键，因为它把原来四次方程中的结构拆成了“平方差”和“积”的结构。

尤其是

`b^2 = 2mn`

和

`a^2 = m^2 - n^2`

分别会在后面承担不同作用：

- 前者负责最终把多个因子判成平方；
- 后者负责导出第二个勾股三元组。

## 8. 第五步：第二次勾股数组参数化

由

`a^2 = m^2 - n^2`

可改写为

`a^2 + n^2 = m^2`

所以 `(a, n, m)` 又是一个勾股三元组。

formal proof 接着证明：

- `a` 与 `n` 互素；
- `a` 是奇数；
- `m > 0`。

于是再次调用 primitive Pythagorean triple 分类，得到 `r, s`，使得：

- `a = r^2 - s^2`
- `n = 2rs`
- `m = r^2 + s^2`

此处整个下降链已经被推进到了第二层参数。

这正是经典证明中“二次参数化”的核心。

## 9. 第六步：从 `b^2 = 4mrs` 推出每个因子都是平方

把前面两轮参数化合并：

- `b^2 = 2mn`
- `n = 2rs`

可得：

`b^2 = 4 m r s`

因此

`(b / 2)^2 = m r s`

如果再证明 `m`、`r`、`s` 两两互素，
那么“一个平方数分解成三个两两互素因子的乘积”，就意味着这三个因子必须分别都是平方。

formal proof 正是在这里花了很多工夫去建立：

- `m` 与 `rs` 互素
- `r` 与 `s` 互素
- 所以 `m`、`r`、`s` 两两互素

于是可写成：

- `m = i^2`
- `r = ± j^2`
- `s = ± k^2`

因为这里是整数环境，formal proof 先得到“平方或负平方”，然后再借助正性与非零性排除错误符号。

## 10. 第七步：构造更小反例

将

`m = r^2 + s^2`

代回：

`i^2 = j^4 + k^4`

于是 `(j, k, i)` 又给出了一个新的 `Fermat42` 解：

`j^4 + k^4 = i^2`

剩下只要证明：

`|i| < |c|`

就和最小性矛盾了。

formal proof 中这个不等式来自以下链条：

- `c = m^2 + n^2`
- 因为 `n ≠ 0`，所以 `m^2 < c`
- 而 `m = i^2`
- 因此 `i^2 < c`
- 再结合绝对值和平方的基本不等式，得到 `|i| < |c|`

这就是 `Fermat42.not_minimal` 的收束点。

## 11. 第八步：从桥梁命题回到 FLT(4)

一旦 `not_fermat_42` 说明

`a^4 + b^4 = c^2`

无非平凡整数解，那么原来的 `n = 4` 立刻得到：

- 若 `a^4 + b^4 = c^4`
- 就令 `C = c^2`
- 则 `a^4 + b^4 = C^2`
- 与 `not_fermat_42` 矛盾

于是 `fermatLastTheoremFour` 成立。

## 12. 这条证明的真正核心是什么

如果只看标题，很多人会把 `n = 4` 的证明理解成一句：

> 由勾股数分类做无限递降。

但从 formal proof 的角度看，这句话太粗了。

真正被 machine-check 的骨架是：

1. 明确引入桥梁方程 `a^4 + b^4 = c^2`
2. 明确构造最小反例
3. 明确证明最小反例互素
4. 明确做第一次 primitive triple 参数化
5. 明确做第二次 primitive triple 参数化
6. 明确证明几个乘积因子两两互素
7. 明确把“乘积是平方”拆成“各因子是平方”
8. 明确构造更小反例并比较大小

也就是说，它不是一句“用无限递降”，而是一条完整的下降制造流水线。

## 13. 与 formal theorem 的一一对应

| 数学步骤 | 对应 formal 对象 |
|---|---|
| 引入桥梁方程 | `Fermat42` |
| 取最小反例 | `Fermat42.exists_minimal` |
| 互素化 | `Fermat42.coprime_of_minimal` |
| 奇 + 正规范化 | `Fermat42.exists_pos_odd_minimal` |
| 两次参数化并构造更小反例 | `Fermat42.not_minimal` |
| 排除 `a^4 + b^4 = c^2` | `not_fermat_42` |
| 回到 FLT(4) | `fermatLastTheoremFour` |

## 14. 阅读建议

如果你只想把这条 proof 真正看懂，建议按这个顺序读：

1. 先读本稿。
2. 再回到 [`../process_audit.md`](../process_audit.md) 看过程总表。
3. 然后对照 `Four.lean` 里的 `Fermat42.not_minimal`。

因为 `not_minimal` 才是整条 `n = 4` 机器证明真正“做重活”的地方。

## 15. `n = 4` 定理树

下面把这条分支改写成一棵更适合继续拆分的定理树。

这条分支固定成 `7` 个 package。

```text
n = 4 branch
├── Root: FermatLastTheoremFor 4
├── Bridge layer
│   ├── FLT(4) → Fermat42
│   └── not_fermat_42 → fermatLastTheoremFour
├── Minimal-counterexample layer
│   ├── exists_minimal
│   ├── coprime_of_minimal
│   └── exists_pos_odd_minimal
├── First parametrization layer
│   ├── (a^2, b^2, c) is primitive Pythagorean triple
│   ├── a^2 = m^2 - n^2
│   ├── b^2 = 2mn
│   └── c = m^2 + n^2
├── Second parametrization layer
│   ├── (a, n, m) is primitive Pythagorean triple
│   ├── a = r^2 - s^2
│   ├── n = 2rs
│   └── m = r^2 + s^2
├── Square-factor layer
│   ├── b^2 = 4mrs
│   ├── m, r, s pairwise coprime
│   └── m, r, s are squares
└── Descent-closing layer
    ├── construct j^4 + k^4 = i^2
    ├── prove |i| < |c|
    └── contradict minimality
```

这棵树里真正需要继续做重工作的，是：

1. 两次 primitive Pythagorean triple 参数化之间的接口。
2. 从 `b^2 = 4mrs` 推到 `m, r, s` 各自为平方的那组互素性论证。
3. 最后比较 `|i| < |c|` 的收束链。

而像“互素”“整除”“奇偶”等初等数论背景动作，
这里只在它们决定 proof flow 时保留，不再拆成教学化小粒度叶子。

### 15.1 与机器节点包的对齐

为了保证 `machine_checked_audit`、`process_audit`、本稿三层口径一致，
下面把人类可读层和机器节点包直接对齐。

| 机器节点包 | 本稿中的可读层 | 说明 |
|---|---|---|
| bridge packaging | Bridge layer | `Fermat42` 与 `not_fermat_42` / `fermatLastTheoremFour` 的桥梁层 |
| minimal normalization | Minimal-counterexample layer | 最小反例、互素化、奇 + 正规范化 |
| first triple classification | First parametrization layer | 第一轮 primitive Pythagorean triple 参数化 |
| second triple classification | Second parametrization layer | 第二轮 primitive Pythagorean triple 参数化 |
| coprimality bridge | Square-factor layer 前半 | 从和平方结构过渡到因子互素 |
| square extraction and sign cleanup | Square-factor layer 后半 | 从平方乘积提取平方因子，并排除负平方分支 |
| smaller-solution construction and size comparison | Descent-closing layer | 构造更小解并证明其严格更小 |

上表右列名称只作为 reader-facing aliases（读者导向别名）使用；它们不创建第二套 canonical node system。
跨文件同步时仍以上表左列 canonical package 名为准。
本稿与 `machine_checked_audit.md`、`process_audit.md` 共用同一组 canonical package 名：
`bridge packaging`、`minimal normalization`、`first triple classification`、
`second triple classification`、`coprimality bridge`、
`square extraction and sign cleanup`、`smaller-solution construction and size comparison`。

### 15.1A `n = 4` human-readable closure note

`Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/FLT4Path.lean`
在本仓库共享源码树里直接导入 `fermatLastTheoremFour`，
因此 `n = 4` 这条 branch 的 theorem-level closure 是 repo-local 的。
在本稿覆盖的人类可读审计层级内，
canonical package、canonical high-risk leaf，
以及此前单列的 package-level subitem
都已完成独立 `<=100` proof-step ledger 整合。

### 15.2 每个 package 再拆一层

以下 package / `one-more-depth` 子包与 `machine_checked_audit.md`、`process_audit.md`
保持同名同步；这些展开项已拥有独立 `<=100` proof-step ledger，
因此下表统一记为 `checked`。

跨文件统一的 canonical high-risk leaf 仍保持为：

1. `raw coprime triple classification`
2. `square extraction for r*s with sign cleanup`
3. `strict natAbs descent hic`

`Int.gcd a n = 1 transfer`
不提升为 canonical high-risk leaf 名；
它已由 `second triple classification` 的独立 ledger 一并关闭。
上述 canonical high-risk leaf 名与 `machine_checked_audit.md`、`process_audit.md`
以及本稿中的 ledger 行保持逐字一致；reader-facing 解释句不提升为新的 leaf 名。

| package | one-more-depth items | status |
|---|---|---|
| `bridge packaging` | `Fermat42 bridge predicate`; `not_fermat_42: normalized witness acquisition`; `not_fermat_42: minimal contradiction handoff`; `not_fermat_42: bridge impossibility closure`; `fermatLastTheoremFour: ℕ ↔ ℤ transport`; `fermatLastTheoremFour: quartic-to-square final closure` | `checked` |
| `minimal normalization` | `minimal witness selection`; `primitive reduction by common-prime descent`; `odd-first-coordinate normalization`; `positive-c normalization` | `checked` |
| `first triple classification` | `ht : PythagoreanTriple (a^2) (b^2) c packaging`; `h2 : Int.gcd (a^2) (b^2) = 1 primitive certificate`; `ha22 : a^2 % 2 = 1 odd-leg certificate`; `raw coprime triple classification`; `PythagoreanTriple.coprime_classification' normal-form pruning` | `checked` |
| `second triple classification` | `PythagoreanTriple a n m packaging`; `Int.gcd a n = 1 transfer`; `0 < m upgrade`; `second PythagoreanTriple.coprime_classification' call`; `r,s output interface` | `checked` |
| `coprimality bridge` | `seed import from second classification`; `single-factor lift via Int.isCoprime_of_sq_sum`; `symmetric single-factor lift`; `product lift via Int.isCoprime_of_sq_sum'`; `API handoff to Int.sq_of_gcd_eq_one` | `checked` |
| `square extraction and sign cleanup` | `even-halving normalization to b'^2 = m * (r*s)`; `square extraction for m`; `square extraction for r*s with sign cleanup`; `split d^2 across coprime r and s`; `square away the residual signs` | `checked` |
| `smaller-solution construction and size comparison` | `sign-normalized fourth-power witnesses`; `new witness equation hh`; `minimality re-instantiation hic'`; `strict natAbs descent hic`; `final contradiction` | `checked` |

### 15.2A-15.2G 独立 ledger 集成摘要

| package | total proof steps | descendant closure carried by the same ledger |
|---|---:|---|
| `bridge packaging` | `14` | no extra canonical descendant beyond the package itself |
| `minimal normalization` | `18` | no extra canonical descendant beyond the package itself |
| `first triple classification` | `33` | closes `raw coprime triple classification` |
| `second triple classification` | `13` | closes former package-level unresolved `Int.gcd a n = 1 transfer` |
| `coprimality bridge` | `12` | no extra canonical descendant beyond the package itself |
| `square extraction and sign cleanup` | `30` | closes `square extraction for r*s with sign cleanup` |
| `smaller-solution construction and size comparison` | `19` | closes `strict natAbs descent hic` |

### 15.3 高风险 leaf 再拆一层

以下高风险 leaf 及其 `one-more-depth` 子包都已由 matching package ledger 关闭。

| leaf | one-more-depth items | status |
|---|---|---|
| `raw coprime triple classification` | `positive-z reduction`; `odd-leg dispatch by symmetry`; `zero-left degenerate branch`; `unit-circle rational parameter extraction`; `mixed-parity admissible reconstruction`; `forbidden parity branch elimination`; `raw tuple packaging` | `checked` |
| `square extraction for r*s with sign cleanup` | `API orientation for extracting the second factor`; `raw signed-square witness for r*s`; `negative-branch rewrite to a nonpositive RHS`; `strict positivity of the square side`; `sign cleanup to a clean square equation` | `checked` |
| `strict natAbs descent hic` | `natAbs target recast`; `left witness square bound`; `new-witness substitution`; `old-c expansion`; `strict gap from the residual square`; `transitive close` | `checked` |

### 15.3A 高风险 leaf 的 process-level wording

这些 proof chunk 的命名保持不变，但都已从 process-budget 角度完成闭合：

| leaf | process-level wording | status |
|---|---|---|
| `raw coprime triple classification` | 先做 `positive-z reduction` 与 `odd-leg dispatch by symmetry`，再进入 `circleEquivGen` 驱动的 `unit-circle rational parameter extraction`，随后通过 parity 分支筛掉不合法 `(m,n)` 形态，最后把 witness 打包回 `coprime_classification` 的原始输出。 | `checked` |
| `square extraction for r*s with sign cleanup` | 先把 `hs` 与 `hcp` 通过 `mul_comm` / `Int.gcd_comm` 改成 `Int.sq_of_gcd_eq_one` 的输入形状，得到 `r*s = d^2 ∨ r*s = -d^2`；再用 `m > 0` 和 `b' ≠ 0` 排除负分支，收束到 `r*s = d^2`。 | `checked` |
| `strict natAbs descent hic` | 先把目标改写成正整数 `c` 上的整数不等式，再沿 `natAbs i ≤ i^2 = m ≤ m^2 < m^2 + n^2 = c` 这条链条收束，其中唯一提供严格性的输入是 `hn : n ≠ 0`。 | `checked` |

### 15.4 `n = 4` status ledger

顶层 theorem-flow 行继续描述 theorem-level 的 machine-checked 事实；
下表只审计 process-tree 的 `<=100` leaf-budget closure。
`7` 个 canonical package、`3` 个 canonical high-risk leaf，
以及此前单列的 `Int.gcd a n = 1 transfer`
都已拥有独立 `<=100` proof-step ledger，
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
`n = 4` 人类可读审计表中已无剩余 package-level unresolved subitem。

<!-- HR18_N4_MERGED_START -->
## 附录：`n = 4` 的 7 个 execution unit 公开归档

下列 `7` 个 unit 的稳定公开说明统一归档在本主稿内，不再需要另设公开子稿。
`FLT-HR-001` 到 `FLT-HR-007` 的唯一公开说明目标就是本文件；`human_steps/`、`.cron/results/*` 与自动化工作副本路径都不是公开归档目标。

### `FLT-HR-001` `n = 4 / bridge packaging`

Scope boundary: this unit is limited to the canonical package `bridge packaging` and its bridge predicates/hooks; it does not prove `minimal normalization`, either triple classification, square extraction, or the final descent contradiction.

#### Human-Readable Expansion
`bridge packaging` 的任务不是重做整个无限递降，而是把真正承担递降的内层论证包成一个可复用的外层接口。对 `n = 4` 这条 branch 来说，这个 unit 只负责三件事。

第一，`Fermat42` 把下降入口命名成单个谓词：
`a ≠ 0 ∧ b ≠ 0 ∧ a ^ 4 + b ^ 4 = c ^ 2`。
这里没有新的数论内容，作用只是把“两个非零条件 + quartic-to-square 方程”压成一个统一输入，便于后续最小反例选择、规范化与递降定理都以同一种 witness 形式接线。

第二，`not_fermat_42` 负责关闭 bridge problem
`a ^ 4 + b ^ 4 = c ^ 2`。
它的做法不是在外层重复证明最小化和递降，而是先从假设
`h : a ^ 4 + b ^ 4 = c ^ 2`
与非零条件 `ha`、`hb`
组装出一个 `Fermat42 a b c` witness；
随后调用 `Fermat42.exists_pos_odd_minimal`，取到规范化的最小反例
`a0 b0 c0`，以及
`hf : Minimal a0 b0 c0`、
`h2 : a0 % 2 = 1`、
`hp : 0 < c0`。
桥接层到这里就停止向内展开，并把这三条标准化输出原样交给
`Fermat42.not_minimal`。
因此本 unit 的真正职责是把 outer witness acquisition 和 contradiction handoff 接好，而不是重写 `minimal normalization`、两次勾股数组参数化、平方提取或严格下降。

第三，`fermatLastTheoremFour` 把真正的 FLT(4) 命题送进 bridge theorem。
它先用 `fermatLastTheoremFor_iff_int` 把自然数版本改写到整数版本；
然后面对方程
`heq : a ^ 4 + b ^ 4 = c ^ 4`，
把 bridge theorem 的右端实例化成 `c ^ 2`，
也就是调用
`@not_fermat_42 _ _ (c ^ 2) ha hb`。
此时只需用 `rw [heq]; ring`
把 `c ^ 4` 改写成 `(c ^ 2) ^ 2`，
就把 FLT(4) 的输入方程精确送到了 bridge problem 的禁止结论上。

从本仓库的本地锚点看，
`Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/FLT4Path.lean`
只是把 `fermatLastTheoremFour` 直接导入为 `flt4Path`，
因此 repo-local 的这层 closure 完全落在
`Fermat42`、`not_fermat_42` 与 `fermatLastTheoremFour`
这一条包装链上。
这也解释了为什么本单元可以局部收口：
它只需要把
`a^4 + b^4 = c^4`
如何转交给
`a^4 + b^4 = c^2`
说清楚，而不必越权重写更深的 descent 内核。

#### Local Budget Ledger
本 unit 的独立预算总计 `14` 步，满足本地 `<=100` 步要求。

| canonical subitem | step range | status |
|---|---|---|
| `Fermat42 bridge predicate` | `1-2` | `checked` |
| `not_fermat_42: normalized witness acquisition` | `3-6` | `checked` |
| `not_fermat_42: minimal contradiction handoff` | `7-8` | `checked` |
| `not_fermat_42: bridge impossibility closure` | `9` | `checked` |
| `fermatLastTheoremFour: ℕ ↔ ℤ transport` | `10-11` | `checked` |
| `fermatLastTheoremFour: quartic-to-square final closure` | `12-14` | `checked` |

1. `Fermat42` 先把桥梁谓词定义为 `a ≠ 0 ∧ b ≠ 0 ∧ a ^ 4 + b ^ 4 = c ^ 2`。
2. 因而 `Fermat42` 的局部作用只是把“两个非零条件 + quartic-to-square 方程”压成统一的下降入口。
3. 在 `not_fermat_42` 中先固定 `ha : a ≠ 0`、`hb : b ≠ 0`，并假设 `h : a ^ 4 + b ^ 4 = c ^ 2`。
4. 用 `And.intro ha (And.intro hb h)` 把这三条数据组装成 `Fermat42 a b c` 的 witness。
5. 对该 witness 调用 `Fermat42.exists_pos_odd_minimal`。
6. 得到 `a0 b0 c0` 以及 `hf : Minimal a0 b0 c0`、`h2 : a0 % 2 = 1`、`hp : 0 < c0`，完成 `normalized witness acquisition`。
7. 把 `hf`、`h2`、`hp` 直接交给 `Fermat42.not_minimal`，不在 bridge layer 内部重做 descent。
8. `Fermat42.not_minimal` 立刻返回 `False`，这就是 `minimal contradiction handoff` 的收束。
9. 因而起始假设 `h` 不成立，得到 `a ^ 4 + b ^ 4 ≠ c ^ 2`，即 `not_fermat_42` 关闭 bridge problem。
10. 在 `fermatLastTheoremFour` 中先用 `rw [fermatLastTheoremFor_iff_int]`，把自然数版 `FLT(4)` 改写成整数版。
11. 于是外层目标只剩：给定整数 `a b c`、非零假设与 `heq : a ^ 4 + b ^ 4 = c ^ 4`，推出矛盾。
12. 调用 `@not_fermat_42 _ _ (c ^ 2) ha hb`，把 bridge theorem 的右端实例化为 `c ^ 2`。
13. 用 `rw [heq]; ring` 把 `heq` 改写成 `a ^ 4 + b ^ 4 = (c ^ 2) ^ 2`，与 step 12 的输入形状对齐。
14. 因而 `not_fermat_42` 与 `heq` 矛盾，最终完成 `fermatLastTheoremFour`，也就完成了从 `a^4 + b^4 = c^4` 到 `a^4 + b^4 = c^2` 的桥接包装。

### `FLT-HR-002` `n = 4 / minimal normalization`

Scope boundary: this unit is limited to the canonical package `minimal normalization`; it does not prove either triple classification, square extraction, or the final smaller-solution contradiction.

#### Human-Readable Expansion
`minimal normalization` 的任务是把任意 bridge witness
`Fermat42 a b c`
规整成后续递降链真正使用的标准最小反例。它不证明最终矛盾，
也不展开两次勾股数组分类；它只负责把 witness 选择、互素性和奇正条件
接成一个局部稳定的输入包。

第一步由 `Fermat42.exists_minimal` 完成。给定任意
`Fermat42 a b c`，先按第三个坐标 `c` 的大小使用良序性选择一个
`Fermat42 a0 b0 c0`，并把“没有更小的同类 witness”记录为
`Minimal a0 b0 c0`。这一层只负责最小反例的存在性，
不额外断言奇偶性或互素性。

第二步由 `Fermat42.coprime_of_minimal` 完成。对已经取得的
`Minimal a0 b0 c0`，若 `a0` 与 `b0` 有公共因子，方程
`a0 ^ 4 + b0 ^ 4 = c0 ^ 2`
会迫使该公共因子也可从右端平方中剥离，进而产生一个第三坐标更小的
`Fermat42` witness。这与 `Minimal a0 b0 c0` 矛盾，
所以最小反例必须满足 `Nat.Coprime a0 b0`。

第三步由 `Fermat42.exists_pos_odd_minimal` 完成。它把前两步的输出
继续整理成后续 package 的标准入口：仍保留
`hf : Minimal a1 b1 c1`，并额外给出
`h2 : a1 % 2 = 1` 与 `hp : 0 < c1`。
其中奇性来自互素最小反例的 parity 规整；正性来自 bridge witness 的
平方右端和非零条件。后续 `first triple classification`、
`second triple classification` 与 `strict descent assembly`
都只消费这些标准化结论，而不重新选择最小反例。

从本仓库的本地锚点看，本 unit 仍然只是说明 mathlib 中
`Fermat42.exists_minimal`、`Fermat42.coprime_of_minimal` 与
`Fermat42.exists_pos_odd_minimal` 这三枚 hook 的组合关系；
repo-local 文件不重新 vend 这些 theorem 的闭包证明。
因此本地记录是 anchor-only 的 statement/module/theorem-name 级审计，
而 theorem closure 仍由上游 mathlib 承担。

#### Local Budget Ledger
本 unit 的独立预算总计 `16` 步，满足本地 `<=100` 步要求。

| canonical subitem | step range | status |
|---|---|---|
| `exists_minimal: witness selection` | `1-4` | `checked` |
| `coprime_of_minimal: common-factor exclusion` | `5-9` | `checked` |
| `exists_pos_odd_minimal: parity and positivity normalization` | `10-14` | `checked` |
| `minimal normalization: handoff boundary` | `15-16` | `checked` |

1. Start with an arbitrary witness `h : Fermat42 a b c`.
2. Apply `Fermat42.exists_minimal` to select a witness `Fermat42 a0 b0 c0` with minimal third coordinate.
3. Record the associated certificate as `hf : Minimal a0 b0 c0`.
4. Keep this step scoped to existence of a minimal bridge witness only.
5. Feed `hf : Minimal a0 b0 c0` into `Fermat42.coprime_of_minimal`.
6. Suppose a nontrivial common divisor divides both `a0` and `b0`.
7. Use the quartic-to-square equation inside `Fermat42 a0 b0 c0` to force the corresponding divisibility on `c0`.
8. Divide out the common factor to construct a smaller `Fermat42` witness.
9. Contradict `hf`, yielding `Nat.Coprime a0 b0`.
10. Apply `Fermat42.exists_pos_odd_minimal` to the original bridge witness.
11. Reuse the minimal-witness selection supplied by `exists_minimal`.
12. Reuse the coprimality obstruction supplied by `coprime_of_minimal` to normalize parity.
13. Obtain `h2 : a1 % 2 = 1` for the standardized minimal witness.
14. Obtain `hp : 0 < c1` for the same standardized minimal witness.
15. Hand off exactly `hf : Minimal a1 b1 c1`, `h2 : a1 % 2 = 1`, and `hp : 0 < c1` to later packages.
16. Do not prove the descent contradiction in this unit; that remains the responsibility of downstream `Fermat42.not_minimal` packages.

### `FLT-HR-003` `n = 4 / first triple classification`

Scope boundary: this unit is limited to the canonical package `first triple classification`; it does not prove the second triple classification, coprimality bridge, square extraction, or final descent closure.

#### Human-Readable Expansion
##### 1. 本 unit 在 `n = 4` 下降链中的职责

这一节只负责把已经规范化好的最小反例
`a^4 + b^4 = c^2`
改写成第一组勾股参数 `m, n`。

更精确地说，本节的输入来自上一单元 `minimal normalization`：

- `h : Minimal a b c`
- `ha2 : a % 2 = 1`
- `hc : 0 < c`

本节的输出是 `not_minimal` 中紧接着被命名为 `ht1` 到 `ht6` 的六条结论：

- `ht1 : a ^ 2 = m ^ 2 - n ^ 2`
- `ht2 : b ^ 2 = 2 * m * n`
- `ht3 : c = m ^ 2 + n ^ 2`
- `ht4 : Int.gcd m n = 1`
- `ht5 : (m % 2 = 0 ∧ n % 2 = 1) ∨ (m % 2 = 1 ∧ n % 2 = 0)`
- `ht6 : 0 ≤ m`

这正是 canonical focus 所说的“把 `(a^2, b^2, c)` 变成 `m, n` 数据”。
本节到这里为止；它不继续证明 `(a, n, m)` 的第二次参数化，
也不在这里做平方因子提取。

##### 2. 先把原方程包装成 primitive Pythagorean triple

`PythagoreanTriple x y z` 的定义是
`x * x + y * y = z * z`。
因此从最小反例的核心方程
`h.1.2.2 : a ^ 4 + b ^ 4 = c ^ 2`
出发，只要把 `a ^ 4` 和 `b ^ 4` 看成 `(a ^ 2)^2` 与 `(b ^ 2)^2`，
就得到
`ht : PythagoreanTriple (a ^ 2) (b ^ 2) c`。

这一步只是在说：

- 第一条直角边是 `a^2`
- 第二条直角边是 `b^2`
- 斜边是 `c`

于是原来的四次方程，已经进入 primitive Pythagorean triple 的标准分类框架。

但要调用 primitive 分类，还缺两条证书：

- `h2 : Int.gcd (a ^ 2) (b ^ 2) = 1`
- `ha22 : a ^ 2 % 2 = 1`

第一条来自上一单元的互素化结果。
因为 `coprime_of_minimal h : IsCoprime a b`，
所以平方后仍互素；
再用 `Int.isCoprime_iff_gcd_eq_one` 转成 `gcd = 1` 形式，
就得到 `h2`。

第二条来自奇偶规范化。
既然 `a % 2 = 1`，那么奇数平方仍是奇数，
故 `a ^ 2 % 2 = 1`。
Lean 中这一点写成 `ha22`，
它的作用不是为了新数学内容，
而是为了在 primitive triple 的分类输出里固定“哪一条腿是 odd leg”。

##### 3. `raw coprime triple classification` 给出的原始形状

如果只看 `PythagoreanTriple.coprime_classification` 的原始输出，
它会告诉我们：对于 primitive triple `(x, y, z)`，
存在整数 `m, n`，使得：

- 要么 `x = m^2 - n^2` 且 `y = 2mn`
- 要么 `x = 2mn` 且 `y = m^2 - n^2`
- 同时 `z = m^2 + n^2` 或 `z = -(m^2 + n^2)`
- 并且 `Int.gcd m n = 1`
- 并且 `m, n` 一奇一偶

这就是审计表里单列的 high-risk leaf
`raw coprime triple classification`。
它真正困难的地方，不在“存在 `m,n`”这句话本身，
而在于它先给出的是一个还没有裁成标准形的原始 disjunction：

- 哪一条腿写成 `2mn` 还没定
- 斜边前面的正负号还没定
- 参数的符号规范也还没定

所以 raw classification 还不能直接作为下降法的接口。
下降法后面真正需要的，是固定成
`a^2 = m^2 - n^2`, `b^2 = 2mn`, `c = m^2 + n^2`
这一种标准朝向。

##### 4. `coprime_classification'` 怎样把原始输出裁成标准形

`not_minimal` 里并没有手工拆 raw theorem 的所有分支，
而是直接调用 refined 版本：

`ht.coprime_classification' h2 ha22 hc`

这个 refined theorem 比 raw theorem 多用了两条信息：

- `ha22 : a ^ 2 % 2 = 1`
- `hc : 0 < c`

它们各自负责剪掉一类不想要的分支。

第一，`ha22` 固定 odd leg。
因为 `a^2` 是奇数，`a^2` 不可能等于 `2mn`；
`2mn` 总是偶数。
所以 raw 输出中“交换两条腿”的分支被消掉，
只能保留
`a^2 = m^2 - n^2` 与 `b^2 = 2mn`。

第二，`hc` 固定斜边符号。
raw theorem 允许
`c = m^2 + n^2`
或
`c = -(m^2 + n^2)`。
但后一种右端非正，与 `0 < c` 矛盾；
所以只剩
`c = m^2 + n^2`。

第三，refined theorem 还做了一个参数符号标准化。
若 raw classification 先产出的是负的 `m`，
就把 `(m, n)` 同时换成 `(-m, -n)`。
因为涉及的表达式只有 `m^2 - n^2`、`2mn`、`m^2 + n^2`，
这种同时取负不会改变三条主等式，
也不会破坏互素与“奇偶相反”这类结构信息。
这样就能额外得到 `0 ≤ m`。

所以，本节的核心不是“凭空发明出 `m,n`”，
而是把 primitive triple 的 raw classification
借助 odd-leg 与 positivity 规整成 descent 真正能用的标准接口。

##### 5. 本节交给下游的接口是什么

本节结束时，`not_minimal` 获得
`⟨m, n, ht1, ht2, ht3, ht4, ht5, ht6⟩`，
其数学含义是：

- `a^2` 被拆成平方差 `m^2 - n^2`
- `b^2` 被拆成双积 `2mn`
- `c` 被拆成平方和 `m^2 + n^2`
- `m,n` primitive，即 `Int.gcd m n = 1`
- `m,n` 奇偶相反
- `m` 已被规整到非负

下一个单元只需要把这些输出原样接走：

- 用 `ht1` 把 `(a, n, m)` 再包装成第二个 `PythagoreanTriple`
- 用 `ht4` 与 `ht5` 继续管理第二层参数化需要的 primitive 条件
- 用 `ht6` 作为后续升级到 `0 < m` 的起点

也就是说，本节已经把“原反例”成功压缩成“第一组参数数据”，
但还没有进入第二次参数化，更没有开始平方提取。

##### 6. 局部闭合判断

就 canonical node 而言，本节已经完成以下闭合：

- `ht : PythagoreanTriple (a^2) (b^2) c packaging`
- `h2 : Int.gcd (a^2) (b^2) = 1 primitive certificate`
- `ha22 : a^2 % 2 = 1 odd-leg certificate`
- `raw coprime triple classification`
- `PythagoreanTriple.coprime_classification' normal-form pruning`

因此本 unit 可以标记为 `completed`。
剩余工作全部属于下游单元 `second triple classification`
及其后继节点，而不是本节的 blocker。

#### Local Budget Ledger
##### Budget Summary

| subitem | step range | status |
|---|---|---|
| `ht : PythagoreanTriple (a^2) (b^2) c packaging` | `1-4` | `checked` |
| `h2 : Int.gcd (a^2) (b^2) = 1 primitive certificate` | `5-9` | `checked` |
| `ha22 : a^2 % 2 = 1 odd-leg certificate` | `10-12` | `checked` |
| `raw coprime triple classification` | `13-27` | `checked` |
| `PythagoreanTriple.coprime_classification' normal-form pruning` | `28-33` | `checked` |

总步数：`33`，满足 `<=100` 步约束。

##### Step Ledger

1. 从 `h : Minimal a b c` 取出核心方程 `h.1.2.2 : a ^ 4 + b ^ 4 = c ^ 2`。
2. 把 `a ^ 4` 识别成 `(a ^ 2)^2`，把 `b ^ 4` 识别成 `(b ^ 2)^2`。
3. 回忆 `PythagoreanTriple x y z` 的定义就是 `x * x + y * y = z * z`。
4. 用 `linear_combination h.1.2.2` 打包出 `ht : PythagoreanTriple (a ^ 2) (b ^ 2) c`。
5. 从上一单元继承 `coprime_of_minimal h : IsCoprime a b`。
6. 对这条互素性做平方提升，得到 `(coprime_of_minimal h).pow : IsCoprime (a ^ 2) (b ^ 2)`。
7. 把互素性改写成 `gcd = 1` 语言。
8. 得到 `h2 : Int.gcd (a ^ 2) (b ^ 2) = 1`。
9. 至此 `(a^2, b^2, c)` 已满足 primitive triple 分类的互素输入条件。
10. 读取本单元输入中的奇偶规范化假设 `ha2 : a % 2 = 1`。
11. 用“奇数平方仍为奇数”计算 `(a ^ 2) % 2`。
12. 得到 `ha22 : a ^ 2 % 2 = 1`，即第一条腿 `a^2` 是 odd leg。
13. 对 `ht` 与 `h2` 应用 primitive triple 的 raw classification 思想。
14. raw theorem 先给出某组暂时未规范的参数 `m, n`。
15. 它允许第一条腿和第二条腿两种朝向之一：`x = m^2 - n^2, y = 2mn` 或反过来。
16. 它也允许斜边有两个符号：`z = m^2 + n^2` 或 `z = -(m^2 + n^2)`。
17. 同时它给出 `Int.gcd m n = 1`。
18. 同时它给出 `m, n` 一奇一偶。
19. 因而 raw theorem 已经把 primitive triple 的内容压缩进两参数表达式。
20. 但这时还没有指定 `a^2` 究竟对应平方差还是双积。
21. 也还没有指定 `c` 究竟取正平方和还是负平方和。
22. 参数本身的符号规范也还没有被固定。
23. 所以后续下降法暂时还不能直接拿 raw 输出当接口。
24. 不过 raw theorem 至少已经暴露出两个关键模板：某条腿是 `2mn`，另一条腿是 `m^2 - n^2`。
25. 这正是下一层下降要使用的“积结构”和“平方差结构”的来源。
26. 对本节而言，剩下唯一要做的是把这些模板定向到 `a^2`、`b^2`、`c` 的正确位置。
27. 这一步在 Lean 中不再手拆 raw theorem，而是交给 refined theorem `coprime_classification'`。
28. 在 `not_minimal` 中直接调用 `ht.coprime_classification' h2 ha22 hc`。
29. 由于 `ha22` 说明 `a^2` 为奇数，分支 `a^2 = 2 * m * n` 被排除，因为 `2 * m * n` 必为偶数。
30. 因而只剩 `a ^ 2 = m ^ 2 - n ^ 2` 与 `b ^ 2 = 2 * m * n` 这一种腿的朝向。
31. 由于 `hc : 0 < c`，分支 `c = -(m ^ 2 + n ^ 2)` 被排除，只剩 `c = m ^ 2 + n ^ 2`。
32. refined theorem 若遇到负的参数 `m`，会把 `(m, n)` 同时替换成 `(-m, -n)`，从而保住三条主等式并补出 `0 ≤ m`。
33. 最终得到 `⟨m, n, ht1, ht2, ht3, ht4, ht5, ht6⟩`，即本节所需的标准化第一组参数接口，并把该接口完整交给下一个 unit。

### `FLT-HR-004` `n = 4 / second triple classification`

Scope boundary: this unit is limited to the canonical package `second triple classification`; it does not prove downstream square extraction, sign cleanup, or the final smaller-solution contradiction.

#### Human-Readable Expansion
##### 1. 本单元在 `not_minimal` 里的输入位置

本单元承接第一次 primitive Pythagorean triple 分类的输出。到这里为止，`Fermat42.not_minimal`
已经有：

- `ht1 : a ^ 2 = m ^ 2 - n ^ 2`
- `ht2 : b ^ 2 = 2 * m * n`
- `ht3 : c = m ^ 2 + n ^ 2`
- `ht4 : Int.gcd m n = 1`
- `ht6 : 0 <= m`
- `ha2 : a % 2 = 1`

其中真正驱动第二次分类的是 `ht1`、`ht4`、`ht6` 和旧的奇数条件 `ha2`。
数学上，`ht1` 说明

`a ^ 2 + n ^ 2 = m ^ 2`

所以 `(a, n, m)` 自身又是一个勾股三元组；剩下要补的只是：

1. 它确实是 primitive 的，即 `Int.gcd a n = 1`。
2. 它满足 `coprime_classification'` 需要的奇偶与正性输入，即 `a` 为奇数且 `0 < m`。

这正对应 canonical 子节点：

- `PythagoreanTriple a n m packaging`
- `Int.gcd a n = 1 transfer`
- `0 < m upgrade`
- `second PythagoreanTriple.coprime_classification' call`
- `r,s output interface`

##### 2. `PythagoreanTriple a n m packaging`

Lean 先定义

`have htt : PythagoreanTriple a n m := by ...`

其证明只做一件事：把 `ht1` 改写成勾股三元组定义需要的平方和形式。

因为

`ht1 : a ^ 2 = m ^ 2 - n ^ 2`

等价于

`a ^ 2 + n ^ 2 = m ^ 2`，

所以 `(a, n, m)` 被正式打包成新的 `PythagoreanTriple` witness `htt`。这一步没有引入新数论内容，
只是把第一次分类留下的代数恒等式转成第二次分类 theorem 的输入形状。

##### 3. `Int.gcd a n = 1 transfer`

这是本单元最关键的本地闭合点，也是此前单列的 package-level unresolved subitem。

第一次分类只直接给了

`ht4 : Int.gcd m n = 1`，

但第二次分类要喂进去的是

`h3 : Int.gcd a n = 1`。

Lean 的处理方式是先证明 `a ^ 2` 与 `n` 互素，再把平方因子从左边剥掉：

1. 用 `ht1` 把 `a ^ 2` 改写成 `m ^ 2 - n ^ 2`。
2. 再把右边写成 `m ^ 2 + (-n) * n`，这样就能直接套用“与 `n` 互素的数，加上 `n` 的倍数后仍与 `n` 互素”的 API。
3. 从 `ht4` 得到 `m` 与 `n` 互素，因此 `m ^ 2` 与 `n` 也互素。
4. 于是 `m ^ 2 + (-n) * n` 与 `n` 互素，也就是 `a ^ 2` 与 `n` 互素。
5. 最后用 `IsCoprime.of_mul_left_left` 把“`a ^ 2` 与 `n` 互素”降回“`a` 与 `n` 互素”。

因此得到：

`h3 : Int.gcd a n = 1`。

这一步的数学含义很直接：如果某个公因子同时整除 `a` 和 `n`，那它也整除 `a ^ 2`；
而 `a ^ 2 = m ^ 2 - n ^ 2` 又会把这个公因子推回去整除 `m ^ 2`，最终与 `m,n` primitive 的已知事实冲突。

##### 4. `0 < m upgrade`

第二次分类 theorem 不只要三元组和 primitive 条件，还要斜边正性。
第一次分类这里只显式留下了

`ht6 : 0 <= m`。

因此本单元要把弱不等式升级成严格正性：

- 若 `m = 0`，则由 `ht2 : b ^ 2 = 2 * m * n` 立刻得到 `b ^ 2 = 0`。
- 但最小反例数据 `h` 自带 `b != 0`，所以 `b ^ 2 != 0`。
- 矛盾。

于是得到：

`h4 : 0 < m`。

这一步的作用不是新分类，而是把第一次分类输出的非负 side-condition
精确升级成第二次分类 API 所要求的正性输入。

##### 5. `second PythagoreanTriple.coprime_classification' call`

到这一步，第二次调用 `coprime_classification'` 所需的三类输入已经齐备：

- `htt : PythagoreanTriple a n m`
- `h3 : Int.gcd a n = 1`
- `ha2 : a % 2 = 1`
- `h4 : 0 < m`

于是源码执行：

`obtain ⟨r, s, _, htt2, htt3, htt4, htt5, htt6⟩ := htt.coprime_classification' h3 ha2 h4`

这表示：对第二个 primitive triple `(a, n, m)` 再做一次标准参数化，
把它拆成一对新参数 `r, s`。

##### 6. `r,s output interface`

这次调用输出的数学接口是经典的第二层参数化：

- `a = r ^ 2 - s ^ 2`
- `htt2 : n = 2 * r * s`
- `htt3 : m = r ^ 2 + s ^ 2`
- `htt4 : Int.gcd r s = 1`

此外还会带出两个奇偶 / 非负 side-condition：

- `htt5 : (r % 2 = 0 ∧ s % 2 = 1) ∨ (r % 2 = 1 ∧ s % 2 = 0)`
- `htt6 : 0 <= r`

在 `not_minimal` 的后续代码里，
本单元立刻实际消费的是：

- `htt2`，因为它会与 `ht2` 合并成 `b ^ 2 = 4 * m * r * s`
- `htt3`，因为它把 `m` 写成和平方，方便后续建立 `m` 与 `r*s` 的互素性
- `htt4`，因为后续要从 `r*s` 是平方推出 `r` 与 `s` 分别是平方

而 `a = r ^ 2 - s ^ 2` 虽然是完整数学接口的一部分，但在 Lean 这段 proof 的紧邻下游里并不是立刻消耗的关键输出，
所以源码把对应证明项记成 `_`。这不是遗漏，而是说明这一单元的 machine-level 重点确实是：

1. 把 `(a, n, m)` 成功送入第二次 primitive classification；
2. 拿到 downstream 真正要用的 `n = 2rs`、`m = r^2 + s^2` 与 `gcd(r,s)=1`。

##### 7. 本单元的局部闭环

因此，`second triple classification` 这个 unit 的本地闭环可以精确表述为：

- 从第一次分类给出的 `a ^ 2 = m ^ 2 - n ^ 2`、`gcd(m,n)=1`、`0 <= m`
- 构造 `PythagoreanTriple a n m`
- 关闭 `Int.gcd a n = 1 transfer`
- 升级出 `0 < m`
- 再次调用 `PythagoreanTriple.coprime_classification'`
- 输出第二层参数 `r, s` 以及后续 `coprimality bridge` / `square extraction` 立即要消费的接口

这就完成了 canonical focus 所说的：

`turning (a, n, m) into r, s data`

而且不越界进入下一单元。

#### Local Budget Ledger
本单元采用 `13` 步局部 ledger，满足 `<=100` 步约束。

| subitem | step range | status |
|---|---|---|
| `PythagoreanTriple a n m packaging` | `1-2` | `checked` |
| `Int.gcd a n = 1 transfer` | `3-7` | `checked` |
| `0 < m upgrade` | `8-10` | `checked` |
| `second PythagoreanTriple.coprime_classification' call` | `11` | `checked` |
| `r,s output interface` | `12-13` | `checked` |

1. 承接第一次分类输出 `ht1 : a ^ 2 = m ^ 2 - n ^ 2`。
2. 用 `delta PythagoreanTriple` 与 `linear_combination ht1` 把它重写成 `a ^ 2 + n ^ 2 = m ^ 2`，得到 `htt : PythagoreanTriple a n m`。
3. 为了证明第二次分类所需的 primitive 条件，目标转成 `h3 : Int.gcd a n = 1`。
4. 先通过 `IsCoprime.of_mul_left_left` 把问题提升到“证明 `a ^ 2` 与 `n` 互素”。
5. 用 `ht1` 与恒等式 `m ^ 2 - n ^ 2 = m ^ 2 + (-n) * n`，把 `a ^ 2` 改写成“与 `n` 互素的平方 `m ^ 2` 加上一个 `n` 的倍数”。
6. 由 `ht4 : Int.gcd m n = 1` 得到 `m` 与 `n` 互素，再经 `.pow_left.add_mul_right_left (-n)` 推出 `a ^ 2` 与 `n` 互素。
7. 回收第 `4-6` 步，得到 `h3 : Int.gcd a n = 1`；这一步关闭 package-level unresolved subitem `Int.gcd a n = 1 transfer`。
8. 从第一次分类继承 `ht6 : 0 <= m`。
9. 反设 `m = 0`，则由 `ht2 : b ^ 2 = 2 * m * n` 得到 `b ^ 2 = 0`。
10. 但最小反例给出 `b != 0`，故 `b ^ 2 != 0`，矛盾；于是 `h4 : 0 < m`。
11. 以 `htt`、`h3`、`ha2 : a % 2 = 1`、`h4` 为输入，调用 `htt.coprime_classification' h3 ha2 h4`。
12. 得到第二层参数 `r, s`，并获得核心接口 `htt2 : n = 2 * r * s`、`htt3 : m = r ^ 2 + s ^ 2`、`htt4 : Int.gcd r s = 1`。
13. 因而 `(a, n, m)` 已成功转换成后续单元直接可消费的 `r, s` 数据；本单元在这里收束，不继续展开 `b'^2 = m * (r*s)` 与平方提取。

### `FLT-HR-005` `n = 4 / coprimality bridge`

Scope boundary: this unit is limited to the canonical package `coprimality bridge`; it does not prove square extraction itself or the final smaller-solution construction.

#### Human-Readable Expansion
##### 1. 本 unit 的局部任务

两次 primitive Pythagorean-triple 分类结束后，手里已经有两组结构数据：

- 第一轮给出 `b ^ 2 = 2 * m * n`。
- 第二轮给出 `n = 2 * r * s`、`m = r ^ 2 + s ^ 2`、`Int.gcd r s = 1`。

把前两式合并，会在下一包得到

`b ^ 2 = 4 * m * r * s`

以及经偶因子整理后的

`hs : b' ^ 2 = m * (r * s)`。

但仅有“乘积是平方”还不够；要把平方结构拆到因子内部，必须先知道乘积两侧互素。
因此本 unit 的唯一职责是把第二轮分类里自带的 `Int.gcd r s = 1`
输运成

- `m` 与 `r` 互素；
- `m` 与 `s` 互素；
- 因而 `m` 与 `r * s` 互素。

这就是 canonical 名字里所谓的 `coprimality bridge`：
它把来自第一轮的参数 `m` 与来自第二轮的参数 `r,s` 接到同一个 primitive square-product 接口上。

##### 2. 为什么 `m` 能和新参数 `r,s` 建立互素关系

关键不是重新做一次 gcd 计算，而是利用第二轮分类给出的形状

`m = r ^ 2 + s ^ 2`。

因为 `(a, n, m)` 是第二个 primitive 勾股三元组，
分类结论已经附带 `htt4 : Int.gcd r s = 1`。
把它改写成 `IsCoprime r s` 后，
`Int.isCoprime_of_sq_sum` 的数学含义正是：

- 若 `r` 与 `s` 互素，则 `r ^ 2 + s ^ 2` 与 `r` 互素；
- 交换 `r,s` 后，同理 `r ^ 2 + s ^ 2` 与 `s` 互素。

所以 `m` 不是孤立出现的中间量，
而是一个由互素参数 `r,s` 生成的平方和；
正因为如此，它能自然地与 `r`、`s` 逐个建立互素性。

##### 3. 从单因子互素提升到乘积互素

在机器证明里，单因子互素与乘积互素分别由两条 hook 承担：

- `Int.isCoprime_of_sq_sum`
- `Int.isCoprime_of_sq_sum'`

前者解释“平方和对单个因子仍然互素”，
后者则把这件事一次性打包成：

`IsCoprime (r ^ 2 + s ^ 2) (r * s)`。

再用 `htt3 : m = r ^ 2 + s ^ 2` 改写左边，
就得到 Lean 后续真正保存下来的证书

`hcp : Int.gcd m (r * s) = 1`。

从代码上看，`not_minimal` 直接用 `Int.isCoprime_of_sq_sum'` 一步得到 `hcp`；
但从人类可读层面，把它拆成

1. `m` 与 `r` 互素，
2. `m` 与 `s` 互素，
3. `m` 与 `r*s` 互素

更能看清这一步到底在做什么：
它不是新引入数论内容，而是把“第二轮 primitive 分类的互素性”
运送到“下一步平方积拆分”的接口上。

##### 4. 这一步为何正好是 square-product bridge

下一包真正会调用的是

`Int.sq_of_gcd_eq_one hcp hs.symm`

其中：

- `hs` 提供“乘积等于平方”；
- `hcp` 提供“两个因子互素”。

没有 `hcp`，`hs` 只说明 `m * (r*s)` 是平方，
却不能推出 `m` 本身是平方，也不能推出 `r*s` 本身是平方。
因此本 unit 虽然不直接抽平方，
却负责把 square extraction 所需的 primitive 条件补齐。

而且这份桥接信息不是一次性的：

- `hcp` 先用于从 `m * (r*s) = b' ^ 2` 抽出 `m = ± i ^ 2`；
- 随后把同一个平方积改写为 `r * s = d ^ 2` 时，
  原始的 `htt4 : Int.gcd r s = 1` 又会继续驱动对 `r`、`s` 的单独平方抽取。

所以这份 ledger 的输出合同非常明确：
它结束时并不产生新解，
只产生后两次 `Int.sq_of_gcd_eq_one` 调用所需的 coprimality certificates。

##### 5. 本 unit 的闭合输出

本 unit 完成后，可以把以下三项视为稳定导出：

- `htt4 : Int.gcd r s = 1`，保留给后续把 `r*s = d^2` 再拆成 `r = ±j^2`、`s = ±k^2`。
- `hcp : Int.gcd m (r * s) = 1`，供 `Int.sq_of_gcd_eq_one hcp hs.symm` 使用。
- `m = r ^ 2 + s ^ 2` 的解释被固定，因此“来自第一轮的 `m`”与“来自第二轮的 `r,s`”之间的互素性输运已经闭合。

#### Local Budget Ledger
`coprimality bridge` 的局部预算总计 `12` 步，满足 `<=100` 约束。

| subitem | step range | status |
|---|---|---|
| `seed import from second classification` | `1-2` | `checked` |
| `single-factor lift via Int.isCoprime_of_sq_sum` | `3-5` | `checked` |
| `symmetric single-factor lift` | `6-7` | `checked` |
| `product lift via Int.isCoprime_of_sq_sum'` | `8-10` | `checked` |
| `API handoff to Int.sq_of_gcd_eq_one` | `11-12` | `checked` |

1. 从第二轮 primitive triple 分类的输出固定两条核心数据：`htt3 : m = r ^ 2 + s ^ 2` 与 `htt4 : Int.gcd r s = 1`。
2. 用 `Int.isCoprime_iff_gcd_eq_one.mpr htt4` 把 `htt4` 转成 `h_rs : IsCoprime r s`，作为全部桥接的种子输入。
3. 由 `isCoprime_comm.mp h_rs` 得到 `IsCoprime s r`。
4. 对这条互素性应用 `Int.isCoprime_of_sq_sum`，得到 `IsCoprime (r ^ 2 + s ^ 2) r`。
5. 用 `htt3` 把左因子改写为 `m`，把这条结论读成“`m` 与 `r` 互素”。
6. 交换 `r,s` 的角色，并用 `rw [add_comm]` 调整平方和顺序，再次应用 `Int.isCoprime_of_sq_sum`。
7. 因而得到 `IsCoprime (r ^ 2 + s ^ 2) s`，再借 `htt3` 读成“`m` 与 `s` 互素”。
8. 对原始 `h_rs : IsCoprime r s` 直接应用 `Int.isCoprime_of_sq_sum'`，得到 `IsCoprime (r ^ 2 + s ^ 2) (r * s)`。
9. 用 `htt3` 改写左因子，得到 `IsCoprime m (r * s)`。
10. 再经 `Int.isCoprime_iff_gcd_eq_one.mp`，输出机器后续真正消费的证书 `hcp : Int.gcd m (r * s) = 1`。
11. 当下一包构造出 `hs : b' ^ 2 = m * (r * s)` 后，`hcp` 正好与 `hs.symm` 组成 `Int.sq_of_gcd_eq_one hcp hs.symm` 的完整输入接口。
12. 此外，`htt4` 不会被消费掉；它会与后续的 `hd : r * s = d ^ 2` 再次配对，用于把 `r*s` 的平方分解继续向 `r` 与 `s` 两个互素因子内部推进。

### `FLT-HR-006` `n = 4 / square extraction and sign cleanup`

Scope boundary: this unit is limited to the canonical package `square extraction and sign cleanup`; it does not prove the final smaller-solution construction or the strict descent contradiction.

#### Human-Readable Expansion
##### 1. 本单元接收的局部输入

本单元只消费平方提取所需的那组局部接口，不回头重做最小化或第二次勾股参数化：

- 已将 `b^2 = 4 m r s` 规整为 `b'^2 = m * (r * s)`。
- 已有 `gcd(m, r * s) = 1`，可直接交给 `Int.sq_of_gcd_eq_one`。
- 已有 `gcd(r, s) = 1`。
- 已有 `m = r^2 + s^2`，因此 `m > 0`。
- 已有 `b' ≠ 0`，因此 `b'^2 > 0`。
- `r`、`s` 的符号规范已在上游固定；这里不重做 primitive triple classification，只消费其输出。

本单元的任务只有一件事：
把 `b'^2 = m * (r * s)` 这条“平方等于互素乘积”的信息，翻译成后续下降直接要用的平方见证
`hi`、`hd`、`hj`、`hk`、`hj0`、`hk0`、`hj2`、`hk2`。

##### 2. `even-halving normalization to b'^2 = m * (r*s)`

这一步是进入平方抽取 API 前的入口整理。

从

`b^2 = 4 m r s`

先读出 `b` 为偶数，写成 `b = 2b'`，代回即得

`b'^2 = m * (r * s)`。

之所以先把 `r * s` 打包成一个整体，是因为第一轮抽取针对的不是 `r` 和 `s` 各自，
而是互素二因子 `(m, r * s)`。
这正好匹配 `Int.sq_of_gcd_eq_one` 的输入形状。

##### 3. `square extraction for m`

已经有：

- `b'^2 = m * (r * s)`
- `gcd(m, r * s) = 1`

因此可以把 `(m, r * s)` 视为“互素两因子乘积为平方”的标准输入，
对第一个因子 `m` 应用平方抽取器，得到 signed witness：

- 存在整数 `i`，使得 `m = i^2`；或
- 存在整数 `i`，使得 `m = -i^2`。

但这里 `m = r^2 + s^2 > 0` 已经是本单元现成输入，
所以负平方分支立即被排除，最终固定 clean witness：

`hi : m = i^2`。

这一步除了给出 `hi` 以外，还有一个局部用途：
后面若出现 `r * s = -d^2` 的负分支，`m > 0` 会提供严格正的乘子，
从而把右边压成非正数。

##### 4. `square extraction for r*s with sign cleanup`

为了让 `Int.sq_of_gcd_eq_one` 作用到第二个整体因子 `r * s`，
先把等式与 gcd 证书都调到“`r*s` 在前”的 API 朝向：

- 把 `b'^2 = m * (r * s)` 用 `mul_comm` 改写成 `b'^2 = (r * s) * m`；
- 把 `gcd(m, r * s) = 1` 用 `Int.gcd_comm` 改写成 `gcd(r * s, m) = 1`。

再对 `(r * s, m)` 调用同一个平方抽取器，得到原始 signed witness：

- `r * s = d^2`；或
- `r * s = -d^2`。

负分支必须在这里清掉。若假设

`r * s = -d^2`，

则原方程变为

`b'^2 = m * (r * s) = -m * d^2`。

此时：

- 右边由于 `m > 0`，只能满足 `-m * d^2 <= 0`；
- 左边由于 `b' ≠ 0`，则 `b'^2 > 0`。

同一等式两边不可能一边严格正、一边非正，因此负分支不成立。
于是这里真正留下的是 clean square equation：

`hd : r * s = d^2`。

这一步正对应 canonical high-risk leaf
`square extraction for r*s with sign cleanup`
及其五个 one-more-depth 子节点：

- `API orientation for extracting the second factor`
- `raw signed-square witness for r*s`
- `negative-branch rewrite to a nonpositive RHS`
- `strict positivity of the square side`
- `sign cleanup to a clean square equation`

##### 5. `split d^2 across coprime r and s`

已知

- `hd : r * s = d^2`
- `gcd(r, s) = 1`

于是可以把平方抽取再向内部推进到 `r` 和 `s`。

先对 `r` 抽取，得到 signed witness：

- `hj : r = j^2` 或 `r = -j^2`。

再交换乘积顺序与 gcd 顺序，对 `s` 抽取，得到：

- `hk : s = k^2` 或 `s = -k^2`。

这里故意不强行把 `hj`、`hk` 立刻清成“正平方”。
Lean 的稳定收束方式是保留 signed witness，
并在下一步把它们统一提升成四次方等式。

##### 6. `square away the residual signs`

对 `hj` 和 `hk`，无论落在正平方还是负平方分支，
两边再平方一次后都会得到同一个 clean 结论：

- 由 `hj` 得 `hj2 : r^2 = j^4`
- 由 `hk` 得 `hk2 : s^2 = k^4`

这样残余符号在四次方层面自动消失。

同时，由 `r * s ≠ 0` 与 `hj`、`hk` 可继续得到：

- `hj0 : j ≠ 0`
- `hk0 : k ≠ 0`

因此，本单元稳定交付给下一单元的局部输出为：

- `hi : m = i^2`
- `hd : r * s = d^2`
- signed witnesses `hj`, `hk`
- nonzero side-conditions `hj0`, `hk0`
- sign-normalized witnesses `hj2 : r^2 = j^4`、`hk2 : s^2 = k^4`

把 `hi`、`m = r^2 + s^2`、`hj2`、`hk2` 串起来，
下一单元就能收束到新的下降方程

`i^2 = j^4 + k^4`。

所以本单元的真实职责不是把参数全部改写成“正平方变量”，
而是把 square extraction layer 所需的 clean witness 和 sign-normalized witness
完整、稳定地准备好。

#### Local Budget Ledger
局部预算总计：`25` 步，满足本单元 `<=100` 的要求。

| step | canonical node | local action | status |
|---|---|---|---|
| 1 | `even-halving normalization to b'^2 = m * (r*s)` | 从上游接收 `b^2 = 4mrs` | `checked` |
| 2 | `even-halving normalization to b'^2 = m * (r*s)` | 写 `b = 2b'`，得到 `b'^2 = m * (r*s)` | `checked` |
| 3 | `even-halving normalization to b'^2 = m * (r*s)` | 记录局部输入：`gcd(m,r*s)=1`、`gcd(r,s)=1`、`m>0`、`b'≠0` | `checked` |
| 4 | `square extraction for m` | 把 `b'^2 = m * (r*s)` 视为互素两因子乘积为平方 | `checked` |
| 5 | `square extraction for m` | 对 `(m, r*s)` 应用平方抽取器 | `checked` |
| 6 | `square extraction for m` | 得到 signed witness：`m = i^2` 或 `m = -i^2` | `checked` |
| 7 | `square extraction for m` | 用 `m > 0` 排除 `m = -i^2` | `checked` |
| 8 | `square extraction for m` | 固定 clean witness `hi : m = i^2` | `checked` |
| 9 | `square extraction for r*s with sign cleanup` | 用 `mul_comm` 改写成 `b'^2 = (r*s) * m` | `checked` |
| 10 | `square extraction for r*s with sign cleanup` | 用 `Int.gcd_comm` 改写成 `gcd(r*s,m)=1` | `checked` |
| 11 | `square extraction for r*s with sign cleanup` | 对 `(r*s, m)` 应用平方抽取器 | `checked` |
| 12 | `square extraction for r*s with sign cleanup` | 得到 signed witness：`r*s = d^2` 或 `r*s = -d^2` | `checked` |
| 13 | `square extraction for r*s with sign cleanup` | 假设负分支并改写成 `b'^2 = -m*d^2` | `checked` |
| 14 | `square extraction for r*s with sign cleanup` | 用 `m > 0` 得到右边 `<= 0` | `checked` |
| 15 | `square extraction for r*s with sign cleanup` | 用 `b' ≠ 0` 得到左边 `b'^2 > 0` | `checked` |
| 16 | `square extraction for r*s with sign cleanup` | 由号性矛盾排除负分支 | `checked` |
| 17 | `square extraction for r*s with sign cleanup` | 固定 clean witness `hd : r*s = d^2` | `checked` |
| 18 | `split d^2 across coprime r and s` | 结合 `gcd(r,s)=1` 与 `hd`，先对 `r` 抽取平方 | `checked` |
| 19 | `split d^2 across coprime r and s` | 得到 signed witness `hj : r = j^2` 或 `r = -j^2` | `checked` |
| 20 | `split d^2 across coprime r and s` | 从 `r*s ≠ 0` 与 `hj` 推出 `hj0 : j ≠ 0` | `checked` |
| 21 | `split d^2 across coprime r and s` | 交换乘积与 gcd 顺序，对 `s` 抽取平方 | `checked` |
| 22 | `split d^2 across coprime r and s` | 得到 signed witness `hk : s = k^2` 或 `s = -k^2` | `checked` |
| 23 | `split d^2 across coprime r and s` | 从 `r*s ≠ 0` 与 `hk` 推出 `hk0 : k ≠ 0` | `checked` |
| 24 | `square away the residual signs` | 将 `hj` 两边平方，得到 `hj2 : r^2 = j^4` | `checked` |
| 25 | `square away the residual signs` | 将 `hk` 两边平方，得到 `hk2 : s^2 = k^4`，并完成本单元出口对齐 | `checked` |

### `FLT-HR-007` `n = 4 / smaller-solution construction and size comparison`

Scope boundary: this unit is limited to the canonical package `smaller-solution construction and size comparison`; it closes the local `n = 4` descent package but does not prove unrelated `n = 3` or regular-primes branches.

#### Human-Readable Expansion
本单元只解释“如何把前面几层已经抽出的平方/四次方结构重新打包成一个更小的 `Fermat42` 解，并用最小性得到矛盾”。
前置构造与互素性证明都视为上一层已经完成；这里不重做那些部分，只接收它们给出的接口。

可直接调用的前置数据如下：

- `h : Minimal a b c`，表示 `(a,b,c)` 是一个 `Fermat42` 最小反例。
- `hc : 0 < c`，因此后面可以把 `Int.natAbs c` 直接改写成 `c`。
- 第一轮参数化给出 `ht3 : c = m^2 + n^2`。
- 平方抽取给出 `hi : m = i^2`。
- 第二轮参数化给出 `htt3 : m = r^2 + s^2`。
- 从 `r*s` 是平方以及 `gcd(r,s)=1` 的抽取步骤，得到带符号的平方见证 `hj`、`hk`；Lean 不要求此时先把 `r`、`s` 各自规范成正平方，而是直接把它们平方掉。
- 由上一步的非零性与乘积非零结论，可继续得到 `hj0 : j ≠ 0`、`hk0 : k ≠ 0`。
- 还知道 `hn : n ≠ 0`。这是最后严格不等式里唯一真正提供“严格性”的输入。

##### `sign-normalized fourth-power witnesses`

`Int.sq_of_gcd_eq_one` 给出的 `hj`、`hk` 本质上是“`r` 与 `s` 各自等于某个平方，或者等于某个平方的相反数”。
因此这里最自然的收束方式不是硬把符号立即清掉，而是先把两边再平方一次：

- 从 `hj` 得到 `hj2 : r^2 = j^4`。
- 从 `hk` 得到 `hk2 : s^2 = k^4`。

这样一来，`r`、`s` 的符号在四次方层面自动消失。
同时，由 `r*s ≠ 0` 可知 `r ≠ 0` 且 `s ≠ 0`；若 `j = 0`，则 `r = 0`，矛盾；同理 `k ≠ 0`。
这一步的结果是：新解的前两个坐标 `j,k` 已经满足 `Fermat42` 所需的非零条件，而且其四次方形态已经被彻底规范化。

##### `new witness equation hh`

将上一层留下来的三个等式串起来：

`i^2 = m = r^2 + s^2 = j^4 + k^4`。

其中：

- `i^2 = m` 来自 `hi`；
- `m = r^2 + s^2` 来自 `htt3`；
- `r^2 = j^4`、`s^2 = k^4` 来自 `hj2`、`hk2`。

Lean 把这条新方程记成

`hh : i^2 = j^4 + k^4`。

但 `Fermat42 j k i` 需要的方向是 `j^4 + k^4 = i^2`，所以在最小性重实例化时实际使用的是 `hh.symm`。
这一步完成后，新的候选下降解已经完全成形：它就是 `(j, k, i)`。

##### `minimality re-instantiation hic'`

`Minimal a b c` 的定义不是一句抽象“最小”，而是一个可重新调用的接口：

对任意新的 `Fermat42 a1 b1 c1`，都有
`Int.natAbs c ≤ Int.natAbs c1`。

因此，只要把刚构造好的 `(j,k,i)` 重新打包成 `Fermat42 j k i`，就立刻得到

`hic' : Int.natAbs c ≤ Int.natAbs i`。

具体打包时只需要三项数据：

- `hj0 : j ≠ 0`；
- `hk0 : k ≠ 0`；
- `hh.symm : j^4 + k^4 = i^2`。

这一步是下降构造和“最小反例”接口真正接上的地方；没有 `hic'`，后面的严格不等式就无法转化成矛盾。

##### `strict natAbs descent hic`

接下来必须证明新解的第三坐标严格更小，也就是

`hic : Int.natAbs i < Int.natAbs c`。

Lean 的收束链非常干净，完全沿着下面这一行展开：

`Int.natAbs i ≤ i^2 = m ≤ m^2 < m^2 + n^2 = c = Int.natAbs c`。

每一段的来源都很明确：

- `Int.natAbs i ≤ i^2` 用的是 `Int.natAbs_le_self_sq i`。
- `i^2 = m` 用的是 `hi`。
- `m ≤ m^2` 用的是 `Int.le_self_sq m`。
- `m^2 < m^2 + n^2` 用的是 `hn : n ≠ 0`，因为这保证 `n^2 > 0`。
- `m^2 + n^2 = c` 用的是第一轮参数化的 `ht3`。
- `Int.natAbs c = c` 用的是 `hc : 0 < c`。

这里最值得强调的一点是：真正制造严格降链的不是 `hi` 也不是 `ht3`，而是 `hn : n ≠ 0`。
如果只知道 `c = m^2 + n^2` 而不知道 `n ≠ 0`，那么最多只能得到 `m^2 ≤ c`，无法推出严格更小。

因此，`hic` 的数学内容可以概括为：
新解的“斜边”是 `i`，而旧解的“斜边”是 `c`；因为旧解中还保留了一个额外的非零平方项 `n^2`，所以 `c` 必然严格大于 `i`。

##### `final contradiction`

两条不等式已经同时到手：

- 由最小性得到 `hic' : Int.natAbs c ≤ Int.natAbs i`；
- 由显式大小比较得到 `hic : Int.natAbs i < Int.natAbs c`。

把它们连起来就是

`Int.natAbs i < Int.natAbs c ≤ Int.natAbs i`，

这显然不可能。
Lean 的写法是

`apply absurd (not_le_of_gt hic) (not_not.mpr hic')`。

因此 `Fermat42.not_minimal` 收束：所谓“最小反例”无法存在。
这就是 `n = 4` 分支无限递降的最后一步，也是本 unit 需要关闭的唯一局部任务。

#### Local Budget Ledger
本 unit 的局部预算总步数为 `19`，满足 `<=100` 的要求。

| canonical subitem | step range |
|---|---:|
| `sign-normalized fourth-power witnesses` | `1-5` |
| `new witness equation hh` | `6-9` |
| `minimality re-instantiation hic'` | `10` |
| `strict natAbs descent hic` | `11-18` |
| `final contradiction` | `19` |

1. 固定本单元可用的前置接口：`h, hc, ht3, hi, htt3, hj, hk, hn`。
2. 由 `hj` 把 `r` 的“带符号平方”见证提升为四次方等式 `hj2 : r^2 = j^4`。
3. 由 `hk` 把 `s` 的“带符号平方”见证提升为四次方等式 `hk2 : s^2 = k^4`。
4. 由前一层的乘积非零结论排除 `j = 0`，得到 `hj0 : j ≠ 0`。
5. 同理排除 `k = 0`，得到 `hk0 : k ≠ 0`。
6. 用 `hi` 把 `m` 改写成 `i^2`。
7. 用 `htt3` 把同一个 `m` 改写成 `r^2 + s^2`。
8. 再用 `hj2`、`hk2` 把 `r^2 + s^2` 改写成 `j^4 + k^4`，得到 `hh : i^2 = j^4 + k^4`。
9. 把 `hh` 翻转成 `hh.symm`，使其符合 `Fermat42 j k i` 的方程方向。
10. 把 `hj0`、`hk0`、`hh.symm` 送入最小性接口 `h.2`，得到 `hic' : Int.natAbs c ≤ Int.natAbs i`。
11. 由 `hc : 0 < c` 把目标右端改写成 `Int.natAbs c = c`。
12. 用 `Int.natAbs_le_self_sq i` 得到 `Int.natAbs i ≤ i^2`。
13. 用 `hi` 把上一步右端改写成 `m`。
14. 用 `Int.le_self_sq m` 继续得到 `m ≤ m^2`。
15. 用 `hn : n ≠ 0` 推出 `n^2 > 0`。
16. 从上一步得到严格不等式 `m^2 < m^2 + n^2`。
17. 用 `ht3` 把 `m^2 + n^2` 改写成 `c`。
18. 合并第 `11-17` 步，收束为 `hic : Int.natAbs i < Int.natAbs c`。
19. 把 `hic` 与 `hic'` 组合成 `Int.natAbs i < Int.natAbs c ≤ Int.natAbs i` 的不可能链，推出矛盾并关闭本 unit。
<!-- HR18_N4_MERGED_END -->
