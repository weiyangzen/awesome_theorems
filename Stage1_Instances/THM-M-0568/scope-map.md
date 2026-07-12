# Scope map

## Frozen metadata scope

- Subject: the Euler characteristic class associated with an oriented vector bundle.
- Intended ordinary form: an oriented real vector bundle of finite rank `n`, with an integral
  cohomology class in degree `n` on its base.
- Standard construction family: pull a Thom class back along the zero section.
- The repository's `已验证` label is untrusted metadata and supplies neither a proposition nor
  human or kernel proof evidence.

These bullets identify a mathematical object family. They do not select a theorem and are not a
canonical statement.

## Decisions required before statement freeze

The statement phase must select an immutable source theorem and freeze:

- topological, smooth, or other vector bundles; real fibers and finite rank;
- the base-space separation, paracompactness, finiteness, and connectedness hypotheses;
- an orientation over `Z`, or the exact generalized cohomology/coefficient orientation;
- ordinary, compactly supported, relative, or generalized cohomology conventions;
- reduced cohomology of a Thom space versus relative cohomology of disk/sphere bundles;
- the Thom class, zero section, pullback map, degree, and sign convention;
- the actual conclusion: existence/uniqueness, Thom pullback characterization, naturality,
  Whitney-sum/product behavior, vanishing under a nowhere-zero section, obstruction meaning, or
  equality of an Euler number with an Euler characteristic;
- quantifier and universe order, rank-zero and empty-base behavior, nonorientable bundles,
  orientation reversal, disconnected bases, and coefficient changes.

Changing any of those choices can change the proposition rather than merely its presentation.

## Explicit exclusions

- An arbitrary cohomology element called `e(E)` with its desired properties assumed as fields.
- The tangent-bundle Euler-number theorem, Poincare-Hopf theorem, or Gauss-Bonnet theorem as an
  unstated substitute for the characteristic-class construction.
- Stiefel-Whitney, Chern, or Pontryagin classes alone.
- A rank-specific or trivial-bundle fact presented as the general Euler-class target.
- The unrelated arithmetic usage "Euler system/classes" found in a legacy Lean module.

No formal target is frozen at intake. A later target must expose concrete bundle, orientation,
cohomology, Thom-class, and zero-section interfaces, or truthfully record the first missing API.
