# THM-M-0003 rev-5.6 intake

This is the `planned` dossier for the snake lemma. The repository metadata's Chinese phrase
"short exact sequences induce a long exact sequence" is too broad by itself: the intended root is
the six-term kernel/cokernel exact sequence associated to a morphism of short exact sequences in an
abelian category. The dependent statement phase must confirm that interpretation against a pinned
source and the actual Lean declaration.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Ambient setting | An abelian category `C` | Universes, typeclasses, and foundation profile await elaboration |
| Input | The commutative diagram and exactness data represented by `ShortComplex.SnakeInput C` | Package fields have not yet been audited one by one |
| Construction | Connecting morphism from the left kernel to the right cokernel | Construction independence and naturality are later obligations |
| Root conclusion | Exactness of `S.composableArrows`, the kernel-to-cokernel sequence | Exact normalized type and expression hash remain open |
| Corollaries | Naturality, mono/epi connecting maps, and module specializations | Supporting scope only; none substitutes for the root |
| Excluded reading | The derived-functor long exact sequence of an arbitrary short exact sequence | Related mathematics, but not the snake lemma root |

The structured claim, ordered domains, candidate formal target, exclusions, and assurance boundary
are in `intake.json`. Source genealogy and the component crosswalk are in
`source_statement_crosswalk.md`.

## Open phase DAG

`STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
Each node remains open and depends on acceptance of its predecessor. Intake creates no proof-body
credit and does not inherit the historical `S1_M_098.lean` result.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M3, R3]`. The first failed theorem gate is
the exact-statement gate: there is no normalized expression hash, environment fingerprint, checked
transport, or mutation record. The theorem is not complete.

The commands in `validation.md` establish target membership, structural consistency, JSON syntax,
and dossier hygiene only.
