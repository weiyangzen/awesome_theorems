# Scope map

## Included root claim

- Object family: the negative half of a quantized enveloping algebra associated with suitable symmetrizable Cartan data.
- Result: existence of Lusztig's distinguished canonical basis, not merely an arbitrary module basis.
- Required structure to preserve: the integral form, bar involution, and the source's basis characterization or construction.
- Parameters still requiring source freeze: Cartan/root datum conventions, base field and indeterminate, finite versus general type, and divided-power normalization.

## Decisions reserved for the statement node

- Identify the exact printed theorem(s) that jointly express the construction and basis property, including every hypothesis.
- Select or define Lean object models for Cartan data, the quantum group half, integral form, bar involution, and basis indexing.
- Freeze ordered binders, universes, coefficient rings, imports, environment fingerprint, and foundation/computation profiles.
- State checked transports among geometric, PBW, and quotient/construction presentations rather than treating them as definitional synonyms.
- Mutation-test symmetrizability, coefficient specialization, integral-form membership, bar invariance, and boundary ranks.

## Explicit exclusions

- The Kazhdan-Lusztig basis of a Hecke algebra (`THM-M-0140`).
- Kashiwara's crystal/global basis as a substitute without a checked equivalence theorem.
- A canonical basis for one low-rank quantum group as replacement for the general source claim.
- Positivity, categorification, tensor-product, or representation-basis corollaries unless they are part of the selected exact root.
- The proposition-valued skeleton in legacy `S1_M_057.lean` as an exact statement or proof.

These exclusions keep nearby canonical-basis results and formalization scaffolding from silently broadening or weakening the target.
