# THM-M-1356 frozen obligation architecture

Item: `S56-M-1356-OBLIGATION_TREE`.

Registry version 1 freezes 50 canonical obligations before proof-phase closure credit.
The route expands Barkovsky's one-line proof of Theorem 40 through the Hermite root-count
bridge, Cauchy-index and Sturm theorems, the regular and nonregular Routh cases, no-pivot
Gaussian elimination of the finite Hurwitz matrix, both logical directions, and exact root
assembly. Provenance, evidence, trust, documentation, and workflow edges remain separate
from mathematical proof requirements.

## Proof route

```text
ROOT -> exact direction assembly
  stable -> positive minors
    complete Routh criterion -> Hermite -> Cauchy index -> Sturm variations
                             -> regular signs + nonregular terminal cases
    Hurwitz minors -> no-pivot elimination -> products of Routh coefficients
  positive minors -> stable (same two engines, reverse implication)
```

Only the two final abstract-child composition declarations are checked here. Every internal
source route is an explicitly unverified decomposition until a future Lean harness consumes
the exact child fingerprints. No source, provenance, trust, or documentation edge can close
a proof obligation.

## Node ledger

<a id="m1356-root"></a>
### M1356-ROOT

For every frozen positive-degree coefficient vector, strict left-half-plane stability is equivalent to positivity of every finite leading Hurwitz minor.

Formal target: `Stage1Instances.THM_M_1356.RouthHurwitzTarget`

Output: The exact canonical proposition.

Source boundary: Statement.lean; elaborated expression sha256 7901eb74686f457348ec06812b8584c69eb09649779637cbb28b2e7bd84b98bf

Step budget: `10`; structured ledger entries: `2`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-s-statement"></a>
### M1356-S-STATEMENT

Preserve the exact degree, coefficient, root, matrix, minor, quantifier, implication, and strict-inequality interfaces.

Formal target: `Stage1Instances.THM_M_1356.{RouthHurwitzTarget,IsStrictlyStable,hurwitzMinor}`

Output: The exact input and output interfaces used by every composition edge.

Source boundary: Statement.lean: sourceCoefficient through RouthHurwitzTarget; Barkovsky pp. 6, 18-19

Step budget: `16`; structured ledger entries: `1`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-s-coefficient"></a>
### M1356-S-COEFFICIENT

Relate descending source coefficients to Polynomial.ofFn, prove coefficient n is a_0, prevent degree drop, and map the real polynomial to Complex.

Formal target: `Stage1Instances.THM_M_1356.{realPolynomial_coeff_degree,realPolynomial_natDegree_eq,complexPolynomial}`

Output: A degree-exact real-to-complex polynomial matching a_0 z^n + ... + a_n.

Source boundary: Statement.lean: sourceCoefficient and realPolynomial adapters; Barkovsky p. 19 eq. (38)

Step budget: `28`; structured ledger entries: `1`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-s-boundaries"></a>
### M1356-S-BOUNDARIES

Retain n > 0, a_0 > 0, exact degree n, strict open half-plane, all n strict minors, and the imaginary-axis/nonregular cases needed by the reverse direction.

Formal target: `Boundary package for Stage1Instances.THM_M_1356.RouthHurwitzTarget`

Output: No zero-degree, degree-drop, non-strict, selected-minor, or regular-only substitute enters the proof.

Source boundary: Statement.lean binders and mutations; Barkovsky pp. 16-20, Theorems 34 and 40

Step budget: `24`; structured ledger entries: `1`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-s-foundation"></a>
### M1356-S-FOUNDATION

Account for classical finite-root arguments, real-to-complex algebra, determinant reasoning, extensionality, the kernel, and the no-oracle policy.

Formal target: `Future axiom, dependency, and TCB report for every terminal declaration`

Output: An accepted foundation and trust boundary for all proof bodies.

Source boundary: Statement receipt profiles; anchor-audit immutable environment

Step budget: `24`; structured ledger entries: `1`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-c-even-odd"></a>
### M1356-C-EVEN-ODD

Split the normalized imaginary-axis evaluation into the alternating real polynomials f_0 and f_1 and prove their coefficient, degree, and common-root identities.

Formal target: `Planned signature: exists_evenOddPair_for_imaginaryAxis`

Output: Real polynomials f_0,f_1 with i^(-n)p(i*w)=f_0(w)-i*f_1(w) and an exact imaginary-axis common-root criterion.

