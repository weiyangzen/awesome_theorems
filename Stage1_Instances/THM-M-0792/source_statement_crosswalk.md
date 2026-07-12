# Source-statement crosswalk

| Claim component | Source anchor | Lean target | Intake assessment |
|---|---|---|---|
| Repository claim | `Docs/Stage0_Blueprint.md`, `THM-M-0792`: "力迫扩张的基本性质" (basic properties of forcing extensions) | none | Names a theorem family but omits domains, binders, hypotheses, and conclusion; insufficient to freeze a proposition |
| Historical forcing construction | P. J. Cohen, "The Independence of the Continuum Hypothesis", *Proceedings of the National Academy of Sciences* 50 (1963), 1143-1148, and 51 (1964), 105-110 | none identified | Primary historical anchor for forcing; a statement/premise/page and errata crosswalk remains open |
| Forcing relation definability | T. Jech, *Set Theory*, 3rd millennium ed., revised and expanded, Springer, 2003, the forcing chapter | candidate only | One standard component of the forcing theorem; exact theorem number, edition text, assumptions, and formula recursion must be pinned |
| Truth lemma | Same modern source family: truth in a generic extension is related to a condition in the generic filter forcing the formula | candidate only | Standard second component; it cannot silently replace the combined theorem |
| Combined forcing theorem | Definability lemma together with `M[G] |= phi(tau_1^G,...,tau_n^G)` iff some `p in G` forces `phi(tau_1,...,tau_n)` | no repo-local declaration identified | Leading interpretation of the title, but still provisional because the repository description says only "basic properties" |
| Generic model theorem | Claims that `M[G]` satisfies a selected base theory and has the expected relationship to `M` | none | Related but stronger/differently shaped family; not an accepted alternate encoding |
| Existing Lean discovery surface | Pinned mathlib comments cite J. Han and F. van Doorn, "A formalization of forcing and the unprovability of the continuum hypothesis" in model-theory modules | none audited | Bibliographic discovery only. No exact forcing theorem declaration, immutable external revision, or repo-local closure is claimed |

## Crosswalk gap

The following choices materially change the proposition and must be resolved before statement work:

1. whether the root is the definability lemma, truth lemma, their conjunction/equivalence, or a generic-model theorem;
2. the ground-model representation, required theory fragment, transitivity, countability, and set/class status;
3. the forcing-order convention and assumptions on the forcing notion;
4. the definition and external existence assumptions for a generic filter;
5. the syntax coding, formula arity, assignments, name hierarchy, valuation, and satisfaction relation;
6. whether parameters are arbitrary members of the extension or valuations of ground-model names;
7. whether the statement is an internal Lean theorem about coded models or an external metatheorem;
8. whether set forcing, Boolean-valued forcing, or class forcing is intended.

No `H0` claim is made. These citations are discovery anchors, not immutable evidence receipts. A
later source audit must pin editions or content hashes, locate exact statements and premises, check
corrections/errata, crosswalk every assumption, and obtain independent review. A later formal audit
must separately identify and inspect exact Lean declarations and terminal proof bodies.
