# Scope map

## Preserved source scope

- Named family: Schauder estimates.
- Claimed effect: a Holder-continuity estimate.
- Attribution and date: Juliusz Schauder, 1934, as repository metadata only.
- Broad subject: differential equations / partial differential equations.

This is all the repository source fixes. In particular, "Schauder estimate" names a family rather
than a unique proposition.

## Decisions required before statement freeze

The statement phase must identify a primary source and freeze: elliptic or parabolic operator;
linear, quasilinear, or nonlinear regime; dimension and scalar field; interior, boundary, local, or
global setting; domain and boundary regularity; solution concept; coefficient ellipticity and
Holder hypotheses; forcing and boundary data; the exponent range; the precise `C^{k,alpha}` norms
and seminorm convention; normalization/scaling; the estimated derivatives; and every dependency of
the constant. It must also address zero data, empty or degenerate domains, endpoint exponents, and
any compatibility conditions admitted by the selected theorem.

## Explicit exclusions

- Choosing the classical interior Poisson estimate, a boundary estimate, or a parabolic estimate
  merely because it has a convenient formal API.
- Replacing the PDE regularity result with a generic Holder-space inequality or embedding theorem.
- Treating the nearby heat-equation Schauder contracts in `S1_M_152.lean` as this theorem: they
  concern `THM-M-1189`, and their abstract packages do not identify this source claim.
- Treating the metadata label `已验证`, the date, or the attribution as source or kernel evidence.
