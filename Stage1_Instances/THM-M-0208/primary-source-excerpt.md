# Primary source excerpt

This file preserves the exact theorem and proof excerpt inspected for the `THM-M-0208` intake. It
does not constitute an independently reviewed translation or an `H0` source receipt.

## Bibliographic identity

- Creator: Vincenzio Viviani.
- Work: *De maximis et minimis, geometrica divinatio* (full catalog title: *De maximis et
  minimis, geometrica divinatio: in quintum Conicorum Apollonii Pergaei*), 1659.
- Holding: Max Planck Institute for the History of Science, Library.
- Permanent viewer identifier: `MPIWG:N7VDDBN4`.
- ECHO transcription identifier: `ECHO:QN4GHYBF.xml`.
- Document endpoint:
  `https://thrax.mpiwg-berlin.mpg.de/mpiwg-mpdl-cms-web/doc/GetDocument?id=/echo/la/Viviani_1659_QN4GHYBF.xml`.
- Retrieved XML: 1,729,692 bytes; SHA-256
  `57a438ef902213671bf06b0cac8088bfc50b10f4127f7eb0b18b0ebe16a8535e`.
- Rights metadata: `CC-BY-SA`; license URL
  `http://creativecommons.org/licenses/by-sa/3.0/`; rights holder Max Planck Institute for the
  History of Science, Library.
- Independent catalog cross-check: DML author index entry for `QN4GHYBF`, retrieved response
  SHA-256 `4b7d986c2f46d390c5ca0fa13238e65b8408d27754b0a6fcac039474de343af6`.

## Exact locator

Appendix, `LEMMA II. PROP. II.`, original printed pages 146-147, scan pages 332-333. In the
retrieved XML this is the section headed by `echoid-head397`; the statement is `echoid-s9208` and
`echoid-s9209`, the two-point setup is `echoid-s9211` through `echoid-s9216`, and the proof is
`echoid-s9218` through `echoid-s9227`.

## Latin statement

Line-break tags from the transcription are removed, while spelling is preserved.

> In quocunque polygono regulari, aggregata perpendicularium ex quibuscunque punctis, (quae tamen
> non sint extra perimetrum polygoni) super omnia eius latera eductarum, inter se sunt aequalia.
> Si vero alterum punctorum fuerit extra perimetrum, aggregatum perpendicularium ex eo eductarum,
> maius semper erit quolibet praedictorum aggregatorum ex puncto, quod non sit extra.

The ECHO transcription uses historical glyphs such as long `s`; the ASCII normalization above is
for readable preservation. The source XML hash and element identifiers bind the exact diplomatic
transcription.

## Working translation

For any regular polygon, the sums of the perpendiculars drawn from any points, provided those
points are not outside the perimeter of the polygon, to all its sides are equal to one another. If
one of the points is outside the perimeter, the sum of the perpendiculars drawn from it is always
greater than any such sum from a point that is not outside.

The proof takes two arbitrary points `F` and `G`, either inside the regular polygon or on its
perimeter, draws their perpendiculars to every side, and joins each point to all vertices. This
partitions the same polygon into two families of triangles. Taking the perpendiculars as bases, the
regular polygon's equal side lengths are the corresponding triangle altitudes. The preceding lemma
therefore compares the sums of perpendicular bases through the two area decompositions. Since each
family fills the same polygon, those sums are equal. For an exterior point the associated triangle
family exceeds the polygon, giving the strict inequality.

This English rendering is a worker translation for crosswalk purposes. No independent Latin
reviewer, critical-edition comparison, correction or errata audit, or accepted translation receipt
exists yet.

## Relationship to the catalog target

The primary result is broader than the catalog: it covers every regular polygon and includes points
on the perimeter. The catalog's equilateral-triangle strict-interior wording is a natural
specialization, but a checked source-to-target specialization is still required. The primary text
asserts equality of the sums for arbitrary admitted points; it does not literally state that the
triangle sum equals an altitude. The altitude formula follows by specializing to a regular
triangle and comparing with a suitable boundary point, so it must be treated as a derived
alternate form rather than silently inserted into the literal root.
