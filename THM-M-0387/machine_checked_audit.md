# THM-M-0387 机器证明审计

本文件聚焦：

> 已 machine-checked 的具体是什么？

## exact source and revision evidence

本仓库本地 Lean 工程在 `Formalizations/Lean/lake-manifest.json` 中固定
`mathlib` source project 为 `leanprover-community/mathlib4`，revision 为
`8a178386ffc0f5fef0b77738bb5449d50efeea95`；`Formalizations/Lean/lakefile.lean`
使用同一 revision。下面所有 mathlib machine-checked claim 均按这个 revision
解释。regular primes 的 theorem closure 属于上游 source project
`leanprover-community/flt-regular`；本仓库没有 vendoring 该证明本体。

| claim family | theorem / declaration names | Lean module | source project | repository-local role |
|---|---|---|---|---|
| statement objects | `FermatLastTheoremWith`, `FermatLastTheoremFor`, `FermatLastTheorem` | `Mathlib.NumberTheory.FLT.Basic` | `leanprover-community/mathlib4` @ `8a178386ffc0f5fef0b77738bb5449d50efeea95` | imported API only |
| reduction lemmas | `FermatLastTheoremWith.mono`, `FermatLastTheoremFor.mono`, `FermatLastTheorem.of_odd_primes`, `fermatLastTheoremWith_nat_int_rat_tfae`, `fermatLastTheoremFor_iff_int`, `fermatLastTheoremFor_iff_rat`, `fermatLastTheoremWith_of_fermatLastTheoremWith_coprime`, `dvd_c_of_prime_of_dvd_a_of_dvd_b_of_FLT`, `isCoprime_of_gcd_eq_one_of_FLT` | `Mathlib.NumberTheory.FLT.Basic` | `leanprover-community/mathlib4` @ `8a178386ffc0f5fef0b77738bb5449d50efeea95` | imported API and local examples |
| `n = 4` terminal theorem | `fermatLastTheoremFour` | `Mathlib.NumberTheory.FLT.Four` | `leanprover-community/mathlib4` @ `8a178386ffc0f5fef0b77738bb5449d50efeea95` | wrapped by repo-local `flt4Path` |
| `n = 4` local wrappers | `flt4Path`, `flt4IntPath`, `flt8ViaFlt4Path` | `AwesomeTheorems.NumberTheory.THM_M_0387.FLT4Path` | this repository, importing `Mathlib.NumberTheory.FLT.Four` | repo-local wrapper / derived-wrapper records |
| `n = 3` terminal theorem | `fermatLastTheoremThree` | `Mathlib.NumberTheory.FLT.Three` | `leanprover-community/mathlib4` @ `8a178386ffc0f5fef0b77738bb5449d50efeea95` | wrapped by repo-local `flt3Path` |
| `n = 3` local wrapper | `flt3Path` | `AwesomeTheorems.NumberTheory.THM_M_0387.FLT3Path` | this repository, importing `Mathlib.NumberTheory.FLT.Three` | repo-local wrapper record |
| regular primes anchor | `regularPrimesStatementShape`, `regularPrimesPathModules`, `regularPrimesPathTerminalTheorem` | `AwesomeTheorems.NumberTheory.THM_M_0387.RegularPrimesPath` | this repository, importing only mathlib statement support | anchor-only statement/module/theorem-name record |
| regular primes upstream theorem closure | `flt_regular` and supporting hooks named below | `FltRegular.FltRegular` plus the listed `FltRegular/...` modules | `leanprover-community/flt-regular` | upstream-only theorem closure; no repo-local vendored proof |

The exact mathlib modules for `FermatLastTheoremFor`, `FermatLastTheorem`, and
the reduction lemmas are therefore all `Mathlib.NumberTheory.FLT.Basic` at
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
The exact mathlib module for `fermatLastTheoremFour` is
`Mathlib.NumberTheory.FLT.Four`; local source inspection of the vendored
mathlib mirror records the declaration at
`/Users/wangweiyang/GitHub/awesome_theorems/Formalizations/Lean/.vendor/mathlib4/Mathlib/NumberTheory/FLT/Four.lean:266`.
The exact mathlib module for `fermatLastTheoremThree` is
`Mathlib.NumberTheory.FLT.Three`; local source inspection of the vendored
mathlib mirror records the terminal declaration at
`/Users/wangweiyang/GitHub/awesome_theorems/Formalizations/Lean/.vendor/mathlib4/Mathlib/NumberTheory/FLT/Three.lean:750`.

