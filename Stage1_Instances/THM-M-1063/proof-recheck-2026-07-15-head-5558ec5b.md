# THM-M-1063 proof recheck at current base

Item: `S56-M-1063-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T07:22:22+08:00`

Base revision: `5558ec5b162bfdfa95b44fafcf97b69a44d1ff37`

Base tree: `f17ce1a24cd65800f536301fdb66a12e18ef3ae3`

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
package. The prerequisite immutable audit likewise found no compatible placeholder-free external
terminal body. A wrapper around the scalar CLT would prove only one-dimensional convergence and
would silently substitute a weaker theorem.

All 29 machine-required obligations still have null terminal proof-body IDs. The first failed gate
is `M1063-C-PATH`: no checked construction packages the frozen floor-based pointwise interpolation
as a continuous path. The substantive root cut remains `M1063-L-CLT`, `M1063-L-MODULUS`,
`M1063-L-ASCOLI`, `M1063-L-PROKHOROV`, `M1063-L-LAW-UNIQUE`, and `M1063-T-API`.
Closing the target requires new checked proofs of path construction and measurability,
finite-dimensional convergence, finite-second-moment uniform tightness, subsequential limit
identification, Brownian-law uniqueness, and final API composition. Assuming any missing package,
strengthening the moment hypotheses, or substituting scalar convergence is forbidden.

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
| `rg` for prohibited constructs in owned Lean sources | 1 | Expected no-match exit; no `sorry`, `admit`, `sorryAx`, bodyless axiom/constant, unsafe, opaque, extern, `implemented_by`, or `native_decide` construct exists. |
| scoped JSON assertion over `obligation-registry.json` | 0 | 31 obligations, 29 machine-required, and every required `terminal_proof_body_id` is null. |
| `cd Formalizations/Lean && lake env lean --version && lake --version; git -C .lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | Lean 4.29.0 at `98dc76e...`; Lake 5.0.0-src; clean mathlib revision `8a178386...`, tree `bdc39a3...`. |
| `sha256sum` over target, architecture, audit, registry, graph, toolchain, manifests, blueprint, and execution skill | 0 | Source and normative input hashes match the structured record. |
| `python3 -m json.tool` plus scoped current-base blocker assertions | 0 | JSON parsed; identity, current base/tree, hashes, open flags, empty proof-credit arrays, 29 null terminal bodies, exact cut set, and absent self-test agree. |
| whitespace checks for both fresh artifacts and the owned path | 0 | No whitespace diagnostics. |
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
