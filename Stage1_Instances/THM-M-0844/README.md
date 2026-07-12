# THM-M-0844 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0844`, the repository label
`Alon-Fischer-Newman定理` (Alon-Fischer-Newman theorem). The catalog supplies the authors, the
year 2007, and only the gloss `正则性引理的测试`, literally "testing of the regularity lemma."
It supplies no citation, definitions, quantified proposition, hypotheses, conclusion, or proof
source. Its `已验证` field is untrusted metadata under rev-5.6.

## Intake result

The metadata points toward graph property testing and regularity but does not identify one theorem.
A strong bibliographic match is Alon, Fischer, and Newman's 2007 paper *Efficient Testing of
Bipartite Graphs for Forbidden Induced Subgraphs*. Later literature attributes to that paper a
polynomial-size, ultra-strong regularity lemma for bipartite graphs of bounded VC-dimension. No
complete copy was present in the repository or successfully retrieved from the inspected lawful
metadata and author-copy leads, however, and the catalog does not name its title, theorem number,
definitions, or exact result.

Two nearby results cannot be silently substituted. *A Combinatorial Characterization of the
Testable Graph Properties: It's All About Regularity* has an additional author and different
2006/2009 dates. The Fischer-Newman testing-versus-estimation theorem omits Alon and has a different
conclusion. The catalog gloss could be a mistranslation or conflation of any of these themes.

The canonical human and Lean statements therefore remain null. `instance.json` freezes the
provisional root vector `[H5, M4, R4]`: `H5` classifies the catalog wording as not yet a stable
truth-valued proposition, not the identified papers as false. `IntakeProbe.lean` elaborates only
adjacent pinned graph, VC-dimension, and regularity APIs. It provides no source-statement or proof
credit. All six downstream tasks remain open in `task-dag.json`.

No canonical statement, H0, M0, R0, accepted proof state, audit completion, theorem completion, or
master acceptance is claimed.
