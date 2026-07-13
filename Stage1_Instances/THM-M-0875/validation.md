# THM-M-0875 intake validation

## Scope

This record validates only the `planned` dossier, scope map, source-statement crosswalk, open task
DAG, bounded historical-source observations, and discovery-only pinned Lean API probe. It does not
validate an exact Weisfeiler-Leman proposition, an algorithm implementation, correctness,
completeness, stabilization, complexity, proof, accepted receipt, audit completion, or theorem
completion.

The worker tree was nonrelease-dirty throughout: the canonical `.lake` link was already untracked,
and this intake's owned artifacts plus the root self-test packet were new. No dependency content,
authority file, generated checklist, execution-DAG state, or other target path was modified. The
automation-provided canonical `.lake` link was used read-only; no update, build, clone, fetch, or
other dependency mutation was performed.

## Environment

- Repository base: `748243faadc15828fb087059337fd05b7be9fdeb`
- Base tree: `e46d642646f80980838b6f016f5d69b817bd464d`
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- Lake: `5.0.0-src+98dc76e`
- mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- mathlib tree: `bdc39a3123201dae413a9d9be56ec242c19e5c2b`
- Platform: Linux `7.0.0-27-generic`, `x86_64`
- Timezone/date: Asia/Shanghai, 2026-07-13
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`

The translation, original scan, and conference preface linked by the University of West Bohemia's
WL2018 page were observed through bounded HTTP requests. Their SHA-256 values were respectively
`4dd47b0568910d2ccb787b192a870aeeb9a2b7802dff54d92486d2f3181a55af`,
`3bb783bde4360767e73e0a349dae88eb24d1904808609fd3c0ff566b113ef93c`, and
`ed622e1e5d65c14d13643e9a22f37e23821bb82772a408b79ead36b2afacd4a6`. No external
source was vendored. These dated network observations are source-family discovery and correction
boundary evidence, not replay-stable H0 evidence or a selected statement.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0875` | 0 | rank 1429, planned, L0/rework_required, no legacy slot, theorem_complete false |
| `git status --short --untracked-files=all` at preflight | 0 | only the pre-existing untracked canonical `.lake` link existed before this intake; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 6411,6416 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded downloads of WL2018 translation, original scan, and preface; `file`, `wc -c`, `pdfinfo`, `pdftotext`, and `sha256sum` | 0 | 11-page 288,939-byte translation, 5-page 336,334-byte scan, and 17,781-byte preface inspected; digests recorded above; preface says generic completeness conjectures were incorrect |
| bounded exact-topic search over repo-local Lean and pinned mathlib | 1 expected | no Weisfeiler/Leman spelling, color-refinement, `1-WL`, or `k-WL` implementation/theorem matched; intake discovery only, not an absence proof |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | pinned versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` before and after probe | 0 | empty output; pinned package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0875/IntakeProbe.lean` | 0 | eleven adjacent pinned APIs elaborated; two axiom reports contain only `propext` and `Quot.sound`; no target theorem introduced; exact output SHA-256 `22b76ee58a5c2077bcef600a5fc4d877a8cf2aadf08d7046cec5e94a86d7ef9a` |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 after finalization | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0875-pycache python3 -m py_compile Stage1_Instances/THM-M-0875/check_intake.py` | 0 | scoped validator compiles without writing cache files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0875/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 after finalization | authorities, target/DAG identity, null target, H5/M4/R4 boundary, pins, artifact hashes, receipt/packet, and six open tasks agree |
| prohibited-declaration scan of `IntakeProbe.lean` | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| wrapper running `git diff --check`, then `git diff --no-index --check /dev/null <file>` for every new file and accepting only exit 1 with empty diagnostics | 0 aggregate | tracked check exited 0; each no-index check exited 1 only because the new file differs from `/dev/null`; all diagnostic streams were empty |

The structural, Lean, JSON, scoped-checker, prohibited-construct, and whitespace commands were
rerun after final artifact serialization.

## Known failures and boundary

Master acceptance is pending. The algorithm-family gloss still lacks a selected exact proposition.
Primary-source admission, publication/edition and translation review, pinpoint definition and
statement/proof/correction mapping, independent Weisfeiler-Leman review, neighboring-target
reconciliation, formal target and mutation certificate, exhaustive anchor audit, obligation
registry, typed graphs, proof, composition, trust closure, readable reconstruction, hermetic
replay, deterministic bundle, and independent verification remain open.

Verdict: `no_state_change`. This self-tested worker proposal may be handed off as `[_]`; it remains
unfinished and unaccepted. `audit_complete=false` and `theorem_complete=false`.
