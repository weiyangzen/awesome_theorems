# THM-M-0387 rev-5.6 Machine Audit

> Audit date: `2026-07-10` (`Asia/Shanghai`)
> Root target: `FermatLastTheorem`
> Root result: partial machine coverage, exact root not kernel-closed

This is the canonical prose surface for machine-proof evidence. Node vectors
and recomputed metrics are in `proof_units.json`; readable mathematics is in
`proof_outline.md`, `readable/`, and `eligibles/`. A local wrapper records a
checked conclusion but never relocates its imported proof body.

Final recomputed coverage is `29/93` machine targets (`31.18%`), with
`7 M0-L`, `10 M0-W`, and `12 M0-P` nodes. Tree classification and readable
closure are each `132/132`; human-source `H0` closure is conservatively
`0/113` because exact primary-source-to-node assumption crosswalks remain
unfinished. The exact root vector is `[H1, M2, R0]`.

## Environment And Policy

| component | immutable version |
|---|---|
| Lean | `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| mathlib | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `leanprover-community/flt-regular` | `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` |
| `checkdecls` | `3d425859e73fcfbef85b9638c2a91708ef4a22d4` |

Accepted foundational axioms are exactly `propext`, `Classical.choice`, and
`Quot.sound`. `sorry`, `admit`, `sorryAx`, `knownin1980s`, and every unreviewed
custom axiom are disallowed. The lint parses declaration-level
`#print axioms` output rather than inferring trust from filenames.

## Exact Statement

Pinned mathlib defines:

```lean
def FermatLastTheoremWith (R : Type*) [Semiring R] (n : Nat) : Prop :=
  forall a b c : R, a != 0 -> b != 0 -> c != 0 ->
    a ^ n + b ^ n != c ^ n

def FermatLastTheoremFor (n : Nat) : Prop :=
  FermatLastTheoremWith Nat n

def FermatLastTheorem : Prop :=
  forall n >= 3, FermatLastTheoremFor n
```

The repo-local `StatementAndReductionPath.lean` freezes the exact alias
`fermatLastTheoremRootStatement` and checks:

```lean
fermatLastTheoremRootStatement_iff :
  fermatLastTheoremRootStatement <-> FermatLastTheorem
```

This is an exact statement identity, not a proof of the proposition.

## Statement And Reduction API

| local declaration | exact checked conclusion | body boundary |
|---|---|---|
| `fermatLastTheoremRootStatement_iff` | root alias iff `FermatLastTheorem` | repo-local definitional proof |
| `fermatLastTheoremFor_iff_coprime` | fixed-exponent statement iff primitive `gcd = 1` formulation | local composition using mathlib primitive reduction |
| `fermatLastTheoremFor_iff_integer` | `FermatLastTheoremFor n <-> FermatLastTheoremWith Int n` | local wrapper over mathlib |
| `fermatLastTheoremFor_iff_rational` | `FermatLastTheoremFor n <-> FermatLastTheoremWith Rat n` | local wrapper over mathlib |
| `fltOfDivisorPath` | `m | n -> FLT(m) -> FLT(n)` | local wrapper over mathlib monotonicity |
| `fltExponentZeroPath` | `FermatLastTheoremFor 0` | local wrapper over mathlib boundary theorem |
| `notFltExponentOnePath` | `not FermatLastTheoremFor 1` | local wrapper over mathlib boundary theorem |
| `notFltExponentTwoPath` | `not FermatLastTheoremFor 2` | local wrapper over mathlib boundary theorem |
| `fermatLastTheoremRootOfOddPrimesPath` | `OddPrimeExponentClosure -> fermatLastTheoremRootStatement` | local wrapper over conditional mathlib assembly |

The transports, primitive reduction, boundary theorems, and monotonicity live
in `Mathlib/NumberTheory/FLT/Basic.lean`. The conditional assembly theorem
`FermatLastTheorem.of_odd_primes` lives in
`Mathlib/NumberTheory/FLT/Four.lean:275`.

The important boundary is logical, not cosmetic: the conditional assembly is
machine-closed for its exact implication, while `OddPrimeExponentClosure` is
not machine-closed. Therefore it cannot be used to label the root `M0-*`.

## Exponent Three

The terminal declaration is:

```lean
fermatLastTheoremThree : FermatLastTheoremFor 3
```

Its proof body is in pinned mathlib at
`Mathlib/NumberTheory/FLT/Three.lean:750`. The local wrapper is:

```lean
flt3Path : FermatLastTheoremFor 3
```

The source tree includes the mod-`9` branch, generalized Eisenstein-integer
equation, typed `Solution'`/`Solution` interfaces, and strict multiplicity
descent. The readable reconstruction and five independent leaf ledgers are in
`eligibles/n3_proof_process.md`. Classification: wrapper `M0-W/E1`; proof body
is mathlib, not repo-local.

## Exponent Four And Derivatives

The mathlib terminal is at `Mathlib/NumberTheory/FLT/Four.lean:266`:

```lean
fermatLastTheoremFour : FermatLastTheoremFor 4
```

Repo-local checked wrappers are:

```lean
flt4Path : FermatLastTheoremFor 4
flt4IntPath : FermatLastTheoremWith Int 4
flt8ViaFlt4Path : FermatLastTheoremFor 8
```

The imported proof tree covers minimal counterexample selection, primitive and
parity normalization, two Pythagorean-triple classifications, coprimality,
square extraction, a strictly smaller solution, and contradiction. Corrected
independent ledger totals are `14`, `16`, `33`, `13`, `12`, `25`, and `19`;
all are at most `100`. Full prose is in `eligibles/n4_proof_process.md`.

Classification: exact exponent-four terminal and derived wrappers `M0-W/E1`.
The tiny local wrapper bodies do not turn the mathlib proof into `M0-L`.

