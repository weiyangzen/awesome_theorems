# THM-M-0429 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for Brauer's theorem on Artin L-functions. It does
not inherit proof credit or accepted state from the legacy `S1-M-082` artifact.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Meromorphic continuation to the complex plane of the Artin L-function attached to a finite-dimensional complex representation of a finite Galois group | Exact conventions and Lean elaboration belong to the dependent statement phase |
| Arithmetic data | A finite Galois extension of number fields, its finite group, representations, inertia invariants, and Frobenius classes | The concrete Lean object model is not frozen |
| Character reduction | Brauer induction: expression of a character as an integral combination of characters induced from one-dimensional characters of subgroups | Architecture only; no formal reduction is credited |
| Analytic bridge | Identification of induced one-dimensional factors with Hecke/abelian L-functions and continuation of their products and quotients | Source assumptions and Lean bridges remain open |
| Pole behavior | Meromorphic continuation, not Artin's stronger holomorphy conjecture for nontrivial irreducible characters | Holomorphy is explicitly excluded from the root claim |
| Foundations | Lean 4 kernel plus a versioned mathlib and any accepted pinned dependency | Toolchain, imports, classical policy, and trust closure remain open |

The legacy module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_082.lean` is discovery material
only. Its abstract data and checked local anchors neither define the standard Artin L-function nor
prove the root theorem. The source relationship and statement ambiguities are recorded in
`source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the exact Lean statement gate: no canonical elaborated expression, environment fingerprint,
source-pinned convention set, transports, or mutation results have been accepted. The theorem is
not complete.

## Validation

The commands in `validation.md` establish target membership, repository-standard consistency, JSON
syntax, and dossier-local hygiene only. No kernel proof or source-fidelity acceptance is claimed.
