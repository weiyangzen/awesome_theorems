# Intake validation

Base revision: `9cf9d5b9dab219e460bb264ec1e565b071591d89`.

The preflight worktree contained only the repository-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only and was
not modified. This is nonrelease worker evidence.

Validation is limited to target-set consistency, dossier structure and scope invariants,
bibliographic metadata, a narrow pinned Lean API probe, a bounded local candidate search,
prohibited-construct hygiene, and whitespace. Because the repository source does not select a
unique proposition, no canonical target, expression hash, mutation result, source acceptance, or
proof is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1408` | exit 0; rank 907, planned, L0/rework_required, legacy artifacts unaccepted, theorem_complete false |
| `curl -L --fail --silent --show-error https://api.crossref.org/works/10.1016/0001-8708%2870%2990029-0` | exit 0; publisher deposit identifies Donald Ornstein, exact paper title, *Advances in Mathematics* 4(3), 1970, pages 337-352, and the DOI; bibliographic discovery only |
| `python3 -m json.tool Stage1_Instances/THM-M-1408/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1408/task-dag.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1408/intake-receipt.json` | exit 0; valid reconciled worker receipt JSON |
| `python3 Stage1_Instances/THM-M-1408/check_intake.py` | exit 0; IDs, L0/planned lifecycle, null target and hashes, `H1/M4/R3`, empty accepted states, six open downstream tasks, artifact inventory, and public boundaries agree |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1408/IntakeProbe.lean)` | exit 0; eight pinned product-measure, measure-preserving, measurable-equivalence, and scalar-entropy APIs elaborated under Lean 4.29.0 |
| bounded pinned-mathlib target-name search | exit 1 with no matches; no Ornstein, Bernoulli-shift, Kolmogorov-Sinai, or measure-entropy named target surface found |
| prohibited Lean proof-escape scan | exit 1 as expected for no matches; no `sorry`, `admit`, `sorryAx`, `axiom`, or `constant` occurs in the owned Lean probe |
| `git diff --check -- Stage1_Instances/THM-M-1408 .stage1-worker-selftest.json` | exit 0; no whitespace errors |

The first downstream gate remains exact source-statement selection and independent review. It must
resolve the alphabet, entropy domain and convention, shift orientation, isomorphism category, and
classification direction before Lean elaboration. Canonical statement mutations, exhaustive formal
anchor audit, discovery/obligation freezes, proof, composition, trust closure, hermetic replay,
independent validation, and master acceptance all remain open. These failures block theorem
completion but do not invalidate a truthful `planned` intake.
