# THM-M-0779 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository claim "ZF+GCH is
consistent relative to ZF", attributed to Kurt Godel and dated 1938. The phrase identifies the
constructible-universe relative-consistency theorem, but it does not yet fix a formal sentence.

The intended mathematical direction is: from a model of ZF, construct its inner model `L`, show
that `L` satisfies ZF and GCH, and hence derive the metamathematical relative-consistency result.
This is not interchangeable with merely proving a cardinal equality in Lean's ambient universe,
with a ZFC model implemented using Lean choice, or with the later forcing direction.

The root remains `[H1, M4, R4]`. A bounded pinned Lean probe checks only that mathlib exposes
first-order theories and satisfiability, ZFC-set and cardinal APIs useful for later encoding. It
does not define ZF/GCH, construct `L`, or prove relative consistency. Exact commands and remaining
gates are recorded in `validation.md`.
