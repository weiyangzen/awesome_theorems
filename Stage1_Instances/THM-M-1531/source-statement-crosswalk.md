# Source-statement crosswalk

## Primary-source candidates

- Peter W. Higgs, "Broken Symmetries and the Masses of Gauge Bosons," *Physical Review Letters*
  13 (1964), 508-509, DOI `10.1103/PhysRevLett.13.508`. This is the closest historical source for
  the gauge-boson mass claim; exact equations and assumptions still require inspection.
- Francois Englert and Robert Brout, "Broken Symmetry and the Mass of Gauge Vector Mesons,"
  *Physical Review Letters* 13 (1964), 321-323, DOI `10.1103/PhysRevLett.13.321`. This is an
  independent primary formulation candidate; it has not yet been cross-checked equation by equation.
- Gerald S. Guralnik, C. R. Hagen, and Tom W. B. Kibble, "Global Conservation Laws and Massless
  Particles," *Physical Review Letters* 13 (1964), 585-587, DOI
  `10.1103/PhysRevLett.13.585`. It is relevant to the gauge/Goldstone boundary, not automatically
  an interchangeable statement.

These bibliographic records are discovery anchors, not `H0`. The next phase must inspect a stable
copy, record exact equations/pages, assumptions and errata, and select one canonical theorem.

## Crosswalk

| Repository phrase | Source-side content to locate | Required Lean object | Intake status |
|---|---|---|---|
| gauge symmetry | local gauge group and representation | group/action or gauge-group interface | included; model open |
| spontaneous breaking | vacuum with proper stabilizer | vacuum orbit and stabilizer theorem | included; degeneracies open |
| gauge-invariant dynamics | covariant kinetic term plus potential | energy/action and invariance hypotheses | included; analytic regime open |
| generated mass | quadratic expansion about the vacuum | mass form/operator derived from representation and vacuum | included; exact conclusion open |
| unbroken sector | directions fixing the vacuum remain residual symmetry | kernel/stabilizer correspondence | intended; source wording open |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_198.lean` provides useful vocabulary for group
actions, stabilizers, potentials, continuous linear operators, and spectra. It is not a
source-faithful closure: `HiggsMechanismData` contains `vacuumBreaksSomeGaugeSymmetry` and
`hasNonzeroMassMode`, while `HiggsMechanismConclusion` asks for those same facts. Its
`StatementShape` is therefore an interface projection, not the Higgs mechanism theorem.

Before `H0`, an independent reviewer must verify the chosen source's edition, equations/pages,
model assumptions, boundary cases, terminology, and errata and approve a row-level source-to-Lean
mapping. Before machine credit, the exact target must elaborate without assuming its conclusion.
