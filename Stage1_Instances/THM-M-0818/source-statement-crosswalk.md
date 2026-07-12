# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6012-6017` supplies `Erdos-Szekeres` theorem, attribution
Erdos/Szekeres, year 1935, and the complete gloss `单调子序列的存在性` (existence of a monotone
subsequence). Git history places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record gives no domains, quantifiers, length
bound, distinctness, monotonicity convention, proof boundary, bibliography, or formal declaration.

`Docs/Stage0_Blueprint.md:22334-22359` repeats the gloss while leaving exact definitions and premises,
proof route, dependency graph, alternate formulations, axioms, machine state, and artifact links
open. The rev-5.6 manifest retains `已验证` only as untrusted metadata and resets the target to
`L0 / rework_required`.

## Primary-source lead

The inspected primary paper is P. Erdos and G. Szekeres, *A combinatorial problem in geometry*,
*Compositio Mathematica* 2 (1935), 463-470, archival locator
`CM_1935__2__463_0`. The observed Numdam PDF has SHA-256
`d6aa57844f6b0f22fc7c78789c4c10b1d35d3b1f399ca0a134dd355abbdd498d`; the archive metadata page
identifies the same authors, title, year, volume, and pages.

The second proof, printed pages 467-468, orders planar points by monotonically increasing abscissae
and states that one can choose points whose ordinates are monotonically increasing or decreasing.
It explicitly permits equal ordinates to be classified either way, defines the symmetric minimum
`f(n,n)`, then defines the asymmetric `f(i,k)`, gives a recurrence, and states sharpness by exhibiting
`(i-1)(k-1)` points avoiding both alternatives. This is the direct source-family match to the
catalog gloss.

The observed OCR drops or corrupts some displayed formulas, and the paper's surrounding main result
is instead the convex-polygon problem. Intake therefore does not promote a reconstructed formula to
the canonical statement. Pinpoint formula transcription, edition/correction status, modern
strictness conventions, and independent mathematical review remain open, so this is `H1`, not H0.

## Component crosswalk

| Catalog/source component | Source meaning | Pinned Lean candidate | Intake assessment |
|---|---|---|---|
| monotone subsequence | choose indices in original order and compare their ordinates | `g : Nat ->o Nat` selects an infinite subsequence | family match; finite/infinite choice open |
| increasing alternative | source permits monotonically increasing ordinates | `forall m n, m < n -> r (f (g m)) (f (g n))` | exact for a selected relation; strictness open |
| decreasing alternative | source permits monotonically decreasing ordinates | `forall m n, m < n -> not r (f (g m)) (f (g n))` | becomes nonincreasing for `r = (<)` in a linear order |
| equal values | source says ties may count as increasing or decreasing | `<` gives strict-increasing/nonincreasing; `<=` gives nondecreasing/strict-decreasing | no fixed relation directly gives weak/weak; transport not frozen |
| finite threshold | asymmetric `f(i,k)` recurrence and sharp lower example | no finite threshold appears in the candidate declaration | important statement mismatch to resolve |
| infinite selection | not the finite statement printed in the inspected second-proof passage | declaration is explicitly documented as infinitary Erdos-Szekeres | credible neighboring candidate, no root credit |
| `已验证` | untrusted catalog status | no proof object or receipt | no H or M credit |

## Lean and source boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Order.OrderIsoNat` declares:

```text
exists_increasing_or_nonincreasing_subseq
  (r : alpha -> alpha -> Prop) [IsTrans alpha r] (f : Nat -> alpha) :
  exists g : Nat ->o Nat,
    (forall m n, m < n -> r (f (g m)) (f (g n))) or
    forall m n, m < n -> not r (f (g m)) (f (g n))
```

Its source comment names it the infinitary Erdos-Szekeres theorem. `IntakeProbe.lean` elaborates this
declaration and adjacent embedding APIs against the pinned environment. That establishes a usable
formal candidate and justifies `M3` discovery status only. Statement identity, minimal imports,
finite/infinite relationship, proof-body provenance, axioms, placeholder and trust closure, and an
external-candidate audit belong to downstream phases.

Before leaving H1, accountable reviewers must verify and hash the exact incorporated source formula,
map every domain, parameter, hypothesis, alternative, equality convention, and boundary case, audit
corrections or errata, and approve the crosswalk. Before machine credit, the statement phase must
freeze and mutation-test the exact elaborated target and checked transports.
