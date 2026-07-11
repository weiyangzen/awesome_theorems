# THM-M-1068 rev-5.6 intake

This directory is the fail-closed `planned` intake for Tanaka's formula. The repository's only
statement, "the Ito formula for reflected Brownian motion", identifies the formula family but does
not fix which of several related identities is the root: the positive-part formula, the
absolute-value formula, or the reflected-Brownian/Skorokhod consequence. This intake preserves
that ambiguity rather than choosing an inequivalent variant.

The intended mathematical family concerns a real continuous semimartingale (at least Brownian
motion in the repository's stated scope), its stochastic integral against a sign or indicator
integrand, and local time at a level. Exact local-time normalization, sign convention, initial
condition, almost-sure quantification, and whether reflection is the theorem or a corollary must be
selected from a pinpoint primary source during the statement phase.

The manifest's historical `已验证` value is untrusted metadata and supplies no human-proof or
kernel-proof credit. No canonical Lean expression, elaboration hash, accepted source crosswalk, or
proof is claimed. The provisional root vector is `[H1, M4, R4]`; audit completion and theorem
completion are both false. See `scope-map.md`, `source-statement-crosswalk.md`, and `task-dag.json`
for the exact boundary and downstream work, and `validation.md` for this intake's checks.
