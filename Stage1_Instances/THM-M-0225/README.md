# THM-M-0225 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the maximum modulus principle. The
repository catalog gives only the title, the attribution Karl Weierstrass, the year 1875, and the
gloss "the modulus of a holomorphic function cannot attain a maximum in the interior." Its
`已验证` label is untrusted metadata under rev-5.6, not a source audit or proof receipt.

The gloss identifies a classical theorem family but is false when read literally without a
constant-function exception: a constant holomorphic function attains its modulus maximum at every
point. It also does not select local versus global maximum, a domain and codomain, connectedness,
the meaning of holomorphicity near the point or on the domain, or whether the conclusion is local
constancy, constancy on a connected domain, or only constancy of the norm.

Pinned mathlib contains several direct named maximum-modulus declarations in
`Mathlib.Analysis.Complex.AbsMax`. Their hypotheses and conclusions differ materially.
`IntakeProbe.lean` authenticates representative local, connected-domain, scalar-value, and
boundary interfaces and reports their current axiom profiles. It does not select one interface as
the catalog root, establish statement identity, or credit a proof body.

The intake therefore freezes the catalog record, theorem-family boundary, pinned formal leads,
proposition-changing choices, exclusions, and six open downstream phases while leaving the
canonical mathematical statement and Lean target null. The provisional vector is `[H1, M3, R4]`:
the historically proved family is recognizable but no exact primary statement has been admitted
and reviewed; usable exact-topic pinned interfaces exist but no source-identical target or checked
transport is frozen; and no source-faithful proof reconstruction exists for an exact root.

`instance.json` is the structured scope authority. `scope-map.md` and
`source-statement-crosswalk.md` define the source and non-substitution boundary. `task-dag.json`
keeps all six downstream phases open. No canonical proposition, H0, M0, R0, accepted proof state,
audit completion, theorem completion, or master acceptance is claimed.
