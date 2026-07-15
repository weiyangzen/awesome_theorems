# THM-M-0005 validation recheck: blocked

Item: `S56-M-0005-VALIDATION`

Base revision: `33a5b0d654c92a894e155f5385edaae684091bb0`

Base tree: `74ed89524afb3c118e31a7fce9b5763fee26b180`

Validation time: `2026-07-15T12:49:48+08:00`

## Verdict

`blocked`. The first failed gate is dependency legality. `S56-M-0005-PROOF` remains
worker-provisional `[_]`, which is unfinished under the dual-cursor protocol. Its strongest
structured receipt is `accepted=false`, supports no frozen obligation, and records
`root_kernel_closed=false`. The frozen graph independently records zero closed obligations and an
open `M3` root. Neither `ObligationTree.root_compose` nor
`ProofProgress20260715Slot21.kunnethFormula_of_fields` is a root proof: both consume the missing
Kunneth construction, exactness, and naturality as premises.

There is also an independent exact-source failure. The source crosswalk says Hatcher Theorem 3B.6
includes a noncanonical splitting, while the frozen `NaturalKunnethSequence` deliberately omits
splitting. The legacy description does not decide whether the intended theorem is the full split
form or only the natural short exact sequence. No archived and hashed primary edition, pinpoint
hypothesis/errata review, checked equivalence, or independent source approval resolves that
difference. The short-exact target is mathematically plausible, but validation cannot certify it as
an exact source theorem.

The root vector stays `[H1, M3, R3]`; `audit_complete=false` and
`theorem_complete=false`. Validation intent does not permit adding the missing proof mathematics or
quietly changing the frozen statement.

## Kernel And Trust Observations

The 18 recipes in `validation-specs.json` all relabel the same conditional
`ObligationTree.lean` elaboration. Every recipe uses the nonconforming keys `env`, `network`, and
`covered_ids`, and omits `env_allowlist`, `network_policy`, `expected_exit`, `expected_outputs`,
`covered_obligation_ids`, and `covered_declarations`. They cover neither the proof-progress modules
nor an unconditional root declaration, terminal-body provenance, exact trust closure, source, or
TCB. A passing run could not support their claimed node labels.

The recorded root recipe did not reach Lean. The automation-provided `.lake` symlink points to the
shared canonical cache, where `flt-regular` has no valid `HEAD` or checkout files. Lake exited 1:

```text
error: .../.lake/packages/flt-regular: could not resolve 'HEAD' to a commit
```

The manifest-pinned commit object
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` is present with tree
`32c9eace926573a9981787ae97643e520353c893`. This is an unavailable pinned checkout, not a changed
pin. No `lake update`, `lake build`, dependency clone/fetch/checkout, or other `.lake` mutation was
performed.

As the smallest additional kernel observation, all six owned Lean modules were copied to a fresh
temporary directory and directly elaborated with the pinned Lean executable, `--trust=0`, one
thread, and only pre-existing read-only package build paths. All six exited 0. Across the 26 printed
axiom reports, every set was a subset of `propext`, `Classical.choice`, and `Quot.sound`. A
comment-stripped parser-aware scan and supplementary ripgrep defense found no active `sorry`,
`admit`, `sorryAx`, custom axiom/constant, opaque/unsafe body, `extern`, `implemented_by`, or
`native_decide` in the six sources.

That warm direct replay is narrow nonrelease evidence only. It does not execute the malformed
recorded recipes, restore `flt-regular`, produce a root proof, derive transitive root provenance, or
supply an accepted foundation profile and complete hashed TCB. The shared cache is not a new
checkout with empty caches or a network-denied restoration. No target-scoped artifact supplies a
restorable SBOM/license bundle, a second signed attestation from a distinct independently
provisioned runner, an independently implemented minimal verifier, or the required
mutation/adversarial suite. Repetition in this workspace is not independent verification.

## Commands And Results

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 and uniform L0/rework-required passed |
| `python3 scripts/stage1_target.py show THM-M-0005` | 0 | rank 100; planned; hard-mathlib lane; theorem incomplete |
| exact DAG assertions for validation and proof | 0 | validation `[ ]` depends on unfinished proof `[_]`; positive acceptance is dependency-illegal |
| `python3 -B Stage1_Instances/THM-M-0005/check_obligation_tree.py` | 0 | 18 obligations and 51 typed edges passed; denominator `563eac89...a762`; root open `M3`; no closure credit |
| exact `jq -e` assertions over `typed-graphs.json` | 0 | `root_closed=false`, zero closed obligations, no audit or theorem completion |
| exact `jq -e` assertions over the strongest proof receipt | 0 | receipt unaccepted, no supported/closed obligation, `root_kernel_closed=false` |
| required-key and scope assertions over `validation-specs.json` | 0 | 18 recipes collapse to one conditional command and each omits six normative keys |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0005/ObligationTree.lean` | 1 | invalid `flt-regular` HEAD prevented Lean from running |
| `bash Stage1_Instances/THM-M-0005/check_direct_sum_proof.sh` | 1 | same dependency failure before elaboration |
| `python3 -B Stage1_Instances/THM-M-0005/check_direct_sum_packet.py` | 1 | historical proof checker requires an absent root worker self-test and is not a current validation recipe |
| direct `/tmp` replay of all six owned modules with pinned Lean and `--trust=0` | 0 | all modules elaborated; 26 axiom reports contained only `propext`, `Classical.choice`, and `Quot.sound` |
| parser-aware hygiene scan over `Stage1_Instances/THM-M-0005/*.lean` | 0 | six Lean files contain no prohibited active construct |
| supplementary prohibited-construct ripgrep scan | 1 | expected no-match |
| source-crosswalk boundary assertions | 0 | provisional `H1`, Hatcher 3B.6, and the splitting boundary remain explicit |
| mathlib revision/tree/cleanliness inspection | 0 | revision `8a178386...ea95`, tree `bdc39a31...1c2b`, tracked worktree clean |
| `git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse --verify HEAD^{commit}` | 128 | no valid HEAD commit |
| pinned `flt-regular` object/tree inspection | 0 | declared commit exists with tree `32c9eace...c893`, but no checkout is present |

## Retry Condition

First master-accept a dependency-legal, placeholder-free proof predecessor that unconditionally
inhabits the unchanged and source-approved root, including all root-critical Eilenberg-Zilber,
algebraic Kunneth, transport, component, exactness, and naturality obligations. Restore the already
declared `flt-regular` checkout without changing its pin and publish conforming declaration-scoped
recipes. Then run complete trust/provenance checks, a cold empty-cache network-denied replay, and a
distinct independent verifier against one immutable snapshot.

This is current-base target-scoped negative validation evidence only. It does not satisfy the
assigned validation node, propose `[_]`, accept a proof or obligation, establish `M0`/`E0`/`E1`,
complete the audit or theorem, release the target, or authorize master acceptance. Because the phase
is not genuinely self-tested, `.stage1-worker-selftest.json` remains absent.
