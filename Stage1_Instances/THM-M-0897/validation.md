# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`; base tree:
`829a47c47ae831cada4f8acc6c2c00ba5883215e`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, source-family discrimination, neighbor-target boundaries, JSON and scoped invariants, a
narrow pinned Lean substrate probe, a bounded repo-local and mathlib search, prohibited-construct
hygiene, and whitespace. It does not validate a canonical theorem statement or proof because the
catalog supplies no stable truth-valued proposition.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

The catalog's exact six-line record has SHA-256
`54a708f4ac97c4cbbc4f3fbe68f80830098cf2a7fcdd505128e92e2ce6d08837` and contains no citation.
Two temporary web observations were used only to confirm that the title spans multiple design types
and multiple mathematical questions:

- Peter J. Cameron's *Encyclopaedia of Design Theory* landing page: 8,130 bytes, SHA-256
  `19fec75a3a171c4eed8404fe13539cdf96d935715ded30eda8e19c0276dad254`.
- *Encyclopedia of Mathematics*, "Block design," revision 44388: 22,811 bytes, SHA-256
  `06d6f7a7721e44c85b225f53545fa2c075efafb05ac867724a10774ef5f83412`.

No downloaded source was added to the repository. Neither mutable reference is catalog provenance
or a pinpoint primary proof source, and neither selects a theorem. No immutable source admission,
complete premise/proof/errata mapping, or independent H0 review is claimed.

## Environment fingerprint

- Platform: Linux x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless another
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0897` | 0 | rank 1039; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6565,6570 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `git rev-parse bcf3f9fa79ab8c2b6610c9875668c2589b35b74f:Docs/researches/math_theorems.md` | 0 | source-record blob `5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf` |
| `curl -L --fail --silent --show-error --max-time 30 https://webspace.maths.qmul.ac.uk/p.j.cameron/design/encyc/ -o /tmp/thm-m-0897-design-encyclopaedia.html` | 0 | retrieved the 8,130-byte mutable breadth reference with the digest recorded above |
| `curl -L --fail --silent --show-error --max-time 30 https://encyclopediaofmath.org/wiki/Block_design -o /tmp/thm-m-0897-block-design.html` | 0 | retrieved the 22,811-byte mutable secondary reference with the digest recorded above |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, x86_64-unknown-linux-gnu, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e` (Lean 4.29.0); no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision/tree above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0897/IntakeProbe.lean)` | 0 | seven finite set-family and counting APIs elaborated; output SHA-256 `f11f4ea2a142713a4343feba8ce7001713683cddf301fcd30ae0937ae18fcf5a` |
| `rg -n -i --glob '*.lean' '\b(BlockDesign\|BalancedIncompleteBlockDesign\|CombinatorialDesign\|SteinerSystem\|SteinerTripleSystem\|TDesign)\b' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 1 (expected no match) | no exact declaration name found; intake discovery only, not an exhaustive anchor audit or global absence claim |
| `python3 -m json.tool Stage1_Instances/THM-M-0897/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0897/task-dag.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0897/intake-receipt.json` | 0 | valid JSON |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | valid JSON |
| `python3 -c "import ast, pathlib; ast.parse(pathlib.Path('Stage1_Instances/THM-M-0897/check_intake.py').read_text(encoding='utf-8')); print('ast parse: ok')"` | 0 | `ast parse: ok`; no bytecode written |
| `python3 -B Stage1_Instances/THM-M-0897/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned H5/M4/R4 state, null target, source hashes, neighbor boundaries, inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0897/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| `rg -n --glob '*.lean' 'sorry\|admit\|sorryAx\|(^\|[[:space:]])axiom[[:space:]]\|(^\|[[:space:]])constant[[:space:]]\|(^\|[[:space:]])opaque[[:space:]]\|(^\|[[:space:]])unsafe[[:space:]]' Stage1_Instances/THM-M-0897` | 1 (expected no match) | no prohibited declaration or proof escape in the API-only probe |
| `git diff --no-index --check /dev/null <path>` run separately for each of the nine owned files and `.stage1-worker-selftest.json` | 1 each (expected new-file difference) | all ten commands emitted no whitespace diagnostics |
| `git diff --check -- Stage1_Instances/THM-M-0897 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |

## Known downstream failures

- The title and gloss do not select one stable proposition. No repository-selected primary source,
  exact design class, parameter tuple, incorporated definitions, assumptions, proof boundary,
  correction/errata decision, or independent source review exists.
- The point/block representation, multiplicity and simplicity conventions, incidence predicate,
  admissibility and divisibility conditions, exact versus asymptotic conclusion, quantifier order,
  and boundary cases remain open.
- Reconciliation with neighboring Kirkman, Wilson, asymptotic design-existence, and Latin-square
  targets remains open.
- No canonical Lean expression, exact imports, expression/environment fingerprint, checked
  alternate encoding, or statement mutation test exists.
- Discovery protocol, formal anchor audit, obligation registry and typed graphs, proof, composition
  and trust checks, readable reconstruction, hermetic replay, deterministic evidence bundle, and
  independent release verification remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze the ambiguity and
open the downstream DAG. Only the integration lane may accept the provisional worker receipt.
