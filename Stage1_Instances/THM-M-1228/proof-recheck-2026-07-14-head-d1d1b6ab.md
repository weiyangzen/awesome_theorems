# THM-M-1228 proof-phase recheck at `d1d1b6ab`

Item: `S56-M-1228-PROOF`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `d1d1b6abb3bf227c43ebb3ce0513779bc96d6294`

Base tree: `c8009994d3b72ece76326dd39eaf0262255cb6a1`

## Verdict

`blocked`. The frozen declaration is the family

```text
CaffarelliKohnNirenbergTarget S =
  forall D, S.IsSuitableWeakSolution D ->
    S.ParabolicHausdorffOneMeasureZero (SingularSet S D).
```

The three predicates in `CKNSourceSemantics` are unconstrained. The tracked,
placeholder-free `ProofBlocker.lean` selects a permitted interpretation with
suitability true and the measure-zero predicate false. Lean kernel-checks

```text
counterexampleTargetIsFalse :
  Not (CaffarelliKohnNirenbergTarget counterexampleSemantics)

noUniformTargetProof :
  Not (forall S : CKNSourceSemantics, CaffarelliKohnNirenbergTarget S)
```

at trust level zero. Therefore no uniform positive body can inhabit the frozen
interface. This is a statement-interface countermodel, not a refutation of the
mathematical Caffarelli-Kohn-Nirenberg theorem. Proving a convenient semantic
specialization, assuming the per-solution conclusion, or replacing parabolic
Hausdorff measure with Euclidean Hausdorff measure would substitute a different
theorem and was not done.

The predecessor registry remains open at `M4`; this worker does not modify its
statement, registry, graphs, or task state. The checked countermodel is `M5`
blocker evidence for the current interface pending versioned repair and master
reconciliation. The frozen root cut remains:

- `M1228-S-CONCRETE`
- `M1228-E-EPSILON`
- `M1228-C-COVER`
- `M1228-L-MEASURE`

No positive proof body, proof receipt, accepted obligation, audit completion,
validation completion, release result, or theorem-completion claim is made.
The assigned item remains `[ ]`.

## Validation

All commands ran in this worker clone using the automation-provided symlink to
the canonical pinned `.lake` artifacts. No `lake update`, `lake build`,
dependency clone/fetch, network action, or `.lake` mutation was performed. The
untracked link makes this nonrelease evidence. Temporary elaboration output was
created under `/tmp` and removed on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1228` | 0 | Rank 156; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; baseline `L0/rework_required`; theorem incomplete. |
| `timeout 300 python3 Stage1_Instances/THM-M-1228/check_statement.py` | 0 | Expression SHA-256 `101ce8f2cda8c25d5a0b9ce0e94560f8b801d011c06912d5e53eb698ecf58e5f`; all four registered mutations killed; pins agree. |
| `python3 Stage1_Instances/THM-M-1228/check_anchor_audit.py` | 0 | `ok: M4 boundary, nine Lean probes, mathlib pin, and four immutable external tree receipts`. |
| `python3 Stage1_Instances/THM-M-1228/check_obligation_tree.py` | 0 | `PASS`: 15 obligations and 31 typed edges; denominator `25704bee664136645e0481ae7d6273ac3fdfd2f1cd20fc5f82ba43f07066f41e`; root open at M4 with a four-obligation analytic cut. |
| Narrow `lake env`/Lean `--trust=0 -t0` recipe below | 0 | The exact statement and both negative declarations elaborated. Each negative declaration reported `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\\b(?:sorry|admit|axiom)\\b|sorryAx|^[[:space:]]*unsafe\\b' Stage1_Instances/THM-M-1228 --glob '*.lean'` | 1 | Expected no-match: no prohibited proof-gap or unsafe declaration in the owned Lean files. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `python3 -m json.tool Stage1_Instances/THM-M-1228/proof-recheck-2026-07-14-head-d1d1b6ab.json >/dev/null` | 0 | The current-base blocker packet is valid JSON. |
| Scoped blocker invariant `jq -e` check | 0 | IDs and base identity agree; verdict is blocked; state stays `[ ]`; proof, root, audit, and theorem completion are false; accepted receipts are empty; and the four-node cut set is unchanged. |
| `git diff --check -- Stage1_Instances/THM-M-1228 .stage1-worker-selftest.json` | 0 | No scoped whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion self-test manifest is deliberately absent. |

The exact narrow Lean recipe, run from the repository root, was:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-1228-proof-d1d1b6ab.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
lean_bin=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 timeout 300 "$lean_bin" \
  --trust=0 -t0 -o "$tmp/Statement.olean" \
  Stage1_Instances/THM-M-1228/Statement.lean
LEAN_PATH="$tmp:$lean_path" LEAN_NUM_THREADS=1 timeout 300 "$lean_bin" \
  --trust=0 -t0 Stage1_Instances/THM-M-1228/ProofBlocker.lean
```

Input SHA-256 values:

- `Statement.lean`: `e5360836f4875e028eabdbf3e76c860aa1566a0f2f4eeb1487588c6ee55ddcc5`
- `ProofBlocker.lean`: `b7c0043752d40a41350080fe5210b65aca2594a2c8cdbae139c3ab058ffacca5`
- `ObligationTree.lean`: `850cb3402e9c9c91fee41fefd6264f30681a172cc87757b29ed1c33beec34fe7`
- `statement.json`: `5719d54346cc641c61a7f5346fd902757c9db55f72c8eaa18a8dd5e5a31d8a8d`
- `obligation-registry.json`: `90e618e7ead41d98804da85b81e7d8e0d366a322b62da0680b9d82043c66892b`
- `typed-graphs.json`: `41e601f13842fd84bc9b7ffcfdeab5cbfa415806836ebe0908e7493dc5ad4330`
- `anchor-audit.json`: `8d18f2332859b387552de7370c72674407d61f7260eb4dd476856694f7a7ba32`
- `validation-specs.json`: `8bc384e7935c1728f703811336580989e3b59f78317c67e6cd9914d5145b318b`

## Retry Condition

Reopen and version the statement around fixed, source-faithful definitions of
suitable weak Navier-Stokes solutions, regular points, and one-dimensional
parabolic Hausdorff measure. Freeze a corrected registry with an append-only
delta, then implement placeholder-free local bodies or immutably pin exact
compatible bodies for all four root-cut obligations, including checked
transports, child composition, and terminal-body provenance.

Because the positive proof phase is not genuinely self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent.
