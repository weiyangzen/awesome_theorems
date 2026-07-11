# THM-M-0430 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the global Langlands reciprocity slot. The
repository phrase "Galois representations and automorphic representations correspond" names a
program, not one theorem. This intake therefore freezes the intended root as the conjectural
global reciprocity correspondence for `GL_n` over number fields, while keeping the exact
coefficient, regularity, and local-global compatibility package open for primary-source review.
It does not replace the root by global class field theory (`n = 1`) or by a proved special case.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Global Langlands reciprocity for `GL_n` over number fields | A prose claim; exact quantifiers and direction(s) must be settled at statement review |
| Galois side | Continuous semisimple `n`-dimensional `l`-adic representations of an absolute Galois group, with appropriate geometric/ramification conditions | Coefficient fields, embeddings, geometricity, and equivalence are unresolved |
| Automorphic side | Algebraic cuspidal automorphic representations of `GL_n` over the adeles | Algebraicity/regularity conventions and isomorphism classes need an exact model |
| Compatibility | Matching unramified Frobenius/Hecke characteristic polynomials and local factors; expected local-global compatibility | Frobenius convention, exceptional places, and normalization must be frozen |
| Included boundary case | `n = 1`, where global class field theory supplies the abelian model | This branch cannot prove the general root |
| Excluded claims | Arbitrary reductive groups, geometric/function-field variants, mod-`p` correspondence, and unrestricted representations | Distinct programs; none supplies root proof credit |
| Foundations | Lean 4 kernel plus pinned mathlib | Toolchain, imports, classical axioms, and TCB closure remain open |

The structured claim is in `instance.json`, source uncertainties are in
`source-statement-crosswalk.md`, and the dependent phases are recorded in `task-dag.json`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. Primary programmatic sources
have been identified but not pinned and audited premise by premise. No exact Lean expression or
adequate automorphic/Galois object model is established. The first failed theorem gate is the exact
statement gate. The theorem is not complete.

