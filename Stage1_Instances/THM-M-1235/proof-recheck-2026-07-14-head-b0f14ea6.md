# THM-M-1235 proof-phase recheck at `b0f14ea6`

Item: `S56-M-1235-PROOF`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `b0f14ea655d04a569f7796528a1860935721948f`

Base tree: `5f7705bbd92801b826caed4950e24c7b942af1f3`

## Verdict

`blocked`. A legal positive proof body cannot inhabit the exact frozen target.
The tracked placeholder-free declaration

```text
Stage1Instances.THMM1235.not_wolibnerGlobalExistenceAndUniqueness :
  Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness
```

kernel-checks at trust level zero against the current pinned environment.
`Motion.conditionI_areaPreservingSelfHomeomorphism` through
`Motion.conditionVIII_continuousSpatialDerivatives` are fields whose values
have type `Prop`; they are not proofs of predicates constraining the five
motion functions. Updating an alleged unique motion's `velocityX` to
`velocityX + 1` therefore preserves the `Motion` type. `SameMotion` would make
the old and new velocity functions equal, but evaluation at `(0, 0), 0` gives
the contradiction `x + 1 = x`. The concrete `counterexampleData` discharges
every explicit premise of the frozen target.

This refutes the frozen encoding, not Wolibner's mathematical theorem. Proving
a corrected, weaker, or conditional proposition would be a forbidden target
substitution. In particular, `root_of_existence_and_uniqueness` assumes both
substantive packages and gives no root proof credit; its current uniqueness
premise is contradicted by the checked refutation.

The item remains `[ ]`. No proof receipt, accepted obligation, audit
completion, theorem completion, validation completion, or release is claimed.
No `.stage1-worker-selftest.json` is written because the requested positive
proof phase is not genuinely complete. The frozen graph projects the root as
`[H3, M3, R4]`; this evidence leaves that vector unchanged and records an M5
exact-target blocker for integration-lane reconciliation. It does not change
human-source or readability classifications.

## Failed Gate And Retry

The first failed gate is exact-target consistency at
`M1235-S-DEFINITIONS`. Reopen `S56-M-1235-STATEMENT`, express conditions
`(I)`-`(VIII)` as predicates of the five functions, and make `Motion` carry
proofs of those predicates. Then re-audit the source formulation and publish a
versioned re-freeze of the canonical expression fingerprint, source
crosswalk, obligation registry, typed graphs, and dependent evidence before
resuming proof execution.

Two later gates are independently open: `validation-specs.json` uses legacy
shell-command strings rather than the structured recipe schema in rev-5.6
section 10.5, and the intake README/crosswalk has not been reconciled with the
later source pinpoints. Neither issue changes the earlier truth blocker.

## Validation

All checks used the existing pinned Lake closure. No `lake update`, `lake
build`, dependency clone/fetch, or `.lake` mutation was performed. The
automation-provided untracked `Formalizations/Lean/.lake` link makes this
nonrelease evidence. Temporary Lean outputs were removed after replay.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | Rank 159; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py` | 0 | 15 obligations and 37 typed edges passed; denominator `9e0bff352aff0e8315b2e5d9067ad143dcc8eb1a5fbf5f4a81ca703dcfaaf9ba`; the stale frozen projection reports an open M3 root. |
| `python3 Stage1_Instances/THM-M-1235/check_statement.py` | 0 | Recomputed expression SHA-256 `77aec2f595a800d145317ae7b7574b9b18dcd2546254e98c9a7e119fbd053c23`; all four statement mutations were distinguished. |
| Isolated tracked `lake env lean --trust=0 -t0` recipe below | 0 | Exact statement and the two tracked negative theorems elaborated; axiom reports were `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe' Stage1_Instances/THM-M-1235/Proof.lean` | 1 | Expected no-match: the retained refutation module contains no prohibited construct. |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `python3 -m json.tool Stage1_Instances/THM-M-1235/proof-recheck-2026-07-14-head-b0f14ea6.json` | 0 | The current-base structured blocker is valid JSON. |
| Scoped `git diff --check` plus added-file whitespace checks | 0 | No whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

Exact Lean recipe, run from `Formalizations/Lean`:

```bash
set -euo pipefail
export LEAN_NUM_THREADS=1
tmp=$(mktemp -d ./.thm-m-1235-slot34-b0f14ea6.XXXXXX)
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
- `validation-specs.json`: `ac97fc72f4f5eb27cacb154ea03d0bf6c9c765b081316f2fba63313465f3f081`
