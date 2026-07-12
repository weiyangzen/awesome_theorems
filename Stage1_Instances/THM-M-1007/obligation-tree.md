# THM-M-1007 frozen obligation architecture

Registry version 1 freezes the exact fixed-cutoff proof architecture before any proof-phase closure credit. Every node has a stable obligation ID and a substantive-step budget at most 100.

## root

**Claim:** For every independent measurable real sequence and fixed c > 0, almost-sure series convergence is equivalent to the three fixed-cutoff conditions.

**Role and output:** The exact frozen biconditional.

**Formal map:** `Stage1Instances.THM_M_1007.KolmogorovThreeSeriesTarget`

**Ledger and boundary:** Inputs are the typed proof/refinement children; the planned inference is `Stage1Instances.THM_M_1007.KolmogorovThreeSeriesTarget`; its exact output feeds the typed parent edge. Budget: 8 substantive steps. No proof closure is credited here.

**Status:** `[H1, M3, R3]`; source, machine, readable-review, and release gates remain as recorded in the structured node.

## s-interface

**Claim:** Preserve the probability space, ordered binders, measurability, mutual independence, positive cutoff, and natural-order convergence predicates.

**Role and output:** The exact binder and hypothesis interface.

**Formal map:** `Statement.lean:KolmogorovThreeSeriesTarget`

**Ledger and boundary:** Inputs are the typed proof/refinement children; the planned inference is `Statement.lean:KolmogorovThreeSeriesTarget`; its exact output feeds the typed parent edge. Budget: 18 substantive steps. No proof closure is credited here.

**Status:** `[H1, M3, R3]`; source, machine, readable-review, and release gates remain as recorded in the structured node.

## s-boundary

**Claim:** Retain values at abs X = c in the truncation and exclude them from the strict large-jump event.

**Role and output:** An exhaustive inclusive-cutoff policy.

**Formal map:** `truncate_eq_self_of_abs_le; truncate_eq_zero_of_lt_abs`

**Ledger and boundary:** Inputs are the typed proof/refinement children; the planned inference is `truncate_eq_self_of_abs_le; truncate_eq_zero_of_lt_abs`; its exact output feeds the typed parent edge. Budget: 12 substantive steps. No proof closure is credited here.

**Status:** `[H1, M3, R3]`; source, machine, readable-review, and release gates remain as recorded in the structured node.

## s-foundation

**Claim:** Fix the Lean kernel, classical measure-theory, integration, variance, and pinned dependency trust boundary.

**Role and output:** A versioned foundation and TCB decision.

**Formal map:** `Lean 4.29.0; mathlib 8a178386`

**Ledger and boundary:** Inputs are the typed proof/refinement children; the planned inference is `Lean 4.29.0; mathlib 8a178386`; its exact output feeds the typed parent edge. Budget: 16 substantive steps. No proof closure is credited here.

**Status:** `[H1, M3, R4]`; source, machine, readable-review, and release gates remain as recorded in the structured node.

## n-truncate

**Claim:** Replace X_n by Y_n = X_n on abs X_n <= c and zero outside, without changing the cutoff convention.

**Role and output:** The bounded truncated sequence Y.

**Formal map:** `Stage1Instances.THM_M_1007.truncate`

**Ledger and boundary:** Inputs are the typed proof/refinement children; the planned inference is `Stage1Instances.THM_M_1007.truncate`; its exact output feeds the typed parent edge. Budget: 14 substantive steps. No proof closure is credited here.

**Status:** `[H1, M3, R3]`; source, machine, readable-review, and release gates remain as recorded in the structured node.

## c-trunc-props

**Claim:** Prove each Y_n measurable, integrable, square-integrable, bounded by c, and mutually independent.

**Role and output:** All analytic and independence invariants needed by the bounded-series engine.

**Formal map:** `planned: measurable/integrable/MemLp and iIndepFun truncation package`

**Ledger and boundary:** Inputs are the typed proof/refinement children; the planned inference is `planned: measurable/integrable/MemLp and iIndepFun truncation package`; its exact output feeds the typed parent edge. Budget: 52 substantive steps. No proof closure is credited here.

**Status:** `[H1, M3, R3]`; source, machine, readable-review, and release gates remain as recorded in the structured node.

## c-event-indep

**Claim:** Derive mutual independence and measurability of the large-jump events {c < abs X_n}.

