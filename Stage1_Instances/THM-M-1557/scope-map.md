# Scope map

## Included claim family

- The two-component Zakharov-Shabat auxiliary spectral problem used for nonlinear Schrodinger
  evolution, with the matrix entries and sign conventions copied from one inspected source edition.
- Its paired time evolution and the mixed-derivative or zero-curvature compatibility condition.
- The potential reduction, such as a conjugacy relation, selected by the source to obtain a concrete
  focusing or defocusing nonlinear Schrodinger equation.
- Exactly the spatial and temporal domains, scalar field, spectral-parameter quantification,
  regularity, and boundary or decay assumptions used by the frozen source passage.
- A checked coefficient comparison between compatibility and NLS, in only the implication
  directions justified by the source.

## Decisions reserved for statement freeze

The statement phase must inspect and select an exact equation range in a primary-source edition. It
must freeze the normalization of NLS; focusing or defocusing sign; meanings of the two potentials;
matrix/operator ordering; commutator and derivative signs; real or complex spectral parameter;
whether the parameter is fixed or universally quantified; the wavefunction and potential types;
regularity; domains; boundary or decay assumptions; and whether compatibility implies NLS, is
implied by NLS, or is genuinely equivalent to it.

The catalogue phrase `NLS\u65b9\u7a0b\u7684Lax\u5bf9` ("a Lax pair for the NLS equation") identifies this family but
does not by itself determine those choices or a single proposition.

## Explicit exclusions

- Defining `ZakharovShabatSystem` or `IsLaxPair` to contain the desired NLS equality and proving the
  result by projection or unfolding.
- Replacing the concrete system by a generic commutator rearrangement or an arbitrary abstract Lax
  pair.
- Substituting the broader AKNS framework, the generic zero-curvature target `THM-M-1551`, or a
  different integrable PDE.
- Claiming inverse-scattering reconstruction, existence or uniqueness of NLS solutions, conserved
  quantities, solitons, or completeness of scattering data unless they are separate frozen source
  obligations.
- Silently choosing focusing instead of defocusing NLS, or changing normalization by scaling or
  gauge transformation without a checked transport.

Repo-local abstract Lax-pair modules are discovery inputs only. None is credited as the canonical
statement or as proof of this source-specific target at intake.
