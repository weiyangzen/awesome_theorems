# Scope map

## Source-supported theorem family

The intake preserves the family named by the catalog and explicitly present in Fejer's inspected
primary article: uniform convergence, for an everywhere-continuous real `2*pi`-periodic function,
of first-order Cesaro means of its symmetric Fourier partial sums. The source presentation uses:

- a real-valued function `f` on the real line with period `2*pi`;
- the usual constant, cosine, and sine Fourier coefficients;
- the symmetric partial sum `s_n` through frequency `n`; and
- the sequence `s_0, (s_0+s_1)/2, ..., (s_0+...+s_(n-1))/n`.

This is a source-supported prose boundary, not a frozen canonical mathematical claim or Lean
expression. Independent source review, exact transcription, incorporated definitions, proof and
errata mapping, and checked transports remain downstream.

## Decisions required at statement freeze

1. Independently approve the primary edition, page-52/page-60 clauses, incorporated definitions,
   proof boundary, translation, corrections, and errata.
2. Decide whether the canonical root is source-literal: real-valued and period `2*pi`, with the
   real-line periodic presentation transported to a circle.
3. If arbitrary positive period or complex values are used, provide checked scaling and scalar
   transports rather than silently generalizing the source.
4. Fix coefficient normalization, Haar-measure scaling, character sign, and the equivalence with
   the source's sine/cosine series.
5. Fix the `n`th symmetric partial sum and reconcile the source's `n`-term average through
   `s_(n-1)` with any zero-based `n+1`-term Lean definition.
6. Fix the exact uniform conclusion: convergence in the continuous-map sup-norm topology,
   `TendstoUniformly`, or an epsilon-supremum statement, with checked transports for every credited
   alternative.
7. Freeze ordered binders and all boundary cases, then mutation-test removed hypotheses, changed
   domains, changed binder scope, scalar/period transports, and initial indices.

## Boundary and degenerate cases

The source fixes period `2*pi`, so a nonpositive or zero arbitrary-period parameter is not part of
the literal source form. A generalized form must exclude or define it explicitly. Statement work
must also cover the zero and constant functions, zeroth Fourier partial sum, first Cesaro mean,
zero denominators under alternate indexing, real-to-complex inclusion, endpoint representatives,
and the relation between uniform and pointwise convergence.

Assuming convergence of the raw Fourier partial sums, absolute summability of every Fourier
coefficient, or the desired uniform estimate is a stronger hypothesis and cannot be introduced
into the root.

## Duplicate and substitution exclusions

- `THM-M-0347` is a distinct harmonic-analysis target with the shorter gloss "the Cesaro means of
  a continuous function converge." Its complex arbitrary-period statement and partial proof are
  useful discovery context only; no source, statement, proof, status, or receipt credit transfers.
- Raw Fourier partial sums need not converge for every continuous function, so their unrestricted
  convergence is not the target.
- `hasSum_fourier_series_of_summable` assumes summable Fourier coefficients. It is not Fejer's
  theorem for arbitrary continuous functions.
- `Filter.Tendsto.cesaro_smul` assumes the averaged sequence already converges. It cannot replace
  the analytic Fejer-kernel argument.
- Dirichlet or Jordan convergence under smoothness or bounded variation, `L1` Fejer convergence,
  the Riesz-Fejer theorem, Carleson-Hunt convergence, ergodic Cesaro averaging, and generic
  approximate-identity results without a checked root transport are separate claims.
- The manifest label `verified`, primary-source discovery, a theorem-name match, or this intake API
  probe gives no statement or proof credit.

## Formal boundary

Pinned mathlib contains the additive-circle carrier, normalized Haar measure, Fourier characters
and coefficients, continuous maps, uniform-convergence predicates, a summable-coefficient Fourier
theorem, and a generic Cesaro lemma. The probe authenticates only those interfaces. It does not
select a canonical expression, establish a source-to-Lean transport, or locate a terminal proof of
the unrestricted uniform theorem. Obligation and discovery hashes remain null at intake.
