# Intake validation record

Base revision: `43b8783c62005322690acf2bed800ea3acbd76c6`.

Commands run from the repository root unless a `cwd` is shown. This intake introduces no Lean
declaration; compiling the legacy file only confirms that the cited discovery surface elaborates.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0450` | 0 | rank 92, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0450/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_092.lean` | 0 | historical statement-shape and descent-anchor file elaborated; Lake cloned the pinned `flt-regular` and mathlib dependencies into this worker clone |
| `git diff --check -- Stage1_Instances/THM-M-0450` | 0 | no whitespace errors |

These checks establish only the intake node's structural and discovery claims. Master acceptance
and every dependent phase remain outstanding.
