# Intake validation

Base revision: `5bc32428da3d17f138ceca67f30fbc2d149da1ba`; base tree:
`7d2433c3e014a9cc8c4d061bcc1b7d5c637ce33f`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, statement and neighbor boundaries, JSON and scoped invariants, a narrow pinned Lean API
probe, bounded local discovery, prohibited-construct hygiene, and whitespace. It does not validate
a canonical theorem statement, either implication of the metrization theorem, or any proof body.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` link to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The intake artifacts and worker packet make the final tree dirty and
nonrelease.

The packet-aware validator mode requires the exact worker base and is worker-only evidence. The
packet-free structured recipe authenticates the recorded base revision by Git ancestry and immutable
base blobs and permits the integration lane to replay the dossier after moving the authoritative
cursor from `[ ]` to `[_]`. That replay still cannot master-accept this provisional receipt.

## Commands and results

All commands ran on 2026-07-13 in Asia/Shanghai. Commands without an explicit `cwd` ran at the
repository root.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0624` | 0 | rank 1318; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 4629,4634 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '4629,4634p' Docs/researches/math_theorems.md \| sha256sum` | 0 | excerpt SHA-256 `cec65ce0...4c765` |
| nLab revision 4 and definition revision 5 inspection | 0 | stable secondary pages expose the familiar regular/Hausdorff and countably locally finite basis wording; neither is primary proof evidence |
| zbMATH records 3061898 and 3064632 plus Crossref DOI metadata | 0 | Nagata's 1950 pages 93-100 and Smirnov's 1951 Russian pages 197-200 original records and Nagata's 1957 DOI lead were authenticated as bibliography; none of the article texts or exact theorems was inspected |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean 4.29.0 at `98dc76e3...`; Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and status | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0624/IntakeProbe.lean)` | 0 | seven adjacent APIs elaborated; stdout SHA-256 `0c5f934a...d61e1`; no target theorem or proof body declared |
| bounded `rg` search in the repository and pinned mathlib | 0 | no Nagata-Smirnov declaration, packaged sigma-locally-finite-basis predicate, or terminal theorem combining metrizability, topological basis, and locally finite layers was found; discovery only |
| `python3 -m json.tool` on owned and root structured files | 0 | all JSON parsed |
| `python3 -c "import ast, pathlib; ast.parse(pathlib.Path('Stage1_Instances/THM-M-0624/check_intake.py').read_text())"` | 0 | scoped validator parsed without bytecode output |
| `python3 -B Stage1_Instances/THM-M-0624/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, pins, planned null-target H1/M4/R4 boundary, artifact hashes, receipt/packet agreement, and six open tasks passed |
| `python3 -B Stage1_Instances/THM-M-0624/check_intake.py` | 0 | packet-free replay passed |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)\b\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-0624` | 1 (expected no match) | no prohibited proof escape or declaration in the API-only probe |
| `git diff --check -- Stage1_Instances/THM-M-0624 .stage1-worker-selftest.json` plus per-file untracked checks | 0 | no whitespace diagnostics in any new artifact |

## Known open gates

An approved immutable primary or authoritative source proposition, exact definitions and premises,
both equivalence directions, proof boundary, translation, correction and errata mapping, and
independent source review remain open. So do the canonical Lean expression and environment
fingerprint, checked transports, statement mutations, exhaustive formal candidate and terminal-body
audit, discovery and obligation freezes, typed graphs, proof and composition, trust and provenance
closure, readable reconstruction, hermetic replay, deterministic bundle, independent verification,
master acceptance, audit completion, and theorem completion. These failures do not invalidate a
truthful, self-tested `planned` intake.
