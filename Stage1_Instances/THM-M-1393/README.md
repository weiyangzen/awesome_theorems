# THM-M-1393 rev-5.6 intake

`THM-M-1393` is the ordinary-differential-equations catalog item "Fredholm alternative." The
repository attributes it to Erik Fredholm, dates it to 1903, and supplies only the gloss
"solvability of linear boundary-value problems" plus an untrusted `verified` label.

## Intake result

This dossier records a fail-closed `planned` instance. The title and gloss identify the classical
Fredholm-alternative family, but they do not select one proposition. Standard forms include a
spectral alternative for a compact endomorphism, injectivity versus surjectivity for the identity
minus a compact operator, an adjoint-kernel compatibility criterion for an inhomogeneous equation,
and a differential boundary-value formulation with source-specific operator domains and adjoint
boundary conditions. Those forms are related only after substantial hypotheses and transports.

The 1903 paper *Sur une classe d'equations fonctionnelles* is a strong historical source lead, but
only its bibliographic record was inspected. No complete immutable edition, exact theorem passage,
definition and assumption map, proof boundary, correction audit, or independent source review has
been admitted. The canonical mathematical claim and Lean expression therefore remain null rather
than being chosen from memory.

## Formal boundary

Pinned mathlib contains `IsCompactOperator.hasEigenvalue_or_mem_resolventSet`, documented as the
Fredholm alternative for compact operators. `IntakeProbe.lean` confirms that declaration and
adjacent ODE/operator APIs elaborate at the pinned revision. This is a candidate interface only:
the repository's ODE boundary-value gloss does not authorize replacing the target with the abstract
spectral theorem, and no compact-integral reduction or adjoint-boundary bridge has been frozen.

The provisional root vector is `[H1, M4, R4]`. A classical proof family and credible source lead
are known, but exact source fidelity is open; no exact formal target or proof body is credited; and
no source-faithful readable reconstruction can attach to an unfrozen root. All six downstream tasks
remain open. No accepted execution state, audit completion, theorem completion, or master acceptance
is claimed.
