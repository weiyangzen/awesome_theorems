# Statement validation

Item: `S56-M-0819-STATEMENT`

Base revision: `fcabbf1e0ad9507eebe91663bccabfa87d22813e`; base tree:
`873e589c594454b7f263c7ed2342089a4d15e842`.

## Exact scope

`Statement.lean` selects the arbitrary-poset Theorem 1.1 printed on original page 161 of
Dilworth's 1950 paper. For every partial order and natural number `k`, every exact-`k + 1` subset is
dependent and some exact-`k` subset is an antichain; the conclusion is a uniquely covering
`Fin k`-indexed family of chains. This unique-membership family is the paper's disjoint set sum.

The printed passage does not explicitly state whether `k` includes zero, and the visible proof
begins at `k = 1`. The canonical total-`Nat` target is therefore literal for positive `k` and adds a
separately checked conservative `k = 0` extension; source approval of that range convention remains
open rather than being silently attributed to the paper.

This phase does not select the modern finite-poset equality from the incompatible external Lean
candidate. No equivalence between that equality and the primary theorem is credited. Complete
source-proof review, corrections, errata, and independent source approval remain open, so `H1`
does not change.

`HasExactly k s := Nonempty (s equiv Fin k)` preserves exact finite cardinality for subsets of an
otherwise arbitrary carrier. It does not use a `Nat` cardinality convention that maps infinite sets
to zero. The `k = 0` case remains present: a checked lemma shows the no-singleton-antichain premise
forces an empty carrier, and another checks its zero-chain decomposition. A singleton one-chain
boundary also kernel-checks.

## Import and environment

The only direct import is `Mathlib.Order.Antichain` from pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. A canonical-target-only fixture elaborates with this
import and fails after deleting it. This establishes that the declared import is necessary for the
source layout; it is not an exhaustive global claim over every possible refactoring of mathlib.

The automation-provided `Formalizations/Lean/.lake` symlink was used read-only. No `lake update`,
`lake build`, dependency clone or fetch, or other `.lake` mutation was performed.

## Gate results

- The canonical explicit expression has SHA-256
  `bdf0aa8f8adac4be9bf2080951be62eac168872b8c589a804ac8587c1878bb19` and no unresolved
  metavariable.
- The fully explicit `HasExactly`, `IsDependent`, and `IsDisjointChainDecomposition` bodies plus
  the root form semantic bundle SHA-256
  `df437e79e306cbbdca0f9344a6a953a7f27886a197db7c614b995c846f8a2195`, so changing a local
  support definition invalidates statement identity even if the root keeps the same constant names.
- The direct expansion is kernel-checked by
  `Stage1Instances.THM_M_0819.dilworthPrimaryTarget_iff_expanded`.
- Lean rejects the removed-witness, fixed-`Nat`-domain, changed-width-scope, and positive-width
  mutations as the canonical exact type. Their explicit expression hashes are distinct. These are
  statement-identity tests, not claims that every fixture is false or logically inequivalent; the
  fixed-domain target is a specialization, and positive width omits the checked zero-width extension.
- The canonical target is a `Prop` definition without a proof body. The checked direct expansion
  and zero-family boundary add no axioms; the other two boundary lemmas report only `propext`.
- Comment-stripped source scanning finds no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`,
  `opaque`, or `unsafe` declaration.

## Commands and results

All repository commands ran from the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution skill pass |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0819` | 0 | rank 1377, planned, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` | 0 | preflight and final dirty-tree boundaries recorded; only owned artifacts, root packet, and the pre-existing `.lake` symlink are present |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0819/Statement.lean` | 0 | target, expansion, boundaries, four expected mutation rejections, axiom reports, and explicit expression elaborate |
| `cd Formalizations/Lean && python3 -B ../../Stage1_Instances/THM-M-0819/check_statement.py --worker-packet ../../.stage1-worker-selftest.json` | 0 | expression, mutations, sole-import deletion, source/receipt/packet hashes, pin, ownership, and governance agree |
| `python3 -m json.tool` on statement metadata, receipt, and worker packet | 0 | all structured artifacts parse |
| Python syntax and scoped forbidden-construct checks | 0 | validator parses and no forbidden construct occurs in executable Lean source |
| pinned mathlib revision/tree/status checks | 0 | revision and tree match the lock; package worktree is clean |
| `python3 -B Stage1_Instances/THM-M-0819/check_intake.py` | 1 | historical intake-only checker expects authoritative intake state `[ ]`; it is superseded by current `[_]` intake state and is not statement evidence |
| whitespace checks over every changed file | 0 | no trailing whitespace, CR, NUL, or missing final newline |
| `git diff --check -- Stage1_Instances/THM-M-0819 .stage1-worker-selftest.json`; per-file `git diff --no-index --check /dev/null <file>` for all six new files | 0 aggregate | no whitespace diagnostics; no-index exit 1 denotes only the expected new-file difference |

## Boundary

The proposed vector moves from `[H1, M5, R3]` to `[H1, M3, R3]`: an exact local statement and
interface now elaborate, while the blocked external finite-equality candidate remains separately
invalid under this pin and supplies no proof credit. Intake and statement receipts are both
unfinished pending dependency-ordered master acceptance. Anchor audit, obligation freeze, proof,
composition, readable reconstruction, full trust closure, hermetic replay, deterministic bundle,
independent release verification, audit completion, and theorem completion remain open. The
integration lane must reconcile the still-null planned `instance.json` target before accepting this
statement proposal; this worker does not edit accepted scope authority.
