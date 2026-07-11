# THM-M-0104 Intake Dossier

## Identity and status

- Item: `S56-M-0104-INTAKE`
- Repository name: 贝祖定理 (Bezout theorem)
- Category: geometry / algebraic geometry
- Execution rank: 29
- Lifecycle: `planned`
- Baseline: `L0 / rework_required`
- Lane: `hard_mathlib_anchor_and_wrapper`
- Root debt at intake: human source unresolved; machine target unresolved; readable proof architecture not begun

The repository source gloss is only “an upper bound on the number of intersection
points of algebraic curves.” That gloss is underspecified. This dossier selects the
standard projective-plane, proper-intersection form as the **planned** canonical scope,
with the multiplicity equality as the root claim and the distinct-point upper bound as
a corollary. The statement phase must confirm this choice against a pinpoint primary
source before it may freeze or elaborate a formal target.

## Intake decision

The target is eligible because it occurs in the frozen 1546-target manifest at rank 29.
No legacy status or the source label `已验证` is accepted as proof evidence. The exact
coefficient field, curve representation, degree convention, local intersection
multiplicity, treatment of points at infinity, and finiteness mechanism remain open
statement obligations.

The authoritative scope is recorded in `intake.yaml`; `scope-map.md` enumerates the
semantic boundary and `source-statement-crosswalk.md` records what the repository
sources do and do not support.

## Phase boundary

This intake creates a planned instance only. It makes no theorem-completion claim and
does not claim source fidelity, Lean elaboration, a mathlib anchor, proof closure,
axiom closure, or master acceptance.