For regular primes, the upstream source reference used by this dossier is
`https://github.com/leanprover-community/flt-regular`.  On `2026-04-24`,
`git ls-remote https://github.com/leanprover-community/flt-regular.git HEAD refs/heads/master`
returned `0ba4fc22e1742623c3923c5a7a1eb7df36d01b10` for both `HEAD` and
`refs/heads/master`; this is source-identification evidence only, not a
repo-local vendored dependency.  The regular-primes setup is realized upstream
in `FltRegular/NumberTheory/RegularPrimes.lean`, with declaration anchors
`IsRegularNumber`, `IsRegularPrime`, and
`isPrincipal_of_isPrincipal_pow_of_coprime`.  The MayAssume layer is realized
upstream in `FltRegular/MayAssume/Lemmas.lean`, with declaration anchors
`MayAssume.coprime`, `MayAssume.p_dvd_c_of_ab_of_anegc`, and `a_not_cong_b`.
Case I is realized upstream in `FltRegular/CaseI/Statement.lean`, supported by
`FltRegular/CaseI/AuxLemmas.lean`, with declaration anchors
`CaseI.SlightlyEasier`, `CaseI.Statement`, `CaseI.may_assume`,
`CaseI.ab_coprime`, `CaseI.exists_ideal`, `CaseI.is_principal`,
`CaseI.caseI_easier`, and `CaseI.caseI`.
Case II is realized upstream in `FltRegular/CaseII/Statement.lean` and
`FltRegular/CaseII/InductionStep.lean`, supported by
`FltRegular/CaseII/AuxLemmas.lean`.  The Case II terminal declaration anchors
in `FltRegular.CaseII.Statement` are `not_exists_solution`,
`not_exists_solution'`, `not_exists_Int_solution`,
`not_exists_Int_solution'`, and `caseII`; the descent and ideal-factor anchors
in `FltRegular.CaseII.InductionStep` include `zeta_sub_one_dvd`,
`span_pow_add_pow_eq`, `div_one_sub_zeta_mem`,
`div_zeta_sub_one_Bijective`, `prod_c`, `exists_ideal_pow_eq_c`,
`root_div_zeta_sub_one_dvd_gcd_spec`, `c_div_principal`, `p_dvd_c_iff`,
`p_dvd_a_iff`, `p_pow_dvd_c_eta_zero`, `p_pow_dvd_a_eta_zero`,
`exists_solution`, and `exists_solution'`.  The exact upstream terminal theorem
declaration for regular primes is in `FltRegular/FltRegular.lean` as
`theorem flt_regular {p : ℕ} [Fact p.Prime] (hreg : IsRegularPrime p) (hodd : p ≠ 2) : FermatLastTheoremFor p`.
This repository records the upstream module names and the `2026-04-24`
`git ls-remote` result, but it does not pin `leanprover-community/flt-regular`
by vendored commit, release tag, or lockfile.  TODO before stronger
reproducibility claims: add a reproducible commit or release pin for upstream
`flt-regular` and record the matching dependency state.

## statement / reduction 层

