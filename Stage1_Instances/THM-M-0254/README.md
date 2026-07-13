# THM-M-0254 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label "functions of
bounded mean oscillation." The repository attributes the entry to Fritz John and Louis Nirenberg,
dates it to 1961, and supplies only the gloss "characterization of BMO functions." Its `已验证`
(`verified`) label is untrusted metadata under rev-5.6 and gives no human-source or Lean proof
credit.

The gloss names a subject or theorem family, not a truth-valued, binder-complete proposition. A
bibliographic lookup identifies John and Nirenberg's 1961 paper *On functions of bounded mean
oscillation*, but metadata alone does not determine whether the catalog intends the definition of
BMO, the John-Nirenberg distribution inequality, exponential integrability, an equivalent
`L^p`-oscillation characterization, or another result in that paper. In particular,
`THM-M-0302` separately owns the John-Nirenberg inequality and the gloss "exponential
integrability of BMO functions." Selecting that theorem here would silently substitute another
scheduled target.

This intake therefore preserves only the bounded-mean-oscillation characterization family and
leaves the canonical mathematical and Lean statements null. The provisional root vector is
`[H5, M4, R4]`: the received gloss is not a stable proposition, no exact usable formal artifact is
identified, and no source-faithful proof reconstruction can attach to an unfrozen target. `H5`
classifies the catalog wording as ill-posed for theorem execution, not BMO theory or the
John-Nirenberg theorem as mathematics; it is a worker proposal awaiting a master target decision,
source correction, and independent review.

The structured scope authority is `instance.json`. `scope-map.md` records every proposition-changing
choice, boundary case, and neighboring-target exclusion. `source-statement-crosswalk.md` maps the
catalog phrases to their missing source and Lean components. All six downstream phases remain open
in `task-dag.json`. `IntakeProbe.lean` authenticates only pinned set-average and Euclidean-volume
APIs; it states and proves no target theorem. No H0, M0, R0, accepted execution state, audit
completion, theorem completion, or master acceptance is claimed.
