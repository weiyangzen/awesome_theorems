# THM-M-0134 statement recheck: blocked

Item: `S56-M-0134-STATEMENT`

Base revision: `798df79b58ea707894a696cd94845d01463df457` (tree
`b346b6fb1026442115a07b3ef939ee5e97577a36`). Rechecked on 2026-07-16
(`Asia/Shanghai`) in worker slot 56.

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

There is also a pre-existing metadata mismatch: the target manifest classifies this item as
"geometry/algebraic geometry," while the catalog gloss and dossier place it in symmetric-group
representation theory. It is recorded for possible master metadata reconciliation, but it supplies
no proposition or source authority and is not the first failed statement gate.

The prior source check remains unresolved: Burnside's 1897 first edition explicitly excludes groups
of linear transformations, Young's 1900 paper was available only as bibliographic metadata, and no
pinpoint statement from Burnside's 1911 second edition was admitted. A fresh bounded Crossref check
also confirmed metadata for Young's 1901 second paper, but no primary passage from it was admitted.
The searches returned no item identified as a "Burnside-Young theorem" or exact primary statement.
This negative result is not exhaustive and is not evidence for selecting any candidate.

HEAD integrates the prior slot-56 recheck, but the fixed target inputs are otherwise unchanged from
its base. Repository source records, intake scope, statement infrastructure, legacy Lean discovery
module, target manifest, toolchain, and dependency lock are unchanged. Canonically extracted
`THM-M-0134` projections from the current rev-5.6 blueprint and execution DAG also compare equal.
Whole-file blueprint and DAG hashes changed only because unrelated target states were integrated.

Consequently there is no truthful canonical Lean expression, canonical minimal-import set,
elaborated-expression hash, canonical-target environment fingerprint, checked alternate transport,
or meaningful removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutation
suite. The first failed gate remains
`exact_source_statement_identity_and_theorem_variant_selection`. Lifecycle remains `planned`, root
debt remains `H4 / M4 / R4`, and the statement node remains `[ ]`. No proof, node receipt, debt
change, audit completion, theorem completion, or master acceptance is claimed.

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
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0134` | 0 | rank 50; planned; legacy slot `S1-M-050`; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided `.lake` symlink; base revision and tree match this record |
| scoped standard, source, intake, legacy-module, and integrated-blocker inspection | 0 | source identity and proposition remain unresolved; the prior recheck remains substantively correct |
| `git diff e6872c198..HEAD` over fixed target inputs, plus canonical blueprint/DAG projection comparison | 0 | fixed inputs are unchanged except integration of the prior recheck; target blueprint/DAG projections compare equal |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0134/StatementInfrastructure.lean` | 0 | four candidate infrastructure types elaborated; no canonical target or proof body was declared |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean AwesomeTheorems/Stage1/S1_M_050.lean` | 0 | legacy discovery infrastructure elaborated; no exact-target credit applies |
| from `Formalizations/Lean`: `lake env lean --version`; `lake --version` | 0 | Lean and Lake versions match the pinned environment above |
| mathlib and `flt-regular` package status plus revision/tree checks | 0 | both dependency worktrees were clean at the pinned revisions and trees above |
| bounded exact-topic `rg` over pinned mathlib and `flt-regular` | 1, expected no match | zero output; no Burnside-Young/Specht/standard-tableau/tabloid target hit; this is not an anchor audit |
| declaration-position prohibited-construct scan over owned and legacy Lean | 1, expected no match | no proof escape, bodyless declaration, unsafe declaration, or backend bypass occurrence |
| bounded Crossref searches for Burnside/Young theorem and representation combinations | 0 | metadata for Young's 1900 and 1901 papers was confirmed, but no result uniquely identified the target or supplied an exact primary statement |
| `python3 -m json.tool` plus scoped blocker/hash assertions | 0 | structured evidence parsed; identity, base/tree, blocked/null-target state, input hashes, current dependency state, and absent-self-test invariants passed |
| no-index whitespace checks for both new files; `git diff --check -- Stage1_Instances/THM-M-0134` | expected new-file exits 1; scoped exit 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | worker self-test intentionally absent because the positive statement gate failed |

## Retry Condition And Boundary

Retry after the intake is master-accepted and accountable reviewers preserve and approve one exact
primary or approved-authoritative theorem passage with stable edition/theorem/page locators,
incorporated definitions, full assumptions and conclusion, proof boundary, corrections, errata
disposition, and independent review. That selection must fix the coefficient field and
characteristic, range of `n`, symmetric-group and representation models, equivalence relation,
construction, ordered binders, typeclass context, and degenerate cases. A fresh worker can then
encode only that approved claim, minimize imports, fingerprint the elaborated expression and
environment, compile every credited transport, and execute all four mutation classes.

This is fresh current-HEAD target-scoped blocker evidence only. Because the positive statement
deliverable did not pass, `.stage1-worker-selftest.json` is intentionally absent and no worker `[_]`
or master acceptance is requested.
