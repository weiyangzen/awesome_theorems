# THM-M-0041 obligation-tree validation

Item: `S56-M-0041-OBLIGATION_TREE`

Base revision: `c76fe0f1a7514b41f191d16840eff25e64ee9d17`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Frozen result

Registry version 1 freezes 17 obligations and 27 directed typed edges across separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs. The denominator
SHA-256 is `c854b50bfd112e0e20a94f25fc6db6f4fda74e248e61b647ffd93d93977c33dc`.

The exact pinned `Matrix.aeval_self_charpoly` body is expanded into its adjugate construction,
matrix-polynomial equivalence, noncommutative right-factor evaluation, and scalar-evaluation
transport. Checked local declarations consume those four engines and the final characteristic-
polynomial transport, yielding the actual frozen target conditionally. The LinearMap theorem,
wrappers, support theorem, and downstream consumer are deduplicated to the same terminal body.

No obligation is accepted closed. The root remains `H1/M3/R3`, `audit_complete=false`, and
`theorem_complete=false`.

## Commands and results

Commands ran in this worker clone. The canonical pre-existing `.lake` closure was reused read-only;
no update, build, clone, fetch, or other dependency mutation command ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard, 15 assurance groups, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets with ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0041` | 0 | rank 1081; planned; L0/rework-required; theorem incomplete |
| `python3 -B Stage1_Instances/THM-M-0041/build_obligation_artifacts.py` | 0 | generated 17 obligations, 27 typed edges, and denominator `c854b50b...c33dc` |
| compile `Statement.lean` to a temporary directory with pinned `lake env which lean` / `LEAN_PATH`, then elaborate `ObligationTree.lean` | 0 | exact root, definitional transport, imported-body conditional composition, and exact root composition elaborated; only `propext`, `Classical.choice`, and `Quot.sound`; stdout SHA-256 `0856a9b...b56a7` |
| `python3 -B Stage1_Instances/THM-M-0041/check_obligation_tree.py` | 0 | target metadata, immutable pins, deterministic regeneration, registry/schema/denominators, typed graphs, reciprocity, reachability, recipe, Lean composition, receipt, root packet, hygiene, and open closure passed |
| `python3 -m json.tool` on the four obligation JSON artifacts and root packet | 0 | all structured artifacts parse as JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0041-obligation-pycache python3 -m py_compile ...` | 0 | generator and validator compile outside the repository tree |
| scoped prohibited-construct scan over `ObligationTree.lean` | 1 (expected no match) | no proof gap, axiom declaration, unsafe/opaque body, oracle, external implementation, TODO, FIXME, or placeholder |
| `git diff --check -- Stage1_Instances/THM-M-0041 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Status boundary

This is provisional worker evidence pending dependency-ordered master acceptance. The pinned anchor
has no accepted E1 receipt and is not installed as accepted M0-W. Pinpoint H0, independently
reviewed R0, full transitive provenance/trust, hermetic replay, independent verification,
deterministic release evidence, `AUDIT-Z`, and theorem completion remain open.
