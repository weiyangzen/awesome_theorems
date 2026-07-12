# THM-M-0338 frozen obligation tree

Registry version 1 freezes 16 root-relevant obligations before any proof-closure metrics are
observed. The immutable denominator is
`e53a0b15267ae38e68bb1b727edd51b52d0b60c8f244fd912fc2153c2a0cca6e`.

The exact root (`M0338-ROOT`) retains the statement encoding audit and splits the final
`ExistsUnique` conclusion into extension existence (`M0338-E-EXTENSION`) and at-most-one among all
state extensions (`M0338-U-UNIQUE`). `M0338-T-ASSEMBLE` is the only implemented composition node:
Lean checks that those two interfaces imply the exact root, but supplies neither interface.

The uniqueness route is frozen through the Kadison-Singer/paving equivalence, Weaver KS2, and a
finite-dimensional MSS package. The MSS package separately owns the mixed characteristic
polynomial identity, interlacing selection, and real-stability/barrier bound. A distinct finite to
infinite transport prevents a finite matrix theorem from silently receiving operator-level credit.
Existence remains an independent bridge because the negative anchor audit found no exact terminal
Lean theorem that could close it.

Source, foundation/trust, and provenance nodes are separate overlays with their own eligibility.
They cannot be inferred from machine closure. Every node has a typed semantic ledger, a validation
recipe, and a step budget of at most 100 in `typed-graphs.json`; aliases and wrappers receive no
additional denominator credit.

The present open root cut set is `M0338-E-EXTENSION`, `M0338-KS-PAVING`, `M0338-W-MSS`,
`M0338-X-SOURCE`, and `M0338-X-FOUNDATION`. Root status remains M3 and theorem completion remains
false.
