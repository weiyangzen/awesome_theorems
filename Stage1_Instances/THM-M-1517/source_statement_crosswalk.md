# Source-statement crosswalk

| Source or claim component | Candidate mathematical node | Intake assessment |
|---|---|---|
| Repository source wording: `经典力学的拉格朗日形式` (the Lagrangian formulation of classical mechanics) | No unique proposition | It names a framework, not a theorem; quantifiers, regularity, boundary conditions, and conclusion are absent |
| J.-L. Lagrange, *Mécanique analytique* (Paris, 1788), historical mechanics source | Equations of motion in generalized coordinates | Primary historical work identified, but edition-level section/page, notation, assumptions, and errata crosswalk have not been established; it cannot yet yield `H0` |
| Candidate modern root: stationarity of the action implies the Euler-Lagrange equations | `ROOT-EL-FORWARD` (prospective ID only) | Plausible narrow theorem behind the label, but not accepted as canonical until a precise source and exact hypotheses are selected |
| Fixed endpoint condition | admissible variations vanish at interval endpoints | Essential to the usual integration-by-parts boundary cancellation; absent from the repository wording |
| Smoothness assumptions | differentiability of the Lagrangian and path sufficient for first variation and the fundamental lemma | Exact regularity is deliberately unfrozen; weakening or strengthening it changes the theorem |
| Configuration model | finite-dimensional real coordinates versus a smooth manifold | These encodings require nontrivial transports and possibly different conclusions; no equivalence is credited |
| Converse direction | Euler-Lagrange equations imply stationary action | Related but logically separate; excluded from the candidate root pending audit |
| Least action, conservation laws, Hamiltonian mechanics, constrained systems, and field theory | separate theorem families | Not consequences of the candidate statement without additional hypotheses; excluded from this intake root |

The source label's metadata status `已验证` is untrusted scheduling input and does not identify a
proof or machine artifact. The statement phase must first choose a primary/authoritative precise
formulation, record edition and pinpoint, freeze all ordered binders and hypotheses, then elaborate
the exact Lean expression and mutation-test endpoints, regularity, domain, and direction. Until
then, source fidelity is `H3` and machine status is `M4`.

Discovery locator, not an immutable evidence receipt:

- Bibliothèque nationale de France catalogue/scan discovery for Lagrange's 1788 *Mécanique
  analytique*; a stable edition hash and exact internal pinpoint remain required.

No claim is made that mathlib or another Lean 4 project already proves this candidate. That search
belongs to the later anchor-audit node and must record exact revisions, modules, declarations, and
dependency feasibility.
