# Stage5 Mathematics Expansion Release Review (historical release 5.3)

> Review date: 2026-08-10  
> Historical reviewed release: 5.3, including immutable releases 5.2, 5.1 and 5.0  
> Disposition: accepted as a source-relative mathematics inventory release  
> Superseding current-status authority: [Stage5 5.6 and Stage6 6.0 final release review](./Stage5_5_6_Stage6_6_0_Final_Release_Review_2026-08-10.md)  
> Reading rule: every use of “current” below is relative to this 5.3 review
> snapshot, not to the repository's current 5.6 pointer.  
> Non-claim: this review does not assert completeness of mathematics, universal
> importance ranking, a proof upgrade for inherited rows, or an independent
> current-status literature survey for every open claim.

## Outcome

Release 5.3 is materialized, not planned. Its manifest binds nine files (eight
non-manifest artifacts) under release root
`9ec5a097c0286b6751b02e89d18c400aab655021ba1ad4843eadba5a69fc41fa`.
It preserves the exact 5.2 catalog and open-claim prefixes, inherits the exact
1,000-member strict-conjecture set, and appends 500 literal mathlib theorem
records with pinned, sorry-free kernel evidence. The deterministic readable
surfaces reproduce all three accepted JSON member sets.

No P0 or P1 release finding remained after the command matrix below. Acceptance
is limited to the exact pinned sources, schemas, curation authorities, record
sets, rights, and evidence levels named here.

One reproducibility caveat remains outside the sealed release package.  The
contract's displayed source-extractor `--check` command omits the
`--thousand-plus-root` argument used to enrich the frozen source artifact from
the separately pinned 1000-plus checkout at commit
`8e04b97dd24adc6e931be78a884da7e935bc8780`.  On this machine that checkout is
not present, so the default command correctly rebuilds the same 1,500 selected
declarations and all selection counts but omits optional upstream titles,
Wikipedia links, and 1000-plus MSC annotations; its bytes therefore differ.
This command-line reproducibility gap does not change the sealed source bytes,
the accepted 500-member set, any release artifact, or the release root.  The
fixed source asset is instead independently authenticated and replayed by the
curation builder, generator, and independent checker.  A from-scratch extractor
replay requires an exact local checkout of that auxiliary commit and an
explicit `--thousand-plus-root /path/to/checkout`.

## Immutable chain

| Release | Parent | Release root SHA-256 |
|---|---|---|
| 5.0 | none | `f6f217c78ce46166805743b9c2a9bba07734c0bc6b5ac6bad98d6a3b6b05b6dc` |
| 5.1 | 5.0 | `ba0aeacfcad136df7eff5b08932a76bf87127bb393b6d9f8ad1eef525cf55016` |
| 5.2 | 5.1 | `edee3a3e5f29a345a16fb526654aecfeaeaaf62da0e0101ed5e9bd2cbb374e2e` |
| 5.3 | 5.2 | `9ec5a097c0286b6751b02e89d18c400aab655021ba1ad4843eadba5a69fc41fa` |

The historical 5.3 manifest file SHA-256 is
`8384deebd8ff33cf06c592ed443fd3ed78a4a294c4cea106362705e95954419a`.
Its catalog and strict-ledger file SHA-256 values are respectively
`957da23fbd1e50244912fb6dbb76fbf663e7970ace3f6da8b19407929211a8bb`
and
`91106334947a4406b75f7e87b400dd9966e25fb0441b6b78eb1047b4bb5a88dc`.

## Exact mathematics accounting

| Measure | 5.2 baseline | Historical 5.3 | Acceptance meaning |
|---|---:|---:|---|
| cumulative Stage5 catalog records | 3,100 | 3,600 | exact `Claim_Catalog.json` rows |
| theorem-status records | 1,500 | 2,000 | exact theorem projection |
| native 5.3 kernel-checked literal theorems | 0 | 500 | appended mathlib rows only |
| syntactic `current_claim_kind=conjecture` records | 1,001 | 1,001 | raw kind, not the strict denominator |
| effective strict conjecture credits | 1,000 | 1,000 | exact strict-ledger credit set |
| `open_problem` records | 599 | 599 | separate kind, never strict conjectures |
| broad open-claim projection | 1,600 | 1,600 | unchanged exact 5.2 projection |

