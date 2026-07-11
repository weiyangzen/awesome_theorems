# THM-M-0402 intake dossier

## Status boundary

This is a rev-5.6 `planned` intake instance at `L0 / rework_required`. It records no accepted proof state. `audit_complete` and `theorem_complete` are both false. The historical file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_015.lean` is discovery input only; its wrappers and prior build history receive no proof credit here.

## Scope map

The repository metadata names “Evertse theorem”, dates it to 1984, and describes it only as “the number of solutions of S-unit equations”. That label does not uniquely determine whether the intended root is the two-variable finiteness statement, a quantitative upper bound, or the general nondegenerate multi-term theorem.

The candidate boundary inherited for investigation is: a number field `K`, a finite set `S` of places containing the archimedean places, and S-units `x,y` satisfying `x + y = 1`; the solution set is finite. The statement phase must not silently replace a quantitative source theorem by this qualitative consequence. It must freeze the exact field/place conventions, any rank or cardinality parameters, degeneracy condition, and bound.

Out of scope are THM-M-0403's recurrence-zero theorem, the Schmidt Subspace Theorem as a substitute, arbitrary finite-set tautologies, and any special case presented as Evertse's full result.

## Source-statement crosswalk

| Record | Source locator | Source content | Target mapping | Intake status |
|---|---|---|---|---|
| SRC-LEGACY-01 | `Docs/researches/math_theorems.md`, Evertse entry | Jan-Hendrik Evertse; 1984; “S-unit equation solution count”; marked “verified” | Identifies topic and author only | Untrusted metadata; no theorem/page or assumptions |
| SRC-LEGACY-02 | `Docs/Stage1_Blueprint.md`, S1-M-015 | Selects Lean 4 lane and describes S-unit equation solution count | Scheduling and discovery scope | Not statement or proof evidence |
| SRC-PRIMARY-CANDIDATE-01 | J.-H. Evertse, *On sums of S-units and linear recurrences*, Compositio Math. 53 (1984), 225-244; NUMDAM `CM_1984__53_2_225_0` | Candidate primary proof source named by the legacy Lean artifact | Must be checked for exact theorem number, arity, hypotheses, degeneracy convention, and bound before H0 or statement freeze | Open; citation identified but pinpoint not yet verified |
| SRC-FORMAL-CANDIDATE-01 | `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_015.lean` | Models pairs of mathlib S-units and weighted/normalized equations | Candidate object-model input for the next statement phase | Legacy, unaccepted, and not a terminal proof |

The first failed downstream gate is the exact-statement gate: a primary-source theorem/page crosswalk and exact Lean expression fingerprint do not yet exist. Consequently the honest intake vector is `[H1, M4, R4]`.

## Intake validation receipt

Base revision: `a8d6489fd935cd71fa4499f2f3f5b051998203f4`.

Commands executed on 2026-07-12 (Asia/Shanghai):

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 15 assurance groups, 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0402
  exit 0: execution rank 15, planned, theorem_complete false
python3 -m json.tool Stage1_Instances/THM-M-0402/instance.json
  exit 0: valid JSON
git diff --check -- Stage1_Instances/THM-M-0402
  exit 0: no whitespace errors
```

No Lean proof validation is claimed or appropriate for this intake-only node. The next phase must elaborate the exact source-faithful target rather than inherit the old wrapper.
