# Intake validation

Base revision: `444860f481e8bbf64a3357008fd4d01a52006f08` (tree
`dee24a14497f877ebd81712a99d2da08de62d7ad`). Validation date: `2026-07-13`
(`Asia/Shanghai`).

Validation is limited to target membership, repository-standard consistency, dossier structure,
JSON syntax, planned-state invariants, immutable input checks, the pinned Lean substrate probe,
proof-hole hygiene, and whitespace. The source record does not determine a proposition, so an
invented graph-homomorphism-count expression would be substitution rather than validation. No
canonical target, expression hash, mutation certificate, theorem declaration, or proof is claimed.

The automation-provided `Formalizations/Lean/.lake` symlink exposes the canonical pinned artifacts.
It existed before this work and was used read-only. No update, build, dependency clone, fetch, or
`.lake` mutation was run.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0845` | 0 | rank 1400, planned, L0/rework_required, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0845/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0845/task-dag.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0845/intake-receipt.json` | 0 | valid JSON after finalization |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | valid worker-packet JSON |
| `python3 -B Stage1_Instances/THM-M-0845/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned lifecycle, null target, H5/M4/R4 boundary, immutable inputs, six-task open chain, artifact inventory, and worker packet agree |
| Crossref DOI metadata retrieval and JSON inspection | 0 | DOI, title, five authors, and pages 315-371 confirmed; JSON SHA-256 `99c855d805cd9572bf7f847e03638f4cb39f33c128b5e785c5b9b9fd4764de07` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0845/IntakeProbe.lean)` | 0 | graph-map, relation-fintype, and cardinality APIs elaborated; output SHA-256 `1232bd8bb9229894e0278d5f7553a78785f0f3435095be419cabe9a50636c209`; no target theorem stated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| bounded general graph-homomorphism-count search in pinned mathlib and repo-local Lean sources | 1 | expected no-match: no named general count or density theorem found; not a complete anchor audit |
| scoped prohibited-declaration scan over `Stage1_Instances/THM-M-0845/*.lean` | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0845 .stage1-worker-selftest.json` | 0 | no tracked-diff whitespace errors; files are new, so a separate scoped byte check covered them |
| scoped final-newline/trailing-whitespace check over all owned files and `.stage1-worker-selftest.json` | 0 | all files ended with newline and had no trailing whitespace |

The bounded search and scoped hygiene commands were:

```bash
rg -n -i --glob '*.lean' 'graph homomorphism count|homomorphism counting|counting graph homomorphism|homomorphism density|hom density|hom_count|homCount|homDensity|Lovasz.*homomorphism|Lovász.*homomorphism' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems
rg -n --glob '*.lean' '\b(sorry|admit)\b|\bsorryAx\b|^[[:space:]]*(axiom|constant|opaque|unsafe)\b' Stage1_Instances/THM-M-0845
python3 -c $'from pathlib import Path\npaths = [p for p in Path("Stage1_Instances/THM-M-0845").iterdir() if p.is_file()] + [Path(".stage1-worker-selftest.json")]\nfor path in paths:\n    data = path.read_bytes()\n    assert data.endswith(b"\\n"), path\n    assert b"\\r" not in data and b"\\x00" not in data, path\n    assert all(not line.endswith((b" ", b"\\t")) for line in data.splitlines()), path\nprint(f"scoped byte check: ok ({len(paths)} files)")'
```

Known downstream failures remain deliberately open: exact source selection and independent review;
canonical statement elaboration and all required mutations; immutable formal anchor audit;
obligation and typed-graph freeze; proof; hermetic replay; deterministic evidence bundle; and
independent release verification. These prevent audit and theorem completion but do not invalidate
a truthful, self-tested `planned` intake proposal.
