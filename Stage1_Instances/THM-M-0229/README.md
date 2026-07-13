# THM-M-0229 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Picard's Great Theorem. The
repository supplies Emile Picard, the year 1879, and only the gloss "in a neighborhood of an
essential singularity, the function takes all complex values with at most one exception." Its
catalog label `已验证` ("verified") is untrusted metadata under rev-5.6 and supplies no human-source
or Lean proof credit.

The gloss identifies a classical theorem family but omits proposition-changing details. It does
not bind the function and singular point, say where the function is holomorphic, define an isolated
essential singularity, quantify the neighborhoods, distinguish finite complex values from values
on the Riemann sphere, or include the standard recurrence clause that every nonexceptional value is
taken infinitely often arbitrarily close to the singularity. Intake does not silently add those
clauses from the theorem's familiar name.

A stable revision of the *Encyclopedia of Mathematics* article "Picard theorem" was inspected as
an authoritative source lead. It distinguishes the little and big theorems, states the big theorem
for a single-valued analytic function near an isolated essential singular point, and lists Picard's
1879-1880 publications. The article also explains the infinitely-often consequence. It is a
disambiguation lead, not accepted `H0` evidence: the repository cites no edition, the source's
definitions and proof boundary have not been preserved and crosswalked, and no independent review
is recorded.

The provisional vector is `[H1, M4, R3]`: a historically proved, recognizable theorem family and
an authoritative source lead are known; no exact source proposition or complete assumption map is
accepted; no usable exact Lean artifact is credited; and the dossier records a scoped proof route
but no source-faithful reconstruction. Pinned mathlib supplies punctured-neighborhood, removable-
singularity, meromorphic-order, and cluster-point substrate. `IntakeProbe.lean` authenticates those
interfaces but declares no target theorem.

`instance.json` is the structured scope authority, and `task-dag.json` keeps all six downstream
phases open. No canonical mathematical or Lean statement, H0, M0, R0, accepted execution state,
audit completion, theorem completion, or master acceptance is claimed.
