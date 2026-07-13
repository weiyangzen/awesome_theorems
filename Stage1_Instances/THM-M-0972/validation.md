# THM-M-0972 intake validation

Validation ran and was finally replayed on 2026-07-13 in the isolated worker clone at base revision
`fcabbf1e0ad9507eebe91663bccabfa87d22813e` and base tree
`873e589c594454b7f263c7ed2342089a4d15e842`. The preflight tree contained only the
automation-provided untracked `Formalizations/Lean/.lake` symlink. The dossier and scheduler packet
are therefore explicitly nonrelease dirty evidence.

## Environment

- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- Dependency lock: `Formalizations/Lean/lake-manifest.json`, SHA-256
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- No `lake update`, `lake build`, dependency fetch, clone, or mutation of `.lake` was run.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0972` | 0 | rank 1506; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only the automation-provided untracked `.lake` symlink; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 7099,7104 -- Docs/researches/math_theorems.md` | 0 | all six catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| immutable EoM revision and Crossref DOI metadata inspection | 0 | multiple Janson variants, two 1990 primary-source leads, union/nonoccurrence mismatch, and page discrepancy recorded; no H0 credited |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit shown above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version shown above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree shown above; package status clean |
| SHA-256 over authority, source, toolchain, lock, five probed mathlib modules, and bounded source excerpts | 0 | hashes recorded in `instance.json` and provisional receipt |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0972/IntakeProbe.lean` | 0 | eleven adjacent APIs elaborated; output SHA-256 `ce661417facb99c70002c3e59ceea29af3e21171e973a6249e1bd409a0227864`; no target or proof body |
| bounded case-insensitive `janson` search in repo-local Lean and pinned mathlib | 1 (expected no match) | empty output SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; intake discovery only |
| inspect immutable `facebookresearch/atlas-lean` commit archive outside the repository | 0 | exact-topic Janson I/II/III declarations found, but root-relevant chains contain explicit `sorry`; no install/build/proof credit; restrictive license recorded |
| `python3 -m json.tool` on all structured artifacts and worker packet | 0 | every JSON artifact parsed after finalization |
| Python AST parse of `check_intake.py` | 0 | scoped checker parsed without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0972/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and dependency pins, H1/M4/R4 null target, inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0972/check_intake.py` | 0 | public replay mode passed without scheduler-only packet |
| prohibited Lean construct scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `bash -c 'for f in .stage1-worker-selftest.json Stage1_Instances/THM-M-0972/*; do out=$(git diff --no-index --check /dev/null "$f" 2>&1); code=$?; test "$code" -eq 1 && test -z "$out" || exit 1; done'` | 0 | all ten untracked artifacts differ from `/dev/null` only as new files, with no whitespace diagnostics |
| `git diff --check -- Stage1_Instances/THM-M-0972 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; no-index checks cover every untracked artifact |

## Known open gates

Exact primary edition and proposition selection; complete definition, premise, conclusion, proof,
pagination, and errata mapping; union/nonoccurrence reconciliation; independent source review;
canonical Lean target and minimal imports; expression and environment fingerprints; checked
transports; all four statement mutation classes; exhaustive anchor audit; discovery protocol;
obligation registry; typed graphs; proof and composition; source/provenance/trust closure; readable
reconstruction; hermetic replay; deterministic bundle; independent verification; audit completion;
theorem completion; and master acceptance all remain open.

No published strict schema for the provisional instance, task-DAG, receipt, or worker-packet shape
exists in this checkout. The local checker validates repository-local invariants only; it cannot
establish schema conformance, evidence authority, or master acceptance.

The external Atlas Lean candidate must additionally undergo exact statement, complete placeholder,
axiom, provenance, build, and license review. Its current placeholder-bearing roots are not usable
formal artifacts and receive no machine proof credit.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0972-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No canonical statement, H0 source closure, proof, audit
completion, theorem completion, or master acceptance is claimed.