The 5.3 raw partition is `2,000 + 1,001 + 599 = 3,600`. The effective
strict set remains distinct from syntax: 401 inherited rows match the older
direct-proposition conjecture predicate, but release 5.2 revoked the Moving
Sofa strict credit at `S5-CLM-00005311` / `ATV-00005311` without changing its
record, identity, text, or mathematical status. Release 5.3 inherits exactly
`400 effective parent + 600 native 5.2 = 1,000 effective strict` conjectures and
adds no open claim.

## Theorem evidence boundary

The 5.2 theorem baseline remains 1,500 source-asserted rows. Within the pinned
Formal Conjectures categories, 1,373 are `research solved`, 127 are the weaker
`textbook` category, all 1,500 have
`formal_proof_state=source_asserted_not_replayed`, and 1,369 imported
declarations report `sorryAx`. Release 5.3 preserves those rows byte-for-byte
and does not retroactively upgrade their proof or importance evidence.

The 500 native 5.3 additions have a separate, stronger boundary:

- every accepted source declaration is literally a theorem, not one of the 265
  source lemmas;
- every record binds `kernel_checked_sorry_free`, `uses_sorry=false`, exact
  `.olean` and `.ilean` hashes, and mathlib commit
  `8a178386ffc0f5fef0b77738bb5449d50efeea95`;
- `batch_axiom_dependency_union` is explicitly a batch union rather than an
  exact per-declaration dependency set; and
- later mathlib commits and universal importance are not inferred.

Thus the repository may accurately report 2,000 theorem-status records, of
which 500 have the native 5.3 pinned kernel evidence. It may not describe all
2,000 as independently human-reviewed landmark theorems or all 2,000 as
repository-replayed placeholder-free proofs.

## 5.3 mathlib source and curation

| Input | Binding |
|---|---|
| mathlib commit | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| 1,500-row source asset SHA-256 | `236b9f6ac192eaf87215663bfd7fadb80c439b452049cef1747ea804c458637a` |
| 1,500-disposition / 500-accepted curation authority | `9661eebbd25bbb8aee3a0c7ae1c9cbe671ec77324f889d25e967811ffd9f7d5d` |
| curation file SHA-256 | `379e165ae52ffd911e383fdb351fc602d36ec585e40bade54612c1512a7a1905` |

The independent reconstruction observes 1,500 source rows, 1,235 literal
theorems, 265 literal lemmas, four source-semantic duplicate theorem rows,
1,231 unique eligible theorems, and a selected `180 + 320 = 500`. The accepted
set contains 180 records with a mathlib 1000-theorems signal and 378 with a
module Main-result signal; 58 carry both. Selection preserves 22 module-root
branches. These are pinned source-documentation signals rather than an
independent universal ranking.

The new records also preserve exact formal types, source ranges and hashes,
Apache-2.0 code/docstring terms, mathlib Community attribution, semantic keys,
and append-only IDs `S5-CLM-00006585..S5-CLM-00007084` with matching ATV IDs.
MSC evidence stays split between 179 source-curated exact codes and 321
transparent module-root crosswalks.

## Inherited 5.2 conjecture boundary

Release 5.3 changes none of the 5.2 open records or strict credits. The native
5.2 source bindings remain:

| Input | Binding |
|---|---|
| GitHub commit | `d2e3afe62098611fabd7236998acc73f64e4b3b7` |
| Hugging Face commit | `fa03d85db95e6edad4ff751b490704fa8a0d9358` |
| full 4,415-row JSONL SHA-256 | `8cf0a7ce4baff47769fe1ca0c40b11eed0767480c858c208a7beae8f5829dd14` |
| 889-row eligible-pool SHA-256 | `8a698e3af53ca0605a2a8ecd2e3a9944ad84157440a86f3c319effaf9792c6ce` |
| 600-row curation authority | `ac78c277984e1ed7e9223323dcf6b3d0a65fc3cc82edad16cda7a0020e8b4bb5` |

