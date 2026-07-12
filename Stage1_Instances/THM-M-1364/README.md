# THM-M-1364 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the ordinary-differential-equations
catalog item `Lorenz系统` (Lorenz system). The repository supplies Edward Lorenz, 1963, and the
gloss `混沌的经典例子` (a classic example of chaos). It gives no equation, parameter values,
definition of chaos, theorem statement, hypotheses, conclusion, or source locator. The catalog's
`已验证` (verified) field is explicitly untrusted metadata.

## Intake result

The title names a system family and the gloss makes an informal classificatory claim, but neither
is one truth-valued mathematical proposition. Possible targets include merely defining Lorenz's
three-dimensional polynomial vector field, proving elementary equilibrium or dissipativity facts,
proving sensitive dependence or another specified chaos predicate, establishing a geometric Lorenz
attractor, or proving a source-specific strange-attractor theorem for classical parameter values.
These choices are not interchangeable.

The attribution and date strongly match Edward N. Lorenz's 1963 paper *Deterministic Nonperiodic
Flow*. Crossref confirms the publication metadata, but the catalog does not cite a page, equation,
numerical experiment, or proposition from that paper. The famous equations and conventional
parameters do not by themselves determine which mathematical assertion is to be proved. Likewise,
a later rigorous theorem such as a computer-assisted existence result cannot silently replace the
catalog gloss.

## Formal boundary

`IntakeProbe.lean` checks only pinned generic ODE, flow, fixed-point, invariant-set, derivative, and
omega-limit interfaces adjacent to possible future encodings. A bounded lexical search found no
Lorenz-system or Lorenz-attractor declaration in repo-local Lean or pinned mathlib. Neither fact is
an exhaustive downstream anchor audit, and neither supplies a target theorem or proof body.

The provisional root vector is `[H5, M4, R4]`. `H5` says that the catalog wording is not yet a
stable proposition; it does not say that rigorous results about Lorenz systems are false or open.
All six downstream tasks remain open. No canonical Lean expression, H0, M0, R0, accepted proof
state, audit completion, theorem completion, or master acceptance is claimed.
