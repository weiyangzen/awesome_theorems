# Scope map

## Included claim boundary

- A source-selected first-order presentation of ZF and exact encodings of CH and AC.
- The positive and negative sides of independence for each selected sentence.
- The metatheoretic assumptions needed to state relative consistency or construct models.
- Checked bridges among syntactic consistency, satisfiability, and model existence if more than one
  formulation receives credit.

## Ambiguities to resolve at statement freeze

1. Whether "independent" means two syntactic relative-consistency implications, two model
   constructions, unprovability/undisprovability under a consistency or soundness assumption, or a
   precisely checked combination.
2. Whether the CH base is ZF or ZFC. The repository literally says ZF, but standard presentations
   often state CH independence over ZFC.
3. Whether "CH is independent" includes the positive consistency direction associated with
   constructibility as well as Cohen's negative direction, and how attribution is recorded.
4. Which form of choice is meant and whether the negative result is `ZF + not AC`, a particular
   failure of choice, or a model construction with atoms followed by transfer.
5. The object-level language, proof calculus, model notion, universes, coding, and external
   metatheory in which consistency is expressed.

The statement phase must obtain immutable sources and freeze all ordered binders, hypotheses,
conclusions, foundation assumptions, and the relationship between the four components.

## Explicit exclusions

- Cardinal arithmetic facts about `Cardinal.continuum` as a substitute for CH independence.
- Mathlib's constructed `ZFSet` model or `ZFSet.choice`, which uses Lean's classical choice, as a
  substitute for an object-theory independence theorem.
- A generic theorem `T.IsSatisfiable` supplied as a hypothesis and projected back as the result.
- Independence over ZFC silently substituted for the literal ZF wording without a source crosswalk.
- Only `Con(ZF) -> Con(ZF + not CH)` presented as the whole two-sided CH claim.
- Historical mathematical certainty or the repository label `已验证` as machine evidence.

No canonical Lean target is frozen at intake because these choices remain source-dependent.
