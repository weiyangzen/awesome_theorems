# THM-M-0750 intake validation

Base revision: `0e5ae82e6d507ee607c3f011900571ffd8096800`; base tree:
`400e6edf1f69b971b60a367e3ea29be359b07907`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, topic-versus-proposition and neighbor discrimination, JSON and scoped invariants, a
narrow pinned Lean API probe, prohibited-construct hygiene, and whitespace. It does not validate a
canonical theorem statement or proof because the catalog does not supply one truth-valued
Turing-degree proposition.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source boundary

`Docs/researches/math_theorems.md:5528-5533` supplies only the title, Post attribution, 1944 date,
topic gloss, importance, and untrusted status. All six lines originate at
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. Stage0 repeats them while leaving every exact
statement and evidence component open. Crossref confirmed Post's 1944 bibliography. Two initial
legacy AMS and Project Euclid paths returned HTML, but an AMS publisher URL with the `/journals/`
path produced a valid 33-page version-of-record PDF, bound by SHA-256
`b2f200e8...d0c1d`; its extracted text is bound by `3e782de4...bad0`.

Printed pages 289-290 give degree terminology and frame determination of degrees as a primary
problem; page 297 proves a highest-degree result under one-one reducibility; section 11 on pages
311-312 gives an explicitly informal general/Turing-reducibility account; and page 314 leaves the
lower-degree question open. The paper therefore supplies several definition, theorem, and open-
problem surfaces rather than selecting one proposition for this catalog row. No H0 or exact target
claim is admitted.

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
- `Mathlib/Computability/TuringDegree.lean` SHA-256:
  `d5fd0caf5c321343ec378e2601913aec152efac58f113ce3b602dca7345b1e5c`.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless another
working directory is shown. The initial successful source retrieval was produced by the concurrent
`THM-M-0748` intake worker in automation clone `workers/slot57`; only its repo-relative worker
identity is public here. This worker independently copied the shared temporary files, verified their
type, page and byte counts, hashes, and pinpoint text, and records both actions rather than
misattributing the network fetch.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0750` | 0 | rank 1336; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 5528,5533 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| shared producer `workers/slot57`: `tmp=$(mktemp -d); curl -L --max-time 60 -sS -A 'Mozilla/5.0' 'https://www.ams.org/journals/bull/1944-50-05/S0002-9904-1944-08111-1/S0002-9904-1944-08111-1.pdf' -o "$tmp/post.pdf"; pdftotext -layout "$tmp/post.pdf" "$tmp/post.txt"` | 0 reported/shared | publisher PDF and extracted text were made available in shared `/tmp`; network retrieval was not rerun successfully by slot78 and is not claimed as slot78 execution |
| `cp /tmp/tmp.ywFHAhhlUH/post.pdf /tmp/slot78-post-shared.pdf; cp /tmp/tmp.ywFHAhhlUH/post.txt /tmp/slot78-post-shared.txt; file /tmp/slot78-post-shared.pdf; pdfinfo /tmp/slot78-post-shared.pdf; wc -c /tmp/slot78-post-shared.pdf /tmp/slot78-post-shared.txt; sha256sum /tmp/slot78-post-shared.pdf /tmp/slot78-post-shared.txt; rg -n 'degree of unsolvability|General \(Turing\) reducibility|still in the informal stage|We shall talk as if|completely on the fence' /tmp/slot78-post-shared.txt` | 0 | slot78 independently observed 33 pages and 3,959,828 PDF bytes, SHA-256 `b2f200e8...d0c1d`; text is 92,496 bytes, SHA-256 `3e782de4...bad0`; relevant printed pages 289-290, 297, 311-312, and 314 inspected |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0750/IntakeProbe.lean)` | 0 | eight exact interfaces elaborated; representative transitivity/equivalence proofs report `propext`; stdout SHA-256 `2da82fb7...6f1a`; no canonical target or wrapper declared |
| `python3 -m json.tool` on the three owned JSON artifacts and `.stage1-worker-selftest.json` | 0 | all finalized structured artifacts are valid JSON |
| Python `ast.parse` and `py_compile` on `check_intake.py` with cache in `/tmp` | 0 | scoped validator parses and compiles without creating an owned generated file |
| `python3 -B Stage1_Instances/THM-M-0750/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned H5/M4/R4 boundary, null target, source and neighbor boundaries, exact inventory, hashes, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0750/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| scoped prohibited-declaration scan over `Stage1_Instances/THM-M-0750/*.lean` | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check /dev/null FILE` and scoped `git diff --check` | 0 aggregate | no whitespace diagnostics; no-index exit 1 represented only the expected new-file difference |

## Known downstream failures

- The catalog is a topic label. Although relevant primary passages were inspected, they expose
  multiple definitions, theorems, and an open problem rather than one selected truth-valued
  proposition; ordered binders, a complete premise/proof crosswalk, errata review, and independently
  approved target correction remain open.
- Selecting reducibility reflexivity/transitivity, equivalence, a quotient definition, partial
  order, bottom, join, density, incomparability, jump, or c.e.-degree structure would choose
  proposition-changing data and can conflict with separately owned neighboring targets.
- No canonical Lean expression, minimal exact imports, expression or environment fingerprint,
  checked encoding transport, or mutation suite is frozen.
- Formal anchor audit, discovery and obligation freezes, typed graphs, proof, composition, trust
  closure, readable reconstruction, hermetic replay, deterministic bundle, independent release
  verification, and master acceptance remain open.

Because `H5` is a target classification, ordinary proof execution is blocked pending an
integration-authorized truth-valued correction or redirection. These failures prevent statement,
audit-completion, and theorem-completion claims. They do not invalidate a truthful, self-tested
`planned` intake whose purpose is to freeze the ambiguity and open the downstream DAG. Only the
integration lane may accept the provisional worker receipt.
