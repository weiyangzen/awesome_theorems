# THM-M-0359 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "Mihlin
multiplier theorem". The repository source gives only the gloss "L^p boundedness of singular
multipliers", the year 1956, and an attribution to Sigurdur Helgason. It does not specify the
multiplier, derivative hypothesis, dimension, exponent range, Fourier normalization, or operator
whose boundedness is asserted. The attribution also requires source review: the theorem is usually
named for S. G. Mikhlin, so the metadata is not treated as historical evidence.

The scope map freezes the classical theorem family without silently choosing among several
non-equivalent derivative criteria and endpoint variants. The root remains `[H3, M4, R4]`. A pinned
Lean probe confirms that mathlib provides Fourier multipliers on Schwartz functions and tempered
distributions, temperate-growth predicates, and `L^p` predicates/norms. Those APIs are encoding
ingredients, not the Mihlin theorem or its proof. Commands and results are in `validation.md`.

