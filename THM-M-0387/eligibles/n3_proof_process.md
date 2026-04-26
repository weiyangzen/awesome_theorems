# THM-M-0387 `n = 3` 证明过程展开稿

## 1. 目标

这里解释的是 `mathlib` 中 `fermatLastTheoremThree` 的证明过程。

本文件保持为 `n = 3` 的单独可读分支；它不是 `FLT-HR-001` 到 `FLT-HR-018` 这 `18` 个 execution unit 的公开合并目标，也不参与该自动展开闸门。
公开归档只指向本 tracked Markdown 主稿，不指向临时运行结果目录或自动化工作副本路径。

默认读者基线是“大学水平、已掌握初等数论常识”。
所以像 `互素`、`整除`、基础模算术整理这种显然预备步骤，
这里只在它们真正决定 proof branch 时提及，不做教学化细拆。

目标命题是：

> 不存在非零整数解满足 `a^3 + b^3 = c^3`。

这条证明和 `n = 4` 很不一样。

`n = 4` 的核心是两次 primitive Pythagorean triple 参数化；  
`n = 3` 的核心则是：

1. 先用模 `9` 处理初等分支；
2. 再把剩余情形搬到 Eisenstein 整数环 `ℤ[ζ₃]`；
3. 最后对 `λ = ζ₃ - 1` 的重数做严格下降。

## 2. 对应的 formal 入口

主要对象都在 `Mathlib/NumberTheory/FLT/Three.lean`：

- `fermatLastTheoremThree_case_1`
- `fermatLastTheoremThree_of_three_dvd_only_c`
- `FermatLastTheoremForThreeGen`
- `Solution'`
- `Solution`
- `exists_Solution_of_Solution'`
- `Solution.exists_minimal`
- `Solution'_descent`
- `exists_Solution_multiplicity_lt`
- `fermatLastTheoremThree`

这条链的逻辑是：

1. 初等分支先关掉；
2. 一般分支规整成“只有 `c` 被 `3` 整除”的情形；
3. 引入 generalized equation；
4. 把解对象类型化；
5. 在 `λ`-重数上做下降；
6. 得到矛盾。

## 3. 全局路线

整条证明可以分成四层。

### 第一层：Case 1，直接做模 `9`

若 `3 ∤ abc`，则每个非零立方模 `9` 都只能是 `1` 或 `8`。

而两个 `{1, 8}` 中元素之和，不可能再等于某个非零立方模 `9` 的值。

所以 `3 ∤ abc` 的情形根本不可能发生。

### 第二层：把剩余情形规整到“只有 `c` 被 `3` 整除”

一旦 `3 | abc`，再结合互素性和对称性，可把问题规整成：

- `3 ∤ a`
- `3 ∤ b`
- `3 | c`
- `a` 与 `b` 互素

这就是后面 Eisenstein 整数下降真正使用的入口条件。

### 第三层：把方程改写成 generalized equation

进入 `ℤ[ζ₃]` 后，最好研究的不是

`a^3 + b^3 = c^3`

而是

`a^3 + b^3 = u * c^3`

其中 `u` 是单位。

原因不是“为了显得一般”，而是下降构造时单位因子无法被稳定控制；
如果不把单位显式写进陈述，下降会在类型层直接断掉。

### 第四层：对 `λ = ζ₃ - 1` 的重数做下降

定义一个适合下降的解对象，
再定义 `λ` 在 `c` 中的重数 `ν_λ(c)`，
然后证明：

- 任意这样的解都能转化为一个更规范的解；
- 对规范解可以显式构造出一个新的解，
  其 `ν_λ(c)` 严格更小。

于是最小重数解不可能存在，原方程无解。

## 4. 第一步：Case 1 的模 `9` 论证

`fermatLastTheoremThree_case_1` formalize 的就是最经典那段分析。

先看整数 `n` 在模 `9` 下的立方：

- 若 `3 | n`，那 `n^3 ≡ 0 (mod 9)`；
- 若 `3 ∤ n`，则 `n^3 ≡ 1` 或 `8 (mod 9)`。

后者由：

- `cube_of_castHom_ne_zero`
- `cube_of_not_dvd`

两步封装出来。

于是若 `3 ∤ abc`，那么：

- `a^3 mod 9` 属于 `{1, 8}`
- `b^3 mod 9` 属于 `{1, 8}`
- `c^3 mod 9` 也属于 `{1, 8}`

