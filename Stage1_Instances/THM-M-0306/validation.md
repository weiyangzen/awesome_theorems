# Intake validation

Base revision: `d257e1e5e5fa003d6e1f26344c0331bf99374fa9`; base tree:
`fa06b50b528e038d182d5479a18296f63fa5eae5`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, source chronology and duplicate discrimination, JSON and scoped invariants, a narrow
pinned Lean substrate probe, a bounded repo-local and mathlib search, prohibited-construct hygiene,
and whitespace. It does not validate a canonical theorem statement or proof because the catalogue
does not supply one exact Friedrichs proposition.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

The *Encyclopedia of Mathematics* entry `Friedrichs inequality`, permanent revision 46991, was
downloaded to temporary worker storage and inspected. The 20,189-byte HTML has SHA-256
`ed668445fe0448f03e874015df74d9ae36f7b0c5475afe48da7e44a9e1212341`. It gives a modern
boundary-term `W_2^1` inequality and attributes a two-dimensional smooth version to Friedrichs,
but its reference points to a gravitation article rather than an evident Sobolev theorem.

The Goettingen Digitalisation Centre IIIF manifest for *Mathematische Annalen* volume 98 was also
inspected. The 995,144-byte manifest has SHA-256
`4d48d3a7e812374ea61b9adeed5e1378c65f0ca219c388800bd8547f076d46e7` and identifies the
complete 1928 volume. Scanned printed pages 566-575 match Springer metadata for Kurt Friedrichs,
DOI `10.1007/BF01451608`, and concern an invariant formulation of Newtonian gravitation and the
Einstein-to-Newton limit. The catalogue instead says 1929. These inputs expose a source-integrity
question; they do not select, correct, or prove the target. No temporary source was added to the
repository, and no H0 source evidence is claimed.

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
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0306` | 0 | rank 1307; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 2195,2200 -- Docs/researches/math_theorems.md` | 0 | the assigned uncited record originates at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `git blame -L 9073,9078 -- Docs/researches/math_theorems.md` | 0 | the same-gloss `THM-M-1240` record originates at the same commit |
| `curl -L --fail --silent --show-error --max-time 60 'https://encyclopediaofmath.org/index.php?title=Friedrichs_inequality&oldid=46991' -o /tmp/friedrichs_eom.html` | 0 | fetched 20,189 bytes; the inspected capture has the recorded digest, while cache metadata makes raw HTML replay hashes unstable; permanent-revision mathematical content and the inconsistent historical reference were inspected as secondary discovery only |
| `curl -L --fail --silent --show-error 'https://manifests.sub.uni-goettingen.de/iiif/presentation/PPN235181684_0098/manifest?version=7a696723' -o /tmp/friedrichs_manifest.json` | 0 | fetched 995,144 bytes with the recorded digest; mapped printed pages 566-575 to canvases 570-579 |
| `curl -L --fail --silent --show-error --max-time 60 'https://link.springer.com/article/10.1007/BF01451608' -o /tmp/friedrichs_springer.html` | 0 | confirmed Kurt Friedrichs, pages 566-575, March 1928, DOI, and the gravitation-article title; discovery only |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0306/IntakeProbe.lean` | 0 | seven compact-support, norm, derivative, and Gagliardo-Nirenberg-Sobolev interfaces elaborated; no target declaration or proof credit |
| `rg -n -i --glob '*.lean' 'Friedrichs\|弗里德里希斯' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 1 (expected no match) | no exact-topic occurrence; discovery only, not a complete anchor audit |
| `python3 -m json.tool Stage1_Instances/THM-M-0306/instance.json >/dev/null` and the same command separately for `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 each | all four structured artifacts valid JSON after finalization |
| `python3 -c "import ast,pathlib; ast.parse(pathlib.Path('Stage1_Instances/THM-M-0306/check_intake.py').read_text())"` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0306/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned H1/M3/R4 boundary, null target, source/duplicate boundaries, inventory, packet, hashes, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0306/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| `rg -n -i --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0306` | 1 (expected no match) | no prohibited declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0306 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |

## Known downstream failures

- No independently accepted primary source, exact theorem, incorporated definition chain,
  assumption map, correction record, or proof crosswalk exists.
- The catalogue's 1929 date conflicts with the inspected secondary and primary metadata; the
  secondary entry's cited article appears unrelated to the modern Sobolev gloss.
- `THM-M-1240` repeats the attribution, date, and gloss; target identity, deduplication, and proof
  ownership remain unresolved.
- Domain, dimension, function model, exponent data, support versus trace condition, derivative,
  norms, constant dependencies, binder order, conclusion, and boundary cases remain open.
- No canonical Lean expression, exact minimal imports, expression/environment fingerprint, checked
  alternate encoding, or statement mutation is frozen.
- Formal anchor audit, discovery and obligation freezes, typed graphs, proof, composition, trust
  closure, readable reconstruction, hermetic replay, deterministic bundle, independent release
  verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze the ambiguity and
open the downstream DAG. Only the integration lane may accept the provisional worker receipt.
