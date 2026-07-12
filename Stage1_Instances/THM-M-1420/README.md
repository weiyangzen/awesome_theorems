# THM-M-1420 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "Pesin theory"
(`Pesin理论`). The complete mathematical gloss is "nonuniform hyperbolic theory"
(`非一致双曲理论`), attributed to Yakov Pesin in 1977. This identifies a research
theory, not one proposition with ordered binders, hypotheses, and a conclusion. The catalog label
`已验证` is explicitly untrusted under rev-5.6 and supplies no source or proof credit.

Pesin theory includes several inequivalent results and constructions: nonuniform stable and
unstable manifold theorems, Pesin blocks, absolute continuity of invariant foliations, closing and
local-ergodicity results, and entropy relations. Each requires choices about the dynamical system,
smoothness, invariant measure, Lyapunov spectrum, almost-everywhere scope, and conclusion. Selecting
one of these from memory would invent the missing mathematics. Oseledets' theorem and Pesin's
entropy formula also have separate repository IDs.

This intake freezes that ambiguity and the decisions an approved source correction must make. The
provisional root vector is `[H5, M4, R4]`. `H5` means only that the supplied catalog wording is not
yet a stable truth-valued proposition; it does not refute or declare open any theorem in Pesin
theory. No exact formal artifact or readable proof can be attached to an unidentified proposition.

The structured intake is `instance.json`, the permitted mathematical boundary is in `scope-map.md`,
and the literal source crosswalk is in `source-statement-crosswalk.md`. All six dependent phases
remain open in `task-dag.json`. `IntakeProbe.lean` checks adjacent pinned Lean APIs only and states
no target theorem. Exact validation is recorded in `validation.md` and the provisional worker
receipt. No H0, M0, R0, audit completion, theorem completion, accepted state, or master acceptance
is claimed.
