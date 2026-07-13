# THM-M-0213 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`双曲平行公设` (hyperbolic parallel postulate). The catalog attributes the entry to Nikolai
Lobachevsky and Janos Bolyai, dates it to 1830, and gives only the gloss `过直线外一点可作无数条平行线`
("through a point outside a line, infinitely many parallel lines can be drawn"). It supplies no
bibliography, geometry axioms, definitions, quantifiers, proof, or formal artifact. Its `已验证`
("verified") label is untrusted metadata under rev-5.6 and gives no source or Lean proof credit.

The gloss does not determine one stable proposition. It leaves open the ambient hyperbolic plane
or model, what counts as a line, incidence and betweenness conventions, whether "parallel" means
merely disjoint, limiting/asymptotic, or ultraparallel, how distinct lines are identified, and
whether "infinitely many" means `Set.Infinite`, a natural-number injection, or a stronger
cardinality claim. It also does not say whether this is an axiom assumed of a synthetic geometry,
a theorem derived from another axiom system, or a model-specific result. Choosing a familiar
version would add proposition-changing mathematics.

This intake therefore freezes the family and exclusion boundary while leaving the canonical human
and Lean statements null. The provisional root vector is `[H5, M4, R4]`: `H5` classifies the
received wording as not yet a stable theorem proposition, not as a claim that standard hyperbolic
parallel results are false; `M4` records that no usable exact formal artifact is admitted; `R4`
records that a source-faithful proof reconstruction cannot precede statement selection.

Pinned mathlib supplies genuine adjacent substrate: an analytic upper-half-plane carrier with its
Poincare metric, generic affine `lineMap`, and set infinitude APIs. None provides synthetic
hyperbolic lines, the source-selected parallel relation, or an exact postulate theorem.
`IntakeProbe.lean` checks only those interfaces. All six downstream phases remain open. No exact
statement, H0, M0, R0, accepted execution state, audit completion, theorem completion, or master
acceptance is claimed.
