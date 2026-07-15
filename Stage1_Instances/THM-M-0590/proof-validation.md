# THM-M-0590 partial proof self-test at `c93e664d`

Item: `S56-M-0590-PROOF`

Recorded: `2026-07-15T17:55:46+08:00`

Base revision: `c93e664d3a7e0383b037cfa2d5e47ba14adfb2cb`

Base tree: `d8ea21a05ed52ff43d984128352a07f479aae6e6`

## Result

Five new placeholder-free Lean declarations provide genuine, narrowly scoped
proof progress:

- `isEssentiallyNormal_of_adjoint_comp_eq_comp_adjoint` proves that the normal
  operator boundary satisfies the frozen essential-normality predicate.
- `unitaryEquivalentModuloCompacts_refl` proves reflexivity of the exact local
  unitary-equivalence-modulo-compacts relation.
- `isCompactOperator_unitary_conjugate` proves preservation of compactness by
  conjugation with a unitary equivalence.
- `isEssentiallyNormal_unitary_conjugate` proves that the frozen
  essential-normality predicate is preserved by unitary conjugation.
- `bdfInvariantEquivalence_refl` proves the exact classification equivalence on
  the diagonal boundary case, with the frozen essential spectrum and index
  definitions unchanged.

All five declarations elaborate under Lean `--trust=0`, are checked by
`assert_no_sorry`, and report exactly `propext`, `Classical.choice`, and
`Quot.sound`. They are partial boundary and forward-invariance substrate only.
No entire frozen obligation is claimed closed.

## Root Boundary

The full Brown-Douglas-Fillmore root remains open at `[H1, M4, R3]`.
`THMM0590.root_of_directional_packages` is still only a conditional composer:
it requires inhabitants of both `ForwardInvariantPackage` and
`BackwardClassificationPackage`. Neither package has a terminal body. The
remaining root cut set is therefore unchanged:

```text
M0590-B-FORWARD
M0590-T-BACKWARD
```

Pinned mathlib has compact-operator, adjoint, and ordinary-spectrum support but
no Calkin algebra, general Fredholm-index and Atkinson package, essential
spectrum API, Busby extension, or BDF classification. The frozen anchor audit
contains no exact immutable external Lean 4 candidate. No premise, axiom,
placeholder, changed convention, weaker target, or moving dependency was added.

The proof phase is not complete. This packet proposes only the worker handoff
state `[_]` for the self-tested partial source; it does not claim an accepted
scheduler transition, M0 root status, validation, release, master acceptance,
or theorem completion.

## Split Required

Twenty-five integrated unresolved root rechecks existed at this base, while the
authoritative proof item still records `attempts=0` and `children=[]` and its
obligation-tree prerequisite remains provisional `[_]`. Rev-5.6 section 10.2
requires a split after five unresolved execution ticks. The master must
reconcile the execution cursor and create dependency-legal child tasks rather
than scheduling another unchanged root-sized proof attempt.

Suitable frozen child boundaries are `M0590-S-BOUNDARY`,
`M0590-S-FOUNDATION`, `M0590-N-CALKIN`, `M0590-N-FREDHOLM`,
`M0590-L-FWD-SPECTRUM`, `M0590-L-FWD-INDEX`, `M0590-B-FORWARD`,
`M0590-C-BUSBY`, `M0590-L-EXT-CLASS`, `M0590-L-INDEX-COMPLETE`, and
`M0590-T-BACKWARD`.

## Validation

Commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` link to canonical pinned artifacts was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation was performed. All generated Lean objects were placed under `/tmp`
and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0590` | 0 | Rank 630; lifecycle `planned`; hard-statement-first lane; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0590/check_obligation_tree.py` | 0 | 17 obligations and 37 typed edges passed; denominator `2d5b17d...9a9e8`; root and both directional packages remain M4. |
| `Stage1_Instances/THM-M-0590/check_proof.sh` | 0 | `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` elaborated through `lake env lean --trust=0 -t0`; all five new declarations were sorry-free and reported axioms `[propext, Classical.choice, Quot.sound]`; final line `PASS THM-M-0590 partial proof bodies`. |
| Owned Lean prohibited-construct scan | 1 (expected) | No `sorry`, `admit`, `sorryAx`, axiom/bodyless declaration, unsafe/oracle, implementation override, or native-decision shortcut was found. |
| Repo-local exact-name Lean search outside this dossier | 1 (expected) | No unconditional root or directional-package body was found. |
| Pinned-mathlib target/API search | 1 (expected) | No BDF target or missing central Calkin, general Fredholm-index, essential-spectrum, or Busby API was found. |
| Mathlib revision/tree/status check | 0 | Revision `8a178386...eea95`, tree `bdc39a31...e5c2b`, clean dependency worktree. |
| Lean/Lake identity and executable hash | 0 | Lean 4.29.0 commit `98dc76e...740`, Lake `5.0.0-src+98dc76e`, executable SHA-256 `3e0d0d3d...28bbf`. |
| JSON parsing, receipt invariants, and scoped whitespace checks | 0 | Structured evidence parsed; source hashes, IDs, root boundary, changed paths, and worker self-test state agreed; no whitespace errors. |

The first failed proof gate remains terminal proof-body availability for
`M0590-B-FORWARD` and `M0590-T-BACKWARD`. Closing it requires the real
Calkin/Atkinson bridges, forward spectrum and index invariance, Busby
extensions, BDF extension classification, and completeness of the index
invariant. The paired JSON receipt records the exact inputs, environment,
declarations, debts, and retry boundary.
