# THM-M-1228 proof-phase recheck at `c887c8e5` (slot 25)

Item: `S56-M-1228-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `c887c8e5d7afe589d4b90386654421a60e998f51`

Base tree: `7a1298612a32286e2a542ffc410cf4de9bb1fabd`

## Verdict

`blocked`. No placeholder-free positive proof body can inhabit the exact frozen
target without changing its meaning. The canonical declaration has type

```text
CaffarelliKohnNirenbergTarget : CKNSourceSemantics -> Prop
```

and all three fields of `CKNSourceSemantics` are unconstrained predicates. A
premise-free declaration parameterized by `S : CKNSourceSemantics` would prove

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
`S56-M-1228-OBLIGATION_TREE` as provisional `[_]`, not accepted `[x]`. Its
registry assigns no positive proof body to the root or the frozen root cut:

- `M1228-S-CONCRETE`
- `M1228-E-EPSILON`
- `M1228-C-COVER`
- `M1228-L-MEASURE`

`ObligationTree.root_compose` is only a conditional binder-assembly theorem;
it assumes the complete per-solution analytic conclusion. The bounded anchor
audit still locates no exact terminal body in the repository, pinned dependency
closure, or four immutable external trees. The proof-relevant inputs are
unchanged since `c45f3c709`, so no new candidate has entered the closure.

Two predecessor evidence defects remain fail-closed. `check_statement.py`
reports `MutationChangedSpatialDimension` as killed without actually comparing
that declaration. All fifteen structured node recipes invoke the same
conditional `ObligationTree.lean` harness, which contains no analytic proof
bodies and cannot validate the analytic nodes it names. A proof worker may not
rewrite those predecessor artifacts, the authoritative DAG, or the generated
checklist.

There were already 40 JSON and 40 Markdown proof-recheck packets before this
run, while the DAG still records zero proof attempts and no children. This is
beyond the rev-5.6 five-tick split threshold. The master must reconcile these
packets and split statement repair from the four analytic obligations rather
than schedule another identical oversized proof attempt.

The vector remains `H1/M4/R4`; lifecycle remains `planned`; the assigned item
remains `[ ]`. No positive proof body, closed obligation, accepted receipt,
audit completion, theorem completion, or master acceptance is claimed.

## Validation

All commands ran inside this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts was reused
read-only. No Lake update/build, dependency clone/fetch, network action, or
`.lake` mutation was performed. The narrow replay copied its three Lean inputs
to a temporary directory under the worker root and removed all temporary output
on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1228` | 0 | Rank 156; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1228/check_statement.py` | 0 | Expression SHA-256 `101ce8f2cda8c25d5a0b9ce0e94560f8b801d011c06912d5e53eb698ecf58e5f`; toolchain and mathlib pin agree. Its spatial-dimension mutation claim remains underchecked as described above. |
| `python3 Stage1_Instances/THM-M-1228/check_anchor_audit.py` | 0 | `ok: M4 boundary, nine Lean probes, mathlib pin, and four immutable external tree receipts` |
| `python3 Stage1_Instances/THM-M-1228/check_obligation_tree.py` | 0 | `PASS`: 15 obligations and 31 typed edges; denominator `25704bee664136645e0481ae7d6273ac3fdfd2f1cd20fc5f82ba43f07066f41e`; root open at M4 with a four-obligation cut. |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| Narrow `lake env lean --trust=0 -t0` replay below | 0 | The exact statement, both negative declarations, and the conditional composition elaborated; all proof declarations reported `[propext, Classical.choice, Quot.sound]`. |
| Token-anchored prohibited-construct scan over owned Lean files | 1 expected | No `sorry`, `admit`, `sorryAx`, bodyless `axiom`, `unsafe`, `extern`, `implemented_by`, or `native_decide` token was found. |
| `git diff --exit-code c45f3c70..HEAD -- <proof-relevant inputs>` | 0 | Statement, blocker, composition, registry, graphs, anchor audit, and validation specs are unchanged. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD` | 0 | `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` |
| `git diff --check -- Stage1_Instances/THM-M-1228 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics before this packet was written. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The successful narrow replay was:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d "$root/.thm-m-1228-proof-c887c8e5.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
lean_bin=$(cd Formalizations/Lean && lake env which lean)
cp Stage1_Instances/THM-M-1228/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-1228/ProofBlocker.lean "$tmp/ProofBlocker.lean"
cp Stage1_Instances/THM-M-1228/ObligationTree.lean "$tmp/ObligationTree.lean"
cd "$tmp"
LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 timeout 300 "$lean_bin" \
  --trust=0 -t0 -o Statement.olean Statement.lean
LEAN_PATH=".:$lean_path" LEAN_NUM_THREADS=1 timeout 300 "$lean_bin" \
  --trust=0 -t0 ProofBlocker.lean
LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 timeout 300 "$lean_bin" \
  --trust=0 -t0 ObligationTree.lean
```

Replay stdout SHA-256 values were
`e2149c8788a7c04dcd2fb74033416a6d52283db3762d11de097377e70842961b`
(statement),
`392f43d6df0dabab37d8684708f8f6a9e68d42302a0b7363c39cfdb81c0002fe`
(countermodel), and
`c8e3c1cb271c2c574815fe19833cf612f106a2e7f054194a18d865bf652c5dd2`
(composition). Each stderr SHA-256 was
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

Input SHA-256 values:

- `Statement.lean`: `e5360836f4875e028eabdbf3e76c860aa1566a0f2f4eeb1487588c6ee55ddcc5`
- `ProofBlocker.lean`: `b7c0043752d40a41350080fe5210b65aca2594a2c8cdbae139c3ab058ffacca5`
- `ObligationTree.lean`: `850cb3402e9c9c91fee41fefd6264f30681a172cc87757b29ed1c33beec34fe7`
- `obligation-registry.json`: `90e618e7ead41d98804da85b81e7d8e0d366a322b62da0680b9d82043c66892b`
- `typed-graphs.json`: `41e601f13842fd84bc9b7ffcfdeab5cbfa415806836ebe0908e7493dc5ad4330`
- `anchor-audit.json`: `8d18f2332859b387552de7370c72674407d61f7260eb4dd476856694f7a7ba32`
- `validation-specs.json`: `8bc384e7935c1728f703811336580989e3b59f78317c67e6cd9914d5145b318b`

## Retry Condition

Master-reconcile the repeated attempts and predecessor state. Reopen and
version the statement around fixed, source-faithful definitions of suitable
weak Navier-Stokes solutions, regular points, and one-dimensional parabolic
Hausdorff measure. Repair the mutation and node-validation coverage, freeze a
corrected split registry, then implement locally or immutably pin exact bodies
for all four root-cut obligations with checked transports, composition, trust,
and terminal-body provenance.

Because the positive proof phase is not genuinely self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent.
