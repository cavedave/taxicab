
The Four Least Solutions in Distinct Positive Integers of the Diophantine Equation
s = x3 + y3 = z3 + w3 = u3 + v3 = m3 + n3

E. ROSENSTIEL, MDS,
London

J. A. DARDIS, AFIMA
University of London Computer Centre

and C. R. ROSENSTIEL
Cambridge



[From The Institute of Mathematics and its Applications Bulletin July, 1991, Volume 27, pp 155-157]


This article describes how one amateur number theorist with only limited computer experience (i.e., E. Rosenstiel) formed a team with two computer scientists to show that

6 963 472 309 248 = 2 4213 + 19 0833 = 5 4363 + 18 9483

= 10 2003 + 18 0723 = 13 3223 + 16 6303

is the least solution in distinct positive integers of

sq = x3 + y3 = z3 + w3 = u3 + v3 = m3 + n3,

that the three next larger solutions are:

12 625 136 269 928 = 4 2753 + 23 2373 = 7 0683 + 23 0663

= 10 3623 + 22 5803 = 12 9393 + 21 8693

21 131 226 514 944 = 1 5393 + 27 6453 = 8 6643 + 27 3603

= 11 7723 + 26 9163 = 17 1763 + 25 2323

26 059 452 841 000 = 4 1703 + 29 6203 = 12 9003 + 28 8103

= 14 5773 + 28 4233 = 21 9303 + 24 9403

and that the next one is greater than 5 x 1013. The paper ends with a brief survey of unsolved related problems.

Introduction (E. Rosenstiel)

THIS project started when I was asked to write a program to list up to as high a limit as a simple microcomputer would permit all so called cubic doublets starting with

1729 = 93 + 103 = 13 + 123,

which was already known in Euler's time as the least integer having two representations as the sum of two positive cubes. (In this century this "least doublet" entered mathematical folklore through Hardy's report of a visit to Ramanujanl in a Putney hospital via taxi cab No.1729.)

My first attempts did not get very far, but a BASIC program written by J. A. Dardis and run on my Commodore PET computer sufficed to list, in about a week, all sums sd under 109 sorted in ascending order, where sd = x3 + y3 = z3 + w3, i.e. , where sd is a doublet.

In order to check these results, but also to extend my list, using the old PET with only 32K memory I had come to the end of my own explorations: J. A. Dardis ran a much faster FORTRAN program on a mainframe machine which quite quickly printed a complete list of all sums sd under 4 x 109 sorted in ascending order but which now included all positive primitive and nonprimitive solutions. And thus happened our first discovery.

Looking in this list for instances where the same value sd occurred, but with different summands x, y, z and w, led to the rediscovery of the least triple identity st, first reported by Leech2 in 1957, namely that the first of these equal sums was

st = 87 539 319 = 1673 + 4363 = 2283 + 4233 = 2553 + 4143.

Here st must be least, and it must be primitive. Otherwise a common factor N > 1 could be removed. Thus let st = N3st* , then st* < st, and st* should have been listed earlier in the search.

Now we had no idea how Leech had programmed his protocomputer over 30 years ago but we realised that we had stumbled on a practical method for finding not just cubic "doublets," but also "triplets," "quadruplets," etc. in ascending order.

Hardy and Wright3 had long ago reproduced the proof that the Diophantine equation

x13 + y13 = x23 + y23 = ... = xr3 + yr3 (*)

has solutions in positive integers for any given r. In their book this relation is referred to as "Theorem 412."

The existence of the least quadruple identity

sq = x3 + y3 = z3 + w3 = u3 + v3 = m3 + n3 ( ** )

was therefore assured, and it only remained to find whether the least quadruplet could be reached with the greatly increased computer power available since 1957. That cubic doublets and triplets could be found "to order" with parametric formulae, which were already known to Euler4 and Werebrusow,5 respectively, does not of course solve the problem of finding the least solutions of ( * ) for given r. It was indeed Leech2 who first identified the five least cubic triplets t1 - t5, and thus disproved Gerardin's5 conjecture published in 1908 that

" ...5603 + 703 = 5523 + 1983 = 5253 + 3153

was "probably" the least triplet in positive integers . . ."

