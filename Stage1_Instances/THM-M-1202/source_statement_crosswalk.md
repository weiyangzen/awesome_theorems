# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Repository seed | `Docs/researches/math_theorems.md`, entry "Lax entropy condition": Peter Lax, 1957, "entropy condition for shocks" | none | Metadata discovery only; the phrase is not an exact proposition and its `verified` label supplies no proof credit |
| Hyperbolic conservation-law setting and shock admissibility | P. D. Lax, *Hyperbolic Systems of Conservation Laws II*, Communications on Pure and Applied Mathematics 10 (1957), 537-566, DOI `10.1002/cpa.3160100406` | a finite-dimensional flux, its derivative, ordered real eigenvalues, two traces, and a speed | Primary-source candidate identified; exact page/equation, edition image, and correction review are still required |
| Jump compatibility | Same paper's shock/discontinuity setup; to be pinned to the exact equation in the source audit | vector equation `f u_R - f u_L = s • (u_R - u_L)` | Mathematical component identified, but orientation and Lean vector-space formulation are not frozen |
| Kth-family compressivity | Classical Lax-shock condition associated with the 1957 paper | `lambda k u_R < s ∧ s < lambda k u_L` | Intended core claim; strictness and left/right convention must be checked against the primary text |
| Other characteristic families | Classical adjacent-speed or incoming-characteristic formulation | inequalities for `k-1` and `k+1`, or a finite cardinality statement | Convention-sensitive candidate only; no equivalence or endpoint handling has been checked |
| First/last family | Boundary specialization of the indexed condition | omit the nonexistent lower/upper adjacent inequality | Required domain boundary, not yet formalized |

## Statement boundary

The name "Lax entropy condition" is used in the literature both for an admissibility definition and
inside results relating shock curves, viscosity limits, or entropy inequalities. This target does
not yet claim any such equivalence, necessity/sufficiency theorem, existence theorem, or uniqueness
theorem. It also does not substitute the scalar Oleinik condition or the later Kruzkov entropy
solution theory. The statement phase must select one exact proposition supported by a pinpoint
primary transcription; inability to do so is a statement-gate blocker, not permission to broaden
the target.

## Source work still required

- Obtain and hash a stable copy of the 1957 paper; record the exact page, displayed formula, symbol
  conventions, assumptions, and any publisher corrections or author errata.
- Determine whether the source orders characteristic speeds increasingly or decreasingly and map
  its left/right shock orientation to the canonical notation.
- Cross-check a modern authoritative edition for interpretation, while retaining the primary paper
  as the historical anchor.
- Obtain independent expert review of every premise-to-source mapping before any `H0` claim.

Discovery links, not immutable evidence receipts:

- DOI: <https://doi.org/10.1002/cpa.3160100406>
- Bibliographic record: Lax, CPAM 10 (1957), pp. 537-566.

No `H0`, Lean elaboration, formal-candidate, or theorem-completion claim is made.
