# Source-statement crosswalk

| Claim component | Source anchor | Formal candidate | Intake assessment |
|---|---|---|---|
| Received repository claim | `Docs/researches/math_theorems.md`, entry `东帕定理`: Patrick Dehornoy, 1989, "large cardinals and the axiom of determinacy" | None | The wording names neither hypotheses nor a conclusion; the manifest's adjacent "verified" label is explicitly untrusted |
| Bibliographic identity | Patrick Dehornoy, *La determination projective*, Seminaire Bourbaki 1988/89, expose 710, Asterisque 177-178 (1989), pp. 261-276, MR 1040576, Zbl 0693.03033 | None | Strong match for author, year, and subject; the record calls it projective determinacy, not "Dongpa theorem" |
| Primary theorem family | Donald A. Martin and John R. Steel, projective-determinacy results from Woodin-cardinal hypotheses, published around 1988-1989 | Candidate model-theoretic implication | Discovery family only. Exact article, theorem number, pages, hypotheses, and errata are not yet accepted |
| Finite-level form | A finite collection of Woodin cardinals together with the appropriate measurable-above hypothesis yields determinacy at a corresponding projective level | Future level-indexed proposition | Candidate only; index shifts and hypothesis variants make paraphrase unsafe as a canonical statement |
| Full projective determinacy | Suitable infinitely-many-Woodin-cardinal hypotheses imply determinacy for all projective payoff sets | Future bundled proposition or corollary | Candidate only; it must not be conflated with determinacy for all sets of reals |
| Games and pointclasses | Length-omega perfect-information games and projective subsets of Baire space/reals | Lean encodings of plays, strategies, winning, and the projective hierarchy | Object coding and internal/external model semantics remain unresolved |
| Large-cardinal premise | Woodin cardinals and, in relevant versions, a measurable cardinal above them | Lean set-theory/model predicates | Exact cardinal count and ordering are root-defining, not implementation details |

## Identity and exactness risks

The Chinese label `东帕定理` does not transliterate "Dehornoy" and repository-wide search supplies no
definition of the eponym. Author, year, and topic instead align with Dehornoy's Bourbaki expose. The
intake therefore treats the label as potentially corrupt metadata and the expose as a discovery
source, not as permission to rename a Martin-Steel theorem.

Several nearby claims are not interchangeable. Borel determinacy is provable without the stated
large-cardinal strength. Full projective determinacy is weaker in scope than the axiom of
determinacy for arbitrary sets of reals. Finite-level Martin-Steel theorems have sensitive index and
large-cardinal hypotheses. A consistency-strength statement is metatheoretic and cannot replace an
object-level implication. The statement phase must select and transcribe one exact source theorem
before constructing a Lean proposition.

## Source status

The Numdam landing page provides stable bibliographic metadata and a public scan for Dehornoy's
expose at `https://www.numdam.org/item/SB_1988-1989__31__261_0/`. This intake used the landing-page
metadata only. It did not archive the scan in the repository or accept it as primary theorem proof
evidence. No primary Martin-Steel theorem text, edition hash, page-level premise/conclusion map,
errata review, or independent reviewer receipt is present. Consequently the source gate remains
`H5`, and no exact human or Lean theorem is claimed.
