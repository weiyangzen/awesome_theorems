# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:10181-10186` is the complete repository research record. It gives
the title `刚性方程`, attributes it to "many mathematicians", dates it only to the twentieth
century, and gives the gloss `刚性问题的数值解法` ("numerical solution of stiff problems"). It
contains no citation, formula, definition, theorem locator, quantifier, hypothesis, conclusion,
proof, or formal artifact. All six lines entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; that is repository provenance, not a mathematical
source revision.

`Docs/Stage0_Blueprint.md:38019-38044` repeats this metadata while explicitly leaving the exact
definitions and premises, proof route, dependencies, equivalent formulations, axioms, machine
status, and artifact links open. The rev-5.6 manifest retains `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Historical source-family lead

C. F. Curtiss and J. O. Hirschfelder, "Integration of Stiff Equations," *Proceedings of the
National Academy of Sciences* 38(3) (1952), 235-243, DOI `10.1073/pnas.38.3.235`, is a credible
historical source-family lead. Crossref metadata was inspected at intake and confirms the title,
authors, journal, volume, issue, date, pages, and DOI. The catalog does not cite this paper or select
a proposition from it. It is therefore bibliographic discovery only, not an immutable admitted
edition, an exact theorem/page crosswalk, `H0`, or proof evidence.

## Component crosswalk

| Repository phrase | Possible mathematical component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "stiff problem" | widely separated modes, eigenvalue/Jacobian scale, or method-dependent step restriction | ODE/vector field plus a source-defined stiffness predicate | no definition or criterion supplied |
| "equation" | scalar/system, linear/nonlinear, autonomous/nonautonomous IVP or BVP | functions between source-selected normed spaces and an ODE solution predicate | domain and solution model open |
| "numerical solution" | one-step, implicit Runge-Kutta, multistep/BDF, extrapolation, or another algorithm | exact recurrence, stages, grid, implicit-solve relation, and initialization | no method selected |
| accuracy reading | consistency, order, local/global error, or convergence | discrete approximation and a quantified norm bound | constants, norm, limit, and conclusion open |
| stability reading | absolute, A-, L-, B-, algebraic, or stiff stability | amplification/stability region or nonlinear stability predicate | separate inequivalent claims; some have neighboring IDs |
| implementation reading | exact arithmetic, floating point, tolerances, or nonlinear solves | computation and certificate policy | completely open |
| `已验证` | untrusted inventory classification | accepted source and kernel receipts would be required | no human or machine credit |

## Neighbor boundary

The immediately adjacent `THM-M-1399` record explicitly names backward differentiation formulas
and glosses them as a numerical method for stiff equations. Numerical-analysis targets
`THM-M-1476`, `THM-M-1477`, and `THM-M-1478` separately name stiff stability, A-stability, and
L-stability. Those records confirm that none of these more specific propositions may be imported
silently as the meaning of `THM-M-1398`.

## Source and Lean exit gate

Before leaving `H5`, an accountable owner must correct the topic label to one exact proposition,
admit and hash a complete source edition, identify the exact theorem/definition/page and proof
boundary, transcribe every binder, hypothesis, conclusion, constant, convention, and degenerate
case, check corrections and errata, and obtain independent source review. Only then may the
statement phase elaborate a minimal-import Lean expression, preserve its expression/environment
fingerprints, add checked transports, and run the required removed-hypothesis, changed-domain,
binder-scope, and boundary mutations.

A bounded pinned search found generic ODE existence, uniqueness, trajectory-distance, and
Gronwall APIs but no exact-topic `stiff`, A-stability, multistep, Runge-Kutta, or BDF declaration.
`IntakeProbe.lean` checks representative adjacent APIs. This is intake discovery only, not the
downstream immutable anchor audit, a complete absence claim, or source-statement/proof evidence.
