# THM-M-0400 obligation registry and typed graphs

This artifact freezes the pre-closure architecture for
`S56-M-0400-OBLIGATION_TREE`. The authoritative structured record is
`obligation-tree.json`; `check_obligation_tree.py` checks its registry digest,
required node fields, denominators, edge endpoints, proof reachability, and
proof acyclicity. Planned statements and step ledgers are execution
specifications, not evidence that their mathematics has been proved.

## Root

`M0400-ROOT` is exactly `Stage1Rev56.THMM0400.Statement`. It can close only by
a checked `M0400-T-COMPOSE` term. The graph gives no credit to the rejected
legacy shape, the one-dimensional approximation results, or the height API.

## Statement and boundary

`M0400-S-DEFINITIONS` owns the three repository encodings. `M0400-S-BOUNDARY`
owns the nonzero-vector height lower bound and the `n >= 2` boundary. These are
separate from the deep number-theoretic engine so that elementary encoding
work cannot disguise an open root.

## Normalization

`M0400-N-COEFFICIENT-FIELD` requires a common finite coefficient field and
compatible complex embedding. `M0400-N-TRANSPORT` requires a checked one-way
transport from a pinpointed source formulation to the exact height, strict
inequality, coercions, and rational-submodule conclusion in `Statement.lean`.
It remains `split-required` because the primary theorem/page and premise
crosswalk are not yet known.

## Core engine

The central route is conservatively divided into auxiliary construction
(`M0400-C-AUXILIARY`), its nonvanishing/index result
(`M0400-L-NONVANISH`), the height-gap/dependence estimate (`M0400-L-GAP`),
rational subspace extraction (`M0400-C-SUBSPACE`), and finite exceptional
cover (`M0400-L-FINITE-COVER`). This is an obligation boundary, not a claim
that one particular published proof has already been verified. Nodes whose
exact signature depends on the primary proof are explicitly `split-required`;
they must be revised append-only after the source crosswalk, then recursively
expanded before machine closure.

## Terminal composition

`M0400-T-COMPOSE` must bind exact child fingerprints, introduce the canonical
binders in order, consume every required conclusion, and produce the complete
root without a new premise. It is open. No child-to-parent Lean certificate is
present in this phase.

## Trust and source boundaries

`M0400-X-FOUNDATION` owns the eventual transitive declaration, axiom, compiled
artifact, executable, and TCB closure. `M0400-X-SOURCE` owns the exact primary
edition/theorem/page, assumption and transition crosswalk, errata audit, and
independent review. The current source status is only `H1`, and the current
machine root is only statement-elaborated historical evidence (`M3`).

## Frozen denominators and status

The registry contains 13 unique obligations: 12 machine-required, 10
human-source-required, and 13 readable-required. Closed-machine, accepted H0,
accepted R0, and accepted terminal-body numerator sets are all empty. The
minimal currently recorded open root cut set is the auxiliary construction,
nonvanishing, gap estimate, finite cover, convention transport, and terminal
composition. Alias, wrapper, and presentation rows add no denominator credit.

The obligation-tree phase is structurally self-tested. Audit completion and
theorem completion remain false, and master acceptance is still required.

## Validation record

Base revision: `6646f3026454e24525976ebd54841f85a50d3ba5`.

- `python3 Docs/tools/check_stage1_standard.py`: exit 0; all 1546 targets and
  assurance groups passed.
- `python3 scripts/stage1_target.py check`: exit 0; 1546 unique L0/rework
  targets passed.
- `python3 scripts/stage1_target.py show THM-M-0400`: exit 0; rank 13,
  planned, theorem incomplete.
- From `Formalizations/Lean`,
  `lake env lean ../../Stage1_Instances/THM-M-0400/Statement.lean`: exit 1;
  `unknown module prefix 'Mathlib'`. The canonical shared `.lake` tree lists
  the pinned package paths but lacks the compiled Mathlib objects. Per worker
  policy, no build, update, clone, fetch, or `.lake` mutation was attempted.
- `python3 Stage1_Instances/THM-M-0400/check_obligation_tree.py`: exit 0 after
  the recorded registry digest was frozen.
- `python3 -m json.tool Stage1_Instances/THM-M-0400/obligation-tree.json`: exit
  0.
- `git diff --check -- Stage1_Instances/THM-M-0400`: exit 0.

The pre-existing untracked `Formalizations/Lean/.lake` link is outside the
owned path and was not modified. The failed fresh Lean replay is a recorded
environment limitation, not theorem evidence and not a blocker to validating
the registry/graph phase itself.
