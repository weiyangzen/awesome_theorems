# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `拉德马赫分拆公式`, Hans Rademacher,
the year 1937, and the gloss `整数分拆函数的精确公式` ("an exact formula for the integer partition
function"). Stage0 repeats those fields. The manifest preserves `已验证` only as
`source_status_untrusted`. These records contain no displayed formula, theorem number, page,
assumptions, proof, errata, or formal declaration.

## Primary-source locator

The intended historical source is plausibly Hans Rademacher, *On the partition function p(n)*,
Proceedings of the London Mathematical Society, second series 43 (1937), 241-254. This bibliographic
locator has not yet been checked against an immutable page image in this intake, so no theorem/page
or exact transcription is accepted. The statement/source phases must inspect the paper, record the
precise result and page, compare later corrigenda or normalization changes, and obtain independent
review. This keeps the repository's sparse metadata from being silently upgraded to `H0`.

## Component crosswalk

| Source component | Intended mathematics | Candidate Lean surface | Intake status |
|---|---|---|---|
| `p(n)` | number of unordered partitions of `n` into positive integers | `Fintype.card (Nat.Partition n)` | pinned type and finite instance probed; source representation transport open |
| `k >= 1` | positive summation index | `k : Nat` with shift or subtype | convention open |
| `A_k(n)` | finite root-of-unity/exponential sum using coprime residues and a multiplier or Dedekind sum | `Finset`, `Nat.Coprime`, `Complex.exp` | definition absent and source signs open |
| square roots and `sinh` | analytic real/complex summand | `Real.sqrt`, `Real.sinh`, coercions | APIs probed; target expression open |
| derivative | derivative of a real extension in the shifted variable | `deriv` | API probed; function and evaluation point open |
| infinite series | convergent sum over positive `k` | `HasSum` / `Summable` / `tsum` | API probed; convergence and codomain open |
| exact formula | equality, not merely asymptotic equivalence | equality after the required coercions | canonical proposition absent |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports the partition definition and basic real/complex analysis. It confirms that
`Nat.Partition n` has a `Fintype`, and checks `Fintype.card`, `Complex.exp`, `Real.sqrt`, `Real.sinh`,
`deriv`, `HasSum`, and `tsum`. A bounded case-insensitive search for `Rademacher` in pinned mathlib
found no names, while mathlib's partition generating-function module explicitly describes the
ordinary partition generating-function specialization as TODO. Those observations are discovery
leads only, not the later immutable anchor audit and not evidence that no external formalization
exists.
