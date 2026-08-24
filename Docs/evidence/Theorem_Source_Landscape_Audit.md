# Theorem Source Landscape and Quality Audit

> Audit date: 2026-08-10
>
> Scope: mathematics theorems only
>
> Original audit snapshot: Stage5 release 5.4; current release update: 5.6
>
> Decision boundary: a theorem-status row is not automatically an important or
> frontier theorem
>
> Historical boundary: sections 1--4 preserve the evidence and proposed route
> as they stood at 5.4. They are not the current inventory statement.

## 0. Current release update: 5.6

Stage5 release 5.6 is now the authenticated current workspace release. It has
**3,500 theorem-status records**, not the 2,500 recorded by the original 5.4
snapshot. The exact current theorem accounting is:

| Denominator | Current 5.6 count | Meaning |
|---|---:|---|
| accepted theorem-status inventory | 3,500 | exact `Theorem_List.json` membership |
| kernel-checked, sorry-free mathlib formal propositions | 2,000 | 1,000 from 5.3/5.4 plus 1,000 from 5.6 |
| source-asserted, not independently replayed theorem rows | 1,500 | inherited Formal Conjectures records |
| important-landmark identities | 1,000 | accepted 5.5 quality overlay on existing theorem identities |
| additional disjoint frontier identities | 582 | accepted 5.5 quality overlay on existing theorem identities |
| unsupported importance/frontier credit | 0 | independently replayed release boundary |
| origin-5.6 theorem additions | 1,000 | 629 Lean `theorem` and 371 Lean `lemma` source declarations; all runtime `thmInfo` |
| ready but terminally unselected candidates | 92 | no catalog ID or inventory credit |
| semantic-review quarantine | 469 | no catalog ID or inventory credit |

The 1,000 important identities and 582 disjoint frontier identities are
quality denominators over already counted theorem records. They do **not** add
another 1,582 theorem records. Release 5.5 added no theorem identity; release
5.6 then appended exactly 1,000 distinct formal-proposition identities. The
catalog does not claim that those formal identities are all distinct
human-level named theorems or that the 3,500 rows form a census of mathematics.

Current release evidence and checker results are summarized in the
[final 5.6/6.0 release review](../reviews/Stage5_5_6_Stage6_6_0_Final_Release_Review_2026-08-10.md)
and the [mathematics inventory delta audit](./Math_Inventory_Delta_Audit.md).
The 5.6 release root is
`ce490ed958240ae1cabc26c3f704ad20b4103e30ad8abfd44e9c3b722fa17877`.

## 1. Historical finding at release 5.4

Release 5.4 has **2,500 independently checker-accepted theorem-status rows**.
That was a real materialized inventory, not a plan. At that audit point, the
5.4 release evidence proved neither that all 2,500 were important to human
mathematics nor that all 2,500 were frontier results.

The exact 5.4 evidence partition was:

| Cohort | Rows | What is proved | What is not proved |
|---|---:|---|---|
| Formal Conjectures, releases 5.0--5.1 | 1,500 | exact formal and natural-language source statements; source category maps 1,373 rows to `research solved` and 127 to `textbook` | independent importance ranking, replayed proof, current literature verification, frontier publication evidence |
| mathlib, releases 5.3--5.4 | 1,000 | literal theorem syntax, exact formal type, pinned kernel-checked sorry-free evidence | independent universal importance ranking or mathematical discovery/publication recency |

Across all 2,500 theorem rows at 5.4:

- 2,500 have nonempty natural-language and exact formal statements;
- 1,500 have `importance.evidence_level = unranked`;
- the other 1,000 explicitly set
  `importance.independent_universal_ranking_claimed = false`;
- no row has an independent per-record importance finding;
- no row has a catalog citation field binding the theorem to a primary proof or
  resolution paper;
- no row carries independent recent-paper/frontier evidence;
- 1,500 Formal Conjectures rows are `source_asserted_not_replayed` and 1,369 of
  the imported declarations report `sorryAx`;
- 1,000 mathlib rows are `kernel_checked_sorry_free` at commit
  `8a178386ffc0f5fef0b77738bb5449d50efeea95`.

