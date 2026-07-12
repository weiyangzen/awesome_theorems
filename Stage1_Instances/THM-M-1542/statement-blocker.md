# Exact-statement gate: blocked

Item: `S56-M-1542-STATEMENT`  
Base revision: `f17146df4b6c898ac25d181a1cc08d9843b0a710`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
entire source claim is the topic phrase `扭量与自对偶Yang-Mills` ("twistors and self-dual
Yang-Mills") under the name "Ward correspondence." It does not identify one theorem or freeze:

- the local or global Ward variant, the real or complex spacetime, its signature, orientation,
  compactification, and twistor-space construction;
- the gauge/structure group, principal bundle topology, connection regularity, curvature and
  Hodge-star conventions, or whether the equation is self-dual or anti-self-dual;
- finite-action, decay, framing, irreducibility, singularity, or other analytic conditions;
- the rank, determinant, stability, reality structure, and line-triviality conditions on the
  holomorphic bundle;
- the two equivalence relations and the exact conclusion, such as a set-level bijection, an
  equivalence of groupoids/categories, or only mutually inverse transforms under restrictions.

These choices yield inequivalent Ward theorems. The Stage0 record explicitly leaves precise
definitions, assumptions, proof dependencies, foundations, and machine artifacts unresolved. The
intake consequently records `statement_precision: provisional_family_not_exact_target`, a null
Lean module/expression/fingerprint, and `[H2, M4, R3]`. Selecting a Euclidean `R^4`, compactified
`S^4`, or complex-spacetime specialization here would substitute newly chosen mathematics for the
source claim rather than elaborate it exactly.

This phase therefore fails at canonical human-claim identity, before the minimal-import,
expression-serialization, checked-transport, and mutation gates in section 5.1 of the rev-5.6
standard. Statement acceptance, audit completion, and theorem completion are all false.

## Legacy Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_183.lean` was inspected as unaccepted discovery
input. Its `StatementShape` universally quantifies over a locally supplied
`WardCorrespondenceData`; that structure itself supplies the gauge theory, twistor geometry,
holomorphic-bundle predicates, reality and stability/framing predicates, and related interfaces.
`WardCorrespondenceTheorem D` is then `Nonempty (WardCorrespondence D)`. This is a useful abstract
API boundary, but it does not select the missing geometry or map its supplied predicates to a
pinpointed source theorem. Its header and synchronization record also state that it is conservative
and not a completed Ward theorem.

The legacy file elaborates in the existing pinned environment, but uses seven broad mathlib
imports. That result proves only that the old abstract module is syntactically and type-correct. It
cannot establish a minimal import for an exact target that has not been identified, an exact
expression fingerprint, or any rev-5.6 statement mutation result.

## Required unblock

An accountable source reviewer must pin an immutable primary-source text and identify its exact
theorem/prose passage, then freeze the geometric variant and every domain, binder, hypothesis,
equivalence relation, convention, and boundary case listed above. The next statement worker can
then encode that claim without broadening or specializing it, minimize pinned imports, serialize
and hash the elaborated expression, add checked transports for credited alternate encodings, and
run removed-hypothesis, changed-domain, binder-scope, and boundary-case mutations.

## Narrow validation evidence

Commands were run from this worker clone on 2026-07-12. Lean commands used only the canonical
pinned `.lake` artifacts through the clone's existing symlink. No update, build, fetch, clone, or
other mutation of `.lake` was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard valid: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | Manifest valid: 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1542` | 0 | Rank 183, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_183.lean)` | 0 | Legacy abstract boundary elaborated and printed its audit `#check` output; this is not exact-statement evidence |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | SHA-256 `651c8acc...b1d2` and `321626c8...2d81` |

Known failures are exact source-statement identity, canonical Lean target, minimal-import
determination, expression fingerprint, checked alternate transports, and all four semantic mutation
classes. The assigned phase is not self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
