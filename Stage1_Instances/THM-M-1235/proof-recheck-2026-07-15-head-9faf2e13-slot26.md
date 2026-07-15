# THM-M-1235 proof-phase recheck at `9faf2e13`

Item: `S56-M-1235-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `9faf2e13566ce7ad1047f54337157387eaed48bf`

Base tree: `438505eefd23e6c86d2100b87e98212be6fd8675`

## Verdict

`blocked`. A legal positive proof body cannot inhabit the exact frozen target.
Two independent, tracked, placeholder-free declarations kernel-check at trust
level zero:

```text
Stage1Instances.THMM1235.not_wolibnerGlobalExistenceAndUniqueness :
  Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness

Stage1Instances.THMM1235.independently_not_wolibnerGlobalExistenceAndUniqueness :
  Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness
```

`Motion.conditionI_areaPreservingSelfHomeomorphism` through
`Motion.conditionVIII_continuousSpatialDerivatives` are freely chosen values
of type `Prop`; they are not proofs of predicates constraining the five motion
functions. The primary refutation changes an alleged unique motion's
`velocityX` to `velocityX + 1`; the independent refutation instead changes its
`pressure` to `pressure + 1`. Both updates preserve the `Motion` type.
`SameMotion` would equate the changed and original function, but evaluation at
`(0, 0), 0` yields the contradiction `x + 1 = x`. Concrete source data
discharge every explicit target premise.

This refutes the frozen formal encoding, not Wolibner's mathematical theorem.
Proving a corrected, weaker, or conditional proposition would be a forbidden
target substitution. `root_of_existence_and_uniqueness` assumes the
substantive existence and uniqueness packages and therefore supplies only
conditional composition, not root proof credit.

The item remains `[ ]`. No proof receipt, accepted obligation, audit
completion, theorem completion, validation completion, or release is claimed.
No `.stage1-worker-selftest.json` is written because the requested positive
proof phase is not genuinely complete. The frozen graph projects the root as
`[H3, M3, R4]`; this run leaves that authoritative vector unchanged and
recommends an `M5` exact-target blocker classification to the integration lane.

## Failed Gate And Retry

The first failed gate is exact-target consistency at
`M1235-S-DEFINITIONS`. Reopen `S56-M-1235-STATEMENT`, define conditions
`(I)`-`(VIII)` as predicates of the five functions, and make `Motion` carry
proofs of those predicates. Equality must also be scoped to the source domain
and `0 <= t <= T`, unless the source justifies equality of globally defined
functions; otherwise off-domain or off-interval perturbations remain possible.
Then re-audit the source and publish a versioned re-freeze of the canonical
expression fingerprint, source crosswalk, obligation registry, typed graphs,
and dependent evidence before proof execution resumes.

The predecessor `S56-M-1235-OBLIGATION_TREE` is still worker-provisional rather
than master-accepted. Two later gates are independently open:
`validation-specs.json` uses legacy shell-command strings instead of the
structured recipe schema required by rev-5.6 section 10.5, and the intake
README/crosswalk has not been reconciled with the later source pinpoints. None
of these later defects changes the earlier truth blocker.

The authoritative DAG still records `attempts=0` and no children despite many
earlier structured rechecks. The master/scheduler should reconcile attempts
and reopen or split the invalid upstream statement work under blueprint
section 10.2 instead of issuing another identical proof-only retry. This worker
did not edit authoritative state.

## Validation

All checks reused existing pinned artifacts read-only. No `lake update`, `lake
build`, dependency clone/fetch/checkout, network access, or `.lake` mutation
was performed. The automation-provided untracked `Formalizations/Lean/.lake`
symlink makes this nonrelease evidence. Temporary Lean sources and objects
were removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | Rank 159; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1235/check_statement.py` | 0 | Canonical expression fingerprint `77aec2f5...`; all four structural mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py` | 0 | 15 obligations and 37 typed edges passed; denominator `9e0bff35...`; frozen root remains open M3. |
| Isolated tracked `lake env lean --trust=0 -t0` recipe below | 0 | Exact statement and both tracked negative modules elaborated; all four negative axiom reports were `[propext, Classical.choice, Quot.sound]`. |
| Prohibited-construct scan over `Proof.lean` and `IndependentRefutation.lean` | 0 | No prohibited proof construct was present. |
| `lake env lean --version` and `lake --version` from `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3...`; Lake `5.0.0-src+98dc76e`. |
| Manifest-pinned dependency revision/tree and input `sha256sum` checks | 0 | Environment revisions and all eight recorded input digests matched the JSON packet. |
| JSON parse and focused semantic assertions | 0 | Packet syntax, item/base identity, unfinished state, refutation, and noncompletion fields passed. |
| Tracked and explicit new-file `git diff --check` checks | 0 | No whitespace diagnostics; no-index exit 1 for each new artifact meant only that its clean added-file diff was nonempty. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

Exact successful Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1235
tmp=$(mktemp -d "$lean_root/.thm-m-1235-proof-9faf2e13-slot26.XXXXXX")
cleanup() { rm -rf "$tmp"; }
trap cleanup EXIT HUP INT TERM
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
cp "$target/IndependentRefutation.lean" "$tmp/IndependentRefutation.lean"
cd "$lean_root"
lean=$(timeout --foreground 120 lake env which lean)
lean_path=$(timeout --foreground 120 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout --foreground --kill-after=10s 600 "$lean" --trust=0 -t0 \
  --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout --foreground --kill-after=10s 600 "$lean" --trust=0 -t0 \
  --root="$tmp" -o "$tmp/Proof.olean" "$tmp/Proof.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout --foreground --kill-after=10s 600 "$lean" --trust=0 -t0 \
  --root="$tmp" -o "$tmp/IndependentRefutation.olean" \
  "$tmp/IndependentRefutation.lean"
sha256sum "$tmp/Statement.olean" "$tmp/Proof.olean" \
  "$tmp/IndependentRefutation.olean"
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib revision/tree
`8a178386ffc0f5fef0b77738bb5449d50efeea95` /
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; `flt-regular` revision/tree
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` /
`32c9eace926573a9981787ae97643e520353c893`. Frozen input SHA-256 values:

