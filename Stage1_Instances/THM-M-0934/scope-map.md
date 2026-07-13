# Scope map

## Frozen identity

| Field | Intake value | Status |
|---|---|---|
| repository ID | `THM-M-0934` | frozen for the current rev-5.6 manifest |
| execution item | `S56-M-0934-INTAKE`, rank 1473 | frozen |
| catalog name | `Erdős-Heilbronn猜想` | frozen as received wording |
| catalog gloss | `子集和的大小下界` | frozen literally; not an exact proposition |
| attribution/date | Paul Erdos / Hans Heilbronn, 1964 | untrusted catalog metadata |
| lifecycle | `planned`, uniform `L0 / rework_required` | frozen |

The current theorem ID must travel with the name and gloss. A historical pre-dedup repository
revision used bare `THM-M-0934` for both this target and Alon-Tarsi; therefore the ID alone is not
source identity for legacy discovery.

## Candidate readings not credited

No item below is selected as the canonical statement at intake.

1. **All-subset sums.** For a finite set `A`, form the sums of every subset of `A` and bound the
   cardinality of that set. This is a literal reading of the catalog gloss, but it is not the usual
   Erdos-Heilbronn restricted-addition problem.
2. **Restricted one-set pair sums.** For prime `p` and `A` in `Z/pZ`, form sums `a + b` with
   `a, b` in `A` and `a != b`, and prove the conventional bound
   `min(p, 2 * |A| - 3)` with an explicitly chosen arithmetic convention.
3. **Restricted two-set pair sums.** For nonempty `A, B` in `Z/pZ`, form `a + b` with `a` in `A`,
   `b` in `B`, and `a != b`, and prove the later bound `min(p, |A| + |B| - 3)`.
4. **Restricted h-fold sums.** Choose `h` distinct elements of `A` and bound the resulting sums,
   commonly by `min(p, h * |A| - h^2 + 1)` in the prime-modulus setting. This stronger theorem
   family is closely tied to the neighboring Dias da Silva-Hamidoune target.
5. **Extensions.** Composite cyclic groups, arbitrary abelian groups, finite groups, inverse
   results, equality cases, or structural classifications are separate theorem families.

## Decisions required at statement freeze

1. Admit and independently review one exact primary statement source. Historical attribution,
   initial conjecture statement, `A = B` proof, and later `A, B` proof are distinct source roles.
2. Select all-subset sums versus restricted sums, and, for restricted sums, select one-set,
   two-set, or `h`-fold scope.
3. Fix the ambient carrier: residues represented by `ZMod p`, another finite cyclic-group model,
   or a stated generalization; freeze primality and positivity assumptions on `p`.
4. Fix `Finset`, finite `Set`, or indexed-family semantics, including duplicate handling and the
   exact cardinality operation.
5. Define the restricted sumset. For two sets, specify whether `a != b` compares elements of the
   same ambient carrier and whether ordered witnesses are deduplicated only after addition. For
   `h`-fold sums, specify subsets, embeddings, tuples, or permutations and prove their relation.
6. Freeze the arithmetic carrier for the lower bound. Integer subtraction, truncated natural
   subtraction, and side conditions such as `2 <= |A|` are not interchangeable at small sizes.
7. Decide whether the conclusion is only a lower bound, also asserts sharpness, or includes
   equality/extremizer classification.
8. Freeze ordered binders, universes, typeclass assumptions, minimal imports, foundation/TCB and
   computation profiles, alternate encodings, expression fingerprint, and statement mutations.

## Boundary cases

No boundary case is excluded at intake. Statement work must resolve `p = 0`, `p = 1`, and `p = 2`;
failure of primality; empty and singleton sets; `A = B`, `A != B`, overlap and disjointness; full
residue sets; bounds whose untruncated integer expression is negative; `h = 0`, `h = 1`, and
`h > |A|`; repeated values versus repeated witnesses; and the fact that different ordered pairs
may produce the same residue.

## Explicit exclusions

- `Finset.subsetSum`, which sums every subset, used as if it defined distinct pairwise sums.
- Cauchy-Davenport's unrestricted `A + B` bound used without a checked restricted-sum argument.
- The general two-set or `h`-fold theorem silently substituted for an unreviewed one-set target, or
  conversely the `A = B` specialization silently substituted for a general target.
- A composite-modulus, arbitrary-group, inverse, or equality-case theorem used without a source-
  approved relationship in the required direction.
- A definition, hypothesis, structure field, or witness that already contains the desired bound.
- Enumeration, native computation, a finite solver run, or a URL/title match used as proof.
- The catalog's `已验证` label used as human-source, formal-source, or kernel evidence.

## Neighbor ownership

`THM-M-0935` separately owns the Dias da Silva-Hamidoune theorem described by the catalog as a
proof of the Erdos-Heilbronn conjecture. `THM-M-0936` separately owns Cauchy-Davenport. Their
statements, proof bodies, and receipts do not transfer to this target. Any eventual use must be a
checked dependency or transport after this target's exact statement is frozen.

No canonical Lean expression, statement fingerprint, alternate transport, obligation registry,
discovery protocol, proof state, or completion state is frozen by this intake.
