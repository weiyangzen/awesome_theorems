# THM-M-1489 intake validation

## Scope

This record validates only the `planned` dossier, scope map, source-statement crosswalk, open task
DAG, source-family discovery boundary, and discovery-only pinned Lean API probe. It does not
validate an exact mathematical statement, a Transformer or attention specification, an
architecture or empirical claim, a proof, an accepted receipt, audit completion, or theorem
completion.

The worker tree was nonrelease-dirty throughout: the automation-provided canonical `.lake` symlink
was already untracked, and this intake's owned artifacts plus the root self-test packet were new.
The shared pinned `.lake` target was used read-only. No `lake update`, `lake build`, dependency
clone/fetch, package mutation, authority-file change, generated-checklist change, execution-DAG
state change, theorem declaration, proof, or other target modification was performed.

## Environment and source observation

- Repository base: `04d551db74b7e1d7d9d261bba4727b3daf8a70d5`
- Base tree: `ee8a3d7a6c48598ca61028d71e21e0802ed968e1`
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- Lake: `5.0.0-src+98dc76e`
- mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- mathlib tree: `bdc39a3123201dae413a9d9be56ec242c19e5c2b`
- Platform: Linux `7.0.0-27-generic`, `x86_64`
- Timezone/date: Asia/Shanghai, 2026-07-13

The official proceedings PDF for *Attention Is All You Need* was inspected with
`curl -L --fail --silent --show-error --max-time 60` from
`https://papers.nips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf`.
It had 11 pages, 569417 bytes, and observed SHA-256
`d87d482d5ae7960e2e43d7dd6d21377e60e73e8fce1bf2a01aff7aca8a08c537`. No external file was
vendored. This mutable remote observation is nonrelease discovery evidence, not an admitted source
bundle or `H0` crosswalk.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1489` | 0 | rank 1166, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` at preflight | 0 | only the pre-existing untracked canonical `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 10882,10887 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded official proceedings PDF retrieval, `sha256sum`, `stat`, `pdfinfo`, and `pdftotext` inspection | 0 | matching 2017 source-family lead and section/equation loci identified; discovery only |
| declaration-shaped exact-topic search over repo-local Lean and pinned mathlib | 1 expected | no `softmax`, self-attention, multi-head-attention, scaled-dot-product-attention, Vaswani, or source-identical Transformer declaration; not an absence proof |
| broad topic search over the same Lean sources | 0 | only unrelated monad-transformer prose and a holor terminology comment; no model-topic terminal declaration |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | pinned Lean version and commit above |
| `(cd Formalizations/Lean && lake --version)` | 0 | pinned Lake version above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty; pinned package worktree remained clean |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1489/IntakeProbe.lean)` | 0 | ten adjacent APIs elaborated; combined-output SHA-256 `8c54753c7c0ca0c5526c12ba25f8a69133c315c628737c38672cdb9a152e0172`; three axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem |
| `python3 -m json.tool` on all owned JSON files and `.stage1-worker-selftest.json` | 0 after finalization | all structured artifacts are valid JSON objects |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1489-pycache python3 -m py_compile Stage1_Instances/THM-M-1489/check_intake.py` | 0 | scoped validator compiles without adding generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-1489/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 after finalization | target/DAG identity, null target, H5/M4/R4 boundary, source and pin hashes, receipt/packet agreement, exact inventory, and six open tasks agree |
| prohibited-construct scan over `Stage1_Instances/THM-M-1489/IntakeProbe.lean` | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token |
| `git diff --check -- Stage1_Instances/THM-M-1489 .stage1-worker-selftest.json` plus per-new-file no-index whitespace checks | 0 after finalization | no whitespace, final-newline, CR, NUL, or trailing-space defect |

## Known downstream failures

- No stable mathematical proposition is selected. Architecture, tensor shapes, attention and
  softmax semantics, masks, positional encoding, scalar and computation model, parameters, data,
  training or cost model, binders, hypotheses, conclusion, boundary cases, immutable primary
  source, and independent reviews remain open.
- No canonical Lean expression, expression or environment hash, minimal imports, checked alternate
  encoding, or statement mutation certificate exists.
- The API probe establishes adjacent substrate only. It does not locate or validate a
  source-identical proof and does not upgrade the root from `M4`.
- Complete anchor and proof-body audit, obligation registry and typed graphs, proof, composition
  and trust checks, readable reconstruction, hermetic replay, deterministic evidence bundle,
  independent release verification, and master acceptance remain open.

These failures block statement and theorem execution but do not invalidate a truthful,
self-tested `planned` intake. Verdict: `no_state_change`. The self-tested worker proposal may be
handed off as `[_]`; it remains unfinished and unaccepted. `audit_complete=false` and
`theorem_complete=false`. Only the integration lane may accept the provisional worker receipt.
