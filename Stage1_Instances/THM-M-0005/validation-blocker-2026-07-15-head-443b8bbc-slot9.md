# THM-M-0005 validation recheck: blocked

Item: `S56-M-0005-VALIDATION`

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

Base tree: `c5771c47c12b80aba613e6d844570f83b39ded6d`

Validation time: `2026-07-15T11:50:28+08:00`

## Verdict

`blocked`. The first failed gate is dependency legality. The proof predecessor is only
worker-provisional `[_]`, which is unfinished under the dual-cursor state protocol and cannot
support positive validation acceptance. Exact-root closure is the next failed gate: the strongest
structured receipt is `accepted=false` with `root_kernel_closed=false`, and the authoritative typed
graph records zero closed obligations and an open `M3` root. No unconditional declaration inhabits
`AwesomeTheorems.Stage1.THM_M_0005.KunnethFormula`.

`KunnethFormula` is only a proposition definition. `ObligationTree.root_compose` and
`ProofProgress20260715Slot21.kunnethFormula_of_fields` consume the still-unimplemented Kunneth
maps, exactness, and naturality fields as premises. The later local files contain real helper
bodies for singular-chain freeness/projectivity, functorial component maps, and direct-sum
reindexing, but even their receipts assign no entire frozen obligation or root credit.

Validation intent permits rechecking evidence, not adding the missing Eilenberg-Zilber and
algebraic Kunneth mathematics or rewriting the frozen architecture. The root vector therefore
remains `[H1, M3, R3]`; `audit_complete=false` and `theorem_complete=false`.

## Recipe Failure

The frozen `validation-specs.json` belongs to `S56-M-0005-OBLIGATION_TREE`, not this validation
node. Its eighteen recipes all relabel the same command:

```text
lake env lean ../../Stage1_Instances/THM-M-0005/ObligationTree.lean
```

Each recipe omits the rev-5.6 structured fields `env_allowlist`, `network_policy`, `expected_exit`,
`expected_outputs`, `covered_obligation_ids`, and `covered_declarations`, using the nonconforming
fields `env`, `network`, and `covered_ids` instead. More importantly, conditional elaboration of
`ObligationTree.lean` cannot cover the root, open Eilenberg-Zilber/algebraic/topological nodes,
later proof modules, source provenance, or the TCB. The recipe set is therefore structurally
nonconforming and false-scoped for positive validation.

A fresh representative replay could not reach Lean. The automation-provided `.lake` symlink points
to the shared canonical cache, where `flt-regular` currently has `HEAD` set to
`refs/heads/.invalid` and has no checked-out files. Lake exits 1 before elaboration:

```text
error: .../.lake/packages/flt-regular: could not resolve 'HEAD' to a commit; the repository may be corrupt, so you may need to remove it and try again
```

The manifest-pinned commit object
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` is present and has tree
`32c9eace926573a9981787ae97643e520353c893`; this is an unavailable pinned checkout, not evidence
that the declared revision changed. This worker did not repair it because `lake update`, `lake
build`, dependency checkout/fetch/clone, and all other `.lake` mutation are forbidden. Historical
warm replay records remain nonrelease observations and cannot replace a fresh validation recipe.

## Trust And Independence

The owned Lean files contain no active `sorry`, `admit`, `sorryAx`, custom axiom/constant,
opaque/unsafe body, `extern`, `implemented_by`, or `native_decide`. That hygiene result does not
close trust: there is no root proof body from which to derive a transitive declaration and axiom
closure, and no accepted foundation policy or complete hashed TCB inventory.

The shared warm `.lake` symlink is not a clean empty-cache build or network-disconnected archive
restoration. No target-scoped accepted artifact supplies a complete restorable SBOM/license/TCB
bundle, second signed attestation from a distinct independently provisioned runner, independently
implemented minimal verifier, or mutation/adversarial acceptance suite. Repeating a command in
this workspace would not be independent verification.

## Commands And Exact Results

No command ran `lake update`, `lake build`, dependency clone/fetch/checkout, or modified `.lake`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 and uniform L0/rework-required passed |
| `python3 scripts/stage1_target.py show THM-M-0005` | 0 | rank 100; planned; hard-mathlib lane; theorem incomplete |
| `python3 -B Stage1_Instances/THM-M-0005/check_obligation_tree.py` | 0 | 18 obligations and 51 typed edges passed; denominator `563eac89...a762`; root open `M3`; no closure credit |
| `jq -e` exact open-root assertions over `typed-graphs.json` | 0 | graph remains `root_closed=false` at `M3`, with no closed obligation, audit, or theorem completion |
| `jq -e` exact unaccepted/root-open assertions over `proof-direct-sum-receipt-20260715-head-5bb51543-slot21.json` | 0 | strongest receipt is unaccepted, supports and closes no obligation, and records `root_kernel_closed=false` |
| `python3 -c` assertion audit of the 18 `validation-specs.json` recipes | 0 | recipes collapse to one conditional module and each omits all six required fields listed above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0005/ObligationTree.lean` | 1 | Lake rejected the invalid `flt-regular` HEAD before Lean ran |
| `bash Stage1_Instances/THM-M-0005/check_direct_sum_proof.sh` | 1 | same missing pinned checkout failure before elaboration |
| `python3 -B Stage1_Instances/THM-M-0005/check_direct_sum_packet.py` | 1 | old proof checker requires an absent historical root worker self-test packet and is not a current validation recipe |
| `rg -n --pcre2 '(?m)^[[:space:]]*(?:axiom|constant|opaque|unsafe|extern)\b|\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b' Stage1_Instances/THM-M-0005/*.lean` | 1 | expected no-match: no prohibited active construct |
| mathlib revision/tree/cleanliness check | 0 | revision `8a178386...ea95`, tree `bdc39a31...1c2b`, tracked worktree clean |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse --verify HEAD^{commit}` | 128 | invalid HEAD has no commit |
| pinned `flt-regular` object/tree inspection | 0 | declared commit object exists with tree `32c9eace...c893`, but no checkout is present |
| Explicit Python LF/CR/NUL/trailing-whitespace assertions over both new blocker files | 0 | both untracked artifacts passed |

## Retry Condition

First close and master-accept the exact proof predecessor: supply placeholder-free Eilenberg-Zilber
and algebraic Kunneth bodies, the required transports and naturality, and an unconditional inhabitant
of the unchanged root. The automation or integration lane must restore the already declared
`flt-regular` checkout without changing its pin, then publish normative declaration-scoped
validation recipes. Validation must subsequently rerun kernel, complete trust/provenance, cold
offline hermetic, and distinct independent-verifier gates against one immutable snapshot.

This is fresh target-scoped negative validation evidence only. It does not satisfy the assigned
validation node, propose `[_]`, accept any obligation, establish `M0`/`E0`/`E1`, complete the audit
or theorem, release the target, or authorize master acceptance. Because the phase is not genuinely
self-tested, `.stage1-worker-selftest.json` remains absent.
