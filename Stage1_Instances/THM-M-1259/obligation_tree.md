# THM-M-1259 frozen obligation tree

## Root

`THM-M-1259-ROOT` is exactly `Stage1Instances.THM_M_1259.hormanderTarget`. Its machine proof
requires `THM-M-1259-L-ANALYTIC-CORE`; the local theorem
`expandedCore_composes_hormanderTarget` is the checked child-to-parent composition certificate.

## Analytic core

`THM-M-1259-L-ANALYTIC-CORE` expands `IsHypoelliptic`: after fixing every coefficient, smoothness
and bracket hypothesis, it fixes distributions `T` and `PT` and must derive smoothness of `T` from
`PT = P T` and smoothness of `PT`. The exact signature elaborates in `Statement.lean`.

## Commutator estimate

`THM-M-1259-L-COMMUTATOR-ESTIMATE` is the critical open PDE leaf. It must formalize localized
fractional Sobolev norms and prove a positive-gain estimate from finite bracket generation. Calling
a generic Sobolev inequality does not close this obligation. Its current planned signature is not
machine credit and must be refined before proof implementation.

## Regularity bootstrap

`THM-M-1259-L-REGULARITY-BOOTSTRAP` is a separate critical open leaf. It consumes the exact local
estimate, regularizes distributions, iterates the gain to arbitrary order, applies local Sobolev
embedding, and patches the smooth densities. None of these steps is hidden in the root wrapper.

## Root composition

`THM-M-1259-T-ROOT-COMPOSITION` is locally kernel-checked and has debt `M0-L`. Its proof only
introduces the root binders and applies the expanded analytic core. It supplies no proof of that
premise and therefore does not change root debt `M4`.

## Boundaries

The object-model and mathlib trust boundaries are separate nodes. Provenance, source, trust, and
workflow edges are typed separately from proof edges in `typed_graphs.json`. All seven canonical
obligations remain in the frozen root-relevant machine denominator; no wrapper, documentation node,
or supporting anchor duplicates proof coverage.
