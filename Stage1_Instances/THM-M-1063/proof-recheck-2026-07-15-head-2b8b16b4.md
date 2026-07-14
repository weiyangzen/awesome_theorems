# THM-M-1063 proof recheck at current base

Item: `S56-M-1063-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T06:19:52+08:00`

Base revision: `2b8b16b4ca4c9ff610215bd8306fdb3f751f5345`

Base tree: `e9c3bddf01615e3a25aac732152cb0975f38f0eb`

## Verdict

`blocked`. The proof phase remains `[ ]`; no proof body or proof credit was added.

The exact target is the finite-variance Donsker invariance principle in continuous path space. It
requires the clipped-floor polygonal interpolation of arbitrary centered i.i.d. real increments
with finite positive variance to converge in distribution in `C([0,1], R)` to standard Brownian
motion. The target-local theorem `target_iff_expandedSourceShape` only unfolds definitions, while
`ObligationTree.exactRoot_of_exactRoot` assumes the complete target and returns it unchanged.
Neither declaration proves a substantive obligation or the root.

Pinned mathlib provides scalar central limit theorems and generic Gaussian-process,
Levy-Prokhorov, tightness, Arzela-Ascoli, and convergence-in-distribution infrastructure. A fresh
exact source scan found no Donsker or functional-central-limit declaration in any pinned Lake
package. The previously audited nearest external candidate, `facebookresearch/atlas-lean` at
`34ffed396f376454c1a9b297f3fd74c5c801fb50`, is only a Rademacher finite-dimensional route; its
decisive CLT and Slutsky bodies contain `sorry`, and it has no continuous-path tightness or
path-space convergence theorem. It is not eligible for import or proof credit.

All 29 machine-required obligations still have null terminal proof-body IDs. The first failed gate
is `M1063-C-PATH`: the pinned closure has no checked construction packaging the frozen pointwise
interpolation formula as a continuous path. The substantive root cut remains `M1063-L-CLT`,
`M1063-L-MODULUS`, `M1063-L-ASCOLI`, `M1063-L-PROKHOROV`,
`M1063-L-LAW-UNIQUE`, and `M1063-T-API`. Closing it requires new proofs of continuous-path
construction and measurability, finite-dimensional convergence, finite-second-moment tightness,
subsequential limit identification, Brownian-law uniqueness, and final API composition. Assuming
one of those packages or substituting scalar convergence or stronger moments would change the
frozen theorem and is forbidden.

## Narrow evidence

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused read-only. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1,546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1063` | 0 | Rank 506; planned lifecycle; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1063/check_obligation_tree.py` | 0 | 31 obligations and 125 typed edges passed; denominator `a55c3e2...26a7703`; root open at M4. |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-1063/DonskerTarget.lean` | 0 | The exact target and definitional expansion elaborated; output identified `DonskerInvariancePrinciple : Prop`. |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-1063/ObligationTree.lean` | 0 | The identity interface elaborated; its complete Donsker hypothesis and conclusion are definitionally the same target. |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-1063/AnchorAudit.lean` | 0 | Scalar CLT and generic convergence anchors resolved; axiom reports contained only `propext`, `Classical.choice`, and `Quot.sound`. |
| `rg` for Donsker/FCLT terms in every pinned Lake package | 1 | Expected no-match exit; no pinned package contains a topical Lean declaration. |
| `rg` for prohibited constructs in owned Lean sources | 1 | Expected no-match exit; no `sorry`, `admit`, `sorryAx`, bodyless axiom, unsafe, opaque, extern, `implemented_by`, or `native_decide` construct exists. |
| scoped JSON assertion over `obligation-registry.json` | 0 | 31 obligations, 29 machine-required, and every `terminal_proof_body_id` is null. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` plus tool versions | 0 | Clean mathlib revision `8a178386...`, tree `bdc39a3...`; Lean 4.29.0 at `98dc76e...`; Lake 5.0.0-src. |
| `sha256sum` over the target, tree, audit, registry, graph, toolchain, and manifest inputs | 0 | Source/input hashes match the structured blocker record. |
| structured blocker JSON parse and invariant assertions | 0 | Identity, base/tree, input hashes, open-state flags, empty proof-credit arrays, null terminal bodies, cut set, and absent self-test agree. |
| whitespace checks for both new blocker artifacts | 0 | No whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test deliberately absent because the proof phase is incomplete. |

## Boundary and retry condition

Lifecycle stays `planned`; `audit_complete=false` and `theorem_complete=false`. The root vector
stays `[H2, M4, R4]`, with no proof-phase delta and no accepted receipt IDs. This current-base
artifact is nonrelease blocker evidence, not a proof receipt. It does not satisfy
`S56-M-1063-PROOF`, change scheduler state, or support master acceptance.

Resume only after the frozen missing packages are implemented without placeholders, or after an
immutable exact Lean 4 Donsker proof becomes available for pinned import, exact-type checking, and
provenance validation. Because the assigned proof deliverable is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.
