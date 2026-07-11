# THM-M-0431 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the local Langlands correspondence. The
manifest label is too broad to denote every local Langlands conjecture, so this intake fixes the
classical, proved correspondence for `GL_n` over non-archimedean local fields of characteristic
zero. It does not claim a correspondence for arbitrary reductive groups, positive-characteristic
fields, or any repo-local proof.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Local Langlands correspondence for `GL_n(F)`, `F` a finite extension of `Q_p`, for every `n >= 1` | A prose-level target; Lean elaboration belongs to the dependent statement phase |
| Representation side | Isomorphism classes of irreducible admissible smooth complex representations of `GL_n(F)` | Quotients, smoothness, admissibility, and irreducibility need an exact Lean object model |
| Parameter side | Equivalence classes of `n`-dimensional Frobenius-semisimple Weil-Deligne representations of `W_F` over `C` | Weil group, topology/continuity, monodromy, and equivalence are not yet encoded here |
| Characterization | Compatibility with local class field theory at `n = 1`, twists, duals, central characters, and local `L`- and epsilon-factors | The definitive uniqueness axiom set and normalizations require primary-source audit |
| Excluded claims | General reductive-group LLC, local Shimura conjectures, geometric LLC, mod-`l`/mod-`p` LLC, and positive-characteristic variants | Separate theorems; none may supply proof credit for this root |
| Foundations | Lean 4 kernel plus pinned mathlib and an accepted classical/choice/quotient policy | Exact toolchain, imports, axioms, and TCB remain open |

The mandatory architecture begins with object definitions and quotient/equivalence relations, then
the bijection, then its normalization and factor-compatibility laws. No branch is considered closed.
The structured claim is in `intake.json`; source-to-statement uncertainties are recorded in
`source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. `H1` records identified primary
proof sources without a completed edition/page/assumption/errata audit. `M4` records that no exact
Lean expression or adequate object model has been identified. The first failed theorem gate is the
exact Lean statement gate. The theorem is not complete.

## Validation

The commands in `validation.md` check manifest membership, repository-standard consistency, JSON
syntax, dossier references, and prohibited proof tokens. They provide no kernel-proof evidence.

