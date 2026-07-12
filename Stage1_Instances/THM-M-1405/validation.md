# Intake validation

Base revision: `028e2535b68678b8296e63e2cacb05ed9775a2d8` (tree
`2845b046547e71984e5d93f4f04045663bd3bcbb`).

Validation date: `2026-07-12` (`Asia/Shanghai`). This phase covers target membership, dossier
structure, JSON integrity, planned-state invariants, a bounded target-name search, and a narrow
pinned Lean API probe. The existing `Formalizations/Lean/.lake` dependency artifacts were present
before this work and used read-only; no update, build, clone, or fetch was run.

Because no exact primary-source proposition is selected, no canonical target, expression hash,
statement mutation result, human-source acceptance, or proof is claimed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1405` | 0 | rank 904, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short` | 0 | only the pre-existing shared `Formalizations/Lean/.lake` link was untracked; it was preserved and excluded from this packet |
| `python3 -m json.tool Stage1_Instances/THM-M-1405/instance.json >/dev/null` | 0 | syntactically valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1405/task-dag.json >/dev/null` | 0 | syntactically valid JSON |
| scoped Python intake assertions | 0 | `THM-M-1405 intake invariant check: ok`; exact identity, null target, provisional vector, artifact inventory, and six-node open dependency chain agree |
| `rg -n -i '\b(sinai\|kolmogorov.?sinai\|measure.?theoretic entropy\|metric entropy\|generating partition\|entropy of.*partition\|partition entropy)\b' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no target-specific name match; expected negative bounded search, not a complete anchor audit |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1405/IntakeProbe.lean)` | 0 | six adjacent APIs elaborated under pinned Lean 4.29.0 and mathlib |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-1405 --glob '*.lean'` | 1 | no prohibited placeholder, bodyless axiom, or match; expected negative scan |
| `git diff --check -- Stage1_Instances/THM-M-1405` | 0 | no whitespace errors |
| scoped Python loop invoking `git diff --no-index --check /dev/null <new-file>` for every dossier artifact | 0 | `new-file whitespace check: ok`; untracked file contents were checked directly |

All source, statement, anchor-audit, obligation, proof, hermetic-replay, independent-verification,
and master-acceptance gates beyond this planned intake remain open. They prevent theorem completion
but do not invalidate a truthful intake dossier.
