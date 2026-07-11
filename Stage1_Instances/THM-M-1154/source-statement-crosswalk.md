# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` lines 8450-8455 is the provenance currently available in the
repository. It names "regular boundary points", attributes the topic only to "many
mathematicians" in the twentieth century, and glosses the statement as existence for the
Dirichlet problem. It gives no bibliography, theorem number, assumptions, or proof. Its
"verified" label is untrusted metadata and is not evidence for H0 or machine closure.

## Primary-source candidates requiring inspection

- Norbert Wiener, *The Dirichlet Problem*, Journal of Mathematics and Physics 3 (1924). This is a
  historical source candidate for the capacity criterion and regular boundary behavior. Exact
  article pagination, statement wording, hypotheses, and errata have not been inspected here.
- Joseph L. Doob, *Classical Potential Theory and Its Probabilistic Counterpart*, Springer (1984),
  chapters on the Dirichlet problem and regular boundary points. This is a modern reference
  candidate, not yet an exact theorem/page anchor.

These entries are discovery leads, not an H0 citation. The statement phase must inspect a stable
edition and record theorem/page/assumptions/errata.

## Crosswalk

| Repository phrase | Candidate mathematical meaning | Required formal component | Intake disposition |
|---|---|---|---|
| regular boundary point | boundary value is attained by the Perron solution, often equivalent to a barrier | domain frontier, regularity predicate, checked equivalence if barrier-based | included; definition open |
| Dirichlet problem | find harmonic `u` with prescribed continuous boundary values | harmonicity, boundary-data type, convergence/extension | included; solution notion open |
| existence | global solution when all points are regular, or local boundary convergence | quantifier scope separating local and global claims | ambiguous; source must decide |
| boundary data | commonly continuous real-valued data on `∂Ω` | concrete function space and topology | included; conventions open |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_144.lean` chooses a planar, barrier-based discovery
surface and explicitly says it lacks the terminal Perron/barrier proof and full Dirichlet existence
theorem. Its abstract packages and historical searches cannot establish the exact source statement
or proof. They may be audited only after the source theorem is frozen.
