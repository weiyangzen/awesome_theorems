# THM-M-0105 statement recheck: blocked

Item: `S56-M-0105-STATEMENT`

Base revision: `255c85c9e88403358cd081cd624f3b90eb808654` (tree
`5165028b1b2e17baadaf6a4936b14b7b5fd8c9ed`). Rechecked on 2026-07-15
(`Asia/Shanghai`) in worker slot 54.

## Decision

The exact-statement gate is still blocked. The intake selects the intended
human formula for a smooth projective geometrically integral curve over an
arbitrary field,

`l(D) - l(K_X - D) = deg(D) + 1 - g(X)`,

where `l(E) = dim_k H^0(X, O_X(E))`. It deliberately leaves the canonical
Lean expression and environment fingerprint null. The Hartshorne Chapter IV,
Section 1, Theorem 1.3 reference remains an unaccepted lead: no approved
edition/page/definition/errata review or bridge to the intake's arbitrary-field,
geometrically-integral scheme normalization exists.

The proposition-changing formal choices remain unresolved: a divisor model
attached to `X`; canonical divisor construction and witness; `O_X(D)` and
global sections; degree and genus; finite-dimensionality; natural versus
integer codomains and coercions; projective versus proper; binder order,
universes, and the empty or nonempty curve boundary. Selecting these from
mathematical familiarity would invent part of the target rather than elaborate
the intake-selected claim.

The legacy declaration
`AwesomeTheorems.Stage1.S1_M_027.THM_M_0105_StatementShapeTarget` remains
ineligible. It existentially chooses an unconstrained
`RiemannRochDivisorData` package, so the chosen data can encode the requested
equality. It omits concrete curve-relative divisors, canonicality, `O_X(D)`,
global sections, degree, genus, projectivity, and geometric integrality.
Renaming or compiling it would be a broadened substitute, not an exact target.

No authoritative target input changed after the integrated blocker attempt.
The target manifest, catalog and Stage0 records, legacy Stage1 blueprint,
execution skill, guidelines, intake dossier, legacy Lean module, toolchain,
and dependency lock are byte-identical. The `THM-M-0105` projections of the
rev-5.6 blueprint and execution DAG are also unchanged. The prior statement
probe and blocker were themselves integrated.

Consequently there is still no canonical Lean expression whose direct imports
can be minimized or whose elaborated expression and environment can be
fingerprinted. Checked alternate transports and the removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations remain
undefined, not passed. The first failed gate remains
`exact_source_statement_identity_and_concrete_lean_definition_chain`.

The predecessor `S56-M-0105-INTAKE` remains provisional `[_]`, with no master
acceptance receipt. Lifecycle remains `planned`, the vector remains
`H5 / M5 / R4`, and this statement node remains `[ ]`. This recheck claims no
statement receipt, proof, debt change, audit completion, or theorem completion.

## Pinned Lean Boundary

`StatementProbe.lean` was replayed with five direct imports. It checks only
adjacent pinned interfaces: schemes, spectra, smoothness, properness,
geometric integrality, scheme modules and their presheaves, sheaf cohomology,
and module finrank. It exits 0 and prints ten lines (820 bytes), with stdout
SHA-256 `73b1db9866910a12bc451c95102136d0a4b8afc91c01e94ef747fd12e9544e29`.
It declares no canonical target, transport, axiom, or proof body. Its imports
therefore are not claimed minimal for the absent root expression.

A bounded pinned-mathlib search still found no algebraic-geometry
Riemann-Roch, Cartier/Weil divisor, canonical or dualizing divisor/sheaf, or
arithmetic-genus interface. Existing scheme-module and sheaf-cohomology APIs
are substrate only; this search is statement-boundary evidence, not the later
anchor audit.

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
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0105` | 0 | rank 27; planned; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided `.lake` symlink; base revision and tree match this record |
| scoped inspection of the standard, skill, manifest, sources, intake dossier, legacy module, and integrated blocker | 0 | the arbitrary-field formula remains selected but its source bridge and concrete Lean target remain unresolved |
| scoped diff from `d5771f240b8fe26277d018c90fec963af76ed7f2` | 0 | target sources, intake, legacy Lean, toolchain, and dependency lock are unchanged; normalized target projections are unchanged; prior blocker artifacts were integrated |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0105/StatementProbe.lean` | 0 | nine adjacent interfaces elaborated; stdout was ten lines/820 bytes at the hash above; stderr was empty |
| from `Formalizations/Lean`: `lake env lean --version`; `lake --version` | 0 | Lean and Lake versions match the pinned environment above |
| mathlib package `git status --short`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | package worktree clean at the pinned revision and tree above |
| bounded exact-topic `rg` search over pinned mathlib | 1, expected no match | no exact-topic declaration was located |
| `python3 -m json.tool` and scoped invariant checks on the companion recheck JSON | 0 | blocked identity, current hashes, two-file change scope, false completion fields, null target/import/hash fields, and self-test absence agreed |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, `unsafe`, `implemented_by`, `native_decide`, or `proof_wanted` occurrence |
| scoped tracked and per-new-file `git diff --check` | 0 | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test is absent because the exact-statement deliverable failed |

## Retry Condition And Boundary

Retry after the intake is master-accepted and an accountable source reviewer
preserves and approves an immutable exact statement and definition chain,
including the arbitrary-field bridge. A later worker can then encode only that
reviewed claim with concrete Lean objects, minimize its imports, serialize and
hash the elaborated expression and environment, compile every credited
transport, and execute all four mutation classes.

This is fresh current-HEAD blocker evidence only. It does not satisfy
`S56-M-0105-STATEMENT`, request worker `[_]`, change scheduler state, or claim
an elaborated target, minimal imports, audit completion, theorem completion,
or master acceptance. Because the positive statement deliverable did not
pass, `.stage1-worker-selftest.json` is intentionally absent.
