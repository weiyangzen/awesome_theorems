# Intake validation

## Scope and environment

This record validates only the `planned` intake dossier for `S56-M-0204-INTAKE`: repository
identity, the received source boundary, proposition-changing choices, two noncredited pinned formal
candidates, the API-only Lean probe, and the six open downstream tasks. It does not validate a
canonical statement, a source-to-Lean transport, a proof body, or any theorem-completion gate.

- Validation date: `2026-07-13`, timezone `Asia/Shanghai`.
- Base revision: `5fe11f4b5e32a06ffb4432460319fc8ae906fe7b`.
- Base tree: `64c5aacf7cf3eb79008f5a1970151e3e53cb9966`.
- Initial worker status contained only the automation-provided untracked
  `Formalizations/Lean/.lake` symlink. It was used read-only, making this nonrelease dirty-worker
  evidence.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake: `5.0.0-src+98dc76e`.
- Mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was run.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0204` | 0 | rank 1536; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | initial status contained only the shared `.lake` symlink; base revision/tree as above |
| `git blame -L 1471,1476 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded public-source search for Matthew Stewart's attributed 1746 work | mixed timeout/no-result | no edition, stable artifact, theorem/page, or proposition was verified; the title remains an uncredited lead |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; clean package worktree |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0204/IntakeProbe.lean` | 0 | six exact or adjacent APIs elaborated; two candidate axiom reports were `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `6150567743a00bd3a290daa3d3ccdd7e4ad7e325ebd2fda418ac8310c2391e86`; no target or proof body declared |
| `rg` exact-topic search over pinned mathlib and repository Lean | 0 | located the two direct declarations in the pinned triangle module and no separate repo-local THM-M-0204 artifact; bounded intake discovery only |
| `python3 -m json.tool` on scoped JSON artifacts and worker packet | 0 | instance, open task DAG, provisional receipt, and packet parsed after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0204-pycache python3 -m py_compile Stage1_Instances/THM-M-0204/check_intake.py` | 0 | checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0204/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, hashes, null formal target, H1/M3/R4 boundary, exact inventory, packet, and six open tasks agreed |
| prohibited Lean construct scan over `IntakeProbe.lean` | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, `axiom`, bodyless `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` plus scoped `git diff --check` | 0 | no whitespace diagnostics; each no-index exit 1 represented only an expected new-file difference |

## Open gates

The first failed downstream gate is exact source-statement identity. The title and literal gloss do
not select between the general cevian theorem and the median/Apollonius specialization. A lawful
immutable source, formula and definition crosswalk, historical and errata review, independent
approval, point/domain/division/directed-length/nondegeneracy/boundary decisions, canonical Lean
expression and environment fingerprint, checked transports, and mutation tests remain open.

The exhaustive anchor and provenance audit, obligation registry, typed graphs, proof and
composition, trust closure, readable reconstruction, hermetic replay, deterministic evidence
bundle, independent verification, audit completion, theorem completion, and master acceptance also
remain open. These failures do not invalidate this fail-closed `planned` intake.
