# THM-M-0105 statement recheck: blocked

Item: `S56-M-0105-STATEMENT`

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff` (tree
`24acf86e69ab2e6fca9480c6269b6429874ba295`). Rechecked on 2026-07-16
(`Asia/Shanghai`) in worker slot 63.

## Decision

The exact-statement gate remains blocked. The intake selects the intended
human formula for a smooth projective geometrically integral curve over an
arbitrary field,

`l(D) - l(K_X - D) = deg(D) + 1 - g(X)`,

where `l(E) = dim_k H^0(X, O_X(E))`. It deliberately leaves the canonical
Lean expression and environment fingerprint null. Hartshorne, Chapter IV,
Section 1, Theorem 1.3 remains an unaccepted source lead: there is no approved
edition and page, definition chain, errata disposition, independent review,
or bridge to the intake's arbitrary-field geometrically integral scheme
normalization.

The proposition-changing choices are still unresolved: a divisor model
attached to `X`; a canonical-divisor construction and witness; `O_X(D)` and
global sections; degree and genus; finite-dimensionality; natural versus
integer codomains and coercions; projective versus proper; binder order,
universes, and the empty or nonempty curve boundary. The pinned dependency
closure exposes adjacent scheme, smoothness, properness, geometric-integrality,
module, sheaf-cohomology, and finrank interfaces, but no coherent divisor,
canonical-divisor or dualizing-sheaf, divisor-sheaf, degree, genus, or
Riemann--Roch API. Selecting abstract replacements would invent part of the
target rather than elaborate the intake-selected claim.

The legacy declaration
`AwesomeTheorems.Stage1.S1_M_027.THM_M_0105_StatementShapeTarget` remains
ineligible. It existentially chooses unconstrained `RiemannRochDivisorData`,
so the chosen package can encode the desired equality. It omits concrete
curve-relative divisors, canonicality, `O_X(D)`, global sections, degree,
genus, projectivity, and geometric integrality. Compiling or renaming it would
substitute a broader theorem.

The predecessor `S56-M-0105-INTAKE` remains provisional `[_]`, with no
master-accepted receipt. Consequently there is no canonical Lean expression
whose direct imports can be minimized or whose elaborated expression and
environment can be fingerprinted. Checked alternate transports and the
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations remain undefined rather than passed. The first failed gate is
`exact_source_statement_identity_and_concrete_lean_definition_chain`.

Lifecycle remains `planned`, the recorded vector remains `H5 / M5 / R4`, and
this statement node remains `[ ]`. This report claims no statement receipt,
proof, debt change, audit completion, or theorem completion.

## Dependency And Reuse Audit

The v2 theorem node has no direct hard parent, transitive hard ancestor,
incoming hard edge, direct reuse hint, or shared group. The required
`dependency-reuse-ledger.json` now records that empty audited closure using
schema `stage1-dependency-reuse-ledger/1.1`, observed graph SHA-256
`73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca`,
and dependency-context SHA-256
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
Its empty closure is not a mathematical independence claim, and no proof
credit is imported.

The repository validator
`scripts.stage1_execution_cron.validate_dependency_reuse_ledger` accepted the
ledger against the supplied graph digest, context, and worker base revision.

## Pinned Lean Boundary

`StatementProbe.lean` was replayed using the existing pinned artifacts. It
exited 0 and printed ten lines (820 bytes), with stdout SHA-256
`73b1db9866910a12bc451c95102136d0a4b8afc91c01e94ef747fd12e9544e29`
and empty-stderr SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
Its nine `#check` commands cover adjacent interfaces only. It declares no
canonical target, transport, axiom, or proof body, so its five imports are not
claimed minimal for the absent root expression.

A bounded pinned-source search for Riemann--Roch, Cartier or Weil divisors,
canonical divisors, dualizing sheaves, and arithmetic genus returned no match.
The pinned environment is Lean `4.29.0`, Lake `5.0.0-src+98dc76e`, and mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` at tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was reused read-only. No dependency update,
build, clone, fetch, or other `.lake` mutation was run.

## Validation Evidence

The structured JSON companion records exact commands, exit codes, input
fingerprints, four undefined mutation classes, empty receipt sets, and the
audited dependency ledger. The material results were:

| Command | Exit | Result |
|---|---:|---|
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0105` | 0 | rank 27, planned, legacy artifacts unaccepted, theorem incomplete |
| v2 ledger validation through `scripts.stage1_execution_cron.validate_dependency_reuse_ledger` | 0 | schema, graph, context, base revision, and all eight empty closure lists passed |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC LEAN_NUM_THREADS=1 lake env lean ../../Stage1_Instances/THM-M-0105/StatementProbe.lean` | 0 | ten stdout lines, 820 bytes, expected digest; nine adjacent APIs elaborated |
| bounded exact-topic search in pinned mathlib | 1 (expected no match) | no concrete algebraic-curve Riemann--Roch API located |
| prohibited-construct scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, unsafe, oracle, or proof placeholder occurrence |

The repository-wide standard and v2 DAG checks both exited 1 because their
fresh deterministic projection inventories these new target-owned JSON files,
while the checked-in authority deliberately remains unmodified in a worker
clone. A temporary generator diagnostic confirmed that the only DAG delta was
the expected addition of this ledger and this JSON recheck to the target's
`structured_json_files`; the authority file was restored byte-for-byte. This
worker may not regenerate or edit that master-owned projection. The target
manifest check, ledger validator, and narrow Lean replay above are therefore
the smallest completed passing validations for this blocked statement attempt.

## Retry Condition And Boundary

Retry after the intake is master-accepted and an accountable source reviewer
preserves and approves an immutable exact statement and definition chain,
including the arbitrary-field bridge. Then supply the missing concrete formal
interfaces, encode only that reviewed claim, minimize imports, serialize and
hash its elaborated expression and environment, compile every credited
transport, and execute all four mutation classes.

This is fresh current-HEAD target-scoped blocker evidence only. It does not
satisfy `S56-M-0105-STATEMENT`, propose worker `[_]`, change scheduler state,
claim an elaborated target or minimal imports, or support audit completion,
theorem completion, or master acceptance. Because the requested deliverable
did not pass, no `.stage1-worker-selftest.json` is emitted.
