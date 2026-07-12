# THM-M-0218 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `庞加莱圆盘模型`
("Poincare disk model"). The catalog gives Henri Poincare, the year 1882, and only the gloss
`双曲几何的共形模型` ("a conformal model of hyperbolic geometry"). It supplies no mathematical
source, definition chain, hypotheses, conclusion, formula, or formal artifact. Its `已验证`
("verified") label is untrusted metadata under rev-5.6 and grants no source or Lean proof credit.

The gloss identifies a standard subject, not one truth-valued proposition. A later statement might
define a hyperbolic metric or line element on the open complex unit disk, characterize its distance
or geodesics, establish constant curvature and completeness, prove conformality with the Euclidean
disk, construct an isometry with another hyperbolic-plane model, or bundle several of these facts.
Those claims have different binders, structures, hypotheses, boundary cases, and proof obligations.
Selecting a familiar bundle at intake would invent mathematics absent from the source.

This intake therefore freezes the ambiguity and its scope boundary while leaving the canonical
mathematical and Lean statements null. The provisional root vector is `[H5, M4, R4]`: `H5` means
the repository target is not yet a stable proposition, not that standard Poincare-disk facts are
false; `M4` means no usable exact formal artifact is admitted; and `R4` means no source-faithful
proof explanation can exist before the proposition is selected.

Pinned mathlib contains `Complex.UnitDisc`, in a file titled "Poincare disc", but it defines only
the open complex unit disk with its inherited Euclidean topology and basic operations. Generic
conformality and an upper-half-plane Poincare metric also exist, but neither supplies a disk-model
statement. `IntakeProbe.lean` checks these adjacent APIs only. All six downstream phases remain
open. No canonical statement, H0, M0, R0, accepted proof state, audit completion, theorem
completion, or master acceptance is claimed.
