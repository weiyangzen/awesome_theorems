# THM-M-0468 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Bogomolov conjecture for
subvarieties of abelian varieties. The manifest's Chinese gloss, "small-height
points in abelian varieties", is not precise enough by itself to select a formal
statement; the claim frozen below follows the standard Ullmo-Zhang formulation.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Ambient data | a number field `K`, an abelian variety `A/K`, an ample symmetric line bundle, and its canonical height | Lean encodings and universe parameters belong to the statement phase |
| Subvariety | a closed geometrically integral subvariety `X` of `A` | Base change and geometric-point conventions must be made explicit later |
| Small points | for every positive real `epsilon`, points of `X` with canonical height at most `epsilon` are Zariski dense | The choice of `<=` versus `<` is expected to be equivalent but is not credited without a checked transport |
| Special locus | `X` is a translate of an abelian subvariety by a torsion point | Field of definition and geometric torsion conventions remain to be normalized |
| Exact root | dense small points if and only if `X` is special | No Lean expression or proof closure is claimed at intake |
| Foundations | Lean 4 kernel with a pinned mathlib and an accepted classical/choice/quotient profile | Exact toolchain, dependency, axiom, and TCB fingerprints remain open |

This scope excludes the distinct Bogomolov conjectures about fundamental groups,
Galois representations, and lower bounds stated only for non-special varieties.
Those may be consequences or alternate formulations, not substitutes for this root.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The primary
proof sources have been identified, but editions, errata, and premise-to-node
mapping have not been independently accepted. No usable Lean declaration has
been located or tested in this intake. The first failed theorem gate is the exact
Lean statement gate. The theorem is not complete.

## Validation

The commands and exact results in `validation.md` establish manifest membership,
repository-standard consistency, JSON syntax, and dossier-local integrity only.

