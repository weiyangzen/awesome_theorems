# THM-M-0936 intake validation

## Environment and mutation boundary

The run used repository base `fb0baac89ea0633612be3b47448464b4b8e4bef7` (tree
`018557070da18ea1733a82de81a238750c59aa84`), Lean 4.29.0 commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The automation-provided
`Formalizations/Lean/.lake` symlink was already untracked at preflight and was used read-only. No
`lake update`, `lake build`, clone, fetch, dependency write, or `.lake` mutation was performed.

This is inherited, dirty, nonhermetic worker evidence. It is neither a cold build nor a release,
offline-replay, independent-runner, or deterministic-bundle attestation.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0 / rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0936` | 0 | rank 1475, planned, no legacy slot, legacy artifacts unaccepted, theorem completion false |
| `git status --short --untracked-files=all` at preflight | 0 | only the pre-existing automation `.lake` symlink was untracked; it was preserved read-only |
| bounded repository and pinned-mathlib exact-topic search | 0 | located `Mathlib.Combinatorics.Additive.CauchyDavenport`, `ZMod.cauchy_davenport`, and `cauchy_davenport_minOrder_add`; no repo-local target-specific artifact was found |
| `tmp=$(mktemp -d); curl -L --fail --silent --show-error -o "$tmp/wheeler.pdf" 'https://arxiv.org/pdf/1202.1816v1'; sha256sum "$tmp/wheeler.pdf"; pdfinfo "$tmp/wheeler.pdf" \| sed -n '1,80p'; pdftotext -layout "$tmp/wheeler.pdf" "$tmp/wheeler.txt"; sed -n '1,260p' "$tmp/wheeler.txt"; rm -rf "$tmp"` | 0 | network-required discovery downloaded the 11-page versioned PDF, observed SHA-256 `eb4bbc4d75ffab654b43a49495b6a24124da446edd16ff8771603b46b244f4fb`, and exposed Definition 1.1, Theorem 1.4, and historical references; the temporary bytes were removed and no `H0` or primary-proof credit is assigned |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` and status | 0 | pinned revision/tree matched the lock and package worktree was clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0936/IntakeProbe.lean` | 0 | both exact-topic APIs elaborated; both report `propext`, `Classical.choice`, and `Quot.sound`; combined output SHA-256 `213f9a1f3818459beca88cfe1305f3901a1bd09f8de0c0dc980c25c8067c6a25` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 each | all structured artifacts are valid JSON |
| `python3 -B Stage1_Instances/THM-M-0936/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | authority identity, pins, source hashes, null canonical target, H1/M3/R4 boundary, exact inventory, receipt/packet, recipes/actions, and six open tasks agree |
| prohibited Lean declaration scan over `IntakeProbe.lean` | expected no-match exit 1 | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token; diagnostic `#print axioms` is intentionally allowed |
| `git diff --check -- Stage1_Instances/THM-M-0936 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |
| `for f in .stage1-worker-selftest.json Stage1_Instances/THM-M-0936/*; do out=$(mktemp); git diff --no-index --check /dev/null "$f" >"$out" 2>&1; rc=$?; test "$rc" -eq 1 && test ! -s "$out" || exit 1; rm -f "$out"; done` | 0 | all ten untracked files differed from `/dev/null` with the expected exit 1 and produced no whitespace diagnostics; the scoped checker also byte-validates the root packet and all owned files |

## Validated boundary

The checks validate only a `planned` intake: target membership, the literal catalog record, the
scope and non-substitution map, a modern source lead, the false arbitrary-extension-field
broadening guard, the discovery-only pinned Lean interfaces, and the six-node open downstream DAG.
The direct candidate axiom output is an observation, not transitive foundation or trust closure.
The two structured replay recipes declare network denial and make no network request, but this
inherited worker did not provide an independently attested OS-level network sandbox. The arXiv
inspection was a separate, explicitly network-required discovery action and is not a denied-network
structured replay recipe. The provisional structure action hashes every explicit input it reads or
hash-checks except its self-referential receipt and the inherited compiled `.lake` closure; those
exclusions are recorded in the receipt and must be recaptured by the master.

The canonical mathematical and Lean statement remain null. Source adoption, primary-source and
errata review, prime-field versus arbitrary-field scope, sumset/cardinality transports, expression
and environment fingerprints, mutation tests, exhaustive candidate/provenance audit, discovery and
obligation freezes, typed graphs, proof, composition, readable reconstruction, hermetic replay,
deterministic evidence, independent verification, audit completion, and theorem completion remain
open. These boundaries do not invalidate a truthful self-tested planned intake, but they forbid any
claim that the theorem itself has been completed.
