# Source-statement crosswalk

| Claim component | Human source anchor | Planned Lean surface | Intake assessment |
|---|---|---|---|
| Classical weak maximum principle for the heat equation | L. C. Evans, *Partial Differential Equations*, 2nd ed., AMS GSM 19 (2010), section 2.3.3, theorem titled "Maximum principle for the heat equation" | root proposition, not yet encoded | Standard statement anchor located; exact page/edition scan and primary historical genealogy remain unverified, so this is not H0 |
| Bounded spatial domain and finite positive time | same theorem's setup for the space-time cylinder | domain and compact-closure obligations | Necessary for the stated attained-max form; exact topology encoding remains open |
| Initial plus lateral parabolic boundary | same section's cylinder/boundary definitions | `parabolicBoundary U T` (planned name only) | Terminal face must not be silently included as boundary data |
| Subsolution inequality `u_t - Delta u <= 0` | same theorem | derivative and Laplacian predicate | Sign convention is frozen; reversing it yields the minimum-principle variant |
| Maximum over closure equals maximum over parabolic boundary | same theorem | extrema or pointwise-bound formulation | Attained-max and supremum encodings need a checked compactness transport |

The repository's Stage0 wording, "maximum principle for parabolic equations," is broader than this
root. It does not specify weak versus strong, classical versus weak solutions, the operator, domain,
regularity, or boundary. This intake does not pretend those variants are equivalent: it narrows the
dossier to the canonical heat operator and records every excluded family in `intake.json`.

The Evans reference is a real mathematical statement anchor but not a primary historical source and
has not yet received a content hash, page-image verification, errata search, premise-to-node audit,
or independent review. Accordingly the human status is `H2`, not `H0`. The statement and source-audit
phases must verify the bibliographic pinpoint and either locate primary provenance or explicitly
justify the accepted source policy before raising that status.

No existing Lean declaration is credited here. Names in this document described as planned are
design labels, not claims about mathlib APIs.
