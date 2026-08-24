# Stage5 mathematics expansion

Stage5 is a source-derived, append-only mathematics inventory release. It is
not a promise that a source archive has magically become a fully human-reviewed
catalog, and it does not retrofit exact semantics onto the 3,484 Stage4
variants.

The normative 5.0/5.1 files in this directory are:

- `Stage5_Math_Expansion_Contract_v5.json`: release, count, identity,
  migration, source, status, dedupe, MSC, rights, hash, and independent-checker
  rules;
- `Math_Claim_Record_Schema_v5.json`: the closed schema for every accepted
  `origin_stage=Stage5` record;
- `Math_Source_Registry_v5.json`: content-pinned source assets and their
  role-specific rights and limitations; and
- `V4_Import_Receipt_v5.json`: the immutable Stage4 ancestry and identity
  import. Stage4 records are conserved in registries and migration artifacts,
  not copied into the Stage5 exact-record schema.

Release 5.2 adds versioned contract, schema, source registry, parent strict
receipt, and OpenConjecture curation authorities with the `_v5_2.json` suffix.
Release 5.3 adds the corresponding `_v5_3.json` mathlib contract, schema,
registry and parent receipt plus `Mathlib_Theorem_Curation_v5_3.json`.
Release 5.4 adds the `_v5_4.json` contract, deeply closed record schema,
source-policy extension, 5.3 parent receipt, and residual
`Mathlib_Theorem_Curation_v5_4.json`. Its registry preserves the exact 5.3
mathlib source row; release-specific residual rules live in an explicit
`source_policy_extensions` row rather than rewriting that source identity.
Release 5.5 appends 425 reviewed strict conjectures and binds separate 1,000-
landmark and 582-additional-frontier theorem quality authorities without
adding theorem identities. Release 5.6 appends exactly 1,000 pinned mathlib
formal-proposition identities and conserves every open and strict-credit row.
The release manifest, rather than this README, is the final binding of an
authority set to immutable release bytes.

## Release boundary

The seven immutable release directories are:

```text
Docs/catalog/v5/releases/5.0/
Docs/catalog/v5/releases/5.1/
Docs/catalog/v5/releases/5.2/
Docs/catalog/v5/releases/5.3/
Docs/catalog/v5/releases/5.4/
Docs/catalog/v5/releases/5.5/
Docs/catalog/v5/releases/5.6/
```

Releases 5.0 and 5.1 each contain one manifest and seven non-manifest artifacts:

```text
Release_Manifest.json
Claim_Catalog.json
Claim_ID_Registry.json
Stage5_Claim_ID_Registry.json
Migration_v4_to_v5.json
Theorem_List.json
Open_Claim_List.json
Coverage_Ledger.json
```

Releases 5.2 through 5.6 contain those eight files plus
`Strict_Conjecture_Ledger.json`: nine files total and eight non-manifest
artifacts. `Claim_Catalog.json` contains Stage5 additions only. Each child
release is cumulative and preserves its parent's exact catalog prefix. The
identity registry and migration artifact, by contrast, cover all inherited and
new IDs, including the Stage4 ancestry.

The 5.0 manifest has `parent_release=null` and
`parent_release_root_sha256=null`; its Stage4 ancestry is proved only through
the V4 import receipt and migration chain. The 5.1 manifest names `5.0`; the
5.2 manifest names `5.1` and binds its independently recomputed release root
`ba0aeacfcad136df7eff5b08932a76bf87127bb393b6d9f8ad1eef525cf55016`.
The 5.2 release root is
`edee3a3e5f29a345a16fb526654aecfeaeaaf62da0e0101ed5e9bd2cbb374e2e`.
The 5.3 manifest names 5.2 and binds that exact root; its own release
root is
`9ec5a097c0286b6751b02e89d18c400aab655021ba1ad4843eadba5a69fc41fa`.
Release 5.4 names that exact 5.3 root; its release root is
`c6f559861849d839ceda2f10bc7878687e35d6c897ea1c316ea4523bc7673813`.
Release 5.5 names that exact 5.4 root; its release root is
`fea893e7b5d0b3b958c64ac672f9164efd06996e086c08385462527dcb75dbb0`.
Release 5.6 names that exact 5.5 root; its release root is
`ce490ed958240ae1cabc26c3f704ad20b4103e30ad8abfd44e9c3b722fa17877`.
After the independent published gate and locked compare-and-swap,
`Current_Release.json` points to 5.6.

