# Stage3 v3 Eighteen-Agent Critical Audit

> Review date: `2026-08-10`
>
> Baseline authority reviewed: `Docs/Stage3_Blueprint.md` version
> `stage3-list-completion/2.0`
>
> Nature: read-only review evidence. This file is not a checklist, truth certificate, legal
> opinion, benchmark release, worker handoff or Master acceptance receipt.

## 1. Review population and evidence boundary

The operator requested three groups of exactly six independent subagent tasks. All eighteen tasks
inspected the same current worktree and were instructed not to edit shared files.

| Group | Six task identities |
|---|---|
| THM-M-0387 | `/root/m0387_kernel`, `/root/m0387_noncircular`, `/root/m0387_identity`, `/root/m0387_math`, `/root/m0387_repro`, `/root/m0387_adversarial` |
| scientific lists and peer benchmarks | `/root/bench_math_formal`, `/root/bench_physics_science`, `/root/bench_cs_tasks`, `/root/bench_task_abi`, `/root/bench_rights_leakage`, `/root/bench_completeness` |
| theorem/open-kind and identifier catalog | `/root/catalog_math_kind`, `/root/catalog_physics_kind`, `/root/catalog_cs_kind`, `/root/catalog_open_status`, `/root/catalog_id_registry`, `/root/catalog_cross_domain` |

Task labels demonstrate the requested division of scope. They are not external-person identities or
signed attestations. Post-repair acceptance still requires durable, content-addressed receipts under
the execution Blueprint.

## 2. Reproducible current facts

- The host resolves Elan `4.2.3`, Lean `4.29.0` commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and all
  eleven materialized package revisions.
- The operator's project toolchain is also the Elan default; `lean --version`, `lake --version`,
  `python3 scripts/check_lean_environment.py`, and `lake build` pass.
- The seven-stage `THM-M-0387/run_local_validation.sh` warm run passes in the current materialized
  tree, including 132 historical nodes and 29 node probes. This remains a warm-cache observation,
  not clean-runner, cold-cache, network-denied or unconditional-FLT evidence.
- The lossless v2 bootstrap independently reproduces 3,338 source occurrences, 3,119 provisional
  families, 3,338 senses/variants, 3,262 legacy aliases and 76 folded occurrences.
- `Coverage_Candidates_v2.json` contains 98 review records, not 62: 62 missing candidates plus 36
  present-collision candidates. The v2 Blueprint froze only the former number explicitly.
- Every current v2 ATV remains human-truth unknown, provenance missing and benchmark not evaluated;
  there are zero qualified human overlays.
- The reviewed v2 authority had 168 rows: 7 Master-accepted bootstrap rows, no self-tested row and
  161 unfinished rows. A green authority/projection check proved structure, not the unfinished
  semantic gates.

## 3. Closed finding-family denominator

The following stable families are the minimum denominator that the v3 review-contract and final
release review must disposition. A later implementation may split a family into finer immutable
findings, but it may not delete, waive or silently rename one.

### 3.1 THM-M-0387

