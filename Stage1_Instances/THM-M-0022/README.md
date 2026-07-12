# THM-M-0022 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalogue item "Hecke character
theorem." The complete repository gloss is only "about a functional equation for L-functions."
It attributes the item to Erich Hecke in 1917 and labels it `已验证`, but rev-5.6 treats that label
as untrusted metadata rather than source or proof evidence.

The words point toward the functional-equation family for L-functions attached to Hecke
characters, but they do not determine one proposition. In particular, they do not select a
number field, definition or class of Hecke character, primitivity hypothesis, conductor and
infinity type, gamma-factor completion, dual character, reflection center, root number, or the
imprimitive and polar cases. The catalogue separately assigns `THM-M-0426` to "the functional
equation for Hecke characters" with the gloss "the functional equation of Hecke L-functions."
There is no accepted distinction, alias, or ownership decision between the two targets.

This intake freezes the received wording, the admissible theorem family, the duplicate boundary,
and the choices required before an exact statement can be selected. The canonical mathematical
statement and Lean target remain null. The provisional vector is `[H1, M4, R3]`: a classical
theorem family is recognizable but the exact primary-source proposition is unaudited; no exact
formal artifact is credited; and only this labeled intake map exists, not a proof reconstruction.

`instance.json` is the structured scope authority. `scope-map.md` and
`source-statement-crosswalk.md` preserve the statement and source decisions, while `task-dag.json`
keeps all six downstream phases open. `IntakeProbe.lean` checks only adjacent pinned APIs. No exact
statement, `H0`, `M0`, `R0`, audit completion, theorem completion, or master acceptance is claimed.
