# Source-statement crosswalk

## Repository source record

`Docs/researches/math_theorems.md` names "Gaussian process", attributes it to many mathematicians,
dates it only to the twentieth century, and gives the statement "the theory of Gaussian
processes". `Docs/Stage0_Blueprint.md` repeats that phrase and leaves the precise definition and
hypotheses open. Neither text identifies a proposition, edition, theorem, or page. The manifest
label `已验证` is therefore discovery metadata, not human-proof or machine-proof evidence.

## Candidate references

- J. L. Doob, *Stochastic Processes*, Wiley, 1953. This is a historical monograph candidate for
  the finite-dimensional definition; chapter, page, wording, assumptions, and later corrections
  require direct inspection.
- R. J. Adler and J. E. Taylor, *Random Fields and Geometry*, Springer, 2007, the introductory
  Gaussian-random-field definitions. This is a modern source candidate for finite linear
  combinations and finite-dimensional distributions; exact definition/page and errata require
  inspection.
- Pinned mathlib discovery lead:
  `Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Def` and
  `Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic`. The latter documents and
  proves finite-dimensional Gaussian-law consequences and preservation lemmas. This lead has not
  been accepted as an exact target or proof in this intake.

These are candidate anchors, not `H0` evidence. A later source audit must select and independently
review a pinpoint edition/page statement before claiming source fidelity.

## Crosswalk

| Repository phrase | Frozen interpretation | Required Lean component | Intake status |
|---|---|---|---|
| Gaussian process | process with Gaussian finite-dimensional laws | process, measure, state space, Gaussian-process predicate | family included; exact types open |
| finite-dimensional restriction | law of every finite coordinate vector is Gaussian | finite index set/tuple, restriction map, `HasGaussianLaw` | included; encoding open |
| finite linear combination | every finite real combination is Gaussian | coefficients, finite sum, scalar Gaussian law | alternate form; relationship must be checked |
| "the theory" | not a proposition | no faithful single Lean target exists from this phrase alone | rejected as a broadened root |
| verified | untrusted source metadata | kernel receipt plus provenance and trust closure | no proof credit |

## Evidence boundary

The statement phase must inspect the pinned module and the chosen human source, then record the
exact Lean declaration or expression, normalized expression hash, environment fingerprint, and
checked transports. The anchor-audit phase must separately record revisions, declaration types,
terminal bodies, axioms, placeholders, and dependency feasibility. Until then, the exact root
remains `M4`, and neither an existing predicate nor its elementary projection lemmas close a
uniquely sourced theorem.
