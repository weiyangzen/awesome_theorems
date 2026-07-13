# THM-M-0887 intake validation

## Scope

This record validates only the `planned` dossier, scope map, source-statement crosswalk, open task
DAG, repository-source provenance, and discovery-only pinned Lean API probe. It does not validate an
exact spectral graph proposition, a selected graph operator or spectrum, a proof, audit completion,
or theorem completion.

The worker input was nonrelease-dirty because the automation-provided canonical `.lake` symlink was
already untracked. It was used read-only. No `lake update`, `lake build`, dependency clone or fetch,
network-triggering Lake operation, or other `.lake` mutation was performed. The new owned artifacts
and root self-test packet make the final worktree dirty as expected.

## Environment

- Repository base: `0c019b7194c9c43fa5f683fa82d637a0b275410d`
- Base tree: `43cf6ac322b1dba09be739b52ab3d02e9f9d8f3e`
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- Lake: `5.0.0-src+98dc76e`
- mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- mathlib tree: `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean
- Platform: Linux `7.0.0-27-generic`, `x86_64`
- Validation date/timezone: 2026-07-13, Asia/Shanghai

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0887` | 0 | rank 1437, planned, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only the pre-existing `Formalizations/Lean/.lake` symlink was untracked; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 6495,6500 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum` over authority, source, toolchain, lockfile, and pinned graph/spectrum modules | 0 | exact hashes recorded in `instance.json` and the provisional receipt |
| bounded Crossref request for an AMS *Spectral Graph Theory* monograph record | 22 | HTTP 429; no source fetched or credited |
| bounded request for an author-hosted spectral-graph-theory page | 60 | certificate verification failed; no source fetched or credited |
| bounded exact-topic `rg` over repo-local Lean and pinned mathlib | 0 | only this intake probe's disclaimer matched; no target-named declaration found; bounded discovery, not an exhaustive absence proof |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the environment record; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0887/IntakeProbe.lean` | 0 | nine adjacent graph-matrix, walk, Laplacian, Hermitian-eigenvalue, and spectrum APIs elaborated; stdout SHA-256 `c6367e0a484f227faedf6fc0668976df9486315d2d4202389d699f8ed156e171`; no target declared |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all JSON valid after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0887-pycache python3 -m py_compile Stage1_Instances/THM-M-0887/check_intake.py` | 0 | scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0887/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/item identity, null target, H5/M4/R4 boundary, source and pin hashes, receipt/packet agreement, exact inventory, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0887/check_intake.py` | 0 | public replay mode passed without scheduler-only packet input |
| prohibited Lean construct scan over the owned path | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check /dev/null` plus scoped `git diff --check` | 0 aggregate | no whitespace diagnostics; no-index exit 1 per file was only the expected new-file difference |

The structural validator, Lean probe, JSON, scoped invariant, prohibited-construct, and whitespace
checks were rerun after final serialization.

## Known failures and boundary

The catalog subject slogan still lacks a selected exact proposition. An immutable primary or
authoritative edition and numbered result, complete definition/premise/conclusion/proof/correction
crosswalk, graph/operator/spectrum and multiplicity conventions, neighboring-target reconciliation,
and independent scope/source review remain open. So do the canonical Lean expression, minimal
imports, expression and environment fingerprints, checked transports, statement mutations,
exhaustive anchor and provenance audit, discovery and obligation freezes, typed graphs, proof,
composition, trust closure, readable reconstruction, hermetic replay, deterministic evidence bundle,
independent verification, and release.

These failures do not invalidate a truthful self-tested planned intake. The first unmet node gate is
integration-lane master acceptance of the provisional receipt. Worker `[_]` remains unfinished;
`audit_complete=false` and `theorem_complete=false`.
