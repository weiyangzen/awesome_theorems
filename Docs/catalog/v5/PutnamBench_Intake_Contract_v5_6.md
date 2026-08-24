# PutnamBench 5.6 intake and one-hop closure contract

Status: implementation contract.  It does not itself grant theorem,
conjecture, relation, or release credit.

## Frozen parent and benchmark

- Parent release: `5.5`.
- Parent release root:
  `fea893e7b5d0b3b958c64ac672f9164efd06996e086c08385462527dcb75dbb0`.
- Parent catalog: 4,525 records, including 2,500 theorems and 2,025 open
  claims.  Release 5.5 added no theorem identities.
- PutnamBench repository: `https://github.com/trishullab/PutnamBench`.
- Commit: `dfb0a47a1c1ec3a10f2a9acfdf41a2043920f33c`.
- Tree: `609c8623a81281f5442c0c4dc7e82dc015e97ed9`.
- Frozen archive SHA-256:
  `843911c7eb432c0ce96ac1e6494f9675336a9be935884cd5b6de4575db042c30`.
- The upstream snapshot has no tag or GitHub release identity.  The commit,
  tree, archive bytes, and component paths are therefore the release identity.

The independently derived denominators are separate and must never be
collapsed into one count:

| universe | count |
|---|---:|
| informal problem keys | 673 |
| Lean 4 formalization files | 672 |
| Isabelle formalization files | 640 |
| Coq formalization files | 412 |
| formalization files in total | 1,724 |
| distinct keys represented by a formalization file | 674 |
| distinct keys in the union of informal and formal components | 675 |
| full 1962--2025 Putnam coordinate grid (`64 * 12`) | 768 |
| full-grid keys outside the PutnamBench component union | 93 |

Known component-presence anomalies are part of the denominator:

- `putnam_1997_a1` is informal-only;
- `putnam_1987_a3` and `putnam_1996_a1` are formal-only.

Declaration-name mismatches and malformed declarations are retained as formal
variant dispositions.  They are not silently renamed, dropped, or counted as
additional theorems.

The 675-key PutnamBench union is a benchmark subset, not the final Putnam seed
denominator.  The full source universe is independently based on:

- PutnamGAP repository `https://github.com/YurenHao0426/PutnamGAP`, commit
  `aee05407afc7e621e8d9c7f909f4f25ccb8131c0`, tree
  `0f55aee4f4b911e767785a7c5977fbe36f58dbbe`, whose
  complete 1938--2024 source denominator contains 1,051 original
  problem-plus-solution rows and whose 1962--2024 grid contribution is 756
  coordinates;
- the Kedlaya Putnam archive for all twelve 2025 coordinates, bound both to
  the canonical `https://kskedlaya.org/putnam-archive/2025{s}.tex` origin and
  to immutable mirror commit
  `bd9408c626737480f9b76ab7e287dad6980154c8`, tree
  `42343fd26c12ffb37597c917ed5374bbc03b276b`.

The PutnamGAP tree, archive bytes, license bytes, all 1,051 row keys, and every
mapped or out-of-scope disposition must be pinned; a count-only selection of
756 rows is insufficient.  The Kedlaya revision, retrieved bytes, all twelve
2025 locators, and row hashes must likewise be pinned before qualification.
Pinning does not authorize redistribution: raw archives containing original
questions or solution prose remain external unless a separate grant is pinned.
The repository stores prose-free row/locator/hash manifests and, where the
component license permits, exact formal declaration headers with third-party
docstrings removed.  A full-source audit accepts the external archive only as
an operator-supplied, SHA-verified input and never copies it into the release.

A coordinate alone is not a proposition: every full-grid row needs a frozen
statement and solution locator/hash, an independently reviewed restatement,
proof/status evidence, and a component-specific rights finding.
The full-seed manifest proves exactly:

```text
768 full seeds = 675 PutnamBench-union seeds + 93 supplemental seeds
```

Neither side may substitute a count-preserving different key set.

