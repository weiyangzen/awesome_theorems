# THM-M-0968 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0968`. The repository title
is `Erdős盒原理`, literally an "Erdős box principle," while the catalog attributes the item to Paul
Erdős in 1965 and gives the gloss `超图中的匹配` ("matchings in hypergraphs"). No citation or exact
proposition accompanies those fields, and the catalog's `已验证` label is untrusted metadata.

The title and gloss do not determine one theorem. A box-principle reading suggests pigeonhole-style
finite counting, but the repository already owns the ordinary pigeonhole principle as
`THM-M-0914`. In contrast, the author, year, and hypergraph-matching gloss closely match the family
stemming from Erdős's 1965 paper *A problem on independent r-tuples*. The paper family asks for
extremal sizes of uniform set families with bounded matching number, but it contains a general
problem, special cases, and a sufficiently-large-`n` theorem. Choosing the modern full conjecture,
the 1965 partial theorem, a special case, or ordinary pigeonhole would change the proposition.

The institutional scan of the 1965 paper and its zbMATH Open record were inspected as source leads.
The paper defines the threshold for forcing `k` pairwise-disjoint edges in an `r`-uniform
hypergraph, proves a sufficiently-large-`n` theorem on page 94, and separately proposes the full
extremal formula as equation (9) on page 95 while saying that its general case is elusive. The
zbMATH review also records a printed correction to equation (8). This evidence makes the intended
family highly plausible but does not decide which of the proved theorem and conjectural formula the
uncited catalog intends. No independent source review has admitted either as the root, so neither
receives `H0` credit.

Pinned mathlib supplies uniform finite-set-family and pairwise-disjointness vocabulary.
`IntakeProbe.lean` elaborates only those adjacent APIs. A bounded exact-topic search found no
Erdős-matching or hypergraph-matching terminal declaration in repo-local Lean or pinned mathlib.
Neither observation selects a statement or supplies proof credit.

The canonical mathematical and Lean statements remain null. The provisional root vector is
`[H5, M4, R4]`: `H5` classifies the received title/gloss conflict as not yet a stable proposition;
it does not classify the underlying Erdős results as false. All six downstream tasks remain open.
No H0, M0, R0, accepted proof state, audit completion, theorem completion, accepted receipt, or
master acceptance is claimed.
