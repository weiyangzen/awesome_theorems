# Statement validation record

Item: `S56-M-1270-STATEMENT`  
Base revision: `67392d9b9aeb94afc0b864b86ce8cdd8ace153ad`

## Frozen target

`Stage1Instances.THM_M_1270.EkelandVariationalPrincipleTarget` freezes the intake-selected
real-valued, two-parameter complete-metric-space form. The pointwise approximation premise avoids
making `sInf` the public interface; the checked theorem `target_iff_infimum_target` proves that the
infimum encoding is equivalent under the root's `BddBelow (range f)` premise.

The only direct import is `Mathlib.Topology.Semicontinuity.Basic`. The three separately printed
mutations remove completeness, remove lower semicontinuity, or weaken strict minimality. They are
review surfaces only and are not theorem counterexamples or replacements for the canonical root.

## Commands and results

All commands ran inside this worker clone on 2026-07-12 (Asia/Shanghai). Lean ran from
`Formalizations/Lean` through the existing pinned Lake environment. No dependency update, fetch,
clone, or broad build command was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1270` | 0 | rank 163, planned, L0/rework-required, historical artifacts unaccepted, theorem incomplete |
| `lake env lean ../../Stage1_Instances/THM-M-1270/Statement.lean` | 0 | canonical and infimum targets, checked equivalence, and three mutations elaborated; explicit propositions printed |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-1270/Statement.lean lean-toolchain lake-manifest.json` | 0 | final hashes recorded in `statement.json` |
| `python3 -m json.tool Stage1_Instances/THM-M-1270/statement.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1270 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is statement-only worker evidence pending master acceptance. Source-complete H0 review,
anchor audit, obligation tree, proof, validation, release, and theorem completion remain open.
