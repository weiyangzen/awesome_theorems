# THM-M-0554 proof-phase recheck: blocked

Item: `S56-M-0554-PROOF`

Intent: `prove`

Recheck time: `2026-07-15T15:13:00+08:00`

Base revision: `88ef135d3efe71de59ce91aa6d4c70e4d958ccef`

Base tree: `ebda76a545e39a06fee5089816880852f68a8719`

## Verdict

`blocked`. The proof-relevant target inputs are unchanged from the preceding
recheck. No source-faithful proof of the cohomological Atiyah-Hirzebruch
spectral sequence exists in the owned dossier or pinned dependency closure.

`Proof.lean` remains a real, placeholder-free conditional composition
harness: it assembles every output field and packages the result as the exact
literal `Statement`, but `statementOfBranchFamily` assumes the complete E2,
differential, convergence, and naturality branch family. It constructs none of
those branches. It therefore closes no frozen obligation and receives no root
proof credit.

The immediate open root cut remains:

- `M0554-X-GENCOH`: generalized-cohomology pair, excision, and wedge infrastructure;
- `M0554-C-EXACT-COUPLE`: the skeletal-filtration exact-couple construction;
- `M0554-C-E2-MODEL`: the cellular-cohomology E2 identification;
- `M0554-L-STRONG`: strong convergence for the finite skeletal filtration.

No proof receipt, composition certificate for closure, accepted receipt, debt
change, or item-state transition is proposed. The root remains `M4`.

## First Failed Gate

Exact-statement fidelity and predecessor authority fail before proof credit.
The selected mathematical claim requires a reduced generalized cohomology
theory and a genuine finite CW construction. The current Lean interface omits
reducedness; stores exactness, wedge, point, and CW requirements as
proposition-valued fields without evidence; leaves `ordinaryCohomology`
unrelated to `H^p(X; E^q(pt))`; represents the induced filtration by the
tautology `K.skeleton = K.skeleton`; and lets the output select bare
propositions for coefficient convention, strong convergence, and naturality.

Consequently, a zero spectral-sequence/`True` witness can inhabit the literal
target while proving no mathematical AHSS. Such a witness is deliberately not
implemented or credited because it would be a fake or substituted result
under the rev-5.6 statement-fidelity and child-composition gates.

The structured authorities are also not proof-ready. `instance.json` is still
`planned` with null canonical formal identity fields. The local `task-dag.json`
is unfrozen and marks proof `blocked_by_predecessors`. Registry v1 contains
planned fingerprints for substantive branches, and the global predecessor is
only provisional rather than master-accepted. A proof-only worker cannot
rewrite those predecessor authorities.

## Fresh Validation

The automation-provided `Formalizations/Lean/.lake` symlink to the canonical
pinned artifacts was reused read-only. No Lake update/build, dependency
clone/fetch, checkout, network action, or `.lake` mutation was performed. Lean
outputs were isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106; lane `frontier_deep_formalization_debt`; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | `PASS THM-M-0554 obligation tree: 32 obligations, 91 typed edges`; denominator `3c72072a...8048b`; root remains open at `M4` without a composition certificate. |
| `LAKE_NO_UPDATE=1 timeout -k 5 60 lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0 commit `98dc76e3...16740`; the pinned environment is available. |
| Isolated `LAKE_NO_UPDATE=1 lake env lean --trust=0 -t0` replay of `Statement.lean`, `Proof.lean`, and `DifferentialProbe.lean` | 0 | Objects were 429072, 280728, and 15576 bytes. Log SHA-256 values were `f1690fd1...d30`, `8cfbfe08...2a1`, and `30cba6d3...156`. The three conditional proof declarations were sorry-free and reported exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Pinned-package AHSS/generalized-cohomology/exact-couple/strong-convergence `rg` scan | 1 | Expected no-match: no terminal proof candidate in the pinned packages. |
| Focused spectral-object API audit | 0 | `HasSpectralSequence.lean` supplies `coreE2Cohomological` for an indexed spectral object, but no actual `CategoryTheory.SpectralSequence`; the terminal constructor and homology glue remain TODO. |
| Prohibited-token scan over owned Lean sources | 1 | Expected no-match: no `sorry`, `admit`, `axiom`, `sorryAx`, unsafe theorem, or `native_decide`. |
| SHA-256 and TODO scan of `Mathlib/Algebra/Homology/SpectralObject/SpectralSequence.lean` | 0 | SHA-256 `2ce62b9d...740aa`; intended spectral-sequence constructors remain documented as TODO. |
| `git diff --quiet 3f5b3108...HEAD --` over the ten proof-relevant inputs | 0 | Statement, proof, diagnostic, structured statement, anchor audit, registry, typed graphs, validation specs, instance, and local task DAG are unchanged. Current HEAD adds blocker evidence only. |
| `find Stage1_Instances/THM-M-0554 -maxdepth 1 -name '*.json' -print0 | xargs -0 -n1 jq empty` | 0 | Every top-level owned JSON artifact parsed before this packet was written. |

The isolated Lean recipe was:

```bash
set -euo pipefail
repo=$PWD
target=$repo/Stage1_Instances/THM-M-0554
lean_root=$repo/Formalizations/Lean
tmp=$(mktemp -d /tmp/thm-m-0554-proof-recheck-88ef135d.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
base_path=$(cd "$lean_root" && LAKE_NO_UPDATE=1 lake env printenv LEAN_PATH)
for source in Statement Proof DifferentialProbe; do
  extra_path=$base_path
  if test "$source" = Proof; then extra_path=$tmp:$base_path; fi
  (
    cd "$lean_root"
    LEAN_NUM_THREADS=1 LEAN_PATH="$extra_path" LAKE_NO_UPDATE=1 \
      timeout -k 5 300 lake env lean --trust=0 -t0 -R "$target" \
        -o "$tmp/$source.olean" "$target/$source.lean"
  ) >"$tmp/$source.log" 2>&1
done
wc -c "$tmp"/*.olean "$tmp"/*.log
sha256sum "$tmp"/*.olean "$tmp"/*.log
```

This warm pinned replay checks the current statement, conditional composition,
and bidegree diagnostic. It is not evidence for the absent AHSS branches or
root.

## Retry Condition

First publish and master-accept a source-faithful statement, reconcile the
instance/task/statement authorities, and issue registry v2 with exact branch
fingerprints. Then implement and compose the four root-cut packages without
placeholders. Alternatively, pin an immutable compatible Lean 4 AHSS proof and
pass exact-type, provenance, trust, and composition gates.

Status boundary: this is durable current-base blocker evidence only. It does
not satisfy `S56-M-0554-PROOF`, close a frozen obligation or root, propose
`[_]`, complete the audit or theorem, enter validation/release, or authorize
master acceptance. Because the assigned proof phase is not genuinely
self-tested as complete, `.stage1-worker-selftest.json` remains absent.
