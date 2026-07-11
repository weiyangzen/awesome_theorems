# THM-M-0392 Frozen Obligation Tree

## Root composition

`M0392-ROOT` is the fingerprinted statement for every nonzero integer parameter. The checked
`ObligationTree.root_compose` certificate deliberately abstracts the future integral-point type and
curve-eligibility predicate. It requires four explicit inputs: eligibility of each nonzero Mordell
curve, finiteness of its abstract integral points, a map from equation solutions to those points,
and injectivity of that map. The local `finite_of_injective` lemma then transfers finiteness to the
exact solution subtype. These hypotheses are not declarations of mathematical facts and give no
root proof credit.

## Mathematical architecture

The proof graph freezes the following substantive route rather than treating “apply Siegel” as a
single opaque line:

1. `M0392-C-CURVE` constructs the short affine Weierstrass model for `y^2=x^3+k` and checks the
   equation correspondence.
2. `M0392-L-NONSINGULAR` specializes the short-form discriminant calculation and uses `k != 0` to
   establish the eligibility required by an integral-points theorem.
3. `M0392-X-SIEGEL` supplies finite integral points for the eligible curve. The anchor audit found
   no Lean 4 terminal theorem for this obligation, so it is the principal open machine cut set.
4. `M0392-T-COORDINATES` constructs and proves injective the representation of integer solution
   pairs as curve integral points.
5. `M0392-L-FINITE-TRANSFER` composes the injective representation with a finite encoding.

Every semantic ledger has at most three steps. That bound records decomposition only; it does not
claim readable reconstruction or proof closure. There are eight required root-relevant obligations
and zero exclusions. The inline statement, composition-harness root, and Northcott infrastructure
are aliases or nonterminal surfaces and receive no duplicate denominator credit.

## Open boundaries

`M0392-X-SOURCE` retains the missing primary-source theorem/page/assumption/errata crosswalk. The
anchor audit's H3 classification is not upgraded. `M0392-X-TRUST` owns the future terminal body's
transitive axioms, imports, provenance, computation boundaries, and independent replay. Until an
exact Lean 4 integral-points theorem is integrated or directly proved, these checks cannot close.

This phase freezes an architecture and checks conditional composition only. The exact root remains
M2; H0, M0, R0, audit completion, theorem completion, release, and master acceptance remain open.
