# Frozen obligation tree

Registry version 1 freezes 22 semantic obligations before proof execution. The selected route constructs the Poisson expression, proves its PDE and initial-data properties, and uses uniqueness in the exact solution class. All analytic leaves remain open unless explicitly marked below.

| Obligation | Kind | Exact output | H/M/R | Budget |
|---|---|---|---|---:|
<a id="m1129-root"></a>
| `M1129-ROOT` | root | The canonical proposition. | H2/M3/R3 | 12 |
<a id="m1129-s-defs"></a>
| `M1129-S-DEFS` | definition | The exact definitions used below. | H2/M0-L/R3 | 15 |
<a id="m1129-s-domain"></a>
| `M1129-S-DOMAIN` | definition | The exact root context. | H2/M0-L/R3 | 18 |
<a id="m1129-s-boundary"></a>
| `M1129-S-BOUNDARY` | branch | A complete boundary policy with no singular substitution at zero. | H2/M4/R3 | 55 |
<a id="m1129-s-transport"></a>
| `M1129-S-TRANSPORT` | transport | A directional checked transport into the canonical unit-disk statement. | H2/M4/R3 | 85 |
<a id="m1129-s-foundation"></a>
| `M1129-S-FOUNDATION` | certificate | An accepted foundation and TCB profile. | H2/M4/R3 | 40 |
<a id="m1129-c-kernel"></a>
| `M1129-C-KERNEL` | construction | Well-defined displacement and velocity integral terms. | H2/M4/R3 | 80 |
<a id="m1129-l-weight"></a>
| `M1129-L-WEIGHT` | core_lemma | The singular kernel is integrable and boundary values are harmless a.e. | H2/M4/R3 | 95 |
<a id="m1129-l-data"></a>
| `M1129-L-DATA` | core_lemma | Domination hypotheses required by the parametric integral API. | H2/M4/R3 | 85 |
<a id="m1129-l-diff"></a>
| `M1129-L-DIFF` | bridge | A checked expression for the outer time derivative. | H2/M4/R3 | 90 |
<a id="m1129-l-spatial"></a>
| `M1129-L-SPATIAL` | core_lemma | The spatial side of the wave equation. | H2/M4/R3 | 90 |
<a id="m1129-l-time"></a>
| `M1129-L-TIME` | core_lemma | The time side of the wave equation. | H2/M4/R3 | 95 |
<a id="m1129-l-pde"></a>
| `M1129-L-PDE` | bridge | The constructed expression solves the PDE at positive time. | H2/M4/R3 | 45 |
<a id="m1129-l-initial-f"></a>
| `M1129-L-INITIAL-F` | terminal | Initial displacement equals f. | H2/M4/R3 | 90 |
<a id="m1129-l-initial-g"></a>
| `M1129-L-INITIAL-G` | terminal | Initial velocity equals g. | H2/M4/R3 | 90 |
<a id="m1129-l-uniqueness"></a>
| `M1129-L-UNIQUENESS` | core_lemma | Any two solutions with the same data agree for positive time. | H2/M4/R3 | 95 |
<a id="m1129-t-construct"></a>
| `M1129-T-CONSTRUCT` | terminal | A represented classical solution with data f and g. | H2/M4/R3 | 60 |
<a id="m1129-t-represent"></a>
| `M1129-T-REPRESENT` | terminal | The complete analytic package, definitionally the canonical target. | H2/M4/R3 | 35 |
<a id="m1129-t-assemble"></a>
| `M1129-T-ASSEMBLE` | transport | The exact canonical proposition, conditionally on the open package. | H2/M0-L/R3 | 3 |
<a id="m1129-x-source"></a>
| `M1129-X-SOURCE` | terminal | An H0-eligible source crosswalk. | H2/not_applicable/R3 | 60 |
<a id="m1129-x-provenance"></a>
| `M1129-X-PROVENANCE` | certificate | A complete terminal-body provenance map. | H2/informational/R3 | 40 |
<a id="m1129-x-trust"></a>
| `M1129-X-TRUST` | certificate | Release-gate trust evidence. | H2/informational/R3 | 45 |

## Proof architecture

`ROOT -> T-ASSEMBLE -> T-REPRESENT -> {T-CONSTRUCT, L-UNIQUENESS}`. Construction expands into kernel well-definedness, differentiation, the wave identity, and both zero-time data obligations. The kernel and differentiation nodes share, without double credit, the singular-weight and data-domination leaves. `L-PDE` expands into separate spatial-Laplacian and second-time-derivative calculations.

`S-BOUNDARY` has logical-decomposition edges to both initial-data leaves. Source, provenance, evidence, trust, documentation, and workflow edges are separate from proof edges and cannot close the root.

## Composition boundary

`poissonFormulaTarget_of_analyticPackage` is kernel checked and consumes an explicit `PoissonAnalyticPackage`, definitionally the exact root. It proves only the child-to-parent interface. It does not prove the analytic package. The first remaining root cut is `M1129-T-REPRESENT`; root debt remains M3 and theorem completion is false.

No node is excluded merely because it is difficult. The source-only and release overlays are root-relevant but are not proof premises. Every planned leaf has a provisional budget at most 100; these budgets freeze granularity and are not R0 evidence.