- `Statement.lean`: `e59d7e8cb43f010533d3354022a042a38a27edc95337775da69c6cc8676a1697`
- `Proof.lean`: `f4afdf626cadef5e7acc9047ef8c517506de7d31fa49a9ed261f2fcc53cb6156`
- `IndependentRefutation.lean`: `71bf09285270d9b296eba46129722027ba2a3a968cde71633f3c0a657a95aa4c`
- `ObligationTree.lean`: `1f244092eded09ae8a474ad4cab0bd1dadac3157c7bbde6b7d73fce4d0d24fb5`
- `obligation-registry.json`: `967ef5ce046879f2da967678e3a7353c44e69a0286804b10397fd4b446a4779e`
- `typed-graphs.json`: `a60f1a527b26db45d619fb50819be8a54804268290d9b345bf2f744bfea47e11`
- `anchor-audit.json`: `e97e800b23920f911df8fb349dfa036fba13fbed790ca104c7291e6ea536f48e`
- `validation-specs.json`: `ac97fc72f4f5eb27cacb154ea03d0bf6c9c765b081316f2fba63313465f3f081`

Temporary object digests were
`cbb0b49360973c6a3e9e45d45965f51efbadf0914f10448c5e68e2dd3654497d`
for `Statement.olean`,
`3af4a429ebac82bfe937a5acd5039cfe0984cead67492d0f9b46d41f3e761169`
for `Proof.olean`, and
`a06c3ab25b0a901364d85a3ac1b2993452810f88edf013f3458545d6622b4b5d`
for `IndependentRefutation.olean`.

## Status Boundary

This current-base artifact is negative, nonrelease blocker evidence. It does
not satisfy `S56-M-1235-PROOF`, propose `[_]` or `[x]`, or support audit or
theorem completion. The retry must begin with statement correction and a
versioned re-freeze; repeating proof search against this exact encoding cannot
close the item.
