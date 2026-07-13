# Scope map

## Preserved catalog scope

The intake preserves target `THM-M-1589`, the title `线性码`, the literal gloss `线性纠错码`, the
attribution to many mathematicians, and the twentieth-century date. The importance and `已验证`
fields are catalog metadata, not source-fidelity or Lean evidence. The record names a structured
class of error-correcting codes, not one theorem.

The narrow subject boundary is finite block codes whose codewords form a linear subspace over a
finite field. That boundary does not choose a theorem about those codes.

## Candidate result families not credited

The following are materially different possible targets. None is selected or credited here:

1. Define a linear code as an `F`-linear subspace of `F^n`.
2. Represent a `k`-dimensional code as the image of a full-rank generator map.
3. Represent the same code as the kernel of a full-rank parity-check map.
4. Prove that a finite `k`-dimensional code over `F_q` has `q^k` codewords.
5. Prove that minimum distance equals the minimum Hamming weight of a nonzero codeword.
6. Put a generator or parity-check matrix into a source-specified systematic normal form.
7. Prove dual-code dimension, double-dual, orthogonality, or generator/parity-check relations.
8. Prove correctness or an error-correction guarantee for a specified encoder and decoder.

A definition cannot substitute for a theorem. Nor can one of these results silently substitute for
another.

## Proposition-changing decisions

An approved statement phase must freeze all of the following from one immutable reviewed source:

- the selected theorem, edition, exact locator, incorporated definitions, proof boundary, correction
  status, and independent review;
- the scalar field or finite field, its cardinality convention, the coordinate index type or natural
  block length, the ambient word representation, and all universes and typeclass assumptions;
- whether the code is a submodule, an image of an injective generator, a kernel of a parity-check
  map, a quotient/equivalence class, or a structure carrying these data;
- row-vector versus column-vector and transpose conventions, matrix dimensions, rank convention,
  basis choices, and equality versus equivalence of code representations;
- code dimension, cardinality, rate, Hamming weight, minimum distance, relative distance, and empty
  or singleton minimum conventions when any appears;
- whether the claim is finite, family-level, probabilistic, or asymptotic and the exact order of all
  existence and universal quantifiers;
- whether an encoder or decoder is data or asserted to exist, the corruption model, error radius,
  tie handling, termination, and correctness relation;
- the exact conclusion, every side condition, and every excluded or included degenerate case; and
- the foundation, classical-choice, finite-enumeration, computation, and trusted-boundary policy.

## Degenerate cases to resolve

- zero block length and empty coordinate types;
- zero-dimensional and full-space codes;
- the trivial field or merely field-like scalar structures versus a finite field with at least two
  elements;
- zero or one codeword and undefined minima over no distinct codeword pairs;
- zero distance, distance one, and distance greater than the block length;
- generator maps with zero-sized domains, nontrivial kernels, repeated basis data, or rank defects;
- parity-check maps with no checks, redundant checks, or non-full row rank;
- characteristic two versus arbitrary characteristic and row/column transpose conventions;
- dual codes with nontrivial self-intersection, self-orthogonal and self-dual cases; and
- decoding with zero errors, over-radius errors, ties, failure, or nontermination.

No case is excluded at intake because no proposition has been selected.

## Neighbor boundaries

- `THM-M-1585` is the broader coding-theory topic.
- `THM-M-1586`, `THM-M-1587`, and `THM-M-1588` are the Hamming, Singleton, and
  Gilbert-Varshamov bounds. Their statements and evidence do not select this root.
- `THM-M-1590`, `THM-M-1591`, and `THM-M-1592` concern cyclic, BCH, and Reed-Solomon code
  subclasses. A special-code construction cannot stand for a theorem about all linear codes.
- `THM-C-0377` is a Stage0 computer-science record about linear-code duality. It lies outside the
  rev-5.6 target set and cannot supply this target's scope or proof state.

## Formal boundary

Pinned mathlib exposes `hammingDist`, `hammingNorm`, `Hamming`, generic `Submodule` data, and
matrix-vector linear maps. The bounded intake search located no `LinearCode` abstraction or
terminal theorem under obvious lexical variants. These APIs are possible encoding ingredients
only. They do not select or prove an unidentified catalog target.

## Status

The planned vector is `[H5, M4, R4]`. The first failed theorem gate is exact target identity: the
catalog topic is not a stable proposition. Retry requires an accountable target correction or an
independently reviewed immutable source decision selecting exactly one claim and all conventions
above. Obligation-tree construction is forbidden until the statement gate freezes and mutation-
tests that claim.
