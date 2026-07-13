# Scope map

## In scope at intake

- Repository UID `THM-M-1586`, execution rank 1208, and item `S56-M-1586-INTAKE` only.
- The classical Hamming or sphere-packing upper-bound family for finite error-correcting codes.
- The literal catalog wording, its provenance, source candidates, proposition-changing variants,
  adjacent pinned Lean APIs, and the exact blockers for selecting a canonical target.
- A `planned` lifecycle with no accepted evidence and six open downstream tasks.

## Proposition-changing choices left open

| Dimension | Choices that an accepted source must settle |
|---|---|
| Alphabet | binary words, a constant finite alphabet of size `q`, dependent coordinate alphabets, or a finite field |
| Code object | arbitrary finite set or subset of words, linear subspace/submodule, encoder image, or an extremal function such as `A_q(n,d)` |
| Word model | `Fin n -> α`, another finite coordinate type, vectors, or Hamming's historical block notation |
| Separation parameter | minimum pairwise distance `d`, guaranteed correction count `t`, or both with an exact relationship |
| Ball radius | `t`, `floor ((d - 1) / 2)`, or another source-defined integer convention |
| Ball volume | an actual finite Hamming ball, the constant-alphabet sum `sum choose(n,i)*(q-1)^i`, or the binary specialization |
| Conclusion | cardinality packing inequality, upper bound on an extremal code size, linear dimension inequality, perfect-code equality case, or asymptotic rate bound |
| Arithmetic | natural, integer, rational, or real casts; multiplication versus division; floors, ceilings, and truncated subtraction |
| Quantifiers | order and dependencies among alphabet, length, code, distance/radius, and nontriviality assumptions |
| Foundation | constructive finite counting versus classical finite-set decisions, choice, quotients, finite fields, or real asymptotics |

The standard finite q-ary formula is a useful candidate discriminator, not the canonical claim:

```text
|C| * sum_{i=0}^t choose(n,i) * (q - 1)^i <= q^n,
where pairwise codeword distance is at least 2*t + 1.
```

An equivalent-looking formulation using minimum distance `d` requires a checked relationship
between `t` and `floor ((d - 1) / 2)`, including natural-number boundary behavior. A linear-code
corollary additionally needs a field and the transport `|C| = q^k`. None is selected at intake.

## Degenerate and boundary cases to resolve

- Empty alphabets and alphabet cardinality `q = 0` or `q = 1`.
- Zero block length and empty coordinate types.
- Empty and singleton codes, and whether a minimum over distinct pairs exists.
- Radius `t = 0`, minimum distance `d = 0` or `d = 1`, and `d > n`.
- Radius greater than the block length and truncated finite sums.
- Natural subtraction in `q - 1` and `d - 1`, plus all casts used by division-style statements.
- Pairwise separation stated with `<`, `<=`, `2*t < d`, or `2*t + 1 <= d`.
- Equality/perfect-code cases, which are not automatically part of an upper-bound theorem.
- Asymptotic relative-distance endpoints, logarithm base, limit versus limsup, and rate conventions.

No case is excluded yet: excluding it before an exact source is selected would change the target.

## Explicitly excluded substitutions

- `THM-M-1585` coding theory, `THM-M-1587` Singleton bound, `THM-M-1588`
  Gilbert-Varshamov bound, or `THM-M-1589` linear-code theory used to select or close this root.
- The Stage0 computer-science duplicate record used as accepted source or proof evidence.
- A binary bound presented as the q-ary theorem, or a linear-code corollary presented as the
  arbitrary-code theorem, without an accepted checked transport.
- The Hamming-code construction or the perfect-code equality case substituted for the packing
  upper bound.
- A generic disjoint-union cardinality lemma, Hamming-distance triangle inequality, or metric-ball
  fact presented as the complete coding theorem.
- A hypothesis, structure field, axiom, opaque declaration, or unsafe mechanism that assumes the
  desired packing inequality.
- Brute-force enumeration or numerical testing presented as a universal theorem proof.
- The catalog's `已验证` label or an unpinned URL presented as source or kernel closure.

## Neighbor and duplicate boundaries

| Record | Boundary |
|---|---|
| `THM-M-1585` coding theory | broader topic; it supplies no root statement or proof credit |
| `THM-M-1587` Singleton bound | distinct puncturing/projection upper bound |
| `THM-M-1588` Gilbert-Varshamov bound | paired covering/existence lower bound, not the packing upper bound |
| `THM-M-1589` linear codes | may supply a specialization's structures but does not select the arbitrary versus linear root |
| `THM-C-0371` Singleton bound | outside rev-5.6 and unrelated to Hamming-root acceptance |
| computer-science Hamming-bound row | likely duplicate metadata outside the rev-5.6 target set; no state or evidence is inherited |
| `THM-C-0380` Hamming code | construction target, not the bound; outside rev-5.6 |

## Frozen status boundary

`H1` records a mathematically established theorem family and bibliographically identified 1950
primary-source lead, not source-fidelity acceptance. `M4` records that no source-identical usable
formal artifact is known for an unselected root. `R4` records that no source-faithful readable
reconstruction can be attached before target selection. The statement, anchor audit, obligation
tree, proof, validation, and release phases remain open.
