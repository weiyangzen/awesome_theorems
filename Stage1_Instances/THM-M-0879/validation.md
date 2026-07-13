# THM-M-0879 intake validation

## Scope

This record validates only the `planned` dossier, scope map, source-statement crosswalk, open task
DAG, catalog provenance, bibliographic ambiguity leads, and discovery-only pinned Lean API probe.
It does not validate a canonical multicommodity-flow proposition, source theorem, network encoding,
proof, accepted receipt, audit completion, or theorem completion.

The worker tree was nonrelease-dirty throughout: the automation-provided canonical `.lake` link was
already untracked, and this intake's owned artifacts plus the root self-test packet were new. The
canonical pinned artifacts were used read-only. No dependency update, build, clone, fetch, or other
`.lake` mutation was performed.

## Environment

- Repository base: `0c019b7194c9c43fa5f683fa82d637a0b275410d`
- Base tree: `43cf6ac322b1dba09be739b52ab3d02e9f9d8f3e`
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- Lake: `5.0.0-src+98dc76e`
- mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- mathlib tree: `bdc39a3123201dae413a9d9be56ec242c19e5c2b`
- Platform: Linux `7.0.0-27-generic`, `x86_64`
- Timezone/date: Asia/Shanghai, 2026-07-13

Mutable Crossref records for Hu's DOI `10.1287/opre.11.3.344` and Shahrokhi-Matula's DOI
`10.1145/77600.77620` were inspected through bounded HTTP requests. Their response SHA-256 values
were respectively `954ca319f3e94ced89c0e7b3d1e90f1fc0ca784141acc169707b2d4c16166725`
and `879196da1abaa73eba9be37243c334ba68df370077714b1769433dab57a14378`.
The publisher article downloads returned HTTP 403. The metadata was used only to demonstrate
distinct candidate meanings and is neither an immutable primary theorem edition nor H0 evidence.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0879` | 0 | rank 1432, planned, L0/rework_required, no legacy slot, theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` link was untracked |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 6439,6444 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate in `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded Crossref queries for the two DOI records | 0 | distinct two-commodity, maximum-throughput, approximation, optimization-dual, and path-cut candidate meanings identified; mutable metadata only |
| publisher article download attempts | 22 | both returned HTTP 403; no primary text, theorem locator, correction review, or H credit claimed |
| bounded exact-topic `rg` over repo-local and pinned Lean | 1 expected | no multicommodity-flow or network-flow declaration found; not an exhaustive absence claim |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0879/IntakeProbe.lean` | 0 | nine adjacent graph-incidence, path, and finite-sum APIs elaborated; no target theorem introduced; exact output SHA-256 `81f150699b50724051374edb1afa616464c4370d9a34db8d498826a6c3fc4174` |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| Python `ast.parse` on `Stage1_Instances/THM-M-0879/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0879/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/item identity, null target, H5/M4/R4 boundary, source and pin hashes, receipt/packet agreement, exact inventory, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0879/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited-construct `rg` over `IntakeProbe.lean` | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check` plus per-new-file no-index whitespace checks | 0 aggregate | no whitespace diagnostics |

The final structure, hashes, JSON, and whitespace results were recorded after receipt and worker
packet creation.

## Known failures and boundary

Master acceptance is pending. The catalog does not determine one proposition. An immutable primary
edition, exact theorem and proof locator, complete definition/assumption/conclusion map, version and
errata review, neighbor-target reconciliation, and independent review remain open. So do the
canonical Lean target, imports, expression and environment fingerprints, checked transports,
statement mutations, exhaustive anchor audit, obligation registry, typed graphs, proof,
composition, provenance and trust closure, readable reconstruction, hermetic replay, deterministic
bundle, and independent verification.

Verdict: `no_state_change`. This self-tested worker proposal may be handed off as `[_]`; it remains
unfinished and unaccepted. `audit_complete=false` and `theorem_complete=false`.