Those 600 rows were curated for claim shape, atomicity, interest signal,
rights, and semantic duplication. Their `open` status remains a pinned
OpenConjecture dataset/model assertion with
`independent_current_status_review=false`; neither 5.2 nor 5.3 claims an
independent current-literature status survey for every statement.

## Reproducible historical command matrix

The following release commands were run on the integrated tree and passed:

```text
python3 Docs/tools/build_mathlib_theorem_curation_v5_3.py --check
PASS ... source_rows=1500 accepted=500
         authority_sha256=9661eebbd25bbb8aee3a0c7ae1c9cbe671ec77324f889d25e967811ffd9f7d5d

python3 Docs/tools/generate_math_catalog_v5_3.py --check
PASS ... release=5.3
         root=9ec5a097c0286b6751b02e89d18c400aab655021ba1ad4843eadba5a69fc41fa

python3 scripts/check_math_catalog_v5_3.py
PASS check_math_catalog_v5_3
NOTE source=1500; literal-theorem=1235; literal-lemma=265;
     unique-theorem=1231; selected=180+320=500
NOTE catalog=3600; theorem=2000; open=1600; open-problem=599; strict=1000+1
NOTE release_root=9ec5a097c0286b6751b02e89d18c400aab655021ba1ad4843eadba5a69fc41fa

python3 scripts/test_math_catalog_v5_3.py
Ran 11 tests in 168.046s
OK

python3 Docs/tools/render_math_catalog_v5.py --release 5.3 --check
PASS ... root=9ec5a097c0286b6751b02e89d18c400aab655021ba1ad4843eadba5a69fc41fa
```

The elapsed test time is observational rather than an acceptance constant.
The required facts are the zero exit status, 11 passing tests, reconstructed
counts, and content-bound outputs. The 5.2 renderer check was also rerun and
passed at its unchanged release root.  The source-extractor command printed in
the contract is deliberately excluded from this passing matrix for the
auxiliary-checkout reason recorded above; no extractor PASS is claimed here.

## Tool and readable-surface receipts

| Path | SHA-256 | Rows represented |
|---|---|---:|
| `Docs/tools/build_mathlib_theorem_curation_v5_3.py` | `04f9ed7e78113ad1957a603066f1bfebb6d433cf16e833cbc076a080cca6ac28` | 1,500 dispositions / 500 accepted |
| `Docs/tools/generate_math_catalog_v5_3.py` | `8bdc8f0e845b7e56c5d6870fbb734d2f5d75063b21bbb6c79afd5421e3cefbaa` | generator |
| `scripts/check_math_catalog_v5_3.py` | `e71325605d566aa43542862f7ec2f9badb057423019ba8e3542f7f72088cfd92` | independent checker |
| `scripts/test_math_catalog_v5_3.py` | `69813a84ede5b40aa4d21864c5116dd0629a68513071712ef397166d3d5e1a8e` | 11 tests |
| `Docs/tools/render_math_catalog_v5.py` | `6736ba1e0f781b91b47212f6748047f89d2432cbeffd4107650256bae2141ac8` | renderer |
| `readable/5.3/Theorem_List.md` | `65b25e7ad16f7ab2fe1cc0f73061889d7755911ede5e588e5b80c5cf81e985f7` | 2,000 |
| `readable/5.3/Open_Claim_List.md` | `83d637e4cedb42dc612f58786add4082b6837ddebf6404ade31b989d0d043777` | 1,600 |
| `readable/5.3/Strict_Conjecture_List.md` | `148dcec350f11f714ee36e564aabc6647780a92519b302ad03347c165581de50` | 1,000 |

Readable Markdown is non-normative: JSON release authorities define
membership, while byte-for-byte renderer replay guards the human-facing copies
against manual drift. The 5.2 readable directory remains available as the
1,500/1,600/1,000 baseline rather than being overwritten by 5.3.

## Final boundary

At this historical review point, release 5.3 met the concrete inventory target at 2,000
theorem-status records and 1,000 effective strict conjectures while preserving
599 separately typed open problems. It is a real append-only source-relative
release, not a future plan. It remains neither a census of all mathematical
knowledge nor a finished formal proof library: the inherited 1,500 theorem
rows retain their weaker evidence, the 500 new rows are pinned to one mathlib
environment, and the conjecture status boundary remains source/model asserted.
