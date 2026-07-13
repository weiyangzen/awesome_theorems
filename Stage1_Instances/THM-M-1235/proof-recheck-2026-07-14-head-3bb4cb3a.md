# THM-M-1235 proof-phase recheck at `3bb4cb3a`

Item: `S56-M-1235-PROOF`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `3bb4cb3ae15dff8b48c93242019edec3bf858e48`

Base tree: `8e911f5a101bd92eb0951794fa0d9a3c0c3a2ddc`

## Verdict

`blocked`. A legal positive proof body cannot inhabit the exact frozen target.
The tracked placeholder-free declaration

```text
Stage1Instances.THMM1235.not_wolibnerGlobalExistenceAndUniqueness :
  Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness
```

kernel-checks at trust level zero against the current pinned environment. In
the frozen encoding, every condition from
`Motion.conditionI_areaPreservingSelfHomeomorphism` through
`Motion.conditionVIII_continuousSpatialDerivatives` is freely chosen data of
type `Prop`. None is a proof of a predicate constraining the motion's five
functions. Updating an alleged unique motion's `velocityX` to `velocityX + 1`
therefore produces another value of the same `Motion` type, while equality of
the two velocity functions at `(0, 0), 0` yields a contradiction. The concrete
`counterexampleData` satisfies all explicit premises of the frozen target.

This refutes the formal encoding, not Wolibner's mathematical theorem. A proof
of a corrected, conditional, or weaker proposition would be a forbidden target
substitution. The conditional theorem `root_of_existence_and_uniqueness` also
cannot supply proof credit: it assumes both terminal packages, and its current
uniqueness interface is inconsistent with the checked counterexample.

The assigned item remains `[ ]`. No proof receipt, accepted obligation, audit
completion, theorem completion, validation completion, or release claim is
made. No `.stage1-worker-selftest.json` is written because the requested
positive proof phase is not genuinely complete.

## Failed Gate And Retry

The first failed gate is exact-target consistency. Reopen
`S56-M-1235-STATEMENT`, define conditions `(I)`--`(VIII)` as predicates of the
five functions, and make `Motion` carry proofs of those predicates. Then
re-audit the source formulation and publish a versioned re-freeze of the
canonical expression fingerprint, source crosswalk, obligation registry,
typed graphs, and dependent evidence before resuming proof execution.

## Validation

All checks used the existing pinned Lake closure. No `lake update`, `lake
build`, dependency clone/fetch, or `.lake` mutation was performed. The
automation-provided untracked `Formalizations/Lean/.lake` link makes this
nonrelease evidence. The isolated Lean recipe removed its temporary directory
on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | Rank 159; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py` | 0 | 15 obligations and 37 typed edges passed; denominator `9e0bff352aff0e8315b2e5d9067ad143dcc8eb1a5fbf5f4a81ca703dcfaaf9ba`; frozen root remains open M3 and the existence/uniqueness packages remain M4. |
| Isolated `lake env lean --trust=0 -t0` recipe below | 0 | The exact statement and both refutation declarations elaborated; each axiom report was `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\\b(?:sorry|admit|axiom)\\b|sorryAx|unsafe' Stage1_Instances/THM-M-1235/Proof.lean` | 1 | Expected no-match result: the proof/refutation module contains no prohibited construct. |
| `python3 -m json.tool Stage1_Instances/THM-M-1235/proof-blocker.json` | 0 | The structured blocker is valid JSON. |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git diff --check -- Stage1_Instances/THM-M-1235` | 0 | No whitespace errors. |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-1235/proof-recheck-2026-07-14-head-3bb4cb3a.md` | 1 | Expected new-file difference exit; the command emitted no whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

Exact Lean recipe, run from `Formalizations/Lean`:

```bash
set -u
tmp=$(mktemp -d ./.thm-m-1235-slot38-recheck.XXXXXX)
cleanup() { rm -rf "$tmp"; }
trap cleanup EXIT
cp ../../Stage1_Instances/THM-M-1235/Statement.lean "$tmp/Statement.lean"
cp ../../Stage1_Instances/THM-M-1235/Proof.lean "$tmp/Proof.lean"
LEAN_PATH_BASE=$(lake env printenv LEAN_PATH)
timeout 300 lake env lean --trust=0 -t0 \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$LEAN_PATH_BASE" \
  timeout 300 lake env lean --trust=0 -t0 "$tmp/Proof.lean"
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Input SHA-256 values:

- `Statement.lean`: `e59d7e8cb43f010533d3354022a042a38a27edc95337775da69c6cc8676a1697`
- `Proof.lean`: `f4afdf626cadef5e7acc9047ef8c517506de7d31fa49a9ed261f2fcc53cb6156`
- `obligation-registry.json`: `967ef5ce046879f2da967678e3a7353c44e69a0286804b10397fd4b446a4779e`
- `typed-graphs.json`: `a60f1a527b26db45d619fb50819be8a54804268290d9b345bf2f744bfea47e11`
- `anchor-audit.json`: `e97e800b23920f911df8fb349dfa036fba13fbed790ca104c7291e6ea536f48e`
