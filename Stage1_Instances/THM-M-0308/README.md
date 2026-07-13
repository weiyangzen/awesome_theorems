# THM-M-0308 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0308`, named "extension
theorem" by the repository and glossed only as "extension of Sobolev functions." The catalog also
attributes the item to Sergei Sobolev and gives the year 1936. It supplies no primary source,
domain class, Sobolev order or exponent, scalar range, extension operator, restriction identity,
or norm estimate.

"Sobolev extension theorem" denotes a family rather than one proposition. Common versions range
from a bounded linear operator on `W^{k,p}` over a Lipschitz domain to per-function existence,
fractional and homogeneous variants, and zero extension on `W_0^{k,p}`. Their hypotheses and
conclusions are not interchangeable. Intake therefore preserves the literal family boundary and
does not choose a familiar theorem from memory.

The provisional root vector is `[H5, M4, R4]`. `H5` means the received catalog phrase is not yet
one stable proposition; it does not dispute classical Sobolev extension results. `M4` records that
no exact usable formal artifact is credited, and `R4` that no source-faithful reconstruction can
attach to an unidentified root.

`instance.json` is the structured intake authority. `scope-map.md` records proposition-changing
choices and exclusions. `source-statement-crosswalk.md` distinguishes the two byte-identical
catalog records from target identity and maps the wording to later source and Lean obligations.
`IntakeProbe.lean` checks only adjacent pinned APIs, and `task-dag.json` keeps all six dependent
phases open.

This is a worker-self-tested intake proposal only. It supplies no canonical mathematical or Lean
statement, accepted source or proof state, audit completion, theorem completion, or master
acceptance.
