# Source-statement crosswalk

## Primary-source candidates

- Juan M. Maldacena, "The Large N Limit of Superconformal Field Theories and Supergravity,"
  arXiv:hep-th/9711200 (submitted 27 November 1997), especially the proposed duality between the
  large-`N` limit of certain conformal field theories and supergravity on anti-de Sitter product
  spaces. Exact version, passages, assumptions, and corrections remain to be inspected.
- S. S. Gubser, I. R. Klebanov, and A. M. Polyakov, "Gauge Theory Correlators from Non-Critical
  String Theory," arXiv:hep-th/9802109 (1998), candidate source for the generating-functional
  prescription. Exact equations and domains remain to be inspected.
- Edward Witten, "Anti De Sitter Space And Holography," arXiv:hep-th/9802150 (1998), candidate
  source for the boundary-CFT/bulk partition-function formulation. Exact equations, caveats, and
  renormalization conventions remain to be inspected.

These bibliographic records are discovery anchors, not `H0` evidence. Version-pinned source copies,
page/equation anchors, errata, and independent source review are downstream requirements.

## Crosswalk

| Repository phrase | Source-level component | Required formal component | Intake status |
|---|---|---|---|
| "AdS/CFT duality" | bulk/boundary correspondence | typed bulk and boundary theories plus equivalence predicate | included; models open |
| "gravity" | string/gravitational bulk theory, often in a limit | bulk state/field/action or observable semantics | included; regime open |
| "quantum field theory" | boundary conformal field theory | CFT states/operators/correlators or generating functional | included; foundations open |
| "duality" | equality of physical content via a dictionary | explicit map and preservation/equality laws | included; equality notion open |
| GKP/Witten prescription | sources/boundary values matched to bulk fields | equality of suitably defined functionals | candidate canonical slice |

## Statement risk

The three sources propose and develop a correspondence; they do not supply a single general
mathematical theorem with repository-ready domains and hypotheses. Consequently the source name
alone cannot justify a Lean proposition. The next phase must either formalize an honestly labeled
axiomatized correspondence statement (without proof credit) or select a genuinely proved special
result and explicitly record that it is not the full THM-M-1535 claim. Broadening, narrowing without
labeling, or assuming the desired equivalence is forbidden.

