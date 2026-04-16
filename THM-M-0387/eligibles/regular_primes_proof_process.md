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
> principal 让线性因子变成单位乘立方，
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
