# THM-M-1228 proof-phase recheck at `3f5b3108` (slot 24)

Item: `S56-M-1228-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `3f5b310884eb802487a4c901cb0d76752e368da0`

Base tree: `a1bb0a117c463908411f55d51fdb5ed25c457ab0`

## Verdict

`blocked`. No placeholder-free positive proof body can inhabit the exact frozen
target without changing its meaning. The canonical declaration has type

```text
CaffarelliKohnNirenbergTarget : CKNSourceSemantics -> Prop
```

and all three fields of `CKNSourceSemantics` are unconstrained predicates. A
premise-free declaration with a parameter `S : CKNSourceSemantics` would be
universally generalized and would establish

```text
forall S : CKNSourceSemantics, CaffarelliKohnNirenbergTarget S.
```

The tracked, placeholder-free `ProofBlocker.lean` selects a permitted
interpretation in which suitability is true and the required measure-zero
predicate is false. Trust-zero Lean replay checks

```text
counterexampleTargetIsFalse :
  Not (CaffarelliKohnNirenbergTarget counterexampleSemantics)

noUniformTargetProof :
  Not (forall S : CKNSourceSemantics, CaffarelliKohnNirenbergTarget S)
```

with only `[propext, Classical.choice, Quot.sound]`. This refutes the universal
closure of the arbitrary semantic interface, not the mathematical
Caffarelli-Kohn-Nirenberg theorem. Selecting favorable semantics, assuming the
per-solution conclusion, storing that conclusion in a structure field, or
replacing parabolic by Euclidean Hausdorff measure would prove a substituted
theorem and was not done.

The proof dependency is unfinished: the authoritative DAG records
`S56-M-1228-OBLIGATION_TREE` as provisional `[_]`, not accepted `[x]`.
`ObligationTree.root_compose` is only conditional binder assembly and assumes
the entire open per-solution analytic conclusion. The frozen root cut has no
positive terminal bodies:

- `M1228-S-CONCRETE`
- `M1228-E-EPSILON`
- `M1228-C-COVER`
- `M1228-L-MEASURE`

The bounded anchor audit locates no exact terminal proof in the repository,
pinned dependency closure, or four immutable external trees. All proof-relevant
inputs are byte-for-byte unchanged from the prior `ec3b52a2` recheck; current
HEAD only integrates that earlier evidence pair.

Two predecessor evidence defects remain fail-closed. `check_statement.py` does
not elaborate or compare `MutationChangedSpatialDimension`, although it appends
that name to `killed_mutations`. All fifteen structured node recipes invoke the
same conditional `ObligationTree.lean` harness, which contains no analytic proof
bodies and therefore cannot validate the analytic nodes it names. A proof
worker may not rewrite those predecessor artifacts, the authoritative DAG, or
the generated checklist.

There were already 30 JSON and 30 Markdown proof-recheck packets before this
run, while the DAG still records zero proof attempts and no children. This is
well beyond the section 10.2 five-tick split threshold. The master must
reconcile the repeated packets and split the repair and analytic obligations
instead of scheduling another identical oversized proof attempt.

The root remains `H1/M4/R4`; the assigned item remains `[ ]`. No positive proof
body, closed obligation, receipt, audit completion, theorem completion, or
master acceptance is claimed.

## Validation

All commands ran from this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, checkout,
network action, or `.lake` mutation was performed. The narrow replay copied its
Lean inputs below `/tmp`, wrote its `.olean` there, and removed all temporary
compilation output on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1228` | 0 | Rank 156; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `timeout 300 python3 Stage1_Instances/THM-M-1228/check_statement.py` | 0 | Expression SHA-256 `101ce8f2cda8c25d5a0b9ce0e94560f8b801d011c06912d5e53eb698ecf58e5f`; toolchain and mathlib pin agree. Its spatial-dimension mutation claim remains underchecked as described above. |
| `timeout 300 python3 Stage1_Instances/THM-M-1228/check_anchor_audit.py` | 0 | `ok: M4 boundary, nine Lean probes, mathlib pin, and four immutable external tree receipts` |
| `timeout 300 python3 Stage1_Instances/THM-M-1228/check_obligation_tree.py` | 0 | `PASS`: 15 obligations and 31 typed edges; denominator `25704bee664136645e0481ae7d6273ac3fdfd2f1cd20fc5f82ba43f07066f41e`; root open at M4 with a four-obligation cut. |
| `(cd Formalizations/Lean && LAKE_NO_UPDATE=1 timeout 60 lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| Narrow `lake env lean --trust=0 -t0` replay below | 0 | The exact statement, both negative declarations, and conditional composition elaborated; all three proof declarations reported `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\\b(?:sorry|admit|axiom)\\b|sorryAx|^[[:space:]]*unsafe\\b' Stage1_Instances/THM-M-1228 --glob '*.lean'` | 1 | Expected no-match: no prohibited proof-gap or unsafe declaration occurs in the owned Lean files. |
| `git diff --exit-code ec3b52a2..HEAD -- <proof-relevant inputs>` | 0 | Statement, countermodel, composition harness, and structured proof inputs are unchanged since the preceding applicable replay. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse 'HEAD^{tree}'` | 0 | `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD` | 0 | Manifest-pinned `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` |
| `python3 -m json.tool Stage1_Instances/THM-M-1228/proof-recheck-2026-07-15-head-3f5b3108-slot24.json >/dev/null` | 0 | The current-base structured blocker is valid JSON. |
| Scoped blocker invariant check | 0 | Identity, base revision/tree, blocked verdict, `[ ]` state, unchanged H1/M4/R4 vector, false completion fields, empty receipts, root cut, changed paths, and self-test absence agree. |
| `git diff --check -- Stage1_Instances/THM-M-1228 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics in the scoped tracked diff. |
| `git diff --no-index --check /dev/null <new packet>` | 1 each | Expected content-difference exits with empty output for both new files, so neither has whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The successful narrow replay was:

