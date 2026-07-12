# THM-M-0708 rev-5.6 intake

This directory is the `planned` rev-5.6 dossier for Rice's theorem. The manifest admits the target
at the uniform `L0 / rework_required` baseline. The source label `已验证` is untrusted metadata and
provides neither source-fidelity nor machine-proof credit.

## Frozen claim

Relative to a fixed acceptable enumeration `phi_e` of unary partial-recursive functions on natural
numbers, every extensional, nontrivial property `S` of the computed partial function has a
noncomputable index predicate `e |-> S(phi_e)`. Here extensional means that equal partial functions
receive the same truth value. Nontrivial means that `S` holds for one enumerated partial-recursive
function and fails for another.

This functional formulation makes "program behavior" precise while retaining the classical Rice
theorem. It deliberately does not cover syntax, running time, promise properties, or the two
constant semantic properties. The full boundary is recorded in `scope-map.md`.

## Intake state

| Surface | State | Boundary |
|---|---|---|
| Membership | confirmed | execution rank 749; lane `hard_statement_first_partial_verification` |
| Human source | `H1` | Rice's primary 1953 paper is identified, but exact theorem/premise/errata review is not accepted |
| Lean target | `M4` | no exact declaration is selected or elaborated; mathlib's partial-recursive code API is discovery only |
| Readability | `R3` | scope and crosswalk exist; no node-by-node proof reconstruction exists |
| Lifecycle | `planned` | no accepted execution state and `theorem_complete=false` |

The dependent statement phase must choose and elaborate an exact predicate-computability encoding,
freeze the acceptable-numbering assumptions, and check all claimed transports. The subsequent
anchor audit must search and classify formal proof candidates without importing proof credit from
the presence of computability definitions alone.

## Validation

`intake-validation.md` records the exact preflight and dossier checks run on base revision
`2ff2721a0184cf5f856054cb7d46b10dbc703f5a`. They validate target membership, JSON syntax, required
intake fields, local references, and clean patch formatting. They do not validate a Lean statement
or theorem proof.
