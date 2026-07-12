# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md` identifies Watts/Strogatz, 1998, and only "small-world
phenomenon". `Docs/Stage0_Blueprint.md` repeats those fields while leaving the exact definitions,
hypotheses, proof route, foundations, and formal artifacts open. The `已验证` value is explicitly
untrusted intake metadata under rev-5.6.

## Primary source candidate

Duncan J. Watts and Steven H. Strogatz, "Collective dynamics of 'small-world' networks",
*Nature* 393 (1998), 440-442, DOI `10.1038/30918`.

The publisher record and abstract, accessed 2026-07-12, identify a regular-ring random rewiring
model, high clustering, small characteristic path length, empirical networks, and dynamical-system
experiments. Publisher Figure 1 describes rewiring without changing the number of vertices or
edges; Figure 2 reports `L(p)` and `C(p)` for the randomly rewired family. This intake did not obtain
or independently review an immutable full-text edition, pinpoint a theorem statement, or establish
that the plotted characteristic regime is presented with an analytic proof. The citation is thus
discovery evidence, not `H0`.

## Crosswalk

| Repository/source phrase | Component that must be frozen | Required Lean component | Intake status |
|---|---|---|---|
| "small-world phenomenon" | one truth-valued quantitative claim | an exact `Prop` rather than a label or structure projection | not identified |
| regular ring lattice | vertex set, degree, and initial edges | finite `SimpleGraph` construction | family identified; parameters open |
| random rewiring | probability space and edge-update rule | distribution or measurable random graph | source procedure requires inspection |
| `L(p)` | characteristic path-length convention | finite pair aggregate of graph distance, including disconnected policy | observable not frozen |
| `C(p)` | local/global clustering convention | triangle/neighbor adjacency statistic and normalization | observable not frozen |
| highly clustered yet short paths | inequalities, comparison baselines, and parameter regime | exact bounds with quantifier and probability semantics | qualitative only |
| empirical examples and dynamics | observation or simulation boundary | no kernel-proof credit | explicitly excluded from root evidence |
| `已验证` | accepted source review or kernel receipt | no direct Lean counterpart | no credit |

## Required follow-up

Before statement credit, an authorized reviewer must select a proposition that is actually supported
by a pinpoint primary source, preserve every model convention and assumption, and state whether the
claim is finite, asymptotic, deterministic, in expectation, or with high probability. Before `H0`,
an independent reviewer must inspect a content-addressed edition, map each premise and conclusion,
check corrections or errata, and approve the crosswalk.

The later anchor-audit phase must separately search pinned mathlib and immutable Lean 4 projects,
record exact declaration types and proof-body provenance, and distinguish useful graph definitions
from an exact small-world theorem. This intake accepts no formal candidate.

Discovery link (not an immutable evidence receipt): <https://doi.org/10.1038/30918>.
