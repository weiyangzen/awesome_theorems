# THM-M-1454 rev-5.6 intake

`THM-M-1454` is the numerical-analysis catalog item "GMRES." The catalog supplies only the gloss
"generalized minimal residual method," attribution to Yousef Saad and Martin Schultz, the year
1986, and an untrusted `verified` label. Those fields identify an algorithm and theorem family, not
a binder-complete mathematical proposition.

## Intake result

This dossier records a fail-closed `planned` instance. It does not silently choose among the
one-step minimal-residual characterization, exact termination of unrestarted GMRES, lucky-breakdown
equivalences, restarted-GMRES convergence under positivity or spectral hypotheses, or operation and
storage estimates.

The primary Saad-Schultz paper was inspected. Its abstract, Algorithm 3, equations (3)-(8),
Propositions 1-4, Theorem 5, and Corollaries 3 and 6 contain materially different claims. In
particular, the paper proves finite exact termination for unrestarted finite-dimensional GMRES, but
also exhibits restarted GMRES(1) stagnation. The catalog does not identify which result is the root,
so adopting any of them as the canonical statement at intake would substitute missing mathematics.

## Formal boundary

`IntakeProbe.lean` elaborates adjacent pinned matrix-vector, Gram-Schmidt, span, orthogonal-
projection, and norm-isometry APIs. A bounded exact-topic search found no GMRES declaration in
pinned mathlib or the repo-local Lean sources. These are discovery observations, not an exhaustive
anchor audit and not proof evidence.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H5, M4, R4]`: the catalog entry is not yet a stable proposition, although the primary paper
establishes several results in the named family; no source-identical usable formal artifact is
credited; and no readable proof reconstruction can attach to an unfrozen root. All six downstream
tasks remain open. Neither audit completion nor theorem completion is claimed.
