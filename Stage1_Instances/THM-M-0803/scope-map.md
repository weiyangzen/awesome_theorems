# Scope map

## Included topic boundary

- Set-theoretic inner models and the constructible hierarchy/universe `L`.
- A source-specified theorem attributed to Jensen, if that attribution survives source inspection.
- The exact ambient theory, model predicate, construction, hypotheses, and conclusion of that theorem.
- Any necessary distinction between an assertion internal to a model and a metatheoretic relative-consistency result.

## Ambiguities to resolve at statement freeze

The repository phrase does not choose among these non-interchangeable readings:

1. **Constructibility theorem:** `L` is a transitive inner model satisfying specified axioms of
   set theory and containing all ordinals.
2. **Fine structure:** a theorem about the hierarchy of levels `L_alpha`, definability, condensation,
   or another fine-structural property associated with Jensen.
3. **Covering:** a version of Jensen's covering lemma, whose conclusion and hypotheses depend on
   whether `0#` exists and on the exact cardinal/set formulation.
4. **Generic inner-model result:** existence or properties of some inner model, possibly under a
   consistency or large-cardinal hypothesis.

The statement phase must select an immutable source passage and freeze one proposition. It must
specify the object theory (ZF, ZFC, or a fragment), ambient/metatheory assumptions, whether the model
is a proper class or set model, transitivity, ordinal containment, all ordered binders, and boundary
cases. The Chinese gloss can also be read as "an inner model *of* the constructible universe", which
is not automatically the standard theorem that `L` is an inner model; translation must be checked.

## Explicit exclusions

- `V = L` itself, which is the adjacent target `THM-M-0802` and is not a theorem of ZFC.
- The core-model target `THM-M-0804` or a large-cardinal inner model as a substitute.
- A rank, ordinal, transitivity, or class lemma merely because it is available in mathlib.
- A structure that assumes satisfaction of the desired axioms and returns that assumption.
- Any arbitrary theorem called the covering lemma without exact hypotheses and source crosswalk.
- The repository label `已验证` as evidence of a human proof or kernel closure.

No canonical Lean target is frozen at intake because the source record does not identify a
proposition.
