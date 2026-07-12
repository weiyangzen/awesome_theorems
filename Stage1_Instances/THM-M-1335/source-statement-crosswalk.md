# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:9740-9745` supplies exactly the title `解的延拓定理`, the
attribution `众多数学家` (many mathematicians), the twentieth century, the gloss
`解的最大存在区间`, importance "high," and status `已验证`. Git provenance places all six uncited
lines in repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no
equation, source, definition, binder, hypothesis, conclusion, proof, correction, or formal artifact.

`Docs/Stage0_Blueprint.md:36318-36343` repeats those fields while explicitly leaving the formal
system, logical foundation, background, exact definitions and premises, proof route, dependencies,
equivalent statements, axioms, machine status, and artifact links open. Its generic planning text
about a known closed result is not source evidence. The rev-5.6 manifest retains `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Literal crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `解` (solution) | solution of an initial-value ODE | vector field, curve, derivative, initial condition, domain-membership predicate | equation and solution notion absent |
| `延拓` (continuation/extension) | enlarge the solution's time domain while preserving old values | partial-domain representation, restriction/agreement, strict domain inclusion | extension relation absent |
| `最大` (maximal) | maximal element under extension, or nonextendibility at endpoints | order on solution-domain pairs and maximality/uniqueness predicate | order and uniqueness absent |
| `存在区间` (interval of existence) | connected open time interval containing the initial time | interval/set object, initial-time membership, endpoint encoding | topology and endpoint convention absent |
| many mathematicians / twentieth century | broad historical provenance | immutable edition, theorem/page, definitions, errata, proof genealogy | no pinpoint source |
| `已验证` | untrusted inventory status | accepted source review and kernel receipt would be required | no H or M credit |

The phrase does not say whether the desired conclusion is maximal-solution existence, an endpoint
extension equivalence, a compact criterion, blow-up, or global existence. These cannot share one
Lean target without an approved source selection.

## Inspected authoritative discovery source

Gerald Teschl, *Ordinary Differential Equations and Dynamical Systems*, Graduate Studies in
Mathematics 140, American Mathematical Society, 2012, DOI `10.1090/gsm/140`, was inspected using
the author-hosted preliminary edition made available with AMS permission. Section 2.6, printed
pages 50-54, distinguishes the likely source family:

- Theorem 2.13, page 51, constructs a unique maximal solution on an open interval
  `(T_-(t0,x0), T_+(t0,x0))` when the IVP has a unique local solution;
- Lemma 2.14, pages 51-52, characterizes extension beyond a finite endpoint by convergence of a
  sequence of graph points to an interior point of the open domain;
- Corollaries 2.15-2.16, pages 52-53, give compact continuation and the contrapositive compact-escape
  conclusion, with divergence to infinity in `U = Real x Real^n`; and
- Theorem 2.17, page 53, adds a linear-growth hypothesis to conclude global existence.

The same edition's IVP setup on printed page 36 uses a continuous vector field on an open subset of
`Real x Real^n`; its Picard-Lindelof theorem adds local Lipschitz continuity in the state variable
to obtain unique local solutions. The source's published errata must be audited before acceptance,
including the scope of unique local solvability in Theorem 2.13.

This inspection proves that multiple standard statements fit the catalog gloss. It does not prove
that the catalog intended Teschl's presentation, establish a primary historical genealogy, close an
errata review, or supply independent H0 review. The PDF hash and bibliographic-response hash are
recorded in `instance.json` and the provisional receipt.

## Candidate source-to-Lean components

| Source-family component | Prospective Lean surface | Intake assessment |
|---|---|---|
| open `U` in spacetime and initial point in `U` | a set of `Real x E`, openness, and membership | state space and domain open |
| continuous vector field, locally Lipschitz in state | continuity and `LipschitzOnWith`/local predicates | exact regularity open |
| local IVP solution | `IsIntegralCurveOn` or an exact derivative-within predicate plus initial value | adjacent APIs checked only |
| unique local solvability | quantified local existence plus agreement on overlap | mathlib has ingredients, exact premise not frozen |
| union/gluing of compatible solution intervals | union of intervals and a well-defined glued partial curve | no target-specific construction audited |
| maximal interval and solution | maximality under extension of domain-solution pairs | no pinned target declaration located |
| endpoint convergence and extension | filters/sequences, graph convergence, and local restart/gluing | not selected and no target declaration located |
| compact escape or norm blow-up | compact subsets of spacetime/state and endpoint filters | stronger variant; hypotheses open |

## Source gate

Before the target can leave `H5`, an accountable reviewer must approve one immutable proposition,
pin its exact edition and theorem/page, incorporate every referenced definition and local-existence
premise, transcribe ordered binders and hypotheses, audit errata and historical/source genealogy,
map every conclusion and boundary case, and explain why neighboring continuation variants are not
part of the root. A second qualified reviewer must approve the mapping. The selected target's H
status must then be classified afresh; it cannot inherit `已验证`.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks integral curves, local Picard-Lindelof existence, and open-interval uniqueness. A bounded
name search over repo-local and pinned mathlib Lean sources found no maximal-solution, maximal-
existence-interval, ODE continuation, compact-escape, or blow-up-alternative declaration. Nearby
local existence and uniqueness theorems do not identify or close the missing root.

The canonical module, declaration/expression, elaborated-expression hash, checked transports, and
statement mutations remain null. The probe and search are intake evidence only, not a complete
formal-candidate audit and not H0, M0, or readable-proof closure.
