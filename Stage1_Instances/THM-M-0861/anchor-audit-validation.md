# THM-M-0861 Anchor-Audit Validation

Item: `S56-M-0861-ANCHOR_AUDIT`

Base revision: `9c75282d42a7ef447d885d1d56997a79418bcd8a`

Base tree: `cc5285432a02107fadffb68c698690d1b98ac5f2`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Result

No exact Lean 4 proof candidate was located for the frozen finite bipartite multigraph target.
Pinned mathlib supplies the selected `Graph` representation, simple-graph bipartiteness, line
graphs, vertex coloring and chromatic number, and Hall matching theorems. Those are `M3` substrate,
not an edge-coloring proof: the simple-graph APIs lose parallel-edge multiplicity, and the Hall
theorems do not build or compose a complete matching decomposition.

The target-owned probe repeats the exact proposition, checks fourteen adjacent interfaces, and
asks Lean to reject the line-graph adjacency and perfect-matching theorems at the root type. Lean
reports both expected type mismatches. It reports the three inspected pinned proof-bearing
declarations sorry-free with exactly `propext`, `Classical.choice`, and `Quot.sound`. This supports
the provisional statement/anchor candidate projection `[H1, M3, R4]`; the authoritative accepted
vector remains `[H1, M4, R4]` until the statement and this node are master-accepted.

## External Inventory

The immutable Formal Conjectures snapshot defines `SimpleGraph.IsEdgeColouring` only as a partition
of simple-graph edges into disjoint classes. It does not require a color class to be a matching and
has no maximum-degree theorem. ATLAS has a file named `Konig.lean`, but it proves the different
matching-versus-vertex-cover theorem; a narrow check reports `sorryAx` through a concrete `sorry`
in its transitive `Berge.lean` dependency. Open mathlib PR 33032 is the same matching-cover name
collision at an immutable head and is also not the target. Moving PR leads for a basic SimpleGraph
edge-coloring API and Vizing's theorem were recorded as E5 research evidence only, not candidates.

The public search ledger records completed zero-result or classified-result queries separately
from access failures. Sourcegraph timed out once and hit one shard limit, GitHub code search was
rate-limited, and grep.app returned HTTP 429. The seven admitted immutable candidate groups are
classified; exhaustive discovery saturation is not claimed.

## Commands And Results

All local checks used the automation-provided canonical `.lake` symlink read-only. No `lake
update`, `lake build`, dependency clone/fetch, checkout, or `.lake` mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0861` | 0 | rank 1415; planned; legacy artifacts unaccepted; theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | revision `8a178386...ea95`, tree `bdc39a...5c2b`, clean worktree |
| bounded `rg`, `git ls-tree`, and history searches over repo-local and manifest-pinned Lean | expected no exact match | no proper multigraph edge-coloring/chromatic-index theorem; candidate APIs classified in the ledger |
| immutable complete-source scans of Formal Conjectures and ATLAS | 0 | mismatched edge-partition interface and matching-cover theorem classified; ATLAS transitive placeholder identified |
| bounded Sourcegraph, GitHub, and grep.app queries | mixed completed/access failures | response hashes, limits, timeouts, and no-saturation boundary recorded in `anchor-audit.json` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0861/AnchorAudit.lean` | 0 | fourteen interfaces, two expected type mismatches, three sorry-free/axiom reports, and exact target; stdout SHA-256 `015cf709...bec9d` |
| `python3 -B Stage1_Instances/THM-M-0861/check_anchor_audit.py` | 0 | authority, pins, hashes, candidates, classifications, receipt, packet, and Lean replay agree |
| `python3 -m json.tool` on anchor JSON and worker packet | 0 | all structured records parse |
| comment-aware prohibited-construct scan over `AnchorAudit.lean` | expected no match | no placeholder, custom axiom, unsafe declaration, or opaque declaration; `#print sorries` retained as an audit command |
| `git diff --check -- Stage1_Instances/THM-M-0861 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Status Boundary

This phase supplies provisional self-tested anchor evidence pending dependency-ordered master
acceptance. It locates no exact proof or integration candidate and does not freeze the obligation
tree, establish proof/composition, accept complete trust closure, close human-source or readable
debt, finish `AUDIT-Z`, or complete the theorem.
