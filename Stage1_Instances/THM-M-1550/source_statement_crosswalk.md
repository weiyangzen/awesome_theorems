# Source-statement crosswalk

| Claim component | Source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Lax equation `dL/dt = PL - LP` | P. D. Lax, *Integrals of Nonlinear Equations of Evolution and Solitary Waves*, Communications on Pure and Applied Mathematics 21 (1968), 467-490, opening operator formulation | `LaxEquationOn`, `matrixCommutator` in `S1_M_209.lean` | Primary source identified; edition hash, exact page/equation transcription, and independent review remain open |
| Spectral values of `L` are time-independent under the Lax evolution | Lax (1968), opening isospectral argument: differentiating `L phi = lambda phi` under `L_t = [P,L]` yields `lambda_t = 0` | `IsospectralOn`; candidate bridge through `IsospectralByConjugationOn` | Matches the conservative root in mathematical intent; exact finite-matrix hypotheses and checked Lean expression remain open |
| Conjugation realizes isospectral evolution | Standard finite-dimensional solution form for a Lax flow, used here as an explicit sufficient input | `ConjugatesAt`, `isospectralOn_of_conjugates` | Historical local theorem is discovery only; later phases must audit its exact type, body, imports, and axioms |
| Characteristic polynomial and traces of powers are conserved | Finite-matrix consequences of similarity/conjugation | `CharacteristicPolynomialInvariantOn`, `TracePowersInvariantOn` | Candidate refinements, not substitutes for the root and not credited at intake |
| "Representation of integrable systems" | Repository research row `Docs/researches/math_theorems.md`, entry `Lax对` | no exact candidate | Metadata summary is not a precise universal theorem; it cannot justify claiming every integrable system has a Lax pair |

Primary-source discovery link: <https://doi.org/10.1002/cpa.3160210503>. This is a bibliographic
anchor, not an immutable evidence receipt. The source audit must still obtain a stable edition,
record page/equation pinpoints and file hashes, check corrections/errata, and map every formal
hypothesis to the source or explicitly label it as a conservative strengthening.

The proposed finite-matrix root deliberately narrows the object model while preserving the standard
Lax isospectrality implication. It does not formalize the informal classification word
"integrable", nor infer existence of `L` and `P` for arbitrary systems. The statement phase must
decide whether conjugating evolution is an explicit hypothesis or is derived from precise ODE
conditions, then elaborate and mutation-test that exact choice before machine evidence is observed.