The release root is SHA-256 of canonical JSON for the sorted non-manifest
`{path, sha256, size_bytes}` inventory, excluding `Release_Manifest.json`:
seven rows in 5.0/5.1 and eight in 5.2 through 5.6. Manifest counts are
informative and never replace recomputation from explicit ID sets.

## Actual count gates

Release 5.0 must contain at least:

- 1,000 distinct new theorem records; and
- 1,000 distinct new open-claim records (with a contract ceiling of 2,000).

Release 5.1 must append at least 500 and at most 1,000 distinct new theorem
records. It may retain a zero-to-1,000 open-candidate reserve, but reserve rows
receive no ATO/ATS/ATV/S5 ID and no quota credit until a later accepted release.

The materialized cumulative 5.2 catalog has this exact accounting:

| Measure | Count |
|---|---:|
| Stage5 catalog records | 3,100 |
| theorem-status records | 1,500 |
| syntactic `current_claim_kind=conjecture` records | 1,001 |
| effective strict-conjecture credits | 1,000 |
| `open_problem` records | 599 |

Thus the raw catalog partitions as `1,500 + 1,001 + 599 = 3,100`, while the
strict-credit denominator is a separate ledger-defined set. Release 5.2 adds
600 curated strict-credit conjectures and revokes the strict credit of the
inherited Moving Sofa row (`S5-CLM-00005311` / `ATV-00005311`) without changing
that row's identity, text, or mathematical status. Therefore 1,001 syntactic
conjecture rows must not be reported as 1,001 strict conjectures. The 599
`open_problem` rows are also reported separately and never relabeled as
conjectures.

Release 5.3 preserves that complete 5.2 prefix and appends exactly 500
literal mathlib theorem records:

| Measure | Cumulative 5.3 count |
|---|---:|
| Stage5 catalog records | 3,600 |
| theorem-status records | 2,000 |
| native 5.3 `kernel_checked_sorry_free` literal theorems | 500 |
| syntactic `current_claim_kind=conjecture` records | 1,001 |
| effective strict-conjecture credits | 1,000 |
| `open_problem` records | 599 |

The 5.3 raw partition is `2,000 + 1,001 + 599 = 3,600`. Release 5.3 adds
no open claims. Its strict ledger carries forward the parent's exact
`strict_credits`, `credit_corrections`, `counts`, and `set_digests`, including
the 5.2 Moving Sofa correction, while its own header binds release 5.3.

Release 5.4 preserves every 5.3 record and identity row, then accepts exactly
500 of the 731 residual unique literal mathlib theorems by deterministic
module-root round-robin:

| Measure | Cumulative 5.4 count |
|---|---:|
| Stage5 catalog records | 4,100 |
| theorem-status records | 2,500 |
| native 5.4 `kernel_checked_sorry_free` literal theorems | 500 |
| syntactic `current_claim_kind=conjecture` records | 1,001 |
| effective strict-conjecture credits | 1,000 |
| `open_problem` records | 599 |

The 5.4 raw partition is `2,500 + 1,001 + 599 = 4,100`. Release 5.4 adds
no open claims and preserves the exact strict-credit rows, correction, counts,
and set digests. Of the original 731 residual theorems, 500 receive new claim
and theorem credit and 231 remain noncredit reserve rows. Historical 5.3
coverage rows remain immutable; each of their 731 effective-state transitions
is recorded by a unique 5.4 row with an explicit `supersedes_candidate_key`
and parent-curation hash.

Release 5.5 preserves every theorem identity and appends 425 effective strict
conjectures:

| Measure | Cumulative 5.5 count |
|---|---:|
| Stage5 catalog records | 4,525 |
| theorem-status records | 2,500 |
| syntactic `current_claim_kind=conjecture` records | 1,426 |
| effective strict-conjecture credits | 1,425 |
| `open_problem` records | 599 |
| broad open-claim projection | 2,025 |

The 5.5 raw partition is `2,500 + 1,426 + 599 = 4,525`. One retained
syntactic conjecture has revoked strict credit, so the 2,025 broad-open rows
contain 1,425 effective strict conjectures and 600 other open entries. Release
5.5 adds no theorem identity; its important/frontier theorem ledgers are
quality overlays on existing identities.

Current release 5.6 preserves the complete 5.5 catalog prefix and appends
exactly 1,000 mathlib formal-proposition theorem records:

