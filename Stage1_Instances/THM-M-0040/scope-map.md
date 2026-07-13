# Scope map

## Frozen identity

| Field | Intake value | Status |
|---|---|---|
| repository ID | `THM-M-0040` | frozen for the rev-5.6 manifest |
| execution item | `S56-M-0040-INTAKE`, rank 1518 | frozen |
| catalog name | `阿密苏尔-列维茨基定理` | frozen as received wording |
| catalog gloss | `矩阵环满足的多项式恒等式` | frozen literally; not a binder-complete proposition |
| attribution/date | Shimshon Amitsur / Alexander Levitzki, 1950 | untrusted catalog metadata; coauthor mismatch open |
| lifecycle | `planned`, uniform `L0 / rework_required` | frozen |

The target identity includes the current ID, name, and gloss. A famous theorem name or a source
paper with several related theorems is not enough to select an exact root by itself.

## Candidate readings not credited

No item below is selected as the canonical statement at intake.

1. **Original standard identity.** For each positive `n`, the alternating standard polynomial in
   `2*n` variables vanishes on all `n x n` matrices over a field. This is Theorem 1 of the inspected
   1950 paper.
2. **General coefficient-ring identity.** The same alternating evaluation vanishes for matrices
   over a commutative ring. This familiar later scope is broader than the inspected paper's stated
   field context and requires a source-approved relationship.
3. **Minimal-degree theorem.** The matrix algebra has no nonzero polynomial identity of degree less
   than `2*n`, and the standard identity realizes degree `2*n`. The lower-bound and exact
   qualification of "identity" are additional claims.
4. **Uniqueness/classification package.** Minimal multilinear identities in `2*n` variables are
   scalar multiples of the standard polynomial, possibly together with the paper's wider
   classification and its small characteristic-two exceptions.
5. **General-algebra extensions.** Simple, semisimple, or arbitrary finite-dimensional algebras
   satisfy related identities. Those are not silently the matrix-ring root.

## Decisions required at statement freeze

1. Admit and independently review the exact source clause owned by this catalog target: standard
   identity alone, minimal degree, uniqueness, or a declared conjunction.
2. Fix the coefficient domain: the paper's field, an arbitrary commutative ring, or another class;
   map any generalization in the required direction.
3. Fix the size binder and index model, including whether `n` is positive and whether matrices are
   indexed by `Fin n` or arbitrary finite types of cardinality `n`.
4. Define the standard polynomial exactly: `2*n` ordered variables, the permutation type, sign
   convention, coefficient embedding, noncommutative product order, and finite sum.
5. Decide whether the target is an evaluated identity for every matrix tuple, an equality in a free
   noncommutative polynomial algebra, or both with a checked transport.
6. If minimality is included, define polynomial identity, nonzero polynomial, total degree,
   coefficient domain, admissible number of variables, and every finiteness or characteristic
   hypothesis.
7. Resolve the catalog's Alexander/J. Levitzki attribution discrepancy, paper edition, corrections,
   errata, and the proof-source role of Levitzki's earlier lower-bound paper.
8. Freeze ordered binders, universes, typeclasses, minimal imports, foundation/TCB/computation
   profiles, alternate encodings, expression fingerprint, and required statement mutations.

## Boundary cases

No boundary case is excluded at intake. Statement work must resolve `n = 0`, `n = 1`, fields versus
zero or nontrivial rings, characteristic two (where `+1` and `-1` can coincide), finite fields,
repeated matrix arguments, zero and identity matrices, the empty ordered product, and whether the
size theorem quantifies one `n` or all positive `n`. If minimality or uniqueness is included, it
must also map the paper's exceptional cases for small matrix sizes over the prime field of
characteristic two.

## Explicit exclusions

- Cayley-Hamilton, which evaluates each matrix's characteristic polynomial, is a different identity.
- A determinant alternation formula or generic fact that an alternating map vanishes on repeated
  inputs does not establish the matrix-ring standard identity.
- The Hopkins-Levitzki theorem concerns Noetherian and Artinian module conditions and is unrelated.
- A fixed-size example, the commutative `n = 1` case, diagonal matrices, or commuting matrices is
  not the general matrix-algebra theorem.
- A definition, structure field, premise, or certificate that assumes the desired identity supplies
  no proof.
- A title match, URL, `#check`, finite computation, or the catalog's `已验证` label supplies no H or
  M credit.

## Neighbor ownership

`THM-M-0039` separately owns the catalog's broad Kaplansky/PI-ring structure entry.
`THM-M-0041` separately owns Cayley-Hamilton. Their statements, proof bodies, and receipts do not
transfer to this target; any later use must be an exact checked dependency after statement freeze.

No canonical Lean expression, statement fingerprint, alternate transport, obligation registry,
discovery protocol, proof state, or completion state is frozen by this intake.
