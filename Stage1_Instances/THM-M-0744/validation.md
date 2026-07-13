# Intake validation

Base revision: `0e5ae82e6d507ee607c3f011900571ffd8096800` (tree
`400e6edf1f69b971b60a367e3ea29be359b07907`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, source and duplicate boundaries,
the source-statement crosswalk, all-open downstream DAG, JSON and scoped invariants, and a narrow
pinned Lean candidate probe. It does not validate a canonical mathematical or Lean statement and
does not claim proof credit. The automation-provided canonical `.lake` symlink was pre-existing and
used read-only; no update, build, clone, fetch, or other dependency mutation was performed. This
dirty worker evidence is nonrelease evidence.

## Source discovery boundary

The immutable Spring 2024 Stanford Encyclopedia of Philosophy archive was retrieved to temporary
storage, hashed, and inspected at Section 3.1, Theorem 3.1. It supplies a standard exact
all-arities statement with a primitive-recursive natural-index transformer. Crossref metadata for
Kleene's 1943 paper was also retrieved and hashed. The SEP theorem is not attributed there to the
1943 paper, and the version-of-record PDF request returned HTTP 429. Thus the primary theorem
passage, definitions, proof, source identity, corrections, and errata remain uninspected. No H0
claim is made.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; its package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Pinned `PartrecCode.lean` SHA-256:
  `543fdfc34bbc62e0d2bdff524be58e58abdd4ebded0ca25fac7edf791aadb2df`.

## Commands and results

All repository commands ran at the repository root unless `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0744` | 0 | rank 1331; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 5486,5491 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded inspection of the catalog, Stage0 projections, manifest/checklist/DAG rows, and neighboring recursion-theory records | 0 | confirmed the sparse parameter-theorem wording, outside-scope duplicate gloss, and separate recursion/fixed-point ownership |
| `curl -L --fail --max-time 60 -A 'Mozilla/5.0' -sS 'https://plato.stanford.edu/archives/spr2024/entries/recursive-functions/' -o /tmp/thm-m-0744-sep-spr2024.html` | 0 | immutable secondary archive retrieved; 299572 bytes; SHA-256 `7d856ecd...af1` |
| scoped `rg` inspection of SEP Section 3.1, Theorem 3.1 | 0 | observed the all-`n,m` primitive-recursive natural-index statement and its argument-specialization explanation |
| `curl -L --fail --max-time 60 -A 'Mozilla/5.0' -sS 'https://api.crossref.org/works/10.1090/S0002-9947-1943-0007371-8' -o /tmp/thm-m-0744-kleene-crossref.json` | 0 | confirmed Kleene, title, 1943, Transactions AMS 53(1), pages 41-73, DOI; response SHA-256 `8883e905...be0`; metadata only |
| `curl -L --fail --max-time 90 -A 'Mozilla/5.0' -sS 'https://www.ams.org/tran/1943-053-01/S0002-9947-1943-0007371-8/S0002-9947-1943-0007371-8.pdf' -o /tmp/thm-m-0744-kleene-1943.pdf` | 22 (expected blocker) | HTTP 429; no primary document accepted and no theorem/page/proof claim made |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}' 'HEAD:Mathlib/Computability/PartrecCode.lean'` | 0 | pinned revision/tree and source blob `6a5a8cd7a1819f65ca068a13e8216714fa9c9401` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short --untracked-files=all` | 0 | empty output; dependency worktree remained clean |
| `sha256sum` over the authority inputs, toolchain lock, and pinned candidate source | 0 | hashes recorded in `instance.json` and `intake-receipt.json` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | pinned Lean and Lake versions recorded above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0744/IntakeProbe.lean)` | 0 | Code/curry/eval, computability predicates, primitive-recursive witness, semantic lemma, and `smn` types elaborated; `smn` reported `propext`, `Classical.choice`, and `Quot.sound`; no target or wrapper declared |
| `rg -n --glob '*.lean' 'Nat.Partrec.Code.smn|S.?m.?n theorem|parameter theorem' Formalizations/Lean/AwesomeTheorems` | 1 (expected no match) | no repo-local exact target artifact found; bounded intake discovery, not exhaustive anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 each | all finalized structured records valid |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0744-pycache python3 -m py_compile Stage1_Instances/THM-M-0744/check_intake.py` | 0 | scoped checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0744/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, planned lifecycle, null target, H1/M4/R4 boundary, input hashes, candidate/duplicate inventories, receipt packet, artifact inventory, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0744/check_intake.py` | 0 | public replay mode passes without the scheduler-only worker packet and permits authoritative intake state `[ ]` or `[_]` |
| `rg -n --glob '*.lean' '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0744` | 1 (expected no match) | no prohibited Lean proof escape or declaration |
| per-new-file `git diff --no-index --check /dev/null FILE`, then `git diff --check -- Stage1_Instances/THM-M-0744 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics; no-index exit 1 for a new file was treated as normal only when output was empty |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0744-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Primary-source identity and independent review,
canonical natural-index/code and arbitrary-arity/packed-unary reconciliation, exact target and
mutation tests, anchor audit, discovery and obligation freezes, typed graphs, proof and composition
provenance, trust closure, readable reconstruction, hermetic replay, deterministic release bundle,
independent verification, and master acceptance remain open. These gates prevent theorem
completion but do not invalidate the planned intake.