| ID | Severity | Finding and required acceptance consequence |
|---|---|---|
| `V3-M38-STATE-001` | P0 | A checkbox or self-digested runtime snapshot is not completion evidence. Every `[_]` and `[x]` transition must resolve raw result, patch, command logs, controller ledger and Master receipt bytes. |
| `V3-M38-CURRENT-002` | P0 | Final acceptance must bind and rederive the accepted repository membership Merkle, item Master-receipt index and fixed validation matrix; deleting a proof or changing a Prop after acceptance must invalidate completion. |
| `V3-M38-CIRCULAR-003` | P0 | `meta.repo_local_validation`, `build_validation.md` and `receipts/current-validation.json` are output/status surfaces and must be outside the semantic read closure. Their absence or byte variation must not change replay. |
| `V3-M38-READSET-004` | P0 | Network denial, filesystem boundary and actual reads must be enforced and independently observed over the descendant process tree; undeclared HOME/XDG/config/source reads fail. |
| `V3-M38-RESOURCE-005` | P0 | Per-stage and total monotonic deadlines, CPU, memory/swap, PID, allocated-block disk and binary-log limits require adversarial OOM, fork, flood and escaped-child tests. |
| `V3-M38-CACHE-006` | P0 | `warm_shared`, `warm_private`, `cache_restored`, `cold_compile` and `offline_bundle` are distinct. A restored or shared `.olean` cannot be labeled cold. |
| `V3-M38-IDENTITY-007` | P0 | M0133/M0387 statement equivalence, claim identity, proof-event relation and evidence applicability are separate decisions; no redirect, second credit or receipt inheritance is implicit. |
| `V3-M38-LINEAGE-008` | P0 | The dossier rev-5.6, Stage1 registry and Stage3 registry are separate snapshots. Multi-source lineage covers `born/rename/split/merge/retire` and never transfers historical M0 credit by default. |
| `V3-M38-IDSPACE-009` | P0 | Obligation, support-edge, evidence-fact, declaration/provider and recipe IDs have separate denominators joined by explicit many-to-many crosswalks; 29 nodes are not 29 declarations. |
| `V3-M38-KERNEL-010` | P0 | The axiom policy is independently frozen to the accepted set, currently `propext`, `Classical.choice`, `Quot.sound`; recording a new `native_decide`, `sorryAx` or custom axiom does not authorize it. |
| `V3-M38-CENSUS-011` | P0 | A module-universe and imported-environment census enumerates every public declaration and any zero-premise canonical-FLT root. Namespace/file movement and late declarations cannot shrink the denominator. |
| `V3-M38-CANONICAL-012` | P0 | Exact ownership must cover every current root selector and M0133 surface needed to establish one imported canonical statement; copied Props and direct upstream bypasses fail. |
| `V3-M38-MATH-013` | P0 | WTW residual-image restrictions and all three 3--5 branches require typed, premise-complete instantiation. High-risk local/global leaves require two independent mathematical checks, not one author's prose. |
| `V3-M38-RECEIPT-014` | P0 | A Stage3 receipt binds accepted ATV/catalog revision, statement asset/type, obligation snapshot, support-edge set, evidence manifest, spec, inputs and explicit genesis. Writers use immutable create, fsync and CAS pointer semantics. |
| `V3-M38-PUBLIC-015` | P0 | Every claim-bearing public file is either a current digest-bound projection or a visibly quarantined immutable historical surface; omitted `132/132` or authority prose is a failure. |
| `V3-M38-RIGHTS-016` | P0 | Unknown, denied or citation-only rights block public payload bytes. M0387 remains public-development/contaminated with held-out-family count zero. |
| `V3-M38-COLDKERNEL-017` | P1 | Cold artifacts receive independent `leanchecker` and `lean --trust=0` checks bound to source/module/olean/tool hashes. |

### 3.2 Scientific lists and benchmark ABI

| ID | Severity | Finding and required acceptance consequence |
|---|---|---|
| `V3-BEN-DENOM-001` | P0 | Conserve all 98 legacy review keys—62 missing plus 36 collision records—and every v3 audit delta key. Counts without explicit ID sets do not pass. |
| `V3-BEN-LIFECYCLE-002` | P0 | Freeze the typed lifecycle `SourceRelease -> SourceProblem -> Claim -> FormalVariant -> ProofAsset -> Task -> Family -> Split -> Attempt -> Decision -> Metric -> Run -> Release`, with cardinality and orphan rules. |
| `V3-BEN-ROLE-003` | P0 | Every external source has one role: ingested, training-only, contamination-reference, comparator-only or excluded. LeanDojo/Workbook, TheoremQA/SciBench and CS peers cannot remain name-only pins. |
| `V3-BEN-PROTOCOL-004` | P0 | Candidate I/O, allowed imports/tools/network/files, visibility, resource, retry, attempt and terminal-result semantics are one executable ABI, not free-form “candidate contract” prose. |
| `V3-BEN-SEMANTIC-005` | P0 | Autoformalization equivalence is tri-state. Only kernel certificates, a frozen decidable normalization subset or blinded content-bound human adjudication can grant semantic accuracy; typecheck alone cannot. |
| `V3-BEN-SCIENCE-006` | P0 | Scientific answer algebra covers units, affine/log scales, near-zero absolute/relative tolerance, significant figures, tensor/tuple/set/multi-answer and uncertainty. Upstream `eval`, global-tolerance and unit-ignoring scorers are negative references. |
| `V3-BEN-CS-007` | P0 | Add code I/O, special/interactive judge, SyGuS, verification+witness, Dafny, security proof/attack/equivalence, distributed safety/liveness and model-check tracks with vacuity fixtures. |
| `V3-BEN-EVIDENCE-008` | P0 | Finite tests, empirical runtime, bounded model checking and symbolic-security search never upgrade universal correctness, asymptotic complexity, unbounded protocol or security-theorem axes. |
| `V3-BEN-REPLAY-009` | P0 | A sealed candidate-output-to-decision-to-metric evaluation-run bundle must replay on two network-denied runners; rebuilding a pack or replaying only the scorer is insufficient. |
| `V3-BEN-RIGHTS-010` | P0 | Every release byte maps to an Asset BOM entry with source, content hash, asset kind, rightsholder/terms and scope. A repository license cannot automatically license embedded textbook, contest, image, data or proof assets. |
| `V3-BEN-EXPOSURE-011` | P0 | Split isolation and pre-existing public-gold/model-training exposure are separate. `training_visibility=unknown` cannot enter a clean aggregate. |
| `V3-BEN-MINIF2F-012` | P0 | Erratum: miniF2F v2 publicly exposes informal proofs for test items; refusing new formal-proof PRs is not a non-public-test-proof guarantee. ProofNet/Workbook/TheoremQA/SciBench also expose gold fields. |
| `V3-BEN-PRIVATE-013` | P0 | Public and private evaluator manifests, roots and access paths are separate; logs, layers, paths, canaries and symlinks cannot exfiltrate private bytes. |
| `V3-BEN-PHYROUTE-014` | P0 | Physics method/device/dataset/framework/definition/nonclaim entities need an exhaustive curation owner and truth-apt child graph. Why/how problem entities are not forced into propositions. |
| `V3-BEN-PHYLINEAGE-015` | P0 | Empirical claims bind release, calibration, cuts, code/container, likelihood/prior, statistic/threshold, trials, blinding and independent replication; dataset and inference identities remain separate. |

