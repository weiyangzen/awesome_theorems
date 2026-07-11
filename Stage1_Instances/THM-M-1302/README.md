# THM-M-1302 rev-5.6 intake

This directory is the `planned` instance for the catalog item “仿微分算子” (paradifferential
operator). The source metadata says only “a tool for nonlinear PDE.” That is a mathematical topic
or construction, not a proposition with a truth value. The intake therefore preserves the target
identity but does not invent a theorem to make the next gate easy.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Catalog identity | Bony, 1981; paradifferential operators in nonlinear PDE | Metadata status “已验证” is untrusted and supplies no formal evidence |
| Mathematical object | A paradifferential operator formed from a symbol by frequency localization | The quantization convention and symbol class are not specified |
| Possible theorem families | mapping estimates, symbolic composition, adjoints, ellipticity/parametrices, paralinearization | None is selected as the root; selecting one without a source pinpoint would substitute the target |
| Neighboring record | Bony paraproduct decomposition (`THM-M-1301`) | It is explicitly excluded from this target |
| Formal surface | future Lean 4 proposition over pinned analytic infrastructure | No module, declaration, expression, or imports are claimed |
| Foundations | future Lean 4 kernel and audited classical/choice policy | Profile cannot be frozen before the proposition and analytic model are fixed |

## Open task DAG

`I1302-SOURCE` must locate the proposition-level primary-source identity. It unlocks
`I1302-SCOPE`, which freezes spaces, symbol class, indices, binders, assumptions, conclusion, and
degenerate cases. `I1302-LEAN` then elaborates the exact target; `I1302-TRANSPORT` checks alternate
encodings and mutations. These are open tasks, not proof obligations credited as complete.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H4, M4, R4]`. The first failed theorem gate is
the exact-source-statement gate. No theorem completion, machine closure, or historical “verified”
status is claimed. The structured record is `intake.json`, and the evidence boundary is detailed in
`source_statement_crosswalk.md`.

## Validation

The commands in `validation.md` establish manifest consistency, JSON syntax, dossier reference
integrity, and clean formatting only. No Lean declaration exists at this intake phase, so no kernel
validation is claimed.
