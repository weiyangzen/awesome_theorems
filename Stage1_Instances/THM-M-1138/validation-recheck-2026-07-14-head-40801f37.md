# THM-M-1138 validation recheck: blocked

Item: `S56-M-1138-VALIDATION`

Base revision: `40801f373a9b0443cc58ff8ec365fb5b75c8b8c3`

Base tree: `f3b8367a9ec13bd00b783bc4367d64003ffcde28`

Validation time: `2026-07-14T02:50:00+08:00`

## Verdict

`blocked`. A fresh current-head replay confirms that `Proof.lean` really kernel-checks the exact
terminal package and public maximum-principle root without placeholders. That observation cannot
satisfy the assigned rev-5.6 validation phase because the proof does not realize the frozen
version-1 architecture.

The first failed gate is frozen-route reconciliation. The registry and typed graphs require an
unperturbed closure maximizer followed by a strong-maximum/local-constancy route. The implemented
proof instead uses strict-subharmonic perturbations. Its own proof receipt therefore withholds
`M1138-C-CLOSURE-MAXIMIZER`, `M1138-B-MAXIMIZER-LOCATION`,
`M1138-L-INTERIOR-LOCAL`, `M1138-L-CONNECTED-PROPAGATION`, and
`M1138-L-CONTINUITY-EXTENSION`, as well as foundation credit. The authoritative graph remains
`root_closed=false`, `M3`, with no accepted closed obligation.

This mismatch cannot be silently repaired during validation. The rev-5.6 registry rule requires a
versioned append-only delta, and validation intent permits rechecking evidence rather than adding
proof or rewriting the architecture to fit an observed result.

## Current Kernel Evidence

`check_proof.sh` passed against the existing pinned toolchain. A separate disposable replay used
the pinned Lean executable with `--trust=0`, `LEAN_NUM_THREADS=1`, and all generated oleans under
`/tmp`. `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` elaborated. Both
`Stage1Instances.THM_M_1138.Proof.boundaryMaximumPackage` and
`Stage1Instances.THM_M_1138.Proof.harmonicWeakMaximumPrinciple` reported
`Declarations are sorry-free!` and exactly these axioms:

```text
propext
Classical.choice
Quot.sound
```

This is real narrow kernel evidence, but it is warm worker evidence only. Axiom observation is not
an accepted foundation profile or complete transitive declaration, source, import, executable, and
TCB closure.

The disposable replay command was:

```bash
ROOT=$PWD
HERE=$ROOT/Stage1_Instances/THM-M-1138
TMP=$(mktemp -d /tmp/thm-m-1138-independent.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
LEAN_BIN=/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
LEAN_PATH_PINNED=$(cd "$ROOT/Formalizations/Lean" && lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$LEAN_PATH_PINNED" timeout 300 "$LEAN_BIN" --trust=0 -t0 \
  -R "$HERE" "$HERE/Statement.lean" -o "$TMP/Statement.olean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$LEAN_PATH_PINNED" timeout 300 "$LEAN_BIN" --trust=0 -t0 \
  -R "$HERE" "$HERE/ObligationTree.lean" -o "$TMP/ObligationTree.olean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$LEAN_PATH_PINNED" timeout 300 "$LEAN_BIN" --trust=0 -t0 \
  -R "$HERE" "$HERE/Proof.lean" -o "$TMP/Proof.olean"
```

All three exits were 0, and the trap removed the generated objects.

The proof-phase Python checker is not a current validation recipe. It is bound to an older proof
snapshot and requires a root `.stage1-worker-selftest.json` that was not integrated into repository
history. Its current invocation exits 1 with `FileNotFoundError`. This does not negate the direct
Lean replay, but it prevents the old receipt checker from supplying fresh proof provenance.

## Recipe And Release Gaps

The frozen `validation-specs.json` belongs to `S56-M-1138-OBLIGATION_TREE`. All fifteen recipes
invoke only `check_obligation_tree.py`; that checker validates the version-1 structural freeze and
explicitly reports an open `M3` root and `M4` terminal package. Its declared boundary says it does
not validate the open analytic proof. There is therefore no truthful structured recipe covering
the perturbation-route declarations.

Additional gates remain open:

- The proof and every predecessor are provisional `[_]`, not master-accepted, and the target
  lifecycle remains `planned`.
- No accepted foundation policy, complete transitive proof-body provenance, TCB inventory,
  independently reviewed primary-source `H0`, or independently reviewed readable `R0` exists.
- The automation-provided `.lake` is an untracked symlink to shared warm pinned artifacts. It is
  neither an empty-cache cold build nor a network-disconnected archive restoration.
- No complete content-addressed SBOM/license archive, distinct signed verifier on an independently
  provisioned clean runner, or independently implemented minimal checker exists.
- Intake-era `README.md`, `intake.json`, and `validation.md` are not reconciled public projections
  of the later provisional statement and proof evidence.

The accepted vector remains `[H1, M3, R3]`; `audit_complete=false` and
`theorem_complete=false`.

## Commands And Exact Results

No command ran `lake update`, `lake build`, dependency clone/fetch, or modified `.lake`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1138` | 0 | rank 343, planned, L0/rework-required, theorem incomplete |
| `python3 -B Stage1_Instances/THM-M-1138/check_obligation_tree.py` | 0 | 15 obligations and 36 typed edges passed; denominator `a2093825...ca49`; root open `M3`; terminal package `M4` |
| `timeout 300 bash Stage1_Instances/THM-M-1138/check_proof.sh` | 0 | exact terminal package and public root elaborated; both sorry-free; axioms exactly `propext`, `Classical.choice`, `Quot.sound` |
| Disposable pinned Lean `--trust=0` replay of `Statement.lean`, `ObligationTree.lean`, and `Proof.lean`, with outputs under `/tmp` | 0 | statement, conditional composition, exact terminal package, and exact root elaborated with the same sorry and axiom results |
| `python3 -B Stage1_Instances/THM-M-1138/check_proof.py` | 1 | expected fail-closed result: historical proof worker packet is absent, so the old snapshot-bound checker cannot replay |
| Comment-stripped prohibited-mechanism scan over owned Lean sources | 1 | expected no-match result: no active `sorry`, `admit`, `sorryAx`, custom axiom/constant, opaque/unsafe body, `extern`, `implemented_by`, or `native_decide` |
| mathlib revision/tree/cleanliness check | 0 | revision `8a178386...ea95`, tree `bdc39a31...1c2b`, tracked worktree clean |

## Retry Condition

An architecture-owning predecessor lane must publish and master-accept an append-only
registry/typed-graph/composition/provenance/recipe revision for the perturbation proof. Validation
can then rerun the exact declarations against that immutable reconciled snapshot. Release assurance
will still require accepted foundation and TCB profiles, complete source provenance, a cold offline
reproduction with SBOM/licenses, and agreeing signed independent verification.

This is current-head negative validation evidence only. It does not satisfy
`S56-M-1138-VALIDATION`, propose `[_]`, accept an obligation, establish `M0`/`E0`, complete the
audit or theorem, release the target, or authorize master acceptance. Because the assigned phase is
not genuinely self-tested, `.stage1-worker-selftest.json` remains absent.
