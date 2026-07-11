# THM-M-1024 rev-5.6 intake

This is the `planned` instance for the Levy-Khintchine representation. The manifest's untrusted
`已验证` label supplies no proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Equivalence between infinite divisibility of a Borel probability law on finite-dimensional real Euclidean space and existence of its Levy triplet | The exact Lean types and normalized expression remain open |
| Analytic identity | Characteristic function with `+i` Fourier sign, Gaussian coefficient `1/2`, and unit-ball truncation | Bochner integration, measurability, and integrability encodings remain open |
| Triplet | Drift vector, symmetric positive-semidefinite covariance operator, and Levy measure | Existence is root content; convention-relative uniqueness is required proof scope |
| Boundary cases | Dirac and Gaussian laws; zero Levy measure or zero covariance | Dimension zero must be tested; subprobabilities and infinite-dimensional laws are excluded |
| Transports | One-dimensional specialization, convolution-semigroup form, alternate truncations | Candidate architecture only; no transport is credited |
| Foundations | Lean 4 kernel with pinned mathlib and an explicit classical measure/integration profile | Toolchain, imports, axioms, and transitive TCB remain open |

The root must cover both directions of the equivalence and the convention-relative uniqueness of
the triplet. A result merely defining the exponent, proving one direction, or handling only compound
Poisson laws is not a substitute.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The source theorem is pinpointed,
but its immutable artifact, premise-level crosswalk, errata status, and independent review are not
accepted. The first failed gate is the exact Lean statement gate: no declaration, elaboration hash,
environment fingerprint, checked transport, or mutation test exists. The theorem is not complete.

## Open task DAG

`STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
Each node remains dependent on master acceptance of this intake. Exact follow-up boundaries are
recorded in `source_statement_crosswalk.md`.

## Validation

The commands in `validation.md` establish manifest membership, repository-standard consistency,
JSON syntax, reference integrity, and clean formatting only. No Lean artifact is introduced in the
intake phase and no kernel result is claimed.
