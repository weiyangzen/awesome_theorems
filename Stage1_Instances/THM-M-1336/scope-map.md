# Scope map

## Received scope

The mathematical catalog fixes only the title `比较定理` ("comparison theorem"), the broad
attribution "many mathematicians," the twentieth-century date, and the gloss
`微分不等式与解的比较` ("comparison of differential inequalities and solutions"). It gives no
primary source, theorem locator, definitions, hypotheses, or proposition-level conclusion. Its
`已验证` label is preserved in the rev-5.6 manifest only as untrusted source metadata.

The ODE category narrows the topic but does not identify one theorem. The execution rank, intake
score, and lane are mechanically generated scheduling metadata and add no mathematical premises.

## Candidate mathematical boundary

An eventual exact target may be a comparison theorem only if an accepted source fixes all of the
following:

- the state space: real-valued functions, a finite-dimensional ordered space, or a general ordered
  Banach space, including every order and topology instance;
- the time domain and direction: a closed, open, half-open, local, maximal, or global interval,
  together with endpoint and reversed/empty interval conventions;
- whether the compared objects are arbitrary differentiable functions, exact ODE solutions,
  subsolutions and supersolutions, approximate trajectories, or integral inequalities;
- the vector field, autonomous or nonautonomous dependence, regularity, local/global existence,
  uniqueness, Lipschitz, monotonicity, or quasimonotonicity assumptions;
- the derivative notion: ordinary, within-set, right Dini derivative, liminf slope, almost
  everywhere derivative, or integral form;
- initial or boundary order, strict versus non-strict differential inequalities, and whether the
  derivative condition is global or required only at a first-contact boundary;
- the exact conclusion: preservation of pointwise order, strict separation, a quantitative bound,
  non-crossing, uniqueness, or comparison with a distinguished solution.

These bullets are a scope inventory, not a canonical statement. No candidate family is credited at
intake.

## Ambiguities to resolve

1. Whether "differential inequalities" refers to comparing two functions directly or comparing a
   subsolution with a solution of `y' = F(t, y)`.
2. Whether the theorem is scalar, componentwise vector-valued, or stated in an ordered normed
   space, and which monotonicity condition makes solution comparison valid.
3. Whether the source assumes uniqueness or one-sided Lipschitz regularity; continuity of the
   vector field alone generally does not select an ordered solution.
4. Whether equality at a first contact requires a strict derivative inequality, or a weak global
   derivative inequality is sufficient.
5. Whether comparison is forward only, backward only, or two-sided from an interior initial time.
6. Whether initial equality, initial weak order, or strict initial order is required, and how
   equality and equilibrium solutions are handled.
7. Whether the intended conclusion is qualitative order preservation or a quantitative estimate.
8. Whether a Gronwall-type formulation belongs instead to the separately cataloged
   `THM-M-1337`, and whether nonlinear integral comparison belongs to `THM-M-1338`.

## Explicit exclusions

- Replacing this item by Gronwall's inequality (`THM-M-1337`) or Bihari-LaSalle's inequality
  (`THM-M-1338`) merely because both involve differential inequalities.
- Treating ODE uniqueness, continuous dependence, stability, or existence as the root conclusion;
  those have separate catalog entries or require a source-selected implication.
- Selecting mathlib's scalar fencing theorem, approximate-trajectory distance estimate, or exact
  trajectory distance estimate solely because its name and API are convenient.
- Assuming an ordered-system monotonicity or Lipschitz premise not present in an accepted source,
  or dropping one because a scalar special case is easier to formalize.
- Proving a vacuous empty/reversed-interval case, a constant-function example, or one explicit ODE
  and presenting it as the general target.
- Packaging the desired order conclusion as a structure field and projecting that field as a
  purported proof.
- Treating `已验证`, a topic-level citation, an API probe, or a passing unrelated Lean file as
  statement or proof evidence.

## Formal boundary

No canonical Lean expression is frozen at intake. At the pinned revision, mathlib provides a
direct scalar fencing family in `Mathlib.Analysis.Calculus.MeanValue` and quantitative
trajectory-comparison results in `Mathlib.Analysis.ODE.Gronwall`. Their inequivalent binders and
conclusions demonstrate feasibility and ambiguity; neither is source-identical to the catalog
gloss. Exact imports, expression and environment fingerprints, checked transports, and mutations
belong to the dependent statement phase after an immutable source proposition is selected and
independently reviewed.
