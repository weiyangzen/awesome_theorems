# THM-M-0822 obligation-tree validation

Item: `S56-M-0822-OBLIGATION_TREE`

Base revision: `f023dbc3411d83201065d1a1156d7406b81135d4`

Base tree: `3b3a73ec19293a2a9b8d9c7e67f0d25da2a511b4`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Frozen result

Registry version 1 freezes 27 unique semantic obligations before proof-phase adoption. Its
canonical ten-field projection has SHA-256
`40ff944c9434231f2656a60ff306e27b69ef6fe302df8dc1bd56f89d314a8f15`. The bundle contains 49
directed edges across separate proof, refinement, provenance, evidence, trust, documentation, and
workflow graphs. It includes 27 substantive ledger steps, six exact conditional composition
certificates, no unverified decompositions, and an explicit open proof and release cut.

The proof spine separates exact root composition, the target-owned star-attainment package, and the
pinned universal-bound terminal. The visible internals of `Finset.erdos_ko_rado` are informational
expository nodes sharing its terminal proof-body identity; they are not independent machine-credit
obligations. The accepted obligation set is empty and the root remains `[H1, M3, R4]`.

Validation used only the existing manifest-pinned Lake artifacts. No `lake update`, `lake build`,
dependency clone/fetch, or `.lake` mutation was performed. The statement `.olean` was created in a
temporary directory and removed automatically.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0822` | 0 | rank 1380; planned; L0/rework-required; theorem incomplete |
| `python3 -B Stage1_Instances/THM-M-0822/build_obligation_artifacts.py` | 0 | wrote 27 obligations and 49 typed edges; denominator `40ff944c...8f15`; repeated generation was byte-identical |
| `python3 -B Stage1_Instances/THM-M-0822/check_obligation_tree.py --worker-packet .stage1-worker-selftest.json` | 0 | registry, denominator, ledgers, seven graphs, proof reciprocity/reachability, certificates, source pins, disposable Lean elaboration, receipt, packet, and open closure passed |
| checker-managed pinned Lean replay of `Statement.lean` then `ObligationTree.lean` | 0 | eight declarations elaborated; six abstract-child composition certificates distinguished; exact root printed; all eight axiom reports were `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `cfae1834...6553` |
| `python3 -m json.tool` over the owned obligation JSON files and worker packet | 0 | every structured artifact parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0822-obligation-pycache python3 -m py_compile Stage1_Instances/THM-M-0822/{build_obligation_artifacts.py,check_obligation_tree.py}` | 0 | both Python files compiled outside the repository tree |
| comment-aware prohibited-construct scan of `ObligationTree.lean` | 1 | expected no match; no placeholder, bodyless declaration, unsafe/opaque/oracle, external implementation, or native shortcut |
| `git diff --check -- Stage1_Instances/THM-M-0822 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Known failures

- The statement, anchor-audit, and this obligation-tree evidence remain provisional until
  dependency-ordered master acceptance.
- The local star and pinned upper-bound terminal are checked candidates but are not installed by
  this phase and receive no accepted M0 credit.
- The imported terminal's internal source-body nodes are informational expository architecture;
  making them separate machine premises would require exact signatures, checked child-consuming
  certificates, and a new registry version.
- Primary-source H0, independently reviewed R0, content-addressed transitive provenance and E1 trust,
  hermetic replay, independent verification, validation, and release remain open.
- The automation-provided `.lake` symlink makes this warm, nonrelease worker evidence.

This completes only the assigned obligation-tree implementation and self-test. It changes no
accepted scheduler state and claims neither `AUDIT-Z` nor theorem completion.
