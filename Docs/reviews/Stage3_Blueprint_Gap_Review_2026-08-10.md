# Stage3 Blueprint Gap Review and Acceptance Mapping

> Review date: `2026-08-10`
>
> Baseline commit: `9c299dbabd34878a420db46ca66d687886fe2b04`
>
> Baseline tree: `807a1067658136803eb33b5f679e6a45d40942b5`
>
> Purpose: synthesize the requested second-pass reviews into executable Stage3 gates. This report is
> read-only audit evidence, not a truth certificate, benchmark release, worker attestation or task
> cursor.

## Executive finding

`Docs/Stage2_Blueprint.md` version `stage2-catalog-integrity/1.0` is a useful schema and identity
bootstrap, but it cannot meet the user's full-list requirement. Its domain work is explicitly sample
repair, its current catalog has zero qualified human overlays, its historical Gantt is schedule-only, its Status
surface and controller are absent, and its M0387 tasks compress distinct mathematics, Lean,
provenance, validation, receipt and benchmark gates into eight broad rows.

Stage3 therefore treats Stage2 as historical evidence and creates a new sole authority. It separates:

```text
source occurrence conservation
  -> identity and scope adjudication
  -> complete domain curation
  -> theorem and open-claim list projections
  -> optional eligible benchmark records
  -> versioned tasks, split, scorer and release
```

No arrow grants truth, proof or redistribution credit automatically.

## Review groups

The three source reports used by this synthesis are content-bound as follows:

| Source report | SHA-256 |
|---|---|
| `Docs/reviews/THM-M-0387_Critical_Audit_2026-08-10.md` | `f692b6ef27af1a026c258d84c80d521fbdafe40b7064c2472087820be4b1728b` |
| `Docs/reviews/THM_List_Benchmark_Audit_2026-08-10.md` | `5dead797a9fa60e9c9cb7e09bf4fdcf74d01dc8ae15d4d34f5a8df7ca35b8200` |
| `Docs/reviews/THM_Catalog_and_ID_Audit_2026-08-10.md` | `40fcfde2afb706582e8f877b9e75ff0fec9b4328574d3601ecb83c299d3c8631` |

Task paths below are collaboration labels reported by the review run. The repository does not contain
their thread registries, prompts or signed result receipts, so the labels prove traceable division of
scope and synthesized findings, not independently replayable subagent identity or attestation.

### M0387 acceptance group — exactly six review tasks

| Review task | Independent scope | Principal finding converted into Stage3 gates |
|---|---|---|
| `/root/m38_accept_math` | human mathematics and pinned-source theorem order | WTW symbol mixing, incomplete residual cases, two-adic gaps, n3 order, n4 signed squares and regular-prime residue/induction require typed source contracts and six post-repair reviews |
| `/root/m38_accept_lean` | canonical Lean identity, declarations and upstream terminals | Statement and Proof duplicate the target; 29 node probes cover only 23 distinct wrappers and omit nine local declarations; wrapper and terminal provenance need separate semantic probes |
| `/root/m38_accept_evidence` | denominator, crosswalk, readable and receipt evidence | retained and Stage1 machine/human denominators disagree; 132/132 is circular/file-level; evidence refs and ledgers are generic; receipt chain and logs are not durable |
| `/root/m38_accept_validator` | current positive authority and failure semantics | Stage1 local checker is superseded, recipes are not executed, intake can report failure with exit zero, and final validation must invoke the current authority with adversarial fixtures |
| `/root/m38_accept_bench` | M0387 task ABI, contamination and scorer | the family is public-proof-exposed, held-out count is zero, retrieval and proof synthesis must be separate, root challenge cannot enter an aggregate, and rights/scorers/fixtures are missing |
| `/root/m38_accept_release` | ownership, dependencies and terminal acceptance | shared `proof_units.json` ownership blocks concurrency, final warm/cold replay occurs too early, and release must join every repair and review rather than just a manifest |

These reviews are inputs. New Stage3 rows `S3-M38-060..065` require six distinct content-addressed
post-repair receipts before `S3-M38-066` can be Master accepted.

The source report names the scopes rather than task labels. The exact crosswalk used here is:

| Reported task label | Source-report scope |
|---|---|
| `/root/m38_accept_math` | mathematical fact checking |
| `/root/m38_accept_lean` | Lean semantic checking |
| `/root/m38_accept_evidence` | cross-file consistency and evidence denominators |
| `/root/m38_accept_validator` | local reproducibility and failure semantics |
| `/root/m38_accept_bench` | benchmark comparison |
| `/root/m38_accept_release` | adversarial release/dependency review |

