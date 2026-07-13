# Source-statement crosswalk

## Repository records

`Docs/researches/math_theorems.md:5458-5463` is the target-bearing recursion-theory record. It gives
the title `停机问题`, Alan Turing, 1936, and the complete gloss `停机问题不可判定` ("the halting
problem is undecidable"). Git history places this uncited catalog text in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:20245-20270` repeats the
gloss while explicitly leaving definitions, premises, proof route, dependencies, equivalent
forms, axioms, and formal artifacts open.

Two repository records are useful but nonauthoritative discovery leads. The proof-theory entry at
`Docs/researches/math_theorems.md:5218-5223` repeats the same short gloss as `THM-M-0707`.
`Docs/researches/cs_theorems.md:23` expands that family as: there is no Turing machine that decides,
for an arbitrary Turing machine and given input, whether it halts. Neither lead resolves the exact
machine semantics or supplies a primary proof source. The manifest deliberately retains `已验证`
only as `source_status_untrusted` and resets this item to `L0 / rework_required`.

## Primary-source lead

The historical candidate is Alan M. Turing, *On Computable Numbers, with an Application to the
Entscheidungsproblem*, *Proceedings of the London Mathematical Society*, second series 42
(1936-1937), 230-265, with the 1937 correction on pages 544-546. Turing's source uses circular and
circle-free machines and related decision problems rather than the repository's exact modern
arbitrary-machine/input sentence.

The worker attempted to acquire a fixed scan from a university-hosted source, but the request
timed out and produced no file. Therefore no source hash, pinpoint statement, incorporated
definition chain, page-level proof map, translation, correction/errata disposition, or independent
review is accepted. The bibliography is a discovery lead only, not `E4` or `H0` evidence.

## Component crosswalk

| Repository or source-family phrase | Material mathematical component | Pinned Lean surface | Current assessment |
|---|---|---|---|
| "halting problem" | a program/machine model, input encoding, and finite termination semantics | `Nat.Partrec.Code`, `Code.eval`, and `Part.Dom` | selected conventional machine model; primary-source transport open |
| "arbitrary machine and input" | universal domain of valid program/input pairs | `Nat.Partrec.Code × Nat` | frozen pair domain; every Code is valid; Turing-machine transport open |
| "decides" | one total effective Boolean procedure correct in both directions | `ComputablePred` | frozen effective-decider contract; historical terminology mapping open |
| "undecidable" | negation of existence of that effective uniform decider | `¬ComputablePred Halts` | exact canonical target elaborated and fingerprinted |
| fixed-input halting | undecidability over all codes at one selected input | `ComputablePred.halting_problem n` | pinned proof-bearing lead; not the arbitrary-pair statement and not credited at intake |
| semidecidability | effective enumeration of halting computations | `ComputablePred.halting_problem_re n` | neighboring true result, not the root conclusion |
| `已验证` | untrusted catalog status | no expression or proof object | no H or M credit |

## Source, duplicate-target, and Lean boundary

`THM-M-0707` is a separately scheduled theorem with different repository identity, category, rank,
owned path, receipts, and reviewers. Its artifacts may guide discovery, but they cannot be imported
as accepted state, and this dossier does not edit or depend on that target. A master reviewer must
later decide whether the two catalog records receive an explicit checked equivalence, remain
separate source interpretations, or are reconciled by the target-set governance process. This
worker does not change the closed target set.

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `Statement.lean` freezes
the pair predicate with the sole direct import `Mathlib.Computability.Halting`. A checked
definitional iff reaches its expanded form, and the validator fingerprints it and four changed
contract/domain/scope/boundary shapes. This is still not an exhaustive anchor audit and supplies no
proof-body credit. Before `H0`, an independent source reviewer must approve the immutable primary
passage, assumptions, proof mapping, correction and errata record, and translation to this model.
Before crediting a concrete Turing-machine alternate, a checked transport in the required direction
must elaborate.
