# THM-M-0396 frozen obligation architecture

Item: `S56-M-0396-OBLIGATION_TREE`

The registry freezes 15 semantic obligations for the exact proposition
`Stage1Rev56.THMM0396.Statement`. Eligibility was assigned from the mathematical
architecture, not from proof availability. The anchor audit found no terminal
Lean 4 Baker-Matveev theorem, so this is an executable proof plan rather than a
completed proof.

## Typed route

`M0396-ROOT` requires `M0396-T`, the exact parameterwise terminal estimate.
That terminal requires logarithm/product normalization (`M0396-N1`), parameter
normalization (`M0396-N2`), construction and nonvanishing of the auxiliary
determinant (`M0396-C1`, `M0396-C2`), its arithmetic lower bound
(`M0396-L1`, `M0396-L2`), its analytic upper bound (`M0396-L3`), and the
explicit constant optimization (`M0396-L4`). Reciprocal `proof_requires` and
`composes` edges record this route.

Refinement, provenance, evidence, trust, documentation, and workflow use
separate typed graph families. In particular, the source boundary `M0396-X1`
and trust boundary `M0396-X2` cannot silently become mathematical premises.

## M0396-root

The exact canonical statement remains `M3`: it elaborates, but has no terminal
proof body. The sole root proof cut is `M0396-T`.

## M0396-s1

Freeze the product, linear-form value, explicit bound, height, domains,
coercions, and ordered hypotheses from `Statement.lean`.

## M0396-s2

`core_iff_statement` checks that the parameterwise `CoreEstimate` neither
drops nor adds a root binder. `root_compose` is a conditional composition
certificate: it consumes `CoreEstimate` as an explicit premise and therefore
does not prove the analytic estimate.

## M0396-s3

`linearFormValue_eq_zero_of_coeff_zero` checks the all-zero-coefficient
boundary. The root's nonvanishing premise excludes that case.

## M0396-n1

Relate the product of positive real embeddings to the exponential of the
corresponding additive logarithmic form. This branch and all later analytic
branches are planned at `M4`.

## M0396-n2

Normalize the degree, coefficient, height, and positivity data without
strengthening the frozen assumptions or weakening the final strict bound.

## M0396-c1

Construct the auxiliary interpolation determinant and its finite index sets.
This is marked `split-required`: a future proof must refine its construction,
dimension, integrality, and multiplicity subclaims before leaf acceptance.

## M0396-c2

Prove determinant nonvanishing through an explicit zero estimate and rank
argument. This central construction cannot be hidden behind a library slogan.

## M0396-l1

Control the logarithmic height of the determinant and all conjugate entries in
terms of the normalized `D`, `B`, and `A_i` parameters.

## M0396-l2

Turn determinant nonvanishing, degree, and height into an arithmetic lower
bound. The precise algebraic lower-bound bridge must be identified and audited.

## M0396-l3

Under the negation of the target estimate, derive an analytic interpolation
upper bound for the same determinant. The internal analytic cases remain to be
split during proof execution.

## M0396-l4

Choose and round the auxiliary integers, discharge every numerical side
condition, and derive exactly the frozen factor
`1.4 * 30^(n+3) * n^(9/2)`. A different or asymptotic constant would not close
this obligation.

## M0396-t

Compose the normalized logarithmic form, determinant construction, lower and
upper estimates, and numerical optimization into `CoreEstimate`. This is the
open root cut and has no proof body.

## M0396-x1

Pinpoint the primary theorem/page, conventions, assumptions, and errata for
every mathematical node. It is human-source required but machine
`not_applicable`, with an explicit exclusion reason rather than denominator
silence.

## M0396-x2

Audit the future terminal body's declaration graph, provenance, axioms,
computation boundary, TCB, and reproducible validation. This is a release gate,
not an additional proof of the theorem.

## Freeze boundary

The content-addressed denominator and all full node records are in
`obligation-registry.json` and `typed-graphs.json`. A later split, merge,
exclusion, or target correction requires a new append-only registry version.
The current root is open, `audit_complete=false`, and
`theorem_complete=false`.
