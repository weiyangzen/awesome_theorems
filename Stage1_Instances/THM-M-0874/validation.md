# Intake validation

Base revision: `748243faadc15828fb087059337fd05b7be9fdeb`; base tree:
`e46d642646f80980838b6f016f5d69b817bd464d`.

This validation covers target membership, a fail-closed planned dossier, the scope map,
source-statement crosswalk, six-node open task DAG, repository provenance, dated source discovery,
JSON and scoped invariants, a narrow pinned Lean API probe, prohibited-construct hygiene, and
whitespace. It does not validate an exact theorem statement or proof because the corrected source
bundle, binder-complete computation contract, and formal target remain open.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
The owned intake files and root worker packet make the final tree dirty and nonrelease.

## Source boundary

The repository's two identical uncited Babai records are preserved exactly. The following external
sources were fetched to temporary paths on 2026-07-13 for discovery and hashed; they are not
vendored, release-preserved, or admitted H0 evidence:

- Babai arXiv `1512.03547v2`: 843,393-byte, 89-page PDF, SHA-256
  `b6393ff36f4ff1c9646d7b9c5ea9ef78cfb222d52634ffdef2f05fa77daa9c62`; abstract and PDF
  page 4, Theorem 1.1.1, Corollary 1.1.2, definition of quasipolynomial boundedness, and the
  graph-to-string reduction were inspected.
- Babai's author update: 4,776-byte HTML, SHA-256
  `d96a4083ffd3b0b6931500f13e81a33ecb3ec5ab9eebadb64c2fca476faf42ca`; it records the
  invalid timing analysis and restored claim. Fetch required `curl -k` because the environment
  could not validate the site's TLS certificate. This weakens transport evidence and precludes
  release use.
- *Fixing the UPCC case of Split-or-Johnson*: 168,694-byte, four-page PDF, SHA-256
  `e4438bf10d131f4642bee9aa29dfbd9fc133776705c85c3fe3d466da38b95653`; the repair and its
  explicit separate Design Lemma correction boundary were inspected. It was fetched from the same
  site with the same TLS caveat.
- Helfgott, Bajpai, and Dona arXiv `1710.04574v1`: 659,668-byte, 67-page PDF, SHA-256
  `f16a953a084a4bc4b77e30b5d0fb35557a566d5d869bf42de155400466b9f2d2`; abstract,
  introduction, Theorem 1.1, Corollary 1.2, graph-to-string reduction, and repair assessment were
  inspected. The detailed remainder and appendix were identified but not fully crosswalked.

These sources support provisional `H1`: the human result and a post-fix detailed reconstruction
are identifiable, while complete correction, incorporated-definition, premise, proof-node, errata,
and independent acceptance mapping remains open. The canonical statement is deliberately null.

## Environment fingerprint

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

Commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0874` | 0 | rank 1428; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6404,6409 -- Docs/researches/math_theorems.md` and duplicate lines 11551-11556 | 0 | both uncited records originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --max-time 90 -A 'Mozilla/5.0' -sS https://arxiv.org/pdf/1512.03547 -o /tmp/thm-m-0874-babai.pdf`; `file`; `wc`; `pdfinfo`; `sha256sum`; `pdftotext -f 1 -l 6 -layout` | 0 | v2 source dimensions and digest above; selected result pages inspected |
| `curl -L --fail --max-time 60 -A 'Mozilla/5.0' -sS https://export.arxiv.org/api/query?id_list=1512.03547` | 0 | arXiv metadata identified only v2, posted 19 January 2016 |
| Crossref title query and DOI `10.1145/2897518.2897542` lookup | 0 | STOC 2016 extended abstract, pages 684-697, confirmed; pre-fix boundary retained |
| initial verified-TLS fetches of `https://people.cs.uchicago.edu/~laci/{update.html,upcc-fix.pdf}` | 60 | expected environmental TLS verification failure; no evidence claimed from failed bytes |
| `curl -k -L --fail --max-time 60 -A 'Mozilla/5.0' -sS https://people.cs.uchicago.edu/~laci/update.html -o /tmp/thm-m-0874-update.html`; `wc`; `sha256sum` | 0 | dated author update fetched with explicit insecure-TLS, discovery-only boundary |
| corresponding `curl -k` fetch of `upcc-fix.pdf`; `file`; `wc`; `pdfinfo`; `sha256sum`; `pdftotext -layout` | 0 | four-page correction dimensions and digest above; source inspected, transport not release-grade |
| `curl -L --fail --max-time 90 -A 'Mozilla/5.0' -sS https://arxiv.org/pdf/1710.04574 -o /tmp/thm-m-0874-helfgott.pdf`; `file`; `wc`; `pdfinfo`; `sha256sum`; `pdftotext -f 1 -l 8 -layout` | 0 | post-fix source dimensions and digest above; selected result pages inspected |
| `curl -L --fail --max-time 60 -A 'Mozilla/5.0' -sS https://export.arxiv.org/api/query?id_list=1710.04574` | 0 | version, authors, date, and 67-page composition confirmed |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | tool versions agree with the fingerprint; no update or build ran |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0874/IntakeProbe.lean` | 0 | ten adjacent graph, language, reduction, and Turing-time APIs elaborated; stdout SHA-256 `c94680a938d92119c98702932b0d292219a326ffea96af8452fba086ee7bf61d`; no target theorem |
| bounded case-insensitive Lean search for `babai`, `string isomorphism`, `coset intersection`, and `quasipolynomial` | 1 for exact-topic query | no matching implementation or source documentation found in scoped repo/mathlib roots; ordinary graph-isomorphism prose matches were separately classified |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all final structured artifacts are valid JSON |
| Python `ast.parse` on `check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0874/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned H1/M4/R4 boundary, null target, source/tool hashes, inventory, packet, receipt, and six open tasks agree |
| scoped prohibited-construct scan over `Stage1_Instances/THM-M-0874` Lean source | 1 (expected no match) | no prohibited declaration or proof escape in the API probe |
| per-new-file whitespace checks plus `git diff --check` | 0 aggregate | no whitespace diagnostics |

## Known downstream failures

- The human result family is identifiable, but no exact binder-complete canonical statement has
  been independently approved.
- The v2 timing flaw, UPCC repair, separate Design Lemma correction, post-fix proof reconstruction,
  incorporated definitions and assumptions, node crosswalk, errata, and independent source review
  are not yet one accepted immutable H0 bundle.
- Graph model and serialization, malformed-input policy, GI decision and output relation,
  deterministic machine and cost semantics, size variable, exact quasipolynomial definition,
  constants, threshold, rounding, and boundary cases remain open.
- No exact Lean target, minimal imports, elaborated expression/environment fingerprint, checked
  graph-to-string transport, statement mutations, usable formal candidate, or proof body exists.
- Discovery protocol, obligation registry, typed graphs, proof, composition, trust closure,
  readable reconstruction, hermetic replay, deterministic bundle, independent verification, audit
  completion, theorem completion, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake. Only the integration lane may accept the
provisional worker receipt.
