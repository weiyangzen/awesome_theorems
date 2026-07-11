# THM-M-0395 frozen obligation architecture

Item: `S56-M-0395-OBLIGATION_TREE`

The registry freezes 17 semantic obligations before proof execution. It follows
the standard reduction of Mordell's conjecture to the Mordell-Lang theorem for
the Abel-Jacobi image of the curve. This is a proof plan, not a completed proof.
The pinned anchor audit found no terminal Lean 4 Faltings or Mordell-Lang body.

## Typed route

`M0395-ROOT` requires terminal composition `M0395-T`. The terminal composition
requires the finite-extension normalization `M0395-N`, Jacobian/Abel-Jacobi
construction `M0395-C`, Mordell-Weil `M0395-L1`, the Faltings/Mordell-Lang core
`M0395-X1`, the no-positive-dimensional-coset lemma `M0395-L2`, and the final
finite-union argument `M0395-L3`.

The proof graph stores reciprocal `proof_requires` and `composes` edges. The
statement layer is linked by `logical_decomposition`; provenance, evidence,
trust, documentation, and workflow are separate graph families and cannot
silently become mathematical premises. In particular `M0395-X2` is a trust
gate, not another proof of the theorem.

## M0395-root

Exact canonical statement `Stage1Rev56.THMM0395.Statement`. Open at `M4`.

## M0395-s

Statement and foundation interface, refined into `M0395-S1` rational sections,
`M0395-S2` curve hypotheses, and `M0395-S3` the checked finite-universal-set
transport. The transport is the sole `M0-L` unit and gives no root proof credit.

## M0395-n

Normalize to a finite number-field extension carrying a curve point. `M0395-N1`
must produce the extension and point; `M0395-N2` must preserve the hypotheses
and inject the original rational points into the base-changed point set.

## M0395-c

Construct the Jacobian (`M0395-C1`) and prove the based Abel-Jacobi map is a
closed immersion, hence injective on rational points (`M0395-C2`). These are
high-risk construction/bridge obligations, not library-name placeholders.

## M0395-l1

Establish Mordell-Weil finite generation for the Jacobian's rational points.

## M0395-x1

Supply the central Mordell-Lang/Faltings theorem for the curve image intersected
with the finitely generated Mordell-Weil group. This is the principal open root
boundary and must eventually resolve to an actual terminal proof body.

## M0395-l2

Prove that the genus-at-least-two Abel-Jacobi curve contains no translate of a
positive-dimensional abelian subvariety.

## M0395-l3

Turn the finite coset decomposition and zero-dimensionality into finiteness of
the rational intersection.

## M0395-t

Compose all exact child conclusions, transport finiteness back along the two
injections, and deliver the unchanged canonical root. This remains the frozen
root cut set and has no composition certificate yet.

## M0395-x2

Future terminal axiom, declaration-dependency, proof-body provenance, TCB, and
reproduction audit. It is linked by `trusts` and cannot affect proof coverage.

## Freeze boundary

The denominator is content-addressed in `obligation-registry.json`. Planned
formal signatures are explicitly labeled `planned:`. Any later split, merge,
exclusion, or target correction requires an append-only registry version; it
must not rewrite this freeze based on which obligations turn out to be easy.
