# THM-M-0484 obligation-tree validation

Item: `S56-M-0484-OBLIGATION_TREE`

Base revision: `fcabbf1e0ad9507eebe91663bccabfa87d22813e`

Base tree: `873e589c594454b7f263c7ed2342089a4d15e842`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Frozen result

Registry version 1 freezes 36 unique obligations. The canonical ten-field projection has SHA-256
`af0c1b5d7bfd4da0a7f1b982646906d20217976af4c5805295d37e43d0b39edf`. The bundle stores 137
typed edges across separate proof, refinement, provenance, evidence, trust, documentation, and
workflow graphs. Eighteen proof requirements have reciprocal composition edges backed by ten
named conditional Lean certificates. Seventeen deeper source-body relations are deliberately marked
unverified as child-to-parent composition and must receive future certificates before parent
machine acceptance.

The validation uses only the automation-provided manifest-pinned Lake artifacts. No `lake update`,
`lake build`, dependency clone/fetch, or other `.lake` mutation was run. The `.lake` symlink was
present before this task, so this is warm nonrelease evidence.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets with ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0484` | 0 | rank 1365; planned; L0/rework-required; theorem incomplete |
| `git status --short --untracked-files=all` before editing | 0 | only the automation-provided untracked `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | mathlib revision `8a178386...ea95`, tree `bdc39a...5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty; pinned source tree clean |
| `python3 Stage1_Instances/THM-M-0484/build_obligation_artifacts.py` twice | 0 | each run wrote 36 obligations and 137 typed edges; all three generated files were byte-identical on replay |
| `python3 -B Stage1_Instances/THM-M-0484/check_obligation_tree.py` | 0 | deterministic registry, denominator, node schemas, seven graph indexes/types, reciprocity, reachability, source expansions, recipes, receipt, hashes, and open-state boundary passed |
| `python3 -B Stage1_Instances/THM-M-0484/check_obligation_tree.py --run-lean` | 0 | statement compiled to a temporary directory; ten conditional certificates elaborated with `--trust=0`; all were sorry-free; no `sorryAx`; output SHA-256 `a04da11a...1bb7` |
| `lake env lean --trust=0 ../../Stage1_Instances/THM-M-0484/AnchorAudit.lean` from `Formalizations/Lean` | 0 | predecessor exact terminal pair remained sorry-free; axiom set and 35,389-declaration/1,243-module trust walk remained unchanged |
| `lake env lean ../../Stage1_Instances/THM-M-0484/Statement.lean` from `Formalizations/Lean` | 0 | exact target, two transports, mutations, and p=2 boundary re-elaborated |
| `python3 ../../Stage1_Instances/THM-M-0484/check_statement.py` from `Formalizations/Lean` | 0 | expression/source fingerprints, mutations, minimal import, and pinned source passed |
| current-hash predecessor invariant check in the obligation checker | 0 | integrated statement SHA, anchor audit SHA, pinned source blob/body IDs/types, dependency pin, and open accepted state matched; historical snapshot-strict worker-packet equality was not misreported as a current successor check |
| `python3 -m json.tool` on all owned JSON and `.stage1-worker-selftest.json` | 0 | every structured artifact parsed without duplicate keys |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0484-obligation-pycache python3 -m py_compile ...` | 0 | builder/checkers compiled outside the repository tree |
| scoped prohibited-construct scan over `ObligationTree.lean` | 1, expected no match | no proof gap, custom axiom/constant, opaque/unsafe declaration, external implementation, native oracle, or placeholder |
| `git diff --check -- Stage1_Instances/THM-M-0484 .stage1-worker-selftest.json` plus no-index new-file checks | 0 | no whitespace diagnostics |

The statement and anchor worker validators retain historical changed-path and base-revision packet
semantics. Rather than weakening those old receipts or falsely rerunning their obsolete packet
equality against successor files, this node independently checks their integrated content hashes,
canonical expression, terminal body identities, source markers, pins, and accepted-state boundary,
then reruns the narrow Lean statement and anchor probes themselves.

## Status boundary

This phase freezes architecture and checks conditional composition. It does not supply either
terminal premise to the root. Both terminals remain candidate-only `M1/E2`; the predecessor's
`M0-W/E2` label is not inherited because rev-5.6 section 4 requires `E1` for `M0-W`. Accepted proof
state is empty, the root remains `[H1, M3, R4]`, and primary-source `H0`, readable `R0`, complete
provenance/TCB, proof installation, validation, independent verification, release, `AUDIT-Z`, and
theorem completion remain open. The packet is provisional pending dependency-ordered master
acceptance.
