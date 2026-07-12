# THM-M-0158 rev-5.6 intake

This directory is the `planned` intake for the Weingarten equations. It freezes the intended
human claim as the local derivative formula for a chosen unit normal of a regular surface in
Euclidean three-space. In matrix form, the tangent coefficients of the normal derivative are
`- I^-1 II`, where `I` and `II` are the first and second fundamental-form matrices under the
convention recorded in `scope-map.md`.

The repository supplies only a short Chinese gloss and an untrusted `已验证` label. No prior
theorem-specific Lean artifact was found, and the exact primary-source theorem/page has not yet
been inspected. The provisional root vector is `[H1, M4, R4]`: the classical result and a modern
source family are identified, but source fidelity, the exact Lean target, and a readable proof
reconstruction remain open.

The statement phase now freezes and elaborates the exact local-coordinate target in `Statement.lean`;
its expression fingerprint, environment, mutation checks, and exact commands are recorded in
`statement.json` and `statement-validation.md`. This is provisional statement-only evidence. No
proof, audit completion, or theorem-completion credit is claimed.