## Required artifacts

The source-freezing lane owns:

- `curation/putnambench_v5_6/PutnamBench_Source_Inventory_v5_6.json`;
- `curation/putnambench_v5_6/PutnamBench_Source_Problems_v5_6.jsonl`;
- `curation/putnambench_v5_6/PutnamBench_Formal_Variants_v5_6.jsonl`.

The full-grid PutnamGAP/Kedlaya source lane owns:

- `curation/putnambench_v5_6/Full_Putnam_Source_Inventory_v5_6.json`;
- `curation/putnambench_v5_6/Full_Putnam_Source_Candidates_v5_6.jsonl`;
- `curation/putnambench_v5_6/Full_Putnam_Seed_Problems_v5_6.jsonl`.

Its prose-free replay support manifests are:

- `curation/putnambench_v5_6/PutnamGAP_Source_Locator_Manifest_v5_6.jsonl`;
- `curation/putnambench_v5_6/Kedlaya_2025_Source_Locator_Manifest_v5_6.jsonl`.

The deterministic producer and repository-only checker are the same
fail-closed program,
`tools/freeze_full_putnam_source_v5_6.py`; an independently written mutation
suite is `tests/test_freeze_full_putnam_source_v5_6.py`.  Repository-only
checking must accept authority
`08fb966f533d6ab0f29b08f02ef55de77752f20471bcec3c65915a518df7df84`.
Full replay additionally requires operator-supplied archives and must be
byte-identical to all five derived artifacts.  The frozen PutnamGAP archive is
15,945,135 bytes with SHA-256
`ebf565f54083e6e54cbcd74ec9998211328c2d0491df02281876695da737b506`;
the immutable 2025 mirror archive is 7,836,269 bytes with SHA-256
`795f53b60d7e6ae4a6ef1c1e2ec998ceefb817d585199752b75bbc09ac59bc0d`.

The candidate ledger retains all 1,051 PutnamGAP rows plus all twelve frozen
Kedlaya 2025 rows, each with an in-grid mapping, duplicate/variant mapping, or
explicit out-of-scope disposition.  The seed ledger has exactly 768 rows:
756 PutnamGAP-backed coordinates and twelve Kedlaya-backed 2025 coordinates.
It also binds the exact 675-key PutnamBench subset and exact 93-key complement.

PutnamGAP candidate IDs are
`putnamgap/aee05407afc7e621e8d9c7f909f4f25ccb8131c0/<native-index>`;
the native `index` value is retained rather than replaced by a sort ordinal.
Kedlaya IDs use `kedlaya/<immutable-revision>/2025-<section>-<number>`.
`source_statement_sha256` and `source_solution_sha256` are SHA-256 of the exact
decoded field value's UTF-8 bytes, excluding JSON quotes and escape syntax.
The source-file hash, Git blob where applicable, source row index, JSON pointer,
raw-row hash, and canonical-row hash are separate bindings.

The semantic-review lane owns:

- `curation/putnambench_v5_6/seed-crosswalk.jsonl`;
- `curation/putnambench_v5_6/formal-variant-crosswalk.jsonl`.

The one-hop-relation lane owns:

- `curation/putnambench_v5_6/relation-source-universe.json`;
- `curation/putnambench_v5_6/relation-candidate-ledger.jsonl`;
- `curation/putnambench_v5_6/closure-node-ledger.jsonl`;
- `curation/putnambench_v5_6/relation-edge-ledger.jsonl`.

The qualification builder produces, and an independently implemented checker
reconstructs:

- `curation/putnambench_v5_6/PutnamBench_Intake_Qualification_v5_6.json`;
- `curation/putnambench_v5_6/coverage-receipt.json`;
- `curation/putnambench_v5_6/relation-closure-receipt.json`.

The eventual 5.6 release generator consumes only the qualified artifacts.  It
must not consume reviewer scratch files, mutable URLs, topic tags, or count-only
claims.

## Source and rights boundaries

