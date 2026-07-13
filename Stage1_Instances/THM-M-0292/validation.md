# Intake validation

Base revision: `72e9e8092182121a6794921f61fcc9cae22f726d` (tree
`0d6c1fdf06d1573c256af331c6b198e5a787af43`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, repository and human-source
boundaries, the scope map and crosswalk, the open downstream task DAG, structured intake
invariants, and a narrow pinned Lean Dini-interface probe. It does not validate source fidelity, a
canonical proposition, a proof, or theorem completion. The automation-provided canonical `.lake`
symlink was pre-existing and used read-only; no dependency update, build, clone, fetch, or other
`.lake` mutation was run. This dirty worker execution is nonrelease evidence.

## Environment

- Linux 7.0.0-27-generic, x86_64.
- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Pinned Dini source SHA-256:
  `d671cee68ea4d518e5260ae2faa98faf05c6e84a32ab4e7a1c8b9b2882b7dfab`.

## Commands and results

All commands ran from the worker clone root unless a `cwd` is stated.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0292` | 0 | rank 1542; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink existed; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 2097,2102 -- Docs/researches/math_theorems.md` | 0 | all six uncited target fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded repository search for `迪尼定理`, `单调函数列的一致收敛`, and `Dini theorem` | 0 | one catalog record and one rev-5.6 target found; no duplicate target located; bounded intake discovery only |
| `curl -L --fail --max-time 45 -sS https://api.digitale-sammlungen.de/iiif/presentation/v2/bsb11374230/manifest -o /tmp/bsb11374230_manifest.json` | 0 | manifest metadata inspected; it enumerates 430 page-image canvases; bounded OCR/image inspection found no accepted exact theorem locator |
| Encyclopedia of Mathematics API query for permanent revision `32779` | 0 | secondary nonnegative-series closed-interval formulation inspected; archived observation SHA-256 `706d060dada3be39e47308589c7cc9b8b0b7e4f1eb07a7f3ef62d81f11f936f7`; E5 only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | pinned Lean and Lake versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; package source worktree clean |
| `rg -n -i --glob '*.lean' 'Dini\|tendstoUniformly_of_forall_tendsto\|tendstoUniformlyOn_of_forall_tendsto' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 0 | exact-topic pinned Dini module and increasing/decreasing interfaces found; no repo-local Dini artifact found; bounded discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0292/IntakeProbe.lean)` | 0 | eight pinned Dini interfaces and two classical `ℕ`/`ℝ` compact-set specializations elaborated; stdout SHA-256 `9c8e4610cf9d4e3c5219936e526205b6b9031b6521798ec21187a64c15759133`; no target declaration or proof body added |
| `python3 -m json.tool` separately on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts parsed as valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0292-pycache python3 -m py_compile Stage1_Instances/THM-M-0292/check_intake.py` | 0 | scoped validator compiled without writing generated files into the owned path |
| `python3 -B Stage1_Instances/THM-M-0292/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, pins, planned `H1/M3/R4` null-target boundary, exact inventory, receipt/packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0292/check_intake.py` | 0 | public replay mode passed without requiring the scheduler-only root packet |
| prohibited Lean construct scan over `IntakeProbe.lean` | 1 | expected no-match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0292 .stage1-worker-selftest.json` | 0 | no tracked-file whitespace diagnostics |
| per-new-file `git diff --no-index --check /dev/null <file>` loop (accepting diff status 1) | 0 | no untracked-file whitespace diagnostics |

## Known open gates

- The original 1878 theorem/page, incorporated definitions, proof boundary, corrections or errata,
  translation, full source crosswalk, and independent source review remain open.
- Compact-space versus compact-set scope, index-monotonicity meaning and direction, index and
  codomain generality, continuity and pointwise-convergence premises, conclusion encoding, ordered
  binders, and degenerate cases are not selected by the catalog.
- The secondary nonnegative-series formulation has no checked partial-sum transport to a selected
  sequence root.
- No canonical Lean target, minimal-import claim, elaborated expression/environment fingerprint,
  checked alternate transport, or required statement mutation exists.
- Direct pinned theorem interfaces support `M3` discovery only; exhaustive candidate, terminal
  provenance, dependency, placeholder, axiom, and trust audits remain open.
- Obligation registry, typed graphs, proof and composition acceptance, readable reconstruction,
  hermetic replay, deterministic bundle, independent verifier, master acceptance, audit completion,
  and theorem completion remain open.

These failures block every downstream claim, but they do not invalidate a truthful, self-tested
`planned` intake that freezes the ambiguity and non-substitution boundary. Only the integration lane
may accept this provisional worker receipt.

The `--worker-packet` command is worker-only: it binds the unintegrated `[ ]` base and root handoff.
The receipt's public structured recipe omits that flag because the integration lane does not merge
`.stage1-worker-selftest.json` and may advance the authoritative intake state independently.
