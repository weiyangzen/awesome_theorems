# THM-M-0134 statement recheck: blocked

Item: `S56-M-0134-STATEMENT`

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff` (tree
`24acf86e69ab2e6fca9480c6269b6429874ba295`). Rechecked on 2026-07-16
(`Asia/Shanghai`) in worker slot 79.

## Decision

The exact-statement gate remains blocked. The repository supplies only the label
"Burnside-Young theorem," W. Burnside/A. Young attribution, the decade "1900s," and the topic
"representation theory of symmetric groups." It supplies no immutable primary-source edition or
theorem/page, field, range of `n`, representation and equivalence conventions, construction,
ordered binders, hypotheses, conclusion, boundary cases, corrections, or errata. The label is not
established as one stable historical theorem name. It does not distinguish classification of
irreducible representations by partitions from character classification, Young's rule, branching,
orthogonal form, hook-length results, or another theorem in the subject.

The predecessor `S56-M-0134-INTAKE` is provisional `[_]`, not master-accepted `[x]`, and records
the partition-indexing classification only as a candidate interpretation. The legacy
`AwesomeTheorems.Stage1.S1_M_050.StatementShape` makes the same local choice but is unaccepted
discovery input under the uniform L0 rework rule. Promoting either candidate to canonical status
without source admission would invent or substitute proposition-changing mathematics.

The current candidate object model has an additional exactness gap: `Rep.{0}` restricts the universe
of its carrier but does not explicitly assert `FiniteDimensional` over `Complex`. Consequently even
the candidate finite-dimensional prose is not automatically identical to the legacy expression.
This observation prevents accidental promotion; it does not select a replacement target.

Fresh exact-name and bibliographic checks found no stable scholarly item called "Burnside-Young
theorem." Burnside's 1900 group-characteristics paper, Young's 1900 and 1901 substitutional-analysis
papers, and Burnside's 1911 second edition remain unadmitted leads, not pinpoint source statements.
A bounded current Crossref query returned 100 records and zero normalized exact-title matches. Its
two titles containing both names concerned Burnside rings relative to Young subgroups and are
unrelated. Negative search evidence is not exhaustive and cannot select a proposition.

Consequently there is no truthful canonical Lean expression, canonical minimal-import set,
elaborated-expression hash, canonical-target environment fingerprint, checked alternate transport,
or meaningful removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutation suite.
The first failed gate remains `exact_source_statement_identity_and_theorem_variant_selection`.
Lifecycle remains `planned`, root debt remains `H4 / M4 / R4`, and the statement node remains `[ ]`.
No proof, node receipt, debt change, audit completion, theorem completion, or master acceptance is
claimed.

## Dependency Context

The v2 node was traversed before any proof work. It has no direct hard parents, transitive hard
ancestors, incoming hard edges, reuse hints, or shared lemma groups. The required target-owned
`dependency-reuse-ledger.json` now records that exact empty closure under schema
`stage1-dependency-reuse-ledger/1.1`, graph SHA-256
`73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`, context SHA-256
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`, ledger SHA-256
`f156002944c5d46589387676188102d7c59f743758d51cc782447c20b9807171`, and this base revision.

The repository's `validate_dependency_reuse_ledger` accepted the ledger with all five context lists,
`inspections`, `reuse_decisions`, and `unresolved_compatibility_obligations` empty. This is a complete
audit of the currently recorded v2 closure. It is not a mathematical independence claim and confers
no statement or proof credit.

## Pinned Lean Boundary

Fresh elaboration of `StatementInfrastructure.lean` emitted the four expected candidate API types,
288 bytes, at SHA-256
`0e62c11e30c2af44aa9426a92ff0bdd7d055678df70be97291612dfedf901192`; stderr was empty. Fresh
elaboration of the legacy discovery module emitted eight API lines, 520 bytes, at SHA-256
`33016b638b99ba3143f382a571a607a442062facdf3311e86cc3abdba2ba0991`; stderr was empty. These
checks prove only that the candidate object model and legacy discovery infrastructure elaborate.
They do not elaborate a source-selected target.