Every source row binds the frozen archive, member path, member SHA-256, Git
blob OID, byte span, and exact span SHA-256.  A declaration name by itself is
not a statement binding.

Rights are component-specific:

- Lean 4 formal code: Apache-2.0 from `lean4/LICENSE`;
- Isabelle formal code: Apache-2.0 from `isabelle/LICENSE`;
- Coq formal code: MIT from `coq/LICENSE`;
- informal problem wording: the upstream README says it is available with MAA
  permission, but the repository contains no license granting downstream
  relicensing.  The code licenses do not flow into the informal text.
- PutnamGAP variants/annotations: CC-BY-4.0 only to the extent actually granted
  by its pinned README/LICENSE;
- underlying original Putnam questions and canonical solutions in PutnamGAP:
  MAA/four-volume-book copyright and fair-use provenance, not automatically
  CC-BY-4.0 and not relicensed by this catalog;
- Kedlaya 2025 question/solution material: source-specific copyright terms must
  be recorded; a public URL alone is not a redistribution license.

Consequently, the frozen inventories may retain source locators and hashes,
but the catalog release must use independently written reviewed statements,
proof summaries, and relation summaries unless a separate redistribution
grant is pinned.  It must not copy PutnamGAP's original question or canonical
solution text under the annotation license.  Exact PutnamBench formal code may
be retained under its component license with attribution.  The catalog never
relicenses upstream material.

In particular, the PutnamBench full archive is not a repository artifact: it
contains all informal statements and informal-solution strings, while the
upstream README's MAA-permission assertion covers statements only and is not a
downstream license for solutions.  Repository-only checking replays the
prose-free manifests and licensed formal-header asset; an optional external
source audit may replay the pinned full archive without redistributing it.

PutnamBench proof holes (`sorry` or `Admitted`) are statement assets, not proof
evidence.  A source problem may receive theorem status only when its exact
reviewed proposition is joined to a separately pinned human proof/official
solution citation or to a replayed proof artifact.  The record must keep these
axes separate:

- human mathematical status;
- external formal-statement availability;
- external formal-proof state;
- repository proof replay state.

A copyrighted official solution may be represented by citation, page/span
hash, and an independently written proof-method summary.  Its text is not
redistributed unless the applicable right is pinned.

## Noncatalog benchmark seeds and formal-variant crosswalk

There is exactly one `seed-crosswalk.jsonl` row for every one of the 768 full
Putnam grid keys.  Its only publishable disposition is
`reviewed_noncatalog_benchmark_seed`.  Every row retains one exact proposition
or an exhaustive list of independently reusable propositions for a genuinely
multipart problem.  Each has an independently written reviewed statement,
qualifying proof evidence, rights findings, and a semantic key so that formal
variants and graph edges have proposition-level endpoints.  Every target's
`identity_action` is
`noncatalog_benchmark_seed`; `stage_claim_id`, `variant_id`, parent-record
binding, and allocation request are all null.

Thus neither a coordinate, a problem/source row, nor even the reviewed seed
proposition receives catalog theorem credit.  The 768 reviewed seed rows and
all of their exhaustive multipart targets are benchmark graph roots only.
Seed rows remain distinct by coordinate and may not alias another coordinate;
multipart targets remain explicitly factored rather than being collapsed or
counted as theorem inventory.  Fuzzy title, tag, MSC, token, embedding, or
declaration-name matches do not establish their exact semantic or proof
bindings.

There is exactly one `formal-variant-crosswalk.jsonl` row for each of the 1,724
formalization-file rows.  Its final disposition is one of:

- `same_exact_claim_variant`;
- `stronger_variant`;
- `weaker_variant`;
- `different_claim_variant`;
- `wrong_problem_duplicate`;
- `malformed_or_nonclaim_variant`.

Every non-malformed variant names the exact reviewed benchmark-seed semantic
key.  A Lean/Isabelle/Coq representation is a representation of that graph
root, not a theorem identity or credit.  File-name and declaration-name
disagreement is explicitly reviewed; the file stem is never silently treated
as the semantic target.

