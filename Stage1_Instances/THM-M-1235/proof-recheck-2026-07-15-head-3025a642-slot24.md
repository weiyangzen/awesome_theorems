# THM-M-1235 proof-phase recheck at `3025a642`

Item: `S56-M-1235-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T08:45:46+08:00`

Base revision: `3025a6428cc070b33e16b1e88145ff9055f6dde2`

Base tree: `a684b3b5f61a32f7e79b8ce365a82e2d8e968714`

## Verdict

`blocked`. A legal positive proof body cannot inhabit the exact frozen target. The tracked,
placeholder-free declaration

```text
Stage1Instances.THMM1235.not_wolibnerGlobalExistenceAndUniqueness :
  Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness
```

freshly kernel-checks at trust level zero against the current pinned environment.
`Motion.conditionI_areaPreservingSelfHomeomorphism` through
`Motion.conditionVIII_continuousSpatialDerivatives` are freely chosen values of type `Prop`; they
are not proofs of predicates constraining the five motion functions. Updating an alleged unique
motion's `velocityX` to `velocityX + 1` therefore preserves the `Motion` type. `SameMotion` would
equate the original and updated velocity functions, but evaluation at `(0, 0), 0` yields the
contradiction `x + 1 = x`. The concrete `counterexampleData` discharges every explicit premise of
the target.

This refutes the frozen formal encoding, not Wolibner's mathematical theorem. Proving a corrected,
weaker, conditional, or otherwise substituted proposition would violate the assigned exact-target
gate. In particular, `root_of_existence_and_uniqueness` assumes both substantive packages and
provides only conditional composition; it gives no positive root proof credit.

The item remains `[ ]`. No proof receipt, accepted obligation, audit completion, theorem
completion, validation completion, release, or master acceptance is claimed. No
`.stage1-worker-selftest.json` is written because the requested positive proof phase is not
genuinely complete. The planned instance authority remains `[H2, M4, R4]` with no accepted proof
state. The later worker-provisional frozen graph projects `[H3, M3, R4]`; this run changes neither
record and proposes `[H5, M5, R4]` only as a diagnosis for master review.

## Failed Gate And Retry

The first failed gate is the rev-5.6 section 5.1 Lean statement/exact-encoding gate at
`M1235-S-DEFINITIONS`. Reopen `S56-M-1235-STATEMENT`, define conditions `(I)`-`(VIII)` as
predicates of the five functions, and make `Motion` carry proofs of those predicates. Equality must
also be scoped to the source domain and `0 <= t <= T`, unless the primary source justifies equality
of the globally defined functions; otherwise off-domain or off-interval perturbations remain
possible. Re-audit the source and publish a versioned re-freeze of the canonical expression
fingerprint, source crosswalk, obligation registry, typed graphs, and dependent evidence before
proof execution resumes.

The predecessor `S56-M-1235-OBLIGATION_TREE` remains worker-provisional, so master proof acceptance
is separately dependency-blocked. Twenty-two earlier structured proof-recheck JSON packets were
present at this base while the authoritative DAG still records `attempts=0` and no child nodes.
The master/scheduler must reconcile those packets with the authoritative attempt count. If at least
five qualify as unresolved execution ticks, blueprint section 10.2 requires a split before another
proof-only attempt. This worker did not edit the DAG or generated checklist.

## Validation

All checks reused the existing pinned Lake closure. No `lake update`, `lake build`, dependency
clone/fetch/checkout, network access, or `.lake` mutation was performed. The automation-provided
untracked `Formalizations/Lean/.lake` symlink makes this nonrelease evidence. Temporary Lean sources
and objects were removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | Rank 159; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1235/check_statement.py` | 0 | Canonical expression digest `77aec2f595a800d145317ae7b7574b9b18dcd2546254e98c9a7e119fbd053c23`; all four structural mutations killed; pins matched. |
| `python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py` | 0 | 15 obligations and 37 typed edges passed; denominator `9e0bff352aff0e8315b2e5d9067ad143dcc8eb1a5fbf5f4a81ca703dcfaaf9ba`; frozen root remains open M3. |
| Isolated trust-zero pinned-Lean recipe below | 0 | Exact statement and both tracked negative theorems elaborated; axiom reports were `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '^\s*(?:sorry|admit|axiom|constant|opaque|unsafe|implemented_by|extern)\b|sorryAx|native_decide' Stage1_Instances/THM-M-1235/Proof.lean` | 1 | Expected no-match: `Proof.lean` contains no prohibited proof construct. |
| Exact environment and input command block below | 0 | Lean 4.29.0, Lake 5.0.0, dependency revisions/trees, clean dependency states, and all seven frozen input hashes matched this packet. |
| `python3 -m json.tool Stage1_Instances/THM-M-1235/proof-recheck-2026-07-15-head-3025a642-slot24.json` | 0 | The structured blocker packet is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-1235` | 0 | No whitespace diagnostics in tracked changes. |
| `git diff --no-index --check /dev/null <each-new-file>` | 1 each | Expected content-difference exits with no whitespace diagnostics; this checks both untracked packet files. |
| Exact focused packet-invariant command below | 0 | Item/base/verdict/state/completion/path invariants and all frozen source hashes matched; no published strict blocker-packet schema validator was located. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

