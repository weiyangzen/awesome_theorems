# THM-M-1235 anchor audit

Item: `S56-M-1235-ANCHOR_AUDIT`. Audit date: 2026-07-12. Repository base:
`935f676246c95d817740248fb8588e8cea34c00d`.

## Verdict

The predecessor freezes
`Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness`, for the source's
bounded-or-exterior closed planar region with analytic boundary components and
conditions `(I)`-`(VIII)`. No exact Lean 4 root theorem was found in the pinned
mathlib tree or the bounded external discovery surface. There is therefore no
candidate eligible to pin and wrap, and no repo-local integration debt. The
root remains `M4 / formalization_debt`; this audit supplies no proof or theorem-
completion credit.

## Pinned mathlib audit

The existing Lake dependency is clean mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, used with Lean 4.29.0. Recursive,
case-insensitive searches of `Mathlib/**/*.lean` used the terms `wolibner`,
`two-dimensional euler`, `2d euler`, `incompressible euler`, `euler equations`,
`vorticity`, `biot-savart`, `perfect fluid`, `ideal fluid`, and `navierstokes`.
They found no terminal theorem or even a fluid-PDE declaration matching the
canonical target.

Mathlib does provide lower-level analysis APIs for Euclidean spaces,
differentiability, integrability and Lp predicates, Laplacians, and divergence
theorems. `AnchorAudit.lean` checks representative declaration names under the
pinned environment. They could support a future expanded PDE model but do not
construct a `Motion`, establish conditions `(I)`-`(VIII)`, or prove the root.
They are classified only as `object_model_only`.

## External Lean 4 audit

Public GitHub repository discovery was run for `Wolibner Lean4`, `Wolibner
lean`, `incompressible Euler Lean4`, `fluid mechanics Lean4`, and `vorticity
Lean4`. The first four returned zero repositories; the last returned the two
projects below. The previously recorded Lean Millennium candidate was also
rechecked at its immutable commit.

| Repository and immutable revision | Candidate assessment | Provenance/trust result |
|---|---|---|
| `lean-dojo/LeanMillenniumPrizeProblems@540da94826f70f3edf4d4fc66ce6cda20e903f61` | Its `Problems.NavierStokes` modules encode the viscous three-dimensional Millennium problem and related solution definitions, not Wolibner's planar ideal-fluid theorem | Exact-type rejected; neither named declaration was imported, built, or credited |
| `Brsanch/sqg-lean-proofs@be3a4fa9713166fb9a93f70508b4fdff8039c03f` | Surface quasi-geostrophic shear-vorticity work; different equation, no Wolibner root in the recorded immutable tree | Rejected as non-exact; not integrated or credited |
| `jcamlin/iDNS-Lean4-Mathlib4@9910d06190244781495720e5047918bc03c5c843` | Three-dimensional Navier-Stokes project; the adjacent immutable-tree audit found no exact root and records admitted/incomplete project state | Rejected as non-exact and not proof-clean; not integrated or credited |

Repository metadata search is bounded discovery, not proof that no other Lean 4
project exists. Unauthenticated GitHub code search was not used. The negative
result is limited to the named, revision-pinned surfaces. No project was cloned
or added to Lake, and `.lake` was not mutated.

## Validation receipt

All commands ran in this worker clone and used the pre-existing dependency
artifacts. Exact exit codes and results are recorded below.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets in ranks 1..1546 passed |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | rank 159, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -ni 'wolibner|two-dimensional euler|2d euler|incompressible euler|euler equations|vorticity|biot-savart|perfect fluid|ideal fluid|navierstokes' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no match; `rg` exit 1 means an empty result |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1235/AnchorAudit.lean` | 0 | all seven supporting mathlib declaration names elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-1235/anchor-audit.json` | 0 | structured audit parsed successfully |
| `git diff --check -- Stage1_Instances/THM-M-1235 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The five recorded GitHub repository searches exited 0 on 2026-07-12. The exact-
name and equation searches returned zero repositories; `vorticity Lean4`
returned the SQG and iDNS projects. Immutable commit/tree/raw-file API checks for
the Lean Millennium candidate exited 0 and confirmed commit
`540da94826f70f3edf4d4fc66ce6cda20e903f61` and the two rejected Navier-Stokes
declarations. A later GitHub tree request was rate-limited (HTTP 403); it is not
used as passing evidence and does not affect the already pinned candidate rows.
