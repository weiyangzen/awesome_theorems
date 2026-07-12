# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`; base tree:
`829a47c47ae831cada4f8acc6c2c00ba5883215e`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, inspection of the exact primary theorem candidate, JSON and scoped invariants, a narrow
pinned Lean substrate probe, a bounded repo-local and mathlib search, prohibited-construct hygiene,
and whitespace. It does not validate a canonical theorem statement or proof because source
admission, independent review, and proposition-changing graph, spectrum, and sequence choices are
still open.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source inspection boundary

The official Annals article page, its published PDF, and immutable arXiv v2 record were inspected.
Published Section 2.3 and Theorem 5.6 identify the exact biregular family and spectral bound; the
proof's repeated 2-lifts show that the sequence grows in vertex count. Published PDF SHA-256:
`1c0f058b4adaa37cfc6e0ce8d75ca67204e725a09fc124228ccbdaabb8ab60cf`; arXiv v2 PDF SHA-256:
`4da468fe22413c0c8a9f77651711db4edadda7d34986e34673db2cd8192bddfb`.
No source file was added to the repository. Full definition incorporation, graph conventions,
cross-edition binder wording, errata disposition, translation review, and independent H0 review
remain open.

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

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0886` | 0 | rank 1037; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6488,6493 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error https://annals.math.princeton.edu/wp-content/uploads/annals-v182-n1-p07-p.pdf -o /tmp/thm-m-0886-source/mss1-published.pdf` | 0 | temporary source input; 417,818-byte, 19-page official PDF with published digest above |
| analogous immutable arXiv v2 PDF download | 0 | temporary source input; 201,114-byte, 16-page PDF with arXiv digest above |
| `pdftotext -layout` and bounded text inspection of both PDFs | 0 | Section 2.3, Theorems 5.5 and 5.6, and the Theorem 5.6 proof boundary inspected |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0886/IntakeProbe.lean)` | 0 | ten adjacent graph, bipartite, degree, adjacency, Hermitian spectrum, multigraph, and permutation-matrix APIs elaborated; combined stdout/stderr SHA-256 `32df9e2c8d621a1d482584389db446453d89d25353d634bf9131b8b6374eb046` |
| bounded exact-topic `rg` over repo-local and pinned-mathlib Lean sources | 1 after excluding unrelated Ramanujan-formula and D. Marcus bibliography hits | no target-family occurrence for biregular Ramanujan graphs or the MSS authors; intake discovery only, not an exhaustive anchor audit |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0886/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0886/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H1/M4/R4 boundary, null formal target, primary candidate, exact inventory, source hashes, packet, and six open downstream tasks agree |
| `python3 -B Stage1_Instances/THM-M-0886/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0886 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |

## Known downstream failures

- The exact primary numbered theorem is identified, but no immutable source admission,
  incorporated-definition map, errata disposition, translation review, or independent source
  approval exists.
- Ordered binders, finite simple-graph carrier, bipartition and degree witnesses, connectedness,
  trivial-eigenvalue multiplicity, non-strict spectral predicate, and size-growing sequence
  encoding remain open.
- No canonical Lean expression, exact minimal imports, expression/environment fingerprint, checked
  alternate encoding, or statement mutation is frozen.
- Formal anchor audit, discovery and obligation freezes, typed graphs, proof, composition, trust
  closure, readable reconstruction, hermetic replay, deterministic bundle, independent release
  verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze the scope boundary
and open the downstream DAG. Only the integration lane may accept the provisional worker receipt.
