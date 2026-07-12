# Intake validation record

Base revision: `562c428c3d520ab42bba305174b7cad9409d7c0b`.

Validation is scoped to target membership, planned-instance invariants, JSON
syntax, pinned Lean API discovery, forbidden proof escapes, and whitespace. It
does not test or claim an exact de la Vallee Poussin statement or proof.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0499` | 0 | rank 876; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0499/instance.json >/dev/null` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0499/task-dag.json >/dev/null` | 0 | valid JSON |
| scoped Python assertions over `instance.json`, `task-dag.json`, and directory entries | 0 | `intake invariant check: ok`; IDs, rank, lifecycle, file inventory, empty accepted state, open downstream tasks, and absent expression/completion claims agree |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0499/IntakeProbe.lean)` | 0 | pinned environment elaborated `Nat.primeCounting`, `Real.log`, `Real.sqrt`, `Real.exp`, `Filter.atTop`, and `Asymptotics.IsBigO` |
| `rg -n '\b(sorry\|axiom)\b' Stage1_Instances/THM-M-0499 --glob '!validation.md'` | 1 | no matches; exit 1 is ripgrep's no-match result |
| `git diff --check -- Stage1_Instances/THM-M-0499` | 0 | no whitespace errors |

The Lean output confirms only the types of these statement-building APIs. In
particular, `Nat.primeCounting` has type `Nat -> Nat`, while `IsBigO` is generic
over a filter and normed codomains. This does not choose or prove the required
real/natural transport or logarithmic-integral definition.

Known downstream failures are deliberate and fail closed: a hashed pinpoint
primary source and errata review, exact `Li` normalization, canonical Lean
expression and expression hash, statement mutation tests, formal-candidate
audit, obligation registry, proof, source/readability review, hermetic replay,
and independent validation remain open. Master acceptance is also outstanding.
