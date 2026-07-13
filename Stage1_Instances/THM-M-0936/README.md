# THM-M-0936 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Cauchy-Davenport theorem. The
repository supplies only the phrase `有限域上子集和的下界` ("a lower bound for subset sums over a
finite field"), the Cauchy/Davenport attribution, and the date 1813. Its `已验证` label is
untrusted metadata and supplies neither an exact source statement nor proof credit.

The conventional theorem is recognizable: for a prime `p` and nonempty subsets `A` and `B` of
`Z/pZ`, the sumset satisfies `|A + B| >= min(p, |A| + |B| - 1)`. A versioned,
checksum-bound modern source lead, Jeffrey Paul Wheeler's arXiv paper `1202.1816v1`, states this
result as Theorem 1.4 and records the separate Cauchy 1813 and Davenport 1935 history. It is not the
catalog's cited source, and no primary Cauchy or Davenport edition, premise/proof/errata map, or
independent source review is admitted, so it is not credited as `H0`.

The catalog wording is materially underdetermined. It does not say that there are two nonempty
sets, define their pointwise sumset, require prime cardinality, or give the capped cardinality
formula. Moreover, "finite field" can mean an extension field. Replacing `Z/pZ` by an arbitrary
finite field while capping at the field cardinality is false: a nontrivial proper additive subgroup
`H` has `H + H = H`. A valid field-general result instead depends on the characteristic. Intake
therefore does not silently turn the conventional prime-field theorem into a broader claim.

Pinned mathlib contains `Mathlib.Combinatorics.Additive.CauchyDavenport` and the exact-topic
declaration `ZMod.cauchy_davenport`, as well as the stronger group-level interface
`cauchy_davenport_minOrder_add`. `IntakeProbe.lean` authenticates both APIs and prints their direct
axiom reports. This is candidate discovery only: canonical-root selection, checked source
transport, proof-body provenance, and trust closure remain downstream work.

The provisional vector is `[H1, M3, R4]`. All six later phases remain open. No canonical
mathematical or Lean statement, accepted proof state, audit completion, theorem completion,
accepted receipt, or master acceptance is claimed.

See `scope-map.md` for proposition-changing choices, `source-statement-crosswalk.md` for the
source/formal component map, `task-dag.json` for the open execution route, and `validation.md` for
the exact self-test boundary.