来源：source project `leanprover-community/mathlib4`，module
`Mathlib.NumberTheory.FLT.Basic`，revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`。

| theorem / object | 数学作用 | 状态 |
|---|---|---|
| `FermatLastTheoremWith` | 一般半环上固定指数陈述 | 已 machine-checked |
| `FermatLastTheoremFor` | 自然数上的固定指数陈述 | 已 machine-checked |
| `FermatLastTheorem` | 总陈述：所有 `n ≥ 3` | 已 machine-checked |
| `FermatLastTheoremWith.mono` | 指数整除约化 | 已 machine-checked |
| `FermatLastTheoremFor.mono` | 自然数版本的指数整除约化 | 已 machine-checked |
| `FermatLastTheorem.of_odd_primes` | 由 `n = 4` 与所有奇素数指数拼回总 FLT | 已 machine-checked |
| `fermatLastTheoremWith_nat_int_rat_tfae` | `ℕ/ℤ/ℚ` 三版本等价 | 已 machine-checked |
| `fermatLastTheoremFor_iff_int` | 切到整数版本 | 已 machine-checked |
| `fermatLastTheoremFor_iff_rat` | 切到有理数版本 | 已 machine-checked |
| `fermatLastTheoremWith_of_fermatLastTheoremWith_coprime` | 约化到 primitive solution | 已 machine-checked |
| `dvd_c_of_prime_of_dvd_a_of_dvd_b_of_FLT` | 整除传播工具 | 已 machine-checked |
| `isCoprime_of_gcd_eq_one_of_FLT` | `gcd = 1` 到互素 | 已 machine-checked |

这层已经足以解释为什么 `4` 以上非素数指数不单列成独立 branch：

1. 若 `4 ∣ n`，则由 `FermatLastTheoremFor.mono`，`n = 4` 直接推出指数 `n`。
2. 若 `4 ∤ n` 但 `n` 是合数且 `n > 2`，则存在奇素数 `p ∣ n`，由指数 `p` 推指数 `n`。

因此，`6, 8, 9, 10, 12, ...` 都被 statement / reduction 层吸收，而不是遗漏。

Repository-local boundary: this repository does not contain a repo-local
machine-checked proof of the full theorem `FermatLastTheorem`.  The local
sample only records mathlib statement/reduction APIs and wrappers around
special exponents; the full FLT proof chain is not vendored or closed as a
repo-local theorem in this repository.

Local wrappers and upstream-only closure are separate layers: `flt4Path`,
`flt3Path`, `flt4IntPath`, and `flt8ViaFlt4Path` are repo-local wrappers,
while regular primes theorem closure remains upstream-only via `flt-regular`.

### machine-checked boundary summary

| branch / theorem | repo-local status | source boundary |
|---|---|---|
| `n = 4` / `flt4Path` | repo-local theorem-level closure is the wrapper theorem `flt4Path` | proof body is `fermatLastTheoremFour` imported from `Mathlib.NumberTheory.FLT.Four` |
| `n = 3` / `flt3Path` | repo-local theorem-level closure is the wrapper theorem `flt3Path` | proof body is `fermatLastTheoremThree` imported from `Mathlib.NumberTheory.FLT.Three` |
| `flt4IntPath` | repo-local derived wrapper | derived from the mathlib `FermatLastTheoremFor 4` / `FermatLastTheoremWith ℤ 4` equivalence, via `fermatLastTheoremFor_iff_int` |
| `flt8ViaFlt4Path` | repo-local derived wrapper | derived from `flt4Path` by `FermatLastTheoremFor.mono` and the exponent-divisibility witness `4 ∣ 8` |
| full `FermatLastTheorem` | not repo-local machine-checked in this repository | only statement/reduction APIs and examples are imported locally |
| regular primes / `flt_regular` | theorem closure is upstream, not vendored into this repository | repo-local material is anchor-only: statement shape, upstream module names, and terminal theorem-name record |

Local wrapper rows (`flt4Path`, `flt3Path`, `flt4IntPath`, `flt8ViaFlt4Path`) are repo-local theorem or derived-wrapper records backed by mathlib imports; the regular-primes row is different and records only upstream-only theorem closure plus repo-local anchor metadata, not a repo-local proof of `flt_regular`.

Source-of-truth note: this file is the canonical public surface for
machine-boundary evidence.  `process_audit.md`, `full_study.md`, `README.md`,
and the `eligibles/` files may restate the same boundary sentence for reader
orientation, but they do not create an independent or stronger machine-boundary
claim.

## `n = 4`

来源：source project `leanprover-community/mathlib4`，module
`Mathlib.NumberTheory.FLT.Four`，revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`。

