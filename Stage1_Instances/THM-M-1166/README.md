# THM-M-1166 rev-5.6 intake

This `planned` instance covers the catalogue item **Elliptic equations** (`椭圆型方程`). The only
provided wording is “the theory of second-order elliptic equations.” A mathematical theory is not
a single proposition: it may refer to existence, uniqueness, regularity, maximum principles,
estimates, or representation results under materially different assumptions. The intake therefore
fails closed rather than substituting a convenient elliptic PDE theorem.

## Scope map

| Surface | Catalogue scope | Intake boundary |
|---|---|---|
| Identity | Second-order elliptic equations | Preserved as a source-disambiguation target, not converted into a new theorem |
| Operator | Linear/quasilinear; divergence/non-divergence; scalar/system alternatives | No alternative is selected without a primary statement |
| Analytic setting | Domain, dimension, coefficient class, ellipticity, solution and boundary notions | Every parameter remains open |
| Possible conclusions | Solvability, uniqueness, regularity, estimates, or qualitative principles | No disjunction or conjunction is treated as the root claim |
| Neighbor boundary | PDE catalogue family | Schauder estimates belong to `THM-M-1167`; Green-function spectral expansion belongs to `THM-M-1165` |
| Lean surface | Exact proposition over pinned analysis/PDE APIs | No module or declaration can truthfully be selected yet |

The structured record is `intake.json`, the evidence-to-statement gap is documented in
`source_statement_crosswalk.md`, and `task_dag.json` orders the required follow-up.

## Intake verdict

Lifecycle remains `planned`, with provisional root vector `[H5, M4, R4]`. The first failed gate is
exact source-statement identification. The later statement phase is blocked until a primary source
selects a single theorem and fixes its assumptions. No Lean elaboration, proof, or theorem
completion is claimed.
