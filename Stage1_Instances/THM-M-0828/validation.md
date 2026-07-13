# Intake validation

Base revision: `be8701e88e791545c16a262edd1909486d5cef4b`; base tree:
`78b0a751473bf6d71f453a6aad18b130268a3428`.

This validation covers target membership, the planned dossier and open task DAG, catalog and
cross-record provenance, the bibliographic primary-source lead, proposition-changing scope,
structured intake invariants, a narrow pinned Lean API probe, prohibited-construct hygiene, and
whitespace. It does not validate a canonical Edmonds-Karp statement or proof because none is
frozen.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned files and root worker packet make the final tree dirty
and nonrelease.

## Source boundary

The Stage1-bearing catalog says only "a polynomial-time algorithm for maximum flow." The separate
computer-science record says `O(VE^2)`, but is a different UID and lacks definitions. Crossref and
DBLP agree on the 1972 Edmonds-Karp paper's bibliographic identity. The Crossref JSON payload was
5971 bytes with SHA-256
`25aa7ca0f3f4b1e93644a2e83cd5e2ea03639615f87502f8d579c0e46622d079`. The ACM primary PDF returned
HTTP 403, so no statement, proof-page, correction, or errata inspection is claimed. This supports
an H1 source lead with explicit reconstruction debt, not H0.

## Environment fingerprint

- Platform: Linux 7.0.0-27-generic, x86_64.
- Lean: 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0828` | 0 | rank 1386; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6082,6087 -- Docs/researches/math_theorems.md` | 0 | all six uncited source-record lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| inspect `Docs/researches/cs_theorems.md:172` and Stage0 `THM-C-0097` | 0 | separate UID says `O(VE^2)`; recorded only as a scope discrepancy, not target authority |
| `curl -L --fail -sS https://api.crossref.org/works/10.1145/321694.321699 -o /tmp/edmonds-karp-crossref.json` | 0 | 5971-byte bibliographic payload with the SHA-256 above |
| `curl -L --fail -sS https://dblp.org/rec/journals/jacm/EdmondsK72.xml` | 0 | title, authors, venue, volume, pages, year, and DOI agree with Crossref |
| `curl -L --fail -sS https://dl.acm.org/doi/pdf/10.1145/321694.321699 -o /tmp/edmonds-karp-1972.pdf` | 22 | HTTP 403; primary text unavailable, explicitly retained as an open source gate |
| bounded `rg` over pinned mathlib and repo-local Lean for Edmonds-Karp, Ford-Fulkerson, maximum/minimum flow, residual network, and augmenting path | bounded search completed | no relevant declaration located; unrelated analytic uses of `flow` excluded; not a global absence claim |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build ran |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0828/IntakeProbe.lean)` | 0 | twelve generic directed-adjacency, path, shortest-walk, and finite-walk APIs elaborated; complete stdout SHA-256 `26db1cd1e80c5e67d57d285af0cbb92b463c563abbd3320e70f294bab3b65434`; no target or proof credit |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all JSON parsed after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0828/check_intake.py` | 0 | scoped validator parsed without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0828/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | authority identity, planned H1/M4/R4 boundary, null target, source and artifact hashes, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0828/check_intake.py` | 0 | public replay mode passed without the scheduler-only packet |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 per new file was only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0828 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; preceding no-index checks covered untracked files |

## Known downstream failures

- An immutable lawful primary or approved authoritative source must be inspected for the exact
  network, flow, algorithm, correctness, complexity, proof, correction, and errata boundaries and
  then independently reviewed.
- The Stage1 polynomial gloss must be reconciled explicitly with the companion `O(VE^2)` wording;
  the network/capacity/residual/BFS/output/correctness/cost-model clauses remain unselected.
- No canonical Lean expression, minimal imports, expression/environment fingerprint, checked
  alternate transport, or required statement mutation is frozen.
- The pinned APIs are generic adjacent infrastructure, not a maximum-flow artifact; no terminal
  proof body, provenance, trust closure, or formal candidate receives credit.
- Discovery and obligation freezes, typed graphs, proof, composition, readable reconstruction,
  hermetic replay, deterministic bundle, independent release verification, and master acceptance
  remain open.

These failures block statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake. Only the integration lane may accept the
provisional worker receipt.
