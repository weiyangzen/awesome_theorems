# THM-M-0721 proof recheck at `6bf9ee93` (slot41)

Item: `S56-M-0721-PROOF`

Verdict: `blocked`; the item remains `[ ]`.

## Dependency and reuse audit

The required `dependency-reuse-ledger.json` now binds the supplied v2 graph digest, target context
digest, and current base revision. The hard parent, ancestor, edge, and reuse-hint closures are
empty. Both weak shared-module groups were inspected through actual member `THM-M-0874`:

- `Mathlib.Computability.Reduce` supplies unrestricted computable many-one reductions, not the
  frozen polynomial-time reduction or an NP-completeness body.
- `Mathlib.Computability.TuringMachine.Computable` supplies only the general bundled TM2 substrate.
  The member has no accepted statement or proof artifact, and the module has no SAT, `InNP`,
  Cook-Levin, or exact NP-completeness endpoint.

Both decisions are therefore `not_applicable`; no proof credit was transferred.

## Exact proof blocker

The only checked path to the root is `root_of_candidate_packages`, which assumes rather than builds
the two immediate packages. The minimal root cut remains:

- `M0721-T-SAT-IN-NP`: faithful binary SAT encodings, a polynomial-time TM2 verifier, correctness,
  and certificate bounds;
- `M0721-T-UNIVERSAL-HARDNESS`: arbitrary verifier normalization, a Cook-Levin tableau, both
  correctness directions, and polynomial-time TM2 construction of the reduction.

All eleven underlying SAT and Cook-Levin registry nodes remain open and have no terminal proof-body
IDs. Pinned mathlib supplies only identity and the machine substrate;
`TM2ComputableInPolyTime.comp` is source-level `proof_wanted`, not a checked declaration. No local,
pinned, shared-group, or audited external artifact closes either terminal package.

A trust-zero throwaway probe constructed a genuine constant-output finite TM2. This confirms that
constant predicates are easy in the frozen model, but it does not expose an oracle or prove
hardness: empty and universal languages are both easy `InNP` examples and neither can reduce every
other such language to itself; identity proves only reflexivity.

The proof phase is also not acceptance-legal yet because its obligation-tree prerequisite is only
worker-provisional `[_]`. Thirty-six earlier dated blocker records already exceed the five-tick
mandatory split threshold, while the authoritative proof item still has zero attempts and no
children. Only the master may repair that DAG structure.

## Validation boundary

The target statement checker passed with expression digest
`758b1033903c92b231a24ae3fb5e01e0bbb0d6fdb0bc41f809c062deb7b4b204` and killed all four
mutations. The obligation checker passed 18 nodes and 45 typed edges but truthfully reported the
root at `M3` and both terminal packages at `M4`. The new schema-1.1 ledger passed the scheduler's
exact context validator.

The global standard and v2 graph validators now fail a distinct upstream invariant: fresh graph
generation includes the newly required ledger in `evidence_inventory.structured_json_files`, even
though the checked-in graph predates it. The generator excludes dependency ledgers from shared-group
discovery but not from inventory. This worker cannot modify or regenerate the authoritative DAG or
its generator, so the failure is recorded rather than hidden.

No `.stage1-worker-selftest.json` was written. This is current-base, warm-cache blocker evidence,
not a proof implementation, proof receipt, worker `[_]` completion, theorem completion, validation,
release, or master acceptance.