Source boundary: Barkovsky p. 10 eqs. (9)-(12)

Step budget: `46`; structured ledger entries: `3`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-c-even-odd-defs"></a>
### M1356-C-EVEN-ODD-DEFS

Define the alternating real polynomials f_0,f_1 and prove the normalized imaginary-axis evaluation, displayed coefficient formulas, and degree inequality.

Formal target: `Planned signature: alternatingPair_evaluation_and_degree`

Output: i^(-n)p(i*w)=f_0(w)-i*f_1(w), the source coefficient rows (11), and deg f_1 < deg f_0.

Source boundary: Barkovsky p. 10, eqs. (9)-(11)

Step budget: `34`; structured ledger entries: `1`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-l-imag-common-root"></a>
### M1356-L-IMAG-COMMON-ROOT

Identify imaginary-axis roots of p with common real roots of f_0,f_1 and hence real roots of their gcd.

Formal target: `Planned signature: imaginaryRoot_iff_evenOddGcdRoot`

Output: p(i*w)=0 iff f_0(w)=f_1(w)=0 iff gcd(f_0,f_1)(w)=0.

Source boundary: Barkovsky p. 10, eq. (12)

Step budget: `24`; structured ledger entries: `2`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-c-sturm"></a>
### M1356-C-STURM

Construct the signed Euclidean Sturm/Routh sequence from f_0,f_1, including degree decrease, termination, sign-change invariants, and the possible final zero cases.

Formal target: `Planned signature: exists_routhSturmSequence`

Output: A finite Routh sequence with leading coefficients h_0,...,h_n and a complete regular/nonregular terminal classification.

Source boundary: Barkovsky pp. 13-17, eqs. (19)-(33)

Step budget: `72`; structured ledger entries: `6`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-c-signed-remainder"></a>
### M1356-C-SIGNED-REMAINDER

Define one signed Euclidean step f_(k-1) = d_k f_k - f_(k+1) and prove the new remainder has strictly smaller degree when nonzero.

Formal target: `Planned signature: signedRemainder_step`

Output: A next polynomial with the required sign convention and strict degree descent.

Source boundary: Barkovsky p. 14, eq. (25)

Step budget: `44`; structured ledger entries: `1`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-c-sturm-termination"></a>
### M1356-C-STURM-TERMINATION

Iterate signed remainders until the first zero remainder and prove termination, finite indexing, and the greatest-common-divisor terminal invariant.

Formal target: `Planned signature: signedRemainder_terminates_with_gcd`

Output: A finite sequence ending at a nonzero gcd, with every earlier degree strictly descending.

Source boundary: Barkovsky pp. 14, 16-17, eq. (25) and Theorem 34 proof

Step budget: `62`; structured ledger entries: `2`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-c-sturm-invariants"></a>
### M1356-C-STURM-INVARIANTS

Prove the signed-remainder sequence satisfies the Sturm non-simultaneous-zero and opposite-neighbor-sign conditions.

Formal target: `Planned signature: signedRemainder_isSturmSequence`

Output: The exact Sturm conditions needed by Theorem 26 for every nonterminal prefix.

Source boundary: Barkovsky pp. 12-14, conditions (19)-(21) and eq. (25)

Step budget: `58`; structured ledger entries: `2`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-c-routh-recurrence"></a>
### M1356-C-ROUTH-RECURRENCE

Specialize the signed remainder step to alternating coefficients and prove the array update records the next leading coefficient and preserves the alternating row shape.

Formal target: `Planned signature: routhArray_step_matches_signedRemainder`

Output: A Routh array whose stored h_k are exactly the Sturm-polynomial leading coefficients.

Source boundary: Barkovsky pp. 15-16, eqs. (26)-(28) and Routh routine

Step budget: `66`; structured ledger entries: `3`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-l-hermite"></a>
### M1356-L-HERMITE

Relate the argument increment of the imaginary-axis hodograph to the difference between left- and right-half-plane root counts.

Formal target: `Planned signature: hermite_hodograph_root_count`

Output: Delta_p = pi * (n_minus - n_plus) when there is no imaginary-axis root.

Source boundary: Barkovsky pp. 8-9, Theorem 6 and Lemma 5

Step budget: `58`; structured ledger entries: `3`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-l-linear-hodograph"></a>
### M1356-L-LINEAR-HODOGRAPH

Compute the argument increment of the normalized imaginary-axis hodograph for one linear factor z-lambda with nonzero real part.