但 `{1, 8}` 中两个数相加：

- `1 + 1 = 2`
- `1 + 8 = 0`
- `8 + 8 = 7`

没有一个等于 `1` 或 `8`。

所以 `a^3 + b^3 = c^3` 不可能成立。

这关掉了所谓的 first case：

> `3 ∤ abc` 的情形根本无解。

## 5. 第二步：为什么可以规整成“只有 `c` 被 `3` 整除”

formal proof 接下来做的是把所有剩余情况都压缩到一个标准入口。

相关引理包括：

- `three_dvd_b_of_dvd_a_of_gcd_eq_one_of_case2`
- `fermatLastTheoremThree_of_dvd_a_of_gcd_eq_one_of_case2`
- `fermatLastTheoremThree_of_three_dvd_only_c`

数学上在做的事情是：

1. 先用 `FLT.Basic` 层现成的 reduction，把问题规整到 primitive solution。
2. 由于 primitive solution 中三者 gcd 为 `1`，`3` 不可能同时整除两项以上。
3. 再利用方程本身和整除传播，证明如果 `3` 整除了 `a` 或 `b`，就会逼出不允许的公共因子结构。
4. 因此，经过对称交换后，可以固定在：
   `3 | c`，但 `3 ∤ a,b`。

这一步的重要性在于：

- 此后，`3` 的全部 ramification 信息都被集中到 `c` 上；
- 在 Eisenstein 整数里，这会被翻译成：
  `λ = ζ₃ - 1` 整除 `c`，但不整除 `a,b`。

## 6. 第三步：为什么要进入 `ℤ[ζ₃]`

在普通整数环里，

`a^3 + b^3 = (a + b)(a^2 - ab + b^2)`

这个分解还不够细。

在 Eisenstein 整数环 `ℤ[ζ₃]` 中，它可以裂成三线性因子：

`a^3 + b^3 = (a + b)(a + ζ₃ b)(a + ζ₃^2 b)`

这就是 formal proof 中

- `a_cube_add_b_cube_eq_mul`

背后的几何结构。

但一旦进入这个环，就马上会遇到单位问题：

- 三个因子并不一定本身就是立方；
- 更常见的情形是“单位乘以立方”。

所以 formalization 不去硬逼

`a^3 + b^3 = c^3`

而是从一开始就允许

`a^3 + b^3 = u * c^3`

其中 `u` 是单位。

这就是：

- `FermatLastTheoremForThreeGen`

的意义。

## 7. 第四步：`Solution'` 与 `Solution` 的角色

### 7.1 `Solution'`

`Solution'` 表示 generalized equation 的一个“可下降候选解”，它记录：

- `a`
- `b`
- `c`
- 单位 `u`
- `¬ λ ∣ a`
- `¬ λ ∣ b`
- `λ ∣ c`
- `c ≠ 0`
- `IsCoprime a b`
- 方程 `a^3 + b^3 = u * c^3`

可以把它理解为：

> 已经经过 primitive reduction 的标准化输入。

### 7.2 `Solution`

`Solution` 比 `Solution'` 多一个关键条件：

`λ^2 ∣ a + b`

这不是随手附加的技术条件，而是下降构造真正需要的入口。

一旦这个条件成立，就能把三个线性因子中关于 `λ` 的信息精确拆出来，
从而定义新的 `x, y, z` 并做 multiplicity descent。

## 8. 第五步：从 `Solution'` 变成 `Solution`

这一步对应：

- `lambda_sq_dvd_or_dvd_or_dvd`
- `ex_cube_add_cube_eq_and_isCoprime_and_not_dvd_and_dvd`
- `exists_Solution_of_Solution'`

数学上在做的事情是：

1. 证明在三个线性因子
   `a + b`、`a + ηb`、`a + η^2 b`
   里，至少有一个被 `λ^2` 整除。
2. 如果恰好是 `a + b`，那最好，直接满足 `Solution` 的额外条件。
3. 如果是 `a + ηb` 或 `a + η^2 b`，就把 `b` 乘上适当单位 `η` 或 `η^2`，
   重新组织方程。

这样做有两个效果：

- 方程的“形状”不变，仍是 `a'^3 + b'^3 = u * c^3`；
- `c` 不变，所以 `λ` 在 `c` 中的重数也不变；
- 但新的 `(a', b')` 已满足 `λ^2 | a' + b'`。

因此：

