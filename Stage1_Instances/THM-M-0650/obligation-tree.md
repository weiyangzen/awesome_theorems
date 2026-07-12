# THM-M-0650 obligation tree

Item: `S56-M-0650-OBLIGATION_TREE`. Registry version: 1. This is a frozen
proof architecture, not a theorem-proof or release claim.

## Proof spine

```text
M0650-ROOT exact TarskiVaughtTarget
`-- M0650-T-SUBSTRUCTURE specialize to the subtype embedding
    |-- M0650-N-SUBTYPE normalize the inclusion as S.subtype
    |-- M0650-N-WITNESS align the witness premise
    `-- M0650-T-EMBEDDING embedding-level Tarski-Vaught theorem
        |-- M0650-B-FORMULA structural recursion on bounded formulas
        |   |-- M0650-B-ATOMIC falsum/equality/relation cases
        |   |-- M0650-B-IMPLIES implication case
        |   `-- M0650-B-FORALL universal case
        |       |-- M0650-L-WITNESS-NOT counterexample witness from phi.not
        |       `-- M0650-L-REINDEX Fin.snoc/default alignment
        `-- M0650-L-REINDEX final relabeling to Formula.Realize
```

The pinned mathlib theorem contains the central structural induction. Its short
substructure wrapper is not treated as a leaf that hides that work. The local
`root_of_embeddingTarskiVaughtPackage` declaration checks only the exact
child-to-parent specialization. Proof-phase integration and terminal-body
provenance remain downstream.

## Statement and trust overlays

### m0650-root

Exact target: `Stage1Instances.THM_M_0650.TarskiVaughtTarget`. It consumes the
substructure terminal composition. It does not yet carry proof-phase credit.

### m0650-s-definitions

Freezes bounded formulas, realization, the last-variable witness convention,
and `S.IsElementary`. The statement module is the formal authority.

### m0650-s-domains

Records the language universes, ambient model, substructure, coercion, and
finite parameter tuples. No arbitrary embedding is substituted for the root.

### m0650-s-boundary

Keeps `n = 0`; `nullaryParameterBoundary` checks that the premise has no hidden
positive-arity condition.

### m0650-s-transport

The canonical definition and pinned direct binder spelling are definitionally
equivalent. Only the witness-to-elementarity direction is in scope.

### m0650-s-foundation

Requires a later transitive report for `propext`, `Classical.choice`,
`Quot.sound`, the Lean kernel, dependency sources, and placeholder policy.

## Normalization and terminal nodes

### m0650-n-subtype

Packages the inclusion of `S` into `M` as the language embedding `S.subtype`.

### m0650-n-witness

Aligns the frozen substructure witness premise with the embedding premise.
This is checked by the local conditional composition theorem.

### m0650-t-embedding

The exact terminal candidate is
`FirstOrder.Language.Embedding.isElementary_of_exists` at pinned mathlib
revision `8a178386`. It remains open in this phase because proof integration,
transitive provenance, and trust acceptance are assigned downstream.

### m0650-t-substructure

`root_of_embeddingTarskiVaughtPackage` consumes the embedding package and
produces the exact root. It does not manufacture the package.

## Formula recursion

### m0650-b-formula

Expands the terminal body's recursion over the five bounded-formula
constructors rather than treating the imported theorem as one semantic step.

### m0650-b-atomic

The falsum, equality, and relation cases use term realization and preservation
by a language embedding.

### m0650-b-implies

The two induction hypotheses compose through implication realization.

### m0650-b-forall

One direction transports a source element forward. The reverse direction is
proved contrapositively and is the only branch using the witness premise.

### m0650-l-witness-not

Failure of the ambient universal supplies an ambient counterexample. Applying
the witness premise to the negated body yields a counterexample in the source.

### m0650-l-reindex

Tracks `Fin.snoc`, default free-variable assignments, composition, and the
final relabeling between bounded and ordinary formulas.

## External boundaries

### m0650-x-mathlib

Records the exact pinned wrapper-to-body chain. It cannot create duplicate
coverage credit for the wrapper and terminal body.

### m0650-x-source

Primary-source edition, theorem/page, assumptions, directionality, and a
reviewed node crosswalk remain open. The repository title and status label are
not source evidence.

### m0650-x-provenance

Full import, declaration-dependency, axiom, TCB, license, placeholder, replay,
and independent-validation closure remains a release boundary.

## Frozen boundary

The registry contains 19 unique obligations. The current root cut set is
`M0650-T-EMBEDDING`. The anchor audit identifies that node as a credible pinned
`M0-W` candidate, but this obligation-tree phase deliberately does not credit
or integrate its proof. Thus the root remains `M3`, with `H1`, `R3`, audit
completion, and theorem completion unchanged.
