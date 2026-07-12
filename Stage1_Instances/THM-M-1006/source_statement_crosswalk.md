# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Martingale maximal function versus square function | D. L. Burkholder, *Distribution function inequalities for martingales*, Annals of Probability 1 (1973), 19-42, DOI 10.1214/aop/1176997023 | `Stage1Instances.THM_M_1006.StatementShape` | Finite discrete-time target selected and elaborated; theorem/page, assumptions, edition hash, and errata mapping remain anchor-audit work |
| Continuous-local-martingale quadratic-variation form | D. Revuz and M. Yor, *Continuous Martingales and Brownian Motion*, 3rd ed., Springer (1999), Chapter IV, section 4 (BDG inequalities) | No declaration selected | Standard source family identified, but a textbook citation is not accepted H0 evidence |
| Historical Davis contribution to the lower/maximum comparison | B. Davis, *On the integrability of the martingale square function*, Israel Journal of Mathematics 8 (1970), 187-190, DOI 10.1007/BF02771313 | No declaration selected | Discovery genealogy only; exact node crosswalk remains open |
| Uniform constants depending only on `p` | Burkholder (1973), subject to exact source crosswalk | existential `c C` before the probability space and martingale binders | Uniformity is structural; optimal constants are expressly excluded |
| Legacy repository wording: "equivalence of martingale Lp norms" | `Docs/Stage1_Blueprint.md`, THM-M-1006 | `Stage1Instances.THM_M_1006.StatementShape` | Resolved to the finite discrete-time, zero-initial, all-horizons form |

The source family contains several genuinely different formulations. The statement phase freezes
the finite discrete-time member without claiming transport to a continuous-time theorem. Its binder
order preserves `p > 0`, the martingale hypothesis, constant uniformity, the maximum time range,
and the zero-martingale boundary. Pinpoint primary-source fidelity remains anchor-audit work.

No claim of an existing Lean proof, `H0`, or machine closure is made. Source URLs above are
bibliographic discovery anchors, not immutable evidence receipts.