| theorem / object | 数学作用 | 状态 |
|---|---|---|
| `Fermat42` | 把问题改写成 `a^4 + b^4 = c^2` | 已 machine-checked |
| `Fermat42.exists_minimal` | 构造最小反例 | 已 machine-checked |
| `Fermat42.coprime_of_minimal` | 最小反例互素 | 已 machine-checked |
| `Fermat42.exists_odd_minimal` | parity 规整 | 已 machine-checked |
| `Fermat42.exists_pos_odd_minimal` | 规整到奇 + 正 | 已 machine-checked |
| `Fermat42.not_minimal` | 构造更小反例并矛盾 | 已 machine-checked |
| `not_fermat_42` | 排除 bridge problem | 已 machine-checked |
| `fermatLastTheoremFour` | 指数 `4` 的最终结论 | 已 machine-checked |

### repository-local closure note for `n = 4`

`Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/FLT4Path.lean`
在本仓库共享源码树里导入 `Mathlib.NumberTheory.FLT.Four`，
并用 wrapper theorem `flt4Path : FermatLastTheoremFor 4 := fermatLastTheoremFour`
记录 `n = 4` 的 theorem-level closure；因此本仓库的 repo-local 闭合点是
`flt4Path`，证明实质来自 mathlib import。
同一模块还给出两个 repo-local 派生 wrapper：
`flt4IntPath : FermatLastTheoremWith ℤ 4` 由 mathlib 的
`fermatLastTheoremFor_iff_int` 等价推出；
`flt8ViaFlt4Path : FermatLastTheoremFor 8` 由
`FermatLastTheoremFor.mono` 和 `4 ∣ 8` 的指数整除单调性推出。
在本文件覆盖的机器审计层级内，
`n = 4` 这条 branch 的 canonical package、canonical high-risk leaf，
以及此前单列的 package-level subitem 都已完成独立 `<=100` proof-step ledger 整合。

### `n = 4` 再拆一层的机器节点

下面这张表不再只列 branch-level theorem，
而是把 `Fermat42.not_minimal` 内部真正承担证明工作的机器节点继续拆一层。
这里的行状态同时保留两层信息：
formal hook 本身对应的 theorem / lemma 来源是 machine-checked；
`bridge packaging` 到 `smaller-solution construction and size comparison`
这 `7` 个 canonical package 都已补齐独立 ledger，因此统一记为 `checked`。

| 节点包 | 真实 formal hook | 数学作用 | source / budget status |
|---|---|---|---|
| bridge packaging | `Fermat42`, `not_fermat_42`, `fermatLastTheoremFour` | FLT(4) 与桥梁方程之间来回切换 | source theorem machine-checked / budget `checked` |
| minimal normalization | `exists_minimal`, `coprime_of_minimal`, `exists_pos_odd_minimal` | 取得最小反例并规整到标准形态 | source theorem machine-checked / budget `checked` |
| first triple classification | `PythagoreanTriple.coprime_classification'` | 把 `(a^2, b^2, c)` 参数化为第一组 `(m, n)` | source theorem machine-checked / budget `checked` |
| second triple classification | `PythagoreanTriple.coprime_classification'` | 把 `(a, n, m)` 参数化为第二组 `(r, s)` | source theorem machine-checked / budget `checked` |
| coprimality bridge | `Int.isCoprime_of_sq_sum` / `Int.isCoprime_of_sq_sum'` | 建立 `m` 与 `r*s`、以及 `r` 与 `s` 的互素性接口 | source theorem machine-checked / budget `checked` |
| square extraction and sign cleanup | `Int.sq_of_gcd_eq_one`, `Or.resolve_right` + positivity side-conditions in `not_minimal` | 从 `b'^2 = m*(r*s)` 和互素性推出平方因子结构，并排除负平方假分支 | source theorem machine-checked / budget `checked` |
| smaller-solution construction and size comparison | `hh : i^2 = j^4 + k^4`, `hic`, `hic'` inside `not_minimal` | 把参数重新打包成新 `Fermat42` 解并证明其严格更小 | source theorem machine-checked / budget `checked` |

#### `n = 4` 再拆一层的 leaf ledger

