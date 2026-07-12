# THM-M-0516 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "Iwasawa
theory". The source inventory supplies only the gloss "p-adic L-functions of cyclotomic fields",
an attribution to Kenkichi Iwasawa, and the period "1960s". That is a research area, not a theorem
statement: it gives no prime, character, function, interpolation formula, domains, hypotheses, or
conclusion.

Several materially different claims fit the gloss, including construction and interpolation of a
Kubota-Leopoldt p-adic L-function, arithmetic consequences in a cyclotomic tower, and structural
theorems for Iwasawa modules. The adjacent repository entry for the Iwasawa main conjecture is
separate and cannot silently be substituted. The intake therefore freezes this ambiguity and the
exclusion boundary rather than inventing a proposition.

The root remains `[H3, M4, R4]`. A pinned Lean probe confirms that mathlib exposes cyclotomic
fields, p-adic numbers and integers, Dirichlet characters, and complex Dirichlet L-series. These are
encoding ingredients only, not a p-adic L-function theorem or proof. Exact commands and results are
recorded in `validation.md`.
