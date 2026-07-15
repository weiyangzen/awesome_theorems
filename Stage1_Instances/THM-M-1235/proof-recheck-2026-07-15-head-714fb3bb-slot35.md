# THM-M-1235 proof-phase recheck at `714fb3bb`

Item: `S56-M-1235-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `714fb3bb6a070c2f659ece069f1a7219f9c045a0`

Base tree: `2c99a78c5fa247aebc885f31e6818fc029f17a60`

## Verdict

`blocked`. No legal positive proof body can inhabit the exact frozen target in
the checked foundation. The existing placeholder-free declaration

```text
Stage1Instances.THMM1235.not_wolibnerGlobalExistenceAndUniqueness :
  Not Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness
```

freshly elaborates at trust level zero against the pinned Lean executable and
the available compiled mathlib artifacts. `Motion` stores conditions `(I)`
through `(VIII)` as freely chosen values of type `Prop`; it does not store
proofs of predicates constraining the five motion functions. Replacing an
alleged unique motion's `velocityX` with `velocityX + 1` therefore preserves
the `Motion` type, while `SameMotion` would equate the two functions. Evaluating
that equality at `(0, 0), 0` is contradictory. The concrete
`counterexampleData` discharges all explicit target premises.

This refutes the frozen formal encoding, not Wolibner's mathematical theorem.
A corrected, weaker, conditional, or differently scoped target would be a
forbidden substitution in this proof item. The conditional declaration
`root_of_existence_and_uniqueness` also provides no root credit because its two
substantive packages remain hypotheses.

The item remains `[ ]`. No proof receipt, accepted obligation, debt-vector
change, audit completion, theorem completion, validation completion, release,
or master acceptance is claimed. `.stage1-worker-selftest.json` is deliberately
absent because the requested positive proof phase is not complete.

## Failed Gate And Retry

The first failed gate is `S56-5.1-EXACT-TARGET-CONSISTENCY` at
`M1235-S-DEFINITIONS`. Reopen `S56-M-1235-STATEMENT`; define conditions
`(I)`-`(VIII)` as predicates of the five functions and make `Motion` carry
proofs of them. Scope uniqueness to the source domain and `0 <= t <= T` unless
the primary source justifies equality everywhere. Then re-audit the source and
publish a versioned re-freeze of the statement fingerprint, source crosswalk,
obligation registry, typed graphs, and dependent evidence before proof work
resumes.

The proof task is independently dependency-blocked because
`S56-M-1235-OBLIGATION_TREE` is only worker-provisional (`[_]`), not master
accepted. At this base, 28 earlier structured proof-recheck JSON packets were
already tracked while the authoritative DAG still records `attempts=0` and no
children. The scheduler must reconcile this discrepancy and apply the
section 10.2 split/reopen rule rather than issue another identical proof-only
retry. This worker did not edit the DAG or generated checklist.

## Narrow Validation

No `lake update`, `lake build`, dependency clone/fetch/checkout, network access,
or `.lake` mutation was requested or performed. The automation-provided
untracked `Formalizations/Lean/.lake` symlink exposes a shared canonical cache,
so this is nonrelease evidence. The manifest-pinned `flt-regular` checkout has
an invalid `HEAD`; required `lake env` validation timed out. No repair was
attempted. Because this target imports only mathlib, the narrow supplementary
replay used the exact pinned Lean executable and existing compiled package
artifacts while excluding the unavailable unrelated package.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | Rank 159; lifecycle `planned`; baseline L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1235/check_obligation_tree.py` | 0 | 15 obligations and 37 typed edges passed; root open M3; existence and uniqueness remain M4. |
| `cd Formalizations/Lean && timeout 30 lake env lean --version` | 124 | Timed out with no output; no dependency action followed. |
| `timeout 60 python3 Stage1_Instances/THM-M-1235/check_statement.py` | 124 | Timed out with no output while using the same Lake route. |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse --verify HEAD` | 128 | `fatal: Needed a single revision`; `.git/HEAD` is `ref: refs/heads/.invalid`. |
| Isolated direct trust-zero Lean replay below | 0 | The exact statement and both tracked negative theorems elaborated; axiom reports were `[propext, Classical.choice, Quot.sound]`. |
| `rg -n --pcre2 '^\s*(?:sorry\|admit\|axiom\|constant\|opaque\|unsafe\|implemented_by\|extern)\b\|sorryAx\|native_decide' Stage1_Instances/THM-M-1235/Proof.lean` | 1 | Expected no-match exit; no prohibited construct occurs in `Proof.lean`. |
| `python3 -m json.tool Stage1_Instances/THM-M-1235/proof-recheck-2026-07-15-head-714fb3bb-slot35.json` | 0 | The structured blocker packet is valid JSON. |
| `git diff --no-index --check /dev/null <each new owned artifact>` | 1 | Expected new-file diff exit; no whitespace diagnostic was emitted. |

The successful supplementary Lean recipe copied only `Statement.lean` and
`Proof.lean` to a temporary directory, compiled them with
`leanprover/lean4:v4.29.0`, `LEAN_NUM_THREADS=1`, `--trust=0`, `-t0`, and the
existing compiled mathlib paths, hashed the temporary objects, and removed the
directory. The resulting SHA-256 values were:

- `Statement.olean`: `cbb0b49360973c6a3e9e45d45965f51efbadf0914f10448c5e68e2dd3654497d`
- `Proof.olean`: `3af4a429ebac82bfe937a5acd5039cfe0984cead67492d0f9b46d41f3e761169`

Pinned identities and frozen proof inputs were unchanged:

- Lean commit: `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- canonical expression SHA-256: `77aec2f595a800d145317ae7b7574b9b18dcd2546254e98c9a7e119fbd053c23`
- `Statement.lean`: `e59d7e8cb43f010533d3354022a042a38a27edc95337775da69c6cc8676a1697`
- `Proof.lean`: `f4afdf626cadef5e7acc9047ef8c517506de7d31fa49a9ed261f2fcc53cb6156`
- obligation denominator: `9e0bff352aff0e8315b2e5d9067ad143dcc8eb1a5fbf5f4a81ca703dcfaaf9ba`

## Status Boundary

This is a current-base, nonrelease blocker artifact. It does not satisfy
`S56-M-1235-PROOF` or propose `[_]`/`[x]`. The only legal retry starts with a
corrected, source-faithful statement and versioned downstream re-freeze.
