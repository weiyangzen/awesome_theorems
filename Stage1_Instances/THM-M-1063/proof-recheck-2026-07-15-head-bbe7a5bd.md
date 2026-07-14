# THM-M-1063 proof recheck at current base

Item: `S56-M-1063-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T06:37:41+08:00`

Base revision: `bbe7a5bd1c72a12f3f43b79b6a4cac3f62d2085a`

Base tree: `aa558ed6f23779c7d2d9a8427775f709d8b7e31b`

## Verdict

`blocked`. The proof phase remains `[ ]`; no proof body or proof credit was added.

The exact target is the finite-variance Donsker invariance principle in continuous path space. It
requires the clipped-floor polygonal interpolation of arbitrary centered i.i.d. real increments
with finite positive variance to converge in distribution in `C([0,1], R)` to the specified
standard Brownian path law. The local theorem `target_iff_expandedSourceShape` only unfolds the
definitions. `ObligationTree.exactRoot_of_exactRoot` assumes the complete target and returns it
unchanged. Neither declaration proves a substantive obligation or inhabits the root.

A fresh pinned-closure search found no Donsker or functional-central-limit declaration. Mathlib
provides scalar central limit theorems and generic Gaussian-process, tightness, Prokhorov,
Arzela-Ascoli, and convergence-in-distribution infrastructure, but not the missing continuous-path
argument. The previously audited nearest external candidate is only a Rademacher
finite-dimensional route, has `sorry` in decisive bodies, and contains no path-space tightness or
convergence theorem. It is ineligible for import or proof credit.

The assumptions were also checked for a possible legitimate vacuity proof. There is no such
shortcut: the polygonal formula agrees across mesh boundaries, at `t = 1` it sums exactly the first
`n` increments, `n = 0` is the zero path, and positive `sigma` removes denominator degeneracy. The
Gaussian, zero-mean, covariance-`min` Brownian specification is consistent. A `False.elim` proof
would therefore be unsound.

All 29 machine-required obligations still have null terminal proof-body IDs. The first failed gate
is `M1063-C-PATH`, and the substantive root cut remains `M1063-L-CLT`,
`M1063-L-MODULUS`, `M1063-L-ASCOLI`, `M1063-L-PROKHOROV`,
`M1063-L-LAW-UNIQUE`, and `M1063-T-API`. Closing the target requires new checked proofs of path
construction and measurability, finite-dimensional convergence, finite-second-moment tightness,
subsequential limit identification, Brownian-law uniqueness, and final API composition. Assuming
one of those packages, imposing stronger moments, or substituting scalar convergence would change
the frozen theorem.

## Narrow evidence

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused read-only. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed. Bounded
external code-search API requests were attempted, but GitHub rejected the unauthenticated request
with HTTP 403 and grep.app returned HTTP 429; no remote result is credited as proof evidence.

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
| bounded `curl` queries to GitHub code search and grep.app | 22 | GitHub returned HTTP 403 and grep.app returned HTTP 429; no result was used and no source or dependency was downloaded. |
| scoped JSON assertion over `obligation-registry.json` | 0 | 31 obligations, 29 machine-required, and every required `terminal_proof_body_id` is null. |
| `cd Formalizations/Lean && lake env lean --version && lake --version; git -C .lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | Lean 4.29.0 at `98dc76e...`; Lake 5.0.0-src; clean mathlib revision `8a178386...`, tree `bdc39a3...`. |
| `sha256sum` over the exact target, architecture, audit, registry, graph, toolchain, and manifest inputs | 0 | Input hashes agree with the structured blocker record. |

## Boundary and retry condition

Lifecycle stays `planned`; `audit_complete=false` and `theorem_complete=false`. The root vector
stays `[H2, M4, R4]`, with no proof-phase delta and no accepted receipt IDs. This current-base
artifact is nonrelease blocker evidence, not a proof receipt. It does not satisfy
`S56-M-1063-PROOF`, change scheduler state, or support master acceptance.

Resume only after the frozen missing packages are implemented without placeholders, or after an
immutable exact Lean 4 Donsker proof becomes available for pinned import, exact-type checking, and
provenance validation. Because the assigned proof deliverable is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.
