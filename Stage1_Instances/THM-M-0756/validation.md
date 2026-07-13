# Intake validation

Base revision: `d05520867fab3367a9b61b9544c3e12241204f54` (tree
`fb2cfc62077d5b53e9938632cd6361dd60872067`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, topic/scope boundary,
source-statement crosswalk, open task DAG, structured/scoped invariants, and a narrow pinned Lean
API probe. It does not validate a canonical source statement or proof because the catalog gives no
truth-valued proposition. The automation-provided canonical `.lake` symlink was pre-existing and
used read-only; no dependency update, build, clone, fetch, or other `.lake` mutation was performed.
This dirty worker result is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; its package worktree was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0756` | exit 0; rank 1342, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | pre-edit exit 0; only the automation-provided `Formalizations/Lean/.lake` symlink existed; base revision/tree recorded above |
| inspect the target manifest, execution node, repository source, Stage0 projection, git provenance, and pinned computability/ordinal sources | exit 0; identified the scheduled topic-only target and adjacent APIs without selecting or crediting a proposition |
| `git blame -L 5570,5575 -- Docs/researches/math_theorems.md` | exit 0; all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | exit 0; pinned revision/tree recorded above; empty package status |
| `sha256sum` on the toolchain, lockfile, pinned computability, oracle, Turing-degree, and ordinal sources | exit 0; immutable input hashes recorded in `instance.json` and `intake-receipt.json` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0756/IntakeProbe.lean)` | exit 0; twelve adjacent partial-recursive, predicate, oracle, Turing-reduction, well-founded-recursion, and ordinal interfaces elaborated; no theorem declaration or proof body added; stdout SHA-256 `1cf99ee982f4d99308c45d5778010f75148c605d806fcd342b59e98732df4a00` |
| `rg -n -i 'hyperarithmetical\|hyperarithmetic\|hyperarith\|Hyperarithmetical\|Hyperarithmetic' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems -g '*.lean'` | exit 1 as expected for no match; bounded local search found no exact-topic Lean declaration; not a global absence or anchor-audit claim |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0756-pycache python3 -m py_compile Stage1_Instances/THM-M-0756/check_intake.py` | exit 0; scoped validator compiled without creating an owned generated file |
| `python3 -B Stage1_Instances/THM-M-0756/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; target/DAG identity, null canonical target, H5/M4/R4 boundary, artifact inventory, input hashes, worker packet, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0756` | exit 1 as expected for no match; no prohibited declaration or proof escape |
| `git diff --check -- Stage1_Instances/THM-M-0756 .stage1-worker-selftest.json` plus per-new-file `git diff --no-index --check /dev/null <new-file>` | exit 0 for the tracked check; every no-index command found only the expected new-file difference and no whitespace diagnostic |

## Known open gates

An immutable primary or approved authoritative source, exact proposition or definition decision,
pinpoint locator, incorporated definitions, assumptions, conclusion, proof boundary, correction and
errata disposition, translation, and independent review remain open. So do the classified object,
hierarchy or characterization presentation, recursive-ordinal and notation conventions, coding,
parameter policy, successor and limit rules, exact conclusion, ordered binders, hypotheses,
boundary cases, canonical Lean expression and environment fingerprints, checked transports,
statement mutations, discovery protocol, obligation registry, typed graphs, formal anchor/provenance
audit, proof and composition, trust closure, readable reconstruction, hermetic replay, deterministic
bundle, independent verification, master acceptance, audit completion, and theorem completion.
These failures do not invalidate a truthful self-tested `planned` intake.
