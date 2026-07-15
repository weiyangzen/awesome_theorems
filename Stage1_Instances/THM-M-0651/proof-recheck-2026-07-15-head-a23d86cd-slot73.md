# THM-M-0651 proof-phase recheck at `a23d86cd` (slot73)

Item: `S56-M-0651-PROOF`

Recorded at: `2026-07-15T09:30:00+08:00`

Base: `a23d86cd84f03c26102b43c6b1b3b6d0a7a31e61` / tree
`9268aa9f5379837642b6f748f01255e8744c4e78`

## Verdict: blocked with partial proof progress

`ProofLemmas.lean` adds real, unconditional Lean bodies for the countable
enumeration package:

- `countable_symbols` derives countability of the combined language symbols;
- `countable_finite_arity_syntax` derives countability of all finite-arity
  formulas;
- `countable_avoidance_requirements` combines formula work with every family
  index and finite tuple of natural-number names;
- `exists_surjective_avoidance_schedule` produces one surjective `Nat` schedule
  over that combined requirement type;
- the two zero-arity declarations check that nullary formula and tuple work is
  not silently discarded.

These bodies are useful evidence for `M0651-L-ENUM` and the `M0651-B-ARITY0`
boundary. They do not close the frozen obligations by themselves: the
architecture records only planned fingerprints rather than exact formal
signatures, and the enumeration output is not yet consumed by a Henkin
construction. No closed obligation, root closure, or provisional item state is
claimed.

The exact root remains blocked at `M4`. There is still no placeholder-free
body for `M0651-L-DENSE`, `M0651-L-HENKIN`, or `M0651-L-OMIT`. In addition,
the frozen `AvoidanceInterface` is not a valid leaf target: its `Candidate`
stores only an arbitrary countable model of `T`, while the interface says every
such candidate omits all specified nonprincipal types. A real construction
must carry avoidance invariants or return the omitted model jointly.
The prerequisite `S56-M-0651-OBLIGATION_TREE` is also only worker-provisional
`[_]`, so master proof acceptance is dependency-illegal even apart from these
open mathematical bodies.

## Proof and dependency surface

