# THM-M-0116 statement recheck: blocked

Item: `S56-M-0116-STATEMENT`

Base revision: `69f012f979c7114db1ee4a877c5742d4742cadba` (tree
`a4415d1a7f473d7540904dd4fd84d17ac0f99820`). Rechecked on 2026-07-15
(`Asia/Shanghai`) in worker slot 67.

## Decision

The exact-statement gate remains blocked. The frozen claim says that for an
algebraically closed field `k` and a smooth projective algebraic surface `X`
over `k`, the concrete Neron-Severi group `NS(X)`, defined as divisors modulo
algebraic equivalence, is finitely generated as an abelian group.

The pinned closure still lacks the root-critical interfaces needed to express
that target:

- no general projective-morphism predicate for an arbitrary scheme over
  `Spec k`;
- no scheme-level Cartier or Weil divisor group, Picard group, or line-bundle
  group suitable for this surface;
- no algebraic-equivalence relation on divisors or line bundles; and
- no concrete Neron-Severi quotient with an additive-group instance.

A deeper current-HEAD source audit confirms that adjacent sheaf infrastructure
does not close this gap. Mathlib has `Scheme.Modules`, module presheaves and
sheaves, generic sheaf cohomology, `IdealSheafData`, and the ring-level
`CommRing.Pic`. It has no scheme-level locally-free rank-one or invertible-sheaf
group, no sheaf-module tensor/monoidal instance supporting such a group, no
Cartier/Weil divisor or codimension-one cycle interface, and no Picard scheme or
`Pic^0`/algebraic-equivalence quotient. `IdealSheafData` is documented as not
yet being an actual subsheaf of the structure sheaf. Building any of the
divisor, line-bundle, or `H^1(O_X^*)` routes would therefore be a substantial
new formalization, not statement elaboration with minimal imports.

The legacy `AwesomeTheorems.Stage1.S1_M_036.StatementShape` remains
ineligible: it accepts an arbitrary `Scheme -> Type` group parameter, replaces
projectivity by a smooth/proper boundary, and never defines divisors modulo
algebraic equivalence. A seemingly stronger scaffold with an arbitrary
`AddCommGroup`, subgroup, and named `Prop` fields asserting projectivity or
modeling is also not exact. Those propositions have no Lean semantics tying
the data to `X`; they can be set independently, so the quantified target would
range over bogus presentations and state a different theorem. Existing
provisional semantic-interface dossiers for other targets are not accepted
receipts and cannot waive the exact-expression/checked-transport gate here.

No authoritative input for this target changed since the integrated
`b4d239943` recheck. The target manifest, catalog and Stage0 records, legacy
Stage1 blueprint, skill, guidelines, intake dossier, legacy Lean module,
toolchain, dependency lock, and owned probes are byte-identical. The rev-5.6
blueprint and execution DAG changed only for unrelated targets and still leave
intake provisional `[_]` with one attempt and this node `[ ]` with zero
attempts. The prior recheck is the only target-owned addition.

There is consequently no canonical Lean expression whose imports can be
minimized or whose elaborated expression and environment can be fingerprinted.
Checked transports and the four semantic mutation classes remain undefined.
The first failed gate is
`exact_target_expressibility_in_pinned_environment`. Lifecycle remains
`planned`, the vector remains `H2 / M4 / R4`, and the statement node remains
`[ ]`. The intake prerequisite also remains provisional rather than
master-accepted. No receipt, proof, debt change, audit completion, or theorem
completion is claimed.

## Pinned Lean Boundary

Both owned probes and the legacy discovery module were replayed with the
existing pinned Lake artifacts. `StatementInfrastructure.lean` elaborates nine
adjacent APIs and confirms the expected absence of `NeronSeveriGroup` and
`AlgebraicGeometry.IsProjective`. `StatementProbe.lean` elaborates only the
native smooth/proper relative-dimension-two boundary and a generic additive
quotient shape. Neither defines the target, a checked transport, or a proof.

The replay used Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake
`5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided
`Formalizations/Lean/.lake` symlink was reused read-only. No update, build,
clone, fetch, or other dependency mutation was performed.

## Validation Record

Commands ran from this isolated worker clone unless a working directory is
stated otherwise.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0116` | 0 | rank 36; planned; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --branch --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided `.lake` symlink; base revision and tree match this record |
| `git diff b4d239943a37f6c25c377bbfd85c0e1ec7f4acaa..HEAD` over authoritative target inputs | 0 | target inputs and owned probes are unchanged; blueprint/DAG changes concern unrelated targets; only the prior target recheck was integrated |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0116/StatementInfrastructure.lean` | 0 | 12 combined-output lines, 789 bytes, SHA-256 `3e14279a...f4f3`; adjacent APIs elaborated and both expected missing-name checks succeeded |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0116/StatementProbe.lean` | 0 | 12 combined-output lines, 792 bytes, SHA-256 `51a41c02...a538`; native domain and generic quotient boundaries elaborated, not the target |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean AwesomeTheorems/Stage1/S1_M_036.lean` | 0 | 64 combined-output lines, 4846 bytes, SHA-256 `571b97d2...ce5c`; legacy arbitrary-group boundary elaborated and remains ineligible |
| Lean/Lake version and mathlib revision/tree/status checks | 0 | versions and revisions match the pinned environment above; mathlib worktree clean |
| bounded pinned-source audit for projectivity, divisors, line bundles, Picard/NS, algebraic equivalence, tensor structure, and dimension APIs | completed | adjacent sheaf/ring interfaces found, but no root-critical scheme-level declaration or checked construction |
| prohibited-construct scan over owned Lean files | expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, bodyless constant, `opaque`, `unsafe`, `implemented_by`, or `native_decide` occurrence |
| `python3 -m json.tool` on the paired recheck JSON | 0 | structured current-HEAD blocker record parsed as valid JSON after finalization |
| scoped blocker invariant assertions | 0 | item/base identity, blocked state, unchanged vector, null target/import/hash fields, four undefined mutation classes, two-file scope, and self-test absence agree |
| scoped tracked and per-new-file `git diff --check` | 0 tracked; 1 per new file, expected difference | all checks have empty whitespace diagnostics; no-index exit 1 only records that each new file differs from `/dev/null` |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test is absent because the exact-statement gate failed |

## Retry Condition And Boundary

Retry after the intake is master-accepted, reviewers approve the exact source
and modern-definition mapping, and the pinned closure gains native or locally
defined, source-faithful interfaces for projectivity over the base, the chosen
scheme divisor or line-bundle group, algebraic equivalence, and the concrete
Neron-Severi quotient. A fresh worker can then elaborate only that frozen
target, minimize imports, fingerprint the expression and environment, compile
credited transports, and run every mutation class.

This is fresh current-HEAD blocker evidence only. Because the positive
statement deliverable did not pass, `.stage1-worker-selftest.json` is
intentionally absent and no worker `[_]` or master acceptance is requested.
