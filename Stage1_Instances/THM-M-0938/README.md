# THM-M-0938 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0938`, catalogued as
`Kneser定理` (`Kneser's theorem`). The repository supplies Martin Kneser, the year 1953, and only
the gloss `阿贝尔群上子集和的结构` (the structure of sumsets over abelian groups). It supplies no
bibliography, definition, binders, hypotheses, inequality, boundary convention, proof boundary, or
formal artifact. Its `已验证` field is untrusted metadata under rev-5.6.

## Intake result

Primary-source inspection exposes a material catalog ambiguity rather than resolving it. The date
1953 identifies Kneser's *Abschätzung der asymptotischen Dichte von Summenmengen*, whose opening
pages formulate an asymptotic-density dichotomy for sets of rational integers. A different paper,
*Ein Satz über abelsche Gruppen mit Anwendungen auf die Geometrie der Zahlen* (volume 61,
1954/55), states a finite-subset cardinality result in an arbitrary abelian group. A 1956 paper,
*Summenmengen in lokalkompakten abelschen Gruppen*, gives a Haar-measure formulation. These roots
have different domains, assumptions, conclusions, and encodings. The catalog's year points to the
first while its gloss points more naturally toward the latter two.

The familiar finite formulation is therefore recorded only as a candidate. Intake does not choose
between finite cardinality, integer asymptotic density, and locally compact Haar measure; nor does
it silently select an existential period subgroup, the canonical sumset stabilizer, a stronger
coset-count inequality, or a weaker cardinal bound.

Pinned mathlib supplies pointwise sumsets, set and finset stabilizers, and adjacent additive-
combinatorics results. `IntakeProbe.lean` authenticates those interfaces. A bounded exact-name
search found only a Freiman-Kneser TODO/reference, not a classical Kneser declaration. These are
discovery surfaces, not an exact target or proof.

The provisional catalog-target vector is `[H1, M4, R4]`. `H1` records published primary proof
sources while catalog-to-source identity, exact assumptions, corrections, translations, and
independent review remain open. No exact usable Lean target or source-faithful reconstruction can
attach before source selection. All six downstream tasks remain open. No H0, M0, R0, accepted
state, audit completion, theorem completion, or master acceptance is claimed.