| Measure | Current 5.6 count |
|---|---:|
| Stage5 catalog records | 5,525 |
| theorem-status records | 3,500 |
| cumulative `kernel_checked_sorry_free` theorem records | 2,000 |
| syntactic `current_claim_kind=conjecture` records | 1,426 |
| effective strict-conjecture credits | 1,425 |
| `open_problem` records | 599 |
| broad open-claim projection | 2,025 |

The current raw partition is `3,500 + 1,426 + 599 = 5,525`. Release 5.6 adds
no open record or strict credit. Relative to release 5.0, the net additions are
2,500 theorem records and 1,024 effective strict-conjecture credits.

The early theorem minimum is deliberately source-specific. Formal Conjectures credit requires
top-level `declaration_kind=theorem`, `current_claim_kind=theorem`, and
`material_status=proved`; native 5.3 credit requires
`formal_statement.declaration_kind=theorem`, a runtime `thmInfo`, and
`proof_evidence.formal_proof_state=kernel_checked_sorry_free`. Release 5.6
instead uses one canonical runtime `thmInfo` formal proposition as its credit
unit: 629 source declarations use Lean `theorem` syntax and 371 use Lean
`lemma` syntax. The syntax is retained as provenance and never creates a
second credit. Definitions, nonclaims, and pointers cannot fill a theorem
quota.
An old formal `answer(sorry)` shape is an `open_problem`, not a blanket
`conjecture`; a `type_of%` pointer is never a claim-credit row. From 5.2 onward,
membership in the strict conjecture set comes only from
`Strict_Conjecture_Ledger.json`, not from string matching or the broad
`Open_Claim_List.json` projection.

## Frozen source and honest evidence levels

The authoritative 5.0/5.1 release source is the pinned Formal Conjectures
archive:

```text
commit  2270d31e8dd611521f979de6d86da364930b7669
archive Docs/catalog/v5/sources/formal-conjectures-2270d31e8dd611521f979de6d86da364930b7669.tar.gz
sha256  51535f4755574d97672515a75b8b076065aba2c0d79631e99fa57719f484dcc8
bytes   1614060
members 1361, including directories
```

Release 5.2 adds a second pinned source route for strict conjectures:

```text
GitHub commit       d2e3afe62098611fabd7236998acc73f64e4b3b7
Hugging Face commit fa03d85db95e6edad4ff751b490704fa8a0d9358
full JSONL sha256   8cf0a7ce4baff47769fe1ca0c40b11eed0767480c858c208a7beae8f5829dd14
eligible pool       889 records
eligible sha256     8a698e3af53ca0605a2a8ecd2e3a9944ad84157440a86f3c319effaf9792c6ce
accepted curation   600 records
curation authority  ac78c277984e1ed7e9223323dcf6b3d0a65fc3cc82edad16cda7a0020e8b4bb5
```

The eligible pool requires an explicit conjecture environment, nonempty body,
the pinned `real_open_conjecture` label at confidence at least 0.90,
per-paper CC-BY-4.0, a versioned arXiv locator, and unique content hashes. The
accepted 600 then pass the sealed curation and semantic cross-source dedupe.
Their `material_status=open` remains a pinned dataset/model assertion, not a
claim that this repository performed an independent up-to-date literature
status investigation for every row.

Release 5.3 adds the pinned mathlib theorem route:

```text
mathlib commit       8a178386ffc0f5fef0b77738bb5449d50efeea95
source artifact      Docs/catalog/v5/sources/mathlib-theorems-8a178386.json
artifact sha256      236b9f6ac192eaf87215663bfd7fadb80c439b452049cef1747ea804c458637a
source rows          1500
literal theorems     1235
literal lemmas       265 (zero theorem credit)
accepted theorems    500
curation authority   9661eebbd25bbb8aee3a0c7ae1c9cbe671ec77324f889d25e967811ffd9f7d5d
```

All 1,500 source rows were extracted from the pinned compiled environment as
`kernel_checked_sorry_free`, but release credit is narrower: only 500 selected
literal theorem declarations enter 5.3. Four source-semantic duplicates are
rejected, 731 eligible literal theorems remain unselected, and all 265 literal
lemmas receive zero theorem credit. The selection contains 180 records with a
mathlib 1000-theorems signal and 378 with a module Main-result signal, with 58
records carrying both signals. These are source-documentation importance
signals, not an independent universal ranking of mathematics.