以下 package / subpackage 名称已与 `process_audit.md`、`eligibles/n4_proof_process.md` 对齐；
审计口径：下表中的 `trace budget status` 同时作用于 package 本身及其所列 `one-more-depth` 子项；
已拥有独立 `<=100` proof-step ledger 的展开项记为 `checked`，
其余尚未逐条验证为 `<=100` 步 leaf proof 的展开项记为 `unchecked`。

| package | subpackages at one more depth | trace budget status |
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

1. `delta Fermat42`，把 bridge predicate 展开成 `a ≠ 0 ∧ b ≠ 0 ∧ a ^ 4 + b ^ 4 = c ^ 2`。
2. 因而 `Fermat42` 的机器作用只是把“两个非零条件 + quartic-to-square 方程”打包成单个下降入口。
3. 在 `not_fermat_42` 中，先假设 `h : a ^ 4 + b ^ 4 = c ^ 2`。
4. 用 `And.intro ha (And.intro hb h)` 把 `ha`、`hb`、`h` 组装成 `Fermat42 a b c` witness。
5. 对这个 witness 调用 `Fermat42.exists_pos_odd_minimal`。
6. 得到 `a0 b0 c0` 与 `hf : Minimal a0 b0 c0`、`h2 : a0 % 2 = 1`、`hp : 0 < c0`；这就完成了 normalized witness acquisition。
7. 把 `hf`、`h2`、`hp` 直接交给 `Fermat42.not_minimal`。
8. 该 theorem 返回 `False`，即最小规范化 witness 不可能存在。
9. 因而起始假设 `h` 被排除，收束为 `a ^ 4 + b ^ 4 ≠ c ^ 2`。
10. 在 `fermatLastTheoremFour` 中先用 `rw [fermatLastTheoremFor_iff_int]`，把自然数版本转成整数版本。
11. 于是只需对整数 `a b c` 及非零假设 `ha hb _`、方程 `heq : a ^ 4 + b ^ 4 = c ^ 4` 收束。
12. 调用 `@not_fermat_42 _ _ (c ^ 2) ha hb`，把桥梁命题的右端实例化成 `c ^ 2`。
13. 用 `rw [heq]; ring` 把输入方程改写成 `a ^ 4 + b ^ 4 = (c ^ 2) ^ 2`。
14. 因而 `not_fermat_42` 与 `heq` 矛盾，最终得到 `FermatLastTheoremFor 4`。

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

#### `n = 4` 独立 ledger 摘要

| package | total proof steps | descendant closure carried by the same ledger |
|---|---:|---|
| `first triple classification` | `33` | closes `raw coprime triple classification` |
| `second triple classification` | `13` | closes former package-level unresolved `Int.gcd a n = 1 transfer` |
| `coprimality bridge` | `12` | no extra canonical descendant beyond the package itself |
| `square extraction and sign cleanup` | `30` | closes `square extraction for r*s with sign cleanup` |
| `smaller-solution construction and size comparison` | `19` | closes `strict natAbs descent hic` |

跨文件统一的 canonical high-risk leaf 集中在：

1. `raw coprime triple classification`
2. `square extraction for r*s with sign cleanup`
3. `strict natAbs descent hic`

上述 `3` 个 canonical high-risk leaf 现都已随 matching package ledger
一并转为 `checked`；此前单列的
`Int.gcd a n = 1 transfer`
也已由 `second triple classification` 的独立 `13` 步 ledger 关闭，
因此不再保留 unresolved row。

#### `n = 4` 已继续深拆的高风险 leaf

以下高风险 leaf 及其 `one-more-depth` 子包都已由对应 package ledger 关闭，
因此统一记为 `checked`。

| leaf | one-more-depth items | trace budget status | 最高风险点 |
|---|---|---|---|
| `raw coprime triple classification` | `positive-z reduction`; `odd-leg dispatch by symmetry`; `zero-left degenerate branch`; `unit-circle rational parameter extraction`; `mixed-parity admissible reconstruction`; `forbidden parity branch elimination`; `raw tuple packaging` | `checked` | `closed` |
| `square extraction for r*s with sign cleanup` | `API orientation for extracting the second factor`; `raw signed-square witness for r*s`; `negative-branch rewrite to a nonpositive RHS`; `strict positivity of the square side`; `sign cleanup to a clean square equation` | `checked` | `closed` |
| `strict natAbs descent hic` | `natAbs target recast`; `left witness square bound`; `new-witness substitution`; `old-c expansion`; `strict gap from the residual square`; `transitive close` | `checked` | `closed` |

