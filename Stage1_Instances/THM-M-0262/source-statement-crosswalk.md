# Source-statement crosswalk

## Repository authority

`Docs/researches/math_theorems.md:1885-1890` supplies exactly the title `沙利定理`, Dennis
Sullivan, 1985, the gloss `有理函数动力学的分类`, importance `high`, and status `已验证`. All six
uncited fields entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:7247-7272` repeats the gloss while explicitly leaving the exact
definitions and premises, proof route, dependencies, equivalent forms, axioms, machine status, and
artifact links open. Its generic theorem-tree prose is planning boilerplate, not source evidence.
The rev-5.6 target manifest retains `已验证` only as `source_status_untrusted` and resets the target
to `L0 / rework_required`.

The repository also has a distinct record at `Docs/researches/math_theorems.md:10474-10479` for
`THM-M-1434`, `Sullivan无游荡域定理`, with the exact gloss `有理函数的无游荡域`. That explicit
separation prevents this broader, vaguer record from silently taking the no-wandering-domain
statement.

## Source leads inspected

R. Mañé, P. Sad, and D. Sullivan, *On the dynamics of rational maps*, **Annales scientifiques de
l'École Normale Supérieure**, Series 4, 16(2) (1983), 193-217, DOI
`10.24033/asens.1446`, is a credible source-family lead. The official Numdam record identifies the
authors, title, journal, issue, pages, DOI, and an open PDF. Its title and subject fit the catalog
gloss, but the catalog gives no citation or crosswalk selecting one theorem, definition, or proof
boundary from it. It therefore supplies ambiguity/discovery evidence, not a canonical root or H0.

Dennis Sullivan, *Conformal dynamical systems*, **Lecture Notes in Mathematics** 1007 (1983),
725-752, DOI `10.1007/BFb0061443`, is a broad source-context lead. Nothing in the catalog selects
one result from this chapter.

Dennis Sullivan, *Quasiconformal Homeomorphisms and Dynamics I. Solution of the Fatou-Julia
Problem on Wandering Domains*, **Annals of Mathematics** 122(2) (1985), 401-418, DOI
`10.2307/1971308`, matches the catalog year and author. It is not adopted: the repository assigns
that subject to `THM-M-1434`, and the inspected official journal page exposes bibliography but no
theorem text. No edition-to-catalog identity, pinpoint statement, assumption map, errata review, or
independent approval exists here.

## Component crosswalk

| Catalog component | Material interpretations | Required Lean surface | Intake result |
|---|---|---|---|
| `沙利定理` | one of several Sullivan or coauthored complex-dynamics results | one source-versioned canonical `Prop` | no theorem locator selected |
| `有理函数` | algebraic rational function, polynomial, or total rational self-map of the Riemann sphere | exact carrier, sphere model, evaluation at poles/infinity, degree and normalization | all open |
| `动力学` | iterates, orbits, periodic points, Julia/Fatou sets, critical behavior, stability, or parameter variation | total self-map, iterate convention, exact invariant-set and regularity predicates | all open |
| `分类` | classification of maps, conjugacy classes, components, stable regions, or dynamical behavior | classified type, equivalence relation, invariant/classes, exhaustiveness and uniqueness conclusion | no truth-valued conclusion supplied |
| 1985 | no-wandering paper or another historical association | source provenance only | conflicts with the separately cataloged no-wandering root |
| `已验证` | untrusted inventory metadata | accepted source and kernel receipts would be required | no H or M credit |

## Human-source boundary

The received author/topic/year wording is not a stable proposition, so the provisional
classification is `H5`. This does not refute or declare open any standard Sullivan theorem. To
leave `H5`, an accountable owner must approve a corrected truth-valued target, preserve and hash an
immutable primary source, identify the exact result and incorporated definitions, map every ordered
binder, hypothesis, conclusion, classification relation, invariant, exceptional case, and proof
dependency, check corrections and errata, explain the relationship to `THM-M-1434`, and obtain an
independent qualified source review.

## Lean boundary

The pinned environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, with mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. `IntakeProbe.lean` checks representative algebraic
rational-function, one-point compactification, meromorphic, connected-component, iteration, and
periodic-point APIs. A bounded name search found no target-specific complex rational-dynamics
declaration in repo-local Lean or pinned mathlib; unrelated measure-theoretic Fatou lemmas and
scheme-theoretic rational maps do not supply this target.

The canonical module, declaration or expression, elaborated-expression hash, environment
fingerprint, checked transports, and statement mutations remain null. The probe and search are
intake discovery only, not an anchor audit or proof evidence.
