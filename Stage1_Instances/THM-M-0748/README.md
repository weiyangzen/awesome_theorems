# THM-M-0748 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Post's problem in computability
theory. The repository asks whether there is a degree strictly between the computable degree and
the complete degree. Its recursion-theory category, Emil Post attribution, 1944 date, and the
immediately following Friedberg-Muchnik entry identify the intended family as the classical
question about an intermediate **computably enumerable Turing degree**.

That disambiguation does not yet freeze a canonical theorem. The catalog wording omits
"computably enumerable" and "Turing", does not identify the representatives used for degrees, and
is grammatically a question even though the untrusted metadata says `已解决` (solved). A secondary
source states the standard question as existence of a c.e. Turing degree `a` with
`0 <_T a <_T 0'`, and explains its positive Friedberg-Muchnik solution. Post's 1944 primary
publication is identified exactly, but its full text was not available for proposition-level
inspection. The solution papers, assumptions, transports, and relationship between the existence
and incomparability formulations also remain unaudited.

Pinned mathlib contains oracle reducibility and a partial-function quotient named `TuringDegree`.
It does not, on the inspected surface, supply c.e. sets as degree representatives, a computable
bottom and c.e.-complete top in that quotient, or the intermediate-degree existence theorem. The
included Lean file only authenticates those adjacent APIs; it does not select or prove a target.

The root is therefore provisionally `[H1, M4, R4]`. All six downstream tasks remain open. No exact
statement, source-proof acceptance, formal anchor, proof body, audit completion, theorem
completion, accepted receipt, or master state is claimed.
