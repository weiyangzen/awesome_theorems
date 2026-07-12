# Anchor audit

Item: `S56-M-0612-ANCHOR_AUDIT`

Audit date: 2026-07-12. This is an audit of the canonical local-domain target in
`Statement.lean`, not proof evidence for it.

## Repository and pinned mathlib

The repository manifest pins mathlib at commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95` and Lean `v4.29.0`. A complete
case-insensitive scan of the pinned `Mathlib/**/*.lean` sources for
`non.?squeez`, `gromov.?width`, `symplectic`, `pseudo.?holomorphic`, and
`pseudoholomorphic` found no nonsqueezing theorem, symplectic-capacity API, or
pseudoholomorphic-curve proof package.

The useful supporting declarations are in
`Mathlib.LinearAlgebra.SymplecticGroup`: `Matrix.J`, `Matrix.J_transpose`,
`Matrix.J_squared`, `Matrix.symplecticGroup`, `SymplecticGroup.J_mem`, and
`SymplecticGroup.symplectic_det`. They concern finite symplectic matrices, not
nonlinear local embeddings or capacities. `Mathlib.Analysis.Hofer.hofer` is an
elementary complete-metric-space lemma whose module explicitly says mathlib is
"very far away" from its motivating holomorphic-curve application. It is not
a terminal or near-terminal nonsqueezing anchor. `AnchorAudit.lean` checks all
these names against the pinned environment.

The legacy repository file
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_256.lean` supplies definitions
and reflexive wrappers only. Its terminal target remains unproved and its
global-map encoding is not the canonical local-domain target. It receives no
proof credit.

## External Lean 4 candidates

GitHub repository-name/description searches on 2026-07-12 returned zero Lean
repositories for `nonsqueezing`, `non-squeezing`, `pseudoholomorphic`, or
`Gromov width`. A broader `symplectic language:Lean` search returned four
repositories. Three Lean 4 candidates were downloaded as immutable commit
archives and scanned; the Lean 3 `mpenciak/symplectic_groups` result was
excluded by the target-system gate.

| Repository and immutable revision | Toolchain / scope | Result and integration decision |
|---|---|---|
| `hrmacbeth/symplectic@acc509702046aaae6a3c9be4546d5735ad7450cf` (archive SHA-256 `7928647b8ec2182cca61d2594cb532a927d36c8707fab7c98a1f73b21badc33e`) | Lean `v4.19.0-rc3`; mathlib `ff99cdaecce8cab2fcc3d3828ab7f79717fbf77a`; four Lean source files | `Symplectic/Definitions.lean:151` declares `gromovNonsqueezing`, but its body at line 157 is `sorry`. The same file contains 12 `sorry` occurrences, including definitions used by the theorem. Its capacity-normalized ball/cylinder parameters and manifold-map hypothesis also do not definitionally match the canonical radius/local-injectivity target. It is an informative statement candidate only: no proof provenance, no kernel credit, and no permissible pin/import target. |
| `krystophny/geomnum@8b72abbfd96111237a55ea411069ebb395bc4c00` (archive SHA-256 `4c5149b8fc03c15761501cb9d8bee345d7f2b884ef5d010c9f39ece5bf9a2a94`) | Lean `v4.16.0`; three Lean source files; symplectic numerics | Full source scan found no nonsqueezing, Gromov-width, symplectic-capacity, or pseudoholomorphic declaration. Not an integration candidate. |
| `BenFrohman/NS_Millennium_Proof@44ca45c347d6a08d89a31844f83d40dbb66e08d1` (archive SHA-256 `f06481c30be92bd4805461f058c010d7261feb632d292b4cb95f677fed2f2210`) | 47 Lean source files; Navier-Stokes project | Full source scan found none of the terminal search terms. Not an integration candidate. |

The external archives were inspected outside the repository and were not
installed or added to `.lake`. This respects the pinned dependency boundary.
Because the only named external theorem is explicitly admitted, there is no
external closure to integrate and hence no repo-local integration debt to
disguise as completion.

## Classification and boundary

The audit finds real object-level anchors but no terminal Lean 4 proof. The
canonical target remains `M3` formalization debt; no accepted proof state is
added. This phase does not establish `H0` or `R0`, does not complete the full
source/provenance audit, and does not claim audit or theorem completion. The
next obligation-tree phase must model the missing nonlinear symplectic
geometry/capacity or pseudoholomorphic-curve route rather than treating the
matrix API or the admitted external declaration as a proof leaf.
