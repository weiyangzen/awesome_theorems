# Intake validation

Base revision: `508f92b22d15ce42276877b26d34b9da3cac695c` (tree
`765daac67cdaffd2b797474b4c1a3d12f4f99933`). Validation ran on 2026-07-12 in
the isolated worker clone.

Validation is limited to target-set consistency, dossier structure and scope invariants, primary
candidate identification, pinned environment identity, a narrow Lean API probe, a bounded local
target search, proof-escape hygiene, and whitespace. The repository gloss and as-yet unreviewed
source crosswalk do not select an exact proposition, so no canonical target, expression hash,
statement mutation, source acceptance, or proof is claimed.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1421` | 0 | rank 919, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| Crossref DOI metadata query for `10.1070/RM1977v032n04ABEH001639` | 0 | author, title, journal 32(4), 1977, pages 55-114, and DOI agree; bibliographic discovery only |
| Official Math-Net English PDF inspection | 0 | Section 5, Theorem 5.1, printed page 81 and equation (5.0) located; observed 2,975,974-byte PDF SHA-256 `ea326f02...f0f35b`; source crosswalk remains unaccepted |
| `python3 -m json.tool Stage1_Instances/THM-M-1421/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1421/task-dag.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1421/intake-receipt.json` | 0 | valid JSON after receipt finalization |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | valid JSON after worker-manifest finalization |
| `python3 -B Stage1_Instances/THM-M-1421/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned lifecycle, H1/M4/R3 boundary, null target, exact artifact inventory, provisional packet, and six open tasks agree |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1421/IntakeProbe.lean)` | 0 | eight adjacent pinned measure-preserving, topological-entropy, manifold-derivative, integration, and finite-sum APIs elaborated; no target theorem |
| bounded pinned-mathlib target-name search using word boundaries | 1 | expected no-match exit; no Pesin, Lyapunov, Oseledets, metric-entropy, or measure-theoretic-entropy target name found; intake discovery only |
| prohibited Lean proof-escape scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-1421 .stage1-worker-selftest.json` plus per-file no-index checks | 0 | no whitespace errors in tracked or untracked owned artifacts |

Known downstream failures remain deliberately open: complete and independently reviewed source
definitions, assumptions, sign transport, proof boundary, and errata; exact binders, hypotheses,
conclusion, and degenerate cases; canonical Lean elaboration, expression/environment fingerprints,
checked transports, and mutations; immutable formal anchor audit; discovery and obligation freezes;
proof and composition; hermetic replay; deterministic evidence bundling; independent release
verification; and master acceptance. These prevent theorem completion but do not invalidate a
truthful, self-tested `planned` intake.
