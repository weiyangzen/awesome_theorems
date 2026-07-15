# THM-M-0124 statement recheck: blocked

Item: `S56-M-0124-STATEMENT`

Base revision: `cd9c0b0881ba3f56b9892820e7fbba665eb9efed` (tree
`00c421fc989812e85b6764775a1d009366148584`). Rechecked on 2026-07-16
(`Asia/Shanghai`) in worker slot 75.

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
cusp and divisor conventions, Jacobian versus `Pic^0`, ordered binders, boundary cases, and checked
equivalence between the pairwise and all-degree-zero-divisor forms also remain open. Choosing them
here would invent proposition-changing mathematics.

The intake crosswalk records Drinfeld's article under DOI `10.1007/BF01078845`, which is unrelated.
The bibliographic metadata for *Two theorems on modular curves*, volume 7 (1973), pages 155-156
identifies `10.1007/BF01078890` as the correction candidate. This statement-phase record does not
amend or accept the intake source locator; it flags the mismatch for accountable correction and
independent review before the crosswalk can support a canonical statement.

The predecessor intake is only provisional `[_]`, not master-accepted `[x]`. No authoritative
target input changed after the prior same-slot statement recheck. The target manifest, catalog,
Stage0 and legacy Stage1 records, execution skill, guidelines, intake dossier, legacy Lean module,
toolchain, and dependency lock are unchanged. The prior recheck is now integrated. The only
blueprint and execution-DAG delta concerns unrelated `THM-M-0594`; normalized `THM-M-0124` records
are unchanged.

The concrete pinned Lean surface also cannot encode the planned claim. It supplies congruence
subgroups, cusps, cusp orbits, and finiteness of those orbits, but the bounded local search found no
associated compactified modular curve, curve Jacobian or degree-zero Picard group, cuspidal
divisor-class construction, Abel-Jacobi map, or exact Manin-Drinfeld declaration. Mathlib's
`RingTheory.PicardGroup` and elliptic-curve Jacobian-coordinate files are not the needed geometric
object model.

The historical `AwesomeTheorems.Stage1.S1_M_043.StatementShape` cannot fill the gap. Its caller
supplies an abstract compactified-curve point type, additive target, cusp inclusion, and arbitrary
divisor-class map. It therefore assumes away the missing modular curve, Jacobian, and Abel-Jacobi
construction. Fresh elaboration succeeds, but the module explicitly labels itself
`statementShapeOnly` and says it may not mark the theorem completed.

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
| scoped source, standard, skill, intake, legacy-module, and prior-blocker inspection | 0 | source ambiguity, planned scope, exclusions, and failed exact-statement gate remain unchanged |
| scoped `git diff de3690e5c...HEAD` and normalized target-record comparison | 0 | target authorities and inputs are unchanged; integrated target evidence and unrelated `THM-M-0594` blueprint/DAG changes leave every `THM-M-0124` record unchanged |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0124/StatementProbe.lean` | 0 | four stdout lines and 310 bytes at SHA-256 `2d31e6...93547`; empty stderr; concrete cusp substrate only |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean AwesomeTheorems/Stage1/S1_M_043.lean` | 0 | 17 stdout lines and 1,296 bytes at SHA-256 `0f9cf6...fe11`; empty stderr; abstract discovery surface only |
| Lean/Lake version and pinned dependency revision/tree/status checks | 0 | versions and revisions match the environment above; mathlib and `flt-regular` worktrees are clean |
| bounded exact-topic `rg` over pinned mathlib and `flt-regular` | 1 per tree, expected no match | zero output; no exact target or concrete required construction was found in these bounded surfaces |
| `python3 -m json.tool` and scoped invariant assertions on this recheck JSON | 0 | current-base identity, blocked state, unchanged vector, null target/import/hash fields, four undefined mutation classes, exact two-file scope, and absent self-test agree |
| prohibited-construct scan over owned Lean files | 1, expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, `unsafe`, `implemented_by`, or `native_decide` occurrence |
| scoped `git diff --check` and per-new-file no-index checks | 0 tracked; 1 per new file, expected difference | no whitespace diagnostics; no-index exits only record that each new file differs from `/dev/null` |
| post-write dependency pin/status checks | 0 | mathlib and `flt-regular` remain clean and at the recorded immutable revisions |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test is absent because the exact-statement gate failed |

## Retry Condition And Boundary

Retry after the intake is master-accepted and accountable reviewers preserve and approve one exact
primary or approved-authoritative statement with stable theorem/page locators, incorporated
definitions, assumptions, proof boundary, corrections, errata disposition, and independent review.
The intake's Drinfeld DOI must also be corrected and independently checked. That review must fix
subgroup generality, base, cusp/divisor conventions, Jacobian or `Pic^0` target, ordered binders,
typeclass assumptions, boundary cases, and every credited alternate form. Concrete pinned Lean
constructions for the associated compactified modular curve, its Jacobian or degree-zero Picard
group, and the cuspidal divisor-class map must then exist or be supplied. A fresh worker can encode
only that reviewed proposition, minimize imports, fingerprint the expression and environment,
compile every credited transport, and execute all four mutation classes.

This is fresh current-HEAD blocker evidence only. Because the positive statement deliverable did
not pass, `.stage1-worker-selftest.json` is intentionally absent and no worker `[_]` or master
acceptance is requested.
