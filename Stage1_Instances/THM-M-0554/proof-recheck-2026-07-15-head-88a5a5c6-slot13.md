# THM-M-0554 proof phase blocked at `88a5a5c6`

Item: `S56-M-0554-PROOF`

Recheck time: `2026-07-15T19:50:07+08:00`

Base revision: `88a5a5c6fe6bac0d813a74ca20fa553eaf2a6d68`

Base tree: `a0a75048a918a3bf566c3dbcf6b4352c3b2ee8e4`

## Verdict

`blocked`. No source-faithful Atiyah-Hirzebruch spectral-sequence proof body
exists in the repository or pinned dependency closure. No proof body, frozen
node closure, composition certificate, proof receipt, debt-vector change, or
item-state transition is proposed. The root remains `[H3, M4, R4]`.

The first failed gate is
`S56-5.1-EXACT-TARGET-CONSISTENCY / M0554-S-DATA`. The literal Lean interface
can be inhabited without constructing the canonical mathematical AHSS. A
fresh temporary trust-zero probe chose zero page complexes, defined
`ordinaryCohomology` from an arbitrary zero object, used unrelated zero
objects for the filtration families, and selected `True` for the output
propositions. The exact literal root declaration elaborated, was sorry-free,
and reported only `propext`, `Classical.choice`, and `Quot.sound`.

That probe was deleted and receives no proof credit. It did not identify
`E2^{p,q}` with `H^p(X; E^q(pt))`, construct the skeletal filtration, prove
strong convergence, or establish naturality. Retaining it would be a fake
result and would bypass the required children in the frozen proof graph.

The defect is structural: reducedness is absent; `pointIsPoint`,
`exactnessAxiom`, `wedgeAxiomOrRepresentability`, `finiteCW`, `exhaustive`,
and `cellAttachments` are proposition-valued data rather than evidence;
`ordinaryCohomology` is unconstrained; `coefficientConvention`,
`strongConvergence`, and `naturalityInSpace` are output-selected propositions;
and `filtrationIsInducedBy` is only `K.skeleton = K.skeleton`.

The existing `Proof.lean` declarations are valid placeholder-free conditional
composition bodies. `statementOfBranchFamily` assumes the complete E2,
differential, convergence, and naturality family, so it constructs none of the
missing branches and cannot close their parent.

The genuine mathematical root cut remains:

- `M0554-X-GENCOH`: generalized-cohomology pair, excision, and wedge infrastructure;
- `M0554-C-EXACT-COUPLE`: the skeletal-filtration exact-couple construction;
- `M0554-C-E2-MODEL`: the cellular-cohomology E2 identification;
- `M0554-L-STRONG`: strong convergence for the finite skeletal filtration.

Pinned mathlib contains generic spectral-sequence, CW, and singular-homology
substrate only. Its spectral-object module still documents the intended
`spectralSequence`, `homologyData`, and `spectralSequenceHomologyData`
constructors as `TODO`. The legacy `S1_M_106.lean` file and analogous spectral
sequence targets expose interfaces and explicit debt gates, not a terminal
AHSS proof.

Predecessor authority independently blocks acceptance. The global obligation-
tree item is provisional `[_]`; `instance.json` remains `planned` with null
formal identity fields; and the local `task-dag.json` is unfrozen and marks
`PROOF` as `blocked_by_predecessors`.

At worker start, this target contained 43 prior tracked proof JSON/Markdown
pairs while scheduler authority still recorded zero attempts and no children.
Those files are not an authoritative tick ledger, but repeated unchanged
dispatch is far beyond the five-unresolved-tick split threshold. Integration
must reconcile that ledger and redirect execution to statement repair rather
than schedule the unchanged proof root again.

## Validation

