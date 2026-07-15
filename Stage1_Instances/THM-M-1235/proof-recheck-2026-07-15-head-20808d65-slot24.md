# THM-M-1235 proof-phase recheck at `20808d65`

Item: `S56-M-1235-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T17:24:24+08:00`

Base revision: `20808d65f53d8801e78f061504b93bb7efd49489`

Base tree: `a5bf33a278a7a285878c89177838ae1a0dcc9990`

## Verdict

`blocked`. No legal positive proof body can inhabit the exact frozen target.
The tracked, placeholder-free declaration

```text
Stage1Instances.THMM1235.not_wolibnerGlobalExistenceAndUniqueness :
  Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness
```

freshly kernel-checks at trust level zero against the current pinned
environment. `Motion.conditionI_areaPreservingSelfHomeomorphism` through
`Motion.conditionVIII_continuousSpatialDerivatives` are freely chosen values
of type `Prop`, not proofs of predicates constraining the five motion
functions. Updating an alleged unique motion's `velocityX` to `velocityX + 1`
therefore preserves the `Motion` type. `SameMotion` would equate the original
and updated velocity functions, but evaluation at `(0, 0), 0` yields the
contradiction `x + 1 = x`. The concrete `counterexampleData` discharges every
explicit premise of the target.

This refutes the frozen formal encoding, not Wolibner's mathematical theorem.
Proving a corrected, weaker, conditional, or otherwise substituted proposition
would violate the assigned exact-target gate. `root_of_existence_and_uniqueness`
assumes both substantive packages and provides only conditional composition; it
does not supply a positive root proof.

The item remains `[ ]`. No proof receipt, accepted obligation, audit
completion, theorem completion, validation completion, release, or master
acceptance is claimed. No `.stage1-worker-selftest.json` is written because the
requested positive proof phase is not genuinely complete. The planned instance
record remains `[H2, M4, R4]`, and the later worker-provisional graph remains
`[H3, M3, R4]`; this packet proposes `[H5, M5, R4]` only as a diagnosis for
master reconciliation.

## Failed gate and retry

The first failed gate is the rev-5.6 section 5.1 exact-statement/encoding gate
at `M1235-S-DEFINITIONS`. Reopen `S56-M-1235-STATEMENT`, define conditions
`(I)`-`(VIII)` as predicates of the five functions, and make `Motion` carry
proofs of those predicates. Equality must also be scoped to the source domain
and `0 <= t <= T`, unless the primary source justifies equality of globally
defined functions. Re-audit the source and publish a versioned re-freeze of the
canonical expression fingerprint, source crosswalk, obligation registry,
typed graphs, and dependent evidence before proof execution resumes.

`S56-M-1235-OBLIGATION_TREE` is only worker-provisional, so master proof
acceptance is independently dependency-blocked. Forty earlier structured
proof-recheck JSON packets were present at this base while the authoritative
DAG still records `attempts=0` and no child nodes. The master/scheduler must
reconcile that history. If at least five packets qualify as unresolved
execution ticks, section 10.2 requires reopening or splitting the invalid
upstream work rather than scheduling another identical proof-only retry. This
worker did not edit the DAG or generated checklist.

## Validation