### Scientific benchmark and list group — primary six-task audit

| Review task | Independent scope | Principal finding converted into Stage3 gates |
|---|---|---|
| `/root/bench_math` | mathematics and PutnamBench/miniF2F/ProofNet comparison | exact quantifiers, assumptions, atomicity, open status and duplicate identity require full curation rather than sample repair |
| `/root/bench_physics` | physics, SciBench/TheoremQA and scientific-claim boundaries | law/model/effect/observation routes require regime, units, observable, uncertainty and task-specific oracle contracts |
| `/root/bench_cs` | all CS occurrences and formal/executable CS task shapes | 400 source occurrences versus 398 aliases expose two folded rows; all model/encoding/resource/adversary fields are placeholders; exact semantic negative fixtures are required |
| `/root/bench_schema` | global records, tasks, split, visibility, scorers and release | source problem, claim, formal variant and task must be separate; reference pins, family graph, asset rights, metrics, contamination and offline release replay are independent gates |
| `/root/bench_status` | status and evidence axes | human truth, empirical support, external formal proof, repository integration and provenance cannot collapse into one verified flag |
| `/root/bench_sampling` | deterministic stratified sampling and extrapolation limits | duplicates, aliases, granularity, difficulty, era and category coverage require frozen denominators and forbid sample-to-universe extrapolation |

The later `/root/bench_list_math`, `/root/bench_list_physics`, `/root/bench_cs` and
`/root/bench_schema` tasks supplied full-denominator implementation detail. Two earlier nested M0387
audits supplied additional shell, split, scientific-task and coverage observations. Those six inputs
are supplemental second-pass material: the two reused nested tasks are not newly launched scientific
reviewers, and this report does not relabel them as another independent six-person audit.

### Catalog, conjecture and ID group — exactly six review tasks

| Review task | Independent scope |
|---|---|
| `/root/catalog_math_kind` | theorem, lemma, conjecture, axiom, definition, equation, algorithm, proof-event and thesis triage |
| `/root/catalog_physics_kind` | law, model, equation, effect, observation, device, framework, open problem, regime and sense |
| `/root/catalog_cs_kind` | theorem, algorithm, protocol, definition, game, framework, thesis and computation/adversary/fault model |
| `/root/catalog_open_status` | historical, open, refuted, partial, independent and conditional scope with dated sources |
| `/root/catalog_id_registry` | occurrence/family/sense/variant, append-only allocation, alias, split, merge, redirect and receipt migration |
| `/root/catalog_cross_domain` | taxonomy imbalance, hard homonyms, duplicates, granularity, coverage gaps and catalog/task separation |

## Reproducible current-state facts

The generated v2 catalog reports:

| Fact | Current value |
|---|---:|
| ATO | 3,338 |
| ATF | 3,119 |
| ATS | 3,338 |
| ATV | 3,338 |
| all schema records | 13,133 |
| legacy aliases | 3,262 |
| exact duplicate clusters / folded occurrences | 74 / 76 |
| qualified human overlays | 0 |

For all 3,338 ATV, `exact_statement.completeness=source_prose`, human truth is unknown, provenance is
missing, atomicity is unknown and benchmark status is not evaluated. Lexical triage labels 62
conjectures and 14 hypotheses; no member has thereby obtained an accepted exact statement or dated
status. The bounded coverage inventory has 62 missing seeds — mathematics 24, physics 18, CS 20 —
and expressly disclaims completeness and automatic ID allocation.

Domain identity counts are:

| Domain | ATO | provisional domain ATF tags | ATS/ATV | legacy aliases | folded occurrences |
|---|---:|---:|---:|---:|---:|
| mathematics | 1,666 | 1,556 | 1,666 | 1,601 | 65 |
| physics | 1,272 | 1,232 | 1,272 | 1,263 | 9 |
| computer science | 400 | 397 | 400 | 398 | 2 |

ATF tags can include cross-domain membership, so their domain-tag total is not the global family
denominator.

## M0387 acceptance gaps

### Human mathematics

- W04 still mixes FLT exponent `pF` with semistable-modularity residual characteristic `r in {3,5}`
  and consumes the wrong W03.5 edge.
- The two-adic normalization lacks a fully auditable integral model, invariant and conductor table.
- The residual split omits the `E[3]` and `E[5]` both reducible branch; irreducibility citations and
  exceptional-prime range are not frozen.
