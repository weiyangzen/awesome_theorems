# Theorem quality landmark review v5.5

This directory preserves the unified review of 1,200 identities from the pinned
1000+ named-theorem candidate pool. It is an existing-catalog quality review,
not a release append and not a universal importance or frontier ranking.

The frozen decisions are:

- 439 eligible for existing-entry quality credit;
- 714 pending further statement or identity review;
- 47 rejected;
- 0 new release theorem credits;
- 0 strict conjecture credits.

The frozen ledger above is not rewritten. A later, separately pinned
Wikipedia-statement plus human reference-match review for the parent-pending
indices in `0..66` lives at
`reviews/wiki-reference-review-000-066.json`. It reviews exactly 51 rows:

- 30 gain existing-entry quality credit;
- 15 remain pending;
- 6 become rejects;
- 0 gain new release theorem credit; and
- 0 claim an externally checked proof.

`landmark-overlay-000-066.json` carries those bounded changes without mutating
the frozen ledger. The deterministic
`landmark-ledger-0-1199-overlay-000-066.json` aggregate therefore moves from
439 to 469 existing-quality credits, with 678 pending and 53 rejected. The
release inventory remains 2,500 theorem-status records and 1,000 effective
strict conjectures; this overlay changes neither count.

A second, disjoint review at
`reviews/wiki-reference-review-067-133.json` examines the 52 parent-pending
rows in that range under the same exact-statement plus human-reference-match
rule. It grants 27 existing-entry quality credits, leaves 19 pending, and
rejects 6 non-atomic theorem families. `landmark-overlay-067-133.json` is
chained to the frozen `0..66` aggregate; it does not rewrite the first layer.
The cumulative
`landmark-ledger-0-1199-overlay-000-133.json` therefore contains 496
existing-quality credits, 645 pending rows, and 59 rejects. Both new-inventory
deltas remain exactly zero.

`landmark-ledger-0-1199.json` binds every decision to the repository-owned
source, reference-candidate asset, and one of the six review slices under
`reviews/`. Reference candidates remain unverified citation leads and grant no
credit automatically.

`mathlib-important-inventory-1000.json` is the complementary, complete
quality ledger for the 1,000 mathlib theorem identities admitted in releases
5.3 and 5.4. It uses a deliberately operational importance gate: 180 rows are
mapped by maintainers to the mathlib 1000-theorems list, and 820 are explicitly
named by maintainers as module `Main statements` results. All 1,000 bind exact
formal statements, pinned kernel-checked proofs without `sorry`, catalog
identities, source records, and rights. It qualifies existing inventory only;
new theorem identity and new proof credit are both zero. It does not assert a
universal ranking of mathematics.

Two legacy NaturalProofs scratch-path locators in the 0–199 slice were replaced
with the pinned repository join asset. The original upstream content hash and
the pre-migration slice and ledger hashes remain recorded as provenance; no
ephemeral filesystem path remains authoritative.

Reproduce and verify the ledger from the repository root:

```bash
python3 Docs/catalog/v5/tools/build_theorem_quality_landmark_v5_5.py --check
python3 Docs/catalog/v5/tools/check_theorem_quality_landmark_v5_5.py
python3 -m unittest Docs.catalog.v5.tests.test_theorem_quality_landmark_v5_5
python3 Docs/catalog/v5/tools/build_theorem_quality_wiki_review_000_066_v5_5.py
python3 Docs/catalog/v5/tools/check_theorem_quality_wiki_review_000_066_v5_5.py
python3 Docs/catalog/v5/tools/build_theorem_quality_landmark_overlay_v5_5.py --check
python3 Docs/catalog/v5/tools/check_theorem_quality_landmark_overlay_v5_5.py
python3 -m unittest Docs.catalog.v5.tests.test_theorem_quality_wiki_overlay_v5_5
python3 Docs/catalog/v5/tools/build_theorem_quality_wiki_review_067_133_v5_5.py --check
python3 Docs/catalog/v5/tools/check_theorem_quality_wiki_review_067_133_v5_5.py
python3 Docs/catalog/v5/tools/build_theorem_quality_landmark_overlay_067_133_v5_5.py --check
python3 Docs/catalog/v5/tools/check_theorem_quality_landmark_overlay_067_133_v5_5.py
python3 -m unittest Docs.catalog.v5.tests.test_theorem_quality_wiki_overlay_067_133_v5_5
python3 Docs/catalog/v5/tools/build_mathlib_important_inventory_v5_5.py --check
python3 Docs/catalog/v5/tools/check_mathlib_important_inventory_v5_5.py --repo-root .
python3 -m unittest Docs.catalog.v5.tests.test_mathlib_important_inventory_v5_5
```