The coverage receipt must therefore close both equations independently:

```text
768 = reviewed_noncatalog_benchmark_seed
675 = PutnamBench-subset reviewed_noncatalog_benchmark_seed
1724 = same + stronger + weaker + different + wrong_duplicate + malformed
```

It also reports the exact number of distinct reviewed benchmark propositions,
which is at least 768 because exhaustive multipart targets remain separate,
and zero seed theorem catalog credits.  The 1,724 formal rows likewise
contribute zero.

## Bounded one-hop relation closure

"Complete" means complete relative to the exact frozen relation-source and
candidate-universe manifests.  It never means that all mathematical
literature has been searched.

The relation-source universe pins every included official solution,
bibliographic source, formal dependency asset, encyclopedia revision, or
paper.  For each seed/source pair it records the deterministic discovery rule
and the complete candidate-occurrence key set.  Every candidate occurrence has
exactly one final row in `relation-candidate-ledger.jsonl`; zero missing,
duplicate, pending, blocked, or unreviewed rows is a publication gate.

Accepted relation types are:

- `direct_prerequisite`;
- `standard_solution_uses`;
- `generalization`;
- `specialization`;
- `equivalence`;
- `dual`;
- `analogy`;
- `corollary`;
- `strengthening`;
- `weakening`;
- `direct_open_generalization`;
- `partial_progress`.

The qualified 768-seed closure contains at least one accepted proposition-level
edge of every listed type.  A type-level zero may remain in a research audit,
but it does not satisfy the user's requested 5.6 closure surface and therefore
cannot pass the qualification gate.

It also contains at least one accepted proposition-level edge for every one of
the 768 seed coordinates.  The independent checker reconstructs the set from
`relation-edge-ledger.jsonl[*].seed_problem_key` and requires exactly:

```text
accepted_edge_seed_coverage = 768
missing_accepted_edge_seed_keys = 0
```

Having reviewed obligations whose candidates were all rejected is auditable,
but it does not satisfy the requested closure for that seed.  A shared topic,
tag, import, method label, or person cannot be used to fill the missing edge;
normally a seed is connected through an exact theorem used in its standard
solution or an exact direct prerequisite, with proof-step evidence.

Every accepted edge binds two exact truth-apt endpoint statements and exact
evidence for the asserted relation.  A proof-use edge additionally binds the
proof step or exact formal declaration reference showing the use.  An
explicitly derived relation records the reviewed mathematical derivation and
its assumptions.

The following evidence is never sufficient for an accepted edge:

- shared Putnam tag, MSC class, keyword, title token, or named object;
- co-occurrence in a page, bibliography, search result, or model response;
- a Lean/Isabelle/Coq import alone;
- a dependency on a definition, tactic, notation, or implementation helper;
- "related work" wording without a proposition-level relation;
- a topic, method name, person, field, or historical event as an endpoint.

Those occurrences remain visible with a rejected reason such as
`topic_only`, `import_only`, `nonclaim_method`, `cooccurrence_only`, or
`relation_not_established`.

Every closure node has distance zero (one of the reviewed noncatalog
benchmark-seed propositions, including factored multipart targets) or distance
one (an independently reviewed neighbor).  Every distance-zero node has
`catalog_action` equal to
`noncatalog_benchmark_seed` and contributes zero credit.  Every distance-one
node is incident to at least one accepted seed edge.  An edge between two
distance-one nodes cannot admit a new node or satisfy a seed obligation.  No
recursive expansion from a distance-one node is part of this release.

Distance-one closure nodes are partitioned without overlap into:

- proved theorem identities;
- strict conjecture identities;
- other current open claims (`hypothesis` or `open_problem`);
- rejected nonclaims, which receive no catalog identity or count.

The theorem and open ledgers are append-only and separately counted.  A direct
open generalization or partial-progress record is never inserted into the
theorem projection merely because it is adjacent to a proved seed.  Proof,
importance, frontier, and open-status evidence never transfer across an edge.

