# THM-M-1079 rev-5.6 intake

This directory is the `planned` intake dossier for the repository label "martingale difference
sequence". The source record says only "properties of martingale difference sequences" and does
not identify one proposition. Accordingly, this intake freezes the mathematical family and its
boundaries, but deliberately leaves the exact root theorem open for the statement phase. Choosing
one familiar property here would silently substitute a theorem not present in the source record.

The intended object is a discrete-time integrable adapted sequence whose next term has conditional
expectation zero with respect to the current filtration. Natural candidate roots include the
martingale property of its partial sums and the converse construction from successive increments
of a martingale. Neither candidate is selected or credited at intake.

The manifest's historical `已验证` label is untrusted metadata. No exact Lean expression, accepted
source proof, formal anchor, or kernel closure is claimed. The provisional root vector is
`[H1, M4, R3]`; audit completion and theorem completion are false. The first failed downstream gate
is exact statement identification. See `scope-map.md`, `source-statement-crosswalk.md`, and
`task-dag.json` for the frozen boundary and open work, and `validation.md` for self-test evidence.
