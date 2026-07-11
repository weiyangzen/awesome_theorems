# Source-statement crosswalk

| Claim component | Primary-source discovery anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Nahm equations and monopole construction program | W. Nahm, *A Simple Formalism for the BPS Monopole*, Phys. Lett. B 90 (1980), 413-414, DOI `10.1016/0370-2693(80)90961-2` | `NahmData`, `NahmTransformHypotheses` in the legacy module | Primary historical anchor located, but edition/page text, precise hypotheses, and errata have not been audited |
| Transform via a Dirac-family kernel | N. J. Hitchin, *On the Construction of Monopoles*, Communications in Mathematical Physics 89 (1983), 145-190, DOI `10.1007/BF01211826` | `DiracKernel`, `NahmTransformPackage` | Likely construction anchor; theorem/page and convention-to-field mapping remain open |
| Boundary/pole residues and charge | Hitchin (1983), sections and theorem pinpoints not yet accepted | fields of `NahmTransformHypotheses` | Charge, interval, residue representation, endpoint, and framing choices must be extracted rather than inferred |
| Bogomolny output | Hitchin (1983), exact result pinpoint pending | `IsBogomolny` and `NahmTransformConclusion` | Candidate conclusion boundary only; the legacy predicate is abstract and supplies no proof credit |
| Regularity and finite energy | Hitchin (1983), analytic assumptions/results pinpoint pending | regularity and `finiteEnergy` fields | Source premise/result distinction and analytic spaces are unresolved |

The repository metadata says only `单极子的构造` (construction of monopoles) and labels the entry
verified. That label is untrusted under rev-5.6 and cannot determine whether the intended root is an
existence construction, one direction of the Nahm correspondence, or a bijection modulo gauge.
This intake deliberately selects only the conservative construction direction as a candidate and
keeps exact-source acceptance open.

Required statement-phase/source-audit work: obtain immutable source copies and hashes; identify
edition, theorem/proposition and page ranges; record all charge, smoothness, irreducibility,
boundary, gauge and framing assumptions; check corrections/errata; distinguish bounded abstractions
from the actual unbounded Dirac operator; and obtain independent review. No `H0`, exact Lean target,
checked transport, or machine closure is claimed.
