# THM-M-0124 statement recheck: blocked

Item: `S56-M-0124-STATEMENT`

Base revision: `6ee4e043011799c8a8d6f7f5a2b68dd5fb819679` (tree
`8e7811b64a8ad5298ec20aa3f40898f299dce655`). Rechecked on 2026-07-15
(`Asia/Shanghai`) in worker slot 80.

## Decision

The exact-statement gate remains blocked. The repository catalog names the Manin-Drinfeld theorem
but describes only unspecified "properties of Heegner points on elliptic curves." That is a
different topic and is not a proposition that can be elaborated as this named theorem.

The planned intake instead identifies the standard theorem family: a degree-zero divisor supported
on the cusps of a modular curve attached to a congruence subgroup has torsion class in its
Jacobian, with pairwise cusp differences intended as an equivalent generator form. That family is
only prose-frozen. The cited Manin and Drinfeld papers still lack an accepted theorem/page
transcription, exact hypotheses and generality, incorporated definition chain, translation and
errata review, and independent source review. The arithmetic base, geometric-versus-rational cusp
and divisor conventions, Jacobian versus `Pic^0`, ordered binders, boundary cases, and checked
equivalence between the pairwise and all-degree-zero-divisor formulations remain open. Selecting
these proposition-changing conventions here would invent missing mathematics.

The predecessor intake is only provisional `[_]`, not master-accepted `[x]`. No authoritative
target input changed after the integrated slot72 statement recheck. The target manifest, catalog,
Stage0 and legacy Stage1 records, execution skill, guidelines, intake dossier, legacy Lean module,
toolchain, dependency lock, and the `THM-M-0124` checklist entries remain unchanged. Current HEAD
integrates the prior target recheck and state or evidence for unrelated targets only.

The pinned Lean closure still cannot express the planned claim concretely. It supplies congruence
subgroups, cusps, cusp orbits, and finite cusp orbits. A bounded search of pinned mathlib and
`flt-regular` found no Manin-Drinfeld declaration, associated compactified modular curve, curve
Jacobian or degree-zero Picard group, cuspidal divisor-class construction, or Abel-Jacobi map.
Mathlib's elliptic-curve `Jacobian` modules concern Jacobian coordinates for Weierstrass curves, not
the Jacobian variety of an arbitrary compactified modular curve.

The historical `AwesomeTheorems.Stage1.S1_M_043.StatementShape` cannot fill the gap. Its caller
supplies an abstract compactified-curve point type, additive target, cusp inclusion, and arbitrary
divisor-class map. It therefore assumes away the missing modular curve, Jacobian, and Abel-Jacobi
construction. Fresh elaboration succeeds, but the module explicitly reports a
`statementShapeOnly` boundary and that it may not mark the theorem completed.

Consequently there is no truthful canonical Lean expression, minimal canonical import set,
expression hash, environment fingerprint, checked alternate-form transport, or meaningful
removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutation suite. The first
failed gate remains `exact_source_statement_and_concrete_formal_object_model`. Lifecycle stays
`planned`, root debt stays `H1 / M4 / R4`, and the statement node stays `[ ]`. No proof, receipt,
debt change, audit completion, theorem completion, or master acceptance is claimed.

## Pinned Lean Boundary

`StatementProbe.lean` has one direct import,
`Mathlib.NumberTheory.ModularForms.Cusps`. Fresh elaboration emitted four API types and 310 bytes at
SHA-256 `2d31e6ab6b2dd3018738af639c7e84a7dcea236e34a0dbe4fca31b6bffa93547`; stderr was
empty. Its congruence-subgroup cusp-orbit finiteness example elaborated too. This establishes only
that the pinned installation and adjacent cusp substrate work. The import is minimal for this
probe, not for the absent canonical target.

The legacy discovery module freshly elaborated with 17 stdout lines and 1,296 bytes at SHA-256
`0f9cf61b87219c06e8e2f14479e2ad675a4f097e0447d7a3bf8434833c01fe11`; stderr was empty.
It receives discovery credit only.

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
| scoped standard, source, dossier, legacy-module, and prior-blocker inspection | 0 | the source ambiguity, planned scope, exclusions, and failed exact-statement gate remain unchanged |
| scoped `git diff 69f012f97...HEAD` over authoritative target inputs | 0 | catalog, manifest, intake, legacy Lean, toolchain, lock, skill, and guidelines are unchanged; only the prior target recheck was integrated, while blueprint/DAG changes concern unrelated nodes |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0124/StatementProbe.lean` | 0 | 4 stdout lines and 310 bytes at SHA-256 `2d31e6...93547`; empty stderr; concrete cusp substrate only |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean AwesomeTheorems/Stage1/S1_M_043.lean` | 0 | 17 stdout lines and 1,296 bytes at SHA-256 `0f9cf6...fe11`; empty stderr; abstract discovery surface only |
| Lean/Lake version and pinned dependency revision/tree/status checks | 0 | versions and revisions match the environment above; mathlib and `flt-regular` worktrees are clean |
| bounded exact-topic `rg` over pinned mathlib and `flt-regular` | 1 per tree, expected no match | zero output; no exact target or concrete required construction was found in these bounded surfaces |
| `python3 -m json.tool` and scoped invariant assertions on the recheck JSON | 0 | current-base identity, blocked state, unchanged vector, null target/import/hash fields, four undefined mutation classes, exact two-file scope, and absent self-test agree |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, `unsafe`, `implemented_by`, or `native_decide` occurrence |
| scoped `git diff --check` and per-new-file no-index checks | 0 tracked; 1 per new file, expected difference | no whitespace diagnostics; no-index exits only record that each new file differs from `/dev/null` |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test is absent because the exact-statement gate failed |

## Retry Condition And Boundary

Retry after the intake is master-accepted and accountable reviewers preserve and approve one exact
primary or approved-authoritative statement with stable theorem/page locators, incorporated
definitions, assumptions, proof boundary, corrections, errata disposition, and independent review.
That review must fix subgroup generality, base, cusp/divisor conventions, Jacobian or `Pic^0`
target, ordered binders, typeclass assumptions, boundary cases, and every credited alternate form.
Concrete pinned Lean constructions for the associated compactified modular curve, its Jacobian or
degree-zero Picard group, and the cuspidal divisor-class map must then exist or be supplied. A fresh
worker can encode only that reviewed proposition, minimize imports, fingerprint the expression and
environment, compile every credited transport, and execute all four mutation classes.

This is fresh current-HEAD blocker evidence only. Because the positive statement deliverable did
not pass, `.stage1-worker-selftest.json` is intentionally absent and no worker `[_]` or master
acceptance is requested.
