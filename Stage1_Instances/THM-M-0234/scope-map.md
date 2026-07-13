# Scope map

## Preserved theorem family

The repository metadata supports only the Rouche zero-stability theorem family in one complex
variable. A familiar candidate route has:

- two complex-valued functions holomorphic on a neighborhood of an enclosed compact region;
- a simple closed boundary, a circle, or another source-selected contour and its interior;
- a strict pointwise boundary inequality making one function or perturbation smaller;
- absence of zeros of the dominant function on the boundary; and
- equality of the finite interior zero counts, with analytic multiplicity.

These bullets delimit a recognizable family. They are not an accepted statement, an alternate
encoding, or proof evidence.

## Proposition-changing decisions

The statement phase must resolve all of the following from an immutable, independently reviewed
source rather than from convenience:

1. Decide whether `THM-M-0234` is an alias or duplicate of `THM-M-0232`, or whether the two IDs own
   distinct source formulations. No state or proof credit transfers automatically.
2. Select the source edition, exact theorem locator, incorporated definitions, translation,
   correction and errata boundary, and reconcile the catalog's 1862 date with the located 1866
   printed work.
3. Fix the domain: a disk, Jordan domain, bounded open set, region inside a simple closed curve,
   or a general contour/cycle, including orientation and connected-component conventions.
4. Fix regularity: holomorphic on a neighborhood of the closure, holomorphic inside and continuous
   on the boundary, or another exact source condition.
5. Fix whether the inequality is `norm g < norm f` with conclusion comparing `f` and `f + g`, or
   `norm (f - g) < norm f` with conclusion comparing `f` and `g`; record which function dominates.
6. Freeze strictness and scope of the boundary inequality. Equality or a non-strict inequality is
   not silently admissible.
7. Define the zero count, prove its finiteness, count analytic multiplicities, and state whether
   boundary zeros are excluded or handled separately.
8. Freeze all domains, universes, ordered binders, hypotheses, conclusions, coercions, and
   degenerate cases before a Lean expression or transport is credited.

## Boundary cases and later mutations

- zero or constant dominant functions and identically zero perturbations;
- empty, degenerate, self-intersecting, oppositely oriented, or disconnected boundaries;
- radius zero or a domain with empty interior;
- zeros on the boundary and functions identically zero on a component;
- equality at one boundary point or replacement of `<` by `<=`;
- zero-free interiors, repeated zeros, and multiplicity greater than one;
- swapping the dominant and perturbing functions; and
- moving the existential/domain binders or weakening neighborhood holomorphicity.

These are mutation obligations for a future exact statement, not theorem claims at intake.

## Explicit exclusions

- `THM-M-0232`, its future artifacts, or any automatic duplicate-ID evidence transfer.
- The argument principle or a winding-number identity alone as the terminal target.
- Hurwitz's theorem on locally uniform limits or local persistence of zeros.
- A polynomial-only, disk-only, one-zero, or simple-zero corollary chosen without source approval.
- A meromorphic zero-minus-pole generalization without a checked relationship to the selected root.
- A zero count that ignores multiplicity, an unchecked numerical root count, or sampled boundary
  evidence.
- A structure, premise, axiom, or opaque interface that stores the desired equal zero count.
- The catalog's untrusted `已验证` label or an adjacent API check as H0 or M0 evidence.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib supplies analytic orders, isolated-zero
lemmas, locally finite divisors of meromorphic functions, and complex integration infrastructure.
A bounded exact-topic search found no Rouche-named or same-zero-count declaration in pinned
mathlib or repo-local Lean. The API probe authenticates only nearby types and declarations; it is
not the downstream immutable anchor audit and supplies no statement or proof credit.
