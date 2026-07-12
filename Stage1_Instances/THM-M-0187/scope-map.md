# Scope map

## Preserved repository scope

The repository supplies four facts: the name "Aleksandrov uniqueness theorem", attribution to
Aleksandr Aleksandrov, the year 1942, and the gloss "uniqueness of closed surfaces of constant
Gaussian curvature". They are preserved as source metadata, but together they do not yet define a
truth-valued canonical claim.

## Candidate theorem families

1. **Constant Gaussian curvature rigidity (Liebmann family).** A sufficiently regular connected
   compact surface in Euclidean three-space with constant Gaussian curvature is a round sphere,
   with positivity and immersion/embedding hypotheses stated exactly. This best matches the gloss,
   but not the supplied theorem name, attribution, or year.
2. **Aleksandrov constant-mean-curvature theorem.** A sufficiently regular connected compact
   embedded hypersurface in Euclidean space with constant mean curvature is a round sphere. This
   matches a standard theorem name, but changes Gaussian curvature to mean curvature and does not
   match the supplied year.
3. **Aleksandrov convex-surface uniqueness/rigidity.** Closed convex surfaces with the same
   intrinsic metric, or data specified by an exact Aleksandrov uniqueness theorem, are congruent.
   This is compatible with the attribution and historical period but is not a constant-curvature
   statement as presently worded.

No candidate is adopted as the root at intake.

## Decisions required at statement freeze

The statement phase must select an immutable primary-source proposition and freeze: ambient
dimension and Euclidean structure; surface versus hypersurface; immersion versus embedding;
connectedness, compactness, boundarylessness, orientability, and convexity; differentiability
class; Gaussian versus mean curvature and its sign/normal convention; whether the curvature
constant is quantified or fixed and whether positivity is assumed or derived; the conclusion
(round sphere, congruence, or uniqueness up to rigid motion); and all boundary cases, including an
empty or disconnected surface and zero or negative curvature.

These choices alter binders, hypotheses, and conclusion. In particular, Gaussian curvature cannot
be replaced by mean curvature, and a classification as a sphere cannot be replaced by uniqueness
from an intrinsic metric without an approved source correction.

## Explicit exclusions

- Silently relabeling the gloss as Liebmann's theorem while retaining Aleksandrov attribution.
- Silently changing Gaussian curvature to mean curvature to obtain the soap-bubble theorem.
- Replacing global closed-surface rigidity with a local constant-curvature patch theorem.
- Assuming convexity, embeddedness, positive curvature, or sphere congruence inside a structure and
  projecting the desired conclusion from that assumption.
- Proving only that a round sphere has constant curvature (the converse direction).
- Treating the repository label `已验证` as human-source or Lean kernel evidence.

No canonical Lean expression is frozen during intake. The retry condition is an independently
reviewed source correction or exact primary proposition resolving the conflict above.
