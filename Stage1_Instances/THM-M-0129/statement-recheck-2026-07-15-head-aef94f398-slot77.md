# THM-M-0129 statement recheck: blocked

Item: `S56-M-0129-STATEMENT`

Base revision: `aef94f39853f9222e48f83b2358a6822aafd3c50` (tree
`8c42e198fdbcc36b0f5cc0f865e0961715a35c17`). Rechecked on 2026-07-15
(`Asia/Shanghai`) in worker slot 77.

## Decision

The exact-statement gate remains blocked. The earlier blocker correctly rejected the legacy Lean
shape, but its claim that no primary text was retrievable is no longer the decisive boundary. A
43-page discovery copy of Shimura's 1973 paper was recovered and printed pages 457-459 were
inspected. The official Annals metadata independently confirms the article identity, pages 440-481,
and DOI `10.2307/1970831`.

The primary text exposes a proposition-changing mismatch rather than closing the gate. Shimura's
Main Theorem on printed page 458 fixes odd `k >= 3`, positive `N` divisible by four, a character
`chi` modulo `N`, `f` in the half-integral cusp-form space, positive squarefree `t`, a derived
character `chi_t`, and coefficients `A_t` through an explicit Dirichlet-series equation. Under an
eigenfunction premise at specified prime divisors of `N`, it puts `F_t` in an integral-weight
modular-form space of weight `k - 1`, character `chi^2`, and a certain level `N_t`; it concludes
cuspidality only when `k >= 5`.

That is not the provisional combined claim in `intake.json`. The intake says that cuspidal input
yields a cuspidal lift and also requires Hecke compatibility. The page-458 Main Theorem does not
state general operator compatibility, and its cusp conclusion excludes the weight-three case.
Coefficient recurrences and the all-prime Euler-product branch instead occur in Corollary 1.8,
Theorem 1.9, and the corollary spanning pages 458-459. The theorem-family label does not decide
whether the root is the `t`-indexed Main Theorem, that all-prime corollary, a later weight-three or
operator refinement, or a reviewed conjunction. Selecting the Main Theorem alone would narrow the
intake; silently conjoining other results would invent a new root. The intake must be reconciled and
reaccepted after exact source selection.

No canonical human statement, Lean target, minimal import set, expression fingerprint, checked
transport, or mutation certificate is therefore emitted. The first failed gate is
`exact_source_statement_identity_and_intake_reconciliation`. Lifecycle remains `planned`, the root
vector remains `H1 / M3 / R3`, and the statement item remains `[ ]`. The intake prerequisite is
also only provisional `[_]`, not master-accepted `[x]`.

The discovery scan is not vendored and receives no `H0` credit. Lawful immutable preservation,
exact transcription review, definition and notation genealogy, correction and errata disposition,
result-composition ownership, and independent source review remain open.

## Pinned Lean Boundary

`StatementInfrastructure.lean` checks the native substrate that actually exists. Its two direct
imports expose ordinary `CuspForm`, `DirichletCharacter`, and character conductor data; deleting
either import makes its corresponding checks fail. The same file checks that the plausible exact-
topic identifiers `HalfIntegralWeightModularForm`, `ShimuraLift`, and `ShimuraCorrespondence` are
absent. It defines no proxy predicate, canonical target, transport, axiom, or proof body.

A bounded source search found no half-integral-weight, metaplectic, Shimura-lift, Shimura-
correspondence, Kohnen, or half-integral Hecke declaration in pinned mathlib or `flt-regular`. The
unchanged historical `S1_M_047.lean` still elaborates, but its `StatementShape` uses unconstrained
`Prop` fields for source laws and target conclusions, omits `t` and the coefficient equality, and
can receive no exact-statement credit. An extracted copy through `StatementShape` elaborated with
ordinary `ModularForms.Basic` alone, underscoring that it is an ordinary-interface shell rather
than Shimura's typed theorem.

The replay used Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, and `flt-regular`
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`. The automation-provided `.lake` symlink was reused
read-only. No update, build, clone, fetch, or other dependency mutation was performed.

## Validation Record

Commands ran from this isolated worker clone unless a working directory is stated otherwise.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0129` | 0 | rank 47; planned; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided `.lake` symlink; base revision and tree match this record |
| `curl -L --max-time 45 --silent --show-error https://annals.math.princeton.edu/1973/97-3/p03` | 0 | official metadata HTML SHA-256 `671dad90...16825e`; author, title, volume, issue, pages, and DOI confirmed; no theorem text |
| `pdfinfo /tmp/shimura1973.pdf`; `sha256sum /tmp/shimura1973.pdf` | 0 | discovery scan: 43 pages, 2379592 bytes, SHA-256 `78105f88...c64f4`; inspected only, not vendored or accepted as `H0` |
| `pdftotext -f 19 -l 21 -layout /tmp/shimura1973.pdf -` | 0 | printed pages 457-459 inspected; stream SHA-256 `1627c701...1dba8`; exact source mismatch recorded above |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0129/StatementInfrastructure.lean` | 0 | 6 stdout lines, 389 bytes, SHA-256 `8ef43829...e2f29`; empty stderr; three native declarations and three expected missing identifiers checked |
| import-deletion probes for `StatementInfrastructure.lean` | 1 each, expected | deleting `ModularForms.Basic` makes `CuspForm` unknown; deleting `DirichletCharacter.Basic` makes the two character names unknown |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean AwesomeTheorems/Stage1/S1_M_047.lean` | 0 | unchanged legacy discovery module elaborated with empty output; no target or proof credit |
| from `Formalizations/Lean`: `lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib and `flt-regular` package status plus `rev-parse HEAD 'HEAD^{tree}'` | 0 | both package worktrees clean at the recorded immutable revisions and trees |
| bounded exact-topic `rg` over pinned mathlib and `flt-regular` Lean sources | 1, expected no match | no root-critical half-integral or Shimura-lift declaration; this is a statement-surface check, not a completed anchor audit |
| prohibited-construct scan over target-owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, `unsafe`, `implemented_by`, or `native_decide` |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test is absent because the exact-statement deliverable did not pass |

## Retry Condition And Boundary

Retry after the intake is master-accepted, accountable reviewers lawfully preserve and
independently approve an exact primary result or explicit result composition, and the intake is
reconciled and reaccepted for its cuspidality, Hecke, level, character, parity, conductor, and
boundary choices. The pinned closure must also gain native half-integral source forms, the
theta-multiplier action, source Hecke operators and eigenfunction predicates, and checked character
and coefficient-transform interfaces. A later worker can then encode only the approved claim,
minimize imports, fingerprint the elaborated expression and environment, compile every credited
transport, and run all four mutation classes.

This is fresh current-HEAD blocker evidence only. It corrects the earlier source-availability
boundary and kernel-checks adjacent infrastructure, but it does not complete the statement item or
any downstream item. `.stage1-worker-selftest.json` is intentionally absent, and no worker `[_]`,
`H0`, master acceptance, audit completion, theorem completion, or proof credit is claimed.