**Role and output:** The independence premise for converse Borel-Cantelli.

**Formal map:** `planned: iIndepSets events derived from iIndepFun`

**Ledger and boundary:** Inputs are the typed proof/refinement children; the planned inference is `planned: iIndepSets events derived from iIndepFun`; its exact output feeds the typed parent edge. Budget: 28 substantive steps. No proof closure is credited here.

**Status:** `[H1, M3, R3]`; source, machine, readable-review, and release gates remain as recorded in the structured node.

## b-large-jump-nec

**Claim:** From almost-sure convergence of sum X_n, prove summability of P(c < abs X_n) using X_n -> 0 and converse Borel-Cantelli.

**Role and output:** The first three-series condition in the necessity direction.

**Formal map:** `planned: converse Borel-Cantelli bridge`

**Ledger and boundary:** Inputs are the typed proof/refinement children; the planned inference is `planned: converse Borel-Cantelli bridge`; its exact output feeds the typed parent edge. Budget: 72 substantive steps. No proof closure is credited here.

**Status:** `[H1, M3, R4]`; source, machine, readable-review, and release gates remain as recorded in the structured node.

## b-large-jump-suff

**Claim:** From summability of P(c < abs X_n), prove that large jumps occur only finitely often almost surely by first Borel-Cantelli.

**Role and output:** Almost-sure eventual equality of X and Y.

**Formal map:** `MeasureTheory.ae_eventually_notMem plus event-series transport`

**Ledger and boundary:** Inputs are the typed proof/refinement children; the planned inference is `MeasureTheory.ae_eventually_notMem plus event-series transport`; its exact output feeds the typed parent edge. Budget: 46 substantive steps. No proof closure is credited here.

**Status:** `[H1, M3, R4]`; source, machine, readable-review, and release gates remain as recorded in the structured node.

## t-eventual

**Claim:** Show that two real series whose terms are eventually equal have equivalent convergence, pointwise and almost everywhere.

**Role and output:** Transfer of almost-sure convergence between X and Y.

**Formal map:** `planned: finite-prefix/eventual-equality series convergence transport`

**Ledger and boundary:** Inputs are the typed proof/refinement children; the planned inference is `planned: finite-prefix/eventual-equality series convergence transport`; its exact output feeds the typed parent edge. Budget: 34 substantive steps. No proof closure is credited here.

**Status:** `[H1, M3, R3]`; source, machine, readable-review, and release gates remain as recorded in the structured node.

## n-center

**Claim:** Decompose Y_n into the deterministic mean integral Y_n plus the centered variable Z_n and preserve independence and variance.

**Role and output:** A centered independent bounded sequence and deterministic mean series.

**Formal map:** `planned: Y_n = (Y_n - E Y_n) + E Y_n`

**Ledger and boundary:** Inputs are the typed proof/refinement children; the planned inference is `planned: Y_n = (Y_n - E Y_n) + E Y_n`; its exact output feeds the typed parent edge. Budget: 54 substantive steps. No proof closure is credited here.

**Status:** `[H1, M3, R4]`; source, machine, readable-review, and release gates remain as recorded in the structured node.

## l-bounded-nec

**Claim:** For independent uniformly bounded Y_n, almost-sure convergence implies convergence of sum E[Y_n] and summability of Var(Y_n).

**Role and output:** The second and third conditions from convergence of the truncated series.

**Formal map:** `planned: necessity half of bounded independent-series criterion`

**Ledger and boundary:** Inputs are the typed proof/refinement children; the planned inference is `planned: necessity half of bounded independent-series criterion`; its exact output feeds the typed parent edge. Budget: 100 substantive steps. No proof closure is credited here.

**Status:** `[H1, M3, R4]`; source, machine, readable-review, and release gates remain as recorded in the structured node.

## l-bounded-suff

**Claim:** For independent uniformly bounded Y_n, convergence of sum E[Y_n] and summability of Var(Y_n) imply almost-sure convergence of sum Y_n.

**Role and output:** Almost-sure convergence of the truncated series.

**Formal map:** `planned: Kolmogorov convergence criterion for centered bounded variables`

**Ledger and boundary:** Inputs are the typed proof/refinement children; the planned inference is `planned: Kolmogorov convergence criterion for centered bounded variables`; its exact output feeds the typed parent edge. Budget: 100 substantive steps. No proof closure is credited here.

