# Scope map

## Included claim

- The real KdV initial-value problem on the line, with a normalization to be frozen from source.
- Initial data in a sufficiently regular, rapidly decaying class.
- Direct scattering for the associated one-dimensional Schrodinger operator.
- Evolution of reflection, bound-state, and norming data under the KdV flow.
- Inverse reconstruction (typically through the Gel'fand-Levitan-Marchenko equation) producing a
  potential that solves KdV and attains the prescribed initial data.

## Statement-phase decisions

The selected primary theorem must fix the sign and constants in KdV and the Lax operator, the
function spaces and decay moments, real-valuedness, the time domain and solution regularity,
spectral assumptions (including zero-energy resonance and bound-state multiplicity), scattering
normalizations, uniqueness, and whether the conclusion is classical or weaker. Degenerate data,
reflectionless data, and absence of bound states must be handled rather than silently excluded.

## Explicit exclusions

- A single soliton formula or the reflectionless finite-soliton case as a substitute for IST.
- Merely proving a Lax commutator identity, conservation law, or evolution of already-given data.
- Assuming existence of the reconstructed KdV solution or inverse transform as structure fields.
- Numerical inverse scattering, experimental claims, or the phrase "KdV equation solution" alone.
- Other integrable equations or periodic/finite-gap inverse spectral theory without a checked
  transport to the frozen line problem.

The later formal statement must expose the analytic model and reconstruction interfaces or record
a precise mathlib/API blocker; an abstract implication that assumes the desired result earns no
statement or proof credit.
