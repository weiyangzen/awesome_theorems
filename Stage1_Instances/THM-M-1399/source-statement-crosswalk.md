# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10188-10193` supplies exactly the title `向后微分公式`, attribution
to many mathematicians, the twentieth century, the gloss `刚性方程的数值方法`, importance "high,"
and status `已验证`. Git history attributes all six uncited lines to repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, stable source ID,
edition, theorem or page locator, equation, definition, binder, hypothesis, conclusion, proof
boundary, correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:38046-38071` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof process, dependencies, alternate forms, axioms,
machine status, and artifact links open. Its generated `公式 / 恒等式` classification does not
supply a formula. The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted` and
resets this target to `L0 / rework_required`.

## Historical discovery leads

- C. F. Curtiss and J. O. Hirschfelder, "Integration of Stiff Equations," *Proceedings of the
  National Academy of Sciences* 38(3) (March 1952), 235-243,
  DOI `10.1073/pnas.38.3.235`, PMID 16589085, PMCID PMC1063538.
- C. W. Gear, "The automatic integration of ordinary differential equations,"
  *Communications of the ACM* 14(3) (March 1971), 176-179,
  DOI `10.1145/362566.362571`.

DOI content-negotiation records were retrieved during intake and hashed. Europe PMC independently
confirmed the 1952 bibliographic fields and reports that article as not open access. The publisher
does not permit full-text XML download through PMC, so no equation or theorem passage was
transcribed. The catalog cites neither paper. Both records are therefore discovery evidence only,
not accepted source identity or H0 evidence. No claim is made that either paper contains the exact
root the catalog intended.

## Component crosswalk

| Repository element | Possible mathematical component | Prospective Lean component | Intake assessment |
|---|---|---|---|
| `向后微分公式` | a family of implicit linear multistep formulas | coefficients, history sequence, time grid, vector field, and recurrence predicate | method family, not a unique proposition |
| "backward differentiation" | derivative of an interpolant at a newest node, or normalized coefficient identity | `Lagrange.interpolate`, polynomial derivative and evaluation, after source-controlled typing | construction and convention absent |
| "stiff equation" | an ODE problem class or motivation for implicit stability | `IsIntegralCurve`, normed state space, vector field and a source-defined stiffness predicate | stiffness definition and any performance conclusion absent |
| "numerical method" | definition, computable step, convergence, error, or stability theorem | sequences, implicit relation, existence/uniqueness and analytic estimates | result kind and hypotheses absent |
| many mathematicians / twentieth century | broad historical context | provenance metadata only | no source or pinpoint theorem |
| `已验证` | untrusted inventory field | accepted source proof and kernel receipt would be required | no H or M credit |

## Method-to-theorem boundary

Even a standard-looking recurrence would not resolve the target. Different sources reverse the
history index, rescale coefficients, normalize the newest coefficient or right-hand side, and use
constant or variable time steps. The recurrence itself is a definition or formula; an order,
consistency, convergence, zero-stability, A-stability, or implicit-solvability result is a separate
truth-valued claim with additional hypotheses. No checked equality, implication, or equivalence
between any such candidates is available at intake.

Calling the method useful for stiff equations is also not a theorem until stiffness, usefulness,
the comparison methods, error or stability metric, and quantified problem class are fixed. A
successful computation or stability diagram cannot fill those missing binders.

## Neighbor and substitution boundary

The surrounding catalog separately schedules the finite-difference method (`THM-M-1395`),
Runge-Kutta methods (`THM-M-1396`), Adams methods (`THM-M-1397`), and stiff equations
(`THM-M-1398`). These topics overlap with BDF vocabulary but remain distinct theorem IDs. A
backward difference identity, backward Euler result, generic implicit multistep theorem, or theorem
about stiffness cannot be substituted without an authoritative source decision and checked
transport.

## Source gate

There is no authoritative mathematical source selected by the repository. Before leaving `H5`, an
accountable reviewer must redirect the method label to one exact proposition, preserve an immutable
primary or authoritative source, record edition and equation/theorem/section/page, transcribe all
incorporated definitions, ordered binders, hypotheses, conclusion, proof boundary, coefficient and
index conventions, and exceptional cases, audit errata, reconcile the neighboring targets, and
obtain independent approval of the source-to-statement mapping.

`H5` here does not assert that BDF theory is false. It records that the repository gloss does not
determine a truth-valued target that a Lean kernel could check. No H0 crosswalk can be completed
until a proposition is selected.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only probe
checks `HasDerivAt`, `IsIntegralCurve`, `IsPicardLindelof`, `Lagrange.interpolate`, and
`Lagrange.iterate_derivative_interpolate`. These are possible substrate for future source-selected
encodings, not a BDF statement or proof. A bounded case-insensitive search for exact BDF and
linear-multistep terminology over pinned mathlib and repo-local Lean sources found no match. The
later immutable formal-candidate audit remains open.

The canonical module, declaration or expression, expression and environment fingerprints, checked
alternate encodings, and statement mutations therefore remain null. No statement elaboration,
formal absence theorem, proof, audit completion, or theorem completion is claimed.