### 3.3 Catalog, theorem/open classification and identifiers

| ID | Severity | Finding and required acceptance consequence |
|---|---|---|
| `V3-CAT-ORTHO-001` | P0 | Record role, current/historical claim kind, assertion form and entity kind are orthogonal. Equation/formula/identity does not by itself decide theorem versus entity. |
| `V3-CAT-VARIANT-002` | P0 | ATV means catalog variant, not necessarily truth-apt claim. Entities/aggregates may remain nonclaim umbrellas; extracted propositions receive new append-only ATV IDs with no default child or evidence inheritance. |
| `V3-CAT-RELATION-003` | P0 | Relation vocabulary includes solves/refutes/counterexample/proves/formal-proof-artifact/conditional/corollary semantics with inverse/cardinality rules, not just same-claim and proof-event prose. |
| `V3-CAT-SEMANTIC-ID-004` | P0 | ATO continuation, ATF family, ATS sense and ATV exact semantic payload have different stability rules. Quantifier/hypothesis/conclusion changes mint a new ATV rather than preserving a drifting meaning. |
| `V3-CAT-CAS-005` | P0 | Allocation is locked, atomic, fsynced CAS with parent digest, idempotent request bytes, monotone transactions and crash/two-writer/ABA/tombstone/high-water tests. |
| `V3-CAT-LIFECYCLE-006` | P0 | Active, redirect, split and retired states are exclusive; redirects flatten, splits have no default, mixed graphs are acyclic and tombstones cannot resurrect. |
| `V3-CAT-ARTIFACT-007` | P0 | Freeze a full legacy identity-join artifact/receipt inventory and applicability-aware migration envelope, rather than an unbounded phrase “each historical receipt.” |
| `V3-CAT-POSTCURATION-008` | P0 | The pre-curation CAT fixed point is provisional. Exact domain curation must trigger a second identity/allocation/current-owner fixed point with explicit reopen/invalidation and superseded receipts. |
| `V3-CAT-OWNER-009` | P0 | Final terminal variants equal conserved baseline descendants plus accepted candidate descendants and each has exactly one domain/cross-domain owner; post-fixed-point children cannot be orphaned. |
| `V3-CAT-REPAIR-010` | P0 | All 120 mathematics, 105 physics and 398 CS v2 proposals plus focus obligations receive mapped/rejected/superseded dispositions; proposal-only is never accepted truth. |
| `V3-CAT-PHY-011` | P0 | Physics identities consume quantity/convention authority before merge and retain release/analysis history; source 210 categories and legacy-survivor 208 categories are distinct denominators. |
| `V3-CAT-CS-012` | P0 | CS kinds include theorem/lemma/result, assumption/game, algorithm/protocol/scheme, definition/framework/thesis/aggregate/nonclaim; object and correctness/resource/security children remain distinct. |
| `V3-CAT-OPEN-013` | P0 | Historical/current kind, exact scope, dated status, special cases, refutation witness, independence direction/base theory, conditional/disputed proof and resolution criterion form append-only status events. |
| `V3-CAT-TERMINAL-014` | P0 | `--require-complete` must validate a fixed executable acceptance matrix and current repository/artifact closure; all-`[x]` prose plus cleanup alone is not catalog completion. |
| `V3-CAT-STATUS-015` | P0 | Every material-status truth-apt current ATV has role-specific, exact-variant-applicable sources and exactly one current status bucket; historical names, negative solutions, refutations, partial children and disputed proof claims cannot be conflated. |
| `V3-CAT-GRAPH-016` | P0 | Semantic identity and benchmark leakage are separate typed graphs. File/container co-residence and common premises are not leakage edges; post-curation termination requires zero novel identity or leakage candidates and two identical component digests. |

## 4. Mandatory bounded candidate delta

These keys are review candidates, not accepted facts and not authorization to mint IDs. Each must
receive `existing-family`, `new-family`, `nonclaim`, `collision`, or manifest-policy exclusion with
evidence. The final candidate universe also preserves all 98 v2 records.

