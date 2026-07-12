# Immutable Lean anchor audit

This audit compares the frozen target expression
`7a9628fca04eb72d787efad1f852517f4385377b3ad16f3eba662ccea4bb86a5` with formal candidates. The
local closure uses Lean `4.29.0` and mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, exactly as pinned by `lake-manifest.json`. Existing
artifacts were inspected without updating, building, cloning, or fetching dependencies.

## Result

No exact mathlib or immutable external Lean 4 proof candidate was located. The exact target remains
`M3`: its statement and checked transports exist locally, but there is no proof body. In particular,
this audit supplies neither `M0-W` nor `M1` credit.

The closest pinned mathlib fixed-point declarations are Banach's contracting-map result
`ContractingWith.exists_fixedPoint'` and the interval result
`exists_mem_Icc_isFixedPt_of_mapsTo`. Their elaborated types respectively require contraction on a
complete emetric subset and a single continuous self-map of a real interval. Neither has the target's
arbitrary locally convex ambient space, affine family, pairwise commutation, or common conclusion.
The `RealRMK.integral_rieszMeasure` search hit is a name collision: it is the
Riesz-Markov-Kakutani representation theorem.

The full pinned mathlib and all locally present dependency sources were searched for name and
semantic phrases. A global Sourcegraph search, explicitly including forks and archives, found only
Riesz representation occurrences for the Markov-Kakutani spellings. Those results identify mathlib4
at indexed commit `12b4b4adf73c3bf0917409bb4b9dd4c8b96f4e8f` and Atlas Lean at
`34ffed396f376454c1a9b297f3fd74c5c801fb50`; Atlas only imports the Riesz modules. GitHub repository
searches for four Lean-specific spellings each returned zero repositories. Exact queries, scopes,
revisions, candidate dispositions, and limitations are recorded in `anchor-audit.json`.

Negative discovery is necessarily bounded: it does not establish that private or unindexed code
does not exist. It does establish that no discovered candidate is eligible to wrap or integrate.
Primary human-source theorem/page/errata fidelity, the obligation tree, proof, trust closure, audit
completion, theorem completion, and master acceptance all remain open.

## Validation

Base revision: `730e085f3ee8dfae10bd3b61f2dc8f90e7056880`.

| Command | Result |
|---|---|
| `python3 Stage1_Instances/THM-M-0321/check_anchor_audit.py` | exit 0; pin, target fingerprint, candidate revisions, dispositions, searches, and Lean near-candidate types checked |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0321/AnchorAuditProbe.lean)` | exit 0; all three pinned near-candidate declarations and their actual types elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0321/anchor-audit.json` | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-0321` | exit 0; no whitespace errors |