## 5.6 release and publication gates

The release generator must:

1. authenticate every 5.5 parent artifact and preserve every parent array as
   an exact prefix;
2. append only qualified distance-one closure theorem and open identities,
   allocating dense
   `ATF`/`ATS`/`ATV`/`ATO`/`S5-CLM` identifiers from the authenticated 5.5
   high-watermarks;
3. add explicit coverage rows for all 768 full-grid seed keys, the exact
   675-key PutnamBench subset, all 1,724 formal variants,
   every frozen relation candidate, every accepted edge, and every closure
   node;
4. derive `Theorem_List.json` and `Open_Claim_List.json` only as predicates over
   `Claim_Catalog.json`;
5. preserve the 5.5 strict-conjecture ledger as a prefix and add closure open
   claims only through the same strict status, rights, exact-statement, and
   global semantic-deduplication gates;
6. report parent count, 768 noncatalog seed propositions, zero seed theorem
   credits, new closure theorem identities, independently qualified
   Mathlib-reserve theorem identities, new strict conjectures, other open
   claims, existing-identity joins, formal variants, accepted relation edges,
   and all rejection classes separately;
7. require zero unsupported theorem credit, zero unsupported strict credit,
   zero uncovered full-grid seed, zero uncovered PutnamBench-subset seed, zero
   uncovered formal variant, zero unreviewed relation
   candidate, zero seed without an accepted proposition-level one-hop edge,
   zero orphan closure node, and zero topic-only accepted edge;
8. materialize an immutable `releases/5.6` directory before publication;
9. pass an independently implemented checker which reconstructs the source
   denominators, identity graph, relation closure, release files, and receipts;
10. under the existing writer lock, compare-and-swap `Current_Release.json`
    only from the exact authenticated 5.5 pointer to the exact independently
    accepted 5.6 pointer.  `--write` never publishes, and an idempotent 5.6
    replay must be byte-identical.

Stage6 final renumbering must consume the published 5.6 root.  A Stage6 result
built from the 5.5 counts is a pre-5.6 fixture, not the final migration.

### Independent Mathlib-reserve release partition

The Putnam qualification receipts grant credit only to independently reviewed
distance-one closure identities; benchmark seeds, formal variants, and edges
receive zero.  Release 5.6 may also consume an independently qualified,
kernel-checked Mathlib reserve, but it must expose that partition as
`new_mathlib_verified_reserve_theorems`; it may not fold the reserve into
`new_closure_theorem_identities` or a generic `new_nodes` count.

The release transaction must globally deduplicate reserve semantics against
the authenticated 5.5 parent, every reviewed Putnam seed proposition, and
every Putnam closure identity before allocating IDs.  A Lean source command spelled
`lemma` is a theorem candidate when the pinned environment reports
`ConstantInfo.thmInfo` and the pinned `collectAxioms` replay excludes
`sorryAx`; syntax spelling alone neither grants nor denies theorem credit.
Candidate-only or quarantined reserve rows contribute zero until the separate
reserve acceptance checker and final joint transaction grant them.  The
stable selection operand is
`curation/mathlib_reserve_v5_6/Mathlib_Release_Selection_v5_6.json`, schema
`awesome-theorems/mathlib-release-selection/5.6`.  Its current 1,000 selected
rows, 92 terminal-ready unselected rows, and 469 preserved-quarantine rows all
still carry zero release credit and no allocated IDs; selection is not
publication.  Consequently the release count interface is:

```text
new_theorems =
    new_putnam_closure_theorems
  + new_mathlib_verified_reserve_theorems

new_catalog_records = new_theorems + new_strict_conjectures + new_other_open_claims
```

Any Putnam qualification field named `expected_release_counts` must either
bind the independently accepted reserve count and receipt authority or state
the above formula with an unresolved reserve operand.  It must not publish a
numeric theorem total computed from Putnam closure nodes alone.
