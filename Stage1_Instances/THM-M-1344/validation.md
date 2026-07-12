# Intake validation

Base revision: `8bbb7ffdbb5e6e8e3e1ffaba9955137f6b68c76c`; base tree:
`ade61913e5912b1160e25afe096df7f5b3b0cfed`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, a stable secondary source-family inspection, JSON and scoped invariants, a narrow pinned
Lean substrate probe, bounded name search, prohibited-construct hygiene, and whitespace. It does
not validate a canonical theorem statement or proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

The stable arXiv v1 PDF for Al Jamal, Chow, and Morris, *Linearized stability analysis of nonlinear
partial differential equations*, was retrieved outside the repository and inspected. Theorem 3.1
separates the negative-spectrum exponential-stability branch from the positive-spectrum
instability branch, while the paper distinguishes finite-dimensional ODEs from Banach-space
semigroup variants. Its SHA-256 and locator are recorded in structured artifacts. The catalog does
not cite this secondary source. No primary historical proof chain, approved translation, complete
errata audit, or independent H0 review is claimed.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless `cwd` is
shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1344` | 0 | rank 955; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 9803,9808 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '9803,9808p' Docs/researches/math_theorems.md \| sha256sum` | 0 | excerpt SHA-256 `f92c3657...0469` |
| `curl -L --fail --max-time 60 -sS https://arxiv.org/pdf/1509.05792v1 -o /tmp/lyapunov_indirect_1509.05792v1.pdf` | 0 | downloaded the stable six-page arXiv v1 PDF outside the repository; SHA-256 `8d4a57eb...e2c6` |
| `pdftotext -layout /tmp/lyapunov_indirect_1509.05792v1.pdf /tmp/lyapunov_indirect_1509.05792v1.txt` and bounded `rg` inspection | 0 | located Theorem 3.1 and its distinct finite-dimensional stability and instability branches plus the finite/Banach boundary |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package status clean |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...85b1d2` and `321626c8...d81` as recorded in structured artifacts |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1344/IntakeProbe.lean)` | 0 | nine pinned ODE, derivative, and spectral API checks elaborated; no target theorem stated |
| `rg -n -i --glob '*.lean' 'lyapunov\|liapunov\|exponential stability\|exponentially stable\|asymptotic.*stabl\|linearization.*stabl\|stability.*lineariz\|unstable.*eigen\|eigenvalue.*real part' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 0 | only unrelated Lyapunov CLT/exponent material occurred; no target-specific indirect-method or nonlinear ODE stability theorem found; intake discovery only, not a global absence claim |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured files are valid JSON |
| `python3 -c "import ast, pathlib; ast.parse(pathlib.Path('Stage1_Instances/THM-M-1344/check_intake.py').read_text())"` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1344/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target and execution-DAG identity, current source hashes, planned H1/M4/R4 boundary, null target, exact inventory, receipt/packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1344/check_intake.py` | 0 | public replay mode passes without the scheduler-only root packet |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)\b\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-1344` | 1 (expected no match) | no prohibited proof escape or declaration in the API-only probe |
| `git diff --check -- Stage1_Instances/THM-M-1344 .stage1-worker-selftest.json` plus per-file untracked checks | 0 | no whitespace diagnostics in any new artifact |

## Status boundary

This is provisional worker self-test evidence for `S56-M-1344-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Exact source selection and independent review,
canonical Lean elaboration and statement mutations, complete anchor audit and discovery freeze,
obligation registry, typed graphs, proof, composition, trust closure, readable reconstruction,
hermetic replay, deterministic release bundle, and independent verification remain open. These
failures prevent statement, audit-completion, and theorem-completion claims, but they do not
invalidate the planned intake.
