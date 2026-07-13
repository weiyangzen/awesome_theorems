# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:11756-11761` records only the title `密码学`, proposer
`众多数学家`, time `20世纪`, gloss `现代密码学`, importance `高`, and status `已验证`. It supplies no
bibliography, formula, definitions, quantifiers, hypotheses, conclusion, proof, corrections, or
formal artifact. All six lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; that establishes repository provenance, not a
primary mathematical source.

`Docs/Stage0_Blueprint.md:43390-43415` repeats the gloss while explicitly leaving the formal system,
foundation, precise definitions and premises, proof route, dependencies, equivalent forms, axioms,
machine status, and artifact links open. The target manifest retains `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Clause crosswalk

| Catalog component | Missing mathematical component | Prospective Lean surface | Intake status |
|---|---|---|---|
| `现代` | historical or technical meaning, security parameter, asymptotic and computational model | natural-number parameter, complexity predicate, limit/bound conventions | absent |
| `密码学` | primitive/protocol syntax, algorithms, spaces, correctness and security notions | structures and functions over messages, keys, randomness, games, adversaries | absent; no definition accepted |
| implicit theorem | exact assumption, game or reduction, quantified agents, advantage, conclusion | one binder-complete `Prop` | absent; field label only |
| `众多数学家` / `20世纪` | source identity, edition, exact result locator, proof boundary and corrections | immutable source revision and node crosswalk | untrusted metadata only |
| `已验证` | human proof mapping or formal declaration, body, dependency and kernel receipt | accepted H or M evidence | no credit |

## Source-family discovery boundary

The separate computer-science survey at `Docs/researches/cs_theorems.md:288-348` lists mutually
different claims about one-way functions, pseudorandomness, zero knowledge, commitments, secret
sharing, public-key encryption, signatures, chosen-ciphertext security, and homomorphic encryption.
That inventory demonstrates ambiguity; none of its rows is linked as the source statement for
`THM-M-1596`, and its metadata statuses supply no evidence here.

The same survey's bibliography names Oded Goldreich, *Foundations of Cryptography* (2001-2004).
Crossref identifies the monograph *Foundations of Cryptography*, Cambridge University Press, DOI
`10.1017/CBO9780511546891`, published 2001-08-06. This is a broad bibliographic lead only. The
repository does not link it to this target or provide a volume, chapter, page, theorem, incorporated
definitions, correction audit, or proposition crosswalk. It therefore supplies neither a canonical
statement nor H0 credit.

## Pinned Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Probability.Distributions.Uniform` provides finite uniform probability mass functions,
while `Mathlib.Computability.TuringMachine.Computable` provides finite Turing-machine and abstract
computability-in-polynomial-time interfaces. `IntakeProbe.lean` checks six such declarations. These
are plausible substrate for some formal security models, but they define no cryptographic primitive,
game, adversary, advantage, reduction, or source-selected theorem.

A bounded case-insensitive search over repo-local Lean and pinned mathlib found only unrelated uses
of words such as “indistinguishable,” “decrypting,” and “decipherability,” and no source-selected
cryptography declaration. This is discovery-only evidence, not an exhaustive anchor audit or a
global absence proof.

## Required source acceptance

The statement phase may proceed only after accountable reviewers select one immutable truth-valued
source proposition, freeze every primitive, algorithm, space, computational/adversarial model,
security experiment, probability and advantage, assumption, quantifier, conclusion, reduction,
asymptotic convention, and boundary case in `scope-map.md`, and approve the pinpoint source and
correction mapping. A fresh statement worker must then elaborate exactly that claim with minimal
pinned imports and run removed-hypothesis, changed-domain, binder-scope, and boundary mutations.
