# THM-M-1236 rev-5.6 intake

This directory is the `planned` intake for the catalog entry "Sobolev space". The source catalog's
entire mathematical content is `广义函数空间` ("generalized-function space"). That is a concept or
family of definitions, not a truth-valued theorem. Intake therefore fails closed rather than
silently replacing it with a convenient completeness, embedding, density, or Hilbert-space result.

## Scope map

| Surface | Candidate scope | Intake boundary |
|---|---|---|
| Root claim | A theorem concerning a precisely defined Sobolev space | No theorem is present in the catalog entry |
| Parameters | domain `Omega`, scalar field, derivative order `k`, exponent `p` | All are unspecified and remain unfrozen |
| Definition | weak/distributional derivatives through order `k` belong to `L^p` | A plausible modern convention, not selected or credited |
| Possible theorem | completeness of `W^{k,p}` or Hilbert structure at `p = 2` | Mutually different propositions; choosing one is editorial invention |
| Neighbor exclusions | embedding, Poincare, trace, extension, compactness, density | Not part of this intake; embedding and Poincare have separate target IDs |
| Lean surface | repository-pinned Lean 4 and mathlib | Module and declaration remain unset until the claim is selected |

## Required statement decision

The dependent statement phase needs an authoritative amendment selecting one exact proposition and
all its parameters. It must then verify that the proposition is actually supported by a pinpointed
source rather than merely associated with Sobolev spaces. Until that decision, mutation tests,
normalized expression hashes, transports, and theorem proof work are inapplicable.

## Intake verdict

Lifecycle remains `planned`; the provisional root vector is `[H3, M4, R3]`. The first failed gate is
exact human-claim identification. This dossier is self-tested as an honest intake artifact, but the
theorem is not complete and no later phase is claimed.

## Validation

The exact commands and results are recorded in `validation.md`. They check target membership,
repository structural consistency, JSON syntax, and dossier-local references only.
