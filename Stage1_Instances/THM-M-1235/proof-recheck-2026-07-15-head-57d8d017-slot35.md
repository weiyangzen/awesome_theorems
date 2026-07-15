# THM-M-1235 proof-phase recheck at `57d8d017`

Item: `S56-M-1235-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `57d8d01796f84ffc9de9adf1f5d0723555e7babb`

Base tree: `cdea5b3fad713816ee6c9ed6aae7a10f9009a18e`

## Verdict

`blocked`. A legal positive proof body cannot inhabit the exact frozen target.
The tracked, placeholder-free declaration

```text
Stage1Instances.THMM1235.not_wolibnerGlobalExistenceAndUniqueness :
  Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness
```

freshly elaborates at trust level zero against the pinned Lean executable and
existing compiled mathlib artifacts. The fields
`Motion.conditionI_areaPreservingSelfHomeomorphism` through
`Motion.conditionVIII_continuousSpatialDerivatives` are freely chosen values
of type `Prop`; they are not proofs of predicates constraining the five motion
functions. Replacing an alleged unique motion's `velocityX` by `velocityX + 1`
therefore preserves the `Motion` type. `SameMotion` would equate the old and new
velocity functions, but evaluation at `(0, 0), 0` gives a contradiction. The
concrete `counterexampleData` discharges every explicit target premise.

This refutes the frozen formal encoding, not Wolibner's mathematical theorem.
Proving a corrected, weaker, or conditional proposition would be a forbidden
target substitution. In particular, `root_of_existence_and_uniqueness` assumes
both substantive packages and supplies only conditional composition; it gives
no root proof credit.

The item remains `[ ]`. No proof receipt, accepted obligation, audit
completion, theorem completion, validation completion, release, or master
acceptance is claimed. No `.stage1-worker-selftest.json` is written because the
requested positive proof phase is not genuinely self-tested or complete. The
frozen graph projects the root as `[H3, M3, R4]`; this run makes no accepted
vector change and proposes `[H5, M5, R4]` only for independent master review.

## Failed Gate And Retry

The first failed gate is `S56-5.1-EXACT-TARGET-CONSISTENCY` at
`M1235-S-DEFINITIONS`. Reopen `S56-M-1235-STATEMENT`, define conditions
`(I)`-`(VIII)` as predicates of the five functions, and make `Motion` carry
proofs of those predicates. Equality must also be scoped to the source domain
and `0 <= t <= T`, unless the source justifies global function equality;
otherwise off-domain or off-interval perturbations remain possible. Re-audit
the source, then publish a versioned re-freeze of the canonical expression
fingerprint, source crosswalk, obligation registry, typed graphs, and dependent
evidence before proof execution resumes.

The predecessor `S56-M-1235-OBLIGATION_TREE` remains worker-provisional (`[_]`),
so proof acceptance is independently dependency-blocked. Two later gates also
remain open: `validation-specs.json` uses legacy command strings rather than the
structured recipe schema required by rev-5.6 section 10.5, and the intake
README/crosswalk has not been reconciled with later source pinpoints. Neither
changes the earlier truth blocker.

Twenty-six earlier structured proof-recheck packets were already present at
this base, while the authoritative DAG still records `attempts=0` and no
children for this proof item. Under blueprint section 10.2, the master/scheduler
must reconcile the attempt count and reopen or split the item instead of
scheduling another identical proof-only retry. This worker did not edit the DAG
or generated checklist.

## Validation

No `lake update`, `lake build`, dependency clone/fetch/checkout, network access,
or `.lake` mutation was performed. The automation-provided untracked
`Formalizations/Lean/.lake` symlink points to a shared canonical dependency
cache and makes this nonrelease evidence. The manifest-pinned `flt-regular`
checkout currently has `HEAD` set to `refs/heads/.invalid`, so the required
`lake env` route and `check_statement.py` fail before target elaboration. The
target imports only mathlib, so the narrowest available supplementary replay
used the exact pinned Lean executable and existing compiled package artifacts,
excluding the incomplete unrelated package. This fallback does not cure the
missing Lake artifact or qualify as release evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | Rank 159; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py` | 0 | 15 obligations and 37 typed edges passed; denominator `9e0bff352aff0e8315b2e5d9067ad143dcc8eb1a5fbf5f4a81ca703dcfaaf9ba`; root open M3, existence and uniqueness M4. |
| `cd Formalizations/Lean && timeout 30 lake env lean --version` | 1 | Lake reported that `flt-regular` could not resolve `HEAD`; no repair was attempted. |
| `python3 Stage1_Instances/THM-M-1235/check_statement.py` | 1 | The same missing `flt-regular` `HEAD` blocked the script before Lean elaboration; no passing result is claimed. |
| Isolated direct trust-zero Lean replay below | 0 | The exact statement and both tracked negative theorems elaborated; axiom reports were `[propext, Classical.choice, Quot.sound]`; object hashes were `cbb0b493...` and `3af4a429...`. |
| `rg -n --pcre2 '^\s*(?:sorry\|admit\|axiom\|constant\|opaque\|unsafe\|implemented_by\|extern)\b\|sorryAx\|native_decide' Stage1_Instances/THM-M-1235/Proof.lean` | 1 | Expected no-match exit: `Proof.lean` contains no prohibited proof construct. |
| Frozen-input and environment `sha256sum` checks | 0 | Seven proof inputs, `lean-toolchain`, and `lake-manifest.json` matched the hashes below. |

Exact successful supplementary Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1235
tmp=$(mktemp -d /tmp/thm-m-1235-proof-57d8d017-slot35.XXXXXX)
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

Pinned environment and input SHA-256 values:

- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- mathlib: revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`
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

## Status Boundary

This current-base artifact is negative, nonrelease blocker evidence. It does
not satisfy `S56-M-1235-PROOF`, propose `[_]` or `[x]`, or support audit or
theorem completion. The retry must begin with statement correction and a
versioned re-freeze; repeating proof search against this encoding cannot close
the item.
