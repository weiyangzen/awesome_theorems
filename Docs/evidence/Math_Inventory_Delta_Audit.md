# Mathematics inventory delta audit

Audit date: 2026-08-10

This note separates released inventory, net additions, quality overlays,
source/intake universes, and unreleased candidates. A candidate, problem,
formal variant, relation edge, or plan is never counted as an addition.

## Current released workspace inventory

The authoritative Stage5 pointer is `Docs/catalog/v5/Current_Release.json`.
It points to release 5.6 and release root
`ce490ed958240ae1cabc26c3f704ad20b4103e30ad8abfd44e9c3b722fa17877`.
The independent published checker reports:

```text
catalog=5525 theorem=3500 open=2025 strict=1425 origin_theorem=1000
```

The exact accounting is:

| Class | Released count |
|---|---:|
| theorem-status records | 3,500 |
| kernel-checked, sorry-free theorem records | 2,000 |
| source-asserted, not independently replayed theorem records | 1,500 |
| effective strict-conjecture credits | 1,425 |
| broad open-claim records | 2,025 |
| syntactic `conjecture` records | 1,426 |
| separately typed `open_problem` records | 599 |
| broad-open rows without strict credit | 600 |

The raw catalog partitions as `3,500 + 1,426 + 599 = 5,525`. One syntactic
conjecture has revoked strict credit, so 1,426 must not be reported as the
strict count. The 600 non-strict broad-open rows comprise that one retained
conjecture plus 599 `open_problem` records.

## What was actually added

Release 5.0 is the first Stage5 mathematics-expansion baseline. Relative to
that materialized baseline:

| Release | Theorem addition | Effective strict-conjecture change | Notes |
|---|---:|---:|---|
| 5.1 | +500 | 0 | Formal Conjectures theorem append |
| 5.2 | 0 | +599 net | +600 credits and one inherited credit revocation |
| 5.3 | +500 | 0 | kernel-checked mathlib theorem append |
| 5.4 | +500 | 0 | kernel-checked mathlib theorem append |
| 5.5 | 0 | +425 | reviewed multi-source strict-conjecture append |
| 5.6 | +1,000 | 0 | kernel-checked mathlib formal-proposition append |
| **Net after 5.0** | **+2,500** | **+1,024** | exact released deltas |

The 5.0 effective strict baseline was 401 before the inherited correction.
The current count is `401 - 1 + 600 + 425 = 1,425`.

## Quality boundary

The quantity additions are release records, not proof that every row is a
universally important or frontier theorem. The release-bound quality
authorities separately accept:

- 1,000 important landmark theorem identities;
- 582 additional, disjoint frontier theorem identities; and
- zero unsupported importance/frontier credits.

Those are quality overlays on existing theorem identities and do not create
another 1,582 theorem records. The origin-5.6 batch adds 1,000 exact formal
proposition identities (629 Lean `theorem` syntax and 371 `lemma` syntax), all
runtime `thmInfo`, kernel-checked, and sorry-free. It explicitly does not claim
exhaustive human-level named-theorem semantic uniqueness or an independent
universal ranking.

Of the 1,561 qualified 5.6 candidates, 1,000 receive release credit, 92 ready
rows are terminally unselected, and 469 remain in semantic-review quarantine.
The latter 561 rows have no catalog ID or quota credit.

## Putnam boundary

The checked source/intake universes contain 768 Putnam coordinates, a 675-key
PutnamBench subset, and 1,724 formal variants. Release 5.6 grants all Putnam
problem seeds, formal variants, closure candidates, and relation edges zero
theorem, conjecture, open-problem, or catalog credit. These counts must remain
separate from the released inventory.

## Stage6 and Git boundary

Stage6 6.0 renumbers the complete 9,009-identity historical graph; it does not
add 9,009 mathematical records. Its current release root is
`0709742a34087727f1ef4e64d8fb5fa5b1dc3661dfbf67a83c3b7b5f6cabca5b`.

Both releases are materialized and independently checked in the shared
workspace, but `git ls-files Docs/catalog` currently returns zero paths.
“Released workspace inventory” must not be misreported as committed, merged,
or pushed to `main`.
