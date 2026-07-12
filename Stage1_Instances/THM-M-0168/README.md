# THM-M-0168 rev-5.6 intake

This directory is the `planned` intake for the two-dimensional Bernstein theorem for minimal
graphs. It freezes the repository gloss "an entire-plane minimal graph is a plane" as the claim
that every sufficiently regular function on all of `R^2` whose graph in `R^3` is minimal is
affine. The scope map records both the geometric and minimal-surface-equation encodings; their
equivalence must be checked rather than assumed at the later statement gate.

The repository supplies only a short Chinese gloss, a 1910 attribution to Sergei Bernstein, and
an untrusted `已验证` label. It supplies no exact publication, theorem/page, hypotheses, proof, or
formal artifact. The provisional root vector is `[H1, M4, R4]`: the classical theorem and a modern
source family are identified, but pinpoint source fidelity, the exact Lean target, and a readable
proof reconstruction remain open.

The statement phase now freezes and elaborates the analytic `C2` minimal-surface-equation target
in `Statement.lean`, using only the pinned calculus definitions import. Its explicit expression,
environment fingerprint, and four structural mutation checks are recorded in `statement.json` and
`statement-validation.md`. This is provisional statement-only evidence. No proof, anchor audit,
geometric/PDE equivalence, or theorem-completion credit is claimed.
