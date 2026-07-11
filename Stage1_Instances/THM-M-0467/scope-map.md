# Scope map

## Included claim

- A finite-dimensional abelian variety `A` over a field of characteristic zero.
- A closed algebraic subvariety `X` of `A`.
- Torsion points in the group `A`, their intersection with `X`, and its Zariski closure.
- The structural conclusion that this closure is a finite union of translates of abelian
  subvarieties by torsion points, with each translate lying in `X`.

This is the general Manin-Mumford/Raynaud conclusion intended by the Stage0 phrase "proof of the
Manin-Mumford conjecture." It includes the familiar curve-in-its-Jacobian finiteness consequence,
but does not silently replace the general theorem by that consequence.

## Decisions deferred to statement phase

Primary-source inspection must fix whether the base is an algebraically closed characteristic-zero
field or a number field followed by base change; whether `X` is integral, reduced, or an arbitrary
closed subscheme; and whether the source states a density criterion, a finite-union decomposition,
or a curve case. It must also fix the exact meaning of torsion translate, the quantifier ordering,
degenerate cases (`X` empty, zero-dimensional `A`, and `X = A`), and any passage between geometric
points and Lean's scheme/variety points.

## Explicit exclusions

- The positive-characteristic analogue, where prime-to-`p` qualifications and additional
  phenomena change the statement.
- Raynaud's theorem on formal schemes, Raynaud uniformization, or Raynaud-Gruson flattening.
- Mordell-Lang, Bogomolov, or the curve-only finiteness corollary as a substituted root theorem.
- An abstract package that assumes the finite-union conclusion as data.

The later statement must use concrete algebraic geometry and torsion-point interfaces or record the
precise missing mathlib API. The metadata label `已验证` supplies no machine-proof credit.
