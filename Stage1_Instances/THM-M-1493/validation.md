# THM-M-1493 intake validation

## Scope

This record validates only the `planned` theorem dossier, scope map, source-statement crosswalk,
six-node open task DAG, source-family inspection, and discovery-only pinned Lean API probe. It does
not validate an exact mathematical statement, a specific simplex algorithm or pivot rule, solver
correctness or termination, an accepted proof body, audit completion, or theorem completion.

The worker tree was nonrelease-dirty throughout: the automation-provided canonical `.lake` link was
already untracked, and this intake's owned artifacts plus the root self-test packet were new. The
link and its canonical pinned package tree were used read-only. No `lake update`, `lake build`,
dependency clone/fetch, or other `.lake` mutation was performed.

## Environment

- Repository base: `04d551db74b7e1d7d9d261bba4727b3daf8a70d5`
- Base tree: `ee8a3d7a6c48598ca61028d71e21e0802ed968e1`
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- Lake: `5.0.0-src+98dc76e`
- mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- mathlib tree: `bdc39a3123201dae413a9d9be56ec242c19e5c2b`
- Platform: Linux `7.0.0-27-generic`, `x86_64`
- Validation date/timezone: 2026-07-13, Asia/Shanghai

The Cowles Foundation author-hosted 418-page scan of *Activity Analysis of Production and
Allocation* was downloaded transiently for inspection. It was 12,008,247 bytes with SHA-256
`4bdbb1ed2e35542c7344c9739c8e81aca97c86bf0ba1f70b416b650344217dce`. The public
contents-page projection used to confirm Chapter XXI and its pages had SHA-256
`340f9cef5f8cb33b71605c2acddcffc3d016a482da811b4796a4b6dbc3a35179`. Neither
mutable observation was vendored or promoted to an immutable, independently reviewed `H0` packet.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1493` | 0 | rank 1170, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` at preflight | 0 | only the pre-existing untracked `Formalizations/Lean/.lake` link existed; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 10910,10915 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| transient `curl` of the Cowles contents page and `m13-all.pdf`, plus PDF page inspection | 0 | located Dantzig Chapter XXI pp. 339-347 and distinct theorem families; hashes recorded above; discovery only |
| `rg -n -i 'simplex method\|simplex algorithm\|dantzig\|linear program\|linear programming' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems --glob '*.lean'` | 0 | located mathlib's linarith simplex-oracle family and adjacent LP prose; no repo-local source-selected THM-M-1493 target |
| `rg -n '^theorem \|^lemma '` over mathlib's `SimplexAlgorithm` source family | 1 expected | no theorem or lemma declaration in the inspected oracle implementation; not a global absence claim |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` before and after validation | 0 | empty output; pinned package worktree clean |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake versions recorded above |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1493/IntakeProbe.lean` | 0 | all 14 adjacent simplex-oracle interfaces elaborated; combined output SHA-256 `a7e566426c9a476590434ba24ba282eb7806b4d65a212df24f05ff22ca57aca4`; no target theorem introduced |
| `python3 -m json.tool` on all owned JSON artifacts and `.stage1-worker-selftest.json` | 0 | every structured artifact parsed as JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1493-pycache python3 -m py_compile Stage1_Instances/THM-M-1493/check_intake.py` | 0 | scoped validator parsed without adding generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-1493/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | authority identity, null target, H5/M4/R4 boundary, source and package hashes, exact inventory, receipt/packet agreement, and six open tasks agree |
| prohibited-token scan over `IntakeProbe.lean` | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token |
| `git diff --check -- Stage1_Instances/THM-M-1493 .stage1-worker-selftest.json` plus per-new-file no-index checks | 0 | no whitespace diagnostics |

The final JSON, scoped invariant, prohibited-token, package-cleanliness, and whitespace results were
recorded after receipt and worker-packet creation. The scoped validator's exact stdout SHA-256 is
`4f847b86d71ff4d4d53ef8a80f9bc1a4340e9797903938871ad012d9e4b84d2d`.

## Known failures and boundary

Master acceptance is pending. The catalog method label still lacks one selected exact proposition.
Source admission and independent optimization/source review, the canonical Lean expression and
mutation certificate, exhaustive formal anchor audit, discovery protocol, obligation registry,
typed graphs, proof and composition, trust/provenance closure, readable reconstruction, hermetic
replay, deterministic bundle, and independent verification remain open.

Verdict: `no_state_change`. This self-tested worker proposal may be handed off as `[_]`; it remains
unfinished and unaccepted. `audit_complete=false` and `theorem_complete=false`.