Therefore the defensible counts are:

| Metric | Defensible 5.4 count |
|---|---:|
| accepted theorem-status inventory | 2,500 |
| rows whose 5.4 release evidence proves independent human importance | 0 |
| rows whose 5.4 release evidence proves mathematical frontier/recent-result status | 0 |
| rows whose 5.4 release evidence proves both | 0 |

The last three zeros describe the **evidence carried by this catalog**, not a
claim that none of the underlying results are in fact important or frontier.

The 5.4 independent check was replayed during the original audit:

```text
PASS independent math catalog 5.4 mode=published
root=c6f559861849d839ceda2f10bc7878687e35d6c897ea1c316ea4523bc7673813
catalog=4100 theorem=2500 open=1600 strict=1000 selected=500 remaining=231
```

## 2. Why the existing signals are insufficient

The 1,000 accepted mathlib rows have at least one source-documentation signal:

| Signal | Rows | Interpretation |
|---|---:|---|
| mathlib `docs/1000.yaml` | 180 | the formal declaration is linked to a 1000+ Theorems identity |
| module `Main result(s/theorems/statements)` documentation | 878 | the module author identifies the declaration as a main result of that module |
| both signals | 58 | overlap of the two preceding groups |

The union is exactly 1,000, but a module-main designation is not an independent
community-wide importance ranking.  Likewise, the 500 source rows selected as a
"dynamic expansion" come from files with header copyright years 2024--2026
(144/287/69 respectively).  A source-file copyright year dates the
**formalization file**, not the discovery or publication of the mathematical
theorem, and cannot establish frontier status.

The Formal Conjectures label `research solved` is a useful discovery lead, but
the release itself says it is a source category rather than a replayed proof or
independent truth review.  Its 1,500 theorem rows come from only 656 source files;
1,071 rows come from 466 Erdos-problem files, including 1,002 `research solved`
rows.  Variants from one problem file must not be mistaken for independently
important theorem identities without semantic review.

## 3. Audited source matrix

### 3.1 1000+ Theorems: importance/notability and identity anchor

Pinned source:

- repository: <https://github.com/1000-plus/1000-plus.github.io>
- commit: `8e04b97dd24adc6e931be78a884da7e935bc8780`
- tree: `c6bba9af8736f82b29ad6c947a20c245beb26263`
- commit date: `2026-07-22T16:23:18+02:00`
- license: Unlicense; pinned `LICENSE` SHA-256
  `6b0382b16279f26ff69014300541967a356a666eb0b91b422f6862f6b7dad17e`

Exact fixed-commit facts:

| Fact | Count |
|---|---:|
| `_thm/*.md` records | 1,200 |
| records with a title heading | 1,200 |
| records with an MSC classification | 1,200 |
| records with a Wikidata identifier | 1,200 |
| records with a Wikipedia-link field | 1,200 |
| records with at least one proof-assistant mapping | 228 |
| records with at least one `formalized` mapping | 227 |
| records with statement-only mappings and no formalized mapping | 1 |
| total proof-assistant mapping entries | 271 |

The README states that the list is the successor to Freek Wiedijk's 100
theorems list and admits entries from Wikipedia's List of Theorems.  This gives
a reproducible **encyclopedic named-theorem/notability signal**, not a universal
importance judgment.

This source does **not** contain the full mathematical statement for each of its
1,200 records.  It cannot alone populate a qualifying theorem catalog.

The 1,200 rows contain 1,210 Wikipedia link occurrences and 1,205 unique linked
page titles.  A MediaWiki API audit resolved 1,204 titles to revision-ID,
timestamp and SHA1 pins.  At record level, 1,198 of the 1,200 records have at
least one resolved page; two do not.  Wikipedia currently publishes its text
under CC BY-SA 4.0.  These 1,198 pages form a statement-extraction candidate
pool with a 198-row buffer over a 1,000-row target, but no page becomes accepted
until a reviewer extracts and verifies a complete theorem statement and its
conditions.

### 3.2 NaturalProofs: large, pinnable natural-statement join source

