# THM-M-0554 rev-5.6 intake

This dossier records a `planned` intake for the Atiyah-Hirzebruch spectral
sequence (AHSS). The selected root is the cohomological AHSS for a finite CW
complex and a generalized cohomology theory: its second page is cellular
cohomology with the coefficient groups of the theory and it converges, with
the skeletal filtration, to the generalized cohomology of the space.

`instance.json` is the authoritative local intake record. `scope-map.md` fixes
what the name does and does not include, while `source-statement-crosswalk.md`
keeps the historical-source pinpoint work explicit. This phase introduces no
Lean declaration and claims neither exact elaboration nor proof closure.

## Status

| Field | Value |
|---|---|
| Lifecycle | `planned` |
| Baseline | `L0 / rework_required` |
| Human debt | `H3`, pending primary-source pinpoint and review |
| Machine debt | `M4`, canonical Lean expression not yet elaborated |
| Readability debt | `R3`, intake outline only |
| Theorem complete | no |

The historical file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_106.lean`
is discovery input only. Its general spectral-sequence wrappers and local
cohomology skeleton neither state nor prove the selected AHSS root.

## Statement phase

`Statement.lean` now freezes the exact closed proposition selected by this
intake. It quantifies the abelian target, generalized-cohomology skeleton,
space, and finite-CW skeletal input, then asks for the cohomological AHSS data,
the `E₂` coefficient identification, naturality, and convergence to the
skeletal associated graded. The file defines this proposition but provides no
inhabitant and makes no proof-completion claim.