### Mathematics

```text
missing.math.banach_alaoglu
missing.math.fisher_neyman_factorization
missing.math.rao_blackwell
missing.math.lehmann_scheffe
missing.math.gauss_markov
missing.math.glivenko_cantelli
missing.math.fundamental_theorem_calculus
missing.math.inverse_function
missing.math.implicit_function
missing.math.group_first_isomorphism
missing.math.group_second_isomorphism
missing.math.group_third_isomorphism
missing.math.orbit_stabilizer
missing.math.group_class_equation
missing.math.inverse_galois
missing.math.fontaine_mazur
missing.math.bombieri_lang
missing.math.standard_conjectures
missing.math.hadamard_matrix
missing.math.lonely_runner
missing.math.erdos_straus
missing.math.union_closed_sets
missing.math.tate_conjecture
missing.math.bateman_horn
missing.math.lehmer_conjecture
missing.math.hadwiger_nelson
```

Named regression rows include THM-M-0323/0324, LLN/CLT assumption families, Euler conjecture versus
counterexample, Dinitz/Galvin, theorem versus proof event/formal artifact, Optional Stopping aliasing,
and the two unrelated Marcus--Spielman--Srivastava claims.

### Physics

```text
missing.physics.hubble_tension
missing.physics.muon_g_minus_2_status_family
missing.physics.neutrino_mass_ordering
missing.physics.proton_radius_discrepancy
missing.physics.gwtc_observation_family
missing.physics.loophole_free_bell_tests
missing.physics.eht_data_product_family
missing.physics.kallen_lehmann
missing.physics.wigner_symmetry
missing.physics.buckingham_pi
missing.physics.black_hole_rigidity
missing.physics.topological_censorship
missing.physics.kohn_theorem
missing.physics.friedel_sum_rule
missing.physics.levinson_theorem
missing.physics.kibble_zurek
```

Named regression families include Euler-equation, Feynman-rules, dispersion, area-law and convention
homonyms; Zeno/anti-Zeno; cosmic censorship; CMB/NANOGrav; Hubble inference; and quark-mass scheme.

### Computer science

```text
missing.cs.sygus_cegis
missing.cs.hoare_relative_completeness
missing.cs.abstract_interpretation_soundness
missing.cs.compiler_refinement
missing.cs.concurrent_memory_models
missing.cs.communication_complexity
missing.cs.streaming_algorithms
missing.cs.sublinear_property_testing
missing.cs.parameterized_complexity
missing.cs.average_case_complexity
missing.cs.online_learning
missing.cs.relational_expressiveness
missing.cs.serializability
missing.cs.concurrency_control
```

Named regressions include Rice, NTIME hierarchy, LFKN, MAX-3SAT, OWF converse, Fiat--Shamir,
compiler correctness, FLP/Paxos, HHL, channel coding, Hamming/Huffman/BWT and the two folded CS ATOs.

Cross-domain graph fixtures additionally include Wedderburn--Artin scope variants,
Hausdorff--Young, the two Caffarelli--Kohn--Nirenberg claims, heat maximum principles,
Nekhoroshev, Maxwell differential/integral forms and model-specific adequacy. Hard-negative fixtures
include the unrelated König, Liouville, uniqueness, CKN and PCP homonyms. These remain review
candidates and do not receive canonical IDs merely by appearing here.

## 5. Required Blueprint changes

The v3 authority must at minimum:

1. add a content-bound `AUD-005` for this review and the miniF2F/SciBench errata;
2. strengthen state transition and terminal currentness gates with raw controller/Master evidence;
3. add owner-approved publication/rights policy without inventing a repository license;
4. add an independent clean-runner and cold-kernel boundary while retaining honest warm evidence;
5. add legacy-artifact/review-inventory conservation and a post-curation identity/current-owner fixed
   point;
6. close physics entity/empirical routing and migrate every domain's v2 proposals;
7. add external-source role, executable candidate ABI, semantic/scientific/CS scorer governance and
   sealed evaluation replay;
8. repair M0387 canonical ownership, axiom policy, module/root census, wrapper/import topology,
   read/resource boundary, rights, receipt identity and independent cold-artifact recheck;
9. freeze the exact v3 stable-ID manifest, generated-validation crosswalk and fixed terminal command
   matrix; and
10. regenerate the same-name Gantt with every ID exactly once and no invented schedule.

## 6. Truthful public boundary

Before the new checklist is executed, the safe statements are:

```text
lean_environment_local_warm = passed
m0387_root_machine_closed = false
m0387_theorem_complete = false
catalog_v2_lossless_bootstrap = true
catalog_v3_manifest_relative_completion = false
benchmark_release_ready = false
rights_closure = incomplete
clean_heldout_claim = forbidden
```

No green structural checker, warm build, high row count, public split name or reviewer label upgrades
any stronger claim.
