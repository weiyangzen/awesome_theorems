# Source-statement crosswalk

| Claim component | Primary source anchor | Intended formal component | Intake assessment |
|---|---|---|---|
| Every semistable elliptic curve over `Q` is modular | A. Wiles, *Modular elliptic curves and Fermat's Last Theorem*, Annals of Mathematics 141 (1995), 443-551, Theorem 0.4 | `forall E, Semistable E -> Modular E` over elliptic curves over `Q` | Root identified, but exact page transcription, edition hash, assumptions, and errata review are not yet accepted: `H1` |
| Meaning of modularity | Wiles (1995), introductory discussion relating elliptic curves and modular forms | association with a weight-two eigenform, with compatible L-series/Galois representation | Exact level and equivalence used by the formal target remain open |
| Ring-theoretic ingredient completing the argument | R. Taylor and A. Wiles, *Ring-theoretic properties of certain Hecke algebras*, Annals of Mathematics 141 (1995), 553-572 | deformation-ring/Hecke-algebra and patching obligations | Companion proof source located; it is not a replacement root statement |
| Modularity-lifting implications | Wiles (1995), especially the deformation-theoretic main conjecture and applications; Taylor-Wiles (1995) | typed bridge from a residual modular representation plus local hypotheses to a modular lift | Several variants and hypotheses occur; none is frozen or credited here |

The repository's Chinese legacy name, "Wiles-Taylor theorem", and content gloss, "modularity
lifting", do not uniquely identify one lifting theorem with ordered hypotheses. The published
semistable modularity theorem is therefore frozen as the root because it is a precise named outcome
of the joint Wiles/Taylor-Wiles argument. This choice preserves rather than broadens the historical
claim. The statement phase must reject it if a more specific authoritative repository source is
found; it must not invent a lifting schema.

Discovery identifiers, not immutable evidence receipts:

- Wiles: DOI `10.2307/2118559`.
- Taylor-Wiles: DOI `10.2307/2118560`.

No `H0` or machine-closure claim is made. Required follow-up includes obtaining immutable source
files and hashes, confirming theorem/page wording, mapping every hypothesis to proof nodes,
checking corrections and errata, independently reviewing the crosswalk, and locating or defining
the exact Lean 4 predicates without weakening either semistability or modularity.
