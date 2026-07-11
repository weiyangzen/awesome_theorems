# Source-statement crosswalk

The repository gloss points to Sergiu Klainerman's null-condition/global-existence result, not every
theorem bearing his name. These bibliography entries are discovery inputs; no immutable source
packet or independent source review is accepted.

| Claim component | Human source anchor | Lean target | Intake assessment |
|---|---|---|---|
| Null condition and global existence | S. Klainerman, “The null condition and global existence to nonlinear wave equations,” *Nonlinear Systems of Partial Differential Equations in Applied Mathematics, Part 1*, Lectures in Applied Mathematics 23 (1986), 293-326 | none | Title and subject match the gloss; theorem number/page, equation class, and premises require a fixed edition: `H1` |
| 3+1-dimensional small-data wave setting | Same primary candidate; pinpoint open | future expression | Scope is provisional, not exact-statement credit |
| Quadratic null condition | Primary paper's definition and theorem, to be transcribed | future coefficient/symbol predicate | No ad hoc definition receives equivalence credit before crosswalk and mutation tests |
| Small smooth data | Primary theorem's norm, differentiability, localization/decay, and compatibility conditions | future data structure | All parameters remain explicit open fields |
| Global classical solution | Primary theorem's time domain, regularity, and uniqueness assertion | future solution predicate | Stronger asymptotics are excluded absent an anchor |
| Proof route | S. Klainerman, “Uniform decay estimates and the Lorentz invariance of the classical wave equation,” *CPAM* 38 (1985), 321-332 | future vector-field/energy nodes | Methodological companion only, not a substitute root |

## Statement-phase tasks

1. Acquire and hash a fixed edition of the 1986 chapter; record title metadata, exact theorem and
   definition pages, and corrections or errata.
2. Transcribe equation, coefficient regularity, vanishing order, null-condition formula, dimension,
   data spaces, support/decay, smallness norm, and conclusion without changing logical strength.
3. Decide whether the selected theorem is semilinear, quasilinear, or covers both; later refinements
   must be separate source nodes rather than silently merged.
4. Crosswalk every source binder and premise to Lean. Missing PDE infrastructure is formalization
   debt, not permission to weaken the theorem.
5. Obtain independent review before any `H0` claim.

No Lean 4 closure is claimed or audited here. The later anchor audit must distinguish definitions
and partial analytic lemmas from an exact root proof.
