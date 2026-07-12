# THM-M-0645 obligation tree

Registry version 1 freezes fifteen canonical obligations and separates the semantic proof route
from source, provenance, trust, documentation, and workflow relations. Every leaf has a substantive
step budget at most 100. Wrappers and the external anchor do not inflate proof coverage.

## M0645-ROOT

The exact `CompletenessTarget` elaborated in `Statement.lean`. It remains `[H2, M4, R4]` and requires
the exact calculus, exact semantics, and the terminal assembly route.

## M0645-D-CALCULUS

Freeze the finite classical natural-deduction rules, equality substitution, empty assumptions, and
`Empty` free-variable domain. A proof in a different calculus cannot silently close this node.

## M0645-D-SEMANTICS

Freeze validity over every nonempty structure using mathlib sentence realization. Empty-domain,
fixed-language, free-formula, or model-theoretic theory completeness variants do not close it.

## M0645-R-NEG-CONSISTENT

Reduce failure of empty-context derivability to consistency of the theory extended by the negated
sentence. This must be proved for the frozen calculus, including its classical and equality rules.

## M0645-C-HENKIN

Construct a consistent complete witness-saturated extension. The ledger includes enumeration,
witness introduction, consistency preservation, maximality, and the required choice principles.

## M0645-C-TERM-MODEL

Build the canonical nonempty structure from closed terms modulo provable equality. Function and
relation interpretations must be independent of representatives.

## M0645-L-EQUALITY

Prove that derivable equality is an equivalence and a congruence for every language symbol. This is
a separate root-critical obligation because the target language includes logical equality.

## M0645-L-TRUTH

By structural induction on formulas, identify realization in the term model with membership in the
complete Henkin theory. Quantifiers consume witness saturation; atomic equality consumes the
equality-congruence package.

## M0645-R-COUNTERMODEL

Assemble the consistency, Henkin, term-model, and truth-lemma results into a nonempty countermodel
whenever the sentence is not derivable.

## M0645-T-CLASSICAL

Use classical contraposition and double-negation elimination to turn the countermodel result into
`Valid phi -> Provable phi`. This delivers the substantive builder interface.

## M0645-T-ASSEMBLE

`completenessTarget_of_builder` is a kernel-checked introduction of the exact root binders from
`CompletenessDerivationBuilder`. It does not inhabit its premise and therefore does not close the
root.

## M0645-X-EXTERNAL

The immutable Foundation candidate remains an optional integration route. It requires checked
translations of syntax, calculus, equality conventions, semantics, and dependencies before its
terminal body can receive machine credit.

## M0645-X-SOURCE

Pinpoint primary-source passages and errata for every substantive proof node. This human-source
boundary is not a machine premise.

## M0645-X-PROVENANCE

Bind wrappers and conclusions to unique terminal bodies, immutable revisions, dependency closure,
and licenses. It is an assurance overlay and earns no semantic proof coverage.

## M0645-X-TRUST

Record transitive axioms, imports, placeholder and unsafe scans, kernel artifacts, and the no-oracle
boundary. It is release-critical but not a substitute proof premise.

## Typed graph boundary

`typed-graphs.json` stores proof, refinement, provenance, evidence, trust, documentation, and
workflow graphs separately. The local proof route is rooted at `M0645-ROOT` and reaches the open
Henkin/term-model leaves through reciprocal `proof_requires` and `composes` edges. The external
route is recorded as a bridge but is not falsely attached as an available proof child.
