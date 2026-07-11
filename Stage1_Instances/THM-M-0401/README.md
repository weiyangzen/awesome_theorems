# THM-M-0401 Intake Dossier

Status: `planned`, `L0 / rework_required`. This dossier records intake only. It does not claim exact Lean statement acceptance, source-proof fidelity, audit completion, or theorem completion.

## Scope Map

The selected human claim is Schmidt's simultaneous approximation theorem in product form. For a positive dimension `n`, algebraic reals `alpha_i`, and linear independence of `1, alpha_0, ..., alpha_(n-1)` over `Q`, the positive denominators `q` for which

`product_i ||q * alpha_i|| < q ^ (-1 - epsilon)`

are finite for every positive `epsilon`. Here `||x||` means distance to the nearest integer.

Included: real algebraic inputs, simultaneous rational approximation with one positive common denominator, the product inequality, and finiteness of exceptional denominators.

Excluded or not yet identified with the root: the full number-field Subspace Theorem, quantitative bounds, effective constants, `n = 0`, zero denominators, nonpositive epsilon, and the coordinatewise `-(1/n)-epsilon` formulation except as a prospective corollary requiring a checked bridge.

The legacy module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_014.lean` is discovery input only. Its `CanonicalProductStatementShape` is the planned formal-target candidate. Rev-5.6 exact elaboration, normalized expression hash, environment fingerprint, transports, and mutation tests belong to `S56-M-0401-STATEMENT` and remain open.

## Source-Statement Crosswalk

| Source | Pinpoint/status | Mapped content | Intake boundary |
|---|---|---|---|
| W. M. Schmidt, *Simultaneous approximation to algebraic numbers by rationals*, Acta Mathematica 125 (1970), 189-201 | Primary paper identified by title, volume, year, and page span; exact theorem/page and errata not yet independently checked | Product-form simultaneous approximation claim | Bibliographic identification only; cannot establish `H0` |
| W. M. Schmidt, *Diophantine Approximation*, LNM 785, Springer (1980) | The repository's `1980` label is treated as a book pointer; theorem/page/edition and errata remain to audit | Later exposition/context | Does not replace the primary-paper pinpoint |
| `Docs/researches/math_theorems.md` | Repository metadata says “代数数的联立逼近” and “已验证” | Candidate identity and topic | Untrusted metadata; no proof or machine credit |
| `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_014.lean` | Legacy `CanonicalProductStatementShape` | Proposed Lean encoding of dimension, algebraicity, independence, epsilon, and finite denominator set | No rev-5.6 statement fingerprint or root proof credit |

Current source debt is `H3`: a plausible primary source and claim are identified, but the exact theorem number/page, assumptions, proof boundary, edition relation, and errata require the anchor/source audit. Current machine debt is `M4`: no rev-5.6 exact target or root closure has been accepted. Current readability debt is `R3`: this is an intake map, not a proof reconstruction.

## Open Task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`

Only intake is self-tested here. All later nodes remain open, and only the integration lane may accept this provisional result.

## Validation Record

Base revision: `a8d6489fd935cd71fa4499f2f3f5b051998203f4`.

The preflight commands `python3 Docs/tools/check_stage1_standard.py`, `python3 scripts/stage1_target.py check`, and `python3 scripts/stage1_target.py show THM-M-0401` exited 0. They reported 15 assurance groups, 1546 uniform-L0 unique targets ranked 1 through 1546, and this target at rank 14 with lifecycle `planned` and `theorem_complete: false`.

The owned-artifact self-test commands and exact outcomes are recorded in `.stage1-worker-selftest.json`. No Lean proof validation is claimed by this intake phase.
