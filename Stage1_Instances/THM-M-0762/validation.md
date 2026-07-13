# Intake validation

Base revision: `d05520867fab3367a9b61b9544c3e12241204f54`; base tree:
`fb2cfc62077d5b53e9938632cd6361dd60872067`.

This validation covers target membership, the planned dossier and open task DAG, catalog
provenance, scope and source boundaries, JSON and scoped invariants, and one narrow pinned Lean API
and axiom probe. It does not validate a canonical theorem statement, source transport, proof body,
or theorem closure. The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink. It and the canonical pinned artifacts were used read-only; no
dependency update, build, clone, fetch, or `.lake` mutation was performed.

## Commands and results

All repository commands ran at the repository root unless `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0762` | 0 | rank 1348; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `Formalizations/Lean/.lake` was initially untracked; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 5612,5617 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded `rg` searches in the repository and pinned mathlib | 0 for exact-topic hits; 1 for the expected repo-local no-match | mathlib supplies CFG definitions and reversal closure; no repo-local THM-M-0762 formalization was found; this is intake discovery, not an exhaustive anchor audit |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` and `git ... status --short` | 0 | pinned revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, clean package source |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...85b1d2` and `321626c8...2d81`, as recorded in `instance.json` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0762/IntakeProbe.lean)` | 0 | nine language/CFG/reversal interfaces elaborated; `Language.IsContextFree.reverse` reported `[propext, Classical.choice, Quot.sound]`; complete output SHA-256 `320921c25c5c868f9699d3f4eeff9488ee290d15236305f9c349b764f4782737` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 each | all structured records valid after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0762-pycache python3 -m py_compile Stage1_Instances/THM-M-0762/check_intake.py` | 0 | scoped checker compiles without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0762/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and dependency pins, H5/M3/R4 null-root boundary, exact inventory, receipt/packet agreement, pinned probe, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0762/check_intake.py` | 0 | public replay mode passes without the scheduler-only root packet |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0762` | 1 (expected no match) | no prohibited Lean proof escape or bodyless declaration; diagnostic `#print axioms` is permitted |
| per-file `git diff --no-index --check /dev/null` for every new owned file and the worker packet | 0 after treating exit 1 as the expected new-file difference | no whitespace diagnostics |
| `git diff --check -- Stage1_Instances/THM-M-0762 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0762-INTAKE` only. It supports a truthful
`planned` dossier, not a master-accepted node receipt. An immutable exact source, operation-set and
polarity selection, independent source review, canonical Lean elaboration and statement mutations,
anchor and provenance audit, discovery and obligation freezes, typed graphs, proof, composition,
trust closure, readable reconstruction, hermetic replay, deterministic release bundle, and
independent verification remain open. They prevent theorem completion but do not invalidate the
planned intake.
