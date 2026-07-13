# THM-M-0912 obligation-tree validation

Item: `S56-M-0912-OBLIGATION_TREE`

Base revision: `b243ebc0f9058ba5afafef8240b92c2dfb2edc6e`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Frozen result

Registry version 1 freezes 16 canonical obligations and 32 directed typed edges across separate
proof, refinement, provenance, evidence, trust, documentation, and workflow graphs.  The frozen
denominator SHA-256 is `c66f1840e6d1bcc7b0a64f7ecdc24ee2f13adc10098ca8467cd238c649f7432b`.

The pinned body `Nat.choose_eq_choose_pred_add` is expanded into its positive-column reindexing and
`Nat.choose_succ_right` children.  The root composition separately consumes positive-row
normalization, the predecessor recurrence, and summand-order transport.  `ObligationTree.lean`
checks only the conditional child-to-root interface; the validator compares the fully explicit
architecture root with the statement-phase expression and its frozen digest.

No obligation receives accepted closure.  The exact pinned recurrence remains candidate-only
`M0-W`, while the authoritative root remains `[H1, M3, R4]`, `audit_complete=false`, and
`theorem_complete=false`.

## Commands and results

Commands ran in this worker clone.  The existing canonical pinned `.lake` closure was reused
read-only.  No update, build, clone, fetch, or dependency mutation command ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard, 15 assurance groups, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0912` | 0 | rank 1454; planned; L0/rework-required; theorem incomplete |
| `python3 -B Stage1_Instances/THM-M-0912/build_obligation_artifacts.py` | 0 | wrote 16 obligations, 32 typed edges, and denominator `c66f1840...7432b` |
| `python3 -B Stage1_Instances/THM-M-0912/check_obligation_tree.py` | 0 | deterministic artifacts, frozen hashes, schemas, exclusions, reciprocal proof edges, reachability, recipes, source pins, Lean expression identity, and open closure passed |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0912/ObligationTree.lean)` | 0 | exact conditional composition elaborated; all four checked declarations axiom-free and sorry-free |
| `python3 -m json.tool` on the four new structured JSON artifacts and worker packet | 0 | every structured artifact parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0912-obligation-pycache python3 -m py_compile ...` | 0 | generator and validator compiled outside the repository tree |
| scoped comment-aware prohibited-construct scan over `ObligationTree.lean` | 1 (expected no match) | no proof gap, axiom declaration, unsafe or opaque body, native oracle, external implementation, or placeholder |
| `git diff --check -- Stage1_Instances/THM-M-0912 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Status boundary

This is provisional worker evidence pending dependency-ordered master acceptance.  The pinned
candidate is not installed as the canonical proof.  Primary-source `H0`, independently reviewed
`R0`, transitive provenance and trust closure, hermetic replay, deterministic release evidence,
independent verification, `AUDIT-Z`, and theorem completion remain open.
