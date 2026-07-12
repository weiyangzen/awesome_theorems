# Scope map

## Repository claim

The only repository-level mathematical wording is `可积系统的统一框架` ("a unified framework for
integrable systems"), attributed to AKNS and dated 1974. It does not specify a domain, binders,
hypotheses, or conclusion. The source label `已验证` is untrusted metadata under rev-5.6.

## Provisional included claim family

- A concrete AKNS auxiliary linear system with a matrix-valued spatial operator and time operator,
  depending on a spectral parameter.
- Sufficient differentiability for mixed derivatives and matrix products to be defined.
- The compatibility condition for the two linear equations, expressed as a zero-curvature identity.
- Coefficient comparison showing equivalence between that identity and the evolution equations for
  the selected potentials, for one source-fixed AKNS flow or reduction.

This is a scope boundary for later source selection, not a frozen theorem statement.

## Decisions required at statement freeze

The next phase must select a pinpointed source result and freeze: the independent variables and
their real or complex domains; scalar field; matrix dimensions; spectral-parameter domain; precise
forms and sign conventions of both operators; differentiability and decay/boundary assumptions;
whether compatibility is equality of mixed derivatives, vanishing curvature, or an operator
commutator; coefficient comparison hypotheses; the selected hierarchy flow; reductions such as
nonlinear Schrodinger, modified KdV, or sine-Gordon; and all degenerate parameter cases.

The binder order, universes, typeclass assumptions, foundation profile, computation policy, and
minimal imports must be derived from that decision. A formal statement cannot be frozen merely by
defining a structure whose field is the desired compatibility equation.

## Explicit exclusions

- A claim that every integrable system is an AKNS system.
- The full inverse-scattering transform, global existence, reconstruction, or completeness unless
  the selected source theorem explicitly states it.
- One named reduction, such as the nonlinear Schrodinger equation, substituted for the requested
  AKNS framework without a checked relationship to the source claim.
- A generic matrix commutator identity with no map to the AKNS operators and coefficient equations.
- Numerical evidence, symbolic examples, or the repository's `已验证` label as proof evidence.

No canonical Lean target is frozen at intake. The later target must expose the operators,
derivatives, compatibility equation, and coefficient evolution rather than assume the conclusion.
