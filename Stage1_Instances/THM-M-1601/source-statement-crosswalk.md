# Source-statement crosswalk

## Repository record

| Catalog component | Repository evidence | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| Target identity | `Docs/researches/math_theorems.md`: `同态加密` | Future canonical namespace and declaration | Stable UID and subject only |
| Attribution and date | Craig Gentry, 2009 | Provenance metadata | Consistent with the first FHE construction, but not a theorem locator |
| Literal claim | `密文上的计算` | No expression | A capability slogan, not a proposition |
| Source status | `已验证` | No receipt | Explicitly untrusted metadata; no H or M credit |
| Exact premises and result | Marked `待补充` in Stage0 | Ordered binders, hypotheses, conclusion | Absent; canonical statement remains null |
| Proof and formal artifact | Marked `待补充` in Stage0 | Proof body, wrapper, or pinned dependency | Absent |

The computer-science catalog separately lists full homomorphic encryption, attributed to Gentry in
2009, with the gloss `FHE的构造`. Stage0 projects it as `THM-C-0210`; it is outside the rev-5.6 Lean
target set. It is a neighbor/duplicate subject record, not authority to replace `THM-M-1601` with a
particular construction theorem.

## Primary-source lead

Craig Gentry, "Fully Homomorphic Encryption Using Ideal Lattices," *Proceedings of the 41st ACM
Symposium on Theory of Computing* (STOC 2009), pages 169-178, DOI
`10.1145/1536414.1536440`, is a primary source-family lead. A publicly hosted ten-page copy of the
primary paper on a CMU course page was
inspected for intake discrimination (observed SHA-256
`ac2bf30d3c26c34fbae072080dd17db5f8c931d364703ad8a27a02b54b3b78a8`).

The paper does not reduce to one theorem named by the catalog. Page 169 states the evaluation
correctness equation and the compactness motivation. Page 170 gives Definitions 1-3 for
homomorphic, fully homomorphic, and leveled fully homomorphic encryption. Page 171 gives Definition
5 and Theorem 3, the bootstrapping-to-leveled-FHE result. Page 172 gives Theorem 6, correctness of
the initial ideal-lattice scheme for permitted circuits. Page 177 gives Theorem 11, a parameter
condition under which `E3` is bootstrappable. Security and final construction claims introduce
additional assumptions and reductions.

This source is not admitted as H0. The repository cites no paper, version, or exact result; no
complete theorem/premise/definition/errata crosswalk, proof-boundary audit, or independent source
review exists. The downloaded bytes and page inspection are discovery inputs only and are not added
to the repository.

## Source-family alternatives

| Source component | Prospective Lean target surface | Intake assessment |
|---|---|---|
| Evaluation correctness equation, p.169 | Key-generation and encryption executions, circuit semantics, evaluation, decryption equality or probability bound | Plausible correctness root; all algorithm, randomness, validity, and circuit binders are absent from the catalog |
| Definitions 1-3, pp.169-170 | Predicate on a scheme, permitted circuits, compactness and complexity bounds | Definitions/property classes, not by themselves a selected existence or construction theorem |
| Bootstrappability, Definition 5 and Theorem 3, p.171 | Inclusion of augmented decryption circuits and construction of a leveled FHE family | Precise theorem family; requires all construction and security boundaries, but is not selected by the catalog |
| Initial construction correctness, Theorem 6, p.172 | Rings, ideals, sampling, valid ciphertexts, permitted generalized circuits, decryption equation | Distinct scheme-specific correctness theorem |
| `E3` bootstrappability, Theorem 11, p.177 | Exact lattice parameters, inequality, noise/decryption bounds, and construction definitions | Distinct conditional technical theorem |
| Overall semantically secure FHE construction | Algorithms, correctness, compactness, security experiment, ideal-lattice and sparse-subset assumptions, reductions | Much stronger composite result; cannot be inferred from `computation on ciphertexts` |

## Pinned Lean discovery surface

| Pinned module/declaration | Possible role | Credited status |
|---|---|---|
| `Mathlib.Algebra.Ring.Hom.Defs`: `RingHom`, `map_add`, `map_mul` | Algebraic operation-preservation vocabulary | API availability only |
| `Mathlib.Logic.Function.Conjugate`: `Function.Semiconj`, `Function.Semiconj₂` | Unary/binary commuting-diagram vocabulary | API availability only |

A bounded case-insensitive search of pinned mathlib and repo-local Lean found no lexical
`homomorphic encryption`, `fully homomorphic`, `ciphertext`, `cryptosystem`, `encrypt`, or `decrypt`
declaration beyond an unrelated prose use of "decrypting". A negative lexical search is not an
exhaustive formal-candidate audit and cannot prove nonexistence under another encoding.
`IntakeProbe.lean` merely authenticates the generic APIs above at the pinned revisions.

## Required source acceptance

Before the statement phase can pass, an accountable source decision must select one proposition and
record an immutable version, stable identifier, theorem/equation/definition/section/page locator,
exact ordered premises and conclusion, incorporated definitions, proof dependencies,
errata/correction status, and independent review. The crosswalk must map every cryptosystem,
circuit, randomness, correctness, compactness, security, complexity, probability, and boundary
choice to the Lean target. Until then the literal target is `H5` because it is not one stable
proposition; the selected published theorem must receive a fresh H classification after source
correction. No machine or theorem-completion claim is legal.
