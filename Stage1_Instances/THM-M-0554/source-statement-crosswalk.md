# Source-statement crosswalk

The theorem name denotes a family rather than one convention-independent
sentence. This intake selects a standard finite-CW cohomological form and
records source candidates without awarding `H0` credit.

| Claim component | Primary-source candidate | Crosswalk status |
|---|---|---|
| Skeletal filtration produces the spectral sequence | M. F. Atiyah and F. Hirzebruch, *Vector bundles and homogeneous spaces*, Proc. Sympos. Pure Math. III (1961), 7-38 | Historical source identified; exact theorem/page and hypotheses require direct edition audit |
| Generalized-cohomology formulation | G. W. Whitehead, *Generalized Homology Theories*, Trans. AMS 102 (1962), 227-283 | Primary foundational candidate; exact AHSS statement mapping not yet pinpointed |
| `E2 = H^p(X; E^q(pt))` | Same historical construction, subject to indexing and reduced/unreduced conventions | Formula selected; notation genealogy and page pinpoint open |
| Differential `d_r : E_r^{p,q} -> E_r^{p+r,q-r+1}` | Standard cohomological convention | Must be reconciled against the audited source convention |
| Convergence and filtration | Finite skeletal filtration of a finite CW complex | Exact strength, edge cases, and extension language require source audit |
| Naturality | Maps compatible with the filtered construction | Precise category of maps and CW approximation assumptions remain open |

The repository's generated phrase "the spectral sequence of a generalized
cohomology theory" is too broad to serve as an exact source statement. A later
source audit must inspect the cited editions, record theorem/page identifiers,
assumptions and known errata, and obtain independent review. Until then the
source status is `H3`; the manifest label `已验证` is untrusted metadata.

The legacy Lean module supplies only generic spectral-sequence APIs and a local
interface skeleton. It has no checked crosswalk to any row above and receives
no proof credit at intake.
