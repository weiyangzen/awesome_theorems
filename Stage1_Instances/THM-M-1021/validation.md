# Intake validation record

Base revision: `d6333f8365b25d4e77164d475fe735a47cf1e37d`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1021` | 0 | rank 497, planned, L0/rework-required, historical artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1021/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '\b(sorry|placeholder)\b' Stage1_Instances/THM-M-1021/{README.md,intake.json,source_statement_crosswalk.md}` | 1 | no matches (`rg` exit 1 means no match) |
| `git diff --check -- Stage1_Instances/THM-M-1021` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. The dossier uses
the word `axiom` only when honestly describing the still-open trust audit; it
contains no Lean source or declaration. No kernel proof result is claimed.

## Statement phase validation

Validation date: 2026-07-12. Worker base revision:
`aaeade67ccb391b2d10e50e766d54427324b3090`.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1021/BochnerStatement.lean` | 0 | both `#check` commands report `BochnerTarget : (Real -> Complex) -> Prop`; no diagnostics |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && git -C .lake/packages/mathlib rev-parse HEAD` | 0 | pinned reused mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && sha256sum lake-manifest.json ../../Stage1_Instances/THM-M-1021/BochnerStatement.lean` | 0 | manifest `321626c...2d81`; Lean source `e17aaf13...2cd` |
| append three `#print` commands to a `/tmp` copy, then `cd Formalizations/Lean && lake env lean -Dpp.universes=true -Dpp.all=false /tmp/THM-M-1021-print.lean` | 0 | printed all three unfolded definitions; output SHA-256 `5b397ee9de0936db2c62ba953794ee0c2b9dc3192370aa06825fdf4aafc8322b` |

The single import is sufficient in the pinned environment; no dependency was
downloaded or changed. This phase validates proposition elaboration only. It
does not validate a proof, an anchor, source fidelity beyond the accepted
intake scope, or theorem completion.