- n3 prose does not follow the pinned `Solution' -> Solution`, PID/UFD, square and formula order.
- n4 prose uses natural coprimality for integers and overstates signed-square witnesses.
- regular Case II uses the wrong residue map and a fictitious minimal witness; the actual map is
  `eta -> ((x+y*eta)/(zeta-1)) mod pIdeal`, includes zero, and closure uses `Nat.le_induction`.
- all 132 `proof_units.json` dependencies are empty, so the claimed theorem DAG is prose rather than
  structured dependency evidence.

### Lean and evidence

- the Stage1 Statement imports only `Init` and copies the FLT proposition; Proof defines another
  target rather than sharing one imported canonical declaration;
- 29 node probes collapse to 23 wrapper names and omit nine current local declarations;
- upstream terminal source, exact type, axiom set, proof body and actual wrapper dependency are not
  independently verified;
- retained dossier denominators are machine 93, human 113, readable 132 while the Stage1 registry is
  machine 121, human 121, readable 132, with no common snapshot and reviewed delta;
- readable targets point to six whole files without anchors, many do not contain the target ID or
  statement, and hundreds of steps are template text;
- current receipt self-hash and input hashes presently recompute, but its predecessor is absent,
  stdout/stderr are temporary, Stage1 recipes were not run, and no independent schema/generator/verifier
  exists.

Stage3 rows `S3-M38-001..034` and `060..066` directly cover these gaps. The required terminal state is:

```text
dossier_acceptance = accepted
root_machine_closed = false
theorem_complete = false
root_open_challenge.aggregate_eligible = false
benchmark_readiness = per-track
```

## External benchmark boundaries

Stage3 freezes immutable pins and independently derives counts rather than quoting mutable `main`:

- PutnamBench teaches separation of source problem, language variant, factored answer and proof task.
- miniF2F teaches frozen version/split and non-public test proof policy.
- ProofNet teaches separate formal proving and autoformalization; Lean 3 and Lean 4 artifacts require a
  reviewed crosswalk.
- LeanDojo teaches family/novel-premise leakage control and budget-bound retrieval/proof metrics.
- Lean Workbook is synthetic training material, not automatic held-out gold.
- TheoremQA is theorem-application QA, not a canonical theorem list.
- SciBench is numerical textbook QA; its universal relative tolerance and unused unit argument are a
  baseline limitation, not a scorer to copy.

Repository or tool licenses do not automatically license textbook statements, explanations, images,
data, answers or hidden tests. Unknown rights keep a record catalog-visible but out of a release pack.

## Stage3 mapping

### M0387 finding-family mapping

| Audit finding family | Stage3 gates |
|---|---|
| P0-1 exponent/residual-characteristic mixing | `S3-M38-002`, `005..007`, `061` |
| P0-2 two-adic normalization and conductor | `S3-M38-003`, `007`, `060` |
| P0-3 incomplete 3--5 residual split | `S3-M38-005..007`, `061` |
| P0-4 regular Case-II map and induction | `S3-M38-010`, `018`, `064` |
| P0-5 historical replay cannot prove current state | `S3-M38-022..023`, `031..034`, `065` |
| P0-6 Stage1 recipe/exit semantics | `S3-M38-020..023`, `031..032`, `065` |
| P0-7 missing benchmark ABI and scorer | `S3-M38-024..030`, `S3-BEN-009..015` |
| Lean identity, wrappers and upstream provenance | `S3-M38-012`, `015..017`, `019` |
| n=3, n=4 and regular-prime P1 mathematics | `S3-M38-008..010`, `018`, `062..064` |
| WTW primary-theorem, level and modern-history P1/P2 | `S3-M38-004..007`, `011`, `018`, `060..061` |
| denominator, readable-anchor, template and metric P1/P2 | `S3-M38-013..019`, `065..066` |
| final independence, warm/cold and truthful root status | `S3-M38-029..034`, `060..066`, `S3-ENV-008` |

### Scientific-list and benchmark finding-family mapping

