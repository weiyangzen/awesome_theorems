# THM-M-0057 intake validation

## Validation boundary

This is nonrelease worker evidence for a `planned` intake only. The worker clone began at revision
`c79ae75db8880483f10bba17c9bc9dd91a9febcf` (tree
`375fa18a4f8afa63bb51d8b05fb4c804f3bb1240`) with the automation-provided untracked
`Formalizations/Lean/.lake` link. That pinned link was read but not changed. No `lake update`,
`lake build`, dependency clone/fetch, or other `.lake` mutation was run.

The source-discovery download and metadata queries were bounded discovery, not hermetic validation
recipes. The arXiv PDF remained temporary and is identified by its observed hash; it is a
secondary lead, not an accepted durable `H0` source. The two structured recipes in
`intake-receipt.json` are local and deny network use.

## Commands and observed results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok` for 15 assurance groups, 41 legacy rows, 300 legacy slots, and exactly 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0057` | 0 | rank 1524, planned, no legacy slot, legacy artifacts unaccepted, theorem complete false |
| `git status --short --untracked-files=all` before editing | 0 | initial status contained only `?? Formalizations/Lean/.lake`; preserved |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision/tree recorded above |
| `git blame -L 426,431 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error --max-time 30 'https://api.crossref.org/works/10.1215/S0012-7094-53-02004-3' -o /tmp/hw-crossref-final.json` | 0 | 1954-byte response SHA-256 `b341d450a0dfa9386c5cf267fde56e9d65e7c94cc88fb212fba2f0b3229bff94`; title, Hoffman/Wielandt, 1953, volume 20 issue 1, and DOI agreed |
| `curl -L --fail --silent --show-error --max-time 30 'https://api.openalex.org/works/doi:10.1215/S0012-7094-53-02004-3' -o /tmp/hw-openalex-final.json` | 0 | 8826-byte response SHA-256 `a335cd9dd4f8785d9434ccea18a15d1ca02189e2c6c0013b358d893634d4ad6b`; title, authors, year, journal, and closed-access status agreed |
| `curl -L --fail --silent --show-error --max-time 30 'https://api.semanticscholar.org/graph/v1/paper/DOI:10.1215/S0012-7094-53-02004-3?fields=title,authors,year,openAccessPdf,externalIds,url' -o /tmp/hw-s2-final.json` | 0 | 499-byte response SHA-256 `2210704e1bf929349a5b33cbb957aca2025494b8d7a822728787e155d2da8f8f`; title, authors, 1953, and closed-access status agreed |
| `curl -L --silent --show-error --max-time 30 'https://projecteuclid.org/journalArticle/Download?urlid=10.1215/S0012-7094-53-02004-3' -o /tmp/hw-euclid-final` | 0 transport status, unusable body | 1051-byte HTML access interstitial, SHA-256 `84bbd9bd5c3f7339a20a4b02ae643a3d5644bff7ff61ee4ed108942d37b85934`; no primary theorem text admitted |
| `curl -L --fail --silent --show-error --max-time 45 https://arxiv.org/pdf/1612.05759 -o /tmp/hw-arxiv.pdf` followed by `sha256sum`, `pdfinfo`, `pdftotext -layout`, and bounded inspection | 0 | 20-page secondary source observed with SHA-256 `c508f6c7f5f1b66ba93e654d380c134f9bc6b4bb98a30eccb9b59ab844cfa953`; abstract and introduction pages 1-2 state and define the familiar result; H1 lead only |
| `cd Formalizations/Lean && lake env lean --version && lake env lake --version` | 0 | Lean 4.29.0 commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux; Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty; pinned package remained clean |
| bounded exact-topic `rg` search in repo-local Lean and pinned mathlib | 0 | Frobenius, spectrum, and Hermitian eigenvalue substrate found; no Hoffman-Wielandt or general-normal eigenvalue-matching declaration located; unrelated permutation-group Wielandt citations excluded |
| `bwrap --unshare-net --ro-bind / / --dev-bind /dev /dev --proc /proc --chdir "$PWD/Formalizations/Lean" /usr/bin/env -i HOME="$HOME" PATH="$(dirname "$(command -v lake)"):/usr/bin:/bin" "$(command -v lake)" env lean ../../Stage1_Instances/THM-M-0057/IntakeProbe.lean` | 0 | network-isolated replay elaborated eight adjacent APIs; three axiom reports were `[propext, Classical.choice, Quot.sound]`; stdout/stderr SHA-256 `39f6cf219e00f6dda383339f1e48a749e9db454ae00f3bac13ad4da397c0b9a6`; no target or proof body |
| `python3 -m json.tool` on the three owned JSON files and root worker packet | 0 | valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0057-pycache python3 -m py_compile Stage1_Instances/THM-M-0057/check_intake.py` | 0 | scoped validator compiled without adding files to the owned path |
| `bwrap --unshare-net --ro-bind / / --dev-bind /dev /dev --proc /proc --chdir "$PWD" /usr/bin/env -i PATH=/usr/bin:/bin /usr/bin/python3 -B Stage1_Instances/THM-M-0057/check_intake.py --worker-packet .stage1-worker-selftest.json --skip-replay` | 0 | network-isolated static target/DAG identity, source/dependency hashes, null target, H1/M4/R4, exact inventory, provisional receipt/packet, and six open tasks agreed; the separate Lean recipe owns declaration replay |
| `python3 -B Stage1_Instances/THM-M-0057/check_intake.py` | 0 | public replay mode passed |
| prohibited Lean construct scan | 0 wrapper status | inner `rg` returned expected no-match exit 1; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration found |
| tracked and per-new-file whitespace checks | 0 | `git diff --check` and no-index checks emitted no whitespace diagnostics |

Per-action timestamps, observed exits, input-manifest digests, output/log hashes, task coverage,
empty obligation coverage, and declaration coverage are recorded in `intake-receipt.json`. The
intake has no canonical obligation registry, so `covered_obligation_ids` is truthfully empty.
`covered_task_ids` records only the assigned intake task and is not theorem-proof coverage.

## Discovery search

The bounded formal search was equivalent to:

```bash
rg -n -i --glob '*.lean' \
  'hoffman.?wielandt|wielandt|spectr.*variation|eigenvalue.*perturb|perturb.*eigenvalue|frobenius.*eigen|eigen.*frobenius' \
  Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib
```

Results were manually discriminated because the name `Wielandt` also occurs in unrelated finite
permutation-group citations. This is intake discovery, not the later immutable discovery protocol
or a global absence claim.

## Result

The original-paper metadata and inspected later source confirm a real theorem family, but they do
not close primary-source fidelity. The Lean probe authenticates adjacent substrate but neither
elaborates nor proves the root. The provisional root assessment is `[H1, M4, R4]`.

The dossier is a worker-self-tested planned intake proposal. Its receipt is unsigned,
non-content-addressed, and not master-accepted. Exact statement, all downstream tasks, audit
completion, and theorem completion remain open.
