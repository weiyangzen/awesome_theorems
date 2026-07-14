# THM-M-0554 proof-phase recheck: blocked

Item: `S56-M-0554-PROOF`

Attempt: `2026-07-15T06:06:29+08:00`

Base revision: `9293a4d141848287a1f656eefe9929eb30465393`

Base tree: `63616ff5bc0e58e05d2eb66cff302101ea0c2fa0`

## Verdict

`blocked`. No genuine Atiyah-Hirzebruch spectral-sequence proof body was
implemented or found in the pinned dependency closure. The exact root remains
`M4`; this attempt adds no proof receipt, composition certificate, debt-vector
change, or state transition.

The immediate root cut remains:

- `M0554-X-GENCOH`: generalized-cohomology pair, excision, and wedge infrastructure;
- `M0554-C-EXACT-COUPLE`: the skeletal-filtration exact-couple construction;
- `M0554-C-E2-MODEL`: the cellular-cohomology `E2` identification;
- `M0554-L-STRONG`: strong convergence for the finite skeletal filtration.

Pinned mathlib supplies generic spectral-sequence, CW-complex, and singular-
homology substrate only. A current-head search of every pinned package found no
AHSS, generalized-cohomology, exact-couple, or strong-convergence proof body.
Mathlib's spectral-object file still documents its intended `spectralSequence`,
`homologyData`, and `spectralSequenceHomologyData` constructions as `TODO`.

## First Failed Gate

Exact-statement fidelity fails before a proof can be credited. The canonical
claim requires a reduced generalized cohomology theory and a genuine finite-CW
structure, but reducedness is absent from the frozen interface. In
`Statement.lean`, the theory facts `pointIsPoint`, `exactnessAxiom`, and
`wedgeAxiomOrRepresentability`, and the CW facts `finiteCW`, `exhaustive`, and
`cellAttachments`, are proposition-valued data rather than required proofs.
The output chooses the meanings of `coefficientConvention`,
`strongConvergence`, and `naturalityInSpace`, while
`filtrationIsInducedBy` is only `K.skeleton = K.skeleton`.

Consequently the literal proposition admits a zero spectral-sequence
inhabitant using zero objects, reflexive isomorphisms, and output-selected
`True` propositions. The unchanged-source blocker lineage contains a
trust-level-zero disposable elaboration of that candidate. It is deliberately
not retained or credited: it constructs no AHSS, closes none of the four
root-cut packages, and supplies no checked child-to-parent composition
certificate. Retaining it would be a fake result and violate exact-statement
fidelity and the no-substitution rule.

Predecessor authority is also unresolved. The global obligation-tree item is
only provisional (`[_]`). In the dossier, `instance.json` still records a null
canonical module, expression, expression hash, and environment fingerprint
with status `open_statement_phase`. `task-dag.json` remains unfrozen, leaves
statement/source/tree open, and marks proof blocked by predecessors. In
addition, `statement.json` attributes convergence fields to the legacy
`AtiyahHirzebruchConvergenceData` declaration instead of the canonical owned
source's `Stage1.THM_M_0554.AtiyahHirzebruchData`. A proof-only worker cannot
silently replace or reconcile those predecessor artifacts.

The structured intake authority records root readability at `R3`, whereas the
existing proof-blocker lineage classifies the materially misleading statement
surface at `R4`. Under the weaker-status-wins rule this recheck conservatively
reports `R4`, but the disagreement itself remains an unreconciled authority
defect rather than an accepted state change.

## Validation

All Lean commands reused the automation-provided symlink to the canonical
pinned `.lake` artifacts. No update, build, dependency clone/fetch, network
action, or `.lake` mutation was performed. Generated Lean output was placed in
a temporary directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | 32 obligations and 91 typed edges passed; denominator `3c72072a...8048b`; root remains M4 without a composition certificate. |
| Isolated resolved `lean --trust=0 -t0 -R "$target" -o "$tmp/Statement.olean" Statement.lean` invocation in the exact recipe below | 0 | The frozen target elaborated with Lean 4.29.0; the temporary object was 429072 bytes and was removed. |
| `rg -n -i --glob '*.lean' 'Atiyah[-_ ]?Hirzebruch\|AtiyahHirzebruch\|\bAHSS\b\|generalized[ _-]*(co)?homology\|exact[ _-]*couple\|strong[ _-]*convergence' Formalizations/Lean/.lake/packages` | 1 | Expected no-match result: no pinned terminal proof candidate was found. |
| The same query over repo-local Lean outside the dossier and pinned cache | 0 | Target-specific hits were the legacy `S1_M_106.lean` interfaces and blocker gates, not a terminal proof body. |
| `rg -n --pcre2 '^\s*(?:sorry\|admit\|axiom)(?:\s\|$)\|\bsorryAx\b\|^\s*unsafe(?:\s\|$)' Stage1_Instances/THM-M-0554 --glob '*.lean'` | 1 | Expected no-match result: no prohibited declaration token occurs. |
| Pinned Lean/Lake and mathlib revision/tree checks | 0 | Lean `4.29.0` commit `98dc76e...16740`; Lake `5.0.0-src+98dc76e`; mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`; mathlib source tree clean. |
| Spectral-object source hash and `TODO` scan | 0 | SHA-256 `2ce62b9d...740aa`; the intended spectral-sequence and homology-data constructors remain documented as `TODO`. |
| `jq empty Stage1_Instances/THM-M-0554/*.json` | 0 | Every owned structured JSON artifact, including this record, parsed. |
| Scoped `jq -e` assertions over this blocker packet | 0 | Identity, base revision/tree, blocked boundary, false completion flags, and the exact four-member root cut agree. |
| `git diff --check -- Stage1_Instances/THM-M-0554 .stage1-worker-selftest.json` | 0 | No tracked whitespace diagnostics. |
| `git diff --no-index --check /dev/null` for each new artifact | 1 | Expected content-difference status with no whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The self-test manifest is absent because the proof phase is blocked. |

The isolated target-elaboration recipe was:

```bash
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0554
tmp=$(mktemp -d /tmp/thm-m-0554-slot21-replay.XXXXXX)
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean" --trust=0 \
  -t0 -R "$target" -o "$tmp/Statement.olean" Statement.lean
rc=$?
size=$(stat -c %s "$tmp/Statement.olean" 2>/dev/null || printf absent)
rm -rf "$tmp"
printf 'Statement.lean trust-zero elaboration exit=%s; temporary olean size=%s; scratch removed\n' \
  "$rc" "$size"
exit "$rc"
```

## Retry Condition

First publish and master-accept a source-faithful corrected statement,
reconcile the instance, task, and statement projections, and issue obligation-
registry version 2. Then implement and compose all four root-cut packages
without placeholders. An alternative is an immutable exact compatible Lean 4
AHSS proof that can be pinned, exact-type transported, and checked with
complete provenance, trust, and composition closure.

This artifact is durable blocker evidence only. It does not satisfy
`S56-M-0554-PROOF`, close an obligation, complete the audit or theorem, or
authorize master acceptance. Because the assigned phase is not genuinely
self-tested as complete, `.stage1-worker-selftest.json` remains absent.
