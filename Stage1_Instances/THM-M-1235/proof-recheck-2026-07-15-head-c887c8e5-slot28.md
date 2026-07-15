# THM-M-1235 proof-phase recheck at `c887c8e5`

Item: `S56-M-1235-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `c887c8e5d7afe589d4b90386654421a60e998f51`

Base tree: `7a1298612a32286e2a542ffc410cf4de9bb1fabd`

## Verdict

`blocked`. No legal positive proof body can inhabit the exact frozen target.
The tracked, placeholder-free declaration

```text
Stage1Instances.THMM1235.not_wolibnerGlobalExistenceAndUniqueness :
  Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness
```

kernel-checks at trust level zero against the current pinned environment.
`Motion.conditionI_areaPreservingSelfHomeomorphism` through
`Motion.conditionVIII_continuousSpatialDerivatives` are values of type `Prop`,
not proof fields for predicates on the five functions. Updating an alleged
unique motion's `velocityX` to `velocityX + 1` therefore preserves the
`Motion` type. `SameMotion` would equate the original and updated velocity
functions, but evaluation at `(0, 0), 0` gives the contradiction `x + 1 = x`.
The concrete `counterexampleData` discharges every explicit target premise.

This refutes the frozen formal encoding, not Wolibner's mathematical theorem.
A proof of a corrected, weaker, or conditional proposition would be forbidden
target substitution. In particular, `root_of_existence_and_uniqueness` assumes
both substantive packages and supplies conditional composition only.

The item remains `[ ]`. No positive proof receipt, accepted obligation, audit
completion, theorem completion, validation completion, or release is claimed.
No `.stage1-worker-selftest.json` is written because the assigned proof phase
is not genuinely complete. The accepted root vector remains `[H3, M3, R4]`;
this packet proposes `[H5, M5, R4]` only as a diagnosis for master review.

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

The predecessor `S56-M-1235-OBLIGATION_TREE` is only worker-provisional, so
master proof acceptance is also dependency-blocked. The planned lifecycle
cannot carry accepted execution state. This independent state gate does not
change the earlier truth blocker.

Forty-four earlier structured proof recheck JSON packets are tracked at this
base while the authoritative DAG still records `attempts=0` and no child
nodes. Under blueprint section 10.2, the master/scheduler must reconcile the
attempt count and split or reopen the defective predecessor work rather than
schedule another identical proof-only retry. This worker did not edit the DAG
or generated checklist.

## Validation

All checks reused the existing pinned Lake closure. No `lake update`, `lake
build`, dependency clone/fetch/checkout, network access, or `.lake` mutation
was performed. The automation-provided untracked `Formalizations/Lean/.lake`
symlink makes this nonrelease evidence. Temporary Lean sources and outputs
were removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | Rank 159; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py` | 0 | 15 obligations and 37 typed edges passed; denominator `9e0bff352aff0e8315b2e5d9067ad143dcc8eb1a5fbf5f4a81ca703dcfaaf9ba`; frozen root remains open M3. |
| Isolated tracked `lake env lean --trust=0 -t0` recipe below | 0 | Exact statement and both tracked negative theorems elaborated; axiom reports were `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '^\s*(?:sorry\|admit\|axiom\|constant\|opaque\|unsafe\|implemented_by\|extern)\b\|sorryAx\|native_decide' Stage1_Instances/THM-M-1235/Proof.lean` | 1 | Expected no-match: `Proof.lean` contains no prohibited proof construct. |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| Manifest-pinned dependency revision/tree and input `sha256sum` checks | 0 | Environment revisions and all seven recorded input digests matched the JSON packet. |
| `python3 -m json.tool Stage1_Instances/THM-M-1235/proof-recheck-2026-07-15-head-c887c8e5-slot28.json` | 0 | The paired structured blocker packet is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-1235` | 0 | No whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

Exact successful Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1235
tmp=$(mktemp -d "$lean_root/.thm-m-1235-proof-c887c8e5-slot28.XXXXXX")
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
cd "$lean_root"
lean_path=$(timeout --foreground --kill-after=5s 120s lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" nice -n 10 \
  timeout --foreground --kill-after=5s 600s lake env lean \
  --trust=0 -t0 -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" nice -n 10 \
  timeout --foreground --kill-after=5s 600s lake env lean \
  --trust=0 -t0 -o "$tmp/Proof.olean" "$tmp/Proof.lean"
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `flt-regular`
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`. Input SHA-256 values:

- `Statement.lean`: `e59d7e8cb43f010533d3354022a042a38a27edc95337775da69c6cc8676a1697`
- `Proof.lean`: `f4afdf626cadef5e7acc9047ef8c517506de7d31fa49a9ed261f2fcc53cb6156`
- `ObligationTree.lean`: `1f244092eded09ae8a474ad4cab0bd1dadac3157c7bbde6b7d73fce4d0d24fb5`
- `obligation-registry.json`: `967ef5ce046879f2da967678e3a7353c44e69a0286804b10397fd4b446a4779e`
- `typed-graphs.json`: `a60f1a527b26db45d619fb50819be8a54804268290d9b345bf2f744bfea47e11`
- `anchor-audit.json`: `e97e800b23920f911df8fb349dfa036fba13fbed790ca104c7291e6ea536f48e`
- `validation-specs.json`: `ac97fc72f4f5eb27cacb154ea03d0bf6c9c765b081316f2fba63313465f3f081`

The isolated object digests were
`c077617be06b602f2a1bc009ffead94aaab6bb53a9a92c709816fa4b743bcb30`
for `Statement.olean` and
`dfad04e5757670a1d48d455a79d292ca6df597ccc527898fab8c65813243ee62`
for `Proof.olean`.

## Status Boundary

This current-base artifact is negative, nonrelease blocker evidence. It does
not satisfy `S56-M-1235-PROOF`, propose `[_]` or `[x]`, or support audit or
theorem completion. The retry must begin with statement correction and a
versioned re-freeze; repeating proof search against this exact encoding cannot
close the item.
