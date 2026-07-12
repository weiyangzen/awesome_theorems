# Exact-statement gate: blocked

Item: `S56-M-1516-STATEMENT`  
Base revision: `98e63368ae23fcc5338261550116996c11891fc1`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
verbatim target wording is only `经典力学的哈密顿形式` ("the Hamiltonian form of classical
mechanics"). This names a formalism, not one proposition. The intake dependency expressly leaves
the exact-source gate open and does not authorize a statement choice.

Repository discovery material contains several inequivalent candidates:

- Hamilton's coordinate equations `qdot = partial H / partial p` and
  `pdot = -partial H / partial q`;
- equivalence with Euler-Lagrange dynamics under a regular Legendre transform;
- conservation of an autonomous Hamiltonian along a solution;
- preservation of a symplectic form by a Hamiltonian flow.

Choosing among these would change the binders, hypotheses, conclusion, and boundary cases. Even
within one candidate, the source record does not fix the phase space, differentiability class,
time domain, solution concept, autonomous/time-dependent policy, Legendre regularity, flow
existence assumptions, or local/global conclusion. Consequently there is no exact expression to
hash, no meaningful minimal-import claim, no source-faithful transport, and no valid
hypothesis/domain/binder mutation suite. Selecting the intake's recommended energy-conservation
example would still substitute a plausible theorem for the unidentified source claim.

The metadata label `已验证` is untrusted under rev-5.6 and supplies neither a source statement nor
kernel evidence. This phase therefore stops at the canonical human-claim identity gate. It does
not broaden the source label into a conjunction or silently specialize it to a convenient model.

## Legacy Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_185.lean` was checked only as discovery input. Its
`StatementShape` quantifies over `HamiltonianMechanicsData`, whose intended premises and outputs
include unconstrained `Prop` fields. It asks three proposition fields to imply three different
proposition fields; neither the structure nor Hamilton's ODE connects those fields. Thus it is an
abstract, generally unprovable schema, not an elaboration of an identified source theorem.

The legacy file imports Gronwall, Picard-Lindelof, and symplectic-group modules and elaborates in
the pinned environment. That establishes syntax and types for the historical artifact only. It
cannot establish minimal imports for an exact rev-5.6 target because no such target has been
identified, and no legacy statement credit is inherited.

## Required unblock

An accountable source reviewer must select a stable primary source by edition and exact
theorem/page, quote one literal claim, and freeze its conventions. For an energy-conservation root,
this must at least specify phase space and scalar field, Hamiltonian regularity, the derivative-to-
gradient convention, trajectory and time-domain regularity, Hamilton's equation, autonomous
policy, and the precise constancy conclusion including empty/singleton domains. A later statement
worker can then encode exactly that claim, minimize imports, print and hash its elaborated type,
check any alternate encodings, and mutation-test the frozen assumptions.

## Narrow validation evidence

Commands ran in this worker clone on 2026-07-12. Lean commands ran from `Formalizations/Lean` using
the existing `.lake` symlink to the canonical pinned artifacts. No dependency update, build, clone,
fetch, or `.lake` mutation was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1516` | exit 0; rank 185, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_185.lean)` | exit 0; legacy abstract statement and discovery anchors elaborated; printed checks include `StatementShape : Prop`, matrix `J` identities, and the ODE uniqueness wrapper |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |

First failed gate: exact source-statement identity. Known failures are the canonical Lean target,
minimal-import determination, expression fingerprint, checked transport, and mutation tests. The
assigned phase is not self-tested or complete, so no `.stage1-worker-selftest.json` is emitted. No
theorem completion or downstream-node credit is claimed.
