# THM-M-0124 statement recheck: blocked

Item: `S56-M-0124-STATEMENT`

Base revision: `b4d239943a37f6c25c377bbfd85c0e1ec7f4acaa` (tree
`5f13e0e86bde3bcaaef38b979819490c648166e3`). Rechecked on 2026-07-15
(`Asia/Shanghai`) in worker slot 79.

## Decision

The exact-statement gate remains blocked. The repository catalog names the Manin-Drinfeld theorem
but describes only unspecified "properties of Heegner points on elliptic curves." That is a
different topic, not a proposition that can be normalized into the requested theorem.

The intake instead selects the standard theorem family: a degree-zero divisor supported on the
cusps of a congruence modular curve should have torsion class in its Jacobian, with the difference
of two cusps as an intended generator form. That selection is expressly prose-frozen but not a
canonical source or Lean statement. The cited Manin and Drinfeld papers still lack an accepted
theorem/page transcription, exact hypotheses and generality, incorporated definitions, translation
and errata review, and independent source review. The arithmetic base, geometric-versus-rational
cusp and divisor conventions, Jacobian versus `Pic^0`, ordered binders, degeneracies, and checked
equivalence between the pairwise and all-degree-zero-divisor forms also remain open. Choosing them
here would invent proposition-changing mathematics.

The predecessor intake is only provisional `[_]`, not master-accepted `[x]`. No authoritative
target input changed after the prior blocker: the target manifest, catalog, Stage0 and legacy
Stage1 records, skill, guidelines, intake dossier, legacy Lean module, toolchain, dependency lock,
and `THM-M-0124` checklist entries are unchanged. The prior probe and blocker were integrated;
intervening blueprint and execution-DAG changes concern unrelated items.

The concrete pinned Lean surface also cannot encode the planned claim. It supplies congruence
subgroups, cusps, cusp orbits, and finiteness of those orbits, but the bounded local search found no
associated compactified modular curve, curve Jacobian or degree-zero Picard group, cuspidal
divisor-class construction, Abel-Jacobi map, or exact Manin-Drinfeld declaration. Mathlib's
`RingTheory.PicardGroup` and analytic Jacobian files are unrelated abstractions, not this geometric
object model.

The historical `AwesomeTheorems.Stage1.S1_M_043.StatementShape` cannot fill the gap. Its caller
supplies an abstract compactified-curve point type, additive target, cusp inclusion, and arbitrary
divisor-class map. It therefore assumes away the missing modular curve, Jacobian, and Abel-Jacobi
construction. It also ranges over arithmetic subgroups while its own decision metadata says the
public root should use congruence subgroups. Fresh elaboration succeeds, but the module explicitly
labels itself `statementShapeOnly` and says it may not mark the theorem completed.

Consequently there is no truthful canonical Lean expression, minimal canonical import set,
expression hash, environment fingerprint, checked alternate-form transport, or meaningful
removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutation suite. The first
failed gate remains `exact_source_statement_and_concrete_formal_object_model`. Lifecycle remains
`planned`, root debt remains `H1 / M4 / R4`, and the statement node remains `[ ]`. No proof,
receipt, debt change, audit completion, theorem completion, or master acceptance is claimed.

## Pinned Lean Boundary

`StatementProbe.lean` has one direct import:
`Mathlib.NumberTheory.ModularForms.Cusps`. Fresh elaboration emitted four API types, 310 bytes, at
SHA-256 `2d31e6ab6b2dd3018738af639c7e84a7dcea236e34a0dbe4fca31b6bffa93547`; stderr was empty. Its
congruence-subgroup cusp-orbit finiteness example elaborated too. This proves that the pinned Lean
installation and adjacent substrate work, not that the Manin-Drinfeld target exists. The import is
minimal for this probe only; target-import minimality is not assessable without a canonical target.

The legacy discovery module freshly elaborated with 17 stdout lines, 1,296 bytes, and SHA-256
`0f9cf61b87219c06e8e2f14479e2ad675a4f097e0447d7a3bf8434833c01fe11`; stderr was empty. It
receives discovery credit only.

Replay used Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`), and `flt-regular` revision
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` (tree
`32c9eace926573a9981787ae97643e520353c893`). Both dependency worktrees were clean. The
automation-provided canonical `.lake` symlink was reused read-only. No update, build, clone, fetch,
or dependency mutation was performed.

## Validation Record

Commands ran from this isolated worker clone unless a working directory is stated otherwise.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0124` | 0 | rank 43; planned; legacy slot `S1-M-043`; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided `.lake` symlink; base revision and tree match this record |
| scoped source, standard, skill, intake, legacy-module, and prior-blocker inspection | 0 | source ambiguity, planned scope, exclusions, and failed statement gate remain unchanged |
| `git diff 90a1d52c...HEAD` over authoritative target inputs | 0 | no target manifest, catalog, Stage0, legacy blueprint, skill, guidelines, intake, legacy Lean, toolchain, or lock change; prior blocker was integrated; blueprint/DAG changes are unrelated to this target |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0124/StatementProbe.lean` | 0 | four stdout lines and 310 bytes at SHA-256 `2d31e6...93547`; empty stderr; concrete cusp substrate only |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean AwesomeTheorems/Stage1/S1_M_043.lean` | 0 | 17 stdout lines and 1,296 bytes at SHA-256 `0f9cf6...fe11`; empty stderr; abstract boundary only |
| from `Formalizations/Lean`: `lake env lean --version`; `lake --version` | 0 | Lean and Lake versions match the pinned environment above |
| mathlib and `flt-regular` package status plus revision/tree checks | 0 | both worktrees clean at the pinned revisions and trees above |
| bounded exact-topic `rg` over pinned mathlib and `flt-regular` | 1, expected no match | zero output; no exact target or concrete modular-curve/Jacobian/Picard construction was located in the searched surfaces |
| `python3 -m json.tool` on the recheck JSON | 0 | structured current-HEAD blocker record parsed |
| scoped blocker invariant assertions | 0 | item/base identity, blocked state, unchanged vector, null target/import/hash fields, four undefined mutations, two-file scope, and absent self-test agree |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, `unsafe`, `implemented_by`, or `native_decide` occurrence |
| scoped tracked and per-new-file `git diff --check` | 0 | no whitespace diagnostics; no-index exit 1 was only each expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test is absent because the exact-statement gate failed |

## Retry Condition And Boundary

Retry after intake master acceptance and after accountable reviewers preserve and approve one exact
primary or approved-authoritative statement with stable theorem/page locators, incorporated
definitions, assumptions, proof boundary, corrections, errata disposition, and independent review.
That review must fix subgroup generality, base, cusp/divisor conventions, Jacobian or `Pic^0`
target, ordered binders, typeclass assumptions, degeneracies, and all credited alternate forms.
Concrete pinned Lean constructions for the associated compactified modular curve, its Jacobian or
degree-zero Picard group, and the cuspidal divisor-class map must then exist or be provided. A fresh
worker can encode only that reviewed claim, minimize imports, fingerprint the elaborated expression
and environment, compile every transport, and execute all four mutation classes.

This is fresh current-HEAD blocker evidence only. Because the positive statement deliverable did
not pass, `.stage1-worker-selftest.json` is intentionally absent and no provisional worker state or
master acceptance is requested.