Pinned publication:

- project: Welleck et al., *NaturalProofs: Mathematical Theorem Proving in
  Natural Language*, NeurIPS 2021 Datasets and Benchmarks;
- dataset DOI: <https://doi.org/10.5281/zenodo.4902289>;
- ProofWiki JSON: 116,780,142 bytes,
  MD5 `f6d0cfcbfa91b47c9390ca654351fa46`;
- Stacks JSON: 49,740,834 bytes,
  MD5 `1cc83913a9d34d469e9e75d693d8a404`.

Exact published dataset counts (paper, Table 3):

| Domain | Theorem statements | Proofs | Definitions | Other pages |
|---|---:|---:|---:|---:|
| ProofWiki | 19,734 | 19,234 | 12,420 | 1,006 |
| Stacks Project | 12,479 | 12,479 | 1,687 | 968 |
| open Real Analysis textbook | 298 | 235 | 86 | 0 |
| open Number Theory textbook | 68 | 64 | 37 | 0 |
| total | 32,579 | 32,012 | 14,230 | 1,974 |

The common JSON schema provides title, mixed natural-language/LaTeX contents,
categories or source structure, references, and proofs when available.  It is a
strong statement and reference source, but it does not rank importance and is
not current frontier evidence.

Rights remain per-file rather than being inferred from the MIT license on the
software repository:

| Dataset file | Declared terms in the pinned Zenodo `LICENSE` |
|---|---|
| `naturalproofs_proofwiki.json` | CC BY-SA 4.0 |
| `naturalproofs_stacks.json` | GNU FDL 1.2 |
| `naturalproofs_trench.json` | CC BY-NC-SA 4.0; exclude from an unrestricted redistribution route |
| `naturalproofs_stein.py` | MIT; it is a download/formatting script rather than a bulk statement asset |

NaturalProofs is therefore suitable for an identity-reviewed statement join
against 1000+ titles, but its 32,579 rows grant **zero importance or frontier
credit by themselves**.

### 3.3 mathlib: proof/status authority and limited importance signals

Pinned source and rights:

- repository commit: `8a178386ffc0f5fef0b77738bb5449d50efeea95`;
- source and documentation: Apache-2.0;
- optional 1000+ metadata: Unlicense at the commit above.

Exact extractor/source-asset facts:

| Fact | Count |
|---|---:|
| indexed declarations | 243,505 |
| source-screened candidates with a configured signal | 2,575 |
| Lean-verified theorem candidates | 2,566 |
| pinned source-asset rows | 1,500 |
| literal theorem rows in that asset | 1,235 |
| unique literal theorem formal types in that asset | 1,231 |
| accepted in 5.3 plus 5.4 | 1,000 |
| remaining packaged, eligible, deduplicated literal theorem rows | 231 |

The remaining 231 rows are formally strong and can be appended quickly under a
quantity/proof contract.  They have only module-main source signals (155 from
Analysis and 76 from RingTheory), so the number immediately appendable under
the user's stronger **human-important plus frontier** contract is zero until
additional evidence is curated.

### 3.4 Stacks Project: deep authoritative supplement

Pinned audit checkout:

- commit: `a04446e57ec1fbc252a871afcec7752fb2807b14`;
- commit date: 2026-07-28;
- license: GNU Free Documentation License 1.2, no invariant sections or cover
  texts in the repository notice.

The exact LaTeX environment census at that commit is 214 `theorem`, 330
`proposition`, and 12,594 `lemma` environments.  Statements, proofs, stable
labels/tags and bibliography context are available.  The source is excellent
for algebra and algebraic geometry, but only 214 rows carry the deliberately
major `theorem` environment, and the source is too narrow to establish a
broad 1,000-landmark inventory by itself.

### 3.5 PlanetMath Free Encyclopedia: secondary statement pool

