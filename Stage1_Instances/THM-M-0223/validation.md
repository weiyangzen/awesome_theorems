# Intake validation

Base revision: `62fad55ced807fdc06921c45d6fcd1f9ad86a1c2`; base tree:
`9d7c8fe49a4c859d90f3069dc47973ffc5ced768`.

This validation covers target membership, planned dossier and open-DAG invariants, repository
source provenance, scope and neighbor boundaries, pinned environment identity, a narrow Lean API
probe, bounded source discovery, JSON and Python integrity, prohibited-construct hygiene, and
whitespace. It does not validate a canonical theorem statement or proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

The packet-aware validator mode binds the handoff to this exact worker base. The packet-free mode
is a narrower public replay of the planned dossier and provisional receipt. Neither mode promotes
the authoritative execution cursor or creates accepted evidence; the integration lane must rerun
the checks and issue a master-accepted receipt.

## Commands and results

Commands ran on 2026-07-13 in Asia/Shanghai. Commands without an explicit `cwd` ran at the
repository root.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0223` | 0 | rank 1236; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 1612,1617 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| repository source and Stage0 crosswalk inspection | 0 | only title, attribution/year, broad gloss, importance, and untrusted status exist; exact definitions, assumptions, conclusion, proof, axioms, machine state, and artifacts are open |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 at `98dc76e3...`; Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package status clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0223/IntakeProbe.lean)` | 0 | eight adjacent circle-integral, Cauchy, meromorphicity, order, and trailing-coefficient APIs elaborated; no target theorem stated |
| bounded `rg` search for residue-theorem and contour/integral-residue names in repo-local Lean and pinned mathlib | 0 | found only unrelated Stage1 prose and specialized Hurwitz-zeta coefficient lemmas; no source-identical general residue-theorem declaration; intake discovery only, not a global absence claim |
| `python3 -m json.tool` on the owned JSON files and `.stage1-worker-selftest.json` | 0 | instance, open task DAG, provisional intake receipt, and worker packet are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0223-pycache python3 -m py_compile Stage1_Instances/THM-M-0223/check_intake.py` | 0 | scoped validator compiled without writing generated files into the owned path |
| `python3 -B Stage1_Instances/THM-M-0223/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, base and current hashes, planned H1/M4/R4 boundary, null target, exact inventory, receipt/packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0223/check_intake.py` | 0 | packet-free planned-dossier replay passed |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)\b\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-0223` | 1 (expected no match) | no prohibited proof escape or declaration in the API-only probe |
| `git diff --check -- Stage1_Instances/THM-M-0223 .stage1-worker-selftest.json` plus per-file no-index checks | 0 | no whitespace diagnostics in any new artifact |

## Known open gates

An approved immutable source proposition, complete contour/domain/meromorphicity/pole/residue/
winding/normalization and proof-boundary crosswalk, correction and errata audit, and independent
source review remain open. So do the canonical Lean expression and environment fingerprint,
checked transports, statement mutations, exhaustive formal anchor audit, discovery protocol,
obligation registry, typed graphs, proof and composition, trust and provenance closure, readable
reconstruction, hermetic replay, deterministic bundle, independent verification, master acceptance,
audit completion, and theorem completion. These failures do not invalidate a truthful self-tested
`planned` intake.
