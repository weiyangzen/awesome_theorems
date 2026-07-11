# Source-statement crosswalk

## Candidate primary sources

- Jacob D. Bekenstein, "Black Holes and Entropy", *Physical Review D* 7 (1973), 2333-2346,
  DOI `10.1103/PhysRevD.7.2333`. This is the historical entropy/area-proportionality source; the
  exact formula, assumptions, and equation anchor still require inspection.
- Stephen W. Hawking, "Particle Creation by Black Holes", *Communications in Mathematical
  Physics* 43 (1975), 199-220, DOI `10.1007/BF02345020`. This is the primary candidate fixing the
  Hawking temperature and the one-quarter coefficient; exact pages/equations and errata remain open.

These bibliographic records are discovery anchors, not `H0` evidence. The next phase must inspect
stable copies and record exact quoted statements, surrounding assumptions, conventions, and errata.

## Crosswalk

| Repository phrase | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| "black-hole entropy" | thermodynamic entropy assigned to a black hole | typed entropy quantity or explicitly normalized real | included; encoding open |
| horizon area | area of the relevant event-horizon cross section | geometric area or axiomatized nonnegative quantity | included; geometry open |
| one quarter | coefficient fixed by Hawking temperature | equality `S_BH = A / 4` in Planck units | included; convention open |
| dimensionful law | `k_B*c^3*A/(4*G*hbar)` | constants, nonzero denominators, dimensional semantics | included; domains open |
| physical regime | semiclassical gravity and source-specific black-hole hypotheses | explicit structure/hypotheses | required; exact list open |

## Evidence boundary

The Stage0 entry supplies only the Chinese label, a 1974 date, and attribution to Bekenstein and
Hawking; it does not contain a precise proposition. The Stage1 legacy prose similarly says only
"black-hole thermodynamic entropy" and lists broad mathlib interfaces. Consequently no exact
source statement can truthfully be elaborated during intake. A later wrapper must not assume the
area law as a structure field and then claim that projection as its proof.