`InternalCoveragePath.lean` additionally exposes exact checked mathlib-backed
endpoints for positive odd minimal normalization, the square-sum product
coprimality bridge, the no-minimal contradiction, and the bridge terminal.
These exact nodes are `M0-W`; neighboring source-map packages without their
own wrapper/type/axiom packets remain `M3`.

## Small Exponents

The pinned `flt-regular` dependency additionally supplies:

```lean
fermatLastTheoremFive : FermatLastTheoremFor 5
fermatLastTheoremSeven : FermatLastTheoremFor 7
fermatLastTheoremEleven : FermatLastTheoremFor 11
fermatLastTheoremThirteen : FermatLastTheoremFor 13
FLT_small (hn : n in Finset.Icc 3 16) : FermatLastTheoremFor n
```

`SmallExponentsPath.lean` exposes exact local wrappers `flt5Path`, `flt7Path`,
`flt11Path`, `flt13Path`, and `fltSmallExponentsPath`. This closes every fixed
exponent in the interval `3 <= n <= 16`; it does not close arbitrary exponents.
Classification: `M0-P/E1`, because the proof bodies are in the immutable pinned
external dependency and checked through the local Lake closure.

## Regular Primes

The pinned terminal is at `FltRegular/FltRegular.lean:14`:

```lean
flt_regular {p : Nat} [Fact p.Prime]
    (hreg : IsRegularPrime p) (hodd : p != 2) :
    FermatLastTheoremFor p
```

The repo-local wrapper `regularPrimesPath` has the same conclusion. Its body is
not vendored. Classification is `M0-P/E1`, and the trust sentence is:

```text
upstream proof body: yes
repo-local checked pinned dependency and wrapper: yes
repo-local vendored proof-body copy: no
```

`InternalCoveragePath.lean` also exposes exact pinned endpoints for primitive
normalization, Case I, and Case II. Those exact package targets are `M0-P`;
their narrower internal source-map children remain `M3` unless independently
wrapped and probed.

Audited upstream packages and corrected declaration anchors include:

| package | exact source anchors |
|---|---|
| regularity | `IsRegularNumber`, `IsRegularPrime`, `isPrincipal_of_isPrincipal_pow_of_coprime` |
| primitive normalization | `MayAssume.coprime`, `FltRegular.p_dvd_c_of_ab_of_anegc`, `FltRegular.a_not_cong_b` |
| Case I | `FltRegular.CaseI.ab_coprime`, `auxf'`, `auxf`, `exists_ideal`, `is_principal_aux`, `is_principal`, `caseI_easier`, `caseI` |
| Case II entry and close | `not_exists_solution`, `not_exists_solution'`, `not_exists_Int_solution`, `not_exists_Int_solution'`, `caseII` |
| distinguished root | `zeta_sub_one_dvd_root`, `p_dvd_c_iff`, `p_dvd_a_iff`, `p_pow_dvd_c_eta_zero`, `p_pow_dvd_a_eta_zero` |
| descent | `exists_solution`, `exists_solution'` |

The names `find_root`, `find_root'`, `irreducible_aux`, bare `irreducible`,
`caseII_statement`, and `MayAssume.p_dvd_c_of_ab_of_anegc` do not exist at the
pinned revision and are not evidence. Corrected readable package ledgers are
in `eligibles/regular_primes_proof_process.md`; totals are `13`, `37`, `16`,
`21`, `13`, `25`, `18`, `25`, `20`, `35`, and `34`.

## Axiom Reports And Source Scan

The audited local wrappers, upstream mathlib endpoints, `FLT_small`, and
`flt_regular` report exactly:

```text
[propext, Classical.choice, Quot.sound]
```

The generic `FermatLastTheoremWith.mono` reports `[propext]`. The rev-5.6 lint
checks exact declaration types first, then parses each `#print axioms` result
against the manifest. It also scans the relevant local, mathlib FLT, and pinned
`flt-regular` sources after stripping comments and strings. No `sorry`,
`admit`, `sorryAx`, or custom `axiom` occurs in those claimed proof bodies.

## Full-FLT Candidate Audit

The fresh Imperial College London candidate audit used immutable revision
`44df7744a2a65cdc111875dc1b6f0db85477348f` (`2026-07-10`). Its toolchain is
Lean `4.32.0-rc1` with mathlib
`8bba4200986270d3b30be2bb2f8840af47a7854f`, incompatible with this closure.

`FLT/Proof.lean` defines an exact `flt : FermatLastTheorem`, but the chain has:

```lean
B4_proof : B4 := sorry
```

The positive-natural terminal reports:

```text
[knownin1980s, propext, sorryAx, Classical.choice, Quot.sound]
```

`knownin1980s` proves an arbitrary proposition. A conservative source scan
found `86` `sorry` occurrences in `25` Lean files. A local upstream rebuild was
not reproduced because the Lean toolchain download failed with an HTTP/2
framing error. Thus the exact candidate is `M5/E3`, never `M1` or `M0-*`.

Source-only Frey/invariant declarations and the abstract patching result
`ker_RtoT_le_nilradical` are `M3/E3` candidates: they were located and their
own files appear placeholder-free, but no independent build, transitive axiom
audit, compatible pin, or composition into the actual FLT objects was obtained.

## Root Gate

The strongest exact local root-shaped declaration is conditional:

```lean
fermatLastTheoremRootOfOddPrimesPath :
  OddPrimeExponentClosure -> fermatLastTheoremRootStatement
```

The nonregular general odd-prime family remains open at the Frey,
modularity-lifting, level-lowering, low-level contradiction, and composition
frontier. No exact placeholder-free local declaration of type
`FermatLastTheorem` exists. Root machine status is therefore `M2`; exact root
kernel closure is `false`.
