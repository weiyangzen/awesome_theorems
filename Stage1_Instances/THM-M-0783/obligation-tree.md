# THM-M-0783 frozen obligation tree

The registry freezes twelve semantic obligations before any proof phase. The proof spine is
`M0783-ROOT -> M0783-T-ASSEMBLE -> M0783-L-DENSE-FAMILY`, with the exact statement interface also
required by the root. The last arrow is a requirement, not evidence that Martin's axiom is provable.

## M0783-ROOT

Exact canonical target `MartinsAxiom`: `MA(kappa)` for every `kappa < continuum`. It remains `M4`.

## M0783-S-INTERFACE

Freeze universes, partial-order and nonemptiness instances, stronger-is-smaller orientation, ccc,
density, filter closure, indexed-family cardinal bound, and strict continuum bound. This interface
elaborates, but an elaborated proposition is not an inhabitant.

## M0783-L-DENSE-FAMILY

Given every binder and hypothesis of `ExpandedMartinsAxiom`, construct a filter meeting every dense
set. This is the whole additional set-theoretic axiom and the first open machine cut. It may not be
closed by declaring an axiom, adding MA as a hypothesis, or proving a weaker conditional theorem.

## M0783-T-ASSEMBLE

`root_of_denseFamilySolver` kernel-checks the transport from the expanded solver to the canonical
target. Its solver parameter is visibly open, so this composition earns no root proof credit.

## M0783-N-NA

No separate normalization is used: the canonical universal statement already is the selected
primitive form. The checked expansion is represented by `M0783-T-ASSEMBLE`.

## M0783-B-NA

No branch split is present. The dense-family obligation is uniform over every quantified instance.

## M0783-C-NA

There is no independently available construction layer. Constructing the meeting filter is exactly
`M0783-L-DENSE-FAMILY`, so duplicating it here would inflate coverage.

## M0783-X-SOURCE

Primary-definition mapping and independent acceptance remain open. The anchor audit is discovery
evidence only and explicitly distinguishes an additional axiom from a theorem of ZFC.

## M0783-X-FOUNDATION

Future evidence must show its full axiom and TCB boundary. An assumed or newly declared MA extends
the foundation and is forbidden as proof closure.

## M0783-X-PROVENANCE

Any future proof body must have an immutable repository revision, exact declaration, license,
terminal-body origin, exact-type check, placeholder scan, axiom report, and freshness inputs.

## M0783-X-READABLE

An independently reviewed readable reconstruction remains open and receives no machine credit.

## M0783-X-WORKFLOW

Proof, validation, independent verification, and release acceptance remain later typed workflow
gates. This worker freezes architecture only and does not claim audit or theorem completion.