#### `n = 4` status ledger

`n = 4` 的 canonical package / high-risk leaf 命名同步，
已经与 `process_audit.md`、`eligibles/n4_proof_process.md` 三层材料保持一致。
`7` 个 canonical package 都已拥有独立 `<=100` proof-step ledger；
因此本节对应的 machine-trace `unchecked` surface 已经收束为 `0`。

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
`n = 4` 审计表中已无剩余 package-level unresolved subitem。

## `n = 3`

来源：source project `leanprover-community/mathlib4`，module
`Mathlib.NumberTheory.FLT.Three`，revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`。

| theorem / object | 数学作用 | 状态 |
|---|---|---|
| `fermatLastTheoremThree_case_1` | mod `9` 排除 `3 ∤ abc` | 已 machine-checked |
| `fermatLastTheoremThree_of_three_dvd_only_c` | 规整到 `3 ∣ c` 而 `3 ∤ a,b` | 已 machine-checked |
| `FermatLastTheoremForThreeGen` | generalized equation | 已 machine-checked |
| `Solution'` / `Solution` | 下降对象 | 已 machine-checked |
| `exists_Solution_of_Solution'` | `Solution' → Solution` | 已 machine-checked |
| `Solution'_descent` | 下降构造 | 已 machine-checked |
| `exists_Solution_multiplicity_lt` | 重数严格下降 | 已 machine-checked |
| `fermatLastTheoremThree` | 指数 `3` 的最终结论 | 已 machine-checked |

### repository-local closure note for `n = 3`

`Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/FLT3Path.lean`
在本仓库共享源码树里导入 `Mathlib.NumberTheory.FLT.Three`，
并用 wrapper theorem `flt3Path : FermatLastTheoremFor 3 := fermatLastTheoremThree`
记录 `n = 3` 的 theorem-level closure；因此本仓库的 repo-local 闭合点是
`flt3Path`，证明实质来自 mathlib import。

## regular primes

来源：source project `leanprover-community/flt-regular`。本仓库仅记录
`AwesomeTheorems.NumberTheory.THM_M_0387.RegularPrimesPath` anchor module；
上游 theorem closure 不属于本仓库 vendored code。

regular primes 的 theorem closure 来自上游 `flt-regular` 项目；
本仓库没有 vendoring 该证明本体，repo-local 内容只记录 statement shape、
上游 module 与 terminal theorem name 的锚点。

| theorem / object | 数学作用 | 状态 |
|---|---|---|
| `IsRegularPrime` | regular prime 定义 | 已 machine-checked |
| `isPrincipal_of_isPrincipal_pow_of_coprime` | ideal principalization engine | 已 machine-checked |
| `MayAssume.coprime` | primitive solution 规整 | 已 machine-checked |
| `a_not_cong_b` | Case I 坏同余规整 | 已 machine-checked |
| `caseI` | `p ∤ abc` 分支 | 已 machine-checked |
| `caseII` | `p ∣ abc` 分支 | 已 machine-checked |
| `flt_regular` | regular primes 总结论 | 已 machine-checked |

### repository-local boundary for `regular primes`

本节 theorem-level 结果来源于上游 `flt-regular`，
其 machine-checked closure 成立于上游项目。
本仓库内的
`Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/RegularPrimesPath.lean`
只是锚点模块：它记录 statement shape、上游模块路径与终端 theorem 名 `flt_regular`，
但并未在本仓库 vendoring 上游 `flt_regular` 证明本体。
It is statement-shape and upstream-anchor code, not a local proof of `flt_regular`.
具体 repo-local anchor-only 记录为
`regularPrimesStatementShape`、`regularPrimesPathModules`，
以及 `regularPrimesPathTerminalTheorem = "flt_regular"`。

