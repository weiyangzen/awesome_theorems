# Source-statement crosswalk

| Claim component | Available source anchor | Lean target surface | Intake assessment |
|---|---|---|---|
| Theorem identity | `Docs/Stage0_Blueprint.md` names Friedrichs inequality and glosses it as an estimate for compactly supported Sobolev functions | none selected | Repository metadata only; it is not a primary mathematical source and is insufficient for statement identity |
| Attribution and date | Stage0 attributes the result to Kurt Friedrichs and gives 1929 | none | Unverified metadata; no publication, edition, theorem number, or page is supplied |
| Norm estimate | The gloss suggests an estimate controlling a function norm from derivative data | planned `L^p`/weak-gradient expression | Direction is plausible but operands, exponent, measure, and constant dependencies are not specified |
| Compact support | Explicit in the Stage0 gloss | planned support predicate or zero-trace Sobolev membership | Included in scope; equivalence to a `W_0^{1,p}` formulation requires a checked transport and domain hypotheses |
| Domain and boundary | Not stated | planned Euclidean open set/domain structure | Hard blocker: boundedness, regularity, dimension, and boundary convention affect truth and formulation |
| Constant | Not stated | existential or explicit nonnegative real constant | Hard blocker: dependencies and whether an optimal/explicit constant is intended are unknown |

## Source boundary

The repository contains no primary citation for this target. The Stage0 row is discovery evidence
only and its `已验证` label supplies neither `H0` nor machine credit. A later source audit must locate
an authoritative edition, pinpoint the exact statement and assumptions, check corrections/errata,
and obtain independent review before `H0` is possible.

Terminology in modern analysis often uses “Friedrichs inequality” for a Poincare-type estimate on
zero-boundary Sobolev functions. That usage informs the provisional family in `scope-map.md`; it is
not asserted here as the unique historical theorem. In particular, this intake does not substitute
a probability Poincare inequality, a general Sobolev embedding, a coercivity axiom packaged as a
hypothesis, or a definition whose conclusion is tautological.

## Required statement-phase crosswalk

The next phase must bind every source quantifier and hypothesis to an exact Lean binder, including
the ambient dimension, domain, scalar field, exponent range, function class, weak-gradient model,
support/trace condition, measure and norm conventions, constant and its dependencies, and all
degenerate cases. Only then may it choose minimal pinned imports, serialize an elaborated expression
and environment fingerprint, check alternate transports, and run the mandated mutations.
