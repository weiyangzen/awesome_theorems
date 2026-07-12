# Intake validation

- Item: `S56-M-1410-INTAKE`
- Base revision: `95073b656f2c285c788e4814325a47fdb4dc1879`
- Base tree: `54d91dc1ea3d413402cc921ad61f7b5ebaaedd13`
- Validation date: 2026-07-12 (Asia/Shanghai)
- Verdict: `no_state_change`; worker state proposed as `[_]`, master acceptance pending

Validation is limited to target membership, manifest consistency, the truthful `planned` dossier,
the target-scoped open DAG projection, source-literal invariants, a narrow pinned Lean API probe,
prohibited-construct hygiene, and whitespace. The repository gloss is not a proposition, so this
does not establish a canonical mathematical claim, exact Lean expression, or proof.

The preflight worktree contained the existing untracked link `Formalizations/Lean/.lake`. It points
to the canonical checkout's pinned artifacts and was used read-only. No `lake update`, `lake build`,
dependency clone/fetch, or other `.lake` mutation was performed. This is nonrelease worker evidence.

Environment fingerprint:

- Platform: Linux `7.0.0-27-generic`, `x86_64`.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`, clean tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- The `.lake` symlink-target text SHA-256 is
  `e8714e9ebb75a5da1eeb16fdb6f50831a6cab29f115df43fa8e7535b38f59826`.

## Commands and results

The canonical `cwd`/`argv`/environment/timeout/network fields and output hashes for normative
worker checks are in `intake-receipt.json`. The human-readable commands below reproduce their
scope; all positive checks exited 0, and both negative searches exited the expected 1.

| Command | Exit | Result |
|---|---:|---|
| `LC_ALL=C TZ=UTC python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `LC_ALL=C TZ=UTC python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `LC_ALL=C TZ=UTC python3 scripts/stage1_target.py show THM-M-1410` | 0 | rank 909; planned; L0/rework_required; legacy artifacts unaccepted; theorem incomplete |
| `git rev-parse HEAD` | 0 | `95073b656f2c285c788e4814325a47fdb4dc1879` |
| cwd `Formalizations/Lean`: `lake env lean --version` | 0 | Lean 4.29.0 at commit `98dc76e3` |
| cwd `Formalizations/Lean`: `lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| cwd `Formalizations/Lean`: `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | mathlib pin `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `python3 -m json.tool Stage1_Instances/THM-M-1410/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1410/task-dag.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1410/intake-receipt.json` | 0 | valid JSON |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | valid JSON |
| `python3 Stage1_Instances/THM-M-1410/check_intake.py` | 0 | IDs, source literals, proposed `[H5,M4,R4]` scope, authoritative DAG projection, receipt boundary, and false completion flags agree |
| cwd `Formalizations/Lean`, env `LC_ALL=C TZ=UTC`: `lake env lean ../../Stage1_Instances/THM-M-1410/IntakeProbe.lean` | 0 | nine adjacent pinned APIs elaborated; no Rokhlin proposition or proof introduced |
| `LC_ALL=C TZ=UTC rg -n -i 'Rokhlin\|Rohlin' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems --glob '*.lean'` | 1 | expected no-match exit; no named candidate found in the bounded search |
| `LC_ALL=C TZ=UTC rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|opaque)[[:space:]]' Stage1_Instances/THM-M-1410 --glob '*.lean'` | 1 | expected no-match exit; no prohibited proof construct |
| `sha256sum Stage1_Instances/THM-M-1410/{README.md,instance.json,scope-map.md,source-statement-crosswalk.md,task-dag.json,IntakeProbe.lean,check_intake.py}` plus the canonical-manifest serialization recorded in `intake-receipt.json` | 0 | seven pre-receipt artifacts individually bound; canonical manifest SHA-256 `7b697c5ffd98c55bbc28699f19601be8a3783b4cdbdee19b246c420333c7f66a` |
| For each path in `.stage1-worker-selftest.json:changed_paths`, run `git diff --no-index --check -- /dev/null PATH`; accept only exit 0/1 with empty diagnostics | 0 | no whitespace diagnostic in any new file |

## Source inspection

These are discovery actions rather than H0 evidence. Exact URLs, split `download_argv` and
`inspection_argv`, hashes, and boundaries are structured in `intake-receipt.json`.

- Weiss publisher PDF: SHA-256
  `ce8ac1bfa65d4b6f924f09eee43246005cf5060a4138749500d6b87935350dcd`; its nine pages were
  converted with `pdftotext -layout`, whose output SHA-256 is
  `3cb362daffcb32388830837efadeaba394bd15c6699f07865a4d339d41c99a66`.
- Bezuglyi-Dooley-Medynets arXiv `math/0410505v2`: PDF SHA-256
  `00ed936da36a28df9bf80e0b95fe6fa25b83b0cd4a13a2ff4c8ca8b17e293155`; extracted-text
  SHA-256 `bbfcf5df035c22b881ecb080188bb02d30f207bd978976a0901229e8a9c97818`.
- Crossref record `https://api.crossref.org/works/10.1090/trans2/049/09`: response SHA-256
  `dab32d70b6087fdede3f4bf52c1b6ebaf05b9554c6488ad34a3844ec9ef0269b`; this confirms
  translation metadata only, not a theorem passage.

## Known downstream failures

- The catalog wording is not a stable proposition. Provisional `H5` is scoped only to that literal
  record and is pending master review. It triggers target correction and an `H` recomputation rather
  than ordinary proof execution.
- No independently reviewed primary theorem passage selects the corrected root. The 1948 short-note
  locator, 1949 survey locator, and measure-preserving/nonsingular formulations remain unreconciled.
- No canonical Lean expression, environment/expression hash, alternate transport, statement
  mutation, discovery protocol, or obligation registry exists.
- Anchor audit, proof architecture, proof, trust/composition checks, readable reconstruction,
  hermetic replay, and independent release verification are all open.
- The repository has no located strict global schema for the established local intake JSON family;
  master framework acceptance remains open, though `check_intake.py` validates target invariants.

These failures prevent source, statement, audit, and theorem-completion claims. They do not
invalidate the self-tested `planned` intake handoff. Its closed-set verdict is `no_state_change`
because only the integration lane may accept the receipt and advance authoritative state.
