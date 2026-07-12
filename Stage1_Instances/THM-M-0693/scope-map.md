# Scope map

## Included topic boundary

- A source-selected logical language and its formulae.
- Sequents with an explicitly chosen antecedent and succedent representation.
- A concrete inductive derivability relation with its structural and logical rules.
- One exact metatheorem about that calculus, if an immutable source establishes that this target is
  intended to denote a theorem rather than merely the definition of a formal system.
- A checked mapping between the source notation and the eventual Lean encoding.

## Decisions required at statement freeze

The repository does not decide between propositional and first-order logic; classical and
intuitionistic logic; one-sided and two-sided presentations; or list, multiset, and set contexts.
It does not specify whether exchange is definitional or a rule, whether weakening and contraction
are present, whether the succedent is single or multiple, how eigenvariable conditions are stated,
or whether cut belongs to the primitive calculus.

Most importantly, it supplies no proposition. The statement phase must pin an immutable source and
decide whether the intended object is only a definition or an exact metatheorem such as soundness,
completeness, admissibility, decidability, or equivalence to another proof system. It must then
freeze ordered binders, universes, hypotheses, conclusion, empty-context behavior, and all rule
side conditions before a Lean target can receive statement credit.

## Explicit exclusions

- `THM-M-0692` cut elimination as the root of this separately identified target.
- Natural deduction (`THM-M-0694`), Hilbert systems, tableaux, resolution, or Lean's own tactic
  state as substitutes for a sequent calculus.
- An inductive type whose constructors merely assume the desired metatheorem.
- The identity axiom or cut rule alone as a theorem standing in for the unspecified root.
- A soundness or completeness result for a convenient special calculus absent a source crosswalk.
- The manifest label `已验证` as human-proof or kernel evidence.

No canonical Lean target is frozen at intake because the repository record is not propositionally
complete.