All Lean checks reused the automation-provided read-only symlink to canonical
pinned Lake artifacts. No `lake update`, `lake build`, dependency clone/fetch,
network action, checkout, or `.lake` mutation occurred. Generated objects and
the rejected diagnostic source lived under `/tmp` and were removed. The
untracked symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | `PASS`: 32 obligations and 91 typed edges; denominator `3c72072a...8048b`; root remains open at `M4` with no composition certificate or proof closure. |
| Isolated `lake env lean --trust=0 -t0` replay of `Statement.lean`, `Proof.lean`, and `DifferentialProbe.lean` | 0 | Objects were 429072, 280728, and 15576 bytes. Output hashes were `f1690fd1...d30`, `8cfbfe08...2a1`, and `30cba6d3...156`. The conditional proof declarations were sorry-free and reported exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Isolated trust-zero temporary statement-defect probe | 0 | The 45216-byte object had SHA-256 `bfa7b4bc...7869`; output SHA-256 `4e5cbf6c...bd84`. Its exact literal root was sorry-free and reported only `propext`, `Classical.choice`, and `Quot.sound`. The source and object were deleted and are not credited. |
| Scoped prohibited-declaration scan | 1 | Expected no-match: no placeholder, bodyless declaration, unsafe declaration, `implemented_by`, `extern`, or `native_decide` occurs in owned Lean sources. |
| Pinned-package AHSS/generalized-cohomology/exact-couple/convergence scan | 1 | Expected no-match: zero source lines; no terminal proof candidate. |
| Equivalent repo-local scan outside this dossier and `.lake` | 0 | 159 source lines; target-specific hits are legacy interfaces and blocker gates, not a terminal body. |
| Lean/Lake and manifest package audit | 0 | Lean `4.29.0` commit `98dc76e...16740`; Lake `5.0.0-src+98dc76e`; all 11 package worktrees clean at recorded revisions; mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`. |
| SHA-256 and `TODO` scan of mathlib spectral-object source | 0 | SHA-256 `2ce62b9d...740aa`; all three intended constructors remain documented as `TODO`. |
| `git diff --quiet 8b931195...HEAD --` over ten proof-relevant inputs | 0 | No proof-relevant source or structured-input delta. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion self-test manifest is absent because the proof phase is blocked. |

The exact isolated Lean recipe was:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-0554
lean_root=$repo/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0554-defect-slot13-88a5a5c6.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
base_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cp /tmp/StatementDefectProbe-slot13.lean "$tmp/StatementDefectProbe.lean"
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" timeout --foreground 300 \
  "$lean" --trust=0 -t0 -R "$target" -o "$tmp/Statement.olean" \
  Statement.lean >"$tmp/statement.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" timeout --foreground 300 \
  "$lean" --trust=0 -t0 -R "$target" -o "$tmp/Proof.olean" \
  Proof.lean >"$tmp/proof.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" timeout --foreground 300 \
  "$lean" --trust=0 -t0 -R "$target" -o "$tmp/DifferentialProbe.olean" \
  DifferentialProbe.lean >"$tmp/differential.log" 2>&1
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_path" timeout --foreground 300 \
  "$lean" --trust=0 -t0 -o "$tmp/StatementDefectProbe.olean" \
  StatementDefectProbe.lean >"$tmp/defect.log" 2>&1
wc -c "$tmp/Statement.olean" "$tmp/Proof.olean" \
  "$tmp/DifferentialProbe.olean" "$tmp/StatementDefectProbe.olean"
sha256sum "$tmp/Statement.olean" "$tmp/Proof.olean" \
  "$tmp/DifferentialProbe.olean" "$tmp/StatementDefectProbe.olean" \
  "$tmp/statement.log" "$tmp/proof.log" "$tmp/differential.log" \
  "$tmp/defect.log" "$tmp/StatementDefectProbe.lean"
cat "$tmp/statement.log" "$tmp/proof.log" "$tmp/differential.log" \
  "$tmp/defect.log"
```

The defect-probe source was written only to `/tmp`; its SHA-256 was
`c25f6bae...aa02`, and it was deleted after the run. The exact bounded search
and hygiene commands were:

```bash
rg -n -i --glob '*.lean' \
  'Atiyah[-_ ]?Hirzebruch|AtiyahHirzebruch|\bAHSS\b|generalized[ _-]*(co)?homology|exact[ _-]*couple|strong[ _-]*convergence' \
  Formalizations/Lean/.lake/packages
rg -n -i --glob '*.lean' --glob '!Stage1_Instances/THM-M-0554/**' \
  --glob '!Formalizations/Lean/.lake/**' \
  'Atiyah[-_ ]?Hirzebruch|AtiyahHirzebruch|\bAHSS\b|generalized[ _-]*(co)?homology|exact[ _-]*couple|strong[ _-]*convergence' .
rg -n --pcre2 --glob '*.lean' \
  '^\s*(?:sorry|admit|axiom|constant|opaque)(?:\s|$)|\bsorryAx\b|^\s*unsafe(?:\s|$)|\bimplemented_by\b|^\s*extern(?:\s|$)|\bnative_decide\b' \
  Stage1_Instances/THM-M-0554
```

Pinned identities: Lean binary SHA-256 `3e0d0d3d...28bbf`, Lake manifest
SHA-256 `321626c8...2d81`, and `lean-toolchain` SHA-256
`651c8acc...5b1d2`. `Statement.olean`, `Proof.olean`, and
`DifferentialProbe.olean` had SHA-256 values `46d2fc1b...9ded`,
`dc72a4c9...30c6`, and `a159b12b...fca9`.

## Retry Condition

Do not reschedule the unchanged proof root. Publish and master-accept a
source-faithful statement that encodes reducedness, inhabited theory/CW
hypotheses, actual ordinary cohomology coefficients, filtration provenance,
convergence, and naturality. Reconcile instance/task/statement authority and
issue obligation-registry version 2 with exact branch fingerprints. Then
implement the genuine four-package root cut. Alternatively, pin an immutable
exact compatible Lean 4 AHSS proof and pass canonical mapping, provenance,
trust, and composition gates.

This packet is blocker evidence only. It does not satisfy
`S56-M-0554-PROOF`, close an obligation, complete the audit or theorem, or
authorize validation, release, or master acceptance. Because the proof phase
is incomplete, `.stage1-worker-selftest.json` remains absent.
