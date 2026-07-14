# THM-M-1063 proof recheck at current base

Item: `S56-M-1063-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T05:46:30+08:00`

Base revision: `c470319c4a07f669317557ea705f6546605ac4da`

Base tree: `680bb215853ecfbfa26fe069d1282188ed3944aa`

## Verdict

`blocked`. The proof phase remains `[ ]`; no proof body or proof credit was added.

The frozen target is the full finite-variance Donsker invariance principle in continuous path
space. The current repository and pinned dependency closure contain no theorem with that result.
`target_iff_expandedSourceShape` only unfolds the target definitions, while
`ObligationTree.exactRoot_of_exactRoot` requires the complete target as its hypothesis and returns
it unchanged. Neither declaration inhabits the root.

Pinned mathlib provides a scalar central limit theorem and generic Gaussian-process, tightness,
Prokhorov, Arzela-Ascoli, finite-dimensional-law, and convergence-in-distribution infrastructure.
Those APIs do not prove polygonal-path measurability, finite-dimensional convergence,
finite-second-moment uniform tightness, or path-law identification for the frozen process. Scoped
searches found no Donsker or functional-central-limit declaration in any pinned package.

The nearest pre-existing external-audit candidate remains `facebookresearch/atlas-lean` at
indexed revision `34ffed396f376454c1a9b297f3fd74c5c801fb50`. Its useful code stops at a
Rademacher finite-dimensional route; the decisive variable-block CLT and deterministic Slutsky
bodies contain `sorry`, and it has no continuous-path tightness or path-space convergence theorem.
It is therefore ineligible for import or proof credit. No dependency was fetched, built, or
modified.

The first failed frozen gate remains `M1063-C-PATH`: no checked construction packages the
floor-based pointwise formula as a continuous path. The substantive root cut remains
`M1063-L-CLT`, `M1063-L-MODULUS`, `M1063-L-ASCOLI`, `M1063-L-PROKHOROV`,
`M1063-L-LAW-UNIQUE`, and `M1063-T-API`. All 29 machine-required obligations remain open and the
root remains `M4`.

## Narrow evidence

The commands below ran in this checkout using the automation-provided, untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. Lean object files were emitted
only under `/tmp` during the direct checks and removed afterward. No `lake update`, `lake build`,
dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1,546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1063` | 0 | Rank 506; planned; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1063/check_obligation_tree.py` | 0 | 31 obligations and 125 typed edges passed; denominator `a55c3e2...26a7703`; root open at M4. |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-1063/DonskerTarget.lean` | 0 | The exact target and definitional expansion elaborated and printed `DonskerInvariancePrinciple : Prop`. |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-1063/ObligationTree.lean` | 0 | The identity interface elaborated and printed the complete Donsker target as both input and output. |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-1063/AnchorAudit.lean` | 0 | Scalar CLT and generic convergence anchors resolved; axiom reports contained only `propext`, `Classical.choice`, and `Quot.sound`. |
| `rg` for Donsker/FCLT terms in pinned mathlib and other pinned packages | 1 | Expected no-match exits; no pinned package contains a topical declaration. |
| `rg` for prohibited constructs in owned Lean sources | 1 | Expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `unsafe`, `opaque`, `extern`, `implemented_by`, or `native_decide` construct exists. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 at `98dc76e...`; Lake 5.0.0-src at the same Lean revision. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | Mathlib revision `8a178386...` and tree `bdc39a3...`; the pinned tree was clean. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent because the assigned proof phase is incomplete. |

## Boundary and retry condition

Lifecycle stays `planned`; `audit_complete=false` and `theorem_complete=false`. The intake-era
manifest still says M3 while the frozen closure says M4, so this recheck reports the fail-closed
vector `[H2, M4, R4]` without editing authoritative state. There are no accepted receipt IDs. This
artifact is nonrelease blocker evidence, not a proof receipt, and it does not satisfy
`S56-M-1063-PROOF` or support master acceptance.

Resume only after the frozen path construction, measurability, finite-dimensional convergence,
finite-second-moment tightness, subsequential limit identification, Brownian-law uniqueness, and
final API composition packages are implemented without placeholders, or after an immutable exact
Lean 4 proof can be pinned, imported, exact-type checked, and provenance validated. Because the
assigned proof deliverable is incomplete, `.stage1-worker-selftest.json` is deliberately absent.
