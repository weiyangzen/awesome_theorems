# THM-M-0786 proof-phase blocker

Item: `S56-M-0786-PROOF`  
Base revision: `8f8873f36acbc62e9b41b932a8bb65bf355c8ccf`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Verdict

The proof phase is blocked and is not self-tested. No proof receipt or worker
self-test manifest is emitted.

The frozen proof route requires the external declaration
`GaleStewartGame.borel_determinacy` from
`sven-manthe/A-formalization-of-Borel-determinacy-in-Lean` at immutable commit
`42bc874b2357ca7e7573b31854a0d09761e11e41`, followed by a checked adapter from
that project's full pruned game to the canonical total-history strategy
encoding. That project is not in the repository's pinned Lake closure. Its
module therefore cannot be imported by the existing toolchain, so neither the
external theorem nor the adapter can be kernel-checked here. Fetching or
installing the absent dependency would violate this worker's pinned-validation
rules.

The existing `ObligationTree.lean` proves only the conditional composition
`PayoffSolver -> BorelDeterminacyTarget`; `PayoffSolver` is definitionally the
entire theorem. It is not a terminal proof body and earns no root proof credit.
The first failed gate is `M0786-L-BORELDET` (external kernel integration). The
dependent `M0786-C-FULLGAME`, `M0786-N-BOREL`, `M0786-N-STRATEGY`,
`M0786-B-WINNER`, and `M0786-T-ADAPTER` obligations consequently remain open.
The root remains `M3`; audit completion and theorem completion are false.

## Commands and exact results

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0
  check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy
  slots, 1546 uniform-L0 Lean 4 targets, execution skill present)

python3 scripts/stage1_target.py check
  exit 0
  stage1_target: ok (1546 unique targets, ranks 1..1546, all
  L0/rework_required)

python3 scripts/stage1_target.py show THM-M-0786
  exit 0
  rank 791; lifecycle planned; L0/rework_required; theorem_complete false

(cd Formalizations/Lean &&
  lake env lean ../../Stage1_Instances/THM-M-0786/Statement.lean)
  exit 0
  canonical BorelDeterminacyTarget elaborated and its explicit type printed

(cd Formalizations/Lean &&
  python3 ../../Stage1_Instances/THM-M-0786/check_obligation_tree.py)
  exit 0
  PASS THM-M-0786 obligation tree: 14 obligations, 44 typed edges
  registry denominator sha256:
  388471796332e9e00b2f291ca80ee0b57ecc8ab3880868fd329ea2b2270d71c3
  root closure: open (M3); external kernel integration and canonical adapter
  remain open

(cd Formalizations/Lean &&
  lake env lean /tmp/<immutable-source>/BorelDet/Proof/borel_determinacy.lean)
  exit 1
  error: unknown module prefix 'BorelDet'; no BorelDet directory or olean is in
  the pinned LEAN_PATH
```

The last check used an ephemeral read-only inspection copy of the exact commit,
not a Lake dependency installation. No `lake update`, `lake build`, dependency
clone/fetch, or `.lake` mutation was performed.

## Reopen condition

The integration lane must first provide the exact external revision and its
locked dependency closure as an accepted pinned or vendored artifact compatible
with a permitted Lean environment. The proof phase can then kernel-check the
external declaration, audit its transitive trust closure, implement the frozen
full-game and strategy transports, and elaborate a premise-free theorem of the
exact canonical target.
