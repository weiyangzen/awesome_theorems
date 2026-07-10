# Wiles--Taylor--Wiles process for THM-M-0387

## Reading contract

This file recursively expands `M0387-WTW-W01` through `M0387-WTW-W09`. It is
a human-readable implementation plan for the machine-open general odd-prime
branch. The mathematical route is accepted in the published literature, but
the exact primary-source location for every project leaf has not yet been
reconstructed. Accordingly every leaf below is conservatively `H1`; no paper
citation changes its machine status. No local exact formal target or checked
composition theorem was located for these historical leaves, so they are
`M4`. Their `R0` records that the target, interfaces, trust boundary, ledger,
composition, and blocker are readable, not that the proof has been formalized.

Each terminal heading uses the same ten parts:

1. exact target;
2. hypotheses/interfaces;
3. proof idea;
4. formal map;
5. trust boundary;
6. axiom report;
7. `H/M/R` vector;
8. an independent ledger of at most 100 logical steps;
9. composition rule;
10. remaining debt/blocker.

The planned signatures use mathematical notation intentionally. They are not
Lean declarations and are never evidence of kernel closure.

## Source map and correction boundary

Primary proof package:

- Andrew Wiles, *Modular elliptic curves and Fermat's Last Theorem*, Annals of
  Mathematics 141 (1995), 443--551, DOI
  [`10.2307/2118559`](https://doi.org/10.2307/2118559). This is the primary
  source for semistable modularity and the modularity-lifting route.
- Richard Taylor and Andrew Wiles, *Ring-theoretic properties of certain Hecke
  algebras*, Annals of Mathematics 141 (1995), 553--572, DOI
  [`10.2307/2118560`](https://doi.org/10.2307/2118560). This is part of the
  published corrected proof package and supplies the ring-theoretic control
  replacing the failed 1993 Euler-system step.
- Jean-Pierre Serre, *Sur les représentations modulaires de degré 2 de
  Gal(Qbar/Q)*, Duke Mathematical Journal 54 (1987), 179--230, DOI
  [`10.1215/S0012-7094-87-05413-5`](https://doi.org/10.1215/S0012-7094-87-05413-5).
- Barry Mazur, *Modular curves and the Eisenstein ideal*, Publications
  Mathématiques de l'IHÉS 47 (1977), 33--186, DOI
  [`10.1007/BF02684339`](https://doi.org/10.1007/BF02684339).
- Kenneth Ribet, *On modular representations of Gal(Qbar/Q) arising from
  modular forms*, Inventiones Mathematicae 100 (1990), 431--476, DOI
  [`10.1007/BF01231195`](https://doi.org/10.1007/BF01231195).

Henri Darmon, Fred Diamond, and Richard Taylor, *Fermat's Last Theorem*,
Current Developments in Mathematics 1995, 1--154, DOI
[`10.4310/CDM.1995.v1995.n1.a1`](https://doi.org/10.4310/CDM.1995.v1995.n1.a1),
is used only as a secondary architecture guide. It does not replace the
primary sources above and does not authorize an unverified page/theorem map.

The correction must be stated precisely. The 1993 announced proof contained a
gap in the Euler-system/commutative-algebra portion intended to control the
relevant Selmer group. Wiles did not merely add a missing sentence. The
published Wiles paper and the Taylor--Wiles companion use auxiliary primes,
augmented deformation/Hecke problems, and ring-theoretic control to supply the
required modularity-lifting result. This file describes that published route.

## W01 primitive odd-prime normalization

### M0387-WTW-W01.1 primitive and coprime normalization

1. **Exact target.** Planned theorem: a nonzero natural solution to
   `a^p + b^p = c^p`, with prime `p ≥ 5`, yields a nonzero integer solution
   `(A,B,C)` with `gcd {A,B,C} = 1` and the same exponent.
2. **Hypotheses/interfaces.** `Nat.Prime p`, `5 ≤ p`, nonzero `a,b,c`, the
   equation, gcd/division APIs, and transport between naturals and integers.
3. **Proof idea.** Divide all three terms by their common gcd; cancellation of
   its `p`-th power preserves the equation and removes all common factors.
4. **Formal map.** Planned historical target; adjacent checked local interface
   is `FermatLastTheoremForCoprime` and
   `fermatLastTheoremFor_iff_coprime`. That interface proves the abstract
   reduction but is not a Frey-package constructor.
5. **Trust boundary.** Human gcd argument plus pinned arithmetic foundations;
   no WTW proof body is imported.
6. **Axiom report.** Planned node, so no terminal Lean axiom report exists.
   `sorryAx` and custom axioms remain disallowed.
7. **H/M/R vector.** `[H1, M4, R0]`; exact primary source location pending.
8. **Independent ledger (7 steps).** (1) Set `d = gcd(a,b,c)`. (2) Prove
   `d ≠ 0`. (3) Write `a=dA`, `b=dB`, `c=dC`. (4) substitute into the
   equation. (5) factor out `d^p`. (6) cancel `d^p`. (7) use maximality of
   the gcd to prove the normalized triple primitive and nonzero.
9. **Composition rule.** Supplies the primitive triple consumed by `W01.2`.
10. **Remaining debt/blocker.** Define the exact Frey input structure and
    prove this normalization into that structure without a placeholder.

### M0387-WTW-W01.2 parity and sign normalization

1. **Exact target.** Planned theorem: a primitive integer solution at an odd
   prime exponent can be permuted and sign-adjusted so exactly one of the two
   relevant parity patterns is selected, with the conventional even entry
   occupying the coordinate required by the Frey model.
2. **Hypotheses/interfaces.** Primitive nonzero `(A,B,C)`, odd prime `p`, and
   `A^p+B^p=C^p`.
3. **Proof idea.** Primitivity excludes two even coordinates; reduction modulo
   `2` forces one coordinate even. Oddness of `p` makes sign changes compatible
   with the equation, and symmetry exchanges `A` and `B`.
4. **Formal map.** No historical WTW Lean declaration located. Planned target
   feeds the exact convention selected for `W02.1`.
5. **Trust boundary.** Human parity calculation; no automation certificate.
6. **Axiom report.** None, because the node is not a Lean theorem.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (6 steps).** (1) show not all entries are odd modulo
   `2`; (2) use primitivity to exclude two even entries; (3) identify the unique
   even coordinate; (4) permute coordinates using equation symmetry; (5) use
   `(-x)^p=-x^p`; (6) record the selected signs/parity in the normalized input.
9. **Composition rule.** Combines with `W01.1` to provide `W01.3`.
10. **Remaining debt/blocker.** The exact convention must match the future
    Weierstrass model and all local formulas.

### M0387-WTW-W01.3 attach the historical Frey route

1. **Exact target.** Planned constructor returning a normalized counterexample
   package with `p ≥ 5` and the precise data required to define the Frey curve.
2. **Hypotheses/interfaces.** Outputs of `W01.1` and `W01.2`.
3. **Proof idea.** Bundle, rather than re-prove, the normalization invariants
   and expose projections with stable names.
4. **Formal map.** A source-only Imperial declaration
   `FreyPackage.of_not_FermatLastTheoremFor_p_ge_5` exists at the audited
   revision, but is an `E3/M3` candidate for a different formal route and is
   not imported here.
5. **Trust boundary.** Historical route and Imperial overlay remain separate.
6. **Axiom report.** No local theorem. The external candidate lacks an
   independent transitive axiom/build report for this declaration.
7. **H/M/R vector.** `[H1, M4, R0]` for the historical node.
8. **Independent ledger (4 steps).** (1) take the primitive triple; (2) take
   its parity/sign witness; (3) package the exponent prime and lower bound;
   (4) expose the equation and nonvanishing fields.
9. **Composition rule.** `W01.1 + W01.2 -> W01.3`, and `W01.3 -> W02.1`.
10. **Remaining debt/blocker.** No repo-local exact package and constructor
    have been kernel checked.

## W02 Frey curve construction

The intended model is the usual Frey curve associated with a normalized
counterexample, for example `E : y^2 = x(x-A^p)(x+B^p)` after one fixed sign
convention. Formula choices must be frozen once; later invariant and conductor
claims are invalid if they silently switch conventions.

### M0387-WTW-W02.1 curve definition

1. **Exact target.** Define an integral Weierstrass model `E_F(A,B,p)` whose
   cubic is `x(x-A^p)(x+B^p)` under the chosen normalization.
2. **Hypotheses/interfaces.** The package `W01.3` and a Weierstrass-model API
   over `ℤ` with base change to `ℚ`.
3. **Proof idea.** Expand the cubic to read off integral coefficients and form
   the corresponding Weierstrass equation.
4. **Formal map.** No local historical declaration. Imperial source-only
   anchors include `freyCurveInt`, `freyCurve`, and `map`, classified `M3/E3`.
5. **Trust boundary.** External anchors are source evidence only, not imported
   proof bodies.
6. **Axiom report.** No local terminal theorem; Imperial transitive report for
   this leaf was not reproduced.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (5 steps).** (1) choose the cubic factors; (2) expand
   them; (3) identify integral Weierstrass coefficients; (4) construct the
   integral model; (5) base-change it to `ℚ`.
9. **Composition rule.** Supplies a model to `W02.2` and `W02.3`.
10. **Remaining debt/blocker.** Needed elliptic-curve object/API compatibility
    and exact sign convention are not locally implemented.

### M0387-WTW-W02.2 nonsingularity

1. **Exact target.** Prove that `E_F(A,B,p)` has nonzero discriminant and hence
   defines an elliptic curve over `ℚ`.
2. **Hypotheses/interfaces.** `A,B,C` nonzero, the Fermat equation, and the
   discriminant formula developed in `W02.3` or a direct distinct-root proof.
3. **Proof idea.** The three roots `0`, `A^p`, and `-B^p` are distinct: equality
   of the latter two would force `C^p=0`; nonzero coordinates exclude the other
   coincidences.
4. **Formal map.** Planned theorem only; source-only Imperial curve definitions
   do not establish repo-local closure.
5. **Trust boundary.** Algebraic identity and field nonsingularity criterion.
6. **Axiom report.** None; no local declaration exists.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (6 steps).** (1) `A^p ≠ 0`; (2) `B^p ≠ 0`; (3)
   suppose `A^p=-B^p`; (4) use the Fermat equation to derive `C^p=0`; (5)
   contradict `C ≠ 0`; (6) invoke the distinct-root/nonzero-discriminant
   criterion.
9. **Composition rule.** Turns the model of `W02.1` into the elliptic curve
   used by all later packages.
10. **Remaining debt/blocker.** A checked bridge from the chosen integral model
    to mathlib's elliptic curve structure is absent.

### M0387-WTW-W02.3 discriminant and c-invariants

1. **Exact target.** Calculate the selected model's `Δ`, `c₄`, and `j`, and
   normalize all units and powers of `2` consistently.
2. **Hypotheses/interfaces.** `W02.1`, the Fermat equation, polynomial/ring
   normalization, and Weierstrass invariant definitions.
3. **Proof idea.** Substitute the model coefficients into universal invariant
   polynomials, expand, and rewrite `A^p+B^p=C^p`.
4. **Formal map.** Imperial source has `Δ`, `c₄`, `j` and
   `j_valuation_of_bad_prime` anchors, but they remain `E3/M3` and are not this
   historical leaf's proof.
5. **Trust boundary.** Symbolic identities need kernel-checked ring
   normalization, not an unchecked computer-algebra result.
6. **Axiom report.** None locally; no candidate has passed the leaf's exact
   type, build, placeholder, and transitive-axiom gates.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (7 steps).** (1) read off `a₁,...,a₆`; (2) compute
   `b₂`; (3) compute `b₄`; (4) compute `b₆,b₈`; (5) substitute in
   `c₄`; (6) substitute in `Δ`; (7) simplify with the Fermat equation and
   define `j=c₄^3/Δ`.
9. **Composition rule.** Provides the arithmetic inputs to `W02.4--W02.6` and
   the representation compatibility in `W03.5`.
10. **Remaining debt/blocker.** Exact formulas must be reconciled against one
    frozen model; source names alone are not proof evidence.

### M0387-WTW-W02.4 minimal model

1. **Exact target.** For every rational prime `ℓ`, give a minimal integral
   local model of `E_F` and relate its minimal discriminant to `W02.3`.
2. **Hypotheses/interfaces.** Invariant formulas, primitive/parity data, local
   valuations, and minimal Weierstrass model/change-of-variables APIs.
3. **Proof idea.** Split `ℓ=2` from odd `ℓ`; for odd primes use
   primitivity to control which coordinate is divisible; at `2`, apply the
   chosen parity normalization and an explicit integral change of variables.
4. **Formal map.** No exact local or integrated external theorem located.
5. **Trust boundary.** Local algebra and valuation case split; every coordinate
   change must preserve the rational elliptic curve.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (8 steps).** (1) fix `ℓ`; (2) split `ℓ=2`/odd;
   (3) for odd `ℓ`, use pairwise coprimality; (4) compute coefficient
   valuations; (5) prove minimality by the local criterion; (6) at `2`, use the
   normalized parity; (7) exhibit and verify the integral variable change;
   (8) calculate the resulting minimal discriminant valuation.
9. **Composition rule.** `W02.3 + W01.2 -> W02.4`; feeds reduction type and
   conductor calculations.
10. **Remaining debt/blocker.** The local minimal-model and especially the
    `2`-adic calculation are not formalized in this repository.

### M0387-WTW-W02.5 semistability

1. **Exact target.** Prove `E_F` has only good or multiplicative reduction at
   every prime, hence is semistable.
2. **Hypotheses/interfaces.** Minimal models from `W02.4`, valuations of `Δ`
   and `c₄` from `W02.3`, and a local reduction criterion.
3. **Proof idea.** At every bad prime, show the minimal discriminant has
   positive valuation while `c₄` is a unit in the relevant local test; this
   rules out additive reduction.
4. **Formal map.** No checked historical-route theorem located.
5. **Trust boundary.** The Néron/Tate local reduction criterion is a major
   imported mathematical boundary and must become its own formal bridge.
6. **Axiom report.** No local declaration.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (7 steps).** (1) fix a prime `ℓ`; (2) if `vℓ(Δ)=0`,
   conclude good reduction; (3) otherwise use primitivity to identify the
   divisible coordinate; (4) apply the invariant formulas; (5) prove the
   multiplicative-reduction criterion for odd `ℓ`; (6) use the separate
   `2`-adic minimal model; (7) quantify over all `ℓ`.
9. **Composition rule.** Supplies the hypothesis for semistable modularity in
   `W04.9`.
10. **Remaining debt/blocker.** Missing formal local-reduction infrastructure
    and exact `2`-adic proof.

### M0387-WTW-W02.6 conductor and local reduction data

1. **Exact target.** Calculate the conductor exponent of `E_F` at each prime
   and the conductor of the residual representation needed by level lowering.
2. **Hypotheses/interfaces.** `W02.3--W02.5`, Tate-module/local representation
   definitions, and conductor comparison theorems.
3. **Proof idea.** Semistability restricts exponents to good/multiplicative
   cases. At primes dividing `ABC`, use the discriminant's multiple-of-`p`
   valuation to control residual ramification; keep the prime `2` separate.
4. **Formal map.** No exact integrated theorem. This node is not replaced by
   merely defining a conductor.
5. **Trust boundary.** Arithmetic conductor and Artin conductor comparison are
   central imported boundaries.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (8 steps).** (1) enumerate bad primes; (2) use good
   reduction off `2ABC`; (3) classify odd bad primes as multiplicative; (4)
   compute their curve conductor exponents; (5) calculate discriminant
   valuations modulo `p`; (6) infer residual unramified/finite conditions;
   (7) perform the `2`-adic calculation; (8) multiply local conductor factors.
9. **Composition rule.** Feeds `W03.4`, `W03.5`, and every hypothesis in `W05`.
10. **Remaining debt/blocker.** No Lean object and proof connect Frey local
    invariants to the exact conductor required by Ribet's theorem.

## W03 mod-p Galois representation

### M0387-WTW-W03.1 p-torsion representation

1. **Exact target.** Construct `ρ̄_E,p : G_Q -> GL₂(F_p)` from the action on
   `E_F[p]`, with a fixed basis-independent isomorphism class.
2. **Hypotheses/interfaces.** The elliptic curve `W02.2`, prime `p`, torsion
   points over an algebraic closure, and continuity/topology APIs.
3. **Proof idea.** Show `E[p]` is two-dimensional over `F_p`; Galois acts
   functorially and linearly, giving a continuous representation after a basis
   choice; conjugacy makes later predicates basis-independent.
4. **Formal map.** No local exact construction specialized to the Frey curve.
5. **Trust boundary.** Elliptic-curve torsion and absolute-Galois
   infrastructure are major formal dependencies.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (7 steps).** (1) form `E[p]`; (2) prove its `F_p`
   module structure; (3) prove dimension two; (4) define Galois action; (5)
   prove linearity; (6) choose a basis and map into `GL₂`; (7) prove
   continuity and basis-conjugacy invariance.
9. **Composition rule.** Representation consumed by `W03.2--W03.5` and `W05`.
10. **Remaining debt/blocker.** Required Galois/torsion APIs and the exact
    continuity proof are not present as a closed local package.

### M0387-WTW-W03.2 irreducibility and exceptional cases

1. **Exact target.** Prove the Frey residual representation is irreducible for
   the prime exponent `p ≥ 5`, treating all exceptional rational-isogeny
   cases explicitly.
2. **Hypotheses/interfaces.** `W03.1`, rational `p`-isogeny criteria, Frey
   invariants, and Mazur's rational-isogeny results.
3. **Proof idea.** Reducibility gives a rational Galois-stable line and hence a
   rational cyclic `p`-isogeny. Mazur restricts possible prime degrees; the
   remaining small possibilities are excluded using the Frey curve's local
   behavior and the normalized equation.
4. **Formal map.** No exact local theorem. Mazur 1977 is a primary source
   boundary, but exact theorem/page-to-leaf reconstruction is pending.
5. **Trust boundary.** Mazur's theorem is a major human theorem and must be an
   explicit imported formal node, never called “standard.”
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (8 steps).** (1) suppose reducible; (2) obtain an
   invariant line; (3) turn it into a rational subgroup; (4) obtain a rational
   `p`-isogeny; (5) apply Mazur's prime-degree restriction; (6) list surviving
   primes `p ≥ 5`; (7) use Frey local/invariant data to exclude each; (8)
   conclude irreducibility.
9. **Composition rule.** Supplies a mandatory hypothesis to modularity lifting
   and level lowering.
10. **Remaining debt/blocker.** Neither Mazur's theorem nor the Frey-specific
    elimination is locally kernel checked.

### M0387-WTW-W03.3 cyclotomic determinant

1. **Exact target.** Prove `det(ρ̄_E,p)` equals the mod-`p` cyclotomic
   character.
2. **Hypotheses/interfaces.** `W03.1` and the nondegenerate Galois-equivariant
   Weil pairing on `E[p]`.
3. **Proof idea.** Galois acts on the alternating Weil pairing through its
   action on `p`-th roots of unity; in dimension two the scalar on the top
   exterior power is the determinant.
4. **Formal map.** No exact local theorem specialized and composed here.
5. **Trust boundary.** Weil-pairing construction and equivariance.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (5 steps).** (1) choose a basis of `E[p]`; (2) evaluate
   the Weil pairing on it; (3) apply a Galois element; (4) use equivariance and
   the cyclotomic action; (5) identify the basis-change scalar with the matrix
   determinant.
9. **Composition rule.** Feeds the fixed-determinant deformation problem and
   the oddness condition.
10. **Remaining debt/blocker.** Missing composed Weil-pairing-to-determinant
    theorem in the selected formal object model.

### M0387-WTW-W03.4 ramification conditions

1. **Exact target.** Prove the residual representation is unramified or
   finite-flat at precisely the local places required by modularity lifting and
   level lowering, with a separate statement at `p` and `2`.
2. **Hypotheses/interfaces.** `W02.6`, Néron--Ogg--Shafarevich/Tate-curve local
   criteria, inertia representations, and finite-flat definitions.
3. **Proof idea.** Good reduction gives unramified torsion away from `p`;
   multiplicative reduction is described by a Tate curve; discriminant
   valuations divisible by `p` remove residual conductor at odd divisors of
   `ABC`; handle `p` and `2` using their dedicated local models.
4. **Formal map.** No exact historical-route Lean theorem located.
5. **Trust boundary.** Local Galois representation and finite-flat group-scheme
   theorems are central external mathematical interfaces.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (8 steps).** (1) fix `ℓ`; (2) split good and bad
   reduction; (3) prove unramifiedness in the good case; (4) invoke the Tate
   description in the multiplicative case; (5) insert discriminant valuations;
   (6) calculate residual inertia for `ℓ | ABC`; (7) establish the local
   condition at `p`; (8) record the separate condition at `2`.
9. **Composition rule.** Supplies local hypotheses to `W04.4` and `W05.1`.
10. **Remaining debt/blocker.** No checked local-to-Galois bridge for this
    curve and no complete finite-flat API packet were located.

### M0387-WTW-W03.5 compatibility with Frey invariants

1. **Exact target.** Bundle irreducibility, determinant, oddness, and all local
   conductor/ramification data into the exact representation interface consumed
   by `W04` and `W05`.
2. **Hypotheses/interfaces.** `W02.3`, `W02.6`, and `W03.1--W03.4`.
3. **Proof idea.** This is an explicit interface theorem: every abstract field
   is discharged by one previously proved invariant or representation lemma.
4. **Formal map.** Planned structure and constructor; no checked declaration.
5. **Trust boundary.** No new imported mathematics, but type/normalization
   mismatches can invalidate composition and must be checked.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (6 steps).** (1) insert `W03.1`; (2) insert
   irreducibility from `W03.2`; (3) insert determinant from `W03.3`; (4) derive
   oddness; (5) insert local conditions from `W03.4`; (6) identify the conductor
   using `W02.6`.
9. **Composition rule.** `W02 + W03.1--W03.4 -> W03.5`; this is the sole
   representation input to later packages.
10. **Remaining debt/blocker.** Exact consumer interfaces for modularity
    lifting and Ribet lowering have not been formalized, so the bundle type is
    not yet frozen.

## W04 semistable modularity over Q

`W04` is the largest high-risk package and must not be a one-line citation.
The route below distinguishes foundations, residual modularity, deformation
problems, local conditions, auxiliary primes, patching, `R=T`, nonminimal
lifting, and the final theorem. It describes the published 1995 route, not the
invalidated 1993 Euler-system step.

### M0387-WTW-W04.1.1 modular forms foundations

1. **Exact target.** Construct the spaces of weight-two cusp forms at the
   required levels, their `q`-expansions, new/old decompositions, and normalized
   eigenforms.
2. **Hypotheses/interfaces.** Congruence subgroups, modular curves, line
   bundles/differentials or an equivalent analytic/algebraic model.
3. **Proof idea.** Define forms with their transformation and cusp conditions;
   use finite-dimensionality and commuting Hecke operators to isolate
   eigenforms.
4. **Formal map.** No full local foundation supporting the terminal WTW chain
   was located.
5. **Trust boundary.** Complex analysis/algebraic geometry and finite-
   dimensional spectral decomposition.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (7 steps).** (1) define `Γ₀(N)`; (2) define weight-two
   forms; (3) impose cusp conditions; (4) construct `q`-expansion; (5) prove
   finite-dimensionality; (6) define old/new subspaces; (7) define normalized
   simultaneous eigenforms.
9. **Composition rule.** Supplies objects for `W04.1.2`, `W04.1.3`, and `W06`.
10. **Remaining debt/blocker.** The required coherent modular-form stack is not
    present in the local FLT dependency closure.

### M0387-WTW-W04.1.2 Hecke algebra foundations

1. **Exact target.** Define the Hecke algebra acting on the selected modular
   form/cohomology module and localize/complete it at a residual maximal ideal.
2. **Hypotheses/interfaces.** `W04.1.1`, Hecke correspondences/operators,
   finite modules, localization, and complete local rings.
3. **Proof idea.** Generate a commutative subalgebra by Hecke operators, prove
   finiteness, select the maximal ideal associated with the residual system,
   and pass to the local completed algebra `T`.
4. **Formal map.** No integrated historical WTW theorem package located.
5. **Trust boundary.** Geometric construction and commutation of Hecke
   operators, plus commutative algebra.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (7 steps).** (1) define `T_ℓ`; (2) prove the
   operators preserve the module; (3) prove commutation; (4) form their generated
   algebra; (5) prove finiteness; (6) define the residual maximal ideal; (7)
   localize and complete.
9. **Composition rule.** Produces the `T` compared with a deformation ring in
   `W04.7`.
10. **Remaining debt/blocker.** Hecke correspondences and the exact localized
    algebra are not locally formalized end to end.

### M0387-WTW-W04.1.3 eigenform-to-representation bridge

1. **Exact target.** Associate to a normalized eigenform the compatible
   two-dimensional `ℓ`-adic and residual Galois representations with the
   prescribed trace/determinant at unramified Frobenius elements.
2. **Hypotheses/interfaces.** `W04.1.1--W04.1.2`, number fields, absolute
   Galois groups, and Deligne/Carayol representation theorems.
3. **Proof idea.** Use the eigenvalues as Frobenius traces and construct the
   representation via the geometry/cohomology of modular curves, then prove
   local-global compatibility.
4. **Formal map.** No checked local theorem of the required scope.
5. **Trust boundary.** This is a major imported theorem, not a definitional
   conversion; it requires its own formalization boundary.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (6 steps).** (1) fix the eigenform and coefficient
   prime; (2) construct the cohomological realization; (3) obtain the Galois
   action; (4) identify Frobenius characteristic polynomials; (5) reduce modulo
   the maximal ideal; (6) prove determinant and local compatibility.
9. **Composition rule.** Makes “modular representation” a concrete interface
   for `W04.2`, `W04.7`, and `W05`.
10. **Remaining debt/blocker.** The representation-attached-to-eigenform
    theorem is absent from the repo-local closure.

### M0387-WTW-W04.2.1 Langlands--Tunnell residual base

1. **Exact target.** Establish residual modularity for the odd irreducible
   mod-`3` representation in the solvable-image situation needed by Wiles.
2. **Hypotheses/interfaces.** Odd irreducible two-dimensional representation
   over `F₃`, projective-image classification, and Langlands--Tunnell.
3. **Proof idea.** Identify the relevant projective image as solvable and apply
   the weight-one modularity theorem; then pass to the modularity input required
   for the elliptic-curve lifting theorem.
4. **Formal map.** No local declaration located.
5. **Trust boundary.** Langlands--Tunnell is a major external theorem and the
   weight-one-to-weight-two bridge is nontrivial.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (6 steps).** (1) form the projective representation;
   (2) classify its image; (3) verify oddness; (4) apply Langlands--Tunnell;
   (5) obtain a modular form; (6) identify the residual representation and
   required local type.
9. **Composition rule.** Supplies the residual modularity input when `E[3]` is
   irreducible.
10. **Remaining debt/blocker.** Langlands--Tunnell and its exact representation
    bridges are not formalized locally.

### M0387-WTW-W04.2.2 the 3--5 trick

1. **Exact target.** If a semistable elliptic curve's mod-`3` representation is
   reducible, construct an auxiliary semistable elliptic curve sharing the
   mod-`5` representation but having irreducible mod-`3`, and transfer
   modularity back.
2. **Hypotheses/interfaces.** Semistable curve, irreducibility criteria,
   rational points on the relevant moduli curve, and lifting theorems at `3`
   and `5`.
3. **Proof idea.** Parametrize curves with the chosen `5`-torsion, use weak
   approximation/Hilbert irreducibility to choose one with good local behavior
   and irreducible `3`-torsion, prove it modular, then use the shared
   `5`-representation to lift modularity of the original curve.
4. **Formal map.** No local exact package.
5. **Trust boundary.** Moduli interpretation, rational-point approximation,
   and both modularity-lifting applications.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (8 steps).** (1) assume reducible `E[3]`; (2) verify
   irreducibility of the relevant `E[5]`; (3) form the twist/moduli problem for
   the shared `5`-representation; (4) prove it is a suitable genus-zero curve;
   (5) choose a rational point with prescribed local conditions; (6) construct
   `E'`; (7) prove `E'` modular using mod `3`; (8) transfer modularity to `E`
   through mod `5` lifting.
9. **Composition rule.** Together with `W04.2.1`, exhausts the residual base
   cases for semistable curves.
10. **Remaining debt/blocker.** Every moduli/approximation/lifting component is
    outside the current local proof closure.

### M0387-WTW-W04.3.1 deformation functor

1. **Exact target.** Define deformations of a fixed residual representation to
   complete local coefficient algebras, modulo strict equivalence, with fixed
   determinant and specified global/local conditions.
2. **Hypotheses/interfaces.** Absolutely irreducible residual representation,
   complete Noetherian local rings, continuous representations, and local
   conditions from `W03.5`.
3. **Proof idea.** Package lifts reducing to `ρ̄`, quotient by conjugation
   congruent to the identity, and prove functoriality under coefficient-ring
   morphisms.
4. **Formal map.** No exact local functor used by an FLT theorem.
5. **Trust boundary.** Topological continuity and strict-equivalence quotient.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (6 steps).** (1) define coefficient category; (2)
   define continuous lifts; (3) impose reduction to `ρ̄`; (4) impose fixed
   determinant/local conditions; (5) define strict equivalence; (6) prove
   pullback gives a functor.
9. **Composition rule.** Input to representability in `W04.3.2`.
10. **Remaining debt/blocker.** Exact category, topology, quotient, and local
    predicates remain to be implemented coherently.

### M0387-WTW-W04.3.2 universal deformation ring

1. **Exact target.** Prove the selected deformation functor is represented by
   a universal complete local ring `R` and universal representation.
2. **Hypotheses/interfaces.** `W04.3.1`, absolute irreducibility, Schlessinger-
   style criteria, and finite-dimensional tangent space.
3. **Proof idea.** Verify pro-representability conditions; identify infinitesimal
   deformations with a Selmer-type cohomology group; construct the universal
   object and prove its mapping property.
4. **Formal map.** No local exact theorem.
5. **Trust boundary.** Pro-representability and continuous group cohomology are
   major formal foundations.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (7 steps).** (1) prove scalar endomorphisms; (2) verify
   fiber-product compatibility; (3) identify the tangent functor; (4) prove its
   finiteness; (5) invoke/prove pro-representability; (6) construct universal
   `ρ_R`; (7) prove uniqueness and the mapping property.
9. **Composition rule.** Produces the `R` mapped to `T` in `W04.7.1`.
10. **Remaining debt/blocker.** No suitable end-to-end pro-representability
    library and Galois-cohomology integration are checked locally.

### M0387-WTW-W04.4.1 finite-flat and ordinary local conditions

1. **Exact target.** Define and prove representability/liftability of the local
   deformation conditions at primes dividing the level and at the residual
   characteristic, including finite-flat or ordinary alternatives as required.
2. **Hypotheses/interfaces.** Local restrictions of `ρ̄`, finite-flat group
   schemes or Fontaine-style conditions, ordinary filtrations, and local rings.
3. **Proof idea.** Specify allowable local lifts, prove invariance under strict
   equivalence/base change, and construct local deformation rings with the
   dimensions used by the global numerical criterion.
4. **Formal map.** No exact local package.
5. **Trust boundary.** Finite-flat classification and local `p`-adic Hodge
   theory are major external mathematical boundaries.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (7 steps).** (1) restrict to each decomposition group;
   (2) define the allowable local type; (3) prove conjugacy invariance; (4)
   prove base-change stability; (5) define the local functor; (6) prove
   representability/formal smoothness as applicable; (7) compute tangent
   dimensions.
9. **Composition rule.** Refines `W04.3` and supplies terms for `W04.4.2`.
10. **Remaining debt/blocker.** Required local representation and finite-flat
    infrastructure is not in the local closure.

### M0387-WTW-W04.4.2 tangent and Selmer control

1. **Exact target.** Identify global deformation tangent/cotangent spaces with
   Selmer/dual-Selmer groups and derive the dimension formula used to select
   auxiliary primes.
2. **Hypotheses/interfaces.** `W04.3--W04.4.1`, continuous Galois cohomology,
   local conditions, Poitou--Tate duality, and Euler characteristic formulas.
3. **Proof idea.** Interpret first-order lifts as `H¹`, impose local subspaces,
   identify obstructions/dual conditions, and apply global duality to compare
   dimensions.
4. **Formal map.** No local exact theorem.
5. **Trust boundary.** Poitou--Tate duality and global Euler-characteristic
   formulas are high-risk external theorems.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (7 steps).** (1) identify unrestricted cocycles; (2)
   quotient coboundaries; (3) impose local tangent subspaces; (4) define the
   Selmer group; (5) define orthogonal dual local conditions; (6) apply global
   duality; (7) derive the dimension/codimension relation.
9. **Composition rule.** Supplies the dual-Selmer dimension killed by
   `W04.5.1` and the numerical count in `W04.6.2`.
10. **Remaining debt/blocker.** Missing formal Galois-cohomology duality and
    exact match to the selected deformation conditions.

### M0387-WTW-W04.5.1 Taylor--Wiles prime existence

1. **Exact target.** For each sufficiently large `n`, choose a set `Q_n` of
   primes with `q ≡ 1 mod p^n`, prescribed distinct residual Frobenius
   eigenvalues, and cardinality sufficient to kill the dual Selmer group.
2. **Hypotheses/interfaces.** `W04.4.2`, irreducible residual representation,
   Chebotarev density, and linear algebra on cohomology restrictions.
3. **Proof idea.** For each nonzero dual-Selmer class, find a Frobenius whose
   restriction detects it while satisfying the eigenvalue condition; iterate
   to obtain the finite auxiliary set and add congruence control.
4. **Formal map.** No checked local theorem.
5. **Trust boundary.** Chebotarev density is a major theorem; compatible
   simultaneous prime selection must be explicit.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (7 steps).** (1) choose a basis of dual Selmer; (2)
   take a nonzero class; (3) build a detecting Galois element; (4) impose the
   distinct-eigenvalue condition; (5) apply Chebotarev with `q ≡ 1 mod p^n`;
   (6) iterate through the basis; (7) prove restriction injectivity and the
   cardinality bound.
9. **Composition rule.** Produces `Q_n` consumed by `W04.5.2` and `W04.6.1`.
10. **Remaining debt/blocker.** Chebotarev and the cohomological detection
    argument are not locally formalized for these representations.

### M0387-WTW-W04.5.2 auxiliary level structures

1. **Exact target.** Define the deformation rings `R_{Q_n}`, Hecke algebras
   `T_{Q_n}`, diamond-operator groups `Δ_n`, and modules at auxiliary level,
   with compatible augmentation maps back to the minimal problem.
2. **Hypotheses/interfaces.** `W04.5.1`, modular curves at raised level,
   local deformation conditions at `Q_n`, and group algebras.
3. **Proof idea.** Add a controlled local eigenline at every Taylor--Wiles
   prime; diamond operators produce the finite abelian group action; quotient
   by the augmentation ideal recovers minimal level.
4. **Formal map.** No local historical WTW package.
5. **Trust boundary.** Moduli-level comparison and freeness/control of
   cohomology at raised level.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (8 steps).** (1) define the added local condition;
   (2) form `R_{Q_n}`; (3) define the raised congruence subgroup; (4) form the
   Hecke module; (5) construct diamond action; (6) form `T_{Q_n}`; (7) define
   maps from the minimal objects; (8) prove augmentation recovers the minimal
   module/algebra.
9. **Composition rule.** Supplies the compatible finite-level system patched
   in `W04.6.1`.
10. **Remaining debt/blocker.** Raised-level modular curves, diamond actions,
    and the control theorem are not integrated locally.

### M0387-WTW-W04.6.1 patched rings and modules

1. **Exact target.** Build a limiting power-series/group-algebra object
   `S_∞`, patched deformation ring `R_∞`, and patched module `M_∞` from
   the auxiliary systems, with finite freeness/depth properties sufficient for
   descent to minimal level.
2. **Hypotheses/interfaces.** `W04.5.2`, compatible truncations, compactness or
   inverse-limit selection, complete local algebra, and module depth.
3. **Proof idea.** Re-index finite quotients, choose compatible subsequences or
   ultraproduct-style data, take inverse limits, and retain uniform generator
   and freeness bounds.
4. **Formal map.** Imperial has an abstract patching stack and source anchor
   `ker_RtoT_le_nilradical`, but it is `M3/E3`, not an integrated historical
   patching proof or modularity theorem.
5. **Trust boundary.** Inverse limits/compactness and commutative algebra; the
   precise 1995 construction must be matched before assigning `H0` to this leaf.
6. **Axiom report.** No local theorem. Imperial leaf was not independently
   built with a transitive allowed-axiom report.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (8 steps).** (1) choose compatible Artinian
   truncations; (2) record uniform generators; (3) pass to a compatible
   subsystem; (4) define `S_∞`; (5) define `R_∞`; (6) define `M_∞`; (7)
   prove finite generation/freeness over `S_∞`; (8) identify augmentation
   quotients with minimal objects.
9. **Composition rule.** Supplies the algebra/module pair used by the numerical
    criterion in `W04.6.2`.
10. **Remaining debt/blocker.** No exact source-to-formal construction and no
    checked specialization to the FLT deformation problem.

### M0387-WTW-W04.6.2 numerical criterion

1. **Exact target.** From the cotangent/congruence-size inequality and the
   patched module's depth/freeness, prove the surjection from deformation ring
   to Hecke algebra is an isomorphism and the relevant module is free.
2. **Hypotheses/interfaces.** `W04.4.2`, `W04.6.1`, complete-intersection
   algebra, Fitting ideals/lengths, and the precise Wiles--Lenstra numerical
   criterion.
3. **Proof idea.** Compare the deformation cotangent space with the Hecke
   congruence ideal; equality forces complete intersection and excludes a
   nonzero kernel.
4. **Formal map.** No checked local exact theorem. An abstract nilpotent-kernel
   statement is insufficient for the exact `R=T` conclusion without all
   hypotheses and reducedness/control.
5. **Trust boundary.** Commutative-algebra numerical criterion is the point at
   which the 1993 gap must not be smuggled back in.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (8 steps).** (1) identify the cotangent module; (2)
   identify the congruence module; (3) establish the length inequality; (4)
   apply the patched freeness/depth result; (5) upgrade inequality to equality;
   (6) prove complete-intersection structure; (7) show the comparison kernel
   vanishes; (8) prove module freeness.
9. **Composition rule.** Closes the algebraic engine used in `W04.7.2`.
10. **Remaining debt/blocker.** Exact criterion, all finiteness hypotheses, and
    their arithmetic verification are not formalized locally.

### M0387-WTW-W04.7.1 comparison map R to T

1. **Exact target.** Construct a canonical surjective local-ring map `R -> T`
   by showing the Hecke-valued modular representation is a deformation of the
   selected residual representation with the required local conditions.
2. **Hypotheses/interfaces.** `W04.1.2--W04.1.3`, `W04.3.2`, and local-global
   compatibility matching `W04.4.1`.
3. **Proof idea.** Apply the universal property of `R` to the representation
   valued in `T`; traces at Frobenius generate `T`, giving surjectivity.
4. **Formal map.** No local exact comparison map.
5. **Trust boundary.** Existence of a `T`-valued representation and
   Chebotarev/pseudorepresentation-to-representation identification.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (7 steps).** (1) construct the Hecke-valued
   representation; (2) reduce it to `ρ̄`; (3) verify determinant; (4)
   verify every local condition; (5) apply universality of `R`; (6) identify
   universal traces with Hecke operators; (7) prove these generate `T` and
   hence surjectivity.
9. **Composition rule.** Supplies the map whose kernel is eliminated in
   `W04.7.2`.
10. **Remaining debt/blocker.** The Hecke-valued representation and exact local
    compatibility are absent from local formalization.

### M0387-WTW-W04.7.2 minimal R equals T

1. **Exact target.** Prove the minimal comparison map `R -> T` is an
   isomorphism and the localized Hecke module has the required freeness.
2. **Hypotheses/interfaces.** `W04.6.2` and `W04.7.1`, with every patched-system
   and numerical hypothesis explicitly instantiated.
3. **Proof idea.** Feed the arithmetic comparison map and numerical equality
   into the corrected Taylor--Wiles algebraic engine.
4. **Formal map.** No local exact theorem; Imperial's abstract patching anchor
   is not this instantiated result.
5. **Trust boundary.** Taylor--Wiles 1995 is primary for the corrected
   ring-theoretic mechanism; exact theorem-location reconstruction is pending.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (5 steps).** (1) obtain the surjection `R -> T`; (2)
   instantiate the auxiliary systems; (3) obtain patched freeness; (4) apply
   the numerical criterion; (5) conclude isomorphism and minimal modularity
   lifting.
9. **Composition rule.** Delivers the minimal modularity-lifting theorem to
   `W04.8` and relevant base cases.
10. **Remaining debt/blocker.** No kernel-checked instantiation from the actual
    Galois representation to the abstract algebraic criterion.

### M0387-WTW-W04.8.1 level induction

1. **Exact target.** Extend minimal modularity lifting to representations with
   the finite set of additional ramified primes occurring for semistable
   elliptic curves.
2. **Hypotheses/interfaces.** `W04.7.2`, local deformation rings at an added
   prime, old/new Hecke comparison, and level raising/lowering control.
3. **Proof idea.** Add one ramified prime at a time, compare deformation and
   Hecke problems, and retain the numerical equality under the local change.
4. **Formal map.** No local exact theorem.
5. **Trust boundary.** Ihara-style lemmas and level comparison are major
   imported arithmetic results.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (7 steps).** (1) order the nonminimal primes; (2) set
   the minimal base; (3) assume lifting at the current level; (4) add one local
   condition; (5) compare new deformation rings; (6) compare Hecke modules and
   congruence ideals; (7) apply the criterion and iterate.
9. **Composition rule.** Feeds the local-global compatibility check in
   `W04.8.2`.
10. **Remaining debt/blocker.** Required Ihara/level-comparison results and
    their exact hypotheses are not formalized locally.

### M0387-WTW-W04.8.2 local-global compatibility

1. **Exact target.** Prove the representation attached to the semistable
   elliptic curve satisfies exactly the local types allowed by the nonminimal
   lifting theorem at every bad prime.
2. **Hypotheses/interfaces.** Semistability, Tate modules, Weil--Deligne/local
   descriptions, and the conditions from `W04.4.1`/`W04.8.1`.
3. **Proof idea.** Good primes are unramified; multiplicative primes have the
   Steinberg/Tate local form; at the residual prime use finite-flat/ordinary
   alternatives and verify the determinant.
4. **Formal map.** No exact local theorem.
5. **Trust boundary.** Local Langlands/local-global compatibility and Tate-curve
   descriptions.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (7 steps).** (1) enumerate bad primes; (2) handle good
   primes; (3) classify split/non-split multiplicative cases; (4) identify the
   local representation type; (5) handle the residual characteristic; (6)
   verify determinant and conductor; (7) assemble the global condition packet.
9. **Composition rule.** `W04.8.1 + W04.8.2 -> W04.9`.
10. **Remaining debt/blocker.** No checked theorem connects all semistable
    elliptic-curve local types to the selected deformation predicates.

### M0387-WTW-W04.9 semistable modularity terminal

1. **Exact target.** Every semistable elliptic curve over `ℚ` is modular.
2. **Hypotheses/interfaces.** `W04.2` residual base cases, `W04.7` minimal
   lifting, `W04.8` nonminimal lifting/local compatibility, and the curve's
   residual representations.
3. **Proof idea.** Split according to reducibility of mod `3`; use
   Langlands--Tunnell directly in the irreducible case and the 3--5 trick in
   the reducible case, then apply the appropriate modularity-lifting theorem.
4. **Formal map.** No local exact terminal theorem located.
5. **Trust boundary.** The complete Wiles plus Taylor--Wiles published package;
   this node cannot hide its children behind a citation.
6. **Axiom report.** None; no repo-local declaration exists.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (7 steps).** (1) take semistable `E`; (2) inspect
   `E[3]`; (3) if irreducible, obtain residual modularity; (4) apply lifting;
   (5) if reducible, perform the 3--5 construction; (6) transfer modularity
   through mod `5`; (7) conclude `E` modular in both cases.
9. **Composition rule.** Applied to the Frey curve using `W02.5`, producing the
   modularity input to `W07`.
10. **Remaining debt/blocker.** Every central child remains outside the local
    kernel-checked dependency closure.

## W05 Ribet level lowering

### M0387-WTW-W05.1 representation hypotheses

1. **Exact target.** Verify the Frey residual representation satisfies the
   irreducibility, oddness, determinant, modularity, finite-flat/local, and
   conductor hypotheses of the exact Ribet level-lowering theorem.
2. **Hypotheses/interfaces.** `W03.5`, modularity of the Frey curve from
   `W04.9`, and Ribet's theorem in a frozen statement.
3. **Proof idea.** Build a field-by-field hypothesis record, refusing to infer
   any condition merely from the phrase “Frey representation.”
4. **Formal map.** No local Ribet theorem or instantiated hypothesis packet.
5. **Trust boundary.** Ribet 1990 is primary; Serre 1987 supplies the
   representation/conductor architecture. Exact page/theorem mapping remains
   under `H1`.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (7 steps).** (1) insert irreducibility; (2) insert
   oddness; (3) insert cyclotomic determinant; (4) obtain modularity from
   `W04.9`; (5) insert finite-flat behavior at `p`; (6) insert unramified/local
   conditions elsewhere; (7) identify the starting conductor and weight.
9. **Composition rule.** Sole input record for `W05.2`.
10. **Remaining debt/blocker.** Exact Ribet theorem signature and every
    hypothesis-to-field mapping are not locally formalized.

### M0387-WTW-W05.2 conductor lowering

1. **Exact target.** Remove every odd prime divisor of `ABC` from the residual
   conductor, leaving the precise power-of-two endpoint required for weight
   two and ultimately level `2`.
2. **Hypotheses/interfaces.** `W02.6`, `W03.4`, and the lowering theorem's local
   conductor criterion.
3. **Proof idea.** At an odd prime `ℓ | ABC`, the Frey discriminant valuation
   is divisible by `p`; the residual representation has the local behavior
   permitting `ℓ` to be removed. Iterate, then perform the separate
   `2`-adic calculation.
4. **Formal map.** No local exact theorem.
5. **Trust boundary.** Local conductor comparison and the prime `2` endpoint.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (7 steps).** (1) list odd primes dividing `ABC`; (2)
   fix one `ℓ`; (3) compute `vℓ(Δ)`; (4) prove its divisibility by `p`;
   (5) apply the local removal criterion; (6) iterate over the finite set; (7)
   use the `2`-adic calculation to identify the endpoint.
9. **Composition rule.** Produces the lowered conductor used by `W05.3`.
10. **Remaining debt/blocker.** No checked local removal criterion or endpoint
    calculation exists in this repository.

### M0387-WTW-W05.3 modular level transition

1. **Exact target.** From a modular residual representation at the original
   Frey level, obtain a weight-two newform at the lowered level, preserving the
   residual representation.
2. **Hypotheses/interfaces.** `W05.1--W05.2`, degeneracy maps, old/new
   decompositions, and Ribet's level-lowering theorem.
3. **Proof idea.** Apply lowering one prime at a time and choose the new quotient
   at each stage; identify Hecke eigenvalues modulo the residual prime.
4. **Formal map.** No local exact theorem.
5. **Trust boundary.** Ribet's theorem is the central imported proof body, not
   a computational simplification.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (6 steps).** (1) start with the modular eigen-system;
   (2) choose a removable prime; (3) apply the local level-lowering theorem;
   (4) pass to the new quotient; (5) preserve residual Frobenius traces; (6)
   iterate to the conductor from `W05.2`.
9. **Composition rule.** Delivers the level-two eigenform asserted in `W05.4`.
10. **Remaining debt/blocker.** Modular curves/Hecke algebra lowering
    infrastructure is not locally checked.

### M0387-WTW-W05.4 lowered representation terminal

1. **Exact target.** Produce a normalized weight-two newform of level `2` whose
   mod-`p` representation is isomorphic to the Frey residual representation.
2. **Hypotheses/interfaces.** `W05.3` and the exact prime-two conductor result.
3. **Proof idea.** Package the terminal newform, its level/weight/newness, and
   the representation isomorphism without weakening any field.
4. **Formal map.** No local declaration.
5. **Trust boundary.** Complete Ribet/level-lowering package.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (4 steps).** (1) take the final lowered eigen-system;
   (2) select its normalized newform; (3) prove weight `2` and level `2`; (4)
   record the residual representation isomorphism.
9. **Composition rule.** Supplies the purported element excluded by `W06.3`.
10. **Remaining debt/blocker.** No repo-local term constructs this newform.

## W06 level-two modular-form impossibility

### M0387-WTW-W06.1 identify weight two and level two

1. **Exact target.** Convert `W05.4` into a nonzero element of
   `S₂(Γ₀(2))`.
2. **Hypotheses/interfaces.** A normalized newform of weight `2`, level `2`, and
   the definition of the cusp-form space.
3. **Proof idea.** Forget the eigen/newform structure but retain membership in
   the ambient cusp space; normalized first Fourier coefficient proves nonzero.
4. **Formal map.** No local declaration.
5. **Trust boundary.** Definitional bridge between newforms and cusp forms.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (4 steps).** (1) take the terminal newform; (2) coerce
   it to the cusp space; (3) retain level and weight indices; (4) use `a₁=1`
   to prove it is nonzero.
9. **Composition rule.** Creates the witness contradicted by `W06.2`.
10. **Remaining debt/blocker.** Newform/cusp-form object models are not present
    in the local FLT chain.

### M0387-WTW-W06.2 compute S2(Gamma0(2)) equals zero

1. **Exact target.** Prove `S₂(Γ₀(2)) = {0}` (equivalently its dimension
   is zero).
2. **Hypotheses/interfaces.** Identification of weight-two cusp forms with
   holomorphic differentials on `X₀(2)`, and a genus/dimension formula or an
   independently verified modular-symbol/Sturm certificate.
3. **Proof idea.** Use the index/cusp/elliptic-point genus formula for `X₀(2)`:
   compute index `3`, two cusps, one elliptic orbit of order `2`, and no orbit
   of order `3`; obtain genus `0`; hence the space of holomorphic differentials,
   and therefore `S₂`, has dimension `0`.
4. **Formal map.** No checked local calculation. A future finite computation
   is legal only with a kernel-checked certificate and explicit checker.
5. **Trust boundary.** Modular-curve genus formula and the cusp-form/
   differential isomorphism; alternatively a named certified computation.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (9 steps).** (1) compute
   `[Γ(1):Γ₀(2)]=3`; (2) enumerate cusps and obtain `c=2`; (3) compute
   one elliptic orbit of order `2`; (4) compute none of order `3`; (5) insert
   these into the compactified modular-curve genus formula; (6) simplify to
   `g(X₀(2))=0`; (7) identify `S₂(Γ₀(2))` with holomorphic
   differentials; (8) use `dim H⁰(X,Ω¹)=g`; (9) conclude the space is zero.
9. **Composition rule.** Combined with `W06.1`, excludes the lowered newform.
10. **Remaining debt/blocker.** Neither the modular-curve genus calculation
    nor a certified alternative is in the local Lean closure.

### M0387-WTW-W06.3 no level-two newform

1. **Exact target.** Prove there is no normalized weight-two newform of level
   `2`.
2. **Hypotheses/interfaces.** `W06.1` coercion/nonzeroness and `W06.2` zero-space
   theorem.
3. **Proof idea.** A normalized newform would be a nonzero vector in a zero
   vector space.
4. **Formal map.** Planned contradiction theorem; no local declaration.
5. **Trust boundary.** No additional mathematics after the two inputs.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (3 steps).** (1) suppose the newform exists; (2) map it
   to the nonzero cusp form of `W06.1`; (3) use `W06.2` to identify it with zero
   and contradict nonzeroness.
9. **Composition rule.** Supplies the negative terminal used by `W07`.
10. **Remaining debt/blocker.** Depends on the open `W06.1--W06.2` formal nodes.

## W07--W09 composition

### M0387-WTW-W07 Frey contradiction

1. **Exact target.** For every prime `p ≥ 5`, prove
   `FermatLastTheoremFor p` by contradiction through the normalized Frey route.
2. **Hypotheses/interfaces.** `W01`, Frey construction/data `W02--W03`,
   semistable modularity `W04.9`, level lowering `W05.4`, and impossibility
   `W06.3`.
3. **Proof idea.** A counterexample gives a semistable Frey curve. Modularity
   makes its representation modular; Ribet lowers it to an impossible level-two
   newform.
4. **Formal map.** No checked local composition theorem.
5. **Trust boundary.** Exactly the named child packages; no hidden theorem.
6. **Axiom report.** None; planned target.
7. **H/M/R vector.** `[H1, M4, R0]`.
8. **Independent ledger (7 steps).** (1) assume a nontrivial solution; (2)
   normalize it with `W01`; (3) construct and analyze the Frey curve via
   `W02--W03`; (4) apply semistable modularity; (5) apply Ribet level lowering;
   (6) obtain a level-two newform; (7) contradict `W06.3`.
9. **Composition rule.** `W01 + W02 + W03 + W04.9 + W05.4 + W06.3 -> W07`.
10. **Remaining debt/blocker.** Every central machine child `W02--W06` is open.

### M0387-WTW-W08 all odd-prime exponents

1. **Exact target.** Construct
   `∀ p : ℕ, Nat.Prime p -> Odd p -> FermatLastTheoremFor p`.
2. **Hypotheses/interfaces.** Checked `flt3Path`, prime arithmetic, and `W07`
   for `p ≥ 5`.
3. **Proof idea.** An odd prime is `3` or at least `5`; dispatch the former to
   the checked exponent-three theorem and the latter to `W07`.
4. **Formal map.** Exact target is the local definition
   `OddPrimeExponentClosure`, but no proof term inhabits it.
5. **Trust boundary.** Pinned mathlib for `p=3`; historical open branch for
   `p≥5`.
6. **Axiom report.** `flt3Path` reports only accepted baseline axioms, but the
   composite has no axiom report because no declaration exists.
7. **H/M/R vector.** `[H1, M2, R0]`; one branch is machine closed, the general
   branch is not.
8. **Independent ledger (5 steps).** (1) fix odd prime `p`; (2) use prime
   arithmetic to split `p=3` or `5≤p`; (3) in the first case apply `flt3Path`;
   (4) in the second apply `W07`; (5) abstract over `p`.
9. **Composition rule.** `B3.5 + W07 -> W08`; supplies the sole premise of
   `W09`.
10. **Remaining debt/blocker.** `W07` has no machine proof.

### M0387-WTW-W09 exact root recomposition

1. **Exact target.** Produce the exact proposition `FermatLastTheorem` from
   `W08` using the checked exponent-four/recomposition theorem.
2. **Hypotheses/interfaces.** `W08`, checked `fermatLastTheoremFour`, and
   checked `FermatLastTheorem.of_odd_primes`.
3. **Proof idea.** For each exponent `n ≥ 3`, mathlib finds either `4 | n` or
   an odd prime divisor; divisor monotonicity transports the corresponding
   fixed-exponent result.
4. **Formal map.** The checked local conditional edge is
   `fermatLastTheoremRootOfOddPrimesPath`. It has exactly the required premise
   but is not an unconditional root declaration.
5. **Trust boundary.** Recomposition proof body is in pinned mathlib
   `Mathlib.NumberTheory.FLT.Four`; the missing input would come from `W08`.
6. **Axiom report.** Conditional wrapper uses only the accepted baseline
   `[propext, Classical.choice, Quot.sound]`; there is no exact unconditional
   terminal report.
7. **H/M/R vector.** `[H1, M2, R0]`.
8. **Independent ledger (5 steps).** (1) assume the all-odd-prime family from
   `W08`; (2) fix `n ≥ 3`; (3) split into `4 | n` or odd prime `p | n`; (4)
   apply the corresponding fixed-exponent theorem and monotonicity; (5)
   abstract over `n` to obtain the root.
9. **Composition rule.** `W08 + B4.8 + R05 -> M0387-ROOT`.
10. **Remaining debt/blocker.** The checked conditional theorem cannot be
    applied because `W08` is not locally proved. Exact FLT machine closure is
    therefore absent.

## Readable conclusion

The historical route is complete as an architecture: every major construction,
local/global bridge, imported theorem, case split, patching layer, computation,
and final composition has a named node and an independent ledger below 100
steps. The route is not complete as Lean. In particular, readable `R0` does
not upgrade any `M4` leaf, and the historically accepted theorem does not
become `H0` at project-leaf granularity until the exact source-location and
assumption crosswalk is finished.