**Status:** `[H1, M3, R4]`; source, machine, readable-review, and release gates remain as recorded in the structured node.

## t-necessity

**Claim:** Compose convergence, large-jump necessity, eventual truncation, and bounded-series necessity into all three right-hand conditions.

**Role and output:** The forward implication of the exact root.

**Formal map:** `Stage1Instances.THM_M_1007.ObligationTree.Necessity`

**Ledger and boundary:** Inputs are the typed proof/refinement children; the planned inference is `Stage1Instances.THM_M_1007.ObligationTree.Necessity`; its exact output feeds the typed parent edge. Budget: 24 substantive steps. No proof closure is credited here.

**Status:** `[H1, M3, R3]`; source, machine, readable-review, and release gates remain as recorded in the structured node.

## t-sufficiency

**Claim:** Compose Borel-Cantelli, the bounded-series sufficiency theorem, and eventual equality into almost-sure convergence of sum X_n.

**Role and output:** The reverse implication of the exact root.

**Formal map:** `Stage1Instances.THM_M_1007.ObligationTree.Sufficiency`

**Ledger and boundary:** Inputs are the typed proof/refinement children; the planned inference is `Stage1Instances.THM_M_1007.ObligationTree.Sufficiency`; its exact output feeds the typed parent edge. Budget: 22 substantive steps. No proof closure is credited here.

**Status:** `[H1, M3, R3]`; source, machine, readable-review, and release gates remain as recorded in the structured node.

## t-assemble

**Claim:** Consume exactly the necessity and sufficiency implications to assemble the canonical biconditional.

**Role and output:** The exact root, conditional on both directed obligations.

**Formal map:** `Stage1Instances.THM_M_1007.ObligationTree.root_of_directions`

**Ledger and boundary:** Inputs are the typed proof/refinement children; the planned inference is `Stage1Instances.THM_M_1007.ObligationTree.root_of_directions`; its exact output feeds the typed parent edge. Budget: 6 substantive steps. No proof closure is credited here.

**Status:** `[H1, M3, R3]`; source, machine, readable-review, and release gates remain as recorded in the structured node.

## x-source

**Claim:** Pinpoint and independently review a primary proof with assumption, cutoff, and errata mapping to every material node.

**Role and output:** Human-source coverage for the architecture.

**Formal map:** `primary-source page and proof crosswalk remains open`

**Ledger and boundary:** Inputs are the typed proof/refinement children; the planned inference is `primary-source page and proof crosswalk remains open`; its exact output feeds the typed parent edge. Budget: 36 substantive steps. No proof closure is credited here.

**Status:** `[H1, M5, R4]`; source, machine, readable-review, and release gates remain as recorded in the structured node.

## x-provenance

**Claim:** Record terminal proof bodies for Borel-Cantelli and every future bounded-series bridge, deduplicating wrappers and transports.

**Role and output:** Body-level provenance for all machine-critical leaves.

**Formal map:** `mathlib 8a178386 plus future local bodies`

**Ledger and boundary:** Inputs are the typed proof/refinement children; the planned inference is `mathlib 8a178386 plus future local bodies`; its exact output feeds the typed parent edge. Budget: 28 substantive steps. No proof closure is credited here.

**Status:** `[H1, M3, R4]`; source, machine, readable-review, and release gates remain as recorded in the structured node.

## x-tcb

**Claim:** Audit transitive Lean, mathlib, foundation, imported artifacts, axioms, and executable trust closure.

**Role and output:** Release-grade trust inventory.

**Formal map:** `Lean 4.29.0; mathlib 8a178386; release audit open`

**Ledger and boundary:** Inputs are the typed proof/refinement children; the planned inference is `Lean 4.29.0; mathlib 8a178386; release audit open`; its exact output feeds the typed parent edge. Budget: 24 substantive steps. No proof closure is credited here.

**Status:** `[H1, M3, R4]`; source, machine, readable-review, and release gates remain as recorded in the structured node.

## closure-boundary

`root_of_directions` kernel-checks only the final iff assembly. The root remains open at `M3`; no obligation is marked closed. The proof-phase cut set is the truncation-invariant package, event independence, both Borel-Cantelli branches, eventual-series transport, and both bounded independent-series directions. Primary-source, provenance, trust, readable-review, hermetic, and independent-validation gates also remain open.
