# THM-M-1007 proof-phase execution

Item: `S56-M-1007-PROOF`

Attempt date: `2026-07-14` (`Asia/Shanghai`)

Base revision: `8f22279fd1216cdfb5676c758e6bdb08e0ba3e01`

## Verdict

`partial worker self-test`; 33 theorem/lemma declarations were checked, including 26 added in this
phase, but the exact Kolmogorov three-series root remains open. This packet proposes `[_]` only for
review of the implemented proof work. It proposes provisional proof closure for
`M1007-T-SUFFICIENCY` and
supplies its target-specialized martingale core for the still-planned generic
`M1007-L-BOUNDED-SUFF`, but no accepted state change or theorem completion.

`Proof.lean` now implements the measurable and bounded truncation package, all finite-measure
`MemLp` bounds and integrability, preservation of independence, measurable mutually independent
large-jump events, both Borel--Cantelli bridges, convergence-to-zero for terms of a convergent
natural-order series, finite-prefix convergence transport, almost-sure original/truncated series
transport, and the centering package. The latter includes measurability, independence, zero mean,
uniform bounds, finite moments, variance invariance, and transport across a convergent deterministic
mean series. A martingale argument now also proves convergence of centered canonical truncations
from summable variances, then proves the exact sufficiency implication of the frozen target.

These declarations materially support the planned truncation, large-jump, eventual-transport, and
centering branches, and provisionally closes the exact sufficiency node above. The worker does not
edit the frozen registry or accepted graph state because only the integration lane may reconcile
them. In particular, `Proof.lean` deliberately contains no declaration of
`Stage1Instances.THM_M_1007.KolmogorovThreeSeriesTarget`.

## Remaining proof cut

After provisionally crediting the new local bodies, the immediate mathematical cut is bounded
independent-series necessity:

- `M1007-L-BOUNDED-NEC`: almost-sure convergence of uniformly bounded independent variables must
  yield convergence of their deterministic mean series and summability of their variances.
Pinned mathlib provides Borel--Cantelli, independence postcomposition, variance, and martingale
convergence substrate. Those ingredients now close the sufficiency direction locally, but the
prerequisite anchor audit found no ready exact theorem for necessity. Retaining necessity as a
premise, postulating it, or proving a weakened substitute would not prove the frozen biconditional.
The exact root therefore remains `H1/M3/R3`, with
`root_closed=false`, `audit_complete=false`, and `theorem_complete=false`.

## Evidence boundary

The narrow replay creates disposable `Statement.olean` and `ObligationTree.olean` output in a
temporary directory and checks `Proof.lean` with `--trust=0 -t0`. Each of the 33 reported
theorem/lemma declarations has exactly the axiom closure
`[propext, Classical.choice, Quot.sound]`; no placeholder or disallowed declaration is present.
The existing pinned `.lake` artifacts are reused without update, build, clone, fetch, checkout, or
mutation. This is warm worker evidence, not a cold hermetic release or independent verification.

Full commands and results are recorded in `proof-validation.md`; the structured evidence is in
`proof-receipt.json`, and the unresolved root is recorded in
`proof-blocker-2026-07-14.json`.
