# Scope map

## Frozen subject

- A real scalar field `u(t,x)` on one space dimension and time.
- The conventional normalized PDE `u_t + 6 u u_x + u_xxx = 0` on the real line.
- Explicit derivative meaning, regularity, time interval, spatial boundary/decay conditions, and
  solution concept must be fixed by the later exact source statement.

This is an equation-level scope freeze, not yet a theorem. The coefficient `6` is normalization
dependent and must be cross-checked against the chosen source; rescaled forms require a checked
transport rather than silent identification.

## Open theorem-level decisions

The repository source row does not say whether the root is well-posedness, existence of a
travelling wave, conservation laws, Lax isospectrality, or an inverse-scattering result. It also
does not fix classical versus weak solutions, Sobolev/Schwartz data, local versus global time,
periodic versus real-line space, or uniqueness/continuous dependence. The statement phase must
recover these from an authoritative source or remain blocked; it must not infer them from the
legacy Lean artifact.

## Explicit exclusions

- Treating the equation definition alone as a proved mathematical theorem.
- Substituting the explicit one-soliton calculation for a general evolution theorem.
- Assuming existence, conservation, or uniqueness as fields of a solution package.
- Replacing the real-line problem with a periodic or finite-domain problem without source support.
- Crediting adjacent Fourier, distribution, derivative, or `MemLp` APIs as terminal KdV closure.

The intended formal root will need concrete quantifiers and hypotheses. Until those exist, the
eligibility denominator contains no accepted proof obligations and no proof metric is meaningful.