Release 5.4 reuses those exact source bytes and the exact 5.3 source-registry
row. Its candidate denominator is only the 731 rows sealed as
`eligible_not_selected` by 5.3. The checker independently replays exact formal
type, whitespace-normalized formal type, and NFKC-casefolded full declaration
name gates against both the residual pool and the complete 5.3 catalog. The
round-robin admits 500 rows and leaves 231 (`Analysis` 155, `RingTheory` 76);
literal lemmas still receive zero credit.

Release 5.6 uses the expanded, pinned 2,566-row mathlib runtime-theorem asset.
After five exact-formal-type duplicate losers are removed, the source contains
2,561 canonical formal identities: 1,000 already present in 5.3/5.4 and 1,561
unadmitted candidates. The closed 5.6 operand dispositions those 1,561 as:

```text
mechanically ready                 1092
selected for release               1000
terminal ready but unselected        92
semantic-review quarantine          469
```

Selection first takes all 511 ready rows with an individual declaration
docstring, then takes 489 rows by deterministic module-root round-robin. Every
selected row is a runtime `thmInfo`, is kernel-checked and sorry-free at the
pinned commit, and passes the parent/batch identity gates. The record unit is
a formal proposition identity; exhaustive human-level named-theorem semantic
uniqueness and an independent universal importance ranking are explicitly not
claimed.

Release 5.5 binds a quality ledger for the complete
1,000-row union admitted by 5.3 and 5.4:

```text
ledger                 Docs/catalog/v5/curation/theorem_quality_v5_5/mathlib-important-inventory-1000.json
existing theorem rows  1000
mathlib 1000 signal    180
module Main signal     820
new theorem credit     0
```

Here “important” has an explicit operational meaning: the theorem was either
mapped by mathlib maintainers to the human-curated mathlib 1000-theorems list,
or it was named by maintainers as a module `Main statements` result. Every row
is also bound to an exact formal type, a pinned kernel-checked proof without
`sorry`, its accepted catalog identity, and source rights. This is a
human-editorial source qualification, not a claim that the ledger is a unique
or universal ranking of all mathematics. The ledger upgrades quality evidence
for existing 5.3/5.4 identities and grants no new identity or proof quota.

The same 5.5 release binds a disjoint 582-row additional-frontier theorem set
and 425 new strict conjectures. The important and frontier sets are quality
denominators over existing theorem records, not inventory additions. Their
accepted counts and zero unsupported credit remain sealed by the 5.5/5.6
release manifests and are consumed as immutable parent evidence by Stage5.1.

The full 1962--2025 Putnam source layer is also pinned and independently
checked: 768 coordinates, a 675-key PutnamBench subset, a 93-key complement,
and 1,724 formal-language variants. These are source/intake universes. Release
5.6 grants them, their closure candidates, and their relation edges zero
catalog credit; none is counted as a theorem, strict conjecture, or other open
problem.

An archive member count grants no catalog credit. Every accepted row binds its
member/file hash, exact UTF-8 byte and line range, raw-block hash, module,
namespace, qualified declaration, formal declaration, formal type, and
nonempty source docstring. The checker reads those bytes independently.

Bulk records may honestly say `source_curated_machine_extracted`,
`machine_validated_exact`, or `independent_machine_validated`. They must not say
that thousands of entries received individual human proof, importance,
frontier, status, or rights review when that did not happen.

Mathematical status and formal-proof assurance are separate axes. In
particular, a source category may assert that a theorem is solved while its
checked-in Lean body still contains `sorry`. Such a row may have
`material_status=proved` together with
`formal_proof_state=statement_elaborated_with_placeholder` or
`source_asserted_not_replayed`; it may not claim
`kernel_checked_sorry_free`. Conversely, a real sorry-free replay must be bound
to the exact source and environment evidence.

In the 5.2 theorem projection, 1,373 rows carry the pinned Formal Conjectures
`research solved` category and 127 carry the weaker `textbook` category. All
1,500 have `formal_proof_state=source_asserted_not_replayed`; 1,369 imported
declarations report `sorryAx`. These are theorem-status/source-asserted records,
not 1,500 independently human-reviewed important theorems and not 1,500
repository-replayed placeholder-free proofs.

Release 5.3 preserves those 1,500 records and their evidence unchanged, then
adds 500 separately evidenced mathlib literal theorems. Each new record binds
the exact formal type, source record and source range, compiled `.olean` and
`.ilean` hashes, the pinned commit, and a runtime theorem/axiom receipt with
`uses_sorry=false`. Its `batch_axiom_dependency_union` is explicitly a batch
union rather than an exact per-declaration dependency set, and no later-commit
status is inferred.

