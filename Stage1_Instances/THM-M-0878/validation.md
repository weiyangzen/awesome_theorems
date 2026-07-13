# THM-M-0878 intake validation

Base revision: `0c019b7194c9c43fa5f683fa82d637a0b275410d` (tree
`43cf6ac322b1dba09be739b52ab3d02e9f9d8f3e`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, source-statement and
non-substitution boundaries, the six-node open task DAG, structured intake invariants, and a narrow
pinned Lean API probe. It does not validate a canonical minimum-cost-flow proposition or proof
because the catalog provides a topic gloss and the inspected source contains several distinct
claims. The automation-provided canonical `.lake` symlink was pre-existing and used read-only; no
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake action, or other
`.lake` mutation was performed. This dirty worker run is nonrelease evidence.

## Source evidence

The MIT DSpace copy of Goldberg and Tarjan, *Finding Minimum-Cost Circulations by Canceling
Negative Cycles*, `MIT/LCS/TM-334` (July 1987), was downloaded to temporary storage and inspected.
The 18-page, 4237080-byte PDF has SHA-256
`8450b621bc6ea4d9fa7954e44451b4e91c1cc547a1ac45a1611a85d72c3c86f7`; text produced by
`pdftotext -layout` has SHA-256
`e5443518cfc87ece59ec065aae4f7d01c3cf5dc9c144f078bc1012bdc0290226`. Section 2 defines the
circulation model and states Theorem 2.1; Sections 3 and 4 contain distinct optimality,
termination, correctness, and complexity results. This supports H1 and the scope map, but catalog
source identity and root selection, complete premise/proof mapping, report-to-journal delta,
corrections, durable source admission, independent review, and H0 remain open.

Crossref confirms the peer-reviewed descendant as Goldberg and Tarjan, *Journal of the ACM* 36(4)
(October 1989), 873-886, DOI `10.1145/76359.76368`. The journal body was not inspected or treated
as source-identical to the report.

## Environment

- Platform: Linux `7.0.0-27-generic`, x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the worker root unless a different `cwd` is shown.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0878` | exit 0; rank 1431, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `git blame -L 6432,6437 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| download the MIT DSpace original bitstream to temporary storage | exit 0; PDF byte count and SHA-256 recorded above |
| `pdfinfo` and `pdftotext -layout` on the temporary PDF, followed by Sections 1-4 inspection | exit 0; 18 pages; model, Theorem 2.1, Theorems 3.1-3.10, and Theorem 4.3 crosswalked |
| fetch Crossref metadata for DOI `10.1145/76359.76368` | exit 0; author/title, JACM volume 36 issue 4, pages 873-886, and October 1989 confirmed; response SHA-256 `55122ed4f299eb96cb876bc695a7823b0d0a57f1d5cf9720213342c64d3d85de` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | exit 0; pinned revision/tree above; package worktree clean |
| bounded `rg` search for minimum-cost flow/circulation, negative residual cycles, cycle canceling, and transshipment over repo-local and pinned mathlib Lean | expected no-match exit 1; no candidate declaration found; this is not a global absence claim |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0878/IntakeProbe.lean)` | exit 0; nine graph/path-weight/sum/argmin APIs elaborated; stdout SHA-256 `edfce5af6c2bfa77b75c654ccb56b5b6993f1839ea7afbb8cba4ee7fddb8152d` |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | exit 0 for each after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0878/check_intake.py` | exit 0; scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0878/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; identity, planned H1/M4/R4 boundary, null target, source/pins/hashes, receipt/packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0878/check_intake.py` | exit 0; public replay mode passes without the scheduler-only packet |
| prohibited Lean proof-escape scan over the owned path | expected no-match exit 1; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | no whitespace diagnostics; per-file exit 1 is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0878 .stage1-worker-selftest.json` | exit 0; tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |

## Known open gates

- Master acceptance of this intake is pending.
- A reviewer must choose circulation optimality, a fixed-value or maximum-value flow theorem,
  existence, integrality, duality, algorithm correctness, complexity, or another exact source
  claim, then map every incorporated definition, premise, conclusion, correction, and boundary case.
- The technical report is inspected and hashed, but its relationship to the uncited catalog record
  and peer-reviewed journal version has not been independently accepted.
- Canonical Lean target, minimal imports, expression and environment fingerprints, checked
  transports, and all four required statement mutations remain open.
- Exhaustive formal anchor and proof-body provenance audit, discovery and obligation freezes, typed
  graphs, proof, composition, trust closure, readable reconstruction, hermetic replay,
  deterministic bundle, independent verification, audit completion, and theorem completion remain
  open.

These failures block statement and theorem execution but do not invalidate a truthful, self-tested
`planned` intake. Only the integration lane may accept the provisional worker receipt.