因此这里需要同时保留三层口径：

- upstream theorem closure: yes
- repo-local vendored theorem closure: no, anchor-only
- repo-local anchor-only statement/module/theorem-name record: yes

Machine-trace boundary sentence fixed as:
`upstream theorem closure: yes / repo-local vendored theorem closure: no, anchor-only / repo-local anchor-only statement/module/theorem-name record: yes`

其中最后一段只表示锚点 statement/module/theorem-name 记录已到位，
不表示本仓库已 vendoring 上游 `flt_regular` 证明本体。

上游 theorem closure 与 repo-local anchor-only 边界已经固定；
在本文件覆盖的机器审计层级内，
regular primes 路线的 canonical package、canonical high-risk leaf，
以及此前单列的 package-level subitem 都已完成独立 `<=100` proof-step ledger 整合。

### regular primes 再拆一层的机器节点

这部分继续按 `MayAssume / Case I / Case II / merge` 往下压一层，
优先记录真正需要留痕的 theorem / lemma。
这里的行状态同样同时保留两层信息：
formal hook 本身对应的 theorem / lemma 来源是 machine-checked，
`setup`、`MayAssume`、Case I / Case II / merge 各层 package
均已补齐独立 ledger，因此统一记为 `checked`。

| 子层 | 真实 formal hook | 数学作用 | source / budget status |
|---|---|---|---|
| setup | `IsRegularPrime` | 定义 regularity | source theorem machine-checked / budget `checked` |
| setup | `isPrincipal_of_isPrincipal_pow_of_coprime` | principalization engine | source theorem machine-checked / budget `checked` |
| MayAssume | `MayAssume.coprime` | 规整到 primitive solution | source theorem machine-checked / budget `checked` |
| MayAssume | `MayAssume.p_dvd_c_of_ab_of_anegc` | Case II 入口侧的整除规整 | source theorem machine-checked / budget `checked` |
| MayAssume | `a_not_cong_b` | Case I 坏同余规整 | source theorem machine-checked / budget `checked` |
| Case I outer statement | `CaseI.SlightlyEasier` / `CaseI.Statement` / `CaseI.may_assume` | 固定分支陈述与附加假设消去 | source theorem machine-checked / budget `checked` |
| Case I ideal extraction | `ab_coprime`, `auxf'`, `auxf`, `exists_ideal` | 为 cyclotomic factorization、有限索引选择以及 ideal 的 `p` 次幂结构做准备并完成抽取 | source theorem machine-checked / budget `checked` |
| Case I principalization | `is_principal_aux`, `is_principal` | 用 regularity 把 ideal-level 信息拉回 element-level | source theorem machine-checked / budget `checked` |
| Case I element recovery / close | `ex_fin_div`, `caseI_easier`, `caseI` | 选取生成元、整理单位与同余并收束矛盾 | source theorem machine-checked / budget `checked` |
| Case II π-language | `zeta_sub_one_dvd`, `span_pow_add_pow_eq`, `div_one_sub_zeta_mem`, `div_zeta_sub_one_Bijective` | 把整数整除转写为 `π = ζ - 1` 的 divisibility 语言 | source theorem machine-checked / budget `checked` |
| Case II ideal-factor layer | `prod_c`, `exists_ideal_pow_eq_c`, `root_div_zeta_sub_one_dvd_gcd_spec`, `c_div_principal` | 建立 `𝔠 η` 与 `𝔞 η` 的 ideal-level `p` 次幂结构 | source theorem machine-checked / budget `checked` |
| Case II distinguished root | `zeta_sub_one_dvd_root_spec`, `p_dvd_c_iff`, `p_dvd_a_iff`, `p_pow_dvd_c_eta_zero`, `p_pow_dvd_a_eta_zero` | 锁定唯一 ramified root `η₀` 并控制 `𝔭`-整除 | source theorem machine-checked / budget `checked` |
| Case II descent core | `exists_solution`, `exists_solution'` | 从 level `m+1` 构造 level `m` 的新解 | source theorem machine-checked / budget `checked` |
| Case II close / merge | `not_exists_solution`, `not_exists_solution'`, `not_exists_Int_solution`, `not_exists_Int_solution'`, `caseII`, `flt_regular` | 取最小 `m` 收束，并与 Case I 合并 | source theorem machine-checked / budget `checked` |