It was in fact Leech's fourth-least triplet t4 which he reported was the only one that had been listed by Dickson5 in 1920. It was later included in Beiler's6 popular tract on Number Theory, while Leech's least positive triplet t1 was duly recorded by Wells7 in 1986.


Our own investigations

We decided to extend Leech's2 results further by searching for least cubic quadruplets, i.e., we had identified our PROJECT as:

Finding the location of the least cubic positive quadruplet sq1 and of as many more sq as computer power would permit. This project would also provide independent confirmation for the first five cubic triple solutions claimed by Leech2 in 1957 just referred to.

At the same time there had evolved the particular algorithm first conceived by J. A. Dardis which was, while undergoing many refinements in the course of our investigations, to be the instrument enabling the completion of the project. Its main features were as follows.

(a) Starting from s = 1729 as the first lower bound it computed all "singlet" sums of two cubes s = x3 + y3 between lower and upper bounds that would essentially depend on the storage capacity of the individual computer.

(b) It then arranged the resulting sums s in ascending order by means of a suitable sorting subroutine.

(c) It identified and listed those sums which appeared more than once, i.e., doublets, triplets, completing thus the first "block,"

(d) Finally it set a new lower bound for the next block to be equal to the previous upper bound and another upper bound, again depending on storage capacity, but also chosen in such a way that there would be neither a gap between nor an overlap of these bounds.

There is little point in reporting the actual codings that were used. Clearly we found much scope for improvements, reflected in faster and faster runs as the project progressed. It was important to monitor the various subsections of each program in order to identify those parts where unnecessary but time-consuming calculations occurred, e.g., while computing and storing lists of cubes, or during the different sorting routines which were tried. Amongst simple number-theoretical limitations on x and y were for instance that always x ≠ y, since otherwise doublets would exist as sd = 2y3 = z3 + w3 (using the notation of the Introduction), but this is impossible from the proven analogue of the famous conjecture known as Fermat's last Theorem.8

At this stage C. R. Rosenstiel joined the project and, using a Philips P3202 PC-AT compatible microcomputer, he succeeded after many months of first interpreted and then steadily improved compiled BASIC programs in finding sql.

In a list of all positive integers representable as cubic triplets st up to 7 x 1012, the least solution of ( ** ) was found thus:

s558 = 6 963 472 309 248

= 13 3223 + 16 6303 = 5 4363 + 18 9483 = 10 2003 + 18 0723
s559 =6 963 472 309 248

= 5 4363 + 18 9483 = 10 2003 + 18 0723 = 2 4213 + 19 0833,
hence

sql = 6 963 472 309 248

= 2 4213 + 19 0833 = 5 4363 + 18 9483 = 10 2003 + 18 0723 = 13 3223 + 16 6303
which resulted from combining the 558th and 559th triplets. The program was such that the other two triplets which also could be combined to form sql were not listed. If this had been the case, it would show that the program contained unnecessary redundancies, making it slower and less efficient.

After many more refinements and by using the most up-to-date Quick-Basic compiler versions as they became available, C. R. Rosenstiel repeated in a rerun lasting only 243 hours the computations for the above claimed least solution sql of ( ** ), which he found after a total of 97 792 doublets.

He then extended the rerun past the 704/705th, the 862/863rd and the 941/942nd triplets which combined into the next larger quadruplets:

sq2 = 12 625 136 269 928

= 4 2753 + 23 2373 = 7 0683 + 23 0663 = 10 3623 + 22 5803 = 12 9393 + 21 8693
sq3 = 21 131 226 514 944

= 1 5393 + 27 6453 = 8 6643 + 27 3603 = 11 7723 + 26 9163 = 17 1763 + 25 2323
sq4 = 26 059 452 841 000

= 4 1703 + 29 6203 = 12 9003 + 28 8103 = 14 5773 + 28 4233 = 21 9303 + 24 9403
This run was finally taken to all sums under 50 694 081 101 000 when, having found a total of 236 771 doublets and 1224 triplets, the program had reached the practical limits of whole number manipulations in Quick Basic, requiring entirely new ideas to extend the run farther. All these results were later confirmed by J. A. Dardis using a compiled Turbo Pascal program.


Summary

