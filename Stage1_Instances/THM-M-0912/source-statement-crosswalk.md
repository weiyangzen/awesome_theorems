# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6672-6677` supplies exactly the title `帕斯卡恒等式`, attribution
to Blaise Pascal, year 1654, gloss `组合数的递推关系`, importance `高`, and status `已验证`. Git
history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The entry contains no formula, bibliography,
definition, domain, ordered binders, side conditions, proof locator, correction record, reviewer, or
formal artifact.

`Docs/Stage0_Blueprint.md:24877-24902` repeats the gloss while explicitly leaving exact definitions
and premises, formal system, foundation, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links unresolved. The rev-5.6 manifest records rank 1454, baseline
`L0 / rework_required`, no legacy slot, `lifecycle_mode: planned`, and `theorem_complete: false`.
Its `已验证` field is explicitly untrusted.

## Clause crosswalk

| Catalog component | Mathematical information fixed | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `组合数` | ordinary binomial coefficients are intended | `Nat.choose` | plausible exact object; definition and source relationship still need approval |
| `递推关系` | a recurrence is intended | `Nat.choose_succ_succ`, its addition spelling, or a predecessor form | formula and index domain absent from catalog |
| `帕斯卡恒等式` | conventional theorem-family name | a future canonical statement plus checked transports | name alone cannot establish exact statement identity |
| Blaise Pascal / 1654 | historical attribution metadata | none | no edition, passage, translation, or historical-source audit |
| `已验证` | untrusted inventory value | exact source and kernel receipts would be required | no H or M completion credit |

## Modern mathematical statement lead

NIST Digital Library of Mathematical Functions, version 1.2.7 (release 2026-06-15), Chapter 26
author D. M. Bressoud, Section 26.3(iii) "Recurrence Relations," equation 26.3.5, permalink
`https://dlmf.nist.gov/26.3.E5`, was inspected on 2026-07-13. It states
`C(m,n) = C(m-1,n) + C(m-1,n-1)` subject to `m >= n >= 1`. The equation's TeX response was 102
bytes with SHA-256 `af43da30b9553896c868f2202e16a0b0a72984111ba0e169bf07814a940663a4`.
The recurrence subsection points to Riordan, *An Introduction to Combinatorial Analysis* (1958),
pages 4-5, and Comtet, *Advanced Combinatorics* (1974), page 10.

This is strong statement-discovery evidence, but not `H0`. DLMF is a modern reference rather than
the catalog's claimed 1654 source; the cited books were not inspected; no complete proof-to-claim,
incorporated-definition, historical-attribution, correction/errata, or independent-review map is
accepted. The provisional human status is therefore `H1`.

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Data.Nat.Choose.Basic` defines `Nat.choose` recursively and exposes:

| Declaration | Candidate type/role | Boundary |
|---|---|---|
| `Nat.choose_succ_succ` | all-natural successor recurrence | exact pinned candidate; broader index domain than DLMF's displayed constraint |
| `Nat.choose_succ_succ'` | addition-spelled all-natural recurrence | syntactic alternate candidate only |
| `Nat.choose_succ_left` | positive-column predecessor recurrence | needs `0 < k`; uses truncated subtraction |
| `Nat.choose_eq_choose_pred_add` | positive-row and positive-column predecessor recurrence | closest direct predecessor candidate, but has explicit hypotheses and term order |

`IntakeProbe.lean` authenticates these names, types, definitions, and candidate axiom reports with
the existing pinned toolchain. It is intentionally not a local wrapper or canonical theorem. The
mathlib body for `Nat.choose_succ_succ` is a definitional `rfl`, but proof-body credit cannot attach
to `THM-M-0912` until the statement phase fixes the exact source claim and later provenance/trust
gates accept the match. The provisional machine status is `M3`, not `M0-W`.

## Statement-phase selection

The statement phase conservatively selects the DLMF-constrained predecessor formula as the exact
provisional root because it is the only formula-level published statement preserved by intake. The
ordered natural binders, both displayed side conditions, conclusion, `Nat.choose` definition
boundary, three domain-preserving encodings, and row/column boundaries are frozen in
`Statement.lean` and `statement.json`. The all-natural successor recurrence remains an explicitly
excluded broader substitution.

This selection is worker-self-tested, not accepted source completion. Dependency-ordered master
acceptance, historical Pascal-source fidelity, complete proof and correction mapping, preservation
of the DLMF side-condition context beyond the observed-response digest, and independent H0 review
remain open. Pinned mathlib declarations still receive no terminal proof-body credit in this phase.
