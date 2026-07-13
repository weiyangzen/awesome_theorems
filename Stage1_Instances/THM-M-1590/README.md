# THM-M-1590 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `循环码`
(`cyclic codes`). The catalog supplies only the gloss `循环移位不变的码` ("codes invariant under
cyclic shift"), a collective attribution, the period "20th century," and an untrusted `已验证`
label. That wording describes a class of codes; it is not a truth-valued theorem with fixed
binders, hypotheses, and a conclusion.

Even as a definition, the gloss leaves material choices open. It does not fix an alphabet, ring,
or field; the word length and coordinate type; left versus right shift; arbitrary-set versus
additive or linear code; closure versus equality under the shift; or the intended result about the
class. Standard algebraic characterizations by ideals of a polynomial quotient, generator
polynomials, duality results, and concrete BCH or Reed-Solomon constructions are different possible
theorems and are not silently adopted.

The provisional root vector is `[H5, M4, R4]`. Here `H5` means that the received catalog wording is
not one stable proposition requiring an ordinary proof lane; it does not say that established
cyclic-code mathematics is false or open. The canonical mathematical statement and Lean target
remain null. A modern textbook chapter was located as a source-family lead, but the repository does
not cite it and its definitions and results were not available for a proposition-level crosswalk.

`IntakeProbe.lean` authenticates only adjacent pinned coordinate-rotation, function-space linear
transport, Hamming-distance, and circulant-matrix APIs. It declares no target and supplies no proof
credit. `scope-map.md` freezes the proposition-changing decisions, `source-statement-crosswalk.md`
records the source boundary, and `task-dag.json` leaves every downstream phase open. No accepted
execution state, audit completion, theorem completion, or master acceptance is claimed.
