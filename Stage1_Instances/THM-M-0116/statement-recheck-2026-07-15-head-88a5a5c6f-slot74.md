# THM-M-0116 statement recheck: blocked

Item: `S56-M-0116-STATEMENT`

Base revision: `88a5a5c6fe6bac0d813a74ca20fa553eaf2a6d68` (tree
`a0a75048a918a3bf566c3dbcf6b4352c3b2ee8e4`). Rechecked on 2026-07-15
(`Asia/Shanghai`) in worker slot 74.

## Decision

The exact-statement gate remains blocked. The frozen target says that for an
algebraically closed field `k` and a smooth projective algebraic surface `X`
over `k`, the concrete Neron-Severi group `NS(X)`, defined as divisors modulo
algebraic equivalence, is finitely generated as an abelian group.

The pinned closure still lacks the root-critical interfaces needed to express
that target:

- no general projective-morphism predicate for an arbitrary scheme over
  `Spec k`;
- no concrete scheme-level divisor or Picard group suitable for this surface;
- no algebraic-equivalence additive congruence on those divisors or line
  bundles; and
- no concrete Neron-Severi quotient with its additive-group instance.

No authoritative target input changed after the prior blocker. The target
manifest, catalog and Stage0 records, legacy Stage1 blueprint, execution skill,
guidelines, intake dossier, legacy Lean module, toolchain, and dependency lock
are unchanged. The rev-5.6 blueprint and execution DAG changed only for
unrelated integration state and still record intake `[_]` with one attempt and
this statement node `[ ]` with zero attempts. The prior blocker and both owned
probes are now integrated. The later `StatementProbe.lean` only checks a
smooth/proper dimension-two domain and an arbitrary additive quotient; it does
not supply the missing semantics or alter the blocker.

The legacy `AwesomeTheorems.Stage1.S1_M_036.StatementShape` remains
ineligible. It accepts an arbitrary `Scheme -> Type` group parameter, replaces
projectivity by a smooth/proper boundary, and never defines divisors modulo
algebraic equivalence. Treating its parameter or a newly invented relation as
`NS(X)` would substitute a different theorem. The ring-level `CommRing.Pic`
API and `Proj.toSpecZero` properness likewise do not provide checked transports
to the frozen scheme-level objects.

There is therefore no canonical Lean expression whose imports can be
minimized or whose elaborated expression and environment can be fingerprinted.
Checked transports and the four structural mutation classes are undefined.
The first failed gate remains
`exact_target_expressibility_in_pinned_environment`. Lifecycle remains
`planned`, the vector remains `H2 / M4 / R4`, and the statement node remains
`[ ]`. No proof, receipt, debt change, audit completion, or theorem completion
is claimed.

The intake prerequisite is independently only provisional `[_]`; it has not
been master-accepted and therefore cannot support statement acceptance.

## Pinned Lean Boundary

Both owned probes were replayed with the existing pinned Lake artifacts.
`StatementInfrastructure.lean` imports the algebraically closed field, smooth,
proper, projective-spectrum, finite-generation, and ring Picard modules. It
elaborates nine adjacent declarations and confirms the expected absence of
`NeronSeveriGroup` and `AlgebraicGeometry.IsProjective`.

`StatementProbe.lean` uses four direct imports for properness, smoothness,
algebraic closedness, and group finiteness. It elaborates only a native
smooth/proper relative-dimension-two boundary and the generic proposition that
an arbitrary additive-congruence quotient is finitely generated. Neither file
declares the canonical target or presents a substitute predicate as that
target; neither contains a transport, axiom, or proof. Their imports are probe
surfaces, not a minimal-import claim for the absent target.

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
| scoped source, standard, skill, dossier, legacy-module, probe, and prior-blocker inspection | 0 | the exact scope and exclusions are unchanged; the prior blocker remains substantively correct |
| `git diff cb7809d0317a837cb067c0d3fe417c84f167b350..HEAD` over authoritative target inputs | 0 | source, intake, legacy Lean, toolchain, and lock are unchanged; blueprint/DAG entries remain semantically unchanged; prior evidence was integrated |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0116/StatementInfrastructure.lean` | 0 | 12 combined-output lines, 789 bytes, SHA-256 `3e14279a...f4f3`; adjacent APIs elaborated and both expected missing-name checks succeeded |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0116/StatementProbe.lean` | 0 | 12 combined-output lines, 792 bytes, SHA-256 `51a41c02...a538`; native domain and generic quotient boundaries elaborated, not the target |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean AwesomeTheorems/Stage1/S1_M_036.lean` | 0 | 64 combined-output lines, 4846 bytes, SHA-256 `571b97d2...ce5c`; legacy arbitrary-group boundary elaborated and remains ineligible |
| Lean/Lake version and mathlib revision/tree/status checks | 0 | versions and revisions match the pinned environment above; mathlib worktree clean |
| four bounded searches over pinned mathlib | completed | no root-critical scheme-level Neron-Severi, algebraic-equivalence, projectivity, Picard, or divisor declaration was found; unrelated matches were rejected |
| `python3 -m json.tool` on the recheck JSON | 0 | structured current-HEAD blocker record parsed after finalization |
| scoped blocker invariant assertions | 0 | item/base identity, blocked state, unchanged vector, null target/import/hash fields, four undefined mutation classes, hashes, two-file scope, and self-test absence agree |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, `unsafe`, `implemented_by`, or `native_decide` occurrence |
| scoped tracked and per-new-file `git diff --check` | 0 tracked; 1 per new file, expected difference | all checks have empty whitespace diagnostics; no-index exit 1 only records that each new file differs from `/dev/null` |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test is absent because the exact-statement gate failed |

## Retry Condition And Boundary

Retry after the intake is master-accepted, reviewers approve the exact source
and modern-definition mapping, and the pinned closure gains conclusion-free
native interfaces for projectivity over the base, the selected scheme divisor
or Picard group, algebraic equivalence, and the concrete Neron-Severi quotient.
A fresh worker can then elaborate only the frozen target, minimize imports,
fingerprint the expression and environment, compile credited transports, and
run every mutation class.

This is fresh current-HEAD blocker evidence only. Because the positive
statement deliverable did not pass, `.stage1-worker-selftest.json` is
intentionally absent and no worker `[_]` or master acceptance is requested.
