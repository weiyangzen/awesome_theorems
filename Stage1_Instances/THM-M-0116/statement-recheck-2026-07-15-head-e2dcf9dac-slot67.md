# THM-M-0116 statement recheck: blocked

Item: `S56-M-0116-STATEMENT`

Base revision: `e2dcf9dac5876bb5b659eb8185d8de16d53b3ff4` (tree
`62cdca59e6cd4e6cccbe8cfafdeb54d3874052ac`). Rechecked on 2026-07-15
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
- no algebraic-equivalence relation on divisors or line bundles, nor a Picard
  scheme or `Pic^0`; and
- no concrete Neron-Severi quotient with an additive-group instance.

The current pinned-source searches found only projective-spectrum and
elliptic-coordinate modules under `Mathlib.AlgebraicGeometry`. Exact searches
found no Neron-Severi, algebraic-equivalence, Cartier/Weil-divisor,
line-bundle, projective-morphism, or general projective-scheme declaration.
The only algebraic-geometry `Picard group` text is prose in the elliptic-curve
Weierstrass module. Ring-level `CommRing.Pic`, `Scheme.Modules`, and
`Scheme.IdealSheafData` are adjacent substrate, not checked scheme Picard or
Neron-Severi constructions.

The legacy `AwesomeTheorems.Stage1.S1_M_036.StatementShape` remains
ineligible. It accepts an arbitrary `Scheme -> Type` group parameter, replaces
projectivity by a smooth/proper boundary, and never defines divisors modulo
algebraic equivalence. An arbitrary group, relation, or author-named semantic
field would likewise substitute a different theorem because it has no checked
connection to `X`. Properness cannot replace projectivity, numerical
equivalence cannot replace algebraic equivalence, and `CommRing.Pic` cannot be
treated as the scheme-level quotient.

No target input that could clear this blocker changed after the integrated
`69f012f97` recheck. The target manifest, catalog and Stage0 records, legacy
Stage1 blueprint, execution skill, guidelines, intake dossier, legacy Lean
module, toolchain, dependency lock, and both owned probes are byte-identical.
The rev-5.6 blueprint and execution DAG changed only for unrelated targets;
they still record intake provisional `[_]` with one attempt and this statement
node `[ ]` with zero attempts. The only target-owned change was integration of
the prior recheck itself.

There is consequently no canonical Lean expression whose imports can be
minimized or whose elaborated expression and environment can be fingerprinted.
Checked transports and the four semantic mutation classes remain undefined.
The first failed gate is
`exact_target_expressibility_in_pinned_environment`. Lifecycle remains
`planned`, the vector remains `H2 / M4 / R4`, and the statement node remains
`[ ]`. The intake prerequisite is also not master-accepted. No receipt, proof,
debt change, audit completion, or theorem completion is claimed.

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
| `git diff 69f012f979c7114db1ee4a877c5742d4742cadba..HEAD` over authoritative target inputs | 0 | source, intake, skill, legacy Lean, toolchain, lock, and probes are unchanged; blueprint/DAG deltas concern unrelated targets; the prior target recheck was integrated |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0116/StatementInfrastructure.lean` | 0 | 12 combined-output lines, 789 bytes, SHA-256 `3e14279a...f4f3`; adjacent APIs elaborated and both expected missing-name checks succeeded |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0116/StatementProbe.lean` | 0 | 12 combined-output lines, 792 bytes, SHA-256 `51a41c02...a538`; native domain and generic quotient boundaries elaborated, not the target |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean AwesomeTheorems/Stage1/S1_M_036.lean` | 0 | 64 combined-output lines, 4846 bytes, SHA-256 `571b97d2...ce5c`; legacy arbitrary-group boundary elaborated and remains ineligible |
| Lean/Lake version and mathlib revision/tree/status checks | 0 | versions and revisions match the pinned environment above; mathlib worktree clean |
| six bounded `rg`/file searches over pinned mathlib for projectivity, divisors, line bundles, Picard/NS, and algebraic equivalence | completed | no root-critical scheme-level declaration or checked construction was found; unrelated projective-spectrum, coordinate, ring-Picard, and prose matches were rejected |
| prohibited-construct scan over owned Lean files | expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, bodyless `constant`, `opaque`, `unsafe`, `implemented_by`, or `native_decide` occurrence |
| `python3 -m json.tool` on the paired recheck JSON | 0 | structured current-HEAD blocker record parsed as valid JSON |
| scoped blocker invariant assertions | 0 | item/base identity, blocked state, unchanged vector, null exact-target fields, four undefined mutations, current hashes, two-file scope, and self-test absence agree |
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
