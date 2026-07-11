# THM-M-0401 obligation-tree validation

Base revision: `72e8a2edc0088f19a59d40d8b64c51a5c9143981`.

This validation is scoped to the registry and typed architecture. It does not prove any
mathematical node. No dependency was fetched, built, updated, or modified.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: Stage1 rev-5.6 standard and 1546-target projection passed
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets; ranks 1..1546; all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0401
  exit 0: rank 14; lifecycle planned; theorem_complete=false
python3 Stage1_Instances/THM-M-0401/validate_obligation_tree.py
  exit 0: 14 obligations and 23 typed edges; frozen denominator hash matched; root remained open M4
python3 -m json.tool Stage1_Instances/THM-M-0401/obligation-registry.json
  exit 0
python3 -m json.tool Stage1_Instances/THM-M-0401/obligation-graphs.json
  exit 0
(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0401/Statement.lean)
  exit 1: unknown module prefix 'Mathlib'; the canonical symlinked .lake has no compiled Mathlib artifacts
git diff --check -- Stage1_Instances/THM-M-0401 .stage1-worker-selftest.json
  exit 0
```

The Lean replay failure is an environmental known failure already documented by the prerequisite
anchor audit. Worker policy forbids repairing it with `lake build`, `lake update`, clone, or fetch.
It prevents fresh statement elaboration in this phase, but not the real structural self-test of the
obligation-tree deliverable. The statement fingerprint is therefore inherited only from the
self-tested prerequisite statement artifact; no new kernel result is claimed.
