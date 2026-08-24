# Full study: why the Boxdot composition proves inclusion

The frozen provider theorem has two conceptual layers. First, a theorem of a
normal modal logic is carried by the boxdot translation to another theorem of
that same logic. Second, the hypothesis that `L` faithfully interprets `KT`
says, formula by formula, that the translated theorem belongs to `L` exactly
when the original formula belongs to `KT`. The conclusion follows by composing
these layers.

Let `φ` be arbitrary and suppose `φ` is a theorem of `L`. Translation closure
gives that `boxdot φ` is a theorem of `L`. The forward direction of the faithful
equivalence at `φ` then gives that `φ` is a theorem of `KT`. Since the choice of
`φ` was arbitrary, every theorem of `L` is a theorem of `KT`, which is precisely
`L ⊆ KT`.

The claim-owned Lean surface makes the first layer an explicit `Set.MapsTo`
hypothesis and the second a pointwise equivalence. This isolates the exact final
composition independently of the pinned provider's unfinished theorem body.
The audit proves that `Set.MapsTo` plus subset notation is bidirectionally
equivalent to the fully elementwise form, so the wrapper changes presentation,
not mathematical content.

No source hypothesis is dropped: the carrier, translation, closure premise,
faithfulness premise, arbitrary formula, and membership proof all occur in the
proof DAG. There is no exceptional formula constructor in the composition.
Constructor-specific work is owned by the explicit translation-closure input;
the faithfulness premise is universal. The trust boundary is correspondingly
clear: this package proves the composition locally without any provider proof
body, while canonical Master must independently elaborate the source/target
semantic transport, constant environment, and cold trust-zero build.