Exact successful Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-1235
lean_root=$repo/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-1235-3025a642-slot24.XXXXXX)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
base=$(cd "$lean_root" && timeout 60 lake env printenv LEAN_PATH)
lean_bin=$(cd "$lean_root" && timeout 60 lake env which lean)
LEAN_NUM_THREADS=1 LEAN_PATH="$base" timeout 300 "$lean_bin" \
  --trust=0 -t0 -R "$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base" timeout 300 "$lean_bin" \
  --trust=0 -t0 -R "$tmp" -o "$tmp/Proof.olean" "$tmp/Proof.lean"
```

Exact environment and input command block:

```bash
cd Formalizations/Lean
lake env lean --version
lake --version
git -C .lake/packages/mathlib rev-parse HEAD HEAD^{tree}
git -C .lake/packages/mathlib status --porcelain
git -C .lake/packages/flt-regular rev-parse HEAD HEAD^{tree}
git -C .lake/packages/flt-regular status --porcelain
cd ../..
sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json \
  Stage1_Instances/THM-M-1235/Statement.lean \
  Stage1_Instances/THM-M-1235/Proof.lean \
  Stage1_Instances/THM-M-1235/ObligationTree.lean \
  Stage1_Instances/THM-M-1235/obligation-registry.json \
  Stage1_Instances/THM-M-1235/typed-graphs.json \
  Stage1_Instances/THM-M-1235/anchor-audit.json \
  Stage1_Instances/THM-M-1235/validation-specs.json
```

Exact focused packet-invariant command:

```bash
jq -e '
  .item_id == "S56-M-1235-PROOF" and
  .theorem_id == "THM-M-1235" and
  .base_revision == "3025a6428cc070b33e16b1e88145ff9055f6dde2" and
  .base_tree == "a684b3b5f61a32f7e79b8ce365a82e2d8e968714" and
  .verdict == "blocked" and .state == "[ ]" and
  (.proof_phase_complete | not) and (.theorem_complete | not) and
  (.selftest_manifest_written | not) and (.changed_paths | length == 2)
' Stage1_Instances/THM-M-1235/proof-recheck-2026-07-15-head-3025a642-slot24.json
for pair in \
  'Statement.lean e59d7e8cb43f010533d3354022a042a38a27edc95337775da69c6cc8676a1697' \
  'Proof.lean f4afdf626cadef5e7acc9047ef8c517506de7d31fa49a9ed261f2fcc53cb6156' \
  'ObligationTree.lean 1f244092eded09ae8a474ad4cab0bd1dadac3157c7bbde6b7d73fce4d0d24fb5' \
  'obligation-registry.json 967ef5ce046879f2da967678e3a7353c44e69a0286804b10397fd4b446a4779e' \
  'typed-graphs.json a60f1a527b26db45d619fb50819be8a54804268290d9b345bf2f744bfea47e11' \
  'anchor-audit.json e97e800b23920f911df8fb349dfa036fba13fbed790ca104c7291e6ea536f48e' \
  'validation-specs.json ac97fc72f4f5eb27cacb154ea03d0bf6c9c765b081316f2fba63313465f3f081'
do
  set -- $pair
  test "$(sha256sum "Stage1_Instances/THM-M-1235/$1" | cut -d' ' -f1)" = "$2"
done
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `flt-regular`
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`. Frozen input SHA-256 values:

- `Statement.lean`: `e59d7e8cb43f010533d3354022a042a38a27edc95337775da69c6cc8676a1697`
- `Proof.lean`: `f4afdf626cadef5e7acc9047ef8c517506de7d31fa49a9ed261f2fcc53cb6156`
- `ObligationTree.lean`: `1f244092eded09ae8a474ad4cab0bd1dadac3157c7bbde6b7d73fce4d0d24fb5`
- `obligation-registry.json`: `967ef5ce046879f2da967678e3a7353c44e69a0286804b10397fd4b446a4779e`
- `typed-graphs.json`: `a60f1a527b26db45d619fb50819be8a54804268290d9b345bf2f744bfea47e11`
- `anchor-audit.json`: `e97e800b23920f911df8fb349dfa036fba13fbed790ca104c7291e6ea536f48e`
- `validation-specs.json`: `ac97fc72f4f5eb27cacb154ea03d0bf6c9c765b081316f2fba63313465f3f081`

Temporary output SHA-256 values were
`cbb0b49360973c6a3e9e45d45965f51efbadf0914f10448c5e68e2dd3654497d`
for `Statement.olean` and
`3af4a429ebac82bfe937a5acd5039cfe0984cead67492d0f9b46d41f3e761169`
for `Proof.olean`.

## Status Boundary

This current-base artifact is negative, nonrelease blocker evidence. It does not satisfy
`S56-M-1235-PROOF`, propose `[_]` or `[x]`, or support audit or theorem completion. The retry must
begin with statement correction and versioned re-freeze; repeating proof search against this exact
encoding cannot close the item.