| Audit finding family | Stage3 gates |
|---|---|
| P0-1 ordinal ID drift and destructive dedupe | `S3-CAT-001`, `003..005`, `008..010`, `S3-MATH-008`, `S3-PHY-008`, `S3-CS-016` |
| P0-2 collapsed truth/formal/repo status | `S3-CAT-002`, `006..007`, `S3-MATH-005`, `010..016`, `S3-PHY-002..003`, `009..015`, `S3-CS-002`, `017..023` |
| P0-3 non-propositions and compound claims | `S3-CAT-002`, `S3-MATH-005`, `008`, `010..016`, `S3-PHY-002..003`, `007`, `009..015`, `S3-CS-002`, `004..014`, `017..023` |
| P0-4 no task/split/scorer authority | `S3-BEN-002`, `006..015` |
| P0-5 rights, provenance and release pins | `S3-BEN-001`, `008`, `014..015` |
| mathematics exactness/open-status sample defects | `S3-MATH-001..020`, especially `005..019` |
| physics model/regime/unit/uncertainty defects | `S3-PHY-001..019`, especially `002..017` |
| CS model/resource/adversary/fault defects | `S3-CS-001..025`, especially `002..024` |
| deterministic sampling and extrapolation limits | `S3-CAT-001`, `008`, `S3-MATH-001..002`, `006..009`, `019..020`, `S3-PHY-001`, `006..008`, `017..019`, `S3-CS-001`, `003..016`, `024..025` |
| task/visibility/family/scorer/metric contract | `S3-BEN-002`, `007`, `009..015` |

### Catalog, conjecture and ID finding-family mapping

| Audit finding family | Stage3 gates |
|---|---|
| occurrence conservation and legacy reversibility | `S3-CAT-001`, `003`, `009`, `011..013` |
| mathematics/physics/CS kind and truth-aptness | `S3-CAT-002`, `S3-MATH-005`, `009..016`, `S3-PHY-002..003`, `007`, `009..015`, `S3-CS-002`, `004..014`, `017..023` |
| historical/open/refuted/independent/conditional status | `S3-CAT-007`, `S3-MATH-017`, `S3-PHY-013`, `016`, `S3-CS-020`, `022`, `S3-CAT-012..013` |
| occurrence/family/sense/variant and stable allocation | `S3-CAT-003..005`, `008..010`, `S3-MATH-008`, `S3-PHY-008`, `S3-CS-016` |
| split/merge/redirect and receipt migration | `S3-CAT-003`, `009..010`, `S3-M38-012`, `022..024`, `031..034` |
| cross-domain homonyms, duplicates and leakage | `S3-CAT-004..005`, `009..010`, `S3-BEN-006..010` |
| 62 bounded missing candidates and taxonomy scope | `S3-CAT-001`, `008`, `S3-MATH-002..008`, `019..020`, `S3-PHY-001`, `005..008`, `017..019`, `S3-CS-001`, `003`, `014..016`, `024..025` |
| theorem/conjecture/hypothesis/open projections | `S3-MATH-017`, `S3-PHY-016`, `S3-CS-020`, `022`, `S3-CAT-011..013` |
| catalog records must not become benchmark tasks automatically | `S3-BEN-001..015` with rights, eligibility, split, scorer and replay gates |

| User objective | Terminal evidence in the new authority |
|---|---|
| install the required Lean 4 environment | `S3-ENV-001..008`, final M0387 warm/cold receipts and environment acceptance |
| six-way M0387 critique becomes complete acceptance | `S3-M38-001..034`, six separate `060..065` receipts and `066` Master review acceptance |
| six-way peer-benchmark critique and full THM lists | full `S3-MATH`, `S3-PHY`, `S3-CS` lanes, then global `S3-CAT-011..013` |
| theorem/conjecture/hypothesis lists and stable numbering | append-only `S3-CAT-003/009`, generated `S3-CAT-012`, domain open-list projections and mutation tests |
| current execution skill, optimized structure and same-name Gantt | `S3-EXE-001..015`, generated Gantt/Status/Kanban and `S3-REL-001..005` |

The three domain lanes use disjoint outputs and full denominators. Shared registries and public
projections have one downstream integrator. This prevents the Stage2 pattern in which independent
workers simultaneously owned `proof_units.json` or another shared public surface.

## Safe public wording

Before Stage3 terminal acceptance the repository may say it has a lossless research catalog
bootstrap, completed review plans, an installed pinned Lean toolchain and bounded coverage candidates.
It may not say the theorem, conjecture or hypothesis lists are complete; that 3,338 records are
theorems; that any Stage0/Stage1 count is a benchmark denominator; that M0387 is unconditionally
machine-closed; or that a Gantt shows authenticated workers unless its content-bound runtime snapshot
actually proves those exact identities. The bootstrap Gantt must instead say runtime unavailable.

After terminal acceptance, list completion is still bounded to the immutable universe digests and the
benchmark release still reports only its exact released task-ID denominator.
