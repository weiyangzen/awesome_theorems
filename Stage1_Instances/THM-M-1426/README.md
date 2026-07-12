# THM-M-1426 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for catalog target `THM-M-1426`,
"multivalued random dynamical systems" (`多值随机动力系统`). The repository supplies only the
attribution "many mathematicians," the period "21st century," and the gloss "random systems with
nonunique solutions" (`非唯一解的随机系统`). It gives no primary-source locator, definition,
ordered binders, hypotheses, or truth-valued conclusion. The catalog's `已验证` label is explicitly
untrusted under rev-5.6.

A multivalued random dynamical system is a framework rather than one theorem. Depending on the
source, a target could define a measurable set-valued cocycle, construct one from a stochastic
differential inclusion, perfect an almost-sure cocycle, prove an attractor theorem, or establish
measurability, compactness, invariance, existence, uniqueness, or asymptotic behavior. These require
materially different state spaces, probability bases, time monoids, solution concepts, exceptional-
set conventions, regularity assumptions, and conclusions. Selecting one familiar result would
substitute mathematics not fixed by the catalog.

A 2002 paper by Caraballo, Langa, and Valero is a strong bibliographic candidate because its title
exactly names the catalog topic and its introduction explicitly treats nonunique stochastic
solutions. Its primary text contains a definition of an MRDS and several distinct attractor and
differential-inclusion theorems. The catalog does not cite the paper or select any one of those
results, so the paper is recorded as source-selection evidence only and receives no H credit.

The provisional root vector is `[H5, M4, R4]`. `H5` classifies the supplied catalog wording as not
yet a stable proposition; it does not refute or declare open any standard MRDS result. `M4` and `R4`
record that no exact formal artifact or proof reconstruction can be attached to an unidentified
proposition. `IntakeProbe.lean` checks only adjacent pinned relation, measurable-space, and
measure-preserving APIs and states no target theorem.

`instance.json` is the structured intake, `scope-map.md` freezes the proposition-changing choices,
and `source-statement-crosswalk.md` preserves the source boundary. All six dependent phases remain
open in `task-dag.json`. The provisional worker receipt and `validation.md` cover this intake only.
No exact Lean statement, H0, M0, R0, accepted proof state, audit completion, theorem completion, or
master acceptance is claimed.
