# Scope map

## Included claim

- A set `X` definable, with the source-permitted parameters, in an o-minimal expansion of the real
  field.
- Rational points in a fixed real affine space, measured using the affine rational height fixed by
  the selected source.
- The algebraic part `X_alg`, formed from connected positive-dimensional semialgebraic subsets of
  `X`, and the complementary transcendental part `X \ X_alg`.
- For each positive real `epsilon`, a constant depending on `X` and `epsilon` that bounds the
  number of rational points of height at most `T` in the transcendental part by `c * T^epsilon`.
- The finiteness of each counted height slice, required before using a finite cardinality in Lean.

## Decisions frozen for statement work

The next phase must select and inspect Pila-Wilkie Theorem 1.8 (first version) together with its
height and algebraic-part definitions. It must preserve the binder order: ambient structure,
dimension, definable set, positive exponent, existential constant, then all permitted height
thresholds. In particular, the constant may depend on `X` and `epsilon` but not on `T`.

The Lean target must express actual o-minimality, definability, affine height, algebraic part, and a
numeric cardinality inequality. None may be replaced by an arbitrary proposition or a field of an
input structure. Exact decisions about parameters, `n = 0`, empty sets, zero-dimensional sets,
`T = 0`, the lower threshold, and strict versus nonstrict inequalities remain source-gated.

## Explicit exclusions

- Wilkie's conjectural or later polylogarithmic bounds for restricted exponential structures.
- Uniform family/block refinements, counting algebraic points of bounded degree, or projective
  variants without a checked transport from the selected theorem.
- Cell decomposition by itself, o-minimality by itself, or a semialgebraic special case as the root.
- A boundary structure that accepts the subpolynomial counting conclusion as input.
- The identically named `THM-M-0441` artifacts as accepted evidence for this target. They are
  cross-target discovery material only and cannot transfer scope, state, or proof credit.
- The repository metadata label `已验证` or successful ingredient elaboration as proof evidence.
