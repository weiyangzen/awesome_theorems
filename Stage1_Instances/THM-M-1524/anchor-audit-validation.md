# THM-M-1524 anchor-audit validation

Item: `S56-M-1524-ANCHOR_AUDIT`  
Base revision: `286ba271be26ff9620e5969b63a73c14792868af`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains no declaration whose
source mentions Heisenberg, Robertson, or an uncertainty principle/relation. It does provide the
needed Cauchy-Schwarz leaves (`inner_mul_inner_self_le`, `norm_inner_le_norm`) and the partial-map
object `LinearPMap`; the latter has a submodule domain but no density, unbounded-adjoint, or
uncertainty API. The narrow Lean probe elaborates these interfaces and reports only `propext`,
`Classical.choice`, and `Quot.sound` for its checked Cauchy-Schwarz wrapper.

The repository's legacy `S1_M_192.lean` proves a bounded/everywhere-defined symmetric-operator
version. That encoding is not the frozen densely-defined self-adjoint target, so it remains
unaccepted discovery evidence.

A bounded external search found a materially stronger candidate:
`adambornemann-glitch/Spectra@8dbaaf6728d1342ae16acf79fd7eef7c59b37e63`. Its modules
`SchrodingerRobertson` and `Heisenberg` contain `observable_robertson_stddev` and
`heisenberg_uncertainty` for self-adjoint unbounded observables with explicit product-domain data.
The immutable source hashes and Apache-2.0 license were verified, and its four-file project-local
import closure has no executable `sorry`, `admit`, `axiom`, `unsafe`, or `implemented_by` marker.
Its toolchain is Lean `4.31.0-rc1`, its mathlib is `40f050...484`, and it is not in this repository's
Lake closure. Moreover, its operator encoding is not definitionally equal to the frozen custom
`Observable`, so a checked transport is still required.

The root remains `M2`: there is credible immutable external mathematical closure, but no repo-local
kernel closure. The next proof work must pin/port the proof body and implement the encoding
transport. This phase does not claim audit or theorem completion.

## Commands and results

All commands ran inside this worker clone. No Lake update/build, dependency clone/fetch, or `.lake`
mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1524` | 0 | rank 192, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty; installed pinned source is clean |
| `rg -li 'heisenberg\|robertson\|uncertainty principle\|uncertainty relation' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 (expected) | no matching pinned mathlib source file |
| public GitHub repository queries for Lean quantum mechanics/information and named uncertainty terms | 0 | four credible repositories inspected; Spectra exposed the matching terminal declarations |
| immutable Git smart-HTTP ref query for `adambornemann-glitch/Spectra` | 0 | master resolved to `8dbaaf6728d1342ae16acf79fd7eef7c59b37e63` |
| immutable raw/archive inspection of Spectra theorem files, toolchain, manifest, license, and local import closure | 0 | theorem bodies, hashes, Lean/mathlib pins, license, and zero scoped executable proof-gap markers verified |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1524/AnchorAudit.lean` | 0 | partial-map and eight analytic interfaces checked; Cauchy-Schwarz wrapper elaborated; axioms printed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1524/Statement.lean` | 0 | frozen target re-elaborated |
| `python3 Stage1_Instances/THM-M-1524/check_anchor_audit.py` | 0 | local pins/hashes, legacy mismatch, immutable Spectra sources/pins/license/import closure, and `M2` boundary agreed |
| `python3 -m json.tool Stage1_Instances/THM-M-1524/anchor-audit.json` | 0 | structured ledger valid |

The external search is bounded discovery rather than proof of global absence. GitHub code search
was unavailable anonymously; that limitation is recorded in the structured ledger.
