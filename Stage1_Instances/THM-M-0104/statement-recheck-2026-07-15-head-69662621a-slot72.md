# THM-M-0104 statement recheck: blocked

Item: `S56-M-0104-STATEMENT`

Base revision: `69662621a19907de342801b09124e8dfe3495e40` (tree
`fbfbc07e2045accdd0144baf892481a9bb6717f8`). Rechecked on 2026-07-15
(`Asia/Shanghai`) in worker slot 72.

## Decision

The exact-statement gate is still blocked. The repository identifies the Bezout theorem family
only through the gloss "an upper bound on the number of intersection points of algebraic curves."
It does not select affine or projective curves, a coefficient field, a curve model, distinct or
multiplicity-weighted intersections, degree and local-multiplicity conventions, a
common-component hypothesis, points at infinity, or equality versus upper bound. Each choice
changes the proposition.

The intake's projective-plane multiplicity equality is explicitly a planned scope, not a frozen
claim: over an algebraically closed field, two projective plane curves with no common irreducible
component should have total local intersection multiplicity equal to the product of their degrees,
with the distinct-point bound as a corollary. The intake requires a pinpoint primary source before
that selection may be frozen or elaborated. Its formal target, expression hash, environment
fingerprint, object model, degree, multiplicity, source pin, and exact toolchain record remain open.
The prerequisite also remains provisional `[_]`, not master-accepted `[x]`.

A bounded source recheck did not cure that defect. At immutable Stacks Project commit
`4ac4815d5a00dc2eacab7824cf4e4baafe2773ac`, the likely intersection, Chow, and curve sources do
not state the exact plane-curve theorem. Stacks tag `0GYA` only asks for a fact related to
"Bezout's theorem on intersections" and even permits a special case; it fixes none of the required
assumptions or conventions. A likely matching Fulton text could not be retrieved from its former
locator, so no edition, page, theorem number, complete passage, or content hash was verified.
Neither lead can lawfully freeze the root.

No authoritative target input changed after the prior blocker attempt. The target manifest,
catalog and Stage0 records, legacy Stage1 blueprint, execution skill, guidelines, intake dossier,
legacy Lean module, toolchain, and dependency lock are unchanged. The rev-5.6 blueprint and
execution DAG changed only for unrelated worker-state projections; all `THM-M-0104` entries are
unchanged. The prior blocker was itself integrated.

The historical `AwesomeTheorems.Stage1.S1_M_029.StatementShape` remains ineligible. Its
`PlaneCurveIntersectionData` stores algebraic closedness, common-component exclusion, projective
support, finiteness, local multiplicity, total multiplicity, and the local/global relationship as
arbitrary data or propositions. It therefore packages the missing geometry instead of defining
the curves and their intersection theory. Its successful elaboration does not identify the
received claim, and its ten imports cannot be certified minimal for an absent canonical target.

Consequently there is still no exact Lean expression whose imports can be minimized or whose
expression and environment can be fingerprinted. Checked transports and the required removed-
hypothesis, changed-domain, changed-binder-scope, and boundary mutations remain undefined. The
first failed gate remains `exact_source_statement_identity_and_intersection_counting_conventions`.
Lifecycle stays `planned`, the root vector stays `H1 / M4 / R4`, and the statement node stays
`[ ]`. No proof, receipt, debt change, audit completion, theorem completion, or master acceptance
is claimed.

## Pinned Lean Boundary

The legacy discovery module was freshly re-elaborated with the pinned environment. Its output has
150 lines, 13,250 bytes, and SHA-256
`3aa7c7c88bbd78e87b58596c17d60edf6355da4c6fdfc190929cb387923bd97a`; stderr was empty. It
checks adjacent Proj, scheme, homogeneous-polynomial, finite-length, and Hilbert-polynomial APIs,
but no concrete projective-plane intersection-multiplicity target.

A fresh bounded search over pinned mathlib and `flt-regular` found only unrelated Bezout identity,
Bezout ring, and Bezout domain declarations. It found no named projective-plane Bezout theorem,
local intersection-multiplicity API, or exact curve-intersection degree declaration in the searched
surfaces. This is local discovery evidence, not a global absence claim or the downstream anchor
audit.

Replay used Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided `.lake` symlink was reused
read-only. No dependency update, build, clone, fetch, or other `.lake` mutation was performed.

## Validation Record

Commands ran from this isolated worker clone unless a working directory is stated otherwise.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0104` | 0 | rank 29; planned; legacy slot `S1-M-029`; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided `.lake` symlink; base revision and tree match this record |
| scoped source, standard, skill, intake, legacy-module, and prior-blocker inspection | 0 | the source ambiguity, planned scope, excluded substitutions, and failed gate remain unchanged |
| `git diff 8400eb33...HEAD` over authoritative target inputs | 0 | no target manifest, catalog, Stage0, legacy blueprint, skill, guidelines, intake, legacy Lean, toolchain, or dependency-lock change; blueprint/DAG changes are unrelated to `THM-M-0104`; prior blocker was integrated |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean AwesomeTheorems/Stage1/S1_M_029.lean` | 0 | 150 stdout lines and 13,250 bytes at SHA-256 `3aa7c7...23bd97a`; empty stderr; abstract discovery surface only |
| from `Formalizations/Lean`: `lake env lean --version`; `lake --version` | 0 | Lean and Lake versions match the pinned environment above |
| mathlib package `git status --short`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | package worktree clean at the pinned revision and tree above |
| bounded exact-topic `rg` over pinned mathlib and `flt-regular` | 0 | only unrelated Bezout identities/rings/domains matched; no exact projective-plane target or local intersection-multiplicity interface was located |
| bounded immutable-source recheck | 0 | Stacks commit `4ac4815...73ac` supplied intersection-theory substrate and exercise tag `0GYA`, but no exact plane-curve Bezout statement; a likely Fulton source locator was unavailable, so no source passage was accepted |
| `python3 -m json.tool` on the recheck JSON | 0 | structured current-HEAD blocker record parsed |
| scoped blocker invariant assertions | 0 | item/base identity, blocked state, unchanged vector, null target/import/hash fields, four undefined mutations, hashes, two-file scope, and self-test absence agree |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, `unsafe`, `implemented_by`, or `native_decide` occurrence |
| scoped tracked and per-new-file `git diff --check` | 0 | no whitespace diagnostics; no-index exit 1 was only each expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test is absent because the exact-statement gate failed |

## Retry Condition And Boundary

Retry after the intake is master-accepted and accountable reviewers lawfully preserve and approve
one exact primary or approved-authoritative proposition with a stable locator, incorporated
definitions, correction and errata disposition, and independent review. The review must fix the
affine/projective boundary, field and characteristic, curve representation, component and
degeneracy policy, degree, local multiplicity, finiteness, points at infinity, equality/bound
relationship, ordered binders, universes, typeclasses, and all credited transports. A fresh worker
can then encode only that claim, minimize pinned imports, fingerprint the elaborated expression and
environment, compile every transport, and execute all four mutation classes.

This is fresh current-HEAD blocker evidence only. Because the positive statement deliverable did
not pass, `.stage1-worker-selftest.json` is intentionally absent and no worker `[_]` or master
acceptance is requested.
