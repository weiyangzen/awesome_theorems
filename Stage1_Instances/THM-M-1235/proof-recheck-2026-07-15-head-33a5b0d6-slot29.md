# THM-M-1235 proof-phase recheck at `33a5b0d6`

Item: `S56-M-1235-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `33a5b0d654c92a894e155f5385edaae684091bb0`

Base tree: `74ed89524afb3c118e31a7fce9b5763fee26b180`

## Verdict

`blocked`. A legal positive proof body cannot inhabit the exact frozen target.
The tracked, placeholder-free declaration

```text
Stage1Instances.THMM1235.not_wolibnerGlobalExistenceAndUniqueness :
  Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness
```

kernel-checks at trust level zero against the current pinned Lean and mathlib
artifacts. `Motion.conditionI_areaPreservingSelfHomeomorphism` through
`Motion.conditionVIII_continuousSpatialDerivatives` are bare `Prop` values,
not proofs of predicates constraining the five motion functions. Replacing an
alleged unique motion's `velocityX` by `velocityX + 1` therefore preserves the
`Motion` type. `SameMotion` would equate the changed and original velocity
functions, but evaluation at `(0, 0), 0` gives the contradiction `x + 1 = x`.
The concrete `counterexampleData` discharges every explicit premise.

This refutes the frozen formal encoding, not Wolibner's mathematical theorem.
A proof of a corrected, weaker, or conditional proposition would be a forbidden
target substitution. In particular, `root_of_existence_and_uniqueness` assumes
both substantive packages and supplies only conditional composition. Although
the malformed existence package is trivially inhabitable, uniqueness and the
root are refuted.

The item remains `[ ]`. No proof receipt, accepted obligation, audit completion,
theorem completion, validation completion, or release is claimed. No
`.stage1-worker-selftest.json` is written because the assigned positive proof
phase is not genuinely complete. The frozen graph projects the root as
`[H3, M3, R4]`; this run leaves that authoritative vector unchanged and
recommends an `M5` exact-target blocker classification to the integration lane.

## Failed Gate And Retry

The first failed gate is rev-5.6 section 5.1 exact-target consistency at
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

## Validation

All checks reused existing pinned artifacts read-only. No `lake update`, `lake
build`, dependency clone/fetch/checkout, network access, or `.lake` mutation was
performed. The automation-provided untracked `Formalizations/Lean/.lake`
symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | Rank 159; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1235/check_statement.py` | 1 | Environmental setup blocker before elaboration: root Lake could not resolve the automation-provided `flt-regular` checkout's `HEAD`, which is `ref: refs/heads/.invalid`. The checkout was not repaired or mutated. |
| `python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py` | 0 | 15 obligations and 37 typed edges passed; denominator `9e0bff352aff0e8315b2e5d9067ad143dcc8eb1a5fbf5f4a81ca703dcfaaf9ba`; root open M3, existence and uniqueness packages M4. |
| First isolated replay with unadjusted nested mathlib paths | 1 | Setup failure only: the nested dependency paths contained no oleans, so Lean reported unknown module prefix `Batteries`; no target evidence was credited. |
| Corrected isolated trust-zero replay below | 0 | Exact statement and both tracked negative declarations elaborated; both axiom reports were `[propext, Classical.choice, Quot.sound]`. |
| Prohibited-construct `rg --pcre2` scan of `Proof.lean` | 1 | Expected no-match: no `sorry`, `admit`, bodyless declaration, unsafe/oracle construct, or `native_decide`. |
| `sha256sum` over the seven frozen inputs | 0 | Every digest matched the structured packet. |
| Inspect pinned Lean, mathlib, and `flt-regular` identities and hash `lean-toolchain` / `lake-manifest.json` | 0 | Lean version/commit, mathlib revision/tree, manifest-pinned `flt-regular` commit object/tree, toolchain hash, and manifest hash matched the structured packet. |
| `git diff --check --no-index /dev/null <new-artifact>` for each artifact | 1 each | Expected new-file diff exits with no whitespace diagnostics. |
| `git diff --check -- Stage1_Instances/THM-M-1235` | 0 | No diagnostics for tracked deltas; the no-index checks covered the two untracked artifacts. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The successful replay ran from the pinned mathlib workspace. Its `lake env`
supplied the pinned Lean 4.29.0 environment and mathlib path; the eight nested
dependency paths were redirected to the corresponding already materialized
root-cache olean paths because the nested copies contained no build artifacts:

```bash
set -euo pipefail
export PATH="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin:$PATH"
export ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0
export LEAN_NUM_THREADS=1
cd Formalizations/Lean/.lake/packages/mathlib
tmp=$(mktemp -d ./.proof-recheck-33a5b0d6-slot29.XXXXXX)
cleanup() { rm -rf "$tmp"; }
trap cleanup EXIT
cp ../../../../../.cron/stage1-rev56/workers/slot29/Stage1_Instances/THM-M-1235/Statement.lean "$tmp/Statement.lean"
cp ../../../../../.cron/stage1-rev56/workers/slot29/Stage1_Instances/THM-M-1235/Proof.lean "$tmp/Proof.lean"
LEAN_PATH_BASE=$(lake env printenv LEAN_PATH)
CANON=/home/sansha-2/external/awesome_theorems/Formalizations/Lean/.lake/packages
LEAN_PATH_BASE=$(printf '%s' "$LEAN_PATH_BASE" | sed \
  "s#$CANON/mathlib/.lake/packages/Cli#$CANON/Cli#g; \
   s#$CANON/mathlib/.lake/packages/batteries#$CANON/batteries#g; \
   s#$CANON/mathlib/.lake/packages/Qq#$CANON/Qq#g; \
   s#$CANON/mathlib/.lake/packages/aesop#$CANON/aesop#g; \
   s#$CANON/mathlib/.lake/packages/proofwidgets#$CANON/proofwidgets#g; \
   s#$CANON/mathlib/.lake/packages/importGraph#$CANON/importGraph#g; \
   s#$CANON/mathlib/.lake/packages/LeanSearchClient#$CANON/LeanSearchClient#g; \
   s#$CANON/mathlib/.lake/packages/plausible#$CANON/plausible#g")
LEAN_PATH="$LEAN_PATH_BASE" timeout 300 lean --trust=0 -t0 \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$LEAN_PATH_BASE" timeout 300 lean --trust=0 -t0 \
  -o "$tmp/Proof.olean" "$tmp/Proof.lean"
sha256sum "$tmp/Statement.olean" "$tmp/Proof.olean"
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib revision/tree
`8a178386ffc0f5fef0b77738bb5449d50efeea95` /
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; manifest-pinned
`flt-regular` commit/tree `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` /
`32c9eace926573a9981787ae97643e520353c893`. The latter commit object is
present, but the checkout's `HEAD` is invalid.

Frozen input SHA-256 values:

- `Statement.lean`: `e59d7e8cb43f010533d3354022a042a38a27edc95337775da69c6cc8676a1697`
- `Proof.lean`: `f4afdf626cadef5e7acc9047ef8c517506de7d31fa49a9ed261f2fcc53cb6156`
- `ObligationTree.lean`: `1f244092eded09ae8a474ad4cab0bd1dadac3157c7bbde6b7d73fce4d0d24fb5`
- `obligation-registry.json`: `967ef5ce046879f2da967678e3a7353c44e69a0286804b10397fd4b446a4779e`
- `typed-graphs.json`: `a60f1a527b26db45d619fb50819be8a54804268290d9b345bf2f744bfea47e11`
- `anchor-audit.json`: `e97e800b23920f911df8fb349dfa036fba13fbed790ca104c7291e6ea536f48e`
- `validation-specs.json`: `ac97fc72f4f5eb27cacb154ea03d0bf6c9c765b081316f2fba63313465f3f081`

Temporary object digests were
`56646c45e436c4462166a555c434f2e5768c61c43133e8e3ecbe52fc10ef0db6`
for `Statement.olean` and
`7ed63ccaa25b3466ef5555eb945801a4b414a67d1ce45cafaa0c37075c3e2ffb`
for `Proof.olean`.

## Status Boundary

This current-base artifact is negative, nonrelease blocker evidence. It does
not satisfy `S56-M-1235-PROOF`, propose `[_]` or `[x]`, or support audit or
theorem completion. The retry must begin with statement correction and a
versioned re-freeze; repeating proof search against this exact encoding cannot
close the item.