The official PlanetMath GitHub organization exposes 63 MSC-class repositories.
A blob-free fixed-tree census during this audit found exactly 9,477 current
`.tex` article paths.  The bytewise-sorted 63-line `repository<TAB>HEAD` pin
manifest has SHA-256
`180f2f1176d46b89f9fccfca9f7bf3a6db99c4e8b62f02881c7964a1b3f9d2d9`.
Entries carry `pmtitle`, `pmtype`, MSC classifications and LaTeX bodies; the
top-level Free Encyclopedia of Mathematics license is CC BY-SA 3.0.

This is a useful secondary join source, but the exact theorem-subtype count and
the semantic overlap with 1000+ were not completed in this audit.  Its 9,477
article count therefore grants no theorem quota credit.  The material is mostly
a 2016 encyclopedia snapshot and cannot establish current frontier status.

### 3.6 Bibliographic metadata: evidence join only

OpenAlex reported 323,998,640 work records on the audit date and publishes its
complete dataset under CC0.  It supplies dates, fields, identifiers and citation
counts, but not reliable complete theorem statements.  A sampled record also
showed that raw citation counts can contain extreme attribution errors, so no
unreviewed threshold may grant importance credit.

OpenAlex, Crossref or zbMATH Open may be used to bind a theorem to a primary
paper and corroborate date/field/citation evidence.  They remain auxiliary
evidence sources, not theorem inventories.

### 3.7 Rejected primary route: TheoremKB/arXiv extraction corpora

TheoremKB documents a reference dataset of 4,400 arXiv articles, but its own
README says that the dataset cannot be reshared for licensing reasons.  Its MIT
license covers extraction code, not the article corpus.  Generic arXiv theorem
extractions have the same paper-by-paper license problem.  They may be used
only after a per-paper open-license gate; they are not a clean bulk release
source.

### 3.8 Erdős status-drift join (post-audit progress, not release credit)

The community Erdős Problems database is now pinned at commit
`af90db960021ff3247f0374e015dae97b5125ff6` (tree
`931fc5b8a230485d49f095b59bbd30e6a0466455`) as a locally replayable
Apache-2.0 archive plus a 1,217-row normalized status snapshot.  An independent
checker replays every normalized row from the archived `problems.yaml`; mutation
tests reject resealed status, count, evidence-boundary, and archive changes.

The exact join against release 5.4 found:

| Finding | Count |
|---|---:|
| parent Erdős records joined | 1,495 |
| represented problem numbers | 571 |
| source-current-open, parent-open distinct identities | 369 |
| those already carrying strict-conjecture credit | 106 |
| uncredited `open_problem` question identities | 263 |
| mechanically addable strict-conjecture credits | 0 |
| parent `research solved` theorem rows whose upstream problem is resolved | 546 |
| distinct resolved problem/source files | 249 |
| candidate capacity with a maximum of two distinct rows per file | 379 |
| parent `research solved` rows whose upstream problem is still open | 414 |

The 414 reverse-status-drift rows are forbidden from frontier theorem credit.
The 263 open questions cannot be converted to conjectures merely by choosing an
answer polarity.  The 379 resolved rows are a review pool, not accepted frontier
theorems: each still needs a matching resolution reference, exact theorem scope,
importance finding, rights check, and semantic deduplication.

## 4. Historical route proposed after the 5.4 audit

This section records the route proposed when the quality counts were still
zero. Release 5.5 subsequently materialized and independently checked the
contract-relative 1,000-landmark and 582-additional-frontier quality
denominators. Those overlays did not create new theorem identities; release
5.6 separately supplied the 1,000-record quantity expansion described in
section 0.

### 4.1 Historical landmark/important route

1. Pin and archive all 1,200 1000+ records and its Unlicense evidence.
2. Normalize the 1,200 theorem identities using title, Wikidata ID, MSC and
   aliases.  Do not split one theorem into multiple credits merely because a
   formal library provides several formulations.
3. Join each identity to a complete statement, in this priority order:
   pinned formal-library statement; pinned NaturalProofs statement; exact
   reviewer-selected source substring from a revision-pinned Wikipedia or
   PlanetMath article.
4. Require explicit hypotheses, scope and conclusion.  Reject historical
   descriptions, proof-only passages, definitions, ambiguous theorem families,
   and incomplete consequences.
