# THM-M-1235 proof-phase recheck at `8c4a58ee`

Item: `S56-M-1235-PROOF`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `8c4a58ee73da7fa8dce7a9f9bfcc0ec5fd713588`

Base tree: `3fa6104e948efe18f95dcfc23e9d2bf7f3dad150`

## Verdict

`blocked`. No legal positive proof body can inhabit the exact frozen target in
the pinned consistent environment. The tracked placeholder-free declaration

```text
Stage1Instances.THMM1235.not_wolibnerGlobalExistenceAndUniqueness :
  Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness
```

kernel-checks at trust level zero. `Motion` stores conditions `(I)`--`(VIII)`
as fields whose values have type `Prop`; it does not store proofs of predicates
that constrain the five motion functions. Given an alleged unique motion,
`perturbVelocityX` replaces its `velocityX` with `velocityX + 1` while
preserving the `Motion` type. `SameMotion` would equate those functions, but
evaluation at `(0, 0), 0` contradicts `x + 1 != x`. The concrete
`counterexampleData` satisfies every explicit premise at `T = 1`, so the
target is not merely refuted through a vacuous or impossible premise.

This refutes the frozen encoding, not Wolibner's mathematical theorem.
Proving a corrected, conditional, or weaker proposition would substitute the
assigned target. The conditional declaration `root_of_existence_and_uniqueness`
assumes both substantive packages and supplies no root proof body; its current
uniqueness premise is itself impossible for the unconstrained `Motion` type.

The item remains `[ ]`. No proof receipt, accepted obligation, audit
completion, theorem completion, validation completion, or release is claimed.
No `.stage1-worker-selftest.json` is written because the assigned positive
proof phase is not complete. The frozen root vector remains `[H3, M3, R4]`;
this run records an M5 exact-target blocker for integration-lane reconciliation
without changing the authoritative vector.

## Failed Gate And Retry

The first failed gate is exact-target consistency at
`M1235-S-DEFINITIONS`. Reopen `S56-M-1235-STATEMENT`, define every domain,
source-data, and motion condition as a predicate of the data or five functions,
and make the structures carry proofs of those predicates. The corrected model
must also restrict the five functions to the source domain and `0 <= t <= T`,
or restrict `SameMotion` to pointwise equality there; global function equality
would remain vulnerable to an off-domain or off-interval perturbation. Re-audit
the primary source formulation, then version and re-freeze the canonical
expression, source crosswalk, obligation registry, typed graphs, and dependent
evidence before proof execution resumes.

The source crosswalk is also stale: it says the stable scan, theorem pages,
definitions, hypotheses, and formulation remain open while later statement
artifacts claim exact pinpoints and a source-faithful freeze. This does not
alter the earlier consistency blocker.

There is a further source-scope mismatch to resolve at re-freeze: the current
root always assumes source decay and never branches on `containsInfinity`,
whereas the cited source distinguishes bounded from infinity-containing
regions. Resolving that mismatch belongs to the statement/source audit, not to
a proof-body workaround.

## Validation

All successful Lean checks used the existing pinned Lake closure. No `lake
update`, `lake build`, dependency clone/fetch, or intentional `.lake` mutation
was performed. The automation-provided untracked `Formalizations/Lean/.lake`
link points to the canonical checkout, so this is nonrelease evidence. During
one statement-validator attempt, concurrent activity in that shared canonical
cache temporarily left the pinned `flt-regular` repository without a resolvable
`HEAD`; that attempt exited 1. After its manifest-pinned commit was again
present, the validator was rerun unchanged and exited 0. The isolated target
kernel replay does not import `flt-regular` and passed independently. All
temporary target files and outputs were removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | Rank 159; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py` | 0 | 15 obligations and 37 typed edges passed; denominator `9e0bff352aff0e8315b2e5d9067ad143dcc8eb1a5fbf5f4a81ca703dcfaaf9ba`; root open M3, existence and uniqueness M4. |
| `timeout 300 python3 Stage1_Instances/THM-M-1235/check_statement.py` (first attempt) | 1 | Concurrent shared-cache race: pinned `flt-regular` could not resolve `HEAD`; no dependency fetch/update was attempted. |
| `timeout 300 python3 Stage1_Instances/THM-M-1235/check_statement.py` (unchanged rerun) | 0 | Expression SHA-256 `77aec2f595a800d145317ae7b7574b9b18dcd2546254e98c9a7e119fbd053c23`; all four mutations killed; manifest pins matched. |
| Isolated `lake env lean --trust=0 -t0` recipe below | 0 | Exact statement and both tracked negative theorems elaborated; both axiom reports were `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '\b(?:sorry\|admit\|axiom)\b\|sorryAx\|unsafe' Stage1_Instances/THM-M-1235/Proof.lean` | 1 | Expected no-match result: no prohibited construct occurs in the refutation module. |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD` (post-race check) | 0 | Manifest-pinned `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`. |
| `python3 -m json.tool Stage1_Instances/THM-M-1235/proof-recheck-2026-07-14-head-8c4a58ee.json` | 0 | Current-base structured blocker is valid JSON. |
| Scoped tracked and new-file `git diff --check` | 0 | No whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

Exact successful Lean recipe, run from `Formalizations/Lean`:

```bash
set -euo pipefail
export LEAN_NUM_THREADS=1
tmp=$(mktemp -d ./.thm-m-1235-slot34-8c4a58ee.XXXXXX)
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

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Input SHA-256 values:

- `Statement.lean`: `e59d7e8cb43f010533d3354022a042a38a27edc95337775da69c6cc8676a1697`
- `Proof.lean`: `f4afdf626cadef5e7acc9047ef8c517506de7d31fa49a9ed261f2fcc53cb6156`
- `obligation-registry.json`: `967ef5ce046879f2da967678e3a7353c44e69a0286804b10397fd4b446a4779e`
- `typed-graphs.json`: `a60f1a527b26db45d619fb50819be8a54804268290d9b345bf2f744bfea47e11`
- `anchor-audit.json`: `e97e800b23920f911df8fb349dfa036fba13fbed790ca104c7291e6ea536f48e`
- `validation-specs.json`: `ac97fc72f4f5eb27cacb154ea03d0bf6c9c765b081316f2fba63313465f3f081`

## Status Boundary

This current-base artifact is negative, nonrelease blocker evidence. It does
not satisfy `S56-M-1235-PROOF`, propose provisional or accepted state, or
support audit/theorem completion. The retry must begin at the statement phase;
repeating proof search against this exact encoding cannot close the item.
