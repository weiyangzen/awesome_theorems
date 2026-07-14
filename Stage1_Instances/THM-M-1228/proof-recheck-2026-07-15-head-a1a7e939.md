# THM-M-1228 proof-phase recheck at `a1a7e939`

Item: `S56-M-1228-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `a1a7e939e58f103f5ff5d23af51437fa8658aa04`

Base tree: `d881fd9641fa3e5f3ebe5082b35672981e90adcf`

## Verdict

`blocked`. The frozen declaration is a family

```text
CaffarelliKohnNirenbergTarget S =
  forall D, S.IsSuitableWeakSolution D ->
    S.ParabolicHausdorffOneMeasureZero (SingularSet S D).
```

It does not select a concrete, source-faithful `S`, and the three predicates in
`CKNSourceSemantics` have no laws relating suitability, regularity, and
parabolic measure. The tracked, placeholder-free `ProofBlocker.lean` chooses a
permitted interpretation with suitability true and the measure-zero predicate
false. At trust level zero Lean checks

```text
counterexampleTargetIsFalse :
  Not (CaffarelliKohnNirenbergTarget counterexampleSemantics)

noUniformTargetProof :
  Not (forall S : CKNSourceSemantics, CaffarelliKohnNirenbergTarget S)
```

Therefore no proof body uniform over the frozen semantic interface can exist.
This countermodel does not refute the mathematical Caffarelli-Kohn-Nirenberg
theorem, nor does it say that every specialization is false. It shows that the
current interface is under-specified. Proving a convenient specialization,
assuming the per-solution conclusion, or replacing parabolic measure by
Euclidean Hausdorff measure would substitute a different theorem and was not
done.

The predecessor registry remains open at `M4`; this proof worker does not
rewrite its statement, obligation registry, typed graphs, DAG, or generated
checklist. The checked countermodel is blocker evidence for the interface, not
positive proof credit. The open root cut remains:

- `M1228-S-CONCRETE`
- `M1228-E-EPSILON`
- `M1228-C-COVER`
- `M1228-L-MEASURE`

No positive canonical-root proof body, receipt, accepted obligation, state
transition, audit completion, validation completion, release result, or
theorem-completion claim is made. The assigned item remains `[ ]`.

## Validation

All commands ran in this worker clone. `Formalizations/Lean/.lake` was already
an untracked automation symlink to the canonical pinned artifacts. Its target
string has SHA-256
`e8714e9ebb75a5da1eeb16fdb6f50831a6cab29f115df43fa8e7535b38f59826`.
This dirty input is classified as nonrelease evidence. No `lake update`, `lake
build`, dependency clone/fetch, network action, or `.lake` mutation was run.
The direct elaboration wrote its temporary `.olean` under `/tmp` and removed
it on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1228` | 0 | Rank 156; lifecycle `planned`; lane `hard_mathlib_anchor_and_wrapper`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1228/check_statement.py` | 0 | Toolchain `leanprover/lean4:v4.29.0`, mathlib pin `8a178386...eea95`, expression SHA-256 `101ce8f2...f58e5f`, and all four registered mutations killed. |
| `python3 Stage1_Instances/THM-M-1228/check_anchor_audit.py` | 0 | `ok: M4 boundary, nine Lean probes, mathlib pin, and four immutable external tree receipts` |
| `python3 Stage1_Instances/THM-M-1228/check_obligation_tree.py` | 0 | `PASS`: 15 obligations and 31 typed edges; denominator `25704bee664136645e0481ae7d6273ac3fdfd2f1cd20fc5f82ba43f07066f41e`; root open at M4 with a four-obligation cut. |
| Narrow `lake env lean --trust=0 -t0` recipe below | 0 | The exact statement and both negative declarations elaborated. Each axiom report was `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-1228 --glob '*.lean'` | 1 | Expected no-match exit: no prohibited proof-gap or unsafe declaration in the owned Lean files. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse 'HEAD^{tree}'` | 0 | `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git diff --check -- Stage1_Instances/THM-M-1228 .stage1-worker-selftest.json` | 0 | No whitespace errors in tracked target changes; there were none. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1228/proof-recheck-2026-07-15-head-a1a7e939.md` | 1 | Expected content-difference exit; stderr was empty (0 bytes), so the untracked Markdown packet has no whitespace diagnostics. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1228/proof-recheck-2026-07-15-head-a1a7e939.json` | 1 | Expected content-difference exit; stderr was empty (0 bytes), so the untracked JSON packet has no whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The success-only worker self-test manifest is absent. |

The exact narrow Lean recipe, run from the repository root, was:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-1228-proof-a1a7e939.XXXXXX)
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
- `obligation-registry.json`: `90e618e7ead41d98804da85b81e7d8e0d366a322b62da0680b9d82043c66892b`
- `typed-graphs.json`: `41e601f13842fd84bc9b7ffcfdeab5cbfa415806836ebe0908e7493dc5ad4330`
- `lake-manifest.json`: `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`
- `lean-toolchain`: `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`

## Retry Condition

Reopen and version the statement around fixed, source-faithful definitions of
suitable weak Navier-Stokes solutions, regular points, and one-dimensional
parabolic Hausdorff measure. Freeze a corrected registry, then implement
placeholder-free local bodies or immutably pin exact compatible bodies for all
four root-cut obligations, with checked transports, child composition, and
terminal-body provenance.

Because the assigned positive proof phase is not genuinely self-tested
complete, `.stage1-worker-selftest.json` is deliberately absent.