regular primes 的 package 层 proof-budget closure 已经完成；
下文继续保留 canonical high-risk leaf 名单，只是为了保持跨文件命名稳定。

#### regular primes 再拆一层的 leaf ledger

以下 package / subpackage 名称已与 `process_audit.md`、`eligibles/regular_primes_proof_process.md` 对齐；
审计口径：下表中的 `trace budget status` 同时作用于 package 本身及其所列 `one-more-depth` 子项；
这些展开项已拥有独立 `<=100` proof-step ledger，因此统一标记为 `checked`。

| package | subpackages at one more depth | trace budget status |
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

#### regular primes 独立 ledger 摘要

| package | total proof steps | descendant closure carried by the same ledger |
|---|---:|---|
| `setup` | `13` | no extra canonical descendant beyond the package itself |
| `Case I outer statement` | `16` | no extra canonical descendant beyond the package itself |
| `Case I ideal extraction` | `21` | closes former package-level unresolved `exists_ideal pairwise ideal coprimality interface` |
| `Case I principalization` | `13` | no extra canonical descendant beyond the package itself |
| `Case I element recovery / close` | `25` | closes former package-level unresolved `caseI_easier / aux-index exclusion` |
| `Case II π-language` | `18` | no extra canonical descendant beyond the package itself |
| `Case II ideal-factor layer` | `25` | closes `Case II ideal-factor layer / global product to local p-th powers` |
| `Case II distinguished root` | `20` | closes `Case II distinguished root / p_pow_dvd_c_eta_zero` |
| `Case II descent core` | `35` | closes `Case II descent core / three-root formula and raw descent` |
| `Case II close / merge` | `34` | closes `Case II close / merge / not_exists_solution'` |

#### regular primes 已继续深拆的高风险 leaf

以下 canonical high-risk leaf 名称保持不变；
它们及其 `one-more-depth` 子包都已由对应 package ledger 关闭，
因此统一记为 `checked`。

| leaf | one-more-depth items | trace budget status | 最高风险点 |
|---|---|---|---|
| `Case II ideal-factor layer / global product to local p-th powers` | `exists_ideal_pow_eq_c_aux / RHS normalization`; `prod_c / cyclotomic product expansion`; `prod_c / factorwise 𝔪·𝔠η·𝔭 substitution`; `prod_c / common-factor cancellation`; `exists_ideal_pow_eq_c / pairwise-coprime local extraction`; `root_div_zeta_sub_one_dvd_gcd / witness packaging` | `checked` | `closed` |
| `Case II distinguished root / p_pow_dvd_c_eta_zero` | `η₀ divisibility criterion import`; `off-root product coprimality`; `gcd-product pivot`; `distinguished factor reinsertion into total product`; `visible 𝔭^(m*p) extraction from global p-th power` | `checked` | `closed` |
| `Case II descent core / three-root formula and raw descent` | `three-root orbit selection`; `root-difference as unit·π`; `three-root cancellation identity`; `raw descended triple packaging`; `raw nondivisibility certification` | `checked` | `closed` |
| `Case II close / merge / not_exists_solution'` | `generalized-family minimal-m closure`; `π-adic normalization of z`; `integer transport`; `primitive gcd cleanup`; `caseII permutation close`; `final merge` | `checked` | `closed` |

#### regular primes status ledger

regular primes 的 canonical package / high-risk leaf 命名同步，
以及 theorem-boundary sentence 的固定口径，
已经与 `process_audit.md`、`eligibles/regular_primes_proof_process.md` 三层材料一致。
`11` 个 canonical package、`4` 个 canonical high-risk leaf，
以及先前曾单列的 `2` 个 package-level unresolved subitem
都已拥有独立 `<=100` proof-step ledger；
因此本节对应的 machine-trace `unchecked` surface 已经收束为 `0`。

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
regular primes 审计表中也已无剩余 package-level unresolved subitem。
