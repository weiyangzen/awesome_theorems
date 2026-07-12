# THM-M-0331 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Stone's theorem on one-parameter
unitary groups. The repository supplies the topic-level gloss "one-parameter unitary groups and
self-adjoint operators" and a second duplicate gloss mentioning their exponential relation. This
identifies the Stone theorem family, but it does not freeze one exact proposition.

The standard theorem is commonly presented as a correspondence: a strongly continuous unitary
representation of the additive real group has a unique self-adjoint infinitesimal generator, and
conversely a self-adjoint operator generates such a group by functional calculus. The inventory
does not say whether the intended target is one direction, the converse, the biconditional, or a
uniqueness statement; nor does it define strong continuity, the unbounded generator, its domain,
or the sign convention in the exponential. Choosing these details without an exact source would
silently replace the source record with a stronger, invented target.

The intake therefore freezes that boundary rather than claiming an exact Lean statement. The root
is conservatively `[H1, M4, R4]`. A pinned Lean probe confirms that mathlib provides complex Hilbert
spaces, partially defined linear maps, self-adjointness, unitary operators, and continuity needed
for a future encoding. It is not Stone's theorem and receives no proof credit. Exact validation is
recorded in `validation.md`.

