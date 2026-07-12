# Intake validation

Base revision: `936bf2b9e968abd3b79b5b36d32f2f2bff648c7e` (tree
`8c9d3261b0ba9a81deb5bfc19a335a02cb80f962`).

Validation is limited to the planned intake dossier, source and duplicate boundary, open task DAG,
pinned API vocabulary, artifact inventory, and whitespace. The pre-existing automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, dependency fetch, or other
`.lake` mutation was run. No canonical theorem expression or proof was selected, so no theorem
kernel result is claimed.

Commands ran from the isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0637` | 0 | rank 1054; topology/point-set topology; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | initial status contained only the pre-existing `.lake` symlink; base revision and tree appear above |
| repository catalog, Stage0, source provenance, and `THM-M-0318` dossier inspection | 0 | compact-map gloss, open Stage0 fields, inspected Satz II family, and duplicate compact-domain boundary recorded |
| Crossref DOI query and publisher PDF inspection | 0 | confirmed 1930 article metadata and found Satz II on printed page 175; external discovery only, not H0 |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 at `98dc76e3`; Lake 5.0.0-src+98dc76e |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, clean package worktree |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0637/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated; complete stdout SHA-256 `9f769abce88c3b748318e8ac4ba392ebcd303d54bfa90d9eeaa7647f59334430`; no target or proof body |
| bounded exact-topic `rg` search in pinned mathlib, repo-local Lean, and `THM-M-0318` | 0 | only the foreign `THM-M-0318` statement matched; discovery only, not an exhaustive anchor audit |
| `python3 -m json.tool` on the three JSON artifacts | 0 | instance, open task DAG, and provisional receipt parsed after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0637-pycache python3 -m py_compile Stage1_Instances/THM-M-0637/check_intake.py` | 0 | scoped checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0637/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, current hashes, null formal target, H1/M4/R4 vector, inventory, worker packet, and six open tasks agreed |
| prohibited Lean construct scan over the owned path | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, bodyless `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` plus `git diff --check` | 0 | no whitespace diagnostics in owned artifacts or the worker packet |

Known downstream failures are an independently accepted immutable source review, the relationship
with `THM-M-0318`, explicit nonemptiness, continuity and map encoding, exact image-compactness
meaning, canonical target elaboration and mutation tests, anchor audit, obligation registry, proof,
trust/composition validation, hermetic replay, and independent release verification. These prevent
theorem completion but do not invalidate this fail-closed planned intake.
