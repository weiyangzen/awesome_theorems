# THM-M-0104 statement recheck: blocked

Item: `S56-M-0104-STATEMENT`

Base revision: `6c6ba6a88ba8abb210744f39722c3aaa0b689925` (tree
`b9a939605d30dd3e029c1cba892d8b47439b500f`). Rechecked on 2026-07-15
(`Asia/Shanghai`) in worker slot 64.

## Decision

The exact-statement gate remains blocked. The repository identifies the Bezout theorem family only
by the gloss "an upper bound on the number of intersection points of algebraic curves." It does not
fix the coefficient field, characteristic, affine or projective setting, curve model, degree,
intersection multiplicity, common-component policy, finiteness, points at infinity, or whether the
root is a distinct-point bound or a multiplicity-weighted equality.

These choices change the proposition. Projective closures can intersect only at infinity when their
affine parts do not; a tangent line and a nonsingular conic have one distinct projective
intersection but intersection number two; shared components can give infinitely many geometric
points; and rational-point counts over a non-algebraically-closed field can differ from geometric
counts. The received gloss therefore cannot identify one of those forms or a checked transport
among them.

The intake selects only a **planned** standard scope: projective plane curves over an algebraically
closed field, no common irreducible component, total local intersection multiplicity equal to the
degree product, with the distinct-point bound as a corollary. Its own README requires a pinpoint
primary source before this scope may be frozen or elaborated. Its formal module, expression,
expression hash, environment fingerprint, exact object model, source pin, and toolchain pin remain
unresolved. The prerequisite is also provisional `[_]`, not master-accepted `[x]`.

No authoritative `THM-M-0104` target input changed since the latest integrated recheck at base
`9faf2e135...`. The target manifest, catalog and Stage0 records, legacy Stage1 blueprint, execution
skill, guidelines, intake scope artifacts, legacy Lean module, toolchain, and dependency lock are
unchanged. The rev-5.6 blueprint and DAG advanced only the unrelated `THM-M-0612` release node, and
the prior blocker recheck was integrated. The target's DAG states remain intake `[_]` and statement
`[ ]`. No exact primary or approved-authoritative theorem passage, definition chain,
correction/errata disposition, immutable preservation, or independent source review was added.

Consequently no exact Lean expression can truthfully be selected, no import set can be certified
minimal for that expression, and no expression/environment fingerprint, checked alternate
encoding, or removed-hypothesis, changed-domain, changed-binder-scope, or boundary-case mutation can
be produced. Freezing the planned equality or the legacy abstract schema would invent or substitute
the received target. The first failed gate remains
`exact_source_statement_identity_and_intersection_counting_conventions`. Lifecycle stays
`planned`, root debt stays `H1 / M4 / R4`, and this item stays `[ ]`.

## Pinned Lean Boundary

The historical discovery module was freshly re-elaborated with the pinned environment. It produced
150 stdout lines and 13,250 bytes with SHA-256
`3aa7c7c88bbd78e87b58596c17d60edf6355da4c6fdfc190929cb387923bd97a`; stderr was empty. Its
`PlaneCurveIntersectionData` stores algebraic closedness, common-component exclusion, projective
support, finiteness, local multiplicity, and the local/global relation as arbitrary propositions or
data. Its `StatementShape` therefore packages the missing geometry instead of defining projective
plane curves and their intersection theory. Successful elaboration establishes adjacent API
feasibility only, not exact statement identity.

A fresh bounded search over pinned mathlib and `flt-regular` using the literal case-insensitive
regexp `bezout` found 58 matching lines, all belonging to unrelated Bezout identities, rings, and
domains. It found no named
projective-plane Bezout theorem, local intersection-multiplicity API, or exact
curve-intersection-degree endpoint under the bounded geometric spellings. This is discovery
evidence only, not the downstream anchor audit or a global absence claim.

Replay used Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`), and `flt-regular` revision
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` (tree
`32c9eace926573a9981787ae97643e520353c893`). Both pinned package worktrees were clean. The
automation-provided `.lake` symlink was reused read-only. No update, build, clone, fetch, or other
dependency mutation ran.

## Validation Record

Commands ran from the isolated worker clone unless a working directory is stated otherwise.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0104` | 0 | rank 29; planned; legacy slot `S1-M-029`; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided `Formalizations/Lean/.lake` symlink; base revision and tree match this record |
| scoped `git diff 9faf2e135...HEAD` over authoritative target inputs | 0 | no target manifest, catalog, Stage0, legacy blueprint, skill, guidelines, intake scope, legacy Lean, toolchain, or dependency-lock change; only the unrelated `THM-M-0612` release state changed in the blueprint/DAG and the prior blocker pair was integrated |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean AwesomeTheorems/Stage1/S1_M_029.lean` | 0 | 150 stdout lines, 13,250 bytes, SHA-256 `3aa7c7...23bd97a`; empty stderr; abstract discovery surface only |
| from `Formalizations/Lean`: `lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned package status and revision/tree inspection | 0 | mathlib and `flt-regular` worktrees clean at the pinned revisions/trees recorded above |
| literal case-insensitive `bezout` `rg` plus bounded geometric-intersection `rg` over pinned mathlib and `flt-regular` | 0, then 1 for the expected geometric no-match | the first regexp returned 58 matching lines, all unrelated; no exact projective/intersection-multiplicity spelling matched |
| prohibited-construct scan over owned Lean files | 1, expected no match | no owned Lean file and no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, `unsafe`, `implemented_by`, or `native_decide` occurrence |
| `python3 -m json.tool` plus scoped invariant assertions on the companion JSON | 0 | valid JSON; item/base identity, blocked state, unchanged vector, null target/import/hash fields, four undefined mutations, current hashes, exact two-file scope, and absent self-test agree |
| scoped tracked and per-new-file `git diff --check` | 0 | no whitespace diagnostics; no-index exit 1 was only each expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test is absent because the exact-statement gate failed |

The companion JSON is the structured blocker packet. It binds the finalized Markdown hash and
explicitly excludes its self-referential JSON hash; the integration lane must recapture both final
hashes. It is unsigned, nonrelease, non-content-addressed evidence, not a statement receipt.

## Retry Condition And Boundary

Retry after the intake is master-accepted and accountable reviewers preserve and approve one exact
primary or approved-authoritative proposition with a stable locator, complete definition chain,
proof boundary, corrections and errata disposition, and independent review. The review must fix the
field and characteristic, affine/projective scope, curve representation, component/degeneracy
policy, degree, local multiplicity, finite support, points at infinity, equality/bound relationship,
ordered binders, universes, typeclasses, and every credited transport. A later statement worker can
then elaborate only that claim with minimal pinned imports, serialize the expression and environment
fingerprints, compile the transports, and run all four mutation classes.

This is current-HEAD target-scoped blocker evidence only. It does not satisfy
`S56-M-0104-STATEMENT`, propose worker `[_]`, alter scheduler state, claim audit or theorem
completion, emit a receipt, or claim master acceptance. Because the requested positive deliverable
did not pass, `.stage1-worker-selftest.json` is intentionally absent.
