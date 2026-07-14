# THM-M-1228 proof-phase recheck at `3d3099d0`

Item: `S56-M-1228-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `3d3099d0d4002093cf89da97132bdf954605810b`

Base tree: `17ea0daeddceb9742a5df33c247d624d2842c520`

## Verdict

`blocked`. No legal positive proof body can inhabit the exact frozen target
uniformly over its semantic interface. Its proposition is

```text
CaffarelliKohnNirenbergTarget S =
  forall D, S.IsSuitableWeakSolution D ->
    S.ParabolicHausdorffOneMeasureZero (SingularSet S D).
```

The three predicates in `CKNSourceSemantics` are unconstrained. The tracked,
placeholder-free `ProofBlocker.lean` instantiates suitability as true and the
measure-zero predicate as false. Lean checks both

```text
counterexampleTargetIsFalse :
  Not (CaffarelliKohnNirenbergTarget counterexampleSemantics)

noUniformTargetProof :
  Not (forall S : CKNSourceSemantics, CaffarelliKohnNirenbergTarget S)
```

at trust level zero. A uniform positive proof would contradict that
countermodel. This refutes only the current semantic-interface encoding, not
the mathematical Caffarelli-Kohn-Nirenberg theorem. Choosing a favorable
semantics, assuming the per-solution conclusion, storing it as a structure
field, importing the unrelated weighted CKN inequality, or replacing
parabolic by Euclidean Hausdorff measure would substitute a different theorem
and was not done. The conditional `ObligationTree.root_compose` consumes the
entire open per-solution analytic conclusion and supplies no root proof credit.

The predecessor registry remains open at `M4`; this proof worker does not
rewrite its statement, registry, graphs, task DAG, or generated checklist. The
checked countermodel is blocker evidence for the interface, not positive proof
credit. The frozen root cut remains:

- `M1228-S-CONCRETE`
- `M1228-E-EPSILON`
- `M1228-C-COVER`
- `M1228-L-MEASURE`

No positive proof body, receipt, accepted obligation, audit completion,
validation completion, release result, or theorem-completion claim is made.
The assigned item remains `[ ]`.

## Validation

All commands ran from this worker clone using the automation-provided symlink
to the canonical pinned `.lake` artifacts. No `lake update`, `lake build`,
dependency clone/fetch, network action, or `.lake` mutation was performed. The
untracked link makes this nonrelease evidence. The narrow Lean recipe wrote
temporary elaboration output below `/tmp` and removed it on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1228` | 0 | Rank 156; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `timeout 300 python3 Stage1_Instances/THM-M-1228/check_statement.py` | 0 | Toolchain and mathlib pin agree; expression SHA-256 is `101ce8f2...f58e5f`; all four registered statement mutations were killed. |
| `python3 Stage1_Instances/THM-M-1228/check_anchor_audit.py` | 0 | `ok: M4 boundary, nine Lean probes, mathlib pin, and four immutable external tree receipts` |
| `python3 Stage1_Instances/THM-M-1228/check_obligation_tree.py` | 0 | `PASS`: 15 obligations and 31 typed edges; denominator `25704bee664136645e0481ae7d6273ac3fdfd2f1cd20fc5f82ba43f07066f41e`; root open at M4 with a four-obligation analytic cut. |
| Narrow `lake env lean --trust=0 -t0` recipe below | 0 | The exact statement and both negative declarations elaborated. Each negative declaration reported `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\\b(?:sorry|admit|axiom)\\b|sorryAx|^[[:space:]]*unsafe\\b' Stage1_Instances/THM-M-1228 --glob '*.lean'` | 1 | Expected no-match: no prohibited proof-gap or unsafe declaration occurs in the owned Lean files. |
| `cd Formalizations/Lean && LAKE_NO_UPDATE=1 timeout 30 lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse 'HEAD^{tree}'` | 0 | `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `python3 -m json.tool Stage1_Instances/THM-M-1228/proof-recheck-2026-07-15-head-3d3099d0.json >/dev/null` | 0 | The current-base structured blocker is valid JSON. |
| Scoped blocker invariant check | 0 | Item and target identity, base revision/tree, blocked verdict, `[ ]` state, unchanged H1/M4/R4 vector, false completion fields, empty accepted receipts, root cut, and declared paths agree. |
| `git diff --check -- Stage1_Instances/THM-M-1228 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics in the owned target changes. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1228/proof-recheck-2026-07-15-head-3d3099d0.md` | 1 | Expected content-difference exit with empty stderr, so the untracked Markdown packet has no whitespace diagnostics. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1228/proof-recheck-2026-07-15-head-3d3099d0.json` | 1 | Expected content-difference exit with empty stderr, so the untracked JSON packet has no whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The exact narrow Lean recipe, run from the repository root, was:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-1228-proof-3d3099d0.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean_path=$(cd Formalizations/Lean && LAKE_NO_UPDATE=1 timeout 60 lake env printenv LEAN_PATH)
lean_bin=$(cd Formalizations/Lean && LAKE_NO_UPDATE=1 timeout 60 lake env which lean)
LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 timeout 300 "$lean_bin" \
  --trust=0 -t0 -o "$tmp/Statement.olean" \
  Stage1_Instances/THM-M-1228/Statement.lean
LEAN_PATH="$tmp:$lean_path" LEAN_NUM_THREADS=1 timeout 300 "$lean_bin" \
  --trust=0 -t0 Stage1_Instances/THM-M-1228/ProofBlocker.lean
```

The statement stdout SHA-256 was
`e2149c8788a7c04dcd2fb74033416a6d52283db3762d11de097377e70842961b`;
the countermodel stdout SHA-256 was
`392f43d6df0dabab37d8684708f8f6a9e68d42302a0b7363c39cfdb81c0002fe`.
Both stderr streams were empty (SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).
The temporary `Statement.olean` SHA-256 was
`9c3fe8b4c407d6881d5e69167f2948e8fd2364467a642116ed4eb11d4abced8c`.

Input SHA-256 values:

- `Statement.lean`: `e5360836f4875e028eabdbf3e76c860aa1566a0f2f4eeb1487588c6ee55ddcc5`
- `ProofBlocker.lean`: `b7c0043752d40a41350080fe5210b65aca2594a2c8cdbae139c3ab058ffacca5`
- `obligation-registry.json`: `90e618e7ead41d98804da85b81e7d8e0d366a322b62da0680b9d82043c66892b`
- `typed-graphs.json`: `41e601f13842fd84bc9b7ffcfdeab5cbfa415806836ebe0908e7493dc5ad4330`
- `anchor-audit.json`: `8d18f2332859b387552de7370c72674407d61f7260eb4dd476856694f7a7ba32`
- `validation-specs.json`: `8bc384e7935c1728f703811336580989e3b59f78317c67e6cd9914d5145b318b`

## Retry Condition

Reopen and version the statement around fixed, source-faithful definitions of
suitable weak Navier-Stokes solutions, regular points, and one-dimensional
parabolic Hausdorff measure. Freeze a corrected registry, then implement
placeholder-free local bodies or immutably pin exact compatible bodies for all
four root-cut obligations, including checked transports, child composition,
and terminal-body provenance.

Because the positive proof phase is not genuinely self-tested complete,
`.stage1-worker-selftest.json` is deliberately absent.
