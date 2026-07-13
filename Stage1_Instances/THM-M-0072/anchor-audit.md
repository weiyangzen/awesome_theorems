# THM-M-0072 Formal Anchor Audit

Item: `S56-M-0072-ANCHOR_AUDIT`

## Exact Comparison

The frozen root asks for an ambient conjugate of every Sylow-2 involution inside every maximal
subgroup of that Sylow subgroup. The bounded immutable inventory contains no Lean declaration with
that conclusion. The repository-local declaration is the exact proposition but has no proof body,
so the root remains `M3`.

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the right
transfer substrate. `MonoidHom.transfer` and its orbit-product and power formulas construct and
compute transfer. The Sylow specialization assumes that the Sylow normalizer centralizes the Sylow
subgroup, an assumption absent from the target. `MonoidHom.ker_transferSylow_isComplement'` proves
Burnside's normal-complement theorem, not an involution-conjugacy statement; Lean rejects it at the
literal target type.

The newer focal-subgroup module supplies an especially relevant intermediate language.
`Subgroup.focalSubgroupOf.mk'_conj_eq` identifies conjugates modulo the focal subgroup,
`Subgroup.transferFocal_eq_pow` computes focal transfer, and
`Subgroup.commutator_inf_eq_focalSubgroup` proves the focal subgroup theorem. These declarations
still do not construct an element of an arbitrary maximal `M` conjugate to the given involution.
Lean likewise rejects the focal theorem at the root type. They are `M3` substrate, not an exact
candidate and not proof credit.

## External Boundary

No exact candidate was found in the repository, the complete locally materialized pinned package
corpus, the immutable path inventory of `google-deepmind/formal-conjectures` at
`b2e608fc52d765510915a244bb69b1a2741acc3c`, or the bounded public Sourcegraph index queries.
`transferFocal` searches returned only mathlib's own module. GitHub repository searches returned no
focused project, while GitHub code search required authentication and grep.app returned a security
checkpoint. These are classified query outcomes, not proof of internet-wide absence. No public
external Lean body was admitted, so there is no pin/import task and no `M1` claim.

Thompson's 1968 Lemma 5.38(a)(i) and Lynd's versioned fusion-system paper remain human mathematical
source leads. Neither is a Lean artifact. Human-source fidelity remains `H1`; it is not advanced by
this formal-anchor phase.

## Result

The six candidate groups in inventory `S56-M-0072-ANCHOR-INVENTORY-20260713-01` are classified.
The inspected pinned proof-bearing substrate elaborates, reports only `propext`,
`Classical.choice`, and `Quot.sound`, and is reported sorry-free by Lean. The worker candidate and
accepted vectors both remain `[H1, M3, R4]`. The node is provisional pending master acceptance;
`audit_complete=false` and `theorem_complete=false`.