A recent review by Churchhouse9 gave many examples of problems in number theory which are still awaiting solutions by number-theoretical methods, but which have meanwhile been disposed of by the methods of enumeration that have become possible since the arrival of electronic computers.

Our investigations have applied these methods to some further problems in the area of Diophantine Equations concerned with the representation of integers by sums of two positive equal powers in more than one way.

A claim made for the solution of the least cubic triplet problem in 19085 was shown by Leech2 to be false, who thus was one of the first to apply the new method of enumeration by computer to problems awaiting answers since the 17th and 18th century.

The "least cubic quadruplet" problem here presented would seem to be even more intractable to solve by "ordinary" number-theoretical methods.

We noted three apparently unconnected facts.

(a) The number of doublets preceding the least triplet was similar in magnitude to the number of triplets preceding the least quadruplet.

(b) When the logarithms of the cumulative numbers of cubic doublets (or triplets) were plotted against the logarithms of the respective sums of these doublets (or triplets), a striking linearity was seen in both cases, (and also in the case of fourth power doublets which will be mentioned in the next section).

(c) There is the Theorem 412 from Hardy and Wright3 [referred to earlier on as ( * )].

These three items may well have a discoverable connection, but it is felt that this is a problem well outside the scope of the project here presented.

Survey of related problems yet unsolved

Similar, but seemingly even harder, challenges arise when one is seeking answers to corresponding problems involving sums of two fourth powers. Parametric solutions of

sd = x4 + y4 = z4 + w4

were already given by Euler, and these, together with more recent, simplified versions, are discussed in Hardy and Wright.10

These versions easily furnish the numeric solution

635318657 = 1334 + 1344 = 594 + 1584 (***)

found by Euler.

However, the proof that this is indeed the least fourth power doublet did not appear until over 200 years later in the paper by Leech2 already quoted. This result was confirmed by J. A. Dardis while he sought solutions to two unsolved problems.

(a) No fourth power triplets are known, and, during a search for the least of these, 1269 doublets including (***) were computed without finding it. The sums were calculated to just past 4.61 x 1018 (the limit of integer arithmetic with the Turbo Pascal compiler used), and the last result was

s1269 = 4 608 535 738 441 446 497

= 1 9184 + 46 3334 = 35 6514 + 41 5944.
Although no fourth power triplet was found, this search established that the first number representable as the sum of two positive fourth powers in three essentially different ways must, if it exists, have at least 19 digits. It is noted here that there is no equivalent known of Hardy and Wright's3 Theorem 412 (the one which guarantees the existence of cubic doublets, triplets, quadruplets etc.) which is valid for any powers higher than three!

(b) A search for the least fifth power doublet soon outran the computer power available without adding to the Summing Up given by Hardy and Wright3 more than 30 years ago, namely that not even doublets are known for higher than fourth powers, i.e., only for 2nd, 3rd and 4th powers have integers been found which can be expressed as the sum of two equal and positive powers in more than one way. This leaves open the possibility of further projects, as and when yet more powerful computers with suitable algorithms can be applied to these remaining unsolved problems.


References

1. Rankin, R. A., IMA Bulletin. 1987, 23, 149.
2. Leech, J., Proc. Camb. Phil. Soc., 1957, 53, 778-780.
3. Hardy, G. H., and Wright, E. M., "Introduction to the Theory of Numbers," Oxford, Clarendon Press, Fifth Edition, 1979, pp. 333-334.
4. Ibid, p. 199.
5. Dickson, L. E., quotes A. S. Werebrusow and A. Gerardin's result in "History of the Theory of Numbers, Vol 2," 1920, cited from its reprinting of 1952 by Chelsea Publishing Co., New York, N.Y., p. 562.
6. Beiler, A. H., "Recreations in the Theory of Numbers," Second Edition, 1966, Dover Publication, Inc., New York, NY, p. 287.
7. Wells, D., "The Penguin Dictionary of Curious and Interesting Numbers," Revised Edition, 1988, Penguin Books Ltd, Harmondsworth, Middlesex, England, p. 189.
8. Carmichael, R. D., "Diophantine Analysis," 1959, Dover Publication, Inc., New York, NY, p. 67.
9. Churchhouse, R. F., IMA Bulletin, 1989, 25, 40.
10. Hardy, G. H., and Wright, E. M., op. cit., p. 201.