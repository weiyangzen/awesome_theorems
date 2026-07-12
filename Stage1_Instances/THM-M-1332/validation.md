# Intake validation

Base revision: `bbb685ee4adcd9f19b5a727d1523cc7d6ad3b07f` (tree
`aadea0300fd76d31a98264ab39039d2247f8e049`). Validation is limited to manifest membership,
standard consistency, planned dossier structure, source and environment pins, a discovery-only
pinned Lean API probe, prohibited-construct hygiene, and whitespace.

The repository record does not determine an exact proposition. `IntakeProbe.lean` therefore checks
only candidate existence and uniqueness interfaces; it introduces no theorem, selects no root, and
supplies no statement or proof credit. The automation-provided `Formalizations/Lean/.lake` symlink
was present before this work and was used read-only. No update, build, dependency clone/fetch, or
`.lake` mutation was run.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1332` | 0 | rank 944, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` | 0 | initial status contained only the pre-existing automation `.lake` symlink; preserved read-only |
| `git blame -L 9719,9724 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref DOI and Numdam item metadata requests for `10.24033/bsmf.481` | 0 | independently agree on Picard, title, 1894, volume 22, pages 52-57; bibliographic discovery only |
| Numdam primary PDF request | 28 | timed out and left an incomplete 103731-byte PDF; no primary-text statement inspection or source credit |
| `python3 -m json.tool Stage1_Instances/THM-M-1332/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1332/task-dag.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1332/intake-receipt.json` | 0 | valid JSON after finalization |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1332-pycache python3 -m py_compile Stage1_Instances/THM-M-1332/check_intake.py` | 0 | scoped validator compiles without generated files in the owned path |
| `python3 Stage1_Instances/THM-M-1332/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, H1/M3/R3 boundary, null formal root, exact artifacts, worker packet, and six open tasks agree |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1332/IntakeProbe.lean)` | 0 | ten pinned Picard-Lindelof existence and ODE uniqueness interfaces elaborated; no root declared |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | toolchain `651c...b1d2`; dependency lock `3216...2d81` |
| scoped forbidden-declaration scan over owned `*.lean` | 1 | expected no match; no `sorry`, `admit`, `sorryAx`, bodyless declaration, `unsafe`, or proof escape |
| per-file `git diff --no-index --check /dev/null <new-file>` | 1 | expected new-file diff status with empty diagnostics for every artifact and the worker packet |
| `git diff --check -- Stage1_Instances/THM-M-1332 .stage1-worker-selftest.json` | 0 | no tracked whitespace error; the checker and per-file checks cover untracked files |

Known downstream failures remain deliberately open: exact primary-source theorem and independent
review; canonical statement, minimal imports, expression/environment fingerprints, checked
transports/composition and mutations; immutable candidate/provenance audit; discovery and
obligation freezes; typed graphs; proof and parent closure; readable proof reconstruction;
hermetic replay, deterministic bundle, and independent release validation. These prevent audit and
theorem completion but do not invalidate a truthful self-tested `planned` intake.
