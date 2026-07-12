# THM-M-1334 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the
Cauchy-Kovalevskaya theorem. The repository supplies the attribution
Augustin Cauchy/Sofia Kovalevskaya, the year 1875, and only the gloss
`解析ODE的解析解` ("analytic solution of an analytic ODE"). It supplies no
citation, definition of analyticity, ordered binders, hypotheses, exact
conclusion, proof, or formal artifact. Its `已验证` value is untrusted metadata
under rev-5.6 and gives neither human-source nor machine-proof credit.

The scope is materially ambiguous. The historical Cauchy-Kovalevskaya theorem
is a PDE Cauchy-problem theorem, whereas this catalog explicitly places the
target in ordinary differential equations. A modern source candidate states an
autonomous real finite-dimensional ODE theorem: an analytic vector field on an
open subset of `R^n` has a unique local analytic solution through every initial
point. That candidate closely matches the gloss, but choosing it would still
decide autonomy, real versus complex scalars, finite dimension, existence plus
uniqueness, the interval and solution predicates, and the meaning of analytic.

This intake freezes that mismatch and the candidate boundary instead of
inventing an exact target. The provisional root vector is `[H1, M4, R3]`: a
classical published theorem and a strong modern ODE source lead exist, but the
catalog-to-source statement and assumption map is unaudited; no usable exact
Lean artifact is identified; and this dossier supplies a scope/status surface,
not a readable proof reconstruction.

`instance.json` is the structured scope authority. `scope-map.md` records the
proposition-changing choices and exclusions, and
`source-statement-crosswalk.md` maps repository wording to the source leads and
pinned Lean boundary. `IntakeProbe.lean` checks only adjacent APIs and neither
states nor proves the target. Every downstream phase remains open in
`task-dag.json`.

The lifecycle remains `planned`. No canonical mathematical or Lean statement,
H0, M0, R0, accepted proof state, audit completion, theorem completion, or
master acceptance is claimed.
