# THM-M-0077 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0077`, the group-theoretic
Hall theorem. The repository supplies only the gloss "existence of Hall subgroups in finite
solvable groups." Intake preserves that existence-only scope. It does not silently add the
classical conjugacy or containment conclusions, and it does not confuse this target with the
separate Hall marriage theorem.

The 1928 article *A Note on Soluble Groups* was identified from stable bibliographic metadata, but
the primary article text was not available in the repository and the observed publisher PDF
endpoint denied access. Consequently the exact theorem locator, the selected set of primes, the
definition of a Hall `pi`-subgroup, incorporated assumptions, proof boundary, and errata mapping
remain open. The catalog's `已验证` field is explicitly untrusted and supplies no H or M credit.

Pinned mathlib contains `IsSolvable` and several Hall-adjacent results: Sylow subgroups have
coprime order and index, the commutator subgroup of a finite Z-group does too, and a normal Hall
subgroup has a complement. `IntakeProbe.lean` checks these interfaces and their reported axioms.
A bounded search found no declaration for arbitrary-`pi` Hall-subgroup existence in every finite
solvable group. These facts establish vocabulary and downstream feasibility only; none is the
target theorem or proof credit.

The provisional root vector is `[H1, M4, R4]`: the historical article identity is known but no
source-complete proposition mapping is accepted; the exact Lean statement and general proof
candidate are unavailable; and no reviewed readable reconstruction exists. `instance.json` is the
structured scope authority, while `task-dag.json` leaves all six downstream phases open. No H0,
M0, R0, accepted proof state, audit completion, theorem completion, or master acceptance is
claimed.
