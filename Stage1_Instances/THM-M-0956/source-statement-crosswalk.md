# Source-statement crosswalk

## Repository record and provenance

`Docs/researches/math_theorems.md:6980-6985` supplies exactly the title `Erdős-Turán构造`,
attribution Erdos/Turan, year 1941, gloss `Sidon集的构造`, importance `高`, and status `已验证`.
All six uncited lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no formula, definition, bibliography,
theorem number, assumptions, conclusion, proof boundary, correction history, reviewer, or formal
artifact.

`Docs/Stage0_Blueprint.md:26065-26090` mechanically repeats the gloss while explicitly leaving
precise definitions and premises, proof route, dependencies, alternate formulations, axioms,
machine status, and artifact links open. Rev-5.6 retains `已验证` only as untrusted metadata, resets
the target to `L0 / rework_required`, and states `theorem_complete=false`.

## Primary-source lead inspected

P. Erdos and P. Turan, "On a Problem of Sidon in Additive Number Theory, and on some Related
Problems," *Journal of the London Mathematical Society* s1-16(4) (October 1941), 212-215, DOI
`10.1112/jlms/s1-16.4.212`. Crossref confirms the title, authors, publication date, volume, issue,
and pages. A four-page scan hosted by the Alfred Renyi Institute was inspected; the observed PDF
has 671160 bytes and SHA-256
`25cc7c8de8b74149511045fa03bf32e7b885893ff4b67c7dfb9366dd70f5b091`.

The paper defines a `B_2` sequence as a strictly increasing sequence of positive integers whose
sums `a_i + a_j` for `i <= j` are all different. Its introduction studies the maximum number
`Phi(n)` of terms not exceeding `n`. Section I, printed page 213, gives the construction candidate:
for prime `p`, set

```text
a_k = 2*p*k + r_k  for k = 1, ..., p - 1,
```

where `r_k` is the unique integer satisfying `k^2 = r_k (mod p)` and `1 <= r_k <= p - 1`. It says
the terms are below `2*p^2` and proves that sums belonging to different unordered/index pairs are
unequal. The proof derives equality of the ordinary index sums and equality of sums of squares
modulo `p`, then obtains equality up to swapping. It consequently records `Phi(2*p^2) >= p - 1` and
passes to a general asymptotic lower bound using that consecutive-prime ratios tend to one.

The scan is discovery evidence, not H0. No independent source reviewer has checked its
transcription, definition incorporation, proof boundary, corrections or errata. The scanned
displayed asymptotic formulas are not reliably captured by text extraction and are deliberately not
transcribed or selected here.

## Clause crosswalk

| Source or catalog clause | Mathematical component | Lean component required later | Intake result |
|---|---|---|---|
| `Erdos-Turan construction` | one source-identified explicit construction | exact selected declaration and source-node map | matching source family only |
| `Sidon set` / source `B_2` sequence | uniqueness of pair sums including diagonal pairs | a precise predicate plus checked transports to any set/difference formulation | convention candidate, not frozen |
| prime `p` | finite construction parameter | `p : Nat`, primality hypothesis, and exact lower-bound cases | binder candidate only |
| `k = 1, ..., p - 1` | construction index domain | interval, subtype, or `Fin` encoding with endpoint proofs | representation open |
| least positive residue of `k^2` | source construction formula | remainder/representative definition and nonzero/uniqueness lemmas | exact encoding open |
| `a_k < 2*p^2` | finite ambient bound | arithmetic inequality and interval containment | source clause located, not formalized |
| unequal sums for different pairs | Sidon invariant | pair canonicalization, equality-up-to-swap, and injectivity theorem | source proof located, no machine credit |
| `Phi(2*p^2) >= p - 1` | extremal corollary | exact `Phi` definition and construction-to-lower-bound bridge | optional candidate, not selected |
| general asymptotic lower bound | density consequence | exact formula, asymptotic encoding, prime theorem, and threshold | excluded pending visual transcription/review |
| `已验证` | untrusted catalog metadata | accepted source and kernel receipts would be required | no H or M credit |

## Neighbor boundary

`THM-M-0955` is separately cataloged as the Bose-Chowla theorem with the same broad gloss,
`Sidon集的构造`, but an attribution to Bose/Chowla and a 1960 date. Its algebraic finite-field
construction is a distinct target. No statement, source, obligation, proof body, receipt, or status
may transfer between the two without an accepted shared-obligation decision.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks finite-set, interval, pairwise, injectivity, finite-sum, and natural-square-root APIs adjacent
to a future encoding. A bounded search of pinned mathlib and repo-local Lean found no lexical
`Sidon`, `B2 sequence`, or named Erdos-Turan additive construction declaration.

The negative query is bounded intake discovery, not the downstream immutable anchor audit or a
proof of global absence. The canonical module/expression, elaborated hash, environment-expression
fingerprint, checked alternate encodings, and statement mutations remain null.

## Source gate

Before `S56-M-0956-STATEMENT`, accountable reviewers must select the explicit construction alone or
an exact source corollary, independently verify the immutable scan and any displayed formula,
freeze the `B_2` convention and all domains, residues, pair identity, bounds, quantifiers, and
boundary cases, audit corrections, and approve the clause map. Only then may the statement phase
freeze minimal imports, the exact Lean expression and environment fingerprints, checked transports,
and required mutations.
