# THM-M-1235 proof-phase recheck at `4990a9d6`

Item: `S56-M-1235-PROOF`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `4990a9d6fa09beb7747e6822c6543c6123ca7504`

Base tree: `b74497bc09c004757aa3974f3bb0622d77e20106`

Target tree: `ba90cd46159ea1f818fa1d88b7f8e25c597b5c2f`

## Verdict

`blocked`. No legal positive proof body can inhabit the exact frozen target.
In `Statement.lean`, `Motion.conditionI_areaPreservingSelfHomeomorphism`
through `Motion.conditionVIII_continuousSpatialDerivatives` are freely chosen
values of type `Prop`; they are not proofs of predicates constraining the
motion's five functions. The tracked placeholder-free `Proof.lean` therefore
constructs a counterexample. `perturbVelocityX` replaces any alleged unique
motion's `velocityX` by `velocityX + 1` while preserving its `Motion` type.
`SameMotion` would equate the old and new functions, but evaluation at
`(0, 0), 0` yields the contradiction `x + 1 = x`. The concrete
`counterexampleData` discharges every explicit premise at `T = 1`.

The tracked declaration has exact type:

```text
Stage1Instances.THMM1235.not_wolibnerGlobalExistenceAndUniqueness :
  Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness
```

This refutes the frozen formal encoding, not Wolibner's mathematical theorem.
A proof of a corrected, conditional, or weaker proposition would be a forbidden
target substitution. The conditional theorem `root_of_existence_and_uniqueness`
assumes both substantive packages and gives no root proof credit; its uniqueness
package is impossible for this interface.

The item remains `[ ]`. No proof receipt, accepted obligation, provisional
state, audit completion, theorem completion, validation completion, release,
or master acceptance is claimed. No `.stage1-worker-selftest.json` is written
because the assigned positive proof phase is not genuinely complete.

## Failed Gate And Retry

The first failed gate is exact-target consistency at
`M1235-S-DEFINITIONS`. Reopen `S56-M-1235-STATEMENT`, define conditions
`(I)`-`(VIII)` as predicates of the five functions, and make `Motion` carry
proofs of those predicates. Restrict the five functions to the source domain
and `0 <= t <= T`, or restrict `SameMotion` to pointwise equality there;
otherwise off-domain or off-interval perturbations still defeat global
function equality. Re-audit the primary source, then issue a versioned
re-freeze of the canonical expression, source crosswalk, obligation registry,
typed graphs, and dependent evidence before proof work resumes.

Two later gates are independently open. `validation-specs.json` uses legacy
shell-command strings rather than the structured recipe schema required by
rev-5.6 section 10.5, and the intake README/crosswalk has not been reconciled
with the later source pinpoints. Neither issue changes the earlier truth
blocker.

## Validation

All checks used the existing pinned Lake closure. No `lake update`, `lake
build`, dependency clone/fetch/checkout, or `.lake` mutation was performed.
The automation-provided untracked `Formalizations/Lean/.lake` symlink makes
this nonrelease evidence. Temporary Lean outputs were removed after replay.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | Rank 159; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py` | 0 | 15 obligations and 37 typed edges passed; denominator `9e0bff352aff0e8315b2e5d9067ad143dcc8eb1a5fbf5f4a81ca703dcfaaf9ba`; frozen projection reports an open M3 root. |
| `timeout 300 python3 Stage1_Instances/THM-M-1235/check_statement.py` | 0 | Recomputed expression SHA-256 `77aec2f595a800d145317ae7b7574b9b18dcd2546254e98c9a7e119fbd053c23`; all four statement mutations were distinguished. |
| Isolated tracked `lake env lean --trust=0 -t0` recipe below | 0 | Exact statement and both tracked negative theorems elaborated; axiom reports were `[propext, Classical.choice, Quot.sound]`. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD` | 0 | Manifest-pinned `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`. |
| Line-level prohibited-token scan over owned Lean files | 1 | Expected no-match: no prohibited declaration or placeholder token. |
| `python3 -m json.tool Stage1_Instances/THM-M-1235/proof-recheck-2026-07-14-head-4990a9d6.json` | 0 | Current-base structured blocker is valid JSON. |
| Scoped `git diff --check` plus added-file whitespace checks | 0 | No whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

Exact Lean recipe, run from `Formalizations/Lean`:

```bash
set -euo pipefail
export LEAN_NUM_THREADS=1
tmp=$(mktemp -d ./.thm-m-1235-slot39-4990a9d6.XXXXXX)
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

Input SHA-256 values:

- `Statement.lean`: `e59d7e8cb43f010533d3354022a042a38a27edc95337775da69c6cc8676a1697`
- `Proof.lean`: `f4afdf626cadef5e7acc9047ef8c517506de7d31fa49a9ed261f2fcc53cb6156`
- `obligation-registry.json`: `967ef5ce046879f2da967678e3a7353c44e69a0286804b10397fd4b446a4779e`
- `typed-graphs.json`: `a60f1a527b26db45d619fb50819be8a54804268290d9b345bf2f744bfea47e11`
- `anchor-audit.json`: `e97e800b23920f911df8fb349dfa036fba13fbed790ca104c7291e6ea536f48e`
- `validation-specs.json`: `ac97fc72f4f5eb27cacb154ea03d0bf6c9c765b081316f2fba63313465f3f081`

## Status Boundary

This current-base artifact is negative, nonrelease blocker evidence. It does
not satisfy `S56-M-1235-PROOF`, propose `[_]` or `[x]`, or support audit or
theorem completion. The retry must begin at statement correction and
versioned re-freeze.