Formal target: `Planned signature: linearFactor_hodographIncrement`

Output: Delta_(z-lambda) = -pi * sign(re lambda).

Source boundary: Barkovsky p. 8, Lemma 5

Step budget: `32`; structured ledger entries: `1`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-l-hodograph-product"></a>
### M1356-L-HODOGRAPH-PRODUCT

Prove argument increments add under multiplication and account for the positive leading scalar and all complex roots with multiplicity.

Formal target: `Planned signature: hodographIncrement_factorization`

Output: The increment of p is the sum of the increments of its linear factors.

Source boundary: Barkovsky pp. 8-9, Theorem 6 proof

Step budget: `42`; structured ledger entries: `2`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-l-cauchy-index"></a>
### M1356-L-CAUCHY-INDEX

Convert half-plane root counts into the Cauchy index of f_1/f_0, without assuming the desired stability criterion.

Formal target: `Planned signature: halfPlaneRootCount_eq_cauchyIndex`

Output: n_minus - n_plus = Ind_{-infinity}^{+infinity}(f_1/f_0).

Source boundary: Barkovsky pp. 10-12, Lemmas 15-17 and Theorem 18

Step budget: `68`; structured ledger entries: `4`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-l-crossing-interior"></a>
### M1356-L-CROSSING-INTERIOR

Compute the hodograph argument increment between consecutive imaginary-axis crossings from their oriented crossing indices.

Formal target: `Planned signature: argumentIncrement_between_crossings`

Output: Each interior increment is pi/2 times the sum of its two crossing indices.

Source boundary: Barkovsky p. 11, Lemma 15

Step budget: `38`; structured ledger entries: `1`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-l-crossing-ends"></a>
### M1356-L-CROSSING-ENDS

Compute the two unbounded-end argument increments from degree f_1 < degree f_0 and the first and last crossing indices.

Formal target: `Planned signature: argumentIncrement_at_infinite_ends`

Output: The two end increments are pi/2 times the first and last crossing indices.

Source boundary: Barkovsky pp. 11-12, Lemma 16

Step budget: `42`; structured ledger entries: `1`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-l-crossing-sum"></a>
### M1356-L-CROSSING-SUM

Sum the disjoint interior and end intervals, including the no-crossing case, and identify the sum of crossing indices with the Cauchy index.

Formal target: `Planned signature: hodographIncrement_eq_cauchyIndex`

Output: Delta_p = pi * Ind(f_1/f_0).

Source boundary: Barkovsky p. 12, Lemma 17 and definitions (15)-(17)

Step budget: `50`; structured ledger entries: `3`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-l-sturm-index"></a>
### M1356-L-STURM-INDEX

Compute the Cauchy index from a signed Sturm sequence, including discontinuity jumps and limiting sign variations.

Formal target: `Planned signature: cauchyIndex_eq_sturmVariation`

Output: The Cauchy index is V(-infinity)-V(+infinity), with the regular leading-coefficient formula as a corollary.

Source boundary: Barkovsky pp. 12-14, Lemmas 24-25 and Theorems 26 and 28

Step budget: `78`; structured ledger entries: `4`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-l-sturm-nojump"></a>
### M1356-L-STURM-NOJUMP

Show the sign-variation count has no jump at a point that is not an odd-multiplicity zero of f_0.

Formal target: `Planned signature: sturmVariation_noJump`

Output: Equal left and right limits of V at every non-pole discontinuity candidate.

Source boundary: Barkovsky p. 13, Lemma 24

Step budget: `44`; structured ledger entries: `1`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-l-sturm-pole-jump"></a>
### M1356-L-STURM-POLE-JUMP

At every odd-multiplicity zero of f_0, identify the jump of sign variation with minus the local Cauchy index.

Formal target: `Planned signature: sturmVariation_jump_eq_neg_index`

Output: V(c+)-V(c-) = -Ind_c(f_1/f_0).

Source boundary: Barkovsky p. 13, Lemma 25

Step budget: `42`; structured ledger entries: `1`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-l-sturm-global"></a>
### M1356-L-STURM-GLOBAL

Sum every jump of the finite sign-variation step function to obtain Sturm's global Cauchy-index formula.

Formal target: `Planned signature: cauchyIndex_eq_variationDifference`

Output: Ind_a^b(f_1/f_0) = V(a+)-V(b-).

Source boundary: Barkovsky pp. 13-14, Theorem 26

