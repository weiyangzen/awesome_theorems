# Scope map

## Preserved theorem family

The intake preserves the complex-analysis theorem named by the catalog: a complex-valued function
on the whole complex plane that is entire and bounded is constant. This is a theorem-family
boundary, not an accepted exact statement. A later statement phase may freeze one proposition only
after an immutable authoritative source passage and its definitions are mapped and independently
reviewed.

## Decisions required at statement freeze

1. Select an immutable primary or authoritative source edition, exact theorem and definition
   locators, proof boundary, correction or errata record, and independent source review.
2. Fix the domain and codomain. The catalog convention suggests `f : Complex -> Complex`; pinned
   mathlib generalizes to maps between arbitrary complex normed spaces, which is stronger and is
   not automatically source-identical.
3. Define "entire": complex differentiable at every point, analytic on the whole plane, or an
   explicitly checked equivalent source formulation.
4. Define "bounded": bounded range, existence of a global norm bound, or another source-selected
   equivalent, including the precise strict or non-strict inequality and quantifier order.
5. Define "constant": pairwise equality, `exists c, forall z, f z = c`, or function equality with
   a constant map. Any credited alternate form needs a checked transport.
6. Freeze the ordered binders, explicit versus implicit premises, universes, namespaces, minimal
   imports, foundation/TCB/computation profiles, and exact environment fingerprint.
7. Resolve whether the source theorem is scalar only or explicitly includes vector-valued or
   higher-dimensional-domain generalizations; no generalization may replace the received root.

## Boundary cases

- Constant functions, including the zero function, must satisfy the conclusion rather than be
  excluded by an artificial nonconstant premise.
- The domain is the whole complex plane; bounded holomorphic functions on a disk, half-plane, or
  other proper domain need not be constant.
- A function bounded only on one subset, one circle, one ray, or outside a compact set is not the
  received premise without a checked reduction.
- Real differentiability, continuity, local boundedness, meromorphicity, and harmonicity do not
  replace entire complex differentiability.
- If a generalized normed-space statement is considered, trivial carriers and the lack of a
  completeness assumption on the codomain must be explicitly source-crosswalked rather than
  inherited from a library theorem name.

## Explicit exclusions

- `THM-M-1520` and related Hamiltonian targets: preservation of phase-space volume is a distinct
  theorem that happens to share Liouville's name.
- `THM-M-1143`: bounded harmonic functions are constant is a separate root with a different
  premise, even though pinned mathlib derives a harmonic Liouville theorem.
- Liouville numbers, Liouville approximation/transcendence theorems, the Liouville function, the
  Arnold-Liouville theorem, and ODE Liouville formulas.
- The maximum-modulus principle, Cauchy estimates, the fundamental theorem of algebra, or a
  polynomial-only corollary used as a substitute for the requested root.
- A structure field or hypothesis that directly assumes constancy, and the catalog's untrusted
  `已验证` label or API probe used as proof credit.

No canonical Lean target, expression fingerprint, checked alternate encoding, discovery protocol,
obligation registry, or proof state is frozen at intake.
