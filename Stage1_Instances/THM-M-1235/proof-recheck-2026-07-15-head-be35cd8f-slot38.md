# THM-M-1235 proof-phase recheck at `be35cd8f`

Item: `S56-M-1235-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `be35cd8f5123e9d06247b12859f3843bdd90c66f`

Base tree: `a275a21a449fbcbd6c2333f5cfe737e906b20db6`

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

The frozen typed graph still projects `[H3, M3, R4]`; this packet makes no
authoritative vector change and recommends `[H5, M5, R4]` for master review.
The older planned `instance.json` projection remains `[H2, M4, R4]`, another
reconciliation that is outside this proof worker's authority.

## Failed Gate And Retry

The first failed gate is the rev-5.6 section 5.1 statement/exact-target
consistency gate at `M1235-S-DEFINITIONS`. Reopen `S56-M-1235-STATEMENT`, define conditions
`(I)`-`(VIII)` as predicates of the five functions, and make `Motion` carry
proofs of those predicates. Equality must also be scoped to the source domain
and `0 <= t <= T`, unless the primary source justifies equality of the globally
defined functions. Re-audit the source and publish a versioned re-freeze of the
canonical expression fingerprint, source crosswalk, obligation registry,
typed graphs, and dependent evidence before proof execution resumes.

The predecessor `S56-M-1235-OBLIGATION_TREE` remains worker-provisional, so
master proof acceptance is separately dependency-blocked. Twenty earlier
structured proof recheck JSON packets are already tracked at current HEAD,
while the authoritative DAG still records `attempts=0` and no child nodes. The
master/scheduler should reconcile these apparent retries with the authoritative
attempt count. If at least five qualify as unresolved execution ticks,
blueprint section 10.2 requires a split before another proof-only retry. This
worker did not edit the DAG or generated checklist.

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
| `python3 Stage1_Instances/THM-M-1235/check_statement.py` | 0 | Exact expression hash matched; all four structural mutations were killed; pinned mathlib/toolchain identity matched. |
| `python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py` | 0 | 15 obligations and 37 typed edges passed; denominator `9e0bff352aff0e8315b2e5d9067ad143dcc8eb1a5fbf5f4a81ca703dcfaaf9ba`; root open M3, existence and uniqueness M4. |
| Isolated `lake env lean --trust=0 -t0` replay below | 0 | Exact statement and both tracked negative declarations elaborated; both axiom reports were `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '^\s*(?:sorry|admit|axiom|constant|opaque|unsafe|implemented_by|extern)\b|sorryAx|native_decide' Stage1_Instances/THM-M-1235/Proof.lean` | 1 | Expected no-match: `Proof.lean` contains no prohibited proof construct. |
| `sha256sum` over the seven frozen inputs | 0 | All current input hashes matched the structured packet. |
| `cd Formalizations/Lean && lake env lean --version`; inspect pinned dependency HEAD/tree revisions; hash `lean-toolchain` and `lake-manifest.json` | 0 | Lean version/commit, dependency revisions/trees, toolchain hash, and manifest hash matched the structured packet. |
| `python3 -m json.tool Stage1_Instances/THM-M-1235/proof-recheck-2026-07-15-head-be35cd8f-slot38.json` | 0 | Structured blocker packet is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-1235` | 0 | No whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

Exact successful Lean replay, run from `Formalizations/Lean`:

```bash
set -euo pipefail
export LEAN_NUM_THREADS=1
tmp=$(mktemp -d ./.proof-recheck-be35cd8f-slot38.XXXXXX)
cleanup() { rm -rf "$tmp"; }
trap cleanup EXIT
cp ../../Stage1_Instances/THM-M-1235/Statement.lean "$tmp/Statement.lean"
cp ../../Stage1_Instances/THM-M-1235/Proof.lean "$tmp/Proof.lean"
LEAN_PATH_BASE=$(lake env printenv LEAN_PATH)
timeout 300 lake env lean --trust=0 -t0 \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$LEAN_PATH_BASE" \
  timeout 300 lake env lean --trust=0 -t0 \
  -o "$tmp/Proof.olean" "$tmp/Proof.lean"
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
`2202187492723df27a5b2509fc6fbe7fabdd80bb70f9c8700c165f7fcd7b6d65`
for `Statement.olean` and
`e4d9a63232911a6cf9f197011c496ce329ee718cbb6e47208db9d2fab0d61699`
for `Proof.olean`.

## Status Boundary

This current-base artifact is negative, nonrelease blocker evidence. It does
not satisfy `S56-M-1235-PROOF`, propose `[_]` or `[x]`, or support audit or
theorem completion. The retry must begin with statement correction and a
versioned re-freeze; repeating proof search against this exact encoding cannot
close the item.
