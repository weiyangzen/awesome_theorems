# THM-M-0554 proof-phase recheck

Item: `S56-M-0554-PROOF`

Attempt date: 2026-07-14 (Asia/Shanghai)

Base revision: `c45f3c7090cb4adf616d45e5414985f956e807b2`

Base tree: `da6f991c07f11e8608ddc090af9356558d64d360`

## Verdict

`blocked`. This retry found no genuine AHSS proof-bearing declaration and
added no proof body. The existing `proof-blocker.json` remains accurate. The
frozen registry has 32 obligations, 30 of them machine-required, and its open
root cut remains:

- `M0554-X-GENCOH`
- `M0554-C-EXACT-COUPLE`
- `M0554-C-E2-MODEL`
- `M0554-L-STRONG`

Pinned mathlib supplies the generic
`CategoryTheory.E2CohomologicalSpectralSequence` container, CW substrate, and
singular-homology substrate. It does not supply the required
generalized-cohomology pair/excision/wedge package, exact-couple AHSS
construction, cellular `E2` identification, skeletal filtration, or strong
convergence theorem. A fresh bounded source search for
`Atiyah-Hirzebruch`, `AHSS`, `generalized cohomology`, `exact couple`, and
`strong convergence` found no candidate in the pinned mathlib sources.

The literal Lean proposition is nevertheless inhabitable for the wrong
reason. A temporary `/tmp` probe constructed every page from
`HomologicalComplex.zero`, used zero objects for all filtration and stable-page
objects, and chose the output-defined `coefficientConvention`,
`strongConvergence`, and `naturalityInSpace` propositions as `True`. The probe
elaborated without `sorryAx`, reporting only `propext`, `Classical.choice`, and
`Quot.sound`. It did not use `E.pointIsPoint`, `E.exactnessAxiom`,
`E.wedgeAxiomOrRepresentability`, `K.finiteCW`, `K.exhaustive`, or
`K.cellAttachments`.

That term was deliberately not retained or credited: it constructs no AHSS
and consumes none of the frozen semantic children. Treating it as the proof
would violate exact-statement fidelity, child-to-parent composition, and the
explicit no-fake-result rule.

## Validation evidence

All checks used the existing pinned `.lake` artifacts. No `lake update`, Lake
build, dependency clone/fetch, or `.lake` mutation was performed. Generated
Lean objects and the rejected probe stayed under `/tmp`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | `PASS`: 32 obligations and 91 typed edges; denominator `3c72072a40a15d829c40df68b5fc121b74662a883799f7f7c277fa9c6ed8048b`; root remains open at M4 with no composition certificate. |
| `lake env lean -R ../../Stage1_Instances/THM-M-0554 -o /tmp/thm-m-0554-statement/Statement.olean ../../Stage1_Instances/THM-M-0554/Statement.lean` from `Formalizations/Lean` | 0 | The frozen target elaborated; object output was outside `.lake`. |
| `LEAN_PATH=/tmp/thm-m-0554-proof-recheck lake env lean /tmp/M0554Explore.lean` from `Formalizations/Lean` | 0 | The temporary zero/`True` probe elaborated and `#print axioms` returned `[propext, Classical.choice, Quot.sound]`; source SHA-256 `4bf0ca6751da1058cdd8c057d5db51f1c0672538f9b9648b1ef515201bfa0f4b`. It was rejected and is not a repository artifact. |
| `rg -n -i 'Atiyah[- ]?Hirzebruch|\bAHSS\b|generalized (co)?homology|exact couple|strong convergence' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | Expected no-match result: no pinned mathlib candidate with those search terms. |
| `rg -n '^\s*(sorry|admit|axiom)(\s|$)' Stage1_Instances/THM-M-0554 --glob '*.lean'` | 1 | Expected no-match result: no prohibited Lean declaration token in owned Lean sources. |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |

The first failed gate remains exact-statement fidelity and composition. Retry
only after publishing and accepting a faithful statement plus obligation
registry v2, then implementing and composing the four root-cut packages
without placeholders; alternatively, pin an immutable exact compatible AHSS
proof and pass exact-type, provenance, trust, and composition validation.

This is durable blocker evidence, not a proof receipt. It does not satisfy the
assigned proof item or claim M0, validation, release, theorem completion, or
master acceptance. Because the assigned phase is not genuinely self-tested as
complete, `.stage1-worker-selftest.json` is deliberately absent.
