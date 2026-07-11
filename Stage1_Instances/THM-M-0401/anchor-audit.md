# THM-M-0401 formal-anchor audit

Audit item: `S56-M-0401-ANCHOR_AUDIT`. Search cutoff: `2026-07-12` (Asia/Shanghai).
This is a frozen candidate inventory, not a proof receipt. The canonical target remains
`Stage1Instances.THMM0401.SchmidtSimultaneousApproximationTarget` from `Statement.lean`.

## Discovery protocol

The search order followed rev-5.6 section 7.2: repo-local Lean, pinned mathlib, official or primary
formalization projects, other public Lean repositories, and statement collections. Queries covered
`Schmidt`, `Schmidt theorem`, `Schmidt's theorem`, `subspace theorem`, `simultaneous approximation`,
`simultaneous approximation to algebraic numbers`, `DiophantineApproximation`, product inequalities,
nearest-integer distance, algebraicity, and rational linear independence.

The immutable local inputs were repository base `1a43068b1644e78dd234d738040b40e4dea60bcb`, mathlib
commit `8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`), Lean `4.29.0`, and the lock file whose SHA-256 is
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`. No dependency was fetched,
updated, or modified.

External discovery used anonymous GitHub repository search for the three quoted topic/name families.
All three returned `total_count: 0`. GitHub code search was unavailable without authentication, and
grep.app returned a Vercel security-checkpoint HTML page rather than search results. Those failures
are explicit access limits: this inventory is complete for the recorded protocol, but it is not an
exhaustive claim about every public Lean repository. The current mathlib `master` head observed only
as a discovery boundary was `4efb186f102ebfd2eea1545c151d6fbcfdff0e43`; it was not fetched or used
as validation evidence.

## Candidate inventory

| ID | Candidate and immutable location | Exact comparison and provenance | Classification |
|---|---|---|---|
| `LOCAL-LEGACY` | `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_014.lean`, repository base above; `AwesomeTheorems.Stage1.S1_M_014.CanonicalProductStatementShape` | An exact product-form statement shape, locally restated and connected to the canonical target by `target_iff_legacyCanonicalProductStatementShape`. The legacy declaration is a `def : Prop`; its only theorem is a definitional expansion. There is no terminal proof body for the proposition. | `M3`, statement/interface only; no root closure |
| `MATHLIB-DIOPH` | `Mathlib/NumberTheory/DiophantineApproximation/Basic.lean`, pinned mathlib commit above; declarations `Real.exists_int_int_abs_mul_sub_le`, `Real.exists_nat_abs_mul_sub_round_le`, `Real.exists_rat_abs_sub_le_and_den_le`, `Real.infinite_rat_abs_sub_lt_one_div_den_sq_of_irrational`, and `Rat.finite_rat_abs_sub_lt_one_div_den_sq` | Kernel-built nearby infrastructure for one-dimensional Dirichlet/continued-fraction approximation. None takes a finite algebraic vector, assumes independence of `1, alpha_i`, or concludes finiteness of the product-form exceptional denominators. It cannot wrap or derive the exact root without the missing Schmidt/Subspace-Theorem argument. | rejected root anchor: statement mismatch; no machine credit for the root |
| `MATHLIB-NAME-HITS` | Entire `Mathlib` tree at the pinned commit | Case-insensitive name/topic search found only Gram-Schmidt/Krull-Schmidt uses of “Schmidt”, plus generic nearest-integer and Diophantine-approximation APIs. No Schmidt simultaneous-approximation or Subspace-Theorem declaration was located. | negative result; root remains `M4` |
| `EXTERNAL-GITHUB` | GitHub public repository index queried at the cutoff | No repository candidate was returned for the three recorded searches. Code search was access-blocked, so no external theorem, module, declaration, toolchain, proof body, axiom report, or dependency graph can be credited. | no candidate; not `M1` |
| `EXTERNAL-GREPAPP` | grep.app public endpoint queried at the cutoff | Endpoint returned a security-checkpoint page for all four alias queries, not a searchable response. | access failure; retry condition below |

The local exact statement is `M3`; it is not a proof candidate. No usable proof artifact for the exact
root was located in pinned mathlib or the accessible external searches, so the root stays `M4`.
In particular, the nearby Dirichlet results are not silently substituted for Schmidt's finiteness
theorem, and no anchor-only result is promoted to `M1` or `M0-*`.

## Human source boundary

Crossref identifies W. M. Schmidt, *Simultaneous approximation to algebraic numbers by rationals*,
Acta Mathematica 125 (1970), 189-201, DOI `10.1007/BF02392334`. This supports `H1`: a published
proof source is identified, but the primary paper's exact internal theorem/page, premise-by-premise
mapping, proof boundary, and errata have not been independently audited. It does not support `H0`.

## Validation and blockers

The structural and target-manifest checks passed. The pinned mathlib commit/tree checks and scoped
source searches passed. A fresh `lake env lean` replay of `Statement.lean` failed with
`unknown module prefix 'Mathlib'`: the worker's symlinked canonical `.lake` currently lacks the
required compiled Mathlib artifacts. Per worker policy no build, update, clone, or fetch was run.
This does not invalidate the prior statement-phase elaboration, but it prevents fresh Lean replay in
this phase.

The anchor audit itself is self-tested as a truthful negative/provenance inventory. Root proof work
is blocked on either (a) a newly located immutable Lean 4 proof with an exact statement mapping and
locally checkable dependency closure, or (b) a new local proof architecture. External discovery
should be rerun with authenticated GitHub code search and an accessible code index. Fresh Lean replay
requires restoration of the canonical pinned `.olean` artifacts by the owning lane.

