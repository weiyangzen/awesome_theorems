# Scope map

## Included claim

- A positive natural-number modulus `q`.
- A reduced residue class modulo `q`, expressed by coprimality or a unit of `ZMod q`.
- Natural primes belonging to that residue class.
- Infinitude of those primes, with the equivalent unbounded-existence formulation retained as an
  alternate encoding to be checked at the statement gate.
- Dirichlet characters and their L-functions only insofar as they occur in the proof architecture;
  they are not the conclusion named by the repository gloss.

## Frozen statement boundary

The canonical encoding uses `q : Nat`, `[NeZero q]`, `a : ZMod q`, and `IsUnit a`, in that order.
Primes are natural numbers and membership in the progression is `(p : ZMod q) = a`. Infinitude is
canonical; `dirichletPrimesInAPTarget_iff_unbounded` checks transport to existence above every
natural bound. `q = 0` is excluded by `NeZero`; `q = 1` is included. Nonunit classes remain outside
the quantified implication's conclusion-bearing cases.

The title and gloss are not interchangeable: `狄利克雷L函数` names the analytic machinery while
`等差数列素数定理` identifies the theorem claimed. The latter controls the root scope.

## Explicit exclusions

- Merely defining `DirichletCharacter.LFunction` or proving analytic continuation, a functional
  equation, Euler product, or nonvanishing as a substitute for infinitude of primes.
- The prime number theorem for arithmetic progressions, asymptotic equidistribution, or an error
  term; these strictly strengthen the repository claim.
- Euclid's theorem (infinitely many primes without a prescribed residue class).
- A theorem for one fixed modulus or one special residue class.
- Non-coprime classes, which can contain at most exceptional primes, as though they satisfied the
  general conclusion.
- Treating the repository labels `已验证` or the presence of a mathlib theorem name as accepted
  source, kernel, provenance, or completion evidence.

The canonical expression is now frozen by the dependent statement artifact. The earlier API probe
remains intake discovery evidence only and supplies no proof credit.