The replay used Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`), and `flt-regular` revision
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` (tree
`32c9eace926573a9981787ae97643e520353c893`). Both dependency worktrees were clean. The
automation-provided canonical `.lake` symlink was reused read-only. No update, build, clone, fetch,
or other dependency mutation was performed.

## Validation Record

Commands ran from this worker clone unless a working directory is stated.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, v2 theorem DAG, and skill presence passed |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 nodes, all 10822 legacy states preserved, 2 hard edges, 5 hints, 310 shared groups, acyclic |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0134` | 0 | rank 50; planned; legacy slot `S1-M-050`; legacy artifacts unaccepted; theorem incomplete |
| `python3 scripts/stage1_execution_cron.py --validate-only --workers 0` | 0 | 10822 items and 1546 targets passed the current v2/rev-5.6 structural gate |
| scoped inspection of all required authorities, the exact v2 node, complete owned dossier, source records, and legacy module | 0 | target is in scope; intake is provisional; source proposition remains unresolved; dependency closure is exactly empty |
| repository `validate_dependency_reuse_ledger` call with supplied graph/context/base bindings | 0 | schema-1.1 empty closure accepted |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0134/StatementInfrastructure.lean` | 0 | four candidate infrastructure types elaborated; no canonical target or proof body was declared |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean AwesomeTheorems/Stage1/S1_M_050.lean` | 0 | legacy discovery infrastructure elaborated; no exact-target credit applies |
| Lean/Lake version and pinned mathlib/`flt-regular` revision, tree, and status checks | 0 | toolchain matched the pinned lock and both dependency worktrees were clean |
| bounded exact-topic `rg` over pinned mathlib and `flt-regular` | 1, expected no match | zero output; this is discovery-only evidence, not an anchor audit |
| declaration-position prohibited-construct scan over owned and legacy Lean | 1, expected no match | no proof escape, bodyless declaration, unsafe declaration, or backend bypass occurrence |
| bounded Crossref exact-phrase query with normalized title analysis | 0 | 100 records; zero exact-title matches; two unrelated Burnside-ring/Young-subgroup matches |
| `python3 -m json.tool` over both JSON files plus target-scoped blocker, hash, changed-path, empty-context, and repository-ledger assertions | 0 | all structured evidence and ledger invariants passed |
| no-index whitespace checks for every new artifact; `git diff --check -- Stage1_Instances/THM-M-0134` | expected new-file exits 1; scoped exit 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | worker self-test intentionally absent because the positive statement gate failed |
| post-edit aggregate standard, v2 DAG, and execution-cron replay plus in-memory graph comparison | 1, expected worker/integration boundary | fresh generation adds both new JSON records only to this node's `evidence_inventory`; context, rank, states, edges, hints, and groups remain identical; integration regenerates and validates the v2 DAG after every blocker batch, while this worker is forbidden to edit that generated authority |

## Retry Condition And Boundary

Retry after the intake is master-accepted and accountable reviewers preserve and approve one exact
primary or approved-authoritative theorem passage with stable edition/theorem/page locators,
incorporated definitions, full assumptions and conclusion, proof boundary, corrections, errata
disposition, and independent review. That selection must fix the coefficient field and
characteristic, range of `n`, symmetric-group and representation models, finite-dimensionality,
equivalence relation, construction, ordered binders, typeclass context, and degenerate cases. A fresh
worker can then encode only that approved claim, minimize imports, fingerprint the elaborated
expression and environment, compile every credited transport, and execute all four mutation classes.

This is fresh current-HEAD target-scoped blocker evidence plus the required empty v2 dependency
ledger. Because the positive statement deliverable did not pass, `.stage1-worker-selftest.json` is
intentionally absent and no worker `[_]` or master acceptance is requested.
