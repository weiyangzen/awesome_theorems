# Stage4 curated gap supplement and claim-number migration

Stage4 is a data release, not another promise to fill the catalog later.  Its
curation fragments contain evidence-bearing decisions for the frozen gap
inventory, and the generator materializes accepted exact records (claims,
entities, and events), append-only typed IDs, immutable Stage4 claim numbers,
migrations, and list projections.

## What Stage4 closes

- all 98 keys in `Coverage_Candidates_v2.json`;
- all 56 bounded candidate-delta keys in the Stage3 v3 critical audit;
- the Stage3 named regression and hard-homonym fixtures, under separately
  keyed discovery dispositions;
- preservation and Stage4 numbering of all 3,338 inherited ATV records;
- immutable historical resolution of all 3,262 legacy `THM-*` aliases;
- explicit conservation of the 76 source occurrences folded by Stage0's
  destructive six-field deduplication;
- explicit preservation/disposition of all 623 v2 domain repair proposals.

The completion claim is deliberately bounded to the audited gap supplement
and full number migration.  The inherited v2 catalog remains machine-triage
data unless a Stage4 curation record explicitly upgrades it.  Consequently,
Stage4 does **not** claim that every inherited source row has completed exact
statement, truth-status, provenance, or rights review, and it does not claim
to enumerate every theorem known to humanity.

## Identity and numbering

`ATV-*` remains the append-only canonical variant identity.  Every allocated
ATV receives exactly one immutable Stage4 number whose ordinal is identical:

```text
ATV-00000393 <-> S4-CLM-00000393
```

For example, the historical alias is resolved from the registry rather than
by arithmetic:

```text
THM-M-0387 -> ATV-00000393 -> S4-CLM-00000393
```

The old alias never changes its historical target.  Redirect and split
resolution is recorded separately; a split has no default child and conveys
no automatic proof, status, evidence, or benchmark credit.

Candidate dispositions preserve their historical `child_keys`, while current
consumers should resolve through `terminal_atv_ids`, `terminal_stage_ids`, or
the paired `terminal_children` rows.  Those terminal fields flatten redirects
without rewriting history; split candidates can therefore resolve to multiple
children and still have no implicit default.

## Authoritative inputs

- `Stage4_Curation_Manifest_v4.json` fixes the release boundary and policy.
- `fragments/Mathematics_v4.json`, `Physics_v4.json`, and
  `Computer_Science_v4.json` contain actual domain additions and sources.
- `fragments/Cross_Domain_v4.json` resolves the 36 known collision keys.
- `fragments/Regression_Fixtures_v4.json` keys and preserves the prose-only
  regression and hard-negative audit fixtures.

The three legacy Markdown source pools are byte-sealed inputs.  New material
is added through the structured fragments so old byte locators and `THM-*`
ABI do not drift.

## Generate and verify

```bash
python3 Docs/tools/generate_claim_catalog_v4.py
python3 Docs/tools/generate_claim_catalog_v4.py --check
python3 scripts/check_claim_catalog_v4.py --require-complete
python3 -m unittest scripts/test_claim_catalog_v4.py
```

JSON files are authoritative.  Markdown theorem/open surfaces are generated
projections and must have exactly the same Stage4 ID sets as their JSON
counterparts.
