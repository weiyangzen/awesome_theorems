# THM-M-1234 anchor audit

Item: `S56-M-1234-ANCHOR_AUDIT`. Audit date: 2026-07-12. Repository base:
`cccb9533ded2784539e0c40ec597b9b01216220e`.

## Verdict

The exact canonical target is `Stage1Rev56.THMM1234.Statement`, the whole-plane,
unforced, finite-energy weak-existence statement frozen by the predecessor node.
No exact Lean 4 root theorem was found in the pinned mathlib tree or in the
recorded external discovery surface. Consequently there is nothing eligible to
pin and wrap, and no repo-local integration debt is created. The root remains
`M4 / formalization_debt`; this audit gives no proof or theorem-completion credit.

## Pinned mathlib audit

The local dependency is the clean git revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, used with Lean 4.29.0. A recursive
case-insensitive search of `Mathlib/**/*.lean` for `yudovich`, `incompressible
euler`, `euler equations`, `bounded vorticity`, and `vorticity` found no matching
root declaration. The only fluid-related textual hit from the broader audit was
a documentation mention of the divergence and Stokes theorems, not the Euler
PDE.

The five imports already selected by `Statement.lean` do expose the relevant
object-model primitives. `AnchorAudit.lean` checks their actual names under the
pinned environment. They support the domain, measure, smooth tests, derivatives,
integrals, and Lp predicates, but none constructs a `GlobalWeakSolution` or has a
type that can close `Statement`. They are therefore `object_model_only`, never a
Yudovich theorem anchor.

## External Lean 4 audit

Public GitHub repository searches were run for `Yudovich theorem`, `Yudovich
lean`, `Lean4 Yudovich`, `Lean4 incompressible Euler`, `vorticity lean4`, and
`Navier Stokes Lean4`. The exact-name queries returned no repository. The two
vorticity discoveries were inspected through immutable commit and recursive-tree
API endpoints:

| Repository and immutable revision | Candidate assessment | Provenance/trust result |
|---|---|---|
| `Brsanch/sqg-lean-proofs@be3a4fa9713166fb9a93f70508b4fdff8039c03f` | SQG shear-vorticity and harmonic-analysis infrastructure; different equation, with no Yudovich or incompressible-Euler root in its pinned tree | Rejected as non-exact; not imported, built, or credited |
| `jcamlin/iDNS-Lean4-Mathlib4@9910d06190244781495720e5047918bc03c5c843` | Three-dimensional Navier-Stokes project whose pinned tree contains only `Basic` and `FourierBasis` Lean modules; its main theorem is listed as planned | Rejected as non-exact and not proof-clean: its own pinned README reports an admitted assumption and an incomplete proof marker in the listed completed Fourier lemma |

Repository metadata search is a bounded discovery method, not a proof that no
other project exists. In particular, unauthenticated GitHub code search was not
available. The negative conclusion is deliberately limited to the named pinned
surfaces. Neither rejected project was cloned or added to Lake, so `.lake` and
the dependency closure were not mutated.

## Validation receipt

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard structure passed: 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | ordered target manifest passed |
| `python3 scripts/stage1_target.py show THM-M-1234` | 0 | rank 158, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -ni 'yudovich|incompressible euler|euler equations|bounded vorticity|vorticity' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no match; `rg` exit 1 denotes an empty result |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1234/AnchorAudit.lean` | 0 | all eight supporting mathlib declaration names elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-1234/anchor-audit.json >/dev/null` | 0 | structured audit is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1234 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The recorded GitHub API queries also exited 0 on 2026-07-12. Their returned
commit IDs and tree contents are captured above and in `anchor-audit.json`.
