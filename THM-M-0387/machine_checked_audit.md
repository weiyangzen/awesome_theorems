# THM-M-0387 机器证明审计

本文件聚焦：

> 已 machine-checked 的具体是什么？

## statement / reduction 层

来源：`Mathlib/NumberTheory/FLT/Basic.lean`

| theorem / object | 数学作用 | 当前状态 |
|---|---|---|
| `FermatLastTheoremWith` | 一般半环上固定指数陈述 | 已 machine-checked |
| `FermatLastTheoremFor` | 自然数上的固定指数陈述 | 已 machine-checked |
| `FermatLastTheorem` | 总陈述：所有 `n ≥ 3` | 已 machine-checked |
| `FermatLastTheoremWith.mono` | 指数整除约化 | 已 machine-checked |
| `fermatLastTheoremWith_nat_int_rat_tfae` | `ℕ/ℤ/ℚ` 三版本等价 | 已 machine-checked |
| `fermatLastTheoremFor_iff_int` | 切到整数版本 | 已 machine-checked |
| `fermatLastTheoremFor_iff_rat` | 切到有理数版本 | 已 machine-checked |
| `fermatLastTheoremWith_of_fermatLastTheoremWith_coprime` | 约化到 primitive solution | 已 machine-checked |
| `dvd_c_of_prime_of_dvd_a_of_dvd_b_of_FLT` | 整除传播工具 | 已 machine-checked |
| `isCoprime_of_gcd_eq_one_of_FLT` | `gcd = 1` 到互素 | 已 machine-checked |

## `n = 4`

来源：`Mathlib/NumberTheory/FLT/Four.lean`

| theorem / object | 数学作用 | 当前状态 |
|---|---|---|
| `Fermat42` | 把问题改写成 `a^4 + b^4 = c^2` | 已 machine-checked |
| `Fermat42.exists_minimal` | 构造最小反例 | 已 machine-checked |
| `Fermat42.coprime_of_minimal` | 最小反例互素 | 已 machine-checked |
| `Fermat42.exists_odd_minimal` | parity 规整 | 已 machine-checked |
| `Fermat42.exists_pos_odd_minimal` | 规整到奇 + 正 | 已 machine-checked |
| `Fermat42.not_minimal` | 构造更小反例并矛盾 | 已 machine-checked |
| `not_fermat_42` | 排除 bridge problem | 已 machine-checked |
| `fermatLastTheoremFour` | 指数 `4` 的最终结论 | 已 machine-checked |

## `n = 3`

来源：`Mathlib/NumberTheory/FLT/Three.lean`

| theorem / object | 数学作用 | 当前状态 |
|---|---|---|
| `fermatLastTheoremThree_case_1` | mod `9` 排除 `3 ∤ abc` | 已 machine-checked |
| `fermatLastTheoremThree_of_three_dvd_only_c` | 规整到 `3 ∣ c` 而 `3 ∤ a,b` | 已 machine-checked |
| `FermatLastTheoremForThreeGen` | generalized equation | 已 machine-checked |
| `Solution'` / `Solution` | 下降对象 | 已 machine-checked |
| `exists_Solution_of_Solution'` | `Solution' → Solution` | 已 machine-checked |
| `Solution'_descent` | 下降构造 | 已 machine-checked |
| `exists_Solution_multiplicity_lt` | 重数严格下降 | 已 machine-checked |
| `fermatLastTheoremThree` | 指数 `3` 的最终结论 | 已 machine-checked |

## regular primes

来源：`flt-regular`

| theorem / object | 数学作用 | 当前状态 |
|---|---|---|
| `IsRegularPrime` | regular prime 定义 | 已 machine-checked |
| `isPrincipal_of_isPrincipal_pow_of_coprime` | ideal principalization engine | 已 machine-checked |
| `MayAssume.coprime` | primitive solution 规整 | 已 machine-checked |
| `a_not_cong_b` | Case I 坏同余规整 | 已 machine-checked |
| `caseI` | `p ∤ abc` 分支 | 已 machine-checked |
| `caseII` | `p ∣ abc` 分支 | 已 machine-checked |
| `flt_regular` | regular primes 总结论 | 已 machine-checked |
