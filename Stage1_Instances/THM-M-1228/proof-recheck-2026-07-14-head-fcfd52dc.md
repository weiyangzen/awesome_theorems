# THM-M-1228 proof-phase recheck at `fcfd52dc`

Item: `S56-M-1228-PROOF`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `fcfd52dc69db3bf455310be55903278133a15a10`

Base tree: `3580154b2d6b61f9bfee3079ce78939155de16ca`

## Verdict

`blocked`. No legal positive proof body can inhabit the frozen formal target as
the assigned Caffarelli-Kohn-Nirenberg source theorem. The declaration is the
under-specified family

```text
CaffarelliKohnNirenbergTarget S =
  forall D, S.IsSuitableWeakSolution D ->
    S.ParabolicHausdorffOneMeasureZero (SingularSet S D).
```

The three predicates in `CKNSourceSemantics` are unconstrained. The tracked,
placeholder-free `ProofBlocker.lean` supplies a permitted interpretation in
which suitability is true and the measure-zero predicate is false. Lean checks

```text
counterexampleTargetIsFalse :
  Not (CaffarelliKohnNirenbergTarget counterexampleSemantics)

noUniformTargetProof :
  Not (forall S : CKNSourceSemantics, CaffarelliKohnNirenbergTarget S)
```

Thus a positive proof uniform over the current interface would contradict a
checked countermodel. This refutes only the under-specified interface, not the
mathematical Caffarelli-Kohn-Nirenberg theorem. Proving a convenient
specialization, assuming the per-solution conclusion, or replacing parabolic
Hausdorff measure with ambient Euclidean Hausdorff measure would substitute a
different theorem and was not done. `ObligationTree.root_compose` merely
consumes the complete open per-solution analytic conclusion. It is also stated
over a duplicated harness interface rather than the canonical declaration;
there is no checked transport between the two structures. It earns no root
proof credit.

The predecessor registry stays open at `M4`; this proof worker does not rewrite
its statement, registry, graphs, or task state. The current interface has
checked `M5` blocker evidence pending a versioned correction and master
reconciliation. The frozen dossier labels the following coarse blocker
frontier as its root cut:

- `M1228-S-CONCRETE`
- `M1228-E-EPSILON`
- `M1228-C-COVER`
- `M1228-L-MEASURE`

These four IDs are not a sufficient completion set by themselves. Their
required children, the terminal per-solution conclusion, exact composition,
and all remaining proof-critical nodes also stay open.

No positive proof body, receipt, accepted obligation, audit completion,
validation completion, release result, or theorem-completion claim is made.
The assigned item remains `[ ]`.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`.lake` symlink points to canonical pinned artifacts, so this is nonrelease
evidence. No `lake update`, `lake build`, dependency clone/fetch, network
action, or `.lake` mutation was performed. Temporary elaboration outputs were
created below `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1228` | 0 | Rank 156; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `timeout 300 python3 Stage1_Instances/THM-M-1228/check_statement.py` | not credited | The multi-probe checker was stopped without a result under severe shared-runner contention. This attempt claims no fresh mutation-suite success; the exact statement source was instead elaborated by the narrow trust-zero recipe. |
| `python3 Stage1_Instances/THM-M-1228/check_anchor_audit.py` | 0 | `ok: M4 boundary, nine Lean probes, mathlib pin, and four immutable external tree receipts`. |
| `python3 Stage1_Instances/THM-M-1228/check_obligation_tree.py` | 0 | `PASS`: 15 obligations and 31 typed edges; denominator `25704bee664136645e0481ae7d6273ac3fdfd2f1cd20fc5f82ba43f07066f41e`; root open at M4 with a four-obligation cut. |
| Narrow `LAKE_NO_UPDATE=1 lake env` / Lean `--trust=0 -t0` recipe below | 0 | Exact statement and both negative declarations elaborated. `ProofBlocker.lean` printed `[propext, Classical.choice, Quot.sound]` for each negative declaration. |
| CKN/Navier-Stokes/parabolic-measure `rg` search in pinned mathlib | 0 | Only two unrelated meromorphic singular-set comments matched; no suitable weak solution, parabolic Hausdorff measure, epsilon regularity, or CKN terminal declaration was found. |
| `git log --all --format='%H' -- Stage1_Instances/THM-M-1228/Proof.lean` | 0 | Empty output: no positive target proof file occurs in repository history. |
| `rg -n --pcre2 '\b(?:sorry\|admit\|axiom)\b\|sorryAx\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-1228 --glob '*.lean'` | 1 | Expected no-match: no prohibited proof-gap or unsafe declaration in the owned Lean files. |
| `cd Formalizations/Lean && LAKE_NO_UPDATE=1 timeout 60 lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| JSON parse plus scoped blocker-invariant check | 0 | IDs/base, blocked `[ ]` state, false completion fields, empty receipts, changed paths, and four-node cut agree. |
| `git diff --check -- Stage1_Instances/THM-M-1228 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The exact narrow Lean recipe, run from the repository root, was:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-1228-proof-fcfd52dc.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean_path=$(cd Formalizations/Lean &&
  LAKE_NO_UPDATE=1 lake env printenv LEAN_PATH)
lean_bin=$(cd Formalizations/Lean && LAKE_NO_UPDATE=1 lake env which lean)
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
