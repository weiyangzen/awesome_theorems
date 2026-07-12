# THM-M-0664 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for "cell decomposition in o-minimal
structures". The repository supplies only that theorem-family label, Pillay/Steinhorn, and 1988;
it gives no source title, theorem number, dimension, parameter convention, definition of a cell, or
choice between set-compatibility and definable-function forms. The metadata label `已验证` is
untrusted and supplies no proof credit.

The provisional root family is finite cylindrical cell decomposition: in an o-minimal expansion of
a dense linear order, every finite family of definable subsets of `M^n` admits a finite cylindrical
cell decomposition of `M^n` compatible with every member. This is a source-review boundary, not a
frozen statement. The statement phase must select and inspect a primary theorem and decide whether
the intended result also includes simultaneous preparation/continuity of definable functions.

`IntakeProbe.lean` checks only generic pinned mathlib ingredients for a later encoding. It does not
define o-minimality or cells and does not state or prove the target. The lifecycle remains `planned`
with root vector `[H3, M4, R4]`; audit completion and theorem completion are both false.
