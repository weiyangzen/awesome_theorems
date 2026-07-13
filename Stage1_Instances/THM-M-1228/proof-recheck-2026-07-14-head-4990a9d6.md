# THM-M-1228 proof-phase recheck at `4990a9d6`

Item: `S56-M-1228-PROOF`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `4990a9d6fa09beb7747e6822c6543c6123ca7504`

Base tree: `b74497bc09c004757aa3974f3bb0622d77e20106`

## Verdict

`blocked`. No legal positive proof body can establish the exact frozen target
as the source theorem. The declaration is the family

```text
CaffarelliKohnNirenbergTarget S =
  forall D, S.IsSuitableWeakSolution D ->
    S.ParabolicHausdorffOneMeasureZero (SingularSet S D).
```

The three predicates in `CKNSourceSemantics` have no defining laws. The
tracked, placeholder-free `ProofBlocker.lean` chooses a permitted
interpretation in which suitability is true and the measure-zero conclusion
is false. Lean kernel-checks

```text
counterexampleTargetIsFalse :
  Not (CaffarelliKohnNirenbergTarget counterexampleSemantics)

noUniformTargetProof :
  Not (forall S : CKNSourceSemantics, CaffarelliKohnNirenbergTarget S)
```

at trust level zero. A convenient fixed interpretation could be chosen, but
that would not be the intended source-faithful CKN theorem. A proof uniform in
the current interface contradicts the checked countermodel. This refutes only
the under-specified interface, not the mathematical Caffarelli-Kohn-Nirenberg
theorem. Assuming the per-solution conclusion, importing the historical
abstract package, or replacing parabolic with ambient Hausdorff measure would
substitute or assume the requested result and was not done.

The frozen registry remains authoritative at `M4` until a versioned correction
and master reconciliation. It has no closed obligations. The root cut remains:

- `M1228-S-CONCRETE`
- `M1228-E-EPSILON`
- `M1228-C-COVER`
- `M1228-L-MEASURE`

No positive proof body, proof receipt, accepted obligation, audit completion,
validation completion, release result, or theorem-completion claim is made.
The assigned item remains `[ ]`.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`.lake` symlink points to canonical pinned artifacts, so this is nonrelease
evidence. This worker used `LAKE_NO_UPDATE=1` and did not run `lake update`,
`lake build`, clone, fetch, network access, or any dependency mutation.
Temporary Lean output was written under `/tmp` and removed on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1228` | 0 | Rank 156; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `timeout 300 python3 Stage1_Instances/THM-M-1228/check_statement.py` | 0 | Expression SHA-256 `101ce8f2cda8c25d5a0b9ce0e94560f8b801d011c06912d5e53eb698ecf58e5f`; all four registered mutations killed; pins agree. |
| `python3 Stage1_Instances/THM-M-1228/check_anchor_audit.py` | 0 | `ok: M4 boundary, nine Lean probes, mathlib pin, and four immutable external tree receipts`. |
| `python3 Stage1_Instances/THM-M-1228/check_obligation_tree.py` | 0 | `PASS`: 15 obligations and 31 typed edges; denominator `25704bee664136645e0481ae7d6273ac3fdfd2f1cd20fc5f82ba43f07066f41e`; root open at M4 with a four-obligation cut. |
| Narrow `LAKE_NO_UPDATE=1 lake env` / Lean `--trust=0 -t0` recipe below | 0 | Exact statement and both negative declarations elaborated. Each negative declaration reported `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\\b(?:sorry\|admit\|axiom)\\b\|sorryAx\|^[[:space:]]*unsafe\\b' Stage1_Instances/THM-M-1228 --glob '*.lean'` | 1 | Expected no-match: no prohibited proof-gap or unsafe declaration in the owned Lean files. |
| `cd Formalizations/Lean && LAKE_NO_UPDATE=1 timeout 30 lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `python3 -m json.tool Stage1_Instances/THM-M-1228/proof-recheck-2026-07-14-head-4990a9d6.json >/dev/null` and scoped `jq -e` blocker-invariant check | 0 | Structured blocker parses; IDs/base, blocked `[ ]` state, false completion fields, empty receipts, changed paths, and four-node cut agree. |
| `git diff --check --no-index /dev/null <each changed artifact>` | 1 for each file | Expected content-difference exit; no whitespace diagnostics were emitted. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The exact narrow Lean recipe, run from the repository root, was:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-1228-proof-4990a9d6.XXXXXX)
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
