# THM-M-0387 证明过程审计

本文件聚焦：

> 已 machine-checked 的这些分支，证明过程各自是怎么走的？

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

## `n = 3` 过程表

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

## 为什么这三张表是范本

未来其他旗舰条目可以直接复用这三类 process table：

1. 初等特例 + 最小反例下降
2. generalized equation + structured descent
3. intermediate generalization + branch split

只要把“步骤 / theorem / 数学作用 / 结果”填全，条目就不会虚。