```bash
set -euo pipefail
ROOT=$PWD
TARGET=$ROOT/Stage1_Instances/THM-M-1228
TMP=$(mktemp -d /tmp/thm-m-1228-proof-3f5b3108-slot24.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
LEAN_BIN=$(cd Formalizations/Lean && LAKE_NO_UPDATE=1 \
  timeout --kill-after=5s 60s lake env which lean)
LEAN_PATH_BASE=$(cd Formalizations/Lean && LAKE_NO_UPDATE=1 \
  timeout --kill-after=5s 60s lake env printenv LEAN_PATH)
cp "$TARGET/Statement.lean" "$TARGET/ProofBlocker.lean" \
  "$TARGET/ObligationTree.lean" "$TMP"/
LEAN_PATH="$LEAN_PATH_BASE" LEAN_NUM_THREADS=1 \
  timeout --foreground --kill-after=5s 300s \
  "$LEAN_BIN" --trust=0 -t0 --root="$TMP" \
  -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_PATH="$TMP:$LEAN_PATH_BASE" LEAN_NUM_THREADS=1 \
  timeout --foreground --kill-after=5s 300s \
  "$LEAN_BIN" --trust=0 -t0 --root="$TMP" "$TMP/ProofBlocker.lean"
LEAN_PATH="$LEAN_PATH_BASE" LEAN_NUM_THREADS=1 \
  timeout --foreground --kill-after=5s 300s \
  "$LEAN_BIN" --trust=0 -t0 --root="$TMP" "$TMP/ObligationTree.lean"
```

Replay SHA-256 values:

- statement stdout: `e2149c8788a7c04dcd2fb74033416a6d52283db3762d11de097377e70842961b`
- countermodel stdout: `392f43d6df0dabab37d8684708f8f6a9e68d42302a0b7363c39cfdb81c0002fe`
- composition stdout: `c8e3c1cb271c2c574815fe19833cf612f106a2e7f054194a18d865bf652c5dd2`
- each stderr: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- temporary `Statement.olean`: `9a3d95793e0a82db705fcdb47fa6c9789c9f092caee9e3abda78e6f85d704cc2`
- Lean executable: `3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf`

Input SHA-256 values:

- `Statement.lean`: `e5360836f4875e028eabdbf3e76c860aa1566a0f2f4eeb1487588c6ee55ddcc5`
- `ProofBlocker.lean`: `b7c0043752d40a41350080fe5210b65aca2594a2c8cdbae139c3ab058ffacca5`
- `ObligationTree.lean`: `850cb3402e9c9c91fee41fefd6264f30681a172cc87757b29ed1c33beec34fe7`
- `obligation-registry.json`: `90e618e7ead41d98804da85b81e7d8e0d366a322b62da0680b9d82043c66892b`
- `typed-graphs.json`: `41e601f13842fd84bc9b7ffcfdeab5cbfa415806836ebe0908e7493dc5ad4330`
- `anchor-audit.json`: `8d18f2332859b387552de7370c72674407d61f7260eb4dd476856694f7a7ba32`
- `validation-specs.json`: `8bc384e7935c1728f703811336580989e3b59f78317c67e6cd9914d5145b318b`

## Retry Condition

Master-reconcile the repeated attempts and repair or accept the predecessor as
appropriate. Reopen and version the statement around fixed, source-faithful
definitions of suitable weak Navier-Stokes solutions, regular points, and
one-dimensional parabolic Hausdorff measure. Complete the source and mutation
gates, freeze a corrected registry with node-accurate validation recipes, and
split the proof into dependency-legal child tasks. Then implement
placeholder-free local bodies or immutably pin exact compatible bodies for all
four root-cut obligations, with checked transports, composition, trust, and
terminal-body provenance.

Because the positive proof phase is not genuinely self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent.
