# THM-M-0105 statement recheck: blocked

Item: `S56-M-0105-STATEMENT`

Base revision: `0c26cec0be4f7fada10abc2c6ed0b213656d1708` (tree
`52417604a8aaccfac38ae970ef94337e6f38d033`). Rechecked on 2026-07-15
(`Asia/Shanghai`) in worker slot 60.

## Decision

The exact-statement gate remains blocked. The intake selects the intended
human formula for a smooth projective geometrically integral curve over an
arbitrary field,

`l(D) - l(K_X - D) = deg(D) + 1 - g(X)`,

where `l(E) = dim_k H^0(X, O_X(E))`. It deliberately leaves the canonical
Lean expression and environment fingerprint null. The Hartshorne Chapter IV,
Section 1, Theorem 1.3 reference is still an unaccepted lead: there is no
approved edition, page, definition chain, errata review, independent review,
or bridge to the intake's arbitrary-field geometrically integral scheme
normalization.

The proposition-changing formal choices remain unresolved: a divisor model
attached to `X`; a canonical-divisor construction and witness; `O_X(D)` and
global sections; degree and genus; finite-dimensionality; natural versus
integer codomains and coercions; projective versus proper; binder order,
universes, and the empty or nonempty curve boundary. Selecting these from
mathematical familiarity would invent part of the target rather than elaborate
the intake-selected claim.

The legacy declaration
`AwesomeTheorems.Stage1.S1_M_027.THM_M_0105_StatementShapeTarget` remains
ineligible. It existentially chooses an unconstrained
`RiemannRochDivisorData` package, so the chosen package can encode the desired
equality. It omits concrete curve-relative divisors, canonicality, `O_X(D)`,
global sections, degree, genus, projectivity, and geometric integrality.
Compiling or renaming it would substitute a broader theorem.

No target-specific authoritative input changed after the prior integrated
recheck based at `12d9becb170c3ef83e7aed51d1b3eed2a1940379`. The target
manifest, catalog and Stage0 records, legacy Stage1 blueprint, execution skill,
guidelines, intake dossier, legacy Lean module, statement probe, toolchain, and
dependency lock are byte-identical. The normalized `THM-M-0105` projections
of the rev-5.6 blueprint and execution DAG are also unchanged; intervening
projection changes belong only to unrelated targets. HEAD integrates the
prior target-local recheck plus unrelated worker evidence.

Consequently there is no canonical Lean expression whose direct imports can
be minimized or whose elaborated expression and environment can be
fingerprinted. Checked alternate transports and the removed-hypothesis,
changed-domain, changed-binder-scope, and boundary-case mutations remain
undefined rather than passed. The first failed gate is
`exact_source_statement_identity_and_concrete_lean_definition_chain`.

The predecessor `S56-M-0105-INTAKE` remains provisional `[_]`, with no master
acceptance receipt. Lifecycle remains `planned`, the vector remains
`H5 / M5 / R4`, and this statement node remains `[ ]`. This recheck claims no
statement receipt, proof, debt change, audit completion, or theorem completion.

## Pinned Lean Boundary

`StatementProbe.lean` was replayed with five direct imports. It checks only
adjacent pinned interfaces: schemes, spectra, smoothness, properness, geometric
integrality, scheme modules and their presheaves, sheaf cohomology, and module
finrank. It exited 0 and printed ten lines (820 bytes), with stdout SHA-256
`73b1db9866910a12bc451c95102136d0a4b8afc91c01e94ef747fd12e9544e29`.
It declares no canonical target, transport, axiom, or proof body. Its imports
therefore are not claimed minimal for the absent root expression.

A bounded pinned-mathlib search again found no algebraic-geometry
Riemann-Roch, Cartier or Weil divisor, canonical or dualizing divisor or
sheaf, or arithmetic-genus interface. Existing scheme-module and
sheaf-cohomology APIs are substrate only.

The pinned environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake
`5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` at tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was reused read-only. No dependency update,
build, clone, fetch, or other `.lake` mutation was run.

## Validation Evidence

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0105` | 0 | rank 27, planned, legacy artifacts unaccepted, theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base and tree match this record |
| `git diff --name-status 12d9becb170c3ef83e7aed51d1b3eed2a1940379..HEAD --` followed by the recorded static target-input path list; projection hashes from `sed` and `jq -S` | 0 | static target inputs and normalized target projections are unchanged; the prior recheck is now integrated |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0105/StatementProbe.lean` | 0 | ten stdout lines, 820 bytes, SHA-256 `73b1db98...4e29`; nine adjacent APIs elaborated and no canonical target was declared |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions above |
| pinned mathlib `status --short` and `rev-parse HEAD 'HEAD^{tree}'` | 0 | dependency worktree clean at the revision and tree above |
| bounded exact-topic search in pinned mathlib | 1 (expected no match) | no algebraic Riemann-Roch/divisor/canonical-sheaf/genus interface located |
| `rg -n --pcre2 '\b(sorry\|admit\|sorryAx\|axiom\|constant\|opaque\|unsafe\|implemented_by\|native_decide\|proof_wanted)\b' Stage1_Instances/THM-M-0105 --glob '*.lean'` | 1 (expected no match) | no prohibited construct occurrence |

The structured companion records the exact command results, fingerprints,
four undefined mutation classes, and empty receipt sets. Final JSON parsing,
scoped invariant checks, whitespace checks, and self-test absence are run after
both artifacts are written.

## Retry Condition And Boundary

Retry after the intake is master-accepted and an accountable source reviewer
preserves and approves an immutable exact statement and definition chain,
including the arbitrary-field bridge. Then encode only that reviewed claim
using concrete Lean objects, minimize its imports, serialize and hash its
elaborated expression and environment, compile every credited transport, and
execute all four mutation classes.

This is fresh current-HEAD target-scoped blocker evidence only. It does not
satisfy `S56-M-0105-STATEMENT`, propose worker `[_]`, change scheduler state,
claim an elaborated target or minimal imports, or support audit completion,
theorem completion, or master acceptance. Because the requested statement
deliverable did not pass, no `.stage1-worker-selftest.json` is emitted.
