# Scope map

## Frozen identity

| Field | Intake value | Status |
|---|---|---|
| repository ID | `THM-M-0933` | frozen |
| execution item | `S56-M-0933-INTAKE`, rank 1472 | frozen |
| catalog name | `Olson定理` | frozen as received wording |
| catalog gloss | `有限阿贝尔群的Davenport常数` | frozen literally |
| attribution | John Olson, 1969 | untrusted catalog metadata, now supported only as a source lead |
| lifecycle | `planned`, uniform `L0 / rework_required` | frozen |

The title and gloss identify a zero-sum/Davenport theorem family, not one proposition. Importance
`高` and status `已验证` are inventory metadata, not human-source or kernel evidence.

## Candidate roots not credited

1. **Olson's p-group equality.** For a finite abelian p-group with invariant factors
   `G = C_(p^a1) direct-sum ... direct-sum C_(p^ar)`, the Davenport constant is
   `D(G) = 1 + sum_i (p^ai - 1)`. A modern proof labels this Theorem 1.5 and attributes the result
   to Olson and independently van Emde Boas-Kruyswijk.
2. **Rank-at-most-two equality.** For `G = C_m direct-sum C_n` with `m | n`, the usual equality is
   `D(G) = m + n - 1`. Modern surveys discuss this beside the p-group result, but the catalog does
   not distinguish the two.
3. **Homocyclic rank-two special case.** `D((Z/nZ)^2) = 2n - 1`, often called a classical Olson
   result. This is only one rank-two specialization and must not replace a p-group theorem.
4. **Forcing form.** Every sequence over the selected group of length at least the displayed bound
   contains a nonempty zero-sum subsequence. This requires a checked equivalence to the selected
   minimum/extremal definition of `D(G)`.
5. **Maximum zero-sum-free form.** The largest length of a zero-sum-free sequence is one less than
   `D(G)`. This is related but uses a maximum, existence, and convention choices.

These candidates are not interchangeable without checked transports and source approval. The
title must also not be confused with the Olson constant of zero-sum-free *sets* or the strong/large
Davenport constants.

## Decisions required before statement freeze

1. Select and independently approve the exact Olson source result: p-groups, rank at most two,
   `(Z/nZ)^2`, another theorem, or an explicitly modeled composite.
2. Define a sequence as a list, multiset, or finitely supported multiplicity function, including
   whether order is quotiented out and repetition is allowed.
3. Define `D(G)` precisely: least positive length forcing a nonempty zero-sum subsequence, maximum
   zero-sum-free length plus one, or another checked equivalent.
4. Fix additive versus multiplicative notation and whether subsequences preserve order or are
   submultisets. The empty subsequence must not witness zero sum.
5. Fix the finite abelian group presentation. For a decomposition, specify ordered invariant
   factors, positivity and divisibility conditions, uniqueness up to equivalence, and how `D*(G)`
   is invariant under the chosen presentation.
6. For the p-group candidate, fix the prime, nontrivial/trivial group policy, positive versus zero
   exponents, repeated cyclic factors, and whether `Finite`, `Fintype`, or explicit equivalence data
   supplies finiteness.
7. Decide whether the target is an equality of defined constants, an upper and lower bound pair,
   or a direct forcing proposition; each proof architecture has different obligations.
8. Freeze minimal Lean imports, universes, ordered binders, hypotheses, conclusion, foundation,
   TCB, computation, freshness, and mutation profiles only after the proposition is selected.

## Boundary and degenerate cases

No case is excluded at intake. Statement work must resolve the trivial group; empty invariant-factor
index type; cyclic rank one; repeated factors; exponent one/zero encodings; prime `p = 2`; empty,
singleton, and exactly-threshold sequences; a sequence containing zero; all-zero sequences;
duplicate terms; a zero-sum subsequence of length one; and the distinction between a nonempty
zero-sum subsequence and the always-zero empty sum.

It must also mutation-test a non-p-group, a group of rank three, a threshold shortened by one, the
removal of nonemptiness, changed binder scope, and list-versus-multiset transports. These changes
are proposition-relevant and cannot be disposed of by theorem-name similarity.

## Exclusions and neighbor ownership

- `THM-M-0931` owns the Erdős-Ginzburg-Ziv theorem, which requires a zero-sum subsequence of a
  specified length. It is not the ordinary Davenport constant.
- `THM-M-0932` owns the broad zero-sum-sequence topic. Its general vocabulary supplies no inherited
  statement or proof credit.
- `THM-M-0936` owns Cauchy-Davenport, a sumset-cardinality theorem over a prime cyclic group.
- The Olson constant (maximum zero-sum-free subset size), strong Davenport constant, large
  Davenport constant for nonabelian groups, EGZ constant, weighted constants, and multi-wise
  constants are distinct invariants.
- A structure theorem for finite abelian groups, generic multiset sum, or EGZ theorem is substrate,
  not an Olson/Davenport proof.
- A finite search, computed small-group table, citation, title match, or the untrusted `已验证` label
  cannot establish the root.

No canonical expression, expression fingerprint, checked transport, obligation registry,
discovery protocol, graph, proof state, or completion claim is frozen by this intake.
