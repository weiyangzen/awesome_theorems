# THM-M-1235 proof-phase recheck at `4d2c7723`

Item: `S56-M-1235-PROOF`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `4d2c77230343716176b4192dc38e26f4c20c7547`

Base tree: `9eebdfdfda6b289fea0b6e778fae8e13327395b2`

## Verdict

`blocked`. No legal positive proof body can inhabit the exact frozen target.
In `Statement.lean`, the eight `Motion` conditions are freely chosen values of
type `Prop`; they are not proofs of predicates constraining the motion's five
functions. The tracked placeholder-free `Proof.lean` therefore constructs a
counterexample: `perturbVelocityX` replaces any alleged unique motion's
`velocityX` by `velocityX + 1` while preserving its `Motion` type. `SameMotion`
would equate the old and new functions, but evaluation at `(0, 0), 0` gives the
contradiction `x + 1 = x`. The concrete `counterexampleData` satisfies every
explicit premise at `T = 1`.

The tracked declaration has exact type:

```text
Stage1Instances.THMM1235.not_wolibnerGlobalExistenceAndUniqueness :
  Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness
```

This refutes the frozen formal encoding, not Wolibner's mathematical theorem.
A proof of a corrected, conditional, or weaker proposition would be a forbidden
target substitution. The conditional theorem
`root_of_existence_and_uniqueness` assumes both substantive packages and gives
no root proof credit; its uniqueness package is impossible for this interface.

The item remains `[ ]`. No proof receipt, accepted obligation, provisional
state, audit completion, theorem completion, validation completion, release,
or master acceptance is claimed. No `.stage1-worker-selftest.json` is written
because the assigned positive proof phase is not genuinely complete.

## Failed Gate And Retry

The first failed gate is exact-target consistency at
`M1235-S-DEFINITIONS`. Reopen `S56-M-1235-STATEMENT`, define every domain,
source-data, and motion condition as a predicate of its data or five functions,
and make the structures carry proofs of those predicates. Restrict the five
functions to the source domain and `0 <= t <= T`, or restrict `SameMotion` to
pointwise equality there; otherwise off-domain or off-interval perturbations
still defeat global function equality. Re-audit the primary source, then issue
a versioned re-freeze of the canonical expression, source crosswalk,
obligation registry, typed graphs, and dependent evidence before proof work.

## Validation

Structural checks passed. Fresh Lean validation was attempted with the
smallest isolated `lake env lean` recipe, but Lake stopped before invoking Lean:
the existing pinned `flt-regular` repository has no resolvable `HEAD`. The
manifest-pinned commit object
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` is present, but this worker did not
repair or check it out. Per the worker contract, no `lake update`, `lake build`,
dependency fetch/clone, checkout, ref repair, or other `.lake` mutation was
performed. This missing pinned artifact is recorded as an additional validation
blocker; no fresh kernel result or axiom report is claimed by this recheck.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `15` assurance groups and `1546` uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | `1546` unique targets, ranks `1..1546`, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | Rank 159; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py` | 0 | 15 obligations and 37 typed edges passed; root open M3. |
| `cd Formalizations/Lean && lake env lean --version` | 1 | Lake could not resolve `flt-regular` `HEAD`; Lean was not launched. |
| Isolated `lake env lean --trust=0 -t0` recipe below | 1 | Same Lake preflight failure; no current-base kernel evidence claimed. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse --verify HEAD` | 128 | No resolvable `HEAD`. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse --verify 56161b6eb5281fbfe9c38f2bcec0f429ebc11a27^{commit}` | 0 | Manifest-pinned commit object exists. |
| line-level prohibited-token scan over owned Lean files | 1 | Expected no-match: no `sorry`, `admit`, `axiom`, `sorryAx`, or `unsafe` declaration. |
| `python3 -m json.tool` on this structured blocker | 0 | Valid JSON. |
| Scoped tracked/new-file whitespace checks | 0 | No whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test deliberately absent. |

Attempted isolated Lean recipe, from `Formalizations/Lean`:

```bash
set -euo pipefail
export LEAN_NUM_THREADS=1
tmp=$(mktemp -d ./.thm-m-1235-slot42-4d2c7723.XXXXXX)
cleanup() { rm -rf "$tmp"; }
trap cleanup EXIT
cp ../../Stage1_Instances/THM-M-1235/Statement.lean "$tmp/Statement.lean"
cp ../../Stage1_Instances/THM-M-1235/Proof.lean "$tmp/Proof.lean"
LEAN_PATH_BASE=$(lake env printenv LEAN_PATH)
timeout 300 lake env lean --trust=0 -t0 \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$LEAN_PATH_BASE" \
  timeout 300 lake env lean --trust=0 -t0 "$tmp/Proof.lean"
```

Input SHA-256 values:

- `Statement.lean`: `e59d7e8cb43f010533d3354022a042a38a27edc95337775da69c6cc8676a1697`
- `Proof.lean`: `f4afdf626cadef5e7acc9047ef8c517506de7d31fa49a9ed261f2fcc53cb6156`
- `obligation-registry.json`: `967ef5ce046879f2da967678e3a7353c44e69a0286804b10397fd4b446a4779e`
- `typed-graphs.json`: `a60f1a527b26db45d619fb50819be8a54804268290d9b345bf2f744bfea47e11`
- `anchor-audit.json`: `e97e800b23920f911df8fb349dfa036fba13fbed790ca104c7291e6ea536f48e`
- `validation-specs.json`: `ac97fc72f4f5eb27cacb154ea03d0bf6c9c765b081316f2fba63313465f3f081`

## Status Boundary

This current-base artifact is negative, nonrelease blocker evidence. It does
not satisfy `S56-M-1235-PROOF`, propose `[_]` or `[x]`, or support audit or
theorem completion. The retry must begin at statement correction and re-freeze;
the canonical cache owner must separately restore the already-pinned
`flt-regular` artifact before fresh validation can run.
