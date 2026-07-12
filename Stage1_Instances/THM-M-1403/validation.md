# Intake validation

Base revision: `028e2535b68678b8296e63e2cacb05ed9775a2d8`.

Validation date: 2026-07-12 (Asia/Shanghai). This evidence covers manifest membership, dossier and
open-DAG invariants, JSON integrity, a narrow elaboration probe against pinned topological-entropy
APIs, prohibited-construct hygiene, and whitespace. It cannot establish a canonical source theorem,
an exact Lean target, or a proof result.

The preflight worktree contained the existing untracked shared link `Formalizations/Lean/.lake`.
It points to the canonical checkout's pinned artifacts and was used read-only. No `lake update`,
`lake build`, dependency clone, fetch, or other `.lake` mutation was run.

Environment fingerprint:

- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1403` | 0 | rank 902; planned; L0/rework_required; legacy artifacts unaccepted; theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version && lake --version && sha256sum lean-toolchain lake-manifest.json && git -C .lake/packages/mathlib rev-parse HEAD` | 0 | Lean, Lake, file hashes, and pinned mathlib revision agree with the fingerprint above |
| `python3 -m json.tool Stage1_Instances/THM-M-1403/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1403/task-dag.json` | 0 | valid JSON |
| scoped Python intake assertions | 0 | IDs/rank, planned lifecycle, null claim/target, `[H5,M3,R4]`, empty accepted state, six open dependency-ordered tasks, and false completion flags agree |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1403/IntakeProbe.lean` | 0 | six pinned entropy APIs elaborated; exact printed types include their universes, structures, binders, hypotheses, and conclusions |
| `rg -n -i 'Adler\|Konheim\|McAndrew\|topological entropy\|coverEntropy' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Dynamics/TopologicalEntropy --glob '*.lean'` | 0 | bounded candidate inventory found the Bowen-Dinaburg modules/declarations and no author-name occurrence; not a comprehensive anchor audit |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-1403 --glob '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom in the target's Lean source |
| per-file `git diff --no-index --check -- /dev/null <new-file>` loop, treating exit 1 as the normal added-content difference and rejecting exit greater than 1 | 0 | all eight new intake files passed the whitespace check |

The first failed downstream theorem gate is the exact-statement gate: the current catalog wording
is not a proposition, and the historical AKM locator has not been mapped to one reviewed passage.
Source selection or an approved target correction, canonical elaboration/fingerprint, alternate
encoding witnesses, mutation tests, formal-anchor audit, obligation freeze, proof, hermetic replay,
and independent release validation remain open. Those failures prevent audit and theorem completion
but do not invalidate this truthful, self-tested `planned` intake.