| Input | SHA-256 |
|---|---|
| `Statement.lean` | `39b09536792acdd585eb62dc09917eca50eff8717211a764bca58d96645d38ea` |
| `ObligationTree.lean` | `2317873fba80bc681a10267eaba79f13828a35f156950168a388b565f9c8c2df` |
| `ProofLemmas.lean` | `5639c2aef1f5359a8714bdb97f417ce621c4137d0a501ffcb1df2e9240d7fc33` |
| `obligation-registry.json` | `9a87b090025b80fde991e80c2eec07a9f67ae84a269802288d30c7ec572d142f` |
| `typed-graphs.json` | `7ae5e1d811de7c88799746b29a6d89d277f0954ab1b131c499f807cb47548900` |
| `anchor-audit.json` | `17fc3419e05444401a36b0146562a552179c663c6a92606f1a05add44b21111c` |
| `lean-toolchain` | `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` |
| `lake-manifest.json` | `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |

The current registry has 11 obligations and 21 typed edges. Its denominator is
`e739a3f3ee963205d34582d0879d767e928e26670f557de0871addcc176f3805`.
The four recorded cut-set leaves remain `M0651-L-ENUM`, `M0651-L-DENSE`,
`M0651-L-HENKIN`, and `M0651-L-OMIT`; this packet proposes no authoritative
registry or graph edit.

Pinned mathlib commit/tree is `8a178386ffc0f5fef0b77738bb5449d50efeea95` /
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. Its ModelTheory tree has no
omitting-types body. A later local git object `ff96409d623285fbfe777cf47c50574f05f63a3d`
adds compact/Baire instances for complete-type spaces as future groundwork,
but it is not an ancestor of the pin and contains no omitting-types theorem.
It therefore receives no proof credit. The audited external infinitary-logic
theorem remains incompatible in syntax, arity, semantics, dependencies, and
toolchain.

## Validation

All commands reused the automation-provided pinned `.lake` symlink read-only.
No Lake update/build, dependency clone/fetch, network operation, or dependency
mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0651` | 0 | Rank 697; planned; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0651/check_statement.py` | 0 | Expression hash `789c281a...`; both frozen mutations killed. |
| `python3 Stage1_Instances/THM-M-0651/check_obligation_tree.py` | 0 | 11 obligations and 21 typed edges passed; root open at M4. |
| Trust-zero isolated Lean recipe below | 0 | Statement, conditional composition, and all seven new proof declarations elaborated. |
| Prohibited-construct `rg` scan | 1, expected | No `sorry`, `admit`, `sorryAx`, axiom/constant/opaque/unsafe/extern declaration, `native_decide`, or `implemented_by` occurs in owned Lean sources. |
| Scoped pinned-mathlib candidate `rg` scan | 1, expected | No omitting-types, nonprincipal, or partial-type declaration occurs under pinned `Mathlib/ModelTheory`. |
| `git diff --quiet f8800826..HEAD -- <frozen inputs and locks>` | 0 | Frozen statement, tree, graph, anchor, toolchain, and manifest inputs are unchanged since the prior proof attempt. |

The trust-zero check copied all three Lean files into a fresh `/tmp` directory,
compiled them with `LEAN_NUM_THREADS=1`, `lake env lean --trust=0 -t0`, and
removed the directory. The new declarations report only `propext`,
`Classical.choice`, and `Quot.sound`; the zero-arity witnesses report no axioms.
The resulting temporary object hashes were `b9f7da7a...06f0` for the statement,
`db013978...d2ef1` for the composition probe, and `ae768581...a090` for the new
proof lemmas.

The exact isolated command was:

```bash
set -euo pipefail
repo=$PWD
tmp=$(mktemp -d /tmp/thm-m-0651-slot73-head-a23d86cd.XXXXXX)
trap 'rm -rf "$tmp"' EXIT HUP INT TERM
cp "$repo/Stage1_Instances/THM-M-0651/Statement.lean" "$tmp/Statement.lean"
cp "$repo/Stage1_Instances/THM-M-0651/ObligationTree.lean" "$tmp/ObligationTree.lean"
cp "$repo/Stage1_Instances/THM-M-0651/ProofLemmas.lean" "$tmp/ProofLemmas.lean"
cd "$repo/Formalizations/Lean"
LEAN_NUM_THREADS=1 timeout --foreground 600 lake env lean --trust=0 -t0 \
  --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 timeout --foreground 600 lake env lean --trust=0 -t0 \
  --root="$tmp" -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean"
LEAN_NUM_THREADS=1 timeout --foreground 600 lake env lean --trust=0 -t0 \
  --root="$tmp" -o "$tmp/ProofLemmas.olean" "$tmp/ProofLemmas.lean"
sha256sum "$tmp/Statement.olean" "$tmp/ObligationTree.olean" \
  "$tmp/ProofLemmas.olean"
```

The exact hygiene scans were:

```bash
rg -n --pcre2 '\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|^[[:space:]]*(?:axiom|constant|opaque|unsafe|extern|external)(?:[[:space:]]|$)' \
  Stage1_Instances/THM-M-0651 --glob '*.lean'
rg -n -i 'omitting[ _-]*types|nonprincipal|non-principal|partial[ _-]*type' \
  Formalizations/Lean/.lake/packages/mathlib/Mathlib/ModelTheory --glob '*.lean'
```

Both returned exit 1 with empty output, the expected no-match result.

## Retry boundary

Refine and version the obligation architecture so the enumeration theorem has
an exact consumed interface and the constructed candidate retains avoidance
invariants. Then implement the nonprincipality extension, Henkin/model
construction, and fair-schedule decoding bodies, or integrate an immutable
compatible exact theorem through checked transports.

This is current-base nonrelease blocker evidence with partial proof bodies. It
does not satisfy `S56-M-0651-PROOF`, does not close the root, and supports
neither audit nor theorem completion. Because the assigned phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.