Release 5.4 preserves all 2,000 inherited theorem records unchanged and adds
500 records with the same pinned proof-evidence boundary. Every new nested
source, formal statement, curation, proof, rights, classification, allocation,
dedupe, and payload field is checked against the deeply closed 5.4 schema and
independently reconstructed from the source and curation authorities.

Release 5.6 preserves all 2,500 parent theorem records byte-semantically and
adds 1,000 separately evidenced formal-proposition records. This brings the
cumulative kernel-checked, sorry-free subset to 2,000 while leaving the 1,500
Formal Conjectures rows at their original weaker evidence level.

`atomicity=atomic` means one exact source-declaration allocation unit in this
import. It is not a claim that every natural-language docstring is logically
irreducible.

## Statements and conservative dedupe

The top-level `statement` is exactly the nested `mathematical_statement` after
removing only its embedded `statement_sha256`; both include
`component_extraction_status`. When hypotheses and conclusion have not been
separately parsed, they remain empty or null and the record says
`not_separately_parsed` instead of inventing a logical decomposition.

The relevant digests are:

```text
statement_sha256 = sha256(canonical_json(statement))
source_statement_sha256 = sha256(exact upstream unelaborated statement payload)
normalized_statement_sha256 = sha256(canonical_json({
  module,
  namespace,
  source_statement_sha256
}))
semantic_payload_sha256 = sha256(canonical_json({
  record_role,
  atomicity,
  truth_apt,
  normalized_formal_statement_sha256: normalized_statement_sha256,
  mathematical_statement_sha256: statement_sha256
}))
```

Those formulas describe the Formal Conjectures record branch. Native 5.2
OpenConjecture rows instead bind the exact `body_tex` and `plain_text`, their
source JSONL record and versioned arXiv locator, a curation-ledger row, and an
`openconjecture-semantic/*` key. The 5.2 checker independently rebuilds the
4,415-row source asset to the 889-row eligible pool and the accepted 600-row
set; neither branch borrows the other's hash formula.

Native 5.3 mathlib rows bind `formal_statement` and
`mathematical_statement`, the source locator, selection and provenance payload,
the proof-evidence payload, and a `mathlib-theorem-semantic/<formal-type-hash>`
key. The 5.3 checker independently rebuilds the 1,500 source dispositions,
literal-theorem/lemma split, semantic duplicates, 500-row accepted set, and all
accepted-set digests rather than borrowing generator output.

Native 5.4 rows use the same payload boundaries but bind the residual 5.4
curation authority and the `selected_remaining_module_root_round_robin`
selection phase. Mutating `theorem_selection` without updating the enclosing
source payload, or mutating any nested closed object, fails the independent
checker and mutation suite.

This context wrapper is essential. A short payload such as `A n` does not
deduplicate declarations in unrelated modules or namespaces. Exact duplicate
credit is rejected conservatively by contextual statement, source-qualified
name, and declaration keys. Within the same context, an identical solved and
open occurrence resolves to one current solved claim; the open occurrence
remains a noncredit source/status-history row. Name equality never merges hard
homonyms.

Coverage dispositions retain both `source_statement_sha256` and the contextual
`normalized_statement_sha256`; recomputing the latter from the candidate's
module, namespace, and source hash is mandatory. A candidate that resolves to
an ATV/S5 pair already present in the parent or current registry is recorded as
`already_allocated_noncredit`. It keeps those existing target IDs for
traceability, allocates nothing new, has `grants_quota=false`, and cannot be
used again toward either release minimum.

## IDs and migration

`ATV-*` remains the canonical claim-variant identity. `S5-CLM-*` is an
immutable Stage5 public number with the same ordinal, but the explicit mapping
is authoritative:

```text
ATV-00000393 <-> S5-CLM-00000393
```