Step budget: `46`; structured ledger entries: `3`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-l-sturm-infinity"></a>
### M1356-L-STURM-INFINITY

For a regular degree-descending sequence, compute both infinite-end sign variations from the leading coefficients.

Formal target: `Planned signature: regularSturm_index_eq_leadingSignChanges`

Output: Ind = n - 2*v(h_0,...,h_n).

Source boundary: Barkovsky p. 14, Theorem 28

Step budget: `40`; structured ledger entries: `3`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-l-routh-regular"></a>
### M1356-L-ROUTH-REGULAR

In the regular case, prove stability iff the Routh procedure terminates and all nonzero leading coefficients h_0,...,h_n have one sign.

Formal target: `Planned signature: stable_iff_routh_regular_sameSign`

Output: The regular Routh sign criterion in both directions.

Source boundary: Barkovsky p. 16, Theorem 33

Step budget: `52`; structured ledger entries: `3`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-b-routh-necessity"></a>
### M1356-B-ROUTH-NECESSITY

From stability derive extreme sign variations at both infinities, maximal Sturm-sequence length, regularity, and one common nonzero sign for all h_k.

Formal target: `Planned signature: stable_implies_routhRegular_sameSign`

Output: The necessity direction of Barkovsky Theorem 33.

Source boundary: Barkovsky p. 16, Theorem 33 proof using Theorems 18 and 26

Step budget: `32`; structured ledger entries: `4`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-b-routh-sufficiency"></a>
### M1356-B-ROUTH-SUFFICIENCY

From regularity and one common nonzero sign for all h_k derive zero sign variation, exact root counts, and strict stability.

Formal target: `Planned signature: routhRegular_sameSign_implies_stable`

Output: The sufficiency direction of Barkovsky Theorem 33.

Source boundary: Barkovsky p. 16, Theorem 33 proof using Theorems 28 and 18

Step budget: `28`; structured ledger entries: `4`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-b-nonregular"></a>
### M1356-B-NONREGULAR

Classify all terminal h_(n-1),h_n zero/sign cases, remove the gcd representing imaginary-axis roots where required, and recompose an exhaustive boundary result.

Formal target: `Planned signature: routh_terminal_cases`

Output: Exact root counts and imaginary-axis-root status for every Routh terminal case.

Source boundary: Barkovsky pp. 16-17, Theorem 34 cases (a)-(e)

Step budget: `82`; structured ledger entries: `9`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-b-terminal-split"></a>
### M1356-B-TERMINAL-SPLIT

Split exhaustively on h_(n-1), h_n, and the sign of h_(n-2)*h_n, with disjoint cases matching Theorem 34.

Formal target: `Planned signature: routhTerminal_exhaustiveCases`

Output: Exactly one of terminal cases A through E.

Source boundary: Barkovsky pp. 16-17, Theorem 34 cases (a)-(e)

Step budget: `28`; structured ledger entries: `1`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-b-terminal-a"></a>
### M1356-B-TERMINAL-A

When h_(n-1) and h_n are nonzero, prove regularity, absence of imaginary-axis roots, and the two sign-variation root counts.

Formal target: `Planned signature: routhTerminal_caseA`

Output: Theorem 34(a), including formula (29).

Source boundary: Barkovsky pp. 16-17, Theorem 34(a)

Step budget: `42`; structured ledger entries: `2`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-b-terminal-b"></a>
### M1356-B-TERMINAL-B

When h_(n-1) is nonzero and h_n is zero, identify the gcd as omega and remove the one simple root at zero before recounting.

Formal target: `Planned signature: routhTerminal_caseB`

Output: Theorem 34(b), including formula (30).

Source boundary: Barkovsky pp. 16-17, Theorem 34(b)

Step budget: `48`; structured ledger entries: `2`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-b-terminal-c"></a>
### M1356-B-TERMINAL-C

When h_(n-1)=0 and h_(n-2)*h_n<0, prove the quadratic terminal gcd has no real zero and compute root counts by Sturm's general formula.

Formal target: `Planned signature: routhTerminal_caseC`

Output: Theorem 34(c), including formula (31).

Source boundary: Barkovsky pp. 16-17, Theorem 34(c)

Step budget: `48`; structured ledger entries: `2`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-b-terminal-d"></a>
### M1356-B-TERMINAL-D

When h_(n-1)=0 and h_(n-2)*h_n>0, remove the two simple nonzero imaginary-axis roots encoded by the quadratic gcd and recount.

