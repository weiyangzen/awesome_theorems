# THM-M-0526 proof architecture

## SVK-ROOT

The frozen root is exactly `SeifertVanKampenTarget` from `Statement.lean`. For fixed cover data,
`SVK-UP` supplies its universal property. The checked `compose_root` certificate consumes the three
typed interfaces of `SVK-UP`; it does not implement them.

```text
SVK-ROOT exact two-open-set based theorem
`-- SVK-UP fixed-cover pushout universal property
    |-- SVK-SQUARE inclusion square commutes
    |   `-- SVK-MAP-FUNCTORIALITY
    |-- SVK-EXISTS compatible cocone has a lift
    |   |-- SVK-LOOP-SUBDIVISION
    |   |   `-- SVK-LEBESGUE-NUMBER
    |   |-- SVK-CHANGE-BASEPATH
    |   |-- SVK-WORD-EVALUATION
    |   |   |-- SVK-WORD-DEFINITION
    |   |   `-- SVK-WORD-INDEPENDENCE
    |   |       |-- SVK-REFINEMENT-INVARIANCE
    |   |       `-- SVK-HOMOTOPY-INVARIANCE
    |   `-- SVK-LIFT-HOM
    `-- SVK-UNIQUE
        |-- SVK-GENERATION
        `-- SVK-AGREEMENT-ON-WORDS
```

The architecture follows the classical loop-subdivision route rather than silently substituting a
groupoid generalization or free-product presentation. Those alternate routes remain excluded until
a checked transport targets the exact frozen proposition.

## Open leaves

All nine logical leaves are open `[H2, M4, R4]`. Their budgets in `obligation-registry.json` are
prospective split limits, not completed proof ledgers. In particular, the compactness/subdivision
and homotopy-grid leaves carry the central geometric work and cannot be hidden behind a short
library invocation. `SVK-MAP-FUNCTORIALITY` is also a bridge obligation: the audited mathlib
declaration is support, not an identified proof of the target.

The minimal open root cut set is the complete nine-leaf set recorded by the registry. Closing only
the commutative square, or only generation, cannot close either `SVK-UP` or `SVK-ROOT`.

## Composition boundary

`ObligationTree.lean` defines exact propositions for square commutativity, lift existence, and lift
uniqueness. `compose_pushout` checks that all three yield the literal conjunction and `ExistsUnique`
conclusion in `IsFundamentalGroupPushout`; `compose_root` checks their cover-parametric packages
yield the exact root. Kernel axiom output reports `propext`, `Classical.choice`, and `Quot.sound`, and
no `sorryAx`. These are composition checks only. There is no local or imported Seifert-van Kampen
proof body, no closed leaf, and no theorem-completion claim.
