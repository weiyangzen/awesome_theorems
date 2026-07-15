# THM-M-1235 proof-phase recheck at `5bb51543`

Item: `S56-M-1235-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `5bb515438bd0e1d53584e5243c5d434dfde7158e`

Base tree: `8055b8d863f0978f110a628ab3ccc7ab1e146b12`

## Verdict

`blocked`. No legal positive proof body can inhabit the exact frozen target.
The tracked, placeholder-free declaration

```text
Stage1Instances.THMM1235.not_wolibnerGlobalExistenceAndUniqueness :
  Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness
```

kernel-checks at trust level zero against the pinned environment. The fields
`Motion.conditionI_areaPreservingSelfHomeomorphism` through
`Motion.conditionVIII_continuousSpatialDerivatives` are freely chosen values
of type `Prop`; they are not proofs of predicates constraining the five motion
functions. Updating an alleged unique motion's `velocityX` to `velocityX + 1`
therefore preserves the `Motion` type. `SameMotion` would equate the old and
new velocity functions, but evaluation at `(0, 0), 0` yields the contradiction
`x + 1 = x`. The concrete `counterexampleData` discharges every explicit
premise of the canonical target.

This refutes the frozen formal encoding, not Wolibner's mathematical theorem.
Proving a corrected, weaker, or conditional proposition would be a forbidden
target substitution. In particular, `root_of_existence_and_uniqueness` assumes
the substantive existence and uniqueness packages; it is only conditional
composition and supplies no root proof body.

The item remains `[ ]`. No proof receipt, accepted obligation, audit
completion, theorem completion, validation completion, release, or master
acceptance is claimed. No `.stage1-worker-selftest.json` is written because
the requested positive proof phase is not genuinely complete.

## Failed Gate And Retry

The first failed gate is `S56-5.1-EXACT-TARGET-CONSISTENCY` at
`M1235-S-DEFINITIONS`. Reopen `S56-M-1235-STATEMENT`, define conditions
`(I)`-`(VIII)` as predicates of the five functions, and make `Motion` carry
proofs of those predicates. Equality must also be scoped to the source domain
and `0 <= t <= T`, unless the primary source justifies equality of the globally
defined functions. Re-audit the source and publish a versioned re-freeze of the
canonical expression fingerprint, source crosswalk, obligation registry,
typed graphs, and dependent evidence before proof execution resumes.

The predecessor `S56-M-1235-OBLIGATION_TREE` remains worker-provisional, so
master proof acceptance is separately dependency-blocked. Nineteen earlier
structured proof recheck JSON packets were already tracked at this base while
the authoritative DAG still records `attempts=0` and no child nodes. Under
blueprint section 10.2, the master/scheduler must reconcile the attempt count
and reopen or split the item rather than schedule another identical proof-only
retry. This worker did not edit the DAG or generated checklist.

## Validation

All checks reused the automation-provided symlink to the existing pinned Lake
closure. No `lake update`, `lake build`, dependency clone/fetch/checkout,
network access, or `.lake` mutation was performed. Temporary Lean sources and
objects were removed. The symlink is untracked, so this is nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | Rank 159; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py` | 0 | 15 obligations and 37 typed edges passed; denominator `9e0bff352aff0e8315b2e5d9067ad143dcc8eb1a5fbf5f4a81ca703dcfaaf9ba`; root open M3, existence and uniqueness M4. |
| Isolated `lake env lean --trust=0 -t0` replay below | 0 | Exact statement and both tracked negative declarations elaborated; both axiom reports were `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '^\s*(?:sorry|admit|axiom|constant|opaque|unsafe|implemented_by|extern)\b|sorryAx|native_decide' Stage1_Instances/THM-M-1235/Proof.lean` | 1 | Expected no-match: `Proof.lean` contains no prohibited proof construct. |
| `sha256sum` over the seven frozen inputs | 0 | All current input hashes matched the structured packet. |
| `cd Formalizations/Lean && lake env lean --version`; inspect pinned dependency HEAD/tree revisions; hash `lean-toolchain` and `lake-manifest.json` | 0 | Lean version/commit, dependency revisions/trees, toolchain hash, and manifest hash matched the structured packet. |
| `python3 -m json.tool Stage1_Instances/THM-M-1235/proof-recheck-2026-07-15-head-5bb51543-slot23.json` | 0 | Structured blocker packet is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-1235` | 0 | No whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

Exact successful Lean replay, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1235
tmp=$(mktemp -d "$lean_root/.thm-m-1235-proof-5bb51543-slot23.XXXXXX")
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
cd "$lean_root"
lean_path=$(timeout 120 lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 600 lake env lean \
  --trust=0 -t0 -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 600 lake env lean \
  --trust=0 -t0 -o "$tmp/Proof.olean" "$tmp/Proof.lean"
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib revision/tree
`8a178386ffc0f5fef0b77738bb5449d50efeea95` /
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; `flt-regular`
revision/tree `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` /
`32c9eace926573a9981787ae97643e520353c893`.

Frozen input SHA-256 values:

- `Statement.lean`: `e59d7e8cb43f010533d3354022a042a38a27edc95337775da69c6cc8676a1697`
- `Proof.lean`: `f4afdf626cadef5e7acc9047ef8c517506de7d31fa49a9ed261f2fcc53cb6156`
- `ObligationTree.lean`: `1f244092eded09ae8a474ad4cab0bd1dadac3157c7bbde6b7d73fce4d0d24fb5`
- `obligation-registry.json`: `967ef5ce046879f2da967678e3a7353c44e69a0286804b10397fd4b446a4779e`
- `typed-graphs.json`: `a60f1a527b26db45d619fb50819be8a54804268290d9b345bf2f744bfea47e11`
- `anchor-audit.json`: `e97e800b23920f911df8fb349dfa036fba13fbed790ca104c7291e6ea536f48e`
- `validation-specs.json`: `ac97fc72f4f5eb27cacb154ea03d0bf6c9c765b081316f2fba63313465f3f081`

The temporary object digests were
`4ef9c0c831f40893e3f02a80bfa7fee8183791cb32b31b34abe1ec3943170f17`
for `Statement.olean` and
`8568915566e61eb93a86a1721e8570e9b3189bb6c301df0039081917e5ab6c1b`
for `Proof.olean`.

## Status Boundary

This current-base artifact is negative, nonrelease blocker evidence. It does
not satisfy `S56-M-1235-PROOF`, propose `[_]` or `[x]`, or support audit or
theorem completion. The retry must begin with statement correction and a
versioned re-freeze; repeating proof search against this exact encoding cannot
close the item.
