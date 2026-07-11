# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Characteristic-zero LLC for `GL_n` | M. Harris and R. Taylor, *The Geometry and Cohomology of Some Simple Shimura Varieties*, Annals of Mathematics Studies 151, Princeton University Press (2001), especially the statement of the local Langlands conjecture in the introduction and the proof developed through the book | No declaration identified | Primary proof source identified; exact theorem/page, hypotheses, normalization, edition hash, and errata mapping remain open: `H1` |
| Uniqueness and numerical local correspondence | G. Henniart, "Une preuve simple des conjectures de Langlands pour GL(n) sur un corps p-adique", *Inventiones Mathematicae* 139 (2000), 439-455, DOI `10.1007/s002220050012` | No declaration identified | Primary complementary proof source identified; premise-by-premise crosswalk and correction search remain open |
| Representation-side domain | Irreducible admissible smooth representations of `GL_n(F)` in the cited formulations | Future quotient of a Lean category/object model | Smooth representation, admissibility, irreducibility, isomorphism classes, and topology APIs have not been audited |
| Parameter-side domain | Frobenius-semisimple `n`-dimensional Weil-Deligne representations | Future Weil/Weil-Deligne parameter object | Weil group, continuity, monodromy relation, Frobenius semisimplification, and equivalence require precise definitions |
| Rank-one normalization | Compatibility with local class field theory | Future `n = 1` normalization node | Reciprocity-map convention and geometric versus arithmetic Frobenius normalization are unresolved |
| Characterizing compatibilities | Twists, contragredients, central characters, and local `L`- and epsilon-factors | Future compatibility fields/nodes | Additive character, Haar measure, reciprocity, and epsilon-factor conventions must be frozen before elaboration |

The repository's source phrase, "local Langlands correspondence for local fields", does not by
itself choose a group, coefficient field, characteristic, or normalization. This dossier therefore
uses the standard proved `GL_n` correspondence over finite extensions of `Q_p`, matching the
manifest's characteristic-zero arithmetic lane while explicitly excluding broader conjectural
programs. Master review must reject or revise this scope if the upstream source intended a different
claim; no silent broadening is allowed.

Discovery links, not immutable evidence receipts:

- Harris-Taylor bibliographic record: <https://press.princeton.edu/books/hardcover/9780691090924/the-geometry-and-cohomology-of-some-simple-shimura-varieties>
- Henniart DOI: <https://doi.org/10.1007/s002220050012>

No `H0` or machine-checked claim is made. The source audit must still record scanned edition hashes,
exact page/theorem anchors, every assumption and convention, known errata, and an independent
node-specific review. The statement phase must separately build or locate the Lean object model,
elaborate the exact expression, check alternate parameter encodings, and mutation-test field
characteristic, rank, binder scope, semisimplicity, and all normalization laws.

