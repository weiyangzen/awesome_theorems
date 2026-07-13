# THM-M-0621 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Urysohn's lemma. The repository
catalog supplies the title, Pavel Urysohn, 1925, and the gloss `正规空间中闭集的分离`
(`separation of closed sets in a normal space`). It supplies no bibliography, exact theorem text,
definition convention, ordered binders, proof boundary, correction history, reviewer, or formal
artifact. Its `已验证` label is untrusted discovery metadata under rev-5.6.

The named classical family conventionally concerns a continuous real-valued function that is zero
and one on two disjoint closed sets. The gloss alone can also describe the open-neighborhood
separation built into a definition of normality. Intake therefore preserves the Urysohn
continuous-function family without silently choosing a proposition, a normal-versus-T4 convention,
a codomain encoding, endpoint orientation, or boundary-case policy.

Pinned mathlib contains the direct exact-topic interface
`exists_continuous_zero_one_of_isClosed` in `Mathlib.Topology.UrysohnsLemma`. It uses mathlib's
`NormalSpace` convention, which does not include `T1Space`, and returns a continuous map to `Real`
with values in `[0, 1]`. `IntakeProbe.lean` authenticates that interface and adjacent normal-space
APIs. This is discovery evidence only. No source-identical target, proof body, or downstream anchor
audit is credited.

The provisional family-level vector is `[H unclassified, M3, R4]`: no named publication or primary
source passage has been admitted for a human-proof classification, a usable direct pinned statement
interface exists, and no source-faithful readable proof has yet been reconstructed. This is not a
derived or accepted root state because the canonical root does not yet exist. The canonical
mathematical and Lean statements remain null. All six downstream tasks remain open. No accepted
state, audit completion, theorem completion, or master acceptance is claimed.
