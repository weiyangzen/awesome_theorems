# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Global reciprocity program | R. P. Langlands, *Problems in the Theory of Automorphic Forms*, Lecture Notes in Mathematics 170, Springer (1970), pp. 18-61 | No declaration identified | Foundational primary program source; exact passage, edition hash, and premise mapping remain open: `H1` |
| Algebraic automorphic to Galois direction | L. Clozel, "Motifs et formes automorphes: applications du principe de fonctorialite", in *Automorphic Forms, Shimura Varieties, and L-functions*, Vol. I (1990), pp. 77-159 | No declaration identified | Source for algebraicity/motivic formulation; conventions and theorem-versus-conjecture boundaries require audit |
| Galois domain | Continuous semisimple `l`-adic representations of `Gal(Kbar/K)` with geometric restrictions | Existing repo file only defines a raw monoid homomorphism from `Field.absoluteGaloisGroup`; it is not the target | Continuity, topology, coefficient field, ramification, geometricity, and equivalence remain undefined |
| Automorphic domain | Algebraic cuspidal automorphic representations of `GL_n(A_K)` | No bundled general automorphic-representation API identified at intake | Adeles exist locally in mathlib, but the representation category and algebraicity predicates are absent |
| Unramified matching | Frobenius characteristic polynomial equals the Hecke/Satake polynomial outside exceptional places | Existing `FrobeniusCompatibleAt` is abstract infrastructure only | Arithmetic versus geometric Frobenius and polynomial normalization remain open |
| Directionality | Automorphic-to-Galois, Galois-to-automorphic, or a correspondence/compatible-system formulation | No exact expression | The broad repository label does not determine a single proved theorem; source review must not silently choose one |
| Rank one | Global Artin reciprocity / class field theory | No audited terminal declaration | Boundary model only; it cannot substitute for general `n` |

The manifest says only "Langlands reciprocity" and describes a correspondence between Galois and
automorphic representations. That is insufficient to claim a universally proved theorem. The
statement phase must choose a source-backed, binder-complete formulation, or explicitly retain a
conjectural `Prop`; it must not promote a special modularity theorem or the `n = 1` case into the
general root.

No `H0` or machine claim is made. A later source audit must pin scans/revisions, locate exact
statements, list every hypothesis and normalization, search errata, and obtain independent review.