5. Treat 1000+ and Wikipedia List of Theorems as one related encyclopedic
   signal, because the former is derived from the latter.  Require one
   additional independent human evidence item per accepted row: a scholarly
   primary/reference paper, a reputable textbook/encyclopedia citation, or an
   independently curated formalization record, plus a reviewer rationale.
6. Bind material status to a proof/reference source.  A title or Wikidata type
   does not prove the theorem.
7. Perform exact, normalized and semantic deduplication against the full parent
   catalog and within the batch.  Aliases and equivalent formulations receive
   one claim credit.
8. Accept exactly the first 1,000 rows that pass all gates.  The 1,198 resolved
   pages provide a buffer, not a guarantee.  If fewer than 1,000 survive, add
   independently curated PlanetMath/Stacks identities; never lower the gate.

### 4.2 Historical additional-frontier route

Frontier must mean the mathematics, not the age of a source file.  A qualifying
frontier row should bind all of:

- a primary proof or resolution paper and exact bibliographic identifier;
- a theorem statement matching that paper or an authoritative open
  formalization;
- proof/publication year within the contract's stated rolling window;
- an independent bibliographic status check as of the review date;
- field/MSC classification;
- importance evidence, such as a named main theorem, resolution of a documented
  open problem, invited-survey/textbook treatment, or reviewed field impact;
- source-specific redistribution rights;
- semantic deduplication against the 1,000-row landmark base and all parents.

Formal Conjectures `research solved` rows and recent mathlib modules were useful
discovery leads, while open-license primary papers plus OpenAlex/zbMATH/Crossref
metadata could provide the evidence join. At the 5.4 audit point, none of those
candidate pools contained 500 independently accepted frontier rows, so the
then-defensible immediate frontier addition was zero.

### 4.3 Required record fields and release gates

Every quality-eligible theorem should carry separate, closed fields for:

- canonical identity and aliases;
- complete natural and/or formal mathematical statement;
- field/MSC;
- material proof status and status-as-of date;
- primary and secondary citations;
- importance tier, evidence items and reviewer;
- frontier class, mathematical publication date and evidence;
- provenance, fixed source locators, exact source substring/hashes and rights;
- semantic keys, duplicate decision and parent relationship.

The then-proposed next stage had to expose at least these independently
recomputed counters:

```text
accepted_theorem_status >= 2500                 # conserved parent inventory
accepted_distinct_important_landmarks >= 1000   # new strong quality denominator
accepted_additional_frontier_theorems >= 500    # dynamic, distinct additions
accepted_additional_frontier_theorems <= 1000
unsupported_importance_or_frontier_credit = 0
```

The landmark and additional-frontier sets should be distinct for quota purposes;
a theorem may carry both labels, but it must not satisfy both numeric additions.

## 5. Reproduction notes

Key local checks used in this audit:

```bash
python3 Docs/catalog/v5/tools/check_math_catalog_v5_4.py

jq -r '.records[] | select(.current_claim_kind=="theorem") |
  [.origin_release, (.importance.evidence_level // ""),
   (.importance.independent_universal_ranking_claimed // ""),
   (.frontier.evidence_level // "")] | @tsv' \
  Docs/catalog/v5/releases/5.4/Claim_Catalog.json

jq '[.records[] | select(.current_claim_kind=="theorem" and
  (.origin_release=="5.3" or .origin_release=="5.4")) |
  {signals:(.theorem_selection.importance_signals // [])}] |
  {total:length,
   docs_1000:map(select(any(.signals[]?; .kind=="mathlib_1000_theorems")))|length,
   module_main:map(select(any(.signals[]?; .kind=="mathlib_module_main_result")))|length}' \
  Docs/catalog/v5/releases/5.4/Claim_Catalog.json

git -C /path/to/1000-plus checkout 8e04b97dd24adc6e931be78a884da7e935bc8780
find /path/to/1000-plus/_thm -maxdepth 1 -type f -name '*.md' | wc -l
```

Remote counts and licenses were checked against the pinned repository files,
the Zenodo record API for record 4902289 and the cited NaturalProofs paper.  No
remote candidate count in this note is release inventory credit.
