# THM-M-1235 proof-phase recheck at `471e4458`

Item: `S56-M-1235-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `471e4458269351ee096972776c478d019941b679`

Base tree: `e30e1cefce39148420ccc4525b726d57f58ee94b`

## Verdict

`blocked`. No legal positive proof body can inhabit the exact frozen target in
a consistent Lean environment. The tracked, placeholder-free declarations

```text
Stage1Instances.THMM1235.not_wolibnerGlobalExistenceAndUniqueness :
  Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness

Stage1Instances.THMM1235.independently_not_wolibnerGlobalExistenceAndUniqueness :
  Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness
```

both kernel-check at trust level zero against the current pinned environment.
The first perturbs `velocityX`; the independent witness perturbs `pressure`.

`Motion.conditionI_areaPreservingSelfHomeomorphism` through
`Motion.conditionVIII_continuousSpatialDerivatives` are freely chosen values
of type `Prop`. They are not proofs of predicates constraining the five motion
functions. Updating an alleged unique motion's `velocityX` to `velocityX + 1`
therefore preserves the `Motion` type. `SameMotion` would equate the original
and updated velocity functions, but evaluation at `(0, 0), 0` yields the
contradiction `x + 1 = x`. The concrete `counterexampleData` discharges every
explicit premise of the target.

This refutes the frozen formal encoding, not Wolibner's mathematical theorem.
Proving a corrected, weaker, or conditional proposition would be a forbidden
target substitution. In particular, `root_of_existence_and_uniqueness`
assumes both substantive packages and supplies only conditional composition;
it gives no root proof credit.

The item remains `[ ]`. No proof receipt, accepted obligation, audit
completion, theorem completion, validation completion, or release is claimed.
No `.stage1-worker-selftest.json` is written because the requested positive
proof phase is not genuinely complete. The frozen graph projects the root as
`[H3, M3, R4]`; this run leaves that accepted vector unchanged and proposes
`[H5, M5, R4]` only as a diagnosis for independent master review.

## Failed Gate And Retry

The first failed gate is `S56-5.1-EXACT-TARGET-CONSISTENCY` at
`M1235-S-DEFINITIONS`. Reopen `S56-M-1235-STATEMENT`, define conditions
`(I)`-`(VIII)` as predicates of the five functions, and make `Motion` carry
proofs of those predicates. Equality must also be scoped to the source domain
and `0 <= t <= T`, unless the source justifies equality of the globally
defined functions; otherwise off-domain or off-interval perturbations remain
possible. Then re-audit the source and publish a versioned re-freeze of the
canonical expression fingerprint, source crosswalk, obligation registry,
typed graphs, and dependent evidence before resuming proof execution.

The predecessor `S56-M-1235-OBLIGATION_TREE` remains worker-provisional, so
master proof acceptance is also dependency-blocked. Two later gates are
independently open: `validation-specs.json` uses legacy shell-command strings
rather than the structured recipe schema required by rev-5.6 section 10.5,
and the intake README/crosswalk has not been reconciled with the later source
pinpoints. None changes the earlier truth blocker.

Forty-nine earlier structured proof recheck JSON packets were present in the
current checkout while the authoritative DAG still records `attempts=0` and
no child nodes. Under blueprint section 10.2, the master/scheduler must
reconcile the attempt count and reopen or split the item instead of scheduling
another identical proof-only retry. This worker did not edit the DAG or
generated checklist.

## Validation

All completed checks reused the existing pinned Lake closure. No `lake update`,
`lake build`, dependency clone/fetch/checkout, network access, or `.lake`
mutation was performed. The automation-provided untracked
`Formalizations/Lean/.lake` symlink makes this nonrelease evidence. Temporary
Lean sources and outputs were removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | Rank 159; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1235/check_statement.py` | 0 | Canonical expression fingerprint `77aec2f5...`; all four structural mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py` | 0 | 15 obligations and 37 typed edges passed; denominator `9e0bff35...`; frozen root remains open M3. |
| Isolated tracked `lake env lean --trust=0 -t0` recipe below | 0 | Exact statement and both tracked negative modules elaborated; all four negative axiom reports were `[propext, Classical.choice, Quot.sound]`. |
| Prohibited-construct `rg --pcre2` scan over `Proof.lean` and `IndependentRefutation.lean` | 1 | Expected no-match: both proof modules contain no prohibited proof construct. |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| Manifest-pinned dependency revision/tree and input `sha256sum` checks | 0 | Environment revisions and all eight recorded input digests matched the JSON packet. |
| `git diff --check -- Stage1_Instances/THM-M-1235` | 0 | No whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

Exact successful Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1235
tmp=$(mktemp -d "$lean_root/.thm-m-1235-proof-471e4458-slot28.XXXXXX")
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
cp "$target/IndependentRefutation.lean" "$tmp/IndependentRefutation.lean"
cd "$lean_root"
lean_path=$(timeout 120 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 600 lake env lean \
  --trust=0 -t0 -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 600 lake env lean \
  --trust=0 -t0 -o "$tmp/Proof.olean" "$tmp/Proof.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 600 lake env lean \
  --trust=0 -t0 -o "$tmp/IndependentRefutation.olean" \
  "$tmp/IndependentRefutation.lean"
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `flt-regular`
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`. Input SHA-256 values:

- `Statement.lean`: `e59d7e8cb43f010533d3354022a042a38a27edc95337775da69c6cc8676a1697`
- `Proof.lean`: `f4afdf626cadef5e7acc9047ef8c517506de7d31fa49a9ed261f2fcc53cb6156`
- `IndependentRefutation.lean`: `71bf09285270d9b296eba46129722027ba2a3a968cde71633f3c0a657a95aa4c`
- `ObligationTree.lean`: `1f244092eded09ae8a474ad4cab0bd1dadac3157c7bbde6b7d73fce4d0d24fb5`
- `obligation-registry.json`: `967ef5ce046879f2da967678e3a7353c44e69a0286804b10397fd4b446a4779e`
- `typed-graphs.json`: `a60f1a527b26db45d619fb50819be8a54804268290d9b345bf2f744bfea47e11`
- `anchor-audit.json`: `e97e800b23920f911df8fb349dfa036fba13fbed790ca104c7291e6ea536f48e`
- `validation-specs.json`: `ac97fc72f4f5eb27cacb154ea03d0bf6c9c765b081316f2fba63313465f3f081`

The isolated object digests were `e866bc8b8a6be798af69aca03c09387d37677fe5cf2a1f5a5a83f9b9be9b79c1`
for `Statement.olean`, `ff41bfdef1b988e0af7c5325e197a25c45ade1ef0385584b5f46dd58d534836a`
for `Proof.olean`, and `d09c9c59e1657282cdc432b6c7d223fec3045a8502a184876a1b3c10614c5934`
for `IndependentRefutation.olean`.

## Status Boundary

This current-base artifact is negative, nonrelease blocker evidence. It does
not satisfy `S56-M-1235-PROOF`, propose `[_]` or `[x]`, or support audit or
theorem completion. The retry must begin with statement correction and
versioned re-freeze; repeating proof search against this exact encoding cannot
close the item.
