# THM-M-0976 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for McDiarmid's inequality. The
repository catalog supplies Colin McDiarmid, the year 1989, and only the gloss `有界差函数的集中`
("concentration of bounded-difference functions"). Its `已验证` label is untrusted metadata under
rev-5.6 and supplies no source, exact statement, or proof credit.

The gloss identifies a classical theorem family but not one proposition. It does not fix the
independent coordinate spaces and laws, the product random input, the codomain and measurability of
the function, the coordinate-replacement relation, deterministic or almost-sure bounded-difference
constants, expectation/integrability conventions, the upper/lower/two-sided tail, the exponent
normalization, or zero-denominator cases. Selecting the familiar one-sided inequality
`P(f(X) - E f(X) >= t) <= exp(-2*t^2 / sum c_i^2)` at intake would add proposition-changing
mathematics absent from the repository record.

Crossref and Cambridge metadata identify a credible bibliographic lead: Colin McDiarmid, "On the
method of bounded differences," *Surveys in Combinatorics, 1989*, pages 148-188, DOI
`10.1017/CBO9781107359949.008`. The full chapter and an exact theorem passage were not admitted or
independently reviewed, so the lead supplies no `H0` credit.

The pinned Lean probe authenticates adjacent probability, independence, function-update,
integration, finite-sum, and exponential APIs. A bounded repository/mathlib search found no usable
exact McDiarmid declaration. The existing Hoeffding wrapper `S1_M_274.lean` explicitly excludes an
Azuma/McDiarmid bounded-difference theorem. These observations are intake discovery only, not an
anchor audit or proof result.

The provisional vector is `[H1, M4, R4]`: a credible human source lead exists but exact source
identity and mapping remain unaudited; no usable exact formal artifact is located; and no
source-faithful readable proof exists. All six downstream phases remain open. No canonical
mathematical or Lean proposition, accepted execution state, audit completion, theorem completion,
or master acceptance is claimed.
