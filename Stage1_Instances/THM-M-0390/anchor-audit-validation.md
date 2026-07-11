# Anchor audit validation record

Item: `S56-M-0390-ANCHOR_AUDIT`  
Base revision: `3eb3bf1bab9ffff7a10bfdd0e5131144e7c71a9b`  
Search cutoff: `2026-07-11T18:30:22Z`

## Result

The immutable local closure contains no terminal Catalan/Mihailescu theorem. Pinned mathlib's
`Q174955` row has no declaration anchor. `Polynomial.flt_catalan` is a checked polynomial theorem
with a mismatched carrier and conclusion. The other identified declarations are support APIs only.

At Formal Conjectures revision `7871d8fc7a8164a1ac16c3765b40c25ce015b681`,
`Catalan.catalans_conjecture` ends in `by sorry`; it is `M5`, not upstream closure. The project's
`Nat.IsPerfectPower` is support infrastructure. No dependency was fetched or added. The canonical
root is `M3/E4`: its proposition elaborates locally, but no terminal proof body was found.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 groups, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets |
| `python3 scripts/stage1_target.py show THM-M-0390` | exit 0; rank 4, planned, incomplete |
| pinned mathlib/flt-regular `git rev-parse HEAD` | exit 0; revisions match the ledger |
| pinned-source `rg` alias queries | expected matches/nonmatches; no terminal declaration found |
| immutable raw fetch of `FormalConjectures/Wikipedia/Catalan.lean` | exit 0; SHA-256 `4d6a944a1cec1df6928207be2cdf44ad0b1e7bdc89263f9812fc93037f6b152c`; body `by sorry` |
| immutable raw fetch of `FormalConjecturesForMathlib/Data/Nat/PerfectPower.lean` | exit 0; SHA-256 `fd5dda002499ae3d1232b9ee10a2e1b91f8d4da2034cfc74e0d9fde03d9c744a`; support only |
| GitHub repository API queries | initial exact queries exit 0/zero; broader aliases HTTP 403, recorded as an access limit |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0390/Statement.lean` | exit 0; canonical statement surface re-elaborated |
| attempted mathlib import probe with `lake env lean` | exit 1; canonical shared cache contains only `Cache/*` oleans and no `Mathlib/*.olean`; recorded as a missing pinned artifact, with no fetch/build attempted |
| JSON parsing and scoped `git diff --check` | exit 0 |

Known limitation: public-project discovery is not claimed exhaustive because rate limiting
interrupted broader queries. The pinned mathlib source revision is inspectable, but its module oleans
are absent, so support declarations were not locally elaborated. These limits prevent saturation and
`AUDIT-Z` claims, but not source-level classification of discovered candidates. Obligation-tree,
proof, hermetic replay, and independent review remain.
