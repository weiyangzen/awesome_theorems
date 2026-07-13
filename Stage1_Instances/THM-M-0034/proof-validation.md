# THM-M-0034 proof-phase attempt

Item: `S56-M-0034-PROOF`

Date: `2026-07-13` (`Asia/Shanghai`)

Base revision: `0d2c3bdcd192266bc255ac3d5186da604517145a`

## Verdict

`blocked`: the exact external body was independently replayed, but it cannot be placed in this
repository's proof closure without a license grant. The immutable archive for
`edmund-ukaisi/QuillenSuslin@e8d85a6f6fa210ba0be12bd02aa22009699f0c35` contains no `LICENSE`,
`COPYING`, `NOTICE`, or other permission artifact. It is also absent from the pinned Lake dependency
graph. The repository rules make unresolved licensing an integration blocker, so none of its source
was copied into the owned path and no dependency was added or fetched.

This is a legal/provenance blocker, not a failed mathematical or Lean proof. An existing immutable
archive and extracted source were available in `/tmp` from the prerequisite audit. Using only the
canonical pinned mathlib artifacts, all 53 source modules in the transitive closure of
`QuillenSuslin.Theorem` elaborated from source into a fresh temporary output tree. The exact wrapper

```lean
theorem quillenSuslinTarget : QuillenSuslinTarget.{u, v} := by
  intro k _ n _ P _ _ _ _
  exact QuillenSuslin.quillenSuslin n P
```

also elaborated. Lean reported exactly `propext`, `Classical.choice`, and `Quot.sound` for both the
external theorem and the wrapper. The upstream lexer-aware scan reported zero live `sorry`, `#exit`,
`native_decide`, or `axiom` tokens across all 76 production files. These temporary checks establish
technical feasibility and strengthen the candidate evidence; they do not pin/import/vendor a proof,
do not close `M0034-X-EXTERNAL-BODY`, and do not justify an `M0-P` or theorem-completion claim.

Because the assigned proof deliverable is incomplete, `.stage1-worker-selftest.json` is deliberately
absent. The root remains `[H1, M3, R4]`; `M0034-X-LICENSE` and
`M0034-X-EXTERNAL-BODY` remain the first cut set.

## Narrow validation evidence

All repository commands ran in this worker clone. The external replay wrote only below `/tmp` and
read the automation-provided canonical `.lake` symlink; it did not run `lake update`, `lake build`,
clone, fetch, checkout, or any command that modified `.lake`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0034` | 0 | Rank 1078; planned; `L0/rework_required`; theorem incomplete. |
| `sha256sum /tmp/m0034-edmund.tar.gz` | 0 | `6072221d080e634f0a9775518855557fce0495cf4004848e4cb57dda4aa7e6d2`; exact audited archive, 1,822,376 bytes. |
| `tar -tzf /tmp/m0034-edmund.tar.gz | rg '/(LICENSE\\|COPYING\\|NOTICE)(\\.\\|$)'` | 1 | Expected no-match result: no license artifact in the archive. |
| `cd /tmp/m0034-edmund-src/lean && ./scripts/sorries` | 0 | `Summary: 0 sorry, 0 #exit, 0 native_decide, 0 axiom`; scanner SHA-256 `824050a90789252b5aa195ce57e43fb432f8addb2535cb9d801006f27e4a65fc`. |
| Fresh 53-module source replay described below | 0 for every module | `QuillenSuslin.Theorem` rebuilt from the immutable source against pinned mathlib; `Theorem.olean` SHA-256 `792186c7df750895f1e76f58c432799b02e36f91f5c7b46e30d4afb620fbd3ea`. |
| Exact statement/wrapper replay described below | 0 each | Canonical `Statement.lean` and exact `quillenSuslinTarget` wrapper elaborated; wrapper output SHA-256 `cb19136bb2f69b9ab349230a647ade69be6e72a94d5792e0988f24a382e35e8c`; both axiom probes reported only the accepted three axioms. |
| `python3 -m json.tool Stage1_Instances/THM-M-0034/proof-blocker.json >/dev/null` | 0 | Structured blocker parses. |
| `rg -n '\\b(sorry\\|admit\\|sorryAx)\\b\\|^[[:space:]]*(axiom\\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0034 -g '*.lean'` | 1 | Expected no-match result: no prohibited Lean proof escape in the owned source. |
| `git diff --check -- Stage1_Instances/THM-M-0034` | 0 | No scoped whitespace diagnostics. |

The replay used a 53-module topological order generated deterministically from the immutable import
graph during this attempt. From `Formalizations/Lean`, each source was checked separately with:

```bash
base=$(lake env printenv LEAN_PATH)
while read -r mod; do
  src=/tmp/m0034-edmund-src/lean/${mod//.//}.lean
  out=/tmp/m0034-research-fromsource/${mod//.//}.olean
  mkdir -p "$(dirname "$out")"
  LEAN_PATH="/tmp/m0034-research-fromsource:$base" lake env lean \
    -DmaxHeartbeats=0 -DsynthInstance.maxHeartbeats=0 \
    -DmaxSynthPendingDepth=3 -DrelaxedAutoImplicit=false \
    --root=/tmp/m0034-edmund-src/lean "$src" -o "$out"
done < /tmp/m0034-research-order.txt
```

The order contains 53 unique modules and has SHA-256
`c3a49d5613e7081a6c7112bf14a89dac0d1ee3a9400fd26847b4bbf44632ac44`; its
per-source SHA-256 inventory has digest
`470c24c9891b6c8985971367d9061fafbb19d14daf09b9b0c4f698f1d2cb3a1d`.
The exact wrapper then imported the fresh `QuillenSuslin.Theorem` object and the separately compiled
canonical `Statement.olean` through an explicit temporary `LEAN_PATH`.

## Reopen condition

Obtain a license grant compatible with pinning or vendoring the exact immutable commit, then add its
53-module theorem closure to the repository validation closure and replay this exact wrapper. An
independent repo-local proof of the frozen target would also reopen the node. Until then proof,
validation, release, master acceptance, `AUDIT-Z`, and theorem completion remain open.
