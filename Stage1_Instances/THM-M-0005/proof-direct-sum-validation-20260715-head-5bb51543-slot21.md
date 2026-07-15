# THM-M-0005 direct-sum proof progress

Item: `S56-M-0005-PROOF`

Base revision: `5bb515438bd0e1d53584e5243c5d434dfde7158e`

Verdict: `no_state_change`, with self-tested partial proof bodies. The exact root remains blocked and
no frozen obligation, accepted state, audit completion, or theorem completion is claimed.

## Implemented bodies

`ProofDirectSum20260715Head5bb51543Slot21.lean` adds eight checked declarations implementing four
conceptual facts toward `M0005-DIRECT-SUM`. They prove the exact equivalence
`TorDegrees (n + 1) ≃ TensorDegrees n`, reindex the actual categorical Tor coproduct along that
equivalence, prove the forward and inverse injection equations, prove that `TorDegrees 0` is empty,
and prove that `TorTerm R X Y 0` is a zero object. Thus both the positive-degree grading convention
and the degree-zero boundary of the frozen subtraction-free target are checked rather than assumed.

These bodies do not close the whole frozen direct-sum obligation. That node also owns the transports
out of an algebraic Kunneth construction, which does not yet exist. In particular, none of the new
declarations constructs an inclusion, projection, short exact sequence, Eilenberg-Zilber comparison,
or inhabitant of `KunnethFormula`.

## Validation

The automation-provided pinned `.lake` symlink was reused read-only. No `lake update`, `lake build`,
dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0005` | 0 | Confirmed rank 100, planned hard-mathlib lane, and `theorem_complete: false`. |
| `bash Stage1_Instances/THM-M-0005/check_direct_sum_proof.sh` | 0 | The bounded checker replayed `KunnethStatement.lean` and the new module with `--trust=0`; it parsed all eight axiom reports and accepted only `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 Stage1_Instances/THM-M-0005/check_obligation_tree.py` | 0 | The frozen 18-obligation, 51-edge architecture passed; the root remains open at M3. |
| `python3 Stage1_Instances/THM-M-0005/check_direct_sum_packet.py` | 0 | Source, exact scope, hashes, pins, receipt boundaries, changed paths, and packet/receipt agreement passed. |
| prohibited-device scan over the new Lean source | 1 | No match; exit 1 is ripgrep's required no-match result. |
| `python3 -m json.tool Stage1_Instances/THM-M-0005/proof-direct-sum-receipt-20260715-head-5bb51543-slot21.json` | 0 | Structured receipt parsed. |
| `git diff --check -- Stage1_Instances/THM-M-0005 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The committed checker resolves the executable and `LEAN_PATH` with `lake env`, copies both sources
to a fresh `/tmp` directory, bounds the overall run to 600 seconds, elaborates into fresh outputs,
and parses every `#print axioms` report against the allowed three-axiom set. Its SHA-256 is
`36c03579f6993d2716c060587c128673da378162cb122599122af19018b7e988`. Both Lean commands
exited 0. The statement emitted only its four existing unused-variable linter warnings. The new
source SHA-256 is
`8577f084bc162051ebd98e996e8870f9ea9dba74192e35973d5edb7b2d5e04e7`; its temporary `.olean`
SHA-256 was `e1133ae18c2082c3b70aacc26183734f80f9fd1ad5ed72ad2e1499639c27ae32`.
Its combined proof-output SHA-256 was
`35ea8e8cb5e99f2f25d13645e69b3ae694df3860dcda79f25f7381690c1170a8`.

Pinned environment: Lean `4.29.0` at
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; `lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Remaining blocker

The first failed root-critical gate remains `M0005-EZ-MAP`. Pinned mathlib contains no
placeholder-free Eilenberg-Zilber or Alexander-Whitney chain comparison and explicitly provides
only minimal Tor infrastructure. The algebraic Kunneth maps, zero composite, exactness, naturality,
and their topological transports are also absent. The audited Atlas lead at immutable commit
`34ffed396f376454c1a9b297f3fd74c5c801fb50` terminates at `sorry` throughout its critical routes.

The authoritative root therefore stays `[H1, M3, R3]`. This self-test supports only the exact scope
above and proposes no semantic-node closure. Master acceptance, later validation/release gates, and
theorem completion remain open.