> 任意 `Solution'` 都能被转成一个 `Solution`，且不增加下降量。

这正是 `exists_Solution_of_Solution'` 的内容。

## 9. 第六步：把下降量显式做成 `λ` 的重数

formal proof 选的下降量不是某个“大小”，而是

`ν_λ(c)`

也就是 `λ = ζ₃ - 1` 在 `c` 中的 multiplicity。

对应定义是：

- `Solution'.multiplicity`
- `Solution.multiplicity`

并先证明：

- 该重数是有限的；
- 实际上至少为 `2`。

为什么至少为 `2`？

因为从 generalized equation 以及对 `a^3`、`b^3` 模 `λ^4` 的分析，
可以推出：

- `λ^4 | c^3`
- 从而 `λ^2 | c`

这一步在源码里对应：

- `a_cube_b_cube_congr_one_or_neg_one`
- `lambda_pow_four_dvd_c_cube`
- `lambda_sq_dvd_c`
- `Solution'.two_le_multiplicity`

## 10. 第七步：给 `Solution` 构造新的分解变量

固定一个 `Solution S`，记其 multiplicity 为 `m`。

formal proof 接着定义：

- `y`，使得 `a + ηb = λ y`
- `z`，使得 `a + η^2 b = λ z`
- `x`，使得 `a + b = λ^(3m - 2) x`
- `w`，使得 `c = λ^m w`

对应定义和性质有：

- `y`, `y_spec`
- `z`, `z_spec`
- `x`, `x_spec`
- `w`, `w_spec`

这些对象并不是“装饰性换元”，而是把方程三因子中的 `λ` 幂次显式剥离出来。

剥离以后，剩余部分 `x, y, z, w` 必须满足更刚性的互素与不可整除条件。

特别是：

- `λ ∤ y`
- `λ ∤ z`
- `λ ∤ x`
- `λ ∤ w`

这些性质确保下一步不会把下降量又偷偷吃回去。

## 11. 第八步：证明 `x, y, z` 两两互素

formal proof 在这里做的，是把“共同素因子”问题全部压到 `λ` 上。

核心思路是：

1. 若某个素元 `p` 同时整除两个线性因子，
   例如同时整除 `a + b` 和 `a + ηb`，
   那么可用线性组合消去 `a`、`b`，
   推出 `p` 必与 `λ` 相关联。
2. 但我们又已经证明 `x, y, z` 不被 `λ` 整除。
3. 因而 `x, y, z` 之间不可能有非平凡公共素因子。

对应 formal 结果包括：

- `associated_of_dvd_a_add_b_of_dvd_a_add_eta_mul_b`
- `associated_of_dvd_a_add_b_of_dvd_a_add_eta_sq_mul_b`
- `associated_of_dvd_a_add_eta_mul_b_of_dvd_a_add_eta_sq_mul_b`
- `isCoprime_x_y`
- `isCoprime_x_z`
- `isCoprime_y_z`

这一步对下降非常关键，因为下一步要从

`x * y * z = unit * w^3`

推出“每一项本身都是 cube up to unit”。

若没有两两互素性，这一步是不成立的。

## 12. 第九步：把 `x, y, z` 分别写成“单位 × 立方”

这一步对应：

- `x_mul_y_mul_z_eq_u_mul_w_cube`
- `exists_cube_associated`
- `X`, `Y`, `Z`
- `u₁`, `u₂`, `u₃`

逻辑是：

1. 由前面展开过的三因子分解，可以整理出
   `x * y * z = unit * w^3`。
2. 由于 `x, y, z` 两两互素，
   所以每一项都必须“单独长得像立方”，
   即：
   - `x = X^3 * u₁`
   - `y = Y^3 * u₂`
   - `z = Z^3 * u₃`
   其中 `u₁,u₂,u₃` 都是单位。

这一步的作用，是把原方程彻底压缩成三个新变量 `X,Y,Z`，
并把全部非立方噪声都集中到少数单位 `u_i` 上。

## 13. 第十步：构造新的 generalized equation

接下来 formal proof 做一串显式代数计算，得到：

`Y^3 + u₄ * Z^3 = u₅ * (λ^(m-1) * X)^3`

这里：

- `u₄`
- `u₅`

是由前面那些单位组合出来的新单位。

对应公式链包括：

- `formula1`
- `formula2`
- `formula3`

