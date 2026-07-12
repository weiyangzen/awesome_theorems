# Scope map

## Preserved source scope

The repository fixes only the Chinese label `Pesin理论`, the gloss `非一致双曲理论`
("nonuniform hyperbolic theory"), Yakov Pesin, 1977, importance "high," and an untrusted `已验证`
status. It supplies no bibliography, theorem locator, definition, premise, conclusion, or formal
artifact. The intake therefore preserves a subject-area and historical boundary only.

## Proposition-changing decisions

An approved source correction must select one immutable primary-source proposition and freeze:

- discrete time via a diffeomorphism or noninvertible map versus continuous time via a flow;
- the phase-space category, dimension, compactness, boundary conventions, Riemannian structure,
  universes, and differentiability class, including the exact meaning of `C^(1+alpha)` or `C^2`;
- the invariant probability measure, whether ergodicity is assumed, and all absolute continuity,
  integrability, or regularity hypotheses;
- the exact Oseledets input: almost-everywhere Lyapunov splitting, multiplicities, zero exponents,
  and whether nonuniform hyperbolicity means every exponent is nonzero;
- definitions of regular points and Pesin blocks, including measurable scopes, radii, constants,
  tempered functions, adapted norms, and forward/backward exponential estimates;
- local versus global stable and unstable sets or manifolds, their tangent-space identification,
  measurability or absolute continuity, and invariance properties;
- the placement of every universal and almost-everywhere quantifier and all exceptional sets; and
- one exact truth-valued conclusion, with all boundary and degenerate cases.

These choices give inequivalent propositions. They are a resolution checklist, not a canonical
claim.

## Candidate families not credited

- A nonuniform stable-manifold theorem producing local stable and unstable disks at almost every
  regular point with quantitative contraction and tangent-space conclusions.
- Existence and exhaustion properties of Pesin blocks with uniform constants on each block.
- Absolute continuity of stable or unstable laminations under source-specific regularity.
- A closing, shadowing, homoclinic, local-ergodicity, or Bernoulli consequence of nonuniform
  hyperbolicity.
- An entropy identity or inequality relating metric entropy to positive Lyapunov exponents.

No family in this list is selected, asserted, or credited at intake.

## Explicit exclusions

The intake must not silently substitute SRB measures (`THM-M-1417`), Lyapunov exponents
(`THM-M-1418`), Oseledets' multiplicative ergodic theorem (`THM-M-1419`), or Pesin's entropy
formula (`THM-M-1421`). The generic stable manifold theorem (`THM-M-1346`), uniform hyperbolic
dynamics (`THM-M-1411`), and Anosov diffeomorphisms (`THM-M-1412`) are separate roots as well.

Also excluded are a definition of nonuniform hyperbolicity without a theorem conclusion, a finite
linear example, a numerical Lyapunov calculation, generic ergodic or manifold-derivative lemmas,
and any structure that assumes the desired invariant manifolds, absolute continuity, estimates, or
conclusion as fields. None can identify or close the catalog topic.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib provides adjacent measure-preserving,
ergodic, manifold-derivative, and tangent-map APIs, but the bounded intake search found no named
Pesin or nonuniform-hyperbolicity declaration. This is substrate discovery only, not an exhaustive
anchor audit, exact-statement elaboration, or machine-proof evidence.
