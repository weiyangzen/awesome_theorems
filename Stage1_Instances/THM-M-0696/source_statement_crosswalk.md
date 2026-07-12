# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Every classically valid propositional formula is formally provable | Emil L. Post, "Introduction to a General Theory of Elementary Propositions," *American Journal of Mathematics* 43(3) (1921), 163-185, DOI `10.2307/2370324` | No object-language declaration selected | Primary historical source candidate for completeness of the Principia-style propositional calculus; exact quoted theorem/page, axiom basis, notation, and errata still require audit |
| Semantic validity ranges over all two-valued assignments | Post's truth-table treatment of truth functions | Candidate valuation type `Atom -> Bool`, with recursive formula evaluation | The modern semantic formulation appears historically aligned, but no source-to-definition or checked Lean mapping is accepted |
| General consequence `Gamma entails phi -> Gamma derives phi` | A modern proof-theory source must be pinned for the premise-context formulation | No context, entailment, or derivability API selected | This is the intended root, but it is stronger in surface form than empty-context tautological completeness unless a finite-premise/deduction transport is proved; arbitrary infinite contexts may also require compactness |
| Empty-context tautological completeness | Post's historical theorem family | Candidate Hilbert theoremhood predicate | Candidate alternate root only; it cannot silently discharge the stated premise-consequence root |
| Choice of proof calculus | Post concerns a particular propositional axiom system; modern natural-deduction and sequent presentations differ | Hilbert, natural-deduction, or sequent syntax | Completeness is relative to a calculus. The statement phase must select one, encode its rules, and later check any transport to another calculus |
| Classical rather than intuitionistic logic | Two-valued truth-function semantics validates excluded middle | Formula language must include a classically complete connective basis | Intuitionistic completeness uses different semantics and is expressly outside scope |

## Provenance boundary

The 1921 Post paper is a credible primary historical anchor and matches the manifest's year, but
this intake does not claim a pinpoint `H0` crosswalk. The exact scan/edition must be pinned and
hashed; the theorem statement, page, axiom basis, premise convention, and any corrections must be
mapped. A modern primary or authoritative source must also be selected for the general
premise-consequence formulation if that remains the canonical root.

Discovery locator, not an immutable evidence receipt:

- <https://doi.org/10.2307/2370324>

No machine status follows from this citation. No Lean declaration was found or credited during
intake, and tactic-level tautology procedures are not object-calculus completeness theorems.

## Statement-phase decisions

1. Select an atom type, inductive formula syntax, classically complete connective basis, and
   Boolean valuation semantics.
2. Select one explicit proof calculus and freeze the direction and binder order of semantic and
   syntactic consequence.
3. Decide whether contexts are finite lists/multisets/finsets or arbitrary sets. If arbitrary sets
   remain in scope, model the finite-use/compactness bridge rather than assuming it.
4. Elaborate the literal Lean target with minimal pinned imports and serialize its expression and
   environment fingerprint.
5. Mutation-test classical versus intuitionistic semantics, empty versus nonempty context, removed
   calculus rules, changed atom domain, binder scope, and empty/contradictory contexts.
6. Credit tautology, normal-form, decision-procedure, or alternate-calculus formulations only after
   kernel-checked transports.