All checks reused the existing pinned Lake closure. No `lake update`, `lake
build`, dependency clone/fetch/checkout, network access, or `.lake` mutation
was performed. The automation-provided untracked `Formalizations/Lean/.lake`
symlink makes this nonrelease evidence. Temporary Lean sources and objects were
removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | Rank 159; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py` | 0 | 15 obligations and 37 typed edges passed; denominator `9e0bff352aff0e8315b2e5d9067ad143dcc8eb1a5fbf5f4a81ca703dcfaaf9ba`; root remains open M3. |
| `timeout --foreground --kill-after=10s 600 python3 Stage1_Instances/THM-M-1235/check_statement.py` | 0 | Canonical expression digest `77aec2f595a800d145317ae7b7574b9b18dcd2546254e98c9a7e119fbd053c23`; all four structural mutations were killed; pins matched. |
| Isolated trust-zero pinned-Lean recipe below | 0 | Exact statement and both tracked negative theorems elaborated; axiom reports were `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '^\\s*(?:sorry|admit|axiom|constant|opaque|unsafe|implemented_by|extern)\\b|sorryAx|native_decide' Stage1_Instances/THM-M-1235/Proof.lean` | 1 | Expected no-match: `Proof.lean` contains no prohibited proof construct. |
| Exact environment and input commands below | 0 | Lean 4.29.0, Lake 5.0.0, dependency revisions/trees, clean dependency states, and all frozen input hashes matched this packet. |
| `python3 -m json.tool Stage1_Instances/THM-M-1235/proof-recheck-2026-07-15-head-20808d65-slot24.json` plus focused `jq` assertions | 0 | JSON syntax and blocker identity, base, state, noncompletion, and changed-path invariants passed. |
| `git diff --check -- Stage1_Instances/THM-M-1235`; `git diff --no-index --check /dev/null <new-artifact>` separately for both files | 0 / 1 each | The tracked diff check passed; each no-index check returned only the expected added-file status 1 and emitted no whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

Exact successful Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-1235
lean_root=$repo/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-1235-proof-20808d65-slot24.XXXXXX)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
lean_path=$(cd "$lean_root" && timeout 120 lake env printenv LEAN_PATH)
lean_bin=$(cd "$lean_root" && timeout 120 lake env which lean)
cd "$lean_root"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 600 "$lean_bin" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 600 "$lean_bin" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/Proof.olean" "$tmp/Proof.lean"
sha256sum "$tmp/Statement.olean" "$tmp/Proof.olean"
```

The object digests were
`cbb0b49360973c6a3e9e45d45965f51efbadf0914f10448c5e68e2dd3654497d`
for `Statement.olean` and
`3af4a429ebac82bfe937a5acd5039cfe0984cead67492d0f9b46d41f3e761169`
for `Proof.olean`.

Exact environment and input commands:

```bash
cd Formalizations/Lean
lake env lean --version
lake --version
cd ../..
git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}
git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain
git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD HEAD^{tree}
git -C Formalizations/Lean/.lake/packages/flt-regular status --porcelain
sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json \
  Stage1_Instances/THM-M-1235/Statement.lean \
  Stage1_Instances/THM-M-1235/Proof.lean \
  Stage1_Instances/THM-M-1235/ObligationTree.lean \
  Stage1_Instances/THM-M-1235/obligation-registry.json \
  Stage1_Instances/THM-M-1235/typed-graphs.json \
  Stage1_Instances/THM-M-1235/anchor-audit.json \
  Stage1_Instances/THM-M-1235/validation-specs.json
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; `flt-regular`
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`, tree
`32c9eace926573a9981787ae97643e520353c893`. Frozen input SHA-256
values:

- `Statement.lean`: `e59d7e8cb43f010533d3354022a042a38a27edc95337775da69c6cc8676a1697`
- `Proof.lean`: `f4afdf626cadef5e7acc9047ef8c517506de7d31fa49a9ed261f2fcc53cb6156`
- `ObligationTree.lean`: `1f244092eded09ae8a474ad4cab0bd1dadac3157c7bbde6b7d73fce4d0d24fb5`
- `obligation-registry.json`: `967ef5ce046879f2da967678e3a7353c44e69a0286804b10397fd4b446a4779e`
- `typed-graphs.json`: `a60f1a527b26db45d619fb50819be8a54804268290d9b345bf2f744bfea47e11`
- `anchor-audit.json`: `e97e800b23920f911df8fb349dfa036fba13fbed790ca104c7291e6ea536f48e`
- `validation-specs.json`: `ac97fc72f4f5eb27cacb154ea03d0bf6c9c765b081316f2fba63313465f3f081`

## Status boundary

This current-base artifact is negative, nonrelease blocker evidence. It does
not satisfy `S56-M-1235-PROOF`, propose `[_]` or `[x]`, or support audit or
theorem completion. The retry must begin with statement correction and a
versioned re-freeze; repeating proof search against this exact encoding cannot
close the item.
