# THM-M-0554 proof-phase recheck: blocked

Item: `S56-M-0554-PROOF`

Attempt: `2026-07-15T08:06:46+08:00`

Base revision: `a9230a2f2eeabee7e39c0a3deb08e27174d17575`

Base tree: `ab8a17b9aa773ce0b8305338f2ca0c66974c1bb6`

## Verdict

`blocked`. No source-faithful Atiyah-Hirzebruch spectral-sequence proof body
was implemented or found in the pinned dependency closure. The exact root
remains `M4`; this attempt adds no proof receipt, closed obligation,
composition certificate, debt-vector change, or state transition.

The eight canonical proof inputs are byte-for-byte unchanged from revision
`6da5c027`, the last revision that changed this target. Intervening commits add
no terminal AHSS declaration or proof body.

The immediate root cut remains:

- `M0554-X-GENCOH`: generalized-cohomology pair, excision, and wedge infrastructure;
- `M0554-C-EXACT-COUPLE`: the skeletal-filtration exact-couple construction;
- `M0554-C-E2-MODEL`: the cellular-cohomology `E2` identification;
- `M0554-L-STRONG`: strong convergence for the finite skeletal filtration.

Pinned mathlib supplies generic spectral-sequence, CW-complex, and singular-
homology substrate only. A current-base scan found no AHSS, generalized-
cohomology, exact-couple, or strong-convergence proof body in any pinned
package. Mathlib's spectral-object source still documents its intended
`spectralSequence`, `homologyData`, and `spectralSequenceHomologyData`
constructors as `TODO`.

## First Failed Gate

Exact-statement fidelity fails before a proof can be credited. The canonical
mathematical claim requires a reduced generalized cohomology theory and a
genuine finite-CW structure, but reducedness is absent from the frozen Lean
interface. In `Statement.lean`, `pointIsPoint`, `exactnessAxiom`,
`wedgeAxiomOrRepresentability`, `finiteCW`, `exhaustive`, and
`cellAttachments` are proposition-valued data rather than evidence. The
output chooses the propositions `coefficientConvention`, `strongConvergence`,
and `naturalityInSpace`, while `filtrationIsInducedBy` is only the tautology
`K.skeleton = K.skeleton`.

Consequently the literal proposition admits a zero spectral-sequence witness
using zero objects, reflexive isomorphisms, and output-selected `True`
propositions. Prior trust-level-zero exploration confirmed that this
diagnostic term elaborates, but it was not retained or credited. It constructs
no AHSS, closes none of the four root-cut packages, and supplies no checked
child-to-parent composition certificate. Retaining it would be a fake result
and would violate exact-statement fidelity and the no-substitution rule.

The retained `DifferentialProbe.lean` body proves only the literal bidegree
relation by `rfl`. Registry v1 makes `M0554-B-DIFFERENTIAL` a nonleaf with a
required edge to the open `M0554-C-SPECTRAL` node. The diagnostic consumes
neither that child nor its conclusion, so it cannot close the frozen branch.

Predecessor authority is also unresolved. The global obligation-tree item is
only provisional (`[_]`). The local intake authority still records a null
canonical formal module, declaration, expression hash, and environment
fingerprint; `task-dag.json` remains unfrozen, leaves statement/source/tree
open, and marks proof blocked by predecessors. A proof-only worker cannot
silently repair or replace these predecessor artifacts.

## Validation

All Lean checks reused the automation-provided symlink to the canonical pinned
Lake artifacts. No update, build, dependency clone/fetch, network action, or
`.lake` mutation was performed. Lean output was written to a temporary
directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | 32 obligations and 91 typed edges passed; denominator `3c72072a...8048b`; root remains `M4` with no composition certificate or proof closure. |
| Isolated resolved `lean --trust=0 -t0 -R "$target" -o "$tmp/Statement.olean" Statement.lean` using the pinned `lake env` executable and `LEAN_PATH` | 0 | The frozen target elaborated with Lean 4.29.0; temporary object was 429072 bytes and was removed. |
| The same isolated pinned invocation for `DifferentialProbe.lean` | 0 | The uncomposed bidegree diagnostic elaborated; `#print axioms` reported `propext`, `Classical.choice`, and `Quot.sound`; temporary object was 15576 bytes and was removed. |
| `rg -n -i --glob '*.lean' 'Atiyah[-_ ]?Hirzebruch\|AtiyahHirzebruch\|\bAHSS\b\|generalized[ _-]*(co)?homology\|exact[ _-]*couple\|strong[ _-]*convergence' Formalizations/Lean/.lake/packages` | 1 | Expected no-match result: no pinned terminal proof candidate was found. |
| The same proof-candidate query over repo-local Lean outside this dossier and `.lake` | 0 | Target-specific matches are the legacy `S1_M_106.lean` interfaces and blocker gates, not a terminal proof body. |
| `rg -n --pcre2 '^\s*(?:sorry\|admit\|axiom)(?:\s\|$)\|\bsorryAx\b\|^\s*unsafe(?:\s\|$)' Stage1_Instances/THM-M-0554 --glob '*.lean'` | 1 | Expected no-match result: no prohibited declaration token occurs in owned Lean sources. |
| Pinned Lean/Lake and mathlib revision/tree/status checks | 0 | Lean `4.29.0` commit `98dc76e...16740`; Lake `5.0.0-src+98dc76e`; mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`; the mathlib source tree was clean. |
| SHA-256 and `TODO` scan of `Mathlib/Algebra/Homology/SpectralObject/SpectralSequence.lean` | 0 | SHA-256 `2ce62b9d...740aa`; the intended constructors remain documented as `TODO`. |
| `git diff --quiet 6da5c027...HEAD --` followed by the eight canonical proof inputs | 0 | The statement, structured statement, anchor audit, registry, typed graphs, validation specs, instance, and local task DAG are unchanged. |
| `python3 -m json.tool` and scoped `jq -e` assertions on the companion JSON | 0 | The packet parsed and its identity, base, blocked state, exact four-node cut, empty closure/change arrays, and false proof/root/theorem/self-test flags agreed. |
| `jq empty Stage1_Instances/THM-M-0554/*.json` | 0 | Every structured JSON artifact in the owned path parsed. |
| `git diff --check -- Stage1_Instances/THM-M-0554 .stage1-worker-selftest.json` plus `git diff --no-index --check /dev/null <new-artifact>` | 0 / 1 expected | No tracked or new-artifact whitespace diagnostic was reported; status 1 for each no-index check denotes content difference. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The self-test manifest is absent because the proof phase is blocked. |

The isolated Lean recipe was:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-0554
lean_root=$repo/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0554-slot6-20260715.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  -R "$target" -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  -R "$target" -o "$tmp/DifferentialProbe.olean" DifferentialProbe.lean
```

## Retry Condition

First publish and master-accept a source-faithful corrected statement,
reconcile the instance/task/statement authorities, and issue obligation-
registry version 2 with corrected branch dependencies. Then implement and
compose the four root-cut packages without placeholders. Alternatively, pin
an immutable exact compatible Lean 4 AHSS proof and pass exact-type,
provenance, trust, and composition checks.

These artifacts are durable blocker evidence only. They do not satisfy
`S56-M-0554-PROOF`, close an obligation, complete the audit or theorem, or
authorize master acceptance. Because the assigned proof phase is not
genuinely self-tested as complete, `.stage1-worker-selftest.json` remains
absent.
