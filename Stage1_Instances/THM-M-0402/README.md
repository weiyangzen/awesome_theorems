# THM-M-0402 intake dossier

## Status boundary

This is a rev-5.6 `planned` intake instance at `L0 / rework_required`. It records no accepted proof state. `audit_complete` and `theorem_complete` are both false. The historical file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_015.lean` is discovery input only; its wrappers and prior build history receive no proof credit here.

## Scope map

The repository metadata names “Evertse theorem”, dates it to 1984, and describes it as “the number of solutions of S-unit equations”. The statement phase resolves this against Theorem 1 of Evertse's 1984 paper: finiteness of nondegenerate projective sums, specialized to S-units by `(c,d) = (1,0)`. This includes every positive projective dimension rather than silently substituting only the two-variable consequence.

The canonical Lean target uses a number field `K`, a finite set `S` of finite primes of its ring of integers, `n > 0`, and `n+1` mathlib S-units. It selects the unique projective representative with `x_0 = 1`, requires the full coordinate sum to vanish, and excludes every vanishing nonempty proper subsum. Infinite places are implicit in the number-field S-unit convention; mathlib's `S` records finite height-one primes.

Out of scope are THM-M-0403's recurrence-zero theorem, the Schmidt Subspace Theorem as a substitute, arbitrary finite-set tautologies, and any special case presented as Evertse's full result.

## Source-statement crosswalk

| Record | Source locator | Source content | Target mapping | Intake status |
|---|---|---|---|---|
| SRC-LEGACY-01 | `Docs/researches/math_theorems.md`, Evertse entry | Jan-Hendrik Evertse; 1984; “S-unit equation solution count”; marked “verified” | Identifies topic and author only | Untrusted metadata; no theorem/page or assumptions |
| SRC-LEGACY-02 | `Docs/Stage1_Blueprint.md`, S1-M-015 | Selects Lean 4 lane and describes S-unit equation solution count | Scheduling and discovery scope | Not statement or proof evidence |
| SRC-PRIMARY-CANDIDATE-01 | J.-H. Evertse, *On sums of S-units and linear recurrences*, Compositio Math. 53 (1984), 225-244; NUMDAM `CM_1984__53_2_225_0` | Candidate primary proof source named by the legacy Lean artifact | Must be checked for exact theorem number, arity, hypotheses, degeneracy convention, and bound before H0 or statement freeze | Open; citation identified but pinpoint not yet verified |
| SRC-FORMAL-CANDIDATE-01 | `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_015.lean` | Models pairs of mathlib S-units and weighted/normalized equations | Candidate object-model input for the next statement phase | Legacy, unaccepted, and not a terminal proof |

The exact statement now elaborates as `Stage1Instances.THMM0402.EvertseSUnitStatement` in `Statement.lean`. This closes only the provisional statement node; proof, anchor audit, source-review H0, and all completion gates remain open. The honest vector is `[H1, M3, R4]`.

## Statement source pinpoint

J.-H. Evertse, *On sums of S-units and linear recurrences*, Compositio Mathematica 53 (1984), 225-244, Theorem 1 on pages 226-227. The paper defines a finite place set containing all infinite places and `(c,d,S)`-admissibility in equation (6). Immediately before Theorem 1 it states that `(1,0,S)`-admissible projective coordinates may be chosen to be S-units. Theorem 1 asserts finiteness subject to equations (7) and (8), the total-sum and nonvanishing proper-subsum conditions. `Statement.lean` is precisely that specialization, with projective scaling normalized by `x_0 = 1`.

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

## Frozen obligation architecture

The obligation-tree phase freezes registry `THM-M-0402-OBLIGATIONS-v1` and seven typed graphs in
`obligation-registry.json` and `obligation-graphs.json`. The proof route keeps S-unit finite
generation, the nondegenerate unit-equation theorem, the multiplicative-group adapter, projective
normalization, exact specialization, and terminal composition as distinct required obligations.
Trust and proof-body provenance are separately root-relevant. No obligation is machine-closed, no
composition certificate exists, and theorem completion remains false. See `obligation-tree.md` for
the public node ledger and `obligation-tree-validation.md` for exact self-test evidence.
