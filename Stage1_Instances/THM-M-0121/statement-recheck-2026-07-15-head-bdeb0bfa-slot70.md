# THM-M-0121 statement recheck: blocked

Item: `S56-M-0121-STATEMENT`

Base revision: `bdeb0bfae66ccfe8b672776c61bc4c74a25bef3d` (tree
`440ac842583ec6b7aa7be989ba908e8b745978b9`). Rechecked on 2026-07-15
(`Asia/Shanghai`) in worker slot 70.

## Decision

The exact-statement gate remains blocked. The repository supplies only the
label "Mori rationality theorem", Shigefumi Mori attribution, the year 1988,
and the gloss "rationality of Fano varieties". It gives no primary-source
theorem or page, exact proposition, incorporated definitions, assumptions,
conclusion convention, correction history, or independent review.

That metadata does not select one theorem. Plausible readings include the
minimal-model-program rationality theorem for a nef threshold, existence of
rational curves or uniruledness for Fano varieties, and rational connectedness
of smooth projective Fano varieties. They have different objects, binders,
hypotheses, and conclusions. The literal unqualified claim that every Fano
variety is birationally rational is false. Choosing any candidate without
source authority, or treating these conclusions as interchangeable, would
invent, weaken, broaden, or substitute the received mathematics.

No authoritative target input has resolved the collision since the latest
integrated blocker attempt. The manifest, catalog and Stage0 records, legacy
Stage1 blueprint, execution skill, intake dossier, legacy Lean module,
toolchain, and dependency lock are unchanged. The normative rev-5.6 blueprint
and execution DAG changed only for unrelated integrations; their normalized
`THM-M-0121` projections are unchanged. The immediately prior statement
recheck is now tracked at this base revision.

Consequently there is no honest canonical Lean expression whose direct
imports can be minimized or whose elaborated expression and environment can
be fingerprinted. Checked alternate transports and the removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations remain
undefined, not passed. The first failed gate remains
`exact_source_statement_identity_and_variant_selection`.

The predecessor `S56-M-0121-INTAKE` also remains provisional `[_]`, with no
master acceptance receipt. Lifecycle remains `planned`, the root vector stays
`H3 / M4 / R4`, and this statement node stays `[ ]`. This recheck claims no
statement receipt, proof, debt change, audit completion, or theorem completion.

## Pinned Lean Boundary

`StatementProbe.lean` was replayed with the existing pinned Lake artifacts. Its
sole direct import, `Mathlib.AlgebraicGeometry.RationalMap`, exposes
`Scheme.RationalMap`, `Scheme.RationalMap.domain`, and
`Scheme.RationalMap.equivFunctionField`. Removing that import makes all three
identifiers unavailable, so it is minimal for this boundary probe. It is not
an import-minimality result for the absent canonical theorem target.

The legacy module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_040.lean` also elaborated. It
explicitly leaves the theorem reading unresolved and takes both the hypothesis
and conclusion of `MoriRationalityStatementShape` as arbitrary predicates. A
successful replay cannot turn that generic interface into the requested exact
theorem.

The replay used Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake
`5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided
`Formalizations/Lean/.lake` symlink was reused read-only. No update, build,
clone, fetch, or other dependency mutation was performed.

## Validation Record

Commands ran from this worker clone unless a working directory is stated.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0121` | 0 | rank 40; planned; legacy slot `S1-M-040`; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided untracked `.lake` symlink; base revision and tree match this record |
| scoped manifest, standard, guidelines, skill, source, intake, legacy-module, probe, and prior-blocker inspection | 0 | source identity and proposition remain unresolved; the integrated blocker remains substantively correct |
| `git diff c4715a2babbead02e04d70708c3ebc58c75a1942..HEAD` over authoritative target inputs and normalized projections | 0 | no target-source, intake, legacy Lean, toolchain, or dependency-lock change; normalized `THM-M-0121` blueprint/DAG projections unchanged; prior recheck integrated |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0121/StatementProbe.lean` | 0 | three adjacent rational-map interface types elaborated; no canonical target or proof body declared |
| remove the sole import in a temporary probe copy, then from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean /tmp/THM-M-0121-no-import-slot70.lean` | 1, expected failure | `AlgebraicGeometry` and all three rational-map identifiers were unavailable; necessity applies only to the boundary probe |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean AwesomeTheorems/Stage1/S1_M_040.lean` | 0 | generic legacy discovery module elaborated with empty output; no exact-target credit |
| from `Formalizations/Lean`: `lake env lean --version`; `lake --version`; pin inspection | 0 | Lean 4.29.0, Lake 5.0.0-src+98dc76e, and pinned mathlib revision matched this record |
| mathlib package `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | package worktree clean at the pinned revision and tree above |
| bounded pinned-mathlib exact-topic search | 1, expected no match | no Fano, uniruledness, rational-connectedness, nef-threshold, or Mori-rationality match in `Mathlib/AlgebraicGeometry`; not a completed anchor audit |
| prohibited-construct scan over owned and legacy Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, `unsafe`, `implemented_by`, or `native_decide` occurrence |
| `python3 -m json.tool` on the recheck JSON | 0 | structured current-HEAD blocker record parsed |
| scoped blocker invariant assertions | 0 | item/base identity, blocked state, unchanged vector, null canonical fields, four undefined mutations, current input hashes, two-file scope, and self-test absence agree |
| scoped tracked and per-new-file `git diff --check` | 0 | no whitespace diagnostics; no-index exit 1 was only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test is absent because the exact-statement gate failed |

## Retry Condition And Boundary

Retry only after dependency acceptance and accountable reviewers preserve and
approve an immutable primary or authoritative theorem passage, select exactly
one claim, and freeze every incorporated definition, domain, ordered binder,
hypothesis, conclusion, correction, erratum, and boundary case. A fresh
statement worker can then encode only that approved claim, minimize pinned
imports, fingerprint the elaborated expression and environment, compile all
credited transports, and run all four mutation classes.

This is fresh current-HEAD target-scoped blocker evidence only. Because the
positive statement deliverable did not pass, `.stage1-worker-selftest.json` is
intentionally absent and no worker `[_]` or master acceptance is requested.
