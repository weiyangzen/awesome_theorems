# THM-M-0112 frozen obligation tree

The canonical route uses the classical relative-connectivity form of weak Lefschetz: construct the
complex Morse data, establish the index bound, obtain relative homotopy vanishing, and use the long
exact sequence to separate lower-degree bijectivity from boundary surjectivity. This architecture
is frozen before either package receives proof credit.

## M0112-ROOT

Exact `WeakTopologicalLefschetzTarget`. It requires `M0112-T-ASSEMBLE`; it is open at `M3`.

## M0112-S-INTERFACE

Bridge the dossier's typed but opaque geometric propositions and `piMap` to native analytic
realization, smoothness, projectivity, hyperplane inclusion, and functorial homotopy maps. This is a
critical obligation because arbitrary proposition fields cannot themselves yield weak Lefschetz.

## M0112-S-BOUNDARY

Resolve dimensions zero and one and the `Pi 0` convention induced by natural subtraction. No
silent assumption `n >= 2` may enter the proof.

## M0112-S-FOUNDATION

Audit classical choice, quotients used by homotopy groups, extensionality, all axioms, and the full
Lean/mathlib trust boundary.

## M0112-N-RELATIVE

Check the precise directed transport from relative homotopy vanishing to the inclusion map result,
with basepoints and the long exact sequence made explicit.

## M0112-C-MORSE-DATA

Construct the affine complement and compatible complex Morse or Lefschetz-pencil data, including
critical strata and all well-definedness and inclusion invariants.

## M0112-L-INDEX

Prove that the relative handles have real index at least the complex dimension. This central
geometric theorem remains a bridge obligation even if eventually invoked by one library call.

## M0112-L-CELLULAR

Turn the handle-index estimate into vanishing of relative homotopy below dimension `n`. This owns
the handle/CW comparison and cannot be hidden inside the long-exact-sequence step.

## M0112-B-BELOW

For every `k < n - 1`, consume both adjacent relative-vanishing facts to prove bijectivity. Its
planned formal output is `BelowBoundaryPackage`.

## M0112-B-EDGE

At `k = n - 1`, consume the required relative-vanishing fact to prove surjectivity only. Its
planned formal output is `BoundaryPackage`.

## M0112-T-ASSEMBLE

`weakTopologicalLefschetz_of_packages` is a checked conditional composition consuming both packages
and yielding the exact root. It has local composition credit only; it proves neither premise.

## M0112-X-SOURCE

Pinpoint primary-source theorem/page/assumption/errata mappings for the Morse, connectivity,
low-dimensional, and long-exact-sequence nodes. It carries no machine-proof credit.

## M0112-X-PROVENANCE

Record unique terminal bodies, wrappers, imports, transitive dependencies, axioms, TCB, and replay
receipts. It is an informational release overlay and cannot close a proof edge.

The frozen root cut set is `M0112-B-BELOW` plus `M0112-B-EDGE`. All listed leaf budgets are at most
100, but those budgets are decomposition thresholds, not evidence of proof or readable closure.
