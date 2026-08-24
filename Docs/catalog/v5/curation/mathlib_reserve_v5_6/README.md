# mathlib verified reserve for a future v5.6 release

This directory materializes the previously count-only mathlib reserve without
changing release 5.5, `Current_Release.json`, any ID registry, or any
PutnamBench artifact.

## Result

The pinned extractor was replayed at mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, Lean 4.29.0, with the same
1000+ metadata checkout at commit
`8e04b97dd24adc6e931be78a884da7e935bc8780` used by the 1,500-row parent
asset. The generated 2,566-row source preserves those 1,500 parent row objects
exactly and appends all 1,066 previously count-only verified rows.

| boundary | count |
|---|---:|
| source-screened runtime `thmInfo`, `uses_sorry = false` | 2,575 |
| selected by the existing truth **and documentation** gate | 2,566 |
| exact/whitespace-normalized proposition identities in those 2,566 rows | 2,561 |
| already admitted mathlib theorems in release 5.5 | 1,000 |
| documented, unadmitted, unique runtime `thmInfo` identities | 1,561 |
| v5.6 theorem records sourced from literal `theorem` / `lemma` commands | 1,072 / 489 |
| exact-identity duplicate losers, all permanently noncredit | 5 |
| independently machine-qualified generator accepted set | 1,092 |
| semantic-variant/family review quarantine | 469 |
| new 1,066-row tail: literal `theorem` / `lemma` | 842 / 224 |
| new-tail literal theorems after exact-identity dedupe | 841 |
| older 5.4 residual literal theorems still unique against 5.5 | 231 |
| reliable mathlib formal-identity inventory if all 1,561 are accepted | **2,561** |

The single new-tail duplicate is
`Measurable.coe_nnreal_real`, whose whitespace-normalized formal type is
identical to the earlier `Measurable.coe_nnreal_ennreal` candidate. The new
tail has zero exact-type, normalized-type, or normalized-full-name conflicts
with the complete 4,525-row release-5.5 catalog.

Nine further declarations passed the Lean runtime truth gate but lack both an
individual declaration docstring and a module Main-result description. They
remain listed in the inventory as metadata-quality exclusions and are not
included in the directly materialized 2,566-row source. A future dedicated
extractor could add them after sealing their source syntax and full row
payloads; this package does not grant them credit.

## v5.6 theorem-record policy and generator lanes

All 2,566 selected rows are compiled Lean theorem constants and are sorry-free
at the pinned commit. In Lean, source commands named `lemma` and `theorem` both
produce `ConstantInfo.thmInfo`. The v5.6 candidate policy therefore emits all
1,561 unadmitted canonical identities as `theorem_record_kind = theorem` while
preserving the original keyword separately as `source_syntax_kind`. It does
not discard the 489 lemma-syntax records.

Exact formal-type and normalized-type dedupe leaves five noncredit losers and
finds zero conflicts between the 1,561 canonical candidates and the complete
2,500-row parent theorem surface. A second, deliberately conservative semantic
screen then compares exact display labels, embedded Markdown-bold named-result
labels, explicit parent aliases, Wikidata IDs, declaration docstrings,
normalized mathlib declaration leaves, and exact module Main-result
descriptions. It routes 469 rows with any such signal to
`semantic_variant_review_quarantine`; 1,092 rows with no such signal enter
`provisional_generator_admission`.

These semantic signals are candidate evidence, not equivalence judgments.
Shared module prose or a shared declaration leaf can describe related but
different theorems, so quarantine requires review rather than automatic
merging. Conversely, absence of these signals does not prove human-level
mathematical distinctness. The exact claim that is already established is
2,561 unique, kernel-checked formal proposition identities—not necessarily
2,561 independently adjudicated named theorem concepts.

They are not yet release entries. A later release generator must still allocate
append-only IDs, preserve the exact parent prefix, bind the candidate row and
source hashes, run the release checker, and publish an independent acceptance
receipt. Every row here therefore has `candidate_only = true`,
`grants_catalog_entry = false`, and `grants_theorem_credit = false`.

The importance evidence is also bounded: every new-tail row is explicitly
named in a mathlib module-doc Main results/theorems/statements bullet, but only
371 have an individualized declaration docstring. A shared module bullet may
describe several declarations. The exact formal type is authoritative; the
shared prose is not presented as an independently reviewed landmark summary.

The current proof evidence records a `collectAxioms` union for each extraction
batch. Absence of `sorryAx` from the union is enough to establish its absence
for every member of that batch, but the union is not a per-declaration direct
dependency graph and must not be reused as a Putnam one-hop relation.

