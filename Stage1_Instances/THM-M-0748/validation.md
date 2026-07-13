# Intake validation

Base revision: `0e5ae82e6d507ee607c3f011900571ffd8096800` (tree
`400e6edf1f69b971b60a367e3ea29be359b07907`). Validation ran on 2026-07-13 in
the isolated worker clone.

Validation is limited to target-set consistency, planned-dossier structure, source and
non-substitution boundaries, the open downstream task DAG, pinned environment identity, a narrow
Lean API and abstract-order-shape probe, bounded local discovery, proof-escape hygiene, and
whitespace. It does not validate a source-identical statement or proof. The preflight worktree
contained only the automation-provided untracked `Formalizations/Lean/.lake` symlink to canonical
pinned artifacts. It was used read-only. No `lake update`, `lake build`, dependency clone or fetch,
or other `.lake` mutation was performed. This is nonrelease worker evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `lean-toolchain` SHA-256 `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256 `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0748` | 0 | rank 1334, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only pre-existing `Formalizations/Lean/.lake`; base revision/tree recorded above |
| `git blame -L 5514,5526 -- Docs/researches/math_theorems.md` | 0 | Post-problem and adjacent Friedberg-Muchnik rows originate at commit `bcf3f9fa...` |
| exact source-discovery commands in the block below | 0 | Post bibliography confirmed; official full-text attempts returned HTML; secondary standard question/solution lead located; observational hashes recorded below |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; package status empty |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0748/IntakeProbe.lean)` | 0 | ten adjacent APIs and an abstract order shape elaborated; stdout SHA-256 `6d773b60...db84`; no theorem or proof |
| exact bounded declaration-search command below | 1 | expected no match; intake discovery only, not an exhaustive anchor audit or global absence claim |
| `for f in Stage1_Instances/THM-M-0748/*.json .stage1-worker-selftest.json; do python3 -m json.tool "$f" >/dev/null || exit; done` | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0748-pycache python3 -m py_compile Stage1_Instances/THM-M-0748/check_intake.py` | 0 | validator syntax valid; no owned generated file |
| `python3 -B Stage1_Instances/THM-M-0748/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, planned H1/M4/R4 boundary, null target, exact inventory, hashes, packet, and six open tasks agree |
| prohibited Lean proof-escape scan over `Stage1_Instances/THM-M-0748` | 1 | expected no match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| exact tracked and untracked whitespace command below | 0 | no whitespace diagnostics; each no-index status 1 was only the expected new file difference |

The network source discovery was performed before the network-denied validation recipes were
frozen. The exact commands were:

```bash
mkdir -p /tmp/thm-m-0748-source
curl -L --fail --max-time 30 -sS 'https://api.crossref.org/works/10.1090/S0002-9904-1944-08111-1' -o /tmp/thm-m-0748-source/crossref-post.json
wc -c /tmp/thm-m-0748-source/crossref-post.json
sha256sum /tmp/thm-m-0748-source/crossref-post.json
jq '.message | {title,author,published,volume,issue,page,DOI,URL,link}' /tmp/thm-m-0748-source/crossref-post.json

curl -L --fail --max-time 60 -A 'Mozilla/5.0' -sS 'https://www.ams.org/bull/1944-50-05/S0002-9904-1944-08111-1/S0002-9904-1944-08111-1.pdf' -o /tmp/thm-m-0748-source/post-ams.pdf
file /tmp/thm-m-0748-source/post-ams.pdf
wc -c /tmp/thm-m-0748-source/post-ams.pdf
sha256sum /tmp/thm-m-0748-source/post-ams.pdf

curl -L --fail --max-time 60 -sS 'https://projecteuclid.org/download/pdf_1/euclid.bams/1183505800' -o /tmp/thm-m-0748-source/post-euclid.pdf
file /tmp/thm-m-0748-source/post-euclid.pdf
wc -c /tmp/thm-m-0748-source/post-euclid.pdf
sha256sum /tmp/thm-m-0748-source/post-euclid.pdf

curl -L --fail --max-time 60 -sS 'https://plato.stanford.edu/entries/recursive-functions/' -o /tmp/thm-m-0748-source/sep.html
rg -n -C 4 'Post.?s Problem|Theorem 3.8|Friedberg|Muchnik' /tmp/thm-m-0748-source/sep.html
wc -c /tmp/thm-m-0748-source/sep.html
sha256sum /tmp/thm-m-0748-source/sep.html
```

Results: the Crossref response was 2143 bytes with SHA-256
`efa22b14262b802773343f95d50fa92f563a35746237355f982483e738bd48d0`; the AMS response was a
919911-byte HTML page, not a PDF; the Project Euclid response was a 1053-byte HTML access page; and
the Stanford Encyclopedia response was 299541 bytes with SHA-256
`5fa44199c0133e1382ef9bd1dcc0ab8e447c0ebf9b33b39a75b129d1cd27a6d7`. These temporary responses
are not archived, accepted primary evidence, or inputs to a network-denied validation recipe.

The exact bounded declaration search was:

```bash
rg -n -i --glob '*.lean' 'post.?s[ _-]*problem|friedberg|muchnik|intermediate[ _-]*(turing[ _-]*)?degree|turing[ _-]*degree.*intermediate' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems
```

It exited 1 with no output, as expected. The exact whitespace command was:

```bash
git diff --check -- Stage1_Instances/THM-M-0748 .stage1-worker-selftest.json
rc=$?
for f in .stage1-worker-selftest.json Stage1_Instances/THM-M-0748/*; do
  out=$(git diff --no-index --check /dev/null "$f" 2>&1)
  x=$?
  test -z "$out" || { printf '%s\n' "$out"; rc=1; }
  test "$x" -eq 0 -o "$x" -eq 1 || rc=1
done
echo "whitespace_exit=$rc"
exit "$rc"
```

Known downstream failures remain deliberately open: immutable primary question and solution
passages with exact premises, conclusions, proof boundaries, translations, corrections, errata,
and independent review; the omitted c.e. and Turing qualifiers; exact representative, endpoint,
strict-order, quotient and set/oracle transports; canonical Lean elaboration, expression and
environment fingerprints, checked alternate encodings and mutations; immutable anchor audit;
discovery and obligation freezes; proof and composition; trust closure; readable reconstruction;
hermetic replay; deterministic evidence bundle; independent verification; release; and master
acceptance. These block ordinary theorem execution and completion but not a truthful, self-tested
`planned` intake.