如果只看纸面证明，这里很容易被写成一句“经整理得”。
但在 formal proof 里，这一段实际上是 descent 最难看的算式核心之一。

## 14. 第十一步：为什么 `u₄` 可以被压成 `±1`

这是整条 `n = 3` 证明最像“Kummer 型引理”的位置。

对应 formal 结果：

- `u₄_eq_one_or_neg_one`
- `u₄_sq`

它依赖源码开头特别点出的结果：

`IsCyclotomicExtension.Rat.Three.eq_one_or_neg_one_of_unit_of_congruent`

直观上，这一步在说：

- `u₄` 不是任意单位；
- 它满足很强的 `λ`-进同余约束；
- 在 `p = 3` 这条特殊分支中，这个约束足够强，能把 `u₄` 压成 `1` 或 `-1`。

一旦 `u₄ = ±1`，就可以把符号吸进立方项，得到与原始 generalized equation 同型的新方程。

## 15. 第十二步：严格下降

定义新的 `Solution'`：

- 新的 `a` 取 `Y`
- 新的 `b` 取 `u₄ * Z`
- 新的 `c` 取 `λ^(m-1) * X`

这就是：

- `Solution'_descent`

接着 formal proof 证明：

- 新解仍满足 generalized equation 所需的全部约束；
- 且新解的 multiplicity 恰好是原来的 `m - 1`。

这对应：

- `Solution'_descent_multiplicity`
- `Solution'_descent_multiplicity_lt`

然后再用

- `exists_Solution_of_Solution'`

把它重新规整回 `Solution`。

于是得到：

> 若存在一个 `Solution`，就存在另一个 multiplicity 更小的 `Solution`。

这正是：

- `exists_Solution_multiplicity_lt`

## 16. 第十三步：最小重数解不可能存在

一旦已经能做严格下降，
就像 `n = 4` 一样，可以取一个最小反例，
只不过最小量不再是 `|c|`，而是 `ν_λ(c)`。

对应 formal 结果：

- `Solution.exists_minimal`

于是：

1. 假设存在 `Solution`；
2. 取最小 multiplicity 的那个；
3. 再由 `exists_Solution_multiplicity_lt` 造出更小的；
4. 矛盾。

故 `Solution` 不存在。

再由：

- `FermatLastTheoremForThree_of_FermatLastTheoremThreeGen`

把 generalized equation 的无解性推回普通 FLT(3)。

这就是最终的：

- `fermatLastTheoremThree`

## 17. 这条证明的真正难点是什么

`n = 3` 的证明最容易被误解成一句：

> 去 Eisenstein 整数里做 descent。

但对 formalization 来说，真正的重活是：

1. 先把初等 case 彻底关掉；
2. 精确定义 generalized equation；
3. 把“可下降的解”做成结构体 `Solution'` / `Solution`；
4. 选出真正可下降的量：`ν_λ(c)`；
5. 把三线性因子的 `λ` 幂次精确剥离；
6. 证明剩余因子两两互素；
7. 证明它们分别是 cube up to unit；
8. 处理关键单位 `u₄`；
9. 构造严格下降。

所以这不是一句“在分圆域里做递降”，而是一整套：

> generalized equation + typed solution objects + λ-adic multiplicity descent

## 18. 与 formal theorem 的一一对应

| 数学步骤 | 对应 formal 对象 |
|---|---|
| Case 1 模 `9` | `fermatLastTheoremThree_case_1` |
| 约化到 `3 | c`, `3 ∤ a,b` | `fermatLastTheoremThree_of_three_dvd_only_c` |
| generalized equation | `FermatLastTheoremForThreeGen` |
| 下降输入对象 | `Solution'`, `Solution` |
| `Solution' → Solution` | `exists_Solution_of_Solution'` |
| 最小重数解 | `Solution.exists_minimal` |
| 显式下降构造 | `Solution'_descent` |
| 严格下降 | `exists_Solution_multiplicity_lt` |
| 回到 FLT(3) | `fermatLastTheoremThree` |

## 19. 阅读建议

如果你想真正把 `n = 3` 看懂，建议顺序是：

1. 先读本稿。
2. 再读 [`../process_audit.md`](../process_audit.md) 里的 `n = 3` 过程表。
3. 然后直接对照 `Three.lean` 中：
   - `Solution'`
   - `Solution`
   - `exists_Solution_of_Solution'`
   - `Solution'_descent`

因为这四块正是整条 formal proof 的骨架。
