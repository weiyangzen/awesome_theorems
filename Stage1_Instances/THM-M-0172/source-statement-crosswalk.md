# Source-statement crosswalk

## Repository source record

`Docs/Stage0_Blueprint.md` records `THM-M-0172` as the Chern-Gauss-Bonnet theorem, summarizes it as
"Euler characteristic's intrinsic representation," attributes it to Shiing-Shen Chern, and gives
1944. It leaves precise definitions, hypotheses, proof path, axioms, equivalent formulations, and
machine artifacts unfilled. `Docs/Stage1_Targets_rev-5.6.json` repeats the Chinese name, places the
target in differential geometry, and carries an explicitly untrusted `已验证` source-status label.
Those records establish intake identity but not source fidelity or machine closure.

The repository separately contains `THM-M-0569` with the same Chinese theorem name but a different
UID, category, summary wording, and execution rank. This dossier does not merge the two UIDs or
borrow the other target's evidence. Any future deduplication is a master target-set decision.

## Candidate primary sources

- Shiing-Shen Chern, "A Simple Intrinsic Proof of the Gauss-Bonnet Formula for Closed Riemannian
  Manifolds," *Annals of Mathematics*, Second Series 45(4), 1944, pages 747-752. The title, date,
  and subject match the repository attribution and intrinsic-formula summary. This bibliographic
  anchor has not yet received edition-level formula and errata inspection in this intake.
- Shiing-Shen Chern, "On the Curvatura Integra in a Riemannian Manifold," *Annals of Mathematics*,
  Second Series 46(4), 1945, pages 674-684. This is a related primary development, not authority for
  silently changing the intended 1944 scope.

These are discovery anchors only. A later source audit must pin stable copies, locate exact formula
and page anchors, inspect assumptions and errata, map notation and normalization, and obtain
independent review. Until then the human status is `H1`, not `H0`.

## Crosswalk

| Repository/source phrase | Frozen mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "closed Riemannian manifolds" | smooth compact boundaryless Riemannian `M` | compact manifold-without-boundary structures and Riemannian metric | included; exact API open |
| even dimension and orientation | oriented `M`, `dim M = 2n` | orientation structure and finite-dimension witness | included; encoding open |
| intrinsic curvature data | Levi-Civita curvature two-form | connection and curvature API | included; convention open |
| Gauss-Bonnet integrand | normalized Pfaffian/Euler form | Pfaffian of curvature as a top form | included; sign and constants open |
| global formula | oriented integral over `M` | differential-form integration | included; API and codomain open |
| Euler characteristic | topological `chi(M)` | concrete topological/homological definition | included; representation open |
| equality | curvature integral equals `chi(M)` | exact equality with necessary coercions | included; Lean expression open |

## Intake discovery boundary

A scoped repository search found no target-specific legacy module or declaration for `THM-M-0172`.
A text search of the locally pinned mathlib sources found no Chern-Gauss-Bonnet, Gauss-Bonnet,
Euler-form curvature, or Pfaffian-curvature declaration. This is negative intake discovery, not the
precommitted immutable-revision anchor audit assigned to the later phase. It neither proves absence
of external formalization nor justifies `M0` or `M1`; the root remains `M4`.

Before the statement phase can pass, the exact primary formula must be crosswalked to a canonical
Lean proposition, including source convention, scalar codomain, connectedness, dimension zero,
and every smoothness, compactness, boundary, and orientation assumption.