Formal target: `Planned signature: routhTerminal_caseD`

Output: Theorem 34(d), including formula (32).

Source boundary: Barkovsky pp. 16-17, Theorem 34(d)

Step budget: `52`; structured ledger entries: `2`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-b-terminal-e"></a>
### M1356-B-TERMINAL-E

When h_(n-1)=h_n=0, remove the double zero root encoded by the quadratic gcd and recount.

Formal target: `Planned signature: routhTerminal_caseE`

Output: Theorem 34(e), including formula (33).

Source boundary: Barkovsky pp. 16-17, Theorem 34(e)

Step budget: `48`; structured ledger entries: `2`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-t-gcd-correction"></a>
### M1356-T-GCD-CORRECTION

Divide p by the polynomial corresponding to the normalized gcd of f_0,f_1, prove the exact root-multiset removal, and transport half-plane counts back to p.

Formal target: `Planned signature: removeImaginaryAxisGcd_and_transport_counts`

Output: A checked bridge used by terminal cases B, D, and E, with no lost multiplicity or changed half-plane convention.

Source boundary: Barkovsky p. 17, Theorem 34 proof after formulas (29)-(33)

Step budget: `70`; structured ledger entries: `3`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-l-routh-criterion"></a>
### M1356-L-ROUTH-CRITERION

Combine Hermite root counting, Cauchy indices, Sturm variation, the regular sign theorem, and the nonregular terminal cases into the complete Routh criterion.

Formal target: `Planned signature: stable_iff_routhLeadingCoefficientsPositive`

Output: For a_0 > 0, stability iff the full Routh leading-coefficient package is positive, with nonregular cases excluded for the correct reason.

Source boundary: Barkovsky pp. 8-17, Theorems 6, 18, 26, 28, 33, and 34

Step budget: `34`; structured ledger entries: `7`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-l-gauss"></a>
### M1356-L-GAUSS

Perform no-pivot Gaussian elimination on every leading Hurwitz block and show each row operation preserves every relevant leading principal determinant.

Formal target: `Planned signature: hurwitzLeadingBlocks_eliminate_to_routh`

Output: The first k Hurwitz block reduces to an upper triangular block with diagonal h_1,...,h_k without changing its determinant.

Source boundary: Barkovsky pp. 18-19, Lemma 39 proof and eqs. (26)-(28)

Step budget: `74`; structured ledger entries: `5`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-l-gauss-step"></a>
### M1356-L-GAUSS-STEP

Show one no-pivot row subtraction eliminates the lower leading entry, preserves the determinant of every enclosing leading block, and produces coefficients of the next Routh polynomial.

Formal target: `Planned signature: hurwitzBlock_oneEliminationStep`

Output: One determinant-preserving reduction from the (f_(k-1),f_k) block to the (f_k,f_(k+1)) block.

Source boundary: Barkovsky pp. 15, 18, eqs. (26)-(28) and Lemma 39 proof

Step budget: `52`; structured ledger entries: `2`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-l-gauss-shape"></a>
### M1356-L-GAUSS-SHAPE

Inductively preserve the shifted Hurwitz block shape after crossing out the completed row and column.

Formal target: `Planned signature: hurwitzBlock_recursiveShape`

Output: After k steps, the remaining block is the Hurwitz-shaped block of f_k,f_(k+1).

Source boundary: Barkovsky p. 18, Lemma 39 proof

Step budget: `58`; structured ledger entries: `2`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-l-triangular-det"></a>
### M1356-L-TRIANGULAR-DET

Compute every leading determinant of the resulting upper triangular matrix as the product of its first k diagonal Routh coefficients.

Formal target: `Planned signature: leadingDet_upperTriangular_eq_diagonalProduct`

Output: eta_k = product_{1<=j<=k} h_j after the determinant-preserving elimination sequence.

Source boundary: Barkovsky p. 19, Lemma 39 and eq. (37)

Step budget: `38`; structured ledger entries: `2`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-l-minor-product"></a>
### M1356-L-MINOR-PRODUCT

Deduce eta_k = h_1*...*h_k for every regular prefix and handle the last-minor identity and zero cases without dividing by an unproved nonzero minor.

Formal target: `Planned signature: hurwitzMinor_eq_routhLeadingProduct`

Output: An exact indexed product identity connecting finite Hurwitz minors to Routh leading coefficients.

Source boundary: Barkovsky pp. 18-19, eqs. (35)-(37) and Lemma 39

