# Exact-statement gate: blocked

Item: `S56-M-0564-STATEMENT`  
Theorem: `THM-M-0564`  
Base revision: `d30ab383279f10fe53d90d3c5b5421638c550b25`

## Decision

The authoritative repository wording is only `向量丛的示性类理论` ("the theory of
characteristic classes of vector bundles"). This names a mathematical subject, not a proposition
with an ordered binder list, hypotheses, and conclusion. The accepted intake accordingly records
`canonical_claim_status` as
`source_wording_is_not_a_single_proposition_target_correction_required` and keeps the machine state
at `M4`.

An exact Lean 4 target cannot be elaborated without choosing mathematics absent from the source.
At minimum, a target correction would have to fix:

- the bundle category (real, complex, oriented, stable, or another category), rank restrictions,
  and base-space hypotheses;
- the cohomology theory, coefficient ring, grading, and reduced/unreduced convention;
- a class family or a precise generic characteristic-class structure;
- whether the proposition concerns existence, uniqueness, pullback naturality, a universal class,
  normalization, a Whitney-sum formula, or another result; and
- all quantifiers, classifying or pullback maps, and boundary cases such as rank zero and empty or
  disconnected bases.

These choices produce inequivalent propositions. In particular, silently selecting a theorem
about Stiefel-Whitney, Pontryagin, or Chern classes would substitute for this target: the manifest
already schedules those subjects separately as `THM-M-0565`, `THM-M-0566`, and `THM-M-0567`.
Defining an abstract structure with the desired laws as fields and projecting a field would instead
assume the intended mathematics. Neither construction can satisfy the rev-5.6 exact-statement
gate.

No canonical declaration, formal-expression hash, alternate-encoding transport, mutation-test
credit, statement acceptance, audit completion, or theorem completion is claimed. There is no
applicable `lake env lean <target>.lean` invocation because the exact target does not exist; making
an arbitrary probe elaborate would be fake evidence rather than the assigned deliverable.

## Pinned boundary and validation

Commands ran in the worker automation clone on 2026-07-12. The existing `.lake` dependency
artifacts were read only. No update, build, clone, or fetch command was run.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0564` | 0 | Rank 612, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for `THM-M-0564`, `示性类`, and "characteristic class(es)" | 0 | Found only the broad source metadata, the intake boundary, adjacent class-family records, and generic dependency/blocker mentions; no exact proposition for this target |
| pinned-mathlib `rg` search for Chern, Stiefel-Whitney, Pontryagin, and generic characteristic-class declarations | 1 | No matching Lean source at the pinned revision (`rg` exit 1 means no match) |

## Retry condition

An accountable source reviewer must approve an immutable primary-source edition and exact
theorem/page, then freeze the bundle category, base hypotheses, coefficient cohomology, class
family, conventions, binders, hypotheses, conclusion, and degenerate cases. The correction must
also explain its non-duplication of the three adjacent class-family targets. A later statement run
can then encode the proposition with minimal pinned imports, serialize its elaborated expression,
crosswalk it to the source, and perform the required removed-hypothesis, changed-domain,
binder-scope, and boundary mutations.

The assigned statement phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
