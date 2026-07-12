# Intake validation record

Base revision: `63728668acb87acd4bab7e755151dce89dc1eeb4`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0152` | 0 | rank 651, planned, L0/rework-required, no accepted legacy artifacts, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, release build |
| `rg -n -i 'gaussian curvature\|Gauss curvature\|Theorema\|sectionalCurvature\|sectional curvature\|local isometr' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | Matches were unrelated uses of "theorem" and a Prime Number Theorem note; no relevant geometry declaration was found |
| `python3 -m json.tool` on `instance.json` and `task-dag.json` | 0 | Both structured intake artifacts parse as JSON |
| dossier file-presence assertion | 0 | `README.md`, `scope-map.md`, `source-statement-crosswalk.md`, `instance.json`, and `task-dag.json` exist and are nonempty |
| forbidden Lean escape-marker scan over the owned path | 0 | No forbidden proof escape marker occurs |
| `git diff --check -- Stage1_Instances/THM-M-0152 .stage1-worker-selftest.json` | 0 | No whitespace errors |

The existing `.lake` link in this worker clone points at canonical pinned artifacts and was not
modified. No dependency update, build, fetch, or clone was run. The Lean command validates the
pinned executable only: intake introduces no Lean declaration, so no kernel theorem result is
claimed.

## Validation-phase execution

Item `S56-M-0152-VALIDATION` was self-tested at base revision
`e51894725a43642d26ce16e4aad3abaf28393de7` on 2026-07-12. The exact frozen
statement and the proof phase's sole closure, `M0152-B-ORIENTATION`, were
re-elaborated. `Validation.lean` independently reconstructs the same quotient
identity by simplification rather than the proof module's ring normalization.
`check_validation.py` independently checks frozen hashes, all 17 registry/graph
identities, root relevance and open-root boundary, toolchain pins, placeholder
policy, elaboration, and axiom reports.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0152
  exit 0: execution rank 651; planned; theorem_complete=false
cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0152/Statement.lean
  exit 0: exact target elaborated
cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0152/Proof.lean
  exit 0: proof reports propext, Classical.choice, and Quot.sound
cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0152/Validation.lean
  exit 0: independent exact branch proof reports the same three axioms
python3 Stage1_Instances/THM-M-0152/check_obligation_tree.py
  exit 0: 17 obligations and 41 typed edges passed; root open M4
python3 Stage1_Instances/THM-M-0152/check_validation.py
  exit 0: statement and exact orientation proof re-elaborated; independent
  probe passed; root remains open
```

These commands reused the existing canonical pinned `.lake` artifacts without
update, build, fetch, clone, or network use. This is truthful partial
validation, not full-root success. The first failed node gate is the open proof
dependency: `M0152-L-INTRINSIC-FORMULA` and `M0152-T-INVARIANCE` remain the
minimal M4 root cut, and no root composition exists. Consequently hermetic cold
replay, distinct-runner attestation, complete root provenance/trust closure,
H0/R0 review, and release evidence are not claimed. `audit_complete=false` and
`theorem_complete=false`; the root vector remains `[H1, M4, R3]`.