All 3,484 Stage4 ATVs receive that historical Stage5 mapping. New Stage5 ATVs
begin at 3,485 and receive no S4 number. Release 5.1 preserves the exact 5.0
allocation prefix and appends a new suffix. Release 5.2 preserves the exact 5.1
prefix and allocates `ATV-00005985..ATV-00006584` together with matching S5
IDs. Release 5.3 preserves that prefix and allocates
`ATV-00006585..ATV-00007084` with matching S5 IDs for the 500 mathlib records.
Release 5.4 allocates `ATO/ATS/ATV/S5-CLM` ordinals `00007085..00007584`
and new-family `ATF` ordinals `00006855..00007354` for its 500 accepted rows.
Release 5.5 allocates `ATO/ATS/ATV/S5-CLM` ordinals
`00007585..00008009` and `ATF` ordinals `00007355..00007779` for its 425
strict-conjecture records. Release 5.6 allocates `ATO/ATS/ATV/S5-CLM`
ordinals `00008010..00009009` and `ATF` ordinals
`00007780..00008779` for its 1,000 formal-proposition records.
ATO and ATS remain append-only but need not share the ATV ordinal; ATF
increments only for a new family.

All 3,262 `THM-*` aliases remain immutable historical pointers, all 76 folded
occurrences remain visible, and the inherited eight redirects plus four splits
remain content-bound. Current resolution is separate from historical binding:
a split has multiple terminal children, no default child, and no automatic
evidence, status, proof, or benchmark inheritance.

## MSC, frontier, importance, and rights

Formal Conjectures branch rows have a source-supplied or explicit machine
crosswalk to an MSC2020 class. The native 5.2 OpenConjecture additions preserve
arXiv subject metadata but have `msc_status=unassigned`; no MSC code is invented
for them. `Coverage_Ledger.json` retains explicit source-relative coverage and
scarcity values. There is no per-class quota: a zero, thin, or unassigned branch
is reported rather than filled with a synthetic classification. Completion
therefore means coverage relative to the pinned sources, not complete coverage
of all mathematics.

The 500 native 5.3 records have two distinct MSC evidence paths: 179 exact
`1000_plus_curated` source classifications and 321 transparent mathlib
module-root crosswalks. The latter are machine classifications, not source
annotations.

The native 5.4 records retain the same explicit source-annotation versus
machine-crosswalk distinction. At release 5.4, `Coverage_Ledger.json` had
5,898 disposition rows plus 63 MSC rows, and the strict ledger had 1,000
credits plus one correction. Current release 5.6 has 7,884 disposition rows
plus 63 MSC rows (`row_count=7,947`) and 1,425 strict credits plus one
correction (`row_count=1,426`). Composite manifest row counts must not be
reported as credit counts.

Unreviewed bulk importance is `unranked_research_level`; a source category is
only a signal. Landmark/major/core/specialized/niche tiers require explicit
review evidence. Frontier and current status may be recorded as
“Formal Conjectures category asserted at the pinned commit,” not as an
independent literature survey. Likewise, the native 5.2 frontier class is
`source_model_asserted_open_frontier`, not an independent current-status audit.

Rights are also per asset class. Formal Conjectures declares Apache-2.0 for
software/Lean files, CC-BY-4.0 for project-authored other materials,
CC-BY-SA-4.0 for Wikipedia/MathOverflow/OEIS material, and source-specific
terms for other third-party content. Accepted rows preserve those terms and
may visibly say `source_terms_preserved_not_independently_cleared`; catalog
presence does not imply independent clearance, relicensing, or benchmark
eligibility. A record whose declaration/docstring cannot be retained under the
source terms stays a noncredit coverage disposition rather than entering the
claim catalog.

The native 5.2 rows are separately restricted to per-record CC-BY-4.0 sources
and preserve paper title, authors, versioned arXiv ID, and license attribution.
Catalog publication does not relicense those source texts.

Native 5.3 formal code and docstrings retain mathlib's Apache-2.0 terms and
attribution to the mathlib Community; optional 1000-theorems metadata uses its
recorded terms. Catalog publication again does not relicense the source.
Release 5.4 inherits this exact source rights policy without rewriting the
source row. Release 5.6 applies the same per-asset terms to its expanded
mathlib source and explicitly preserves all nonselected and quarantined rows
outside the released catalog.

## Independent acceptance

The historical and current replay commands are:

```bash
python3 Docs/tools/generate_math_catalog_v5.py --check
python3 scripts/check_math_catalog_v5.py
python3 -m unittest scripts.test_math_catalog_v5
python3 Docs/tools/build_openconjecture_curation_v5_2.py --check
python3 Docs/tools/generate_math_catalog_v5_2.py --check
python3 scripts/check_math_catalog_v5_2.py
python3 scripts/test_math_catalog_v5_2.py
python3 Docs/tools/render_math_catalog_v5.py --release 5.2 --check
python3 Docs/tools/build_mathlib_theorem_curation_v5_3.py --check
python3 Docs/tools/generate_math_catalog_v5_3.py --check
python3 scripts/check_math_catalog_v5_3.py
python3 scripts/test_math_catalog_v5_3.py
python3 Docs/tools/render_math_catalog_v5.py --release 5.3 --check
python3 Docs/catalog/v5/tools/build_mathlib_theorem_curation_v5_4.py --check
python3 Docs/catalog/v5/tools/generate_math_catalog_v5_4.py --check
python3 Docs/catalog/v5/tools/check_math_catalog_v5_4.py --prepublish
python3 -m unittest Docs.catalog.v5.tests.test_math_catalog_v5_4
python3 Docs/tools/render_math_catalog_v5.py --release 5.4 --check
python3 Docs/catalog/v5/tools/generate_math_catalog_v5_4.py --publish-current
python3 Docs/catalog/v5/tools/check_math_catalog_v5_4.py
python3 Docs/catalog/v5/tools/check_math_catalog_v5_6.py --published
python3 -m unittest Docs.catalog.v5.tests.test_math_catalog_v5_6
python3 Docs/catalog/v5/tools/render_math_catalog_v5_6.py --check
```

The independent checkers must not import the generators or extractors. The
5.0/5.1 checker recomputes source slices, hashes, exact ID sets, minima, dedupe
keys, projections, migration conservation, MSC scarcity rows, release roots,
and the 5.1 parent chain. The 5.2 checker additionally rebuilds the full 4,415
OpenConjecture records to the 889 eligible candidates and accepted 600, checks
cross-source semantic uniqueness, the 5.1 prefix, rights, the Moving Sofa
credit correction, the exact 1,000-row strict ledger, and the nine-file release
root. The 5.3 checker reconstructs all 1,500 mathlib source dispositions, the
1,235/265 literal theorem/lemma split, four semantic duplicates, the 500-row
curated theorem set, compiled-proof bindings, append-only 5.2 prefix, inherited
strict ledger, and the then-current 5.3 root. A green source extraction or a generated
Markdown list alone is not a release receipt.

The 5.4 checker additionally reconstructs the exact 731-row residual pool,
three identity gates, bytewise module-root round-robin, 500 deeply closed claim
records and payload hashes, coverage supersession/effective state, combined
manifest row counts, source-policy extension, readable bytes, and both the
prepublish 5.3 pointer and postpublish 5.4 pointer. Publication is two-phase:
all staged JSON and detailed readable gates pass while Current remains 5.3;
only then does `--publish-current` take the exclusive writer lock, recheck the
complete authenticated parent CAS state, and atomically promote the pointer.

The 5.5 checker independently reconstructs the 425-row strict-conjecture
append, its multi-source curation authorities, the 1,000 important-landmark
set, the disjoint 582-row additional-frontier set, and the exact 5.4 prefix.
The 5.6 checker independently replays the 2,566-row full mathlib source, the
1,561-row qualified denominator, all 1,092 ready/469 quarantine dispositions,
the exact 1,000-row allocation, the three formal-identity gates, the complete
5.5 prefix, all nine release files, readable membership, receipt, and published
current pointer. Its published checker, readable checker, and 13-test mutation
suite pass on the final integrated workspace.

The current deterministic readable surfaces are:

- `readable/5.6/Theorem_List.md` — 3,500 theorem-status rows;
- `readable/5.6/Open_Claim_List.md` — all 2,025 broad open claims; and
- `readable/5.6/Strict_Conjecture_List.md` — exactly the 1,425 effective strict
  conjecture credits joined from the strict ledger.

The 5.2 readable directory remains an immutable-baseline projection at
1,500/1,600/1,000 and is still reproducible with `--release 5.2 --check`.

## Further diversification candidates

Mathlib is authoritative for the 500 accepted 5.3 rows, 500 accepted 5.4
rows, and 1,000 accepted 5.6 formal-proposition rows at the pinned commit. The
closed 5.6 denominator leaves 92 ready rows terminally unselected and 469 rows
in semantic-review quarantine; they grant no catalog or quota credit. Putnam
problems, formal variants, closure candidates, and relation edges likewise
grant zero 5.6 credit. Metamath,
PlanetMath, and similar sources may later diversify or cross-check coverage but
currently grant zero Stage5 quota. Admission requires a separate immutable pin,
exact source and rights contract, collision review, and a new release decision.
