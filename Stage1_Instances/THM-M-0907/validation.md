# Intake validation

Base revision: `39704171d88ffcdc33a47365ae9791f855fa3a44` (tree
`050ab5c6392560337051d2eadd1b82277dbe1c4f`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, a fail-closed planned dossier and open task DAG, literal
catalog provenance, primary-source family discrimination, JSON and scoped invariants, a narrow
pinned Lean substrate probe, bounded formal discovery, prohibited-construct hygiene, and
whitespace. It does not validate an exact Alon-Tarsi statement or proof because source-root and
encoding decisions remain open.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
The owned intake files and root worker packet make the final snapshot dirty and nonrelease.

## Source and environment inspection

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`; Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

The author-hosted primary PDF for Alon and Tarsi's *Colorings and orientations of graphs* was
retrieved to temporary storage only. HTTP and HTTPS yielded identical 149,795-byte content with
SHA-256 `aaf67fe67852b7f0d4a14feaabed7f7b2916c384214324e8253029d7242ee565`.
Theorem 1.1 and its definitions and proof were inspected; Crossref and publisher metadata confirmed
the bibliographic identity. No external bytes were added to the repository or accepted as H0.

## Commands and results

All repository commands ran from the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0907` | 0 | rank 1449; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 6635,6640 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| pre/post-dedup Stage0 history inspection at `c61be3c80710c07c5f7626e3404e51f40ecb39a6` | 0 | Alon-Tarsi moved from `THM-M-0934` to current `THM-M-0907`; pre-dedup `THM-M-0907` was sparse cut, so current provenance is bound to ID plus name/gloss |
| `curl -L --fail --silent --show-error http://www.math.tau.ac.il/~nogaa/PDFS/chrom3.pdf -o /tmp/thm-m-0907-chrom3.pdf` | 0 | author-hosted primary PDF retrieved outside the repository; 149795 bytes and SHA-256 `aaf67fe...565` |
| `pdfinfo` and `pdftotext -layout` on the temporary PDF | 0 | 13-page scan; Theorem 1.1, definitions, proof on printed pp.1-4, alternate roots, and Dinitz boundary inspected; extracted text SHA-256 `f0b8b7a3...f6714` |
| Crossref DOI metadata and Springer landing-page inspection | 0 | authors, title, Combinatorica 12(2), June 1992, pp.125-134, and DOI agreed; mutable observations only |
| bounded Crossref update/relation and erratum inspection | 0 | no registered relation or located erratum; no-match observation only, not proof that no correction exists |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean version, commit, and target recorded above |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake version above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned revision and tree recorded above; package status clean |
| bounded `rg` for Alon-Tarsi, choosability, Eulerian-subgraph parity, and generic Nullstellensatz in repo-local Lean and pinned mathlib | 0 | located only generic 1999 Nullstellensatz declarations and adjacent digraph/coloring APIs; no exact Alon-Tarsi/list-coloring target; intake discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0907/IntakeProbe.lean)` | 0 | eight adjacent pinned API signatures elaborated; complete stdout SHA-256 `c6cbcc52...77cf9`; no target statement or proof body |
| `python3 -m json.tool` on all structured owned files and `.stage1-worker-selftest.json` | 0 each | valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0907-pycache python3 -m py_compile Stage1_Instances/THM-M-0907/check_intake.py` | 0 | scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0907/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and dependency hashes, H1/M4/R4 null-target boundary, exact inventory, provisional receipt, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0907/check_intake.py` | 0 | public replay mode passed without the scheduler-only root packet |
| scoped Lean scan for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declarations | 1 (expected no match) | no prohibited declaration in the discovery-only probe |
| per-new-file `git diff --no-index --check /dev/null FILE` and scoped `git diff --check` | 0 aggregate | no whitespace diagnostics; no-index exit 1 was accepted only as the expected new-file difference |

## Known open gates

Exact source-root selection, lawful immutable preservation, complete graph/orientation and
Eulerian-subgraph semantics, parity counts, list and proper-coloring conventions, premise/proof-node
mapping, corrections and errata, 1992-versus-1999 algebraic route, neighbor ownership, and
independent source approval remain open. So do canonical Lean elaboration, minimal imports,
expression/environment fingerprints, checked transports, all four mutation classes, exhaustive
anchor audit, discovery and obligation freezes, typed graphs, proof and composition, trust closure,
readable reconstruction, hermetic replay, deterministic bundle, independent verification, and
release.

These gates block the statement and theorem, but do not invalidate a truthful self-tested planned
intake. `H1` applies to the inspected complete primary proof candidate with unresolved mapping; it
does not grant H0.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0907-INTAKE` only. It supports a planned
dossier and concrete statement blocker, not an accepted node receipt. No canonical statement,
H0 source closure, proof, audit completion, theorem completion, or master acceptance is claimed.
