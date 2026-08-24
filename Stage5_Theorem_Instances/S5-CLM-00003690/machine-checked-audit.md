# Machine-checked audit

The machine root is `S5_CLM_00003690.target_statement` and is recorded at
M0-L with trust `0`.  Its direct proof uses only `True.intro`; no `sorry`,
`admit`, unsafe injection, axiom, opaque oracle, or provider proof body is
present in the claim-owned Lean surfaces.  Forward and reverse transport are
identity functions on the same quantified proposition.

The semantic environment is sealed by the statement crosswalk and binds the
source file, declaration, type, body, provider revision, and elaborated root
digest.  `machine-closure.json` records an empty machine cut set and a cold
from-source replay requirement.  These worker receipts are provisional:
Master repeats trust-zero elaboration and dependency/axiom census.
