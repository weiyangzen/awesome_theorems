# THM-M-1045 proof phase blocker at `9bce865a`

Item: `S56-M-1045-PROOF`

Base revision: `9bce865a14bcc270344ea909d6936c6ea22aa1c2`

Base tree: `523a9471aac257c4cf54acceee07172fab22f5b4`

Recorded: `2026-07-15T13:44:28+08:00` (`Asia/Shanghai`)

## Verdict

`blocked`. No eligible positive proof body can establish the frozen
`Stage1Instances.THM_M_1045.CameronMartinTarget`, so this phase remains `[ ]` and no root
`.stage1-worker-selftest.json` is written.

The root quantifies over every `WienerData`, but `WienerData.paleyWienerIntegral` is constrained
only by measurability. `ProofBlockerCurrent.lean` preserves all Wiener-law fields, replaces only
that field by the measurable constant-one pairing, and proves:

```text
no_target_of_wienerData (W : WienerData) : Not CameronMartinTarget
```

At the zero direction and zero integrand, the frozen density branch makes the self
Radon-Nikodym derivative equal `ENNReal.ofReal (Real.exp 1)` almost everywhere, while
`Measure.rnDeriv_self` makes it equal one. The checked characterization is therefore:

```text
target_iff_isEmpty_wienerData : CameronMartinTarget iff IsEmpty WienerData
```

Empty elimination is a vacuous result about the malformed interface, not a proof of the
Cameron-Martin theorem. It cannot receive proof credit under the no-substitution gate.

## Failed Gate

Exact-target consistency fails at `M1045-S-DEFINITIONS`, invalidating
`M1045-L-PALEY-WIENER` and blocking `M1045-B-DENSITY`, `M1045-T-ASSEMBLE`, and `M1045-ROOT`.
The proposed truthful vector is `[H1, M3, R3] -> [H1, M5, R3]`. Separately, the predecessor
`S56-M-1045-OBLIGATION_TREE` remains worker-provisional `[_]`, not master-accepted `[x]`.

Two other statement risks remain: the path measurable-space encoding comaps `top` without
establishing the advertised cylinder/Borel sigma-algebra, and `timeMeasure` pushes all real
volume through `Real.toNNReal`, collapsing the negative half-line rather than selecting ordinary
volume on `NNReal`.

Positive proof work can resume only after a source-justified statement revision constrains or
constructs the Paley-Wiener integral without assuming the desired conclusion, corrects or justifies
the measure encodings, publishes a fresh statement fingerprint, and refreezes the dependent anchor
audit and obligation graphs.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was treated as read-only. No `lake update`, `lake build`,
dependency clone/fetch, or other `.lake` mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 ordered targets at L0/rework-required passed. |
| `python3 scripts/stage1_target.py show THM-M-1045` | 0 | Rank 238, planned, legacy artifacts unaccepted, theorem incomplete. |
| `timeout --foreground --kill-after=2s 20s env ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean --version` from `/tmp` | 1 | Pinned Lake resolution reported `dependency 'BochnerMinlos' not in manifest`; no repair was attempted. |
| Independent isolated pinned Lean 4.29.0 replay of the statement, current blocker, characterization, and conditional composer with `--trust=0 -t0` | 0 | All four elaborated; blocker, characterization, and composer axioms were exactly `[propext, Classical.choice, Quot.sound]`. |
| `python3 -B Stage1_Instances/THM-M-1045/check_anchor_audit.py` | 0 | Fingerprint, probes, candidates, and mathlib pin agreed. |
| `python3 -B Stage1_Instances/THM-M-1045/check_obligation_tree.py` | 0 | 15 obligations and 30 typed edges passed; root remains open at M3. |
| Prohibited-construct scan of the blocker, characterization, and composer | 1 expected | No `sorry`, `admit`, `axiom`, `sorryAx`, unsafe/oracle, or opaque proof escape was found. |
| `python3 -m json.tool` on the blocker packet | 0 | Structured blocker evidence parsed. |
| `git diff --check -- Stage1_Instances/THM-M-1045` and new-file whitespace checks | 0 / 1 expected | No whitespace diagnostics; exit 1 only reports each new file differs from `/dev/null`. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No success manifest exists for this blocked phase. |

The pinned statement, blocker, characterization, and conditional-composer log SHA-256 values are
respectively `4adb258a91317991276961bad1d03712638888a5a2af84a12240a92e12a8b110`,
`55dcd476292f394eca6e28e17cf180ad4d1773f6601d84fed4adcc8284a58964`,
`38cd8fdac134d193c3293524684a66c80023fb7d9ab84740f0ad23aeb7bfde95`, and
`8f9246d00cd8e9461675b69ca071323c2818448bedf026cdf27fbaaac2b43737`.

This is target-scoped blocker evidence only. It adds no positive proof body, closes no obligation,
and makes no provisional-state, audit-completion, validation, release, theorem-completion, or
master-acceptance claim.
