# Strict research-conjecture quality inventory v5.5

`strict-research-inventory-1000.json` qualifies the exact 1,000 effective
strict-conjecture identities in release 5.4 under explicit operational source
gates:

- 400 are exact truth-apt propositions curated by Formal Conjectures in its
  pinned `research open` category;
- 245 are high-interest and 355 are medium-interest author-labeled research
  conjectures accepted from the pinned OpenConjecture source and curation.

Every row is joined to the 5.4 strict-credit ledger and claim catalog. Formal
Conjectures rows replay their exact archive member, byte range, raw block, and
formal proposition. OpenConjecture rows replay the exact source JSONL record,
LaTeX body, author/truth review gates, high-or-medium importance assessment,
open-source label, semantic curation, and CC-BY-4.0 rights gate.

This is a source-qualified inventory, not a universal importance ranking or an
independent current-literature survey. It upgrades the quality classification
of existing strict identities; it grants zero new conjecture identities.

Rebuild and independently check it from the repository root:

```bash
python3 Docs/catalog/v5/tools/build_strict_conjecture_research_inventory_v5_5.py --check
python3 Docs/catalog/v5/tools/check_strict_conjecture_research_inventory_v5_5.py --repo-root .
python3 -m unittest Docs.catalog.v5.tests.test_strict_conjecture_research_inventory_v5_5
```
