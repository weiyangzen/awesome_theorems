# Scope map

## Repository claims

The mathematics inventory describes `Church-Turing论题` as `可计算性的等价定义` ("equivalent
definitions of computability") and labels it `已验证`. A second repository inventory describes
the thesis as "all intuitively computable functions are computable by a Turing machine" and labels
it `不可形式化`. These are materially different scopes. Under rev-5.6 both status labels are
untrusted metadata and neither resolves the target.

## Provisional included formal family

- Two source-selected formal computation models, such as Turing computability, partial recursive
  functions, or lambda definability, with exact syntax and operational/denotational semantics.
- Fixed input and output domains and the encoding of tuples, natural numbers, partiality, and
  divergence.
- Both implications between the selected computability predicates, including effective compiler
  or coding maps and their semantic preservation proofs where the source theorem requires them.
- All source restrictions on total versus partial functions and unary versus multi-argument
  functions.

This is a family of mathematical equivalence theorems, not yet a frozen canonical theorem and not
the philosophical thesis itself.

## Decisions required at statement freeze

The statement phase must select one pinpointed primary theorem and freeze: both computation
models; syntax and evaluation relations; totality/partiality convention; domains and codomains;
number and tuple encodings; acceptable numbering and coding assumptions; whether the claim is
pointwise representability, equality of function classes, or computable bidirectional translation;
and every boundary case. It must also state whether the selected theorem is merely formal evidence
for the thesis or is the repository's approved canonical interpretation of the shorter mathematics
gloss. Ordered binders, universes, minimal imports, logical principles, and computation policy
remain open until then.

## Explicit exclusions

- A Lean predicate named `IntuitivelyComputable` whose hypotheses assume its equivalence with
  Turing computability; that would formalize the desired conclusion as an axiom.
- The unrestricted philosophical assertion about every effective method, because "intuitively
  computable" has no fixed formal extension supplied by the repository.
- Equivalence of only two convenient toy evaluators, or equality by definition, substituted for a
  historically substantive equivalence theorem.
- A one-way simulation advertised as equality of computable-function classes.
- The universal-machine theorem, undecidability of the halting problem, or Turing completeness of
  one programming language as a substitute.
- Historical agreement, empirical programmability, or the `已验证` label as kernel evidence.

If the primary-source audit concludes that the intended target is the informal thesis, the correct
result is an exact-statement blocker, not a broadened Lean theorem. If a formal equivalence is
selected, its relation to the thesis must remain explicit in every later artifact.
