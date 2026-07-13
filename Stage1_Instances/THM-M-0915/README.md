# THM-M-0915 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label `生成函数`
("generating functions"). The repository supplies only the gloss `组合序列的生成函数方法`
("the generating-function method for combinatorial sequences"), attributes it collectively to many
mathematicians in the eighteenth century, and labels it `已验证`. That label is untrusted metadata
and supplies neither human-source nor Lean proof credit.

The gloss names a method and subject, not a truth-valued, binder-complete proposition. It does not
select ordinary, exponential, multivariate, probability, or Dirichlet generating functions; formal
or analytic semantics; a coefficient carrier; a sequence or combinatorial class; hypotheses; or a
conclusion. Coefficient recovery, Cauchy products, recurrence solving, combinatorial product rules,
the exponential formula, and particular partition identities are distinct statements. Choosing any
one at intake would invent or substitute proposition-changing mathematics.

Herbert S. Wilf's *generatingfunctionology*, second edition, was inspected as an authoritative
subject-family lead. Its table of contents and pages 30-33 distinguish formal power series, ordinary
and exponential generating functions, analytic theory, and Dirichlet series, while equation (2.1.2)
gives the Cauchy product. This confirms the ambiguity rather than selecting a root. The catalog does
not cite Wilf, and no exact theorem/page, assumption, proof, errata, or independent-review crosswalk
has been accepted. The book therefore receives no `H0` credit.

Pinned mathlib supplies formal power-series construction, coefficient recovery, extensionality, and
Cauchy-convolution APIs. `IntakeProbe.lean` authenticates those adjacent interfaces only. It does
not define the catalog's intended method, select a theorem, or prove `THM-M-0915`.

The canonical mathematical and Lean statements remain null. The provisional vector is
`[H5, M4, R4]`: `H5` classifies the received method gloss as not yet a stable proposition; it does
not classify established generating-function mathematics as false or open. All six downstream
phases remain open. No H0, M0, R0, accepted state, audit completion, theorem completion, accepted
receipt, or master acceptance is claimed.
