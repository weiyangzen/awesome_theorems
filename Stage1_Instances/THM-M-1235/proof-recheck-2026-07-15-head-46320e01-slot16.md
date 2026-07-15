# THM-M-1235 proof recheck on `46320e01` (`slot16`)

Item: `S56-M-1235-PROOF`

Date: `2026-07-15T13:51:44+08:00`

Base revision: `46320e01d1897482417e7b0d03a15a5b77ae5275`

## Verdict

`blocked`: no legal positive proof body exists for the exact frozen target in a
consistent Lean environment. The blocker is in the statement encoding, not in
the amount of proof search performed.

`Motion` stores each source condition `(I)`--`(VIII)` as a bare `Prop` field,
not as a predicate of the five functions and not as a proof of such a
predicate. Therefore those fields constrain neither the functions nor which
records count as motions. For any alleged unique motion, the placeholder-free
tracked declaration `perturbVelocityX` replaces `velocityX` pointwise by
`velocityX + 1` while preserving every other field. `SameMotion` would then
equate the two velocity functions, and evaluation at `(0, 0), 0` yields the
contradiction `x + 1 = x`.

The exact negative theorem
`Stage1Instances.THMM1235.not_wolibnerGlobalExistenceAndUniqueness` was replayed
at trust level zero and has type
`Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness`. Its axiom
report is exactly `[propext, Classical.choice, Quot.sound]`. This refutes only
the frozen formal encoding, not Wolibner's mathematical theorem. It cannot
receive positive root-closure credit or satisfy the assigned proof phase.

## Dependency and repair boundary

The predecessor `S56-M-1235-OBLIGATION_TREE` is still worker-provisional rather
than master-accepted. Its frozen registry has 15 obligations and 37 typed
edges, records only the conditional assembly theorem as closed, and keeps the
root open at M3. The first invalidated obligation is
`M1235-S-DEFINITIONS`.

Repair must reopen the statement phase: define conditions `(I)`--`(VIII)` as
proof-bearing predicates of the five functions, scope uniqueness to the source
domain and time interval unless the source justifies global function equality,
re-audit the source, and version/re-freeze the canonical expression, registry,
typed graphs, and dependent evidence. Only then can positive proof execution
resume.

Twenty-nine earlier structured proof-recheck JSON packets were already present
on this base while the authoritative DAG still records `attempts=0` and no
children. The master/scheduler should reconcile the attempts and reopen or
split the item under blueprint section 10.2 rather than issue another identical
proof-only retry. This worker did not edit the DAG or generated blueprint.

## Validation

No `lake update`, `lake build`, dependency clone/fetch/checkout, network access,
or `.lake` mutation was performed. The automation-provided untracked
`Formalizations/Lean/.lake` symlink points to the shared canonical pinned
cache, making this nonrelease evidence. The manifest-pinned `flt-regular`
checkout has `HEAD` set to `refs/heads/.invalid`; consequently the required
`lake env` path fails before target elaboration. The target imports only
mathlib, so a narrow supplementary replay used the exact pinned Lean executable
and already compiled package paths while excluding the incomplete unrelated
package. That fallback does not cure the missing Lake artifact or qualify as
release evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | Rank 159; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py` | 0 | 15 obligations and 37 typed edges passed; denominator `9e0bff352aff0e8315b2e5d9067ad143dcc8eb1a5fbf5f4a81ca703dcfaaf9ba`; root remains open M3. |
| `cd Formalizations/Lean && timeout 300 lake env lean --version` | 1 | Lake reported that `flt-regular` could not resolve `HEAD` to a commit. No repair was attempted. |
| `python3 Stage1_Instances/THM-M-1235/check_statement.py` | 1 | The same missing `flt-regular` HEAD blocked Lake environment materialization before elaboration. |
| Isolated direct trust-zero Lean replay below | 0 | Exact statement and both negative declarations elaborated; both axiom reports were `[propext, Classical.choice, Quot.sound]`; object hashes were `cbb0b493...` and `3af4a429...`. |
| `rg -n --pcre2 '^\\s*(?:sorry\|admit\|axiom\|constant\|opaque\|unsafe\|implemented_by\|extern)\\b\|sorryAx\|native_decide' Stage1_Instances/THM-M-1235/Proof.lean` | 1 | Expected no-match exit: `Proof.lean` has no prohibited proof construct. |
| Pinned dependency identity and frozen-input SHA-256 checks | 0 | Mathlib revision/tree, available `flt-regular` manifest object/tree, environment hashes, and all seven frozen input hashes matched the structured record. |

Exact successful supplementary recipe, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1235
tmp=$(mktemp -d /tmp/thm-m-1235-proof-46320e01-slot16.XXXXXX)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
lean_bin=$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
lean_path=$(find -L "$lean_root/.lake/packages" \
  -path '*/.lake/build/lib/lean' -type d \
  ! -path '*/flt-regular/*' -print | sort | paste -sd: -)
lean_path="$lean_root/.lake/build/lib/lean:$lean_path:$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 600 "$lean_bin" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 600 "$lean_bin" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/Proof.olean" "$tmp/Proof.lean"
sha256sum "$tmp/Statement.olean" "$tmp/Proof.olean"
```

Pinned identities and input SHA-256 values:

- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- mathlib: revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`
- `flt-regular` manifest object/tree: `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` / `32c9eace926573a9981787ae97643e520353c893`
- `lean-toolchain`: `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`
- `lake-manifest.json`: `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`
- `Statement.lean`: `e59d7e8cb43f010533d3354022a042a38a27edc95337775da69c6cc8676a1697`
- `Proof.lean`: `f4afdf626cadef5e7acc9047ef8c517506de7d31fa49a9ed261f2fcc53cb6156`
- `ObligationTree.lean`: `1f244092eded09ae8a474ad4cab0bd1dadac3157c7bbde6b7d73fce4d0d24fb5`
- `obligation-registry.json`: `967ef5ce046879f2da967678e3a7353c44e69a0286804b10397fd4b446a4779e`
- `typed-graphs.json`: `a60f1a527b26db45d619fb50819be8a54804268290d9b345bf2f744bfea47e11`
- `anchor-audit.json`: `e97e800b23920f911df8fb349dfa036fba13fbed790ca104c7291e6ea536f48e`
- `validation-specs.json`: `ac97fc72f4f5eb27cacb154ea03d0bf6c9c765b081316f2fba63313465f3f081`

The isolated object digests were
`cbb0b49360973c6a3e9e45d45965f51efbadf0914f10448c5e68e2dd3654497d`
for `Statement.olean` and
`3af4a429ebac82bfe937a5acd5039cfe0984cead67492d0f9b46d41f3e761169`
for `Proof.olean`.

## Status boundary

This current-base artifact is negative, nonrelease blocker evidence. It does
not satisfy `S56-M-1235-PROOF`, propose `[_]` or `[x]`, or support audit or
theorem completion. Because the assigned positive proof phase is not genuinely
self-tested complete, `.stage1-worker-selftest.json` is deliberately absent.
