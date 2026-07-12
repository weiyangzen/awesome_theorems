# THM-M-0790 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository topic "supercompact
cardinal". The only supplied claim is "properties of supercompact cardinals". That phrase names a
large-cardinal subject, not a proposition: it supplies neither a definition variant nor a property,
hypotheses, quantifiers, or conclusion.

Standard formulations quantify over every cardinal `lambda >= kappa` and use either an elementary
embedding with critical point `kappa`, closure of the target model, or a fine normal
`kappa`-complete ultrafilter on `P_kappa(lambda)`. These formulations require substantial encoded
set/model semantics and checked equivalence transports. Choosing one property such as
inaccessibility, measurability, or a compactness consequence would silently substitute a theorem.

The intake therefore freezes the ambiguity and an exact downstream scope rather than inventing a
target. The root remains `[H3, M4, R4]`. A pinned Lean probe checks only nearby cardinal,
ultrafilter, elementary-embedding, and ZFC-set APIs; it is not a definition or theorem about
supercompactness. Exact validation and remaining gates are in `validation.md`.
