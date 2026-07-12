# THM-M-0028 intake validation

Base revision: `936bf2b9e968abd3b79b5b36d32f2f2bff648c7e`; base tree:
`8c9d3261b0ba9a81deb5bfc19a335a02cb80f962`. Validation date: 2026-07-13
(Asia/Shanghai); the provisional receipt records the worker validation window.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, the source-matched commutative implication and historical domain boundary,
JSON/scoped invariants, a narrow pinned Lean API probe, prohibited-construct hygiene, and
whitespace. It does not pass the formal statement gate, `H0` source gate, anchor audit, or proof
gate.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned files and worker packet make this nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Source boundary

Crossref metadata confirmed Noether's 1921 article, pages 24-66, and DOI recorded in the
crosswalk. The Zenodo scan was inspected at printed pages 29-31. It identifies a commutative but
not necessarily unital ring, finite ideal bases, Satz I deriving eventual chain stabilization, the
converse observation, and earlier Dedekind/Lasker provenance. Stacks Project tag `00FM` was
inspected as a modern commutative equivalence cross-check. This is enough for an honest `H1`
intake, not `H0`: complete translation, unital-specialization justification, proof and assumption
mapping, errata work, and independent source review remain open.

## Commands and results

All commands ran at the repository root unless a different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0028` | 0 | rank 1073; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 221,226 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error 'https://api.crossref.org/works/10.1007/BF01464225'` with a bounded `jq` projection | 0 | Noether article, year, pages, and authorship confirmed |
| `curl -L --fail --silent --show-error 'https://zenodo.org/api/records/1428306/files/article.pdf/content' -o /tmp/noether1921.pdf`; `sha256sum`, `pdfinfo`, `pdftotext -layout`, and bounded `rg`/`sed` inspection | 0 | observed digest-bound primary scan and printed pages 29-31 findings recorded; no durable-archive, H0, or independent-review claim |
| `curl -L --fail --silent --show-error 'https://stacks.math.columbia.edu/tag/00FM'`; download `https://stacks.math.columbia.edu/download/algebra.pdf`, then `sha256sum`, `pdfinfo`, `pdftotext`, and bounded `rg` inspection | 0 | modern finite-generation/ACC equivalence cross-checked; secondary evidence only |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above; package status clean |
| `sha256sum` on authoritative manifests, source records, toolchain, lock, and two probed mathlib modules | 0 | hashes recorded in `instance.json` and replay-checked by `check_intake.py` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0028/IntakeProbe.lean)` | 0 | seven adjacent APIs elaborated; axiom lists printed; no target declaration or proof credit |
| `python3 -m json.tool` on all structured owned files and the root packet | 0 | valid JSON after finalization |
| `python3 -c` with `ast.parse` on `check_intake.py` | 0 | scoped checker parsed without bytecode output |
| `python3 -B Stage1_Instances/THM-M-0028/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, source/dependency hashes, H1/M3/R3 boundary, exact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0028/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean construct scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` for each owned file and worker packet | 0 aggregate | no whitespace diagnostics; exit 1 from each no-index invocation was only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0028 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; per-file checks cover untracked files |

## Known open gates

Independent primary-source review; complete historical definition, premise, direction, proof,
priority, translation and errata mapping; and the nonunital-to-unital scope decision remain open.
So do canonical Lean elaboration and fingerprints, explicit finite-generation-to-class transport,
checked alternate encodings, four statement mutation classes, exhaustive anchor and proof-body
audit, discovery protocol, obligation registry and typed graphs, proof/composition/provenance/trust
closure, readable proof reconstruction, hermetic replay, deterministic release evidence,
independent verification, master acceptance, audit completion, and theorem completion.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0028-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No H0, M0, R0, proof, audit completion, theorem completion,
or master acceptance is claimed.