Step budget: `48`; structured ledger entries: `3`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-b-stable-to-minors"></a>
### M1356-B-STABLE-TO-MINORS

Use the complete Routh criterion and the determinant product identity to derive strict positivity of every leading Hurwitz minor from strict stability.

Formal target: `Stage1Instances.THM_M_1356.ObligationTree.StableToPositiveMinorsTarget`

Output: The exact forward implication at every frozen binder.

Source boundary: Barkovsky p. 19, Theorem 40 necessity via Lemma 39 and Theorems 33-34

Step budget: `30`; structured ledger entries: `3`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-b-minors-to-stable"></a>
### M1356-B-MINORS-TO-STABLE

Use positive leading minors to derive positive nonzero Routh coefficients, rule out every nonregular/imaginary-axis case, and conclude strict stability.

Formal target: `Stage1Instances.THM_M_1356.ObligationTree.PositiveMinorsToStableTarget`

Output: The exact reverse implication at every frozen binder.

Source boundary: Barkovsky p. 19, Theorem 40 sufficiency via Lemma 39 and Theorems 33-34

Step budget: `36`; structured ledger entries: `3`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-t-assemble"></a>
### M1356-T-ASSEMBLE

Assemble the exact forward and reverse implication packages at the unchanged canonical binders.

Formal target: `Stage1Instances.THM_M_1356.ObligationTree.root_of_directions`

Output: Stage1Instances.THM_M_1356.RouthHurwitzTarget.

Source boundary: ObligationTree.lean conditional composition harness

Step budget: `12`; structured ledger entries: `3`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-x-source"></a>
### M1356-X-SOURCE

Map every material proof node to reviewed primary and modern sources, assumptions, proof steps, translation choices, corrections, and errata.

Formal target: `Node-specific human-source crosswalk`

Output: Human-source evidence without machine-proof credit.

Source boundary: Hurwitz 1895 pp. 273-284; Barkovsky arXiv:0802.1805v1 pp. 6-19

Step budget: `40`; structured ledger entries: `1`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-x-provenance"></a>
### M1356-X-PROVENANCE

Resolve every future local or imported terminal declaration, body, revision, license, dependency, wrapper, placeholder scan, and receipt without duplicate credit.

Formal target: `Future transitive proof-body provenance report`

Output: Proof provenance and evidence coverage without mathematical proof credit.

Source boundary: anchor-audit.json exact negative candidate inventory

Step budget: `36`; structured ledger entries: `1`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-x-trust"></a>
### M1356-X-TRUST

Audit the Lean/mathlib declaration closure, axioms, compiled artifacts, executables, unsafe/oracle boundaries, hermetic replay, and independent verification.

Formal target: `Future release-grade foundation and TCB closure`

Output: A release trust decision without mathematical proof credit.

Source boundary: Lean 4.29.0; mathlib 8a178386; anchor-audit immutable environment

Step budget: `40`; structured ledger entries: `1`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-x-readable"></a>
### M1356-X-READABLE

Produce a fingerprint-linked, independently reviewed readable reconstruction for every required obligation, explicitly labeling every machine-open node.

Formal target: `Future node-specific R0 records`

Output: Readable coverage without machine-proof or human-source credit.

Source boundary: Docs/Stage1_Blueprint_rev-5.6.md sections 8 and 9

Step budget: `32`; structured ledger entries: `1`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

<a id="m1356-x-workflow"></a>
### M1356-X-WORKFLOW

Bind dependency-ordered task acceptance, structured recipes, receipts, reconciliation, freshness, and revocation without treating workflow success as proof.

Formal target: `Future Stage1 receipt and reconciliation closure`

Output: A workflow acceptance decision without mathematical proof credit.

Source boundary: Docs/Stage1_Blueprint_rev-5.6.md sections 9 and 10

Step budget: `34`; structured ledger entries: `1`.

Boundary: frozen plan or checked conditional interface only; the mathematical output and root closure remain open.

## Freeze boundary

No obligation is accepted closed. The root remains `[H1, M3, R4]`: the exact proposition
elaborates, but no Lean proof body for either direction was discovered. Pinpoint proof/errata
review, every substantive machine node, readable `R0`, transitive provenance and trust,
hermetic replay, independent verification, audit completion, theorem completion, and master
acceptance remain open. An architecture or eligibility change requires a new registry version
and an append-only delta; it must not rewrite version 1 denominators.
