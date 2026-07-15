# THM-M-0129 statement recheck: blocked

Item: `S56-M-0129-STATEMENT`

Base revision: `437cbfefc5829160dcb65d52dbe3c5458b187f3b` (tree
`849d1bfa7781d20a7428a64349372f2f43d94d2b`). Rechecked on 2026-07-15
(`Asia/Shanghai`) in worker slot 74.

## Decision

The exact-statement gate remains blocked. The integrated slot-77 recheck corrected the original
blocker after inspecting Shimura's 1973 primary Main Theorem, and fresh source review confirms its
boundary. The result on printed page 458 fixes odd `k >= 3`, level `N` divisible by four, a
character, a half-integral cusp form, positive squarefree `t`, and an explicit coefficient
Dirichlet-series definition. Under a restricted eigenfunction premise it gives an integral-weight
modular form of weight `k - 1`, character squared, and a certain level; it concludes cuspidality
only for `k >= 5`.

This does not match the provisional combined claim in `intake.json`, which says cuspidal input
yields a cuspidal lift and also requires Hecke compatibility. The page-458 Main Theorem does not
state general operator compatibility. Coefficient recurrences and the all-prime eigenform or Euler
product branch are distributed across Corollary 1.8, Theorem 1.9, and the corollary spanning pages
458-459. Selecting the Main Theorem alone would narrow the intake; silently conjoining those other
results would create a new root without an accepted source-composition crosswalk. The exact source
result, its level and character conventions, the weight-three boundary, and the intended Hecke
claim therefore remain proposition-changing choices.

No authoritative target input has resolved this conflict since the prior recheck. The target
manifest, catalog, Stage0 and legacy Stage1 records, skill, guidelines, intake dossier, legacy Lean
module, toolchain, and dependency lock are unchanged. Canonical `THM-M-0129` projections of the
target manifest, rev-5.6 blueprint, and execution DAG are byte-identical to those at the prior base
revision. The current HEAD integrates the prior recheck and its infrastructure probe, but does not
accept a canonical claim or change the target's scheduler projection.

Consequently there is no truthful canonical human statement, canonical Lean expression, target-
minimal import set, expression hash, canonical-target environment fingerprint, checked transport,
or meaningful removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutation
suite. The first failed gate remains
`exact_source_statement_identity_and_intake_reconciliation`. Lifecycle remains `planned`, root
debt remains `H1 / M3 / R3`, and the statement node remains `[ ]`. Its intake prerequisite is only
provisional `[_]`, not master-accepted `[x]`. No proof, node receipt, debt change, audit completion,
theorem completion, or master acceptance is claimed.

## Pinned Lean Boundary

Fresh elaboration of `StatementInfrastructure.lean` emitted six expected lines, 389 bytes, at
SHA-256 `8ef43829eee0a7d1a3a9b63c4ce517f7e808d08b60615dc5bef3b7be6fee2f29`;
stderr was empty. Its two direct imports expose ordinary `CuspForm`, `DirichletCharacter`, and the
character conductor, while three `#check_failure` commands confirm that plausible exact-topic
identifiers are absent. Deleting either import makes its corresponding positive checks fail. This
establishes import minimality only for the boundary probe, not for the absent canonical target.

The historical `S1_M_047.lean` module also elaborated with empty output, but its source and target
structures store theorem-critical laws and conclusions as unconstrained `Prop` fields and omit the
squarefree parameter and actual coefficient equality. Reusing that shell, inventing an opaque
predicate or parameterized source model, or proving mere nonemptiness of the zero cusp-form target
would substitute the theorem. A bounded source search found no half-integral-weight, metaplectic,
Shimura-lift, Shimura-correspondence, Kohnen, or half-integral Hecke declaration in pinned mathlib
or `flt-regular`.

The replay used Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`), and `flt-regular` revision
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` (tree
`32c9eace926573a9981787ae97643e520353c893`). Both package worktrees were clean. The
automation-provided canonical `.lake` symlink was reused read-only. No update, build, clone, fetch,
or other dependency mutation was performed.

## Validation Record

Commands ran from this worker clone unless a working directory is stated.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0129` | 0 | rank 47; planned; legacy slot `S1-M-047`; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided untracked `.lake` symlink; base revision and tree match this record |
| scoped inspection of the standard, skill, source records, dossier, integrated recheck, infrastructure, and legacy module | 0 | the source-result composition conflict and missing native interfaces remain; the prior recheck is substantively correct |
| canonical target projection comparison against `aef94f39853f9222e48f83b2358a6822aafd3c50` | 0 | target manifest, blueprint block, and DAG projection compare equal at SHA-256 `293cfbd7...`, `95245f1f...`, and `635f6c06...` |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0129/StatementInfrastructure.lean` | 0 | three native declarations and three expected missing identifiers checked; stdout 389 bytes at SHA-256 `8ef43829...`; empty stderr; no canonical target or proof body |
| import-deletion probes for `StatementInfrastructure.lean` | 1 each, expected | deleting `ModularForms.Basic` makes `CuspForm` unknown; deleting `DirichletCharacter.Basic` makes both character checks unknown |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean AwesomeTheorems/Stage1/S1_M_047.lean` | 0 | legacy discovery shell elaborated with empty output; no exact-target credit applies |
| from `Formalizations/Lean`: `lake env lean --version`; `lake --version` | 0 | Lean and Lake versions match the pinned environment above |
| mathlib and `flt-regular` status plus revision/tree checks | 0 | both dependency worktrees were clean at the pinned revisions and trees above |
| bounded exact-topic `rg` over pinned mathlib and `flt-regular` Lean sources | 1, expected no match | zero output and empty stderr; no relevant declaration was located; this is not the downstream exhaustive anchor audit |
| prohibited-construct scan over target-owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, `unsafe`, `implemented_by`, or `native_decide` occurrence |
| `python3 -m json.tool` and scoped invariant assertions over the companion recheck JSON | 0 | blocker identity, base, state/vector, null target fields, four undefined mutations, two-file scope, and self-test absence agree |
| scoped tracked and per-new-file `git diff --check` | 0 | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test is absent because the exact-statement deliverable failed |

## Retry Condition And Boundary

Retry after the intake is master-accepted and accountable reviewers lawfully preserve and
independently approve an exact primary result or explicit result composition. Reconcile and
reaccept the intake for its cuspidality, Hecke, level, character, parity, conductor, and boundary
choices. The pinned closure must also gain native half-integral source forms, theta-multiplier
action, source Hecke operators and eigenfunction predicates, and checked character and coefficient-
transform interfaces. A later worker can then encode only the approved claim, minimize imports,
fingerprint the elaborated expression and environment, compile every credited transport, and run
all four mutation classes.

This is fresh current-HEAD target-scoped blocker evidence only. Because the positive statement
deliverable did not pass, `.stage1-worker-selftest.json` is intentionally absent and no worker
`[_]` or master acceptance is requested.