## Artifacts and replay

- `mathlib-verified-theorems-8a178386-full.json` is the complete 2,566-row
  source artifact. SHA-256:
  `7075e0bb151182ae4ba01cd34945657969be4bc60f7ee4ae6a62fc518f5386c3`.
- `Mathlib_Reserve_Candidates_v5_6.jsonl` is the 1,066-row candidate-only tail,
  with a per-row source binding, truth/quality boundary, three-gate identity
  review, disposition, and row seal. Its literal-keyword quota field preserves
  the old 5.3/5.4 policy for audit; it is not the v5.6 generator policy.
- `Mathlib_Reserve_Inventory_v5_6.json` binds every input and output, hard
  counts, set digests, module-root counts, the credit boundary, and the Putnam
  join contract.
- `Mathlib_Qualified_Theorem_Candidates_v5_6.jsonl` is the generator-facing
  1,561-row canonical ledger. Every row is a theorem record, including the 489
  rows whose source keyword is `lemma`; 1,092 rows are in the provisional lane
  and 469 are quarantined for semantic-variant review.
- `Mathlib_Qualified_Batch_Inventory_v5_6.json` seals the qualified ledger,
  all five exact-identity losers, the complete 2,500-theorem parent comparison,
  semantic evidence counts, generator filters, and the zero-credit boundary.
- `build_mathlib_qualified_batch_v5_6.py` deterministically rebuilds or
  byte-checks the generator-facing ledger and inventory with fixed hard counts
  and module-root partitions.
- `Mathlib_Generator_Accepted_Set_v5_6.jsonl` is the exact 1,092-row input for a
  future release generator. It allocates no IDs and grants no credit.
- `Mathlib_Generator_Acceptance_Receipt_v5_6.json` is the independently written
  qualification receipt. It records 1,092 machine-qualified rows, 469 rows
  still pending semantic review, zero rejected canonical candidates, and five
  pre-canonical exact-type duplicate rejections.
- `check_mathlib_generator_acceptance_v5_6.py` independently rebuilds the
  canonical identity and semantic-screen partitions, checks every accepted row
  against the complete 4,525-claim parent, verifies every bound source/olean/
  ilean hash, invokes the independent 5.5 release checker, and byte-checks the
  receipt. Receipt writing additionally requires a live Lean extractor replay.
- `build_mathlib_reserve_inventory_v5_6.py` rebuilds or byte-checks the two
  derived artifacts. Its hard gates include the fixed input hashes, exact
  1,500-row prefix, all count partitions, all module-root partitions, source
  truth/rights fields, identity dispositions, row seals, and output bytes.

Static replay:

```console
python3 Docs/catalog/v5/curation/mathlib_reserve_v5_6/build_mathlib_reserve_inventory_v5_6.py
python3 Docs/catalog/v5/curation/mathlib_reserve_v5_6/build_mathlib_qualified_batch_v5_6.py
python3 Docs/catalog/v5/curation/mathlib_reserve_v5_6/build_mathlib_generator_accepted_set_v5_6.py
python3 Docs/catalog/v5/curation/mathlib_reserve_v5_6/check_mathlib_generator_acceptance_v5_6.py
```

Lean live replay additionally reruns the full pinned extractor. The supplied
1000+ checkout must be clean and at the required commit:

```console
python3 Docs/catalog/v5/curation/mathlib_reserve_v5_6/build_mathlib_reserve_inventory_v5_6.py \
  --live-replay \
  --thousand-plus-root /path/to/1000-plus-checkout
```

## Putnam one-hop interface

This reserve does not infer a relationship merely because a Putnam file
imports `Mathlib`. A one-hop formal candidate requires an exact direct constant
reference in the elaborated Putnam theorem type or in an available elaborated
solution/proof body. The join retains the mathlib declaration, formal-type
hash, module, object-file hash, and environment commit on one side, and the
Putnam problem ID, language, environment commit, direct-constant set, and
extractor hash on the other.

For authoritative human solutions such as a pinned PutnamGAP solution source,
a normalized named-theorem label may seed a crosswalk only when corroborated by
an exact Wikidata identifier or mathlib declaration and then reviewed against
the target statement. Broad topic tags, imports, transitive dependencies, and
label or embedding similarity alone are retrieval hints, not one-hop edges.
Different mathlib commits require declaration replay and elaborated-type
comparison before an edge can be accepted.
