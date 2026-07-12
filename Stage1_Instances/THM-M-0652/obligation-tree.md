# THM-M-0652 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 15 obligations before proof execution. The selected
route is completeness into a first-order calculus, cut elimination and Maehara
interpolant extraction, exact symbol-support transport, and soundness back to
mathlib semantics. The anchor audit found no terminal implementation of these
bridges, so the selection is architecture rather than proof credit.

The ordered machine, human-source, and readable denominators live in
`obligation-registry.json`. Any correction, split, merge, or eligibility change
requires registry version 2 with an append-only delta.

## Typed proof route

```text
M0652-ROOT  exact semantic Statement [open M3]
`-- M0652-T-ASSEMBLE  checked conditional composition [M0-L]
    |-- M0652-B-COMPLETENESS  semantic entailment -> derivation
    |   `-- M0652-N-CALCULUS  exact first-order calculus
    |       `-- M0652-S-BOUNDARY  degenerate vocabulary cases
    |-- M0652-T-SYNTACTIC  syntactic interpolation package
    |   |-- M0652-C-CUTFREE  cut elimination
    |   |   `-- M0652-N-CALCULUS
    |   |-- M0652-L-MAEHARA  rule induction
    |   |   `-- M0652-C-CUTFREE
    |   `-- M0652-L-VOCAB  occurrence/support transport
    |       `-- M0652-S-DEFINITIONS
    `-- M0652-B-SOUNDNESS  derivation -> semantic entailment
        `-- M0652-N-CALCULUS
```

Foundation, source, provenance, and trust obligations are isolated in their
typed graphs and receive no mathematical proof credit. Each node has a semantic
ledger and a budget no greater than 100 steps. A future proof phase must split
any node that exposes hidden rule cases, transports, or deeper terminal bodies.

## Composition boundary

`ObligationTree.lean` defines abstract package propositions and proves only that
completeness, syntactic interpolation, and soundness compose into the exact
canonical `Statement`. It constructs none of those premises. Thus the assembly
node is locally checked while the minimal root cut set remains those three
packages.

## Status boundary

The registry and seven graphs are structurally tested. This phase does not
implement a calculus, completeness, cut elimination, Maehara's lemma, soundness,
or Craig interpolation. It establishes neither source acceptance nor H0/M0/R0,
hermetic replay, independent verification, or theorem completion. The root stays
`[H2, M3, R3]`, lifecycle stays `planned`, and master acceptance remains required.
