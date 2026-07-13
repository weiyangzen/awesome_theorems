# Intake validation

Base revision: `113a7f4d7029a7905d85af76bec7896f679d8c52` (tree
`264a3a56a1cf2a90cd148082a358dd27edb2b0ea`). Validation date: `2026-07-13`
(`Asia/Shanghai`).

Validation is limited to target membership, repository-standard consistency, dossier structure,
JSON syntax, planned-state invariants, immutable input and worker-output hash checks, the pinned Lean substrate probe,
proof-hole hygiene, and whitespace. The source record does not determine a proposition, so an
invented giant-component expression would be substitution rather than validation. No canonical
target, expression hash, mutation certificate, theorem declaration, or proof is claimed.

The automation-provided `Formalizations/Lean/.lake` symlink exposes the canonical pinned artifacts.
It existed before this work and was used read-only. No update, build, dependency clone, fetch, or
`.lake` mutation was run.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0850` | 0 | rank 1405, planned, L0/rework_required, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0850/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0850/task-dag.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0850/intake-receipt.json` | 0 | valid JSON after finalization |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | valid JSON |
| `python3 -B Stage1_Instances/THM-M-0850/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned lifecycle, null target, H5/M4/R4 boundary, immutable inputs, worker-output hashes, six-task open chain, artifact inventory, and worker packet agree |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0850/IntakeProbe.lean)` | 0 | eight connected-component and binomial-random-graph APIs elaborated; no target theorem stated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| bounded pinned-mathlib search for giant/largest/random component declarations | 0 | only historical wording in `BinomialRandomGraph/Defs.lean`; no giant-component theorem found; not a complete anchor audit |
| scoped prohibited-declaration scan over `Stage1_Instances/THM-M-0850/*.lean` | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0850 .stage1-worker-selftest.json` | 0 | no tracked-diff whitespace errors; files are new, so a separate scoped byte check covered them |
| scoped final-newline/trailing-whitespace check over all owned files and `.stage1-worker-selftest.json` | 0 | all files ended with newline and had no trailing whitespace |

The bounded search used this literal command:

```bash
rg -n -i 'giant.{0,40}component|component.{0,40}giant|largest.{0,40}component|component.{0,40}largest|erd[oőö]s.{0,40}r[eé]nyi|random.{0,40}component|component.{0,40}random' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'
```

The two scoped hygiene rows used these literal commands (the `rg` no-match exit `1` is expected):

```bash
rg -n --glob '*.lean' '\b(sorry|admit)\b|\bsorryAx\b|^[[:space:]]*(axiom|constant|opaque|unsafe)\b' Stage1_Instances/THM-M-0850
python3 -c $'from pathlib import Path\npaths = [p for p in Path("Stage1_Instances/THM-M-0850").iterdir() if p.is_file()] + [Path(".stage1-worker-selftest.json")]\nfor path in paths:\n    data = path.read_bytes()\n    assert data.endswith(b"\\n"), path\n    assert b"\\r" not in data and b"\\x00" not in data, path\n    assert all(not line.endswith((b" ", b"\\t")) for line in data.splitlines()), path\nprint(f"scoped byte check: ok ({len(paths)} files)")'
```

Known downstream failures remain deliberately open: exact primary-source selection and independent
review; canonical statement elaboration and all required mutations; immutable formal anchor audit;
obligation and typed-graph freeze; proof; hermetic replay; deterministic evidence bundle; and
independent release verification. These prevent audit and theorem completion but do not invalidate
a truthful, self-tested `planned` intake proposal.
