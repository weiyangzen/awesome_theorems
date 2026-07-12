# Scope map

## Preserved source scope

- Subject: prime ideals in an algebraic number-field extension.
- Behavior: splitting data classified by Frobenius conjugacy information.
- Conclusion kind: a density distribution, not merely infinitude or existence of primes.
- Historical label: Chebotarev density theorem.

The standard theorem family says that for a finite Galois extension `L/K` and a conjugacy class
`C` in `Gal(L/K)`, unramified prime ideals of `K` whose Frobenius class is `C` have density
`|C| / |Gal(L/K)|`. This sentence is a scope locator, not yet the accepted canonical claim.

## Decisions required at statement freeze

The next phase must freeze all of the following from an inspected source:

1. Number fields and the precise finite Galois-extension structure.
2. Nonzero prime/maximal ideals of the ring of integers and the norm used to order them.
3. The finite set of ramified primes excluded from the Frobenius map.
4. Arithmetic versus geometric Frobenius and whether inversion changes the selected class.
5. One conjugacy class, a conjugacy-stable subset, or a splitting-type formulation.
6. Natural density, Dirichlet density, or both, including the exact limiting expression.
7. The value `|C| / |G|`, coercions, and the empty/trivial boundary cases.

## Explicit exclusions

- Dirichlet's theorem on primes in arithmetic progressions as a substitute; it is a special case.
- Mere infinitude of primes with a prescribed Frobenius class.
- A theorem only about decomposition, inertia, or ramification indices.
- A finite-field Frobenius theorem or density statement for rational primes alone.
- A non-Galois splitting-type theorem without checked transport to the frozen Galois statement.
- An abstract equidistribution axiom followed by a tautological density conclusion.
- The repository label `已验证` as human-source or kernel-proof evidence.

No canonical Lean proposition is frozen during intake. In particular, convenient existing APIs may
not determine the density notion or silently strengthen the hypotheses.
