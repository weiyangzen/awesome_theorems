# Source-statement crosswalk

## Source family

The historical primary anchor is Shigefumi Mori, “Threefolds whose canonical bundles are not numerically effective,” *Annals of Mathematics* 116 (1982), 133-176, DOI `10.2307/2007050`. The modern relative log-pair package is normally presented in later minimal-model-program treatments, notably Janos Kollar and Shigefumi Mori, *Birational Geometry of Algebraic Varieties* (Cambridge Tracts in Mathematics 134, 1998), in the cone and contraction theorem chapter.

This intake has not performed edition/page-level inspection of the latter statement or an errata search. It therefore records `H2`, not `H0` or `H1`; exact theorem numbers, page spans, hypotheses, characteristic restrictions, and the relation between Mori's original threefold result and the selected modern formulation remain open.

## Crosswalk

| Canonical component | Source-side role | Disposition |
|---|---|---|
| projective pair over `S` | relative geometric setting | included; exact hypotheses open |
| Q-factorial normal `X` and klt `(X, Delta)` | singularity/divisor assumptions | included; definitions open |
| `N_1(X/S)_R` and closed effective cone | numerical curve-class space | included; Lean carrier open |
| `(K_X+Delta)`-nonnegative subcone | nonnegative summand | included |
| countable negative extremal rays | negative-ray decomposition | included |
| rational curves generating rays | bounded/rational generators | included; numerical bound open |
| local finiteness away from the boundary | finiteness in a strictly negative region | included; topology/quantifiers open |
| contraction of each negative ray | contraction branch | provisionally included; dependency and hypotheses open |

## Metadata correction and provenance boundary

The Stage0 gloss “finite generation of the cone of an algebraic variety” is too broad and potentially false as a literal replacement: the theorem permits countably many negative rays and asserts local finiteness under negativity conditions. The untrusted `已验证` label establishes neither a human-source crosswalk nor kernel closure. The legacy Lean file and its embedded external-search notes receive no rev-5.6 evidence credit until independently re-audited.

## H-gate work

Inspect stable scans of the cited sources; record exact editions, theorem labels, pages, assumptions, all characteristic and dimension restrictions, referenced prerequisites, and errata. Decide whether the root is the classical characteristic-zero relative log cone theorem or Mori's original threefold statement, then obtain independent review of every crosswalk row.
