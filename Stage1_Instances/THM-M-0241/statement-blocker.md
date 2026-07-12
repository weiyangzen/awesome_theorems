# Exact-statement gate: blocked

Item: `S56-M-0241-STATEMENT`

Theorem: `THM-M-0241`

Base revision: `85da7777da7cc5104d4bc4eaa1d947b8137ca5f5` (tree
`ae4ad4de219b61476e1ed10c008e8139247b9d77`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0241-INTAKE` has provisional worker
state `[_]`, not a master-accepted receipt. Independently, no exact Lean 4 target can be truthfully
elaborated from the authoritative repository record. That record supplies only the title
`黎曼-希尔伯特问题` (Riemann-Hilbert problem), the attribution Riemann/Hilbert and year 1900,
and the gloss `单值群与微分方程` ("monodromy group and differential equations"). It gives no
bibliography, formula, incorporated definitions, ordered binders, assumptions, conclusion, proof
boundary, correction history, or formal artifact. The catalog status `已验证` is explicitly
untrusted under rev-5.6.

The intake's discovery copy of Hilbert's Problem 21 asks for a Fuchsian differential equation with
given singular points and monodromic group. It identifies the historical inverse-monodromy problem
family, but does not establish one later correct theorem or decide among proposition-changing
variants:

- a regular-singular connection on some holomorphic vector bundle versus a Fuchsian system on the
  trivial bundle;
- arbitrary versus irreducible or otherwise restricted monodromy;
- a fundamental-group representation versus generators, conjugacy classes, or data modulo overall
  conjugacy;
- fixed singular points and the treatment of infinity versus permission to add apparent
  singularities;
- rank, regularity, resonance, determinant, pole-order, and equivalence conventions; and
- unrestricted positive existence, a restricted positive theorem, an obstruction, a
  classification, or a counterexample to unrestricted existence.

These alternatives are not interchangeable and can change the truth value. Selecting one from
mathematical memory would invent missing scope or substitute a neighboring theorem. In particular,
`THM-M-0242` separately owns Hilbert's twenty-first problem. `THM-M-1559` separately catalogs an
integrable-systems Riemann-Hilbert problem, and its legacy module encodes a contour jump interface.
Neither may supply this target's statement.

Section 5 of the rev-5.6 blueprint makes ambiguity and a missing expression fingerprint hard
blockers. There is consequently no canonical expression for which minimal imports, checked
alternate transports, or removed-hypothesis, changed-domain, changed-binder-scope, and boundary
mutations can be certified. Those mutation tests are undefined, not passed. The first failed gate
is exact source-statement identity and its definition chain. The root remains `[H5, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated using the pinned environment. Its three direct
imports expose `OnePoint ℂ`, fundamental groups, and matrix general linear groups; the file checks
a type for finite-dimensional complex monodromy representations.
It deliberately defines no differential system, bundle or connection, regular-singularity or
Fuchsian predicate, monodromy construction for such an object, realization relation, or target
theorem. Its imports are therefore discovery-only and cannot be certified minimal for a canonical
target that has not been selected.

A bounded pinned-mathlib source search found only abstract local-homeomorphism/path-lifting and
covering-space monodromy declarations for the queried Riemann-Hilbert, Fuchsian, regular-singular,
and monodromy terms. It found no inverse-monodromy realization statement or corresponding
differential-equation interface. This is narrow feasibility evidence, not the downstream anchor
audit and not a proof of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `Formalizations/Lean/.lake`
symlink points to the canonical pinned artifacts and was used read-only. No `lake update`,
`lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0241` | 0 | rank 941; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all && git rev-parse HEAD && git rev-parse 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| repository `rg` search for the theorem ID, Chinese name, catalog gloss, and neighboring targets | 0 | found the underspecified catalog and Stage0 records, generated target entry, and provisional intake; no exact source-selected proposition |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` and `rev-parse 'HEAD^{tree}'` | 0 each | pinned mathlib revision and tree recorded above |
| `sha256sum` over the blueprint, manifests, skill, repository source records, intake records, toolchain files, and probe | 0 | authority, environment, source, intake, and probe hashes recorded in `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0241/IntakeProbe.lean` | 0 | five adjacent punctured-sphere, fundamental-group, general-linear-group, and monodromy-representation type checks elaborated; no target theorem was stated |
| pinned-mathlib `rg` search for Riemann-Hilbert, Fuchsian, regular-singular, and monodromy declarations | 0 | only abstract local-homeomorphism/path-lifting and covering-space monodromy hits; bounded discovery evidence only |
| `python3 Stage1_Instances/THM-M-0241/check_intake.py` (before blocker files) | 0 | planned intake invariants passed with `H5/M4/R4` and six open tasks |
| the same intake checker after blocker files were added | 1 | known intake-only inventory assertion: the frozen checker accepts exactly the original nine intake files; this statement run does not rewrite historical intake evidence |
| prohibited-construct `rg` scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0241/statement-blocker.json` and scoped `jq -e` invariant check | 0 each | blocker JSON parses; identity, null target/imports, undefined mutations, unchanged `H5/M4/R4`, false completion flags, and no-self-test gate agree |
| `git diff --check -- Stage1_Instances/THM-M-0241` and no-index checks for both new files | 0 / 1 each | no whitespace diagnostics; no-index exit 1 is the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition And Status Boundary

The integration lane must first master-accept the intake dependency. Accountable reviewers must
then preserve and hash an immutable primary or authoritative source, select one exact true
positive, restricted, obstruction, classification, or counterexample proposition, transcribe all
incorporated definitions, ordered binders, hypotheses, conclusions, exceptional cases, proof
boundary, corrections, and errata, reconcile the duplicate-target boundary, and independently
approve the source-to-target mapping.

A later statement worker can then encode that same claim with concrete Lean definitions, minimize
its pinned imports, serialize and hash the elaborated expression and environment, compile every
credited transport, and run all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
