# Release documentation stale-surface audit

> Audit date: 2026-08-10
>
> Scope: repository-facing Stage5 mathematics inventory and Stage6
> renumbering documentation
>
> Status: resolved historical audit. This file grants no theorem,
> conjecture, Putnam, relation, migration, checklist, or release credit.

## Resolution

Stage5 5.6 and Stage6 6.0 have now been locally published, independently
checked, and selected by their authenticated current pointers. All stale
surfaces identified below were either updated to the released values or
explicitly labelled as historical snapshots.

| Released surface | Authenticated result |
|---|---|
| Stage5 current | 5.6; 5,525 catalog rows, 3,500 theorems, 2,025 broad open claims, 1,425 strict conjectures |
| Stage5 quality | 1,000 important landmarks plus 582 disjoint additional-frontier identities; zero unsupported credit; no extra identity count |
| Stage5 5.6 addition | 1,000 kernel-checked, sorry-free formal propositions; 92 ready-unselected and 469 quarantine rows remain zero-credit |
| Stage6 current | 6.0; 9,009 historical identities, 8,997 terminal claims, 8,779 families; numbering change only |
| Putnam boundary | 768 coordinates, 675 PutnamBench keys, and 1,724 formal variants remain source/intake counts with zero catalog credit |
| Git boundary | local workspace publication only; `git ls-files Docs/catalog` still returns zero paths |

The authoritative current summary is the
[final 5.6/6.0 release review](./Stage5_5_6_Stage6_6_0_Final_Release_Review_2026-08-10.md).

## Decision boundary

The final Stage5 5.6 and Stage6 6.0 values were copied from their manifests,
authenticated current-release pointers, independent acceptance receipts, and
successful live checker replays. Candidate ledgers, generator constants,
planned paths, provisional hashes, and agent reports remain nonpublication
evidence.

Every final user-facing summary must keep these denominators separate:

- theorem catalog records;
- the kernel-checked, sorry-free formal-proposition subset;
- effective strict-conjecture credits;
- separately typed `open_problem` records;
- syntactic conjecture rows whose strict credit may differ from their syntax;
- noncredit candidates and quarantine rows;
- Putnam problem seeds, formal variants, closure nodes, and relation edges;
- local content-addressed publication versus Git-tracked or pushed content.

## Historical stale surfaces and their resolution

At the prepublication audit point, the following files made current-state
claims that predated 5.6/6.0. Their disposition is now:

| Path | Historical stale surface | Resolution |
|---|---|---|
| `README.md` | At-a-glance table, catalog links, repository tree, and current-status prose pointed to 5.4 | Updated to Stage5 5.6, Stage6 6.0, exact denominators, zero-credit Putnam boundary, and local-only Git boundary |
| `Docs/catalog/v5/README.md` | Release boundary, chain, counts, checks, and readable surfaces ended at 5.4 | Updated through authenticated current 5.6, including 5.5 quality and 5.6 selection dispositions |
| `Docs/evidence/Math_Inventory_Delta_Audit.md` | Current inventory and net additions ended at 5.4 | Replaced with 5.6 inventory, per-release deltas, quality overlays, and candidate dispositions |
| `Docs/evidence/Theorem_Source_Landscape_Audit.md` | Original 5.4 finding was phrased as current | Current 5.6 update placed first; original measurements retained under an explicit historical boundary |
| `Docs/reviews/Stage5_Math_Expansion_Release_Review.md` | Terminal review stopped at 5.3 | Explicitly marked historical and linked to the new final 5.6/6.0 review |
| `Docs/Stage5_Math_Expansion_Blueprint.md` | Twelve bounded 5.0/5.1 checklist rows were blank | All twelve accepted after replay of the original gates; scope explicitly remains the bounded historical tranche |
| `Docs/Stage5_Math_Expansion_Gantt.md` | Generated monitor reported twelve `not_started` rows | Regenerated from the accepted Blueprint; reports twelve accepted and zero unfinished |
| `Docs/catalog/v6/README.md` | Instructions described parent 5.5 and no Stage6 release | Replaced with authenticated parent 5.6 and current Stage6 6.0 publication instructions |
| `Docs/catalog/v6/qualifications/README.md` | Named `parent-5.5.json` as the accepted final path | Replaced with authenticated `parent-5.6.json`; parent 5.5 is labelled superseded history |

## Intentional historical references

Not every older version string is stale. These references must remain, with
their historical role made explicit:

- immutable release roots and counts for Stage5 5.0 through 5.5;
- the 5.4 Stage6 engineering fixture under
  `Docs/catalog/v6/fixtures/parent-5.4/`;
- the superseded parent-5.5 candidate/qualification artifacts retained under
  an explicitly nonrelease history boundary;
- release-origin descriptions for the 5.2 OpenConjecture append, the 5.3 and
  5.4 mathlib appends, and the 5.5 strict-conjecture/quality append;
- the initial 5.4 measurements in the theorem-source landscape audit;
- `rev-5.6` references in the THM-M-0387 dossier, which name a dossier
  revision and not Stage5 catalog release 5.6.

The PutnamBench intake contract correctly freezes Stage5 5.5 as its parent
input. That input binding must not be rewritten merely because 5.6 later
becomes current.

## Evidence already replayed for the bounded Stage5 checklist

The following original 5.0/5.1 gates were replayed on the shared integrated
tree during this audit and exited successfully:

```text
python3 Docs/tools/build_v4_import_receipt_v5.py --check
PASS ... ATV/S4=3484/3484 THM=3262 redirects/splits=8/4 outputs=13

python3 Docs/tools/generate_math_catalog_v5.py --check
PASS ... releases=5.0,5.1

python3 scripts/check_math_catalog_v5.py
PASS ... S5.0 origin theorem/open=1000/1000; S5.1 new theorem=500

python3 Docs/tools/render_math_catalog_v5.py --release 5.0 --check
PASS ...

python3 Docs/tools/render_math_catalog_v5.py --release 5.1 --check
PASS ...

python3 -m unittest scripts/test_v4_import_receipt_v5.py
Ran 10 tests ... OK

python3 -m unittest scripts/test_extract_formal_conjectures_v5.py
Ran 12 tests ... OK

python3 -m unittest scripts/test_math_catalog_v5.py
Ran 22 tests ... OK
```

This evidence, the terminal review, and the checked readable surfaces support
the now-accepted bounded checklist. The generated Gantt reports all twelve
items accepted and no unfinished item.

## Putnam and mathlib released boundary

The full Putnam source/intake layer authenticates a 768-coordinate grid, a
675-key PutnamBench subset, and 1,724 formal-variant files. Those are different
universes and release 5.6 grants them zero catalog or relation credit.
Problem rows and proof-assistant variants must never be reported as additional
theorems. Source-audit relation candidates must never be reported as accepted
one-hop relation edges.

The completed mathlib 5.6 transaction grants theorem credit to exactly 1,000
selected formal-proposition identities. Its formal proposition unit must not
be relabelled as a human-level named-theorem identity. The 92 unselected-ready
and 469 quarantine rows remain outside released counts.

## Git boundary observed during the audit

At the audit point, `git ls-files Docs/catalog` returned zero paths, as did the
query for the Stage5 Blueprint/Gantt and the relevant evidence/review trees.
The shared workspace is on `main` at
`9c299dbabd34878a420db46ca66d687886fe2b04`, with `Docs/catalog/` and the
audited Stage5 documentation trees untracked. Therefore a successful local
release and current-pointer compare-and-swap must still be described as a
local workspace publication, not as committed, merged, or pushed content.

The final documentation audit must rerun this Git query rather than assuming
the boundary is unchanged.
