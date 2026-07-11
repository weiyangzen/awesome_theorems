# Source-statement crosswalk

## Source identification boundary

The repository supplies only the phrases "global compactness", "compactification of noncompact
problems", and "critical-growth compactness". These do not uniquely select a published theorem.
The neighboring PDE context and legacy analysis point toward a Struwe/Lions-style bubble or profile
decomposition, but intake evidence does not justify selecting an author, edition, theorem number,
or page. The statement phase must identify and inspect a primary source, including referenced
definitions, hypotheses, and errata. No bibliographic or H0 claim is made here.

## Crosswalk

| Repository phrase | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| "global compactness" | one specific critical-PDE compactness theorem | one exact theorem expression | family frozen; source theorem open |
| "noncompact problem" | loss of compactness through source-specified symmetries | explicit domain, action, sequence, and failure mode | included; model open |
| critical growth | critical exponent and variational/energy regime | scalar field, dimension, exponent, spaces, functional | included; values open |
| weak limit | background solution after extraction | subsequence and weak convergence in a concrete space | included; topology open |
| bubbles/profiles | rescaled/translated nontrivial limiting solutions | profile family, parameters, separation, profile equations | included; indexing open |
| global compactness conclusion | complete decomposition and remainder control | convergence plus exact norm/energy splitting | included; formula open |

## Legacy Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_174.lean` is a discovery artifact. Its selected
variant agrees with the family above, but `ProfileCompactnessMechanism` and
`GlobalCompactnessProblem` abstract over or package the substantive PDE facts. Its locally proved
compactness statements concern the packaged compact target or an explicitly nonterminal one-point
branch. They are not a formalization of the root claim and grant no M-credit.

Before H0, an independent reviewer must approve the exact edition/theorem/page/assumption/errata
crosswalk. Before M-credit, the canonical Lean statement must elaborate and later work must inspect
real declarations and terminal proof bodies at immutable revisions.
