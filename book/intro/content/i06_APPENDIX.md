
# VI: Appendices

## Practical Implementations and Numerical Insights of the Tholonic I Ching






## π, φ, e, √2, ln(2) Generation from Tholonic Principles


<img src="/home/jw/src/iching_cli/book/intro/Images/times7.png" style='float:right;width:30%'/>Here is the Python3 code to run the Pi generator, which demonstrates the mathematical relationship between tholonic principles and fundamental constants. Also included are the core functions to calculate other constants, which show different patterns and relationships in teh tholon. The image on the right is the triad that is used as input values for calculating &pi;.

```
#!/bin/env python3


def compute_tholonic_constant(constant_type="pi", max_iter=1000000):
    """
    Calculate various mathematical constants using tholonic algorithm variations

    Constants:
    - "pi": π (3.14159...)
    - "phi": φ Golden ratio (1.61803...)
    - "e": Euler's number (2.71828...)
    - "sqrt2": Square root of 2 (1.41421...)
    - "ln2": Natural log of 2 (0.69314...)
    """

    # Initial conditions vary based on constant
    if constant_type == "pi":
        N_k = 1
        h_step = 2
        sum_d = 3
        prod_c = 5
        multiplier = 4  # Final result multiplier

    elif constant_type == "phi":
        N_k = 1
        h_step = 1
        sum_d = 1
        prod_c = 2
        multiplier = 1

    elif constant_type == "e":
        N_k = 2
        h_step = 1
        sum_d = 1
        prod_c = 1
        multiplier = 1

    elif constant_type == "sqrt2":
        N_k = 1
        h_step = 1
        sum_d = 2
        prod_c = 2
        multiplier = 1

    elif constant_type == "ln2":
        N_k = 0.5
        h_step = 1
        sum_d = 1
        prod_c = 2
        multiplier = 1

    for count in range(max_iter):
        if constant_type == "pi":
            N_next = N_k - (1 / sum_d) + (1 / prod_c)
            sum_d += h_step**2
            prod_c += h_step * 2

        elif constant_type == "phi":
            N_next = 1 + (1 / N_k)
            temp = prod_c
            prod_c = prod_c + sum_d
            sum_d = temp

        elif constant_type == "e":
            N_next = N_k + (1 / prod_c)
            prod_c *= count + 1 if count > 0 else 1

        elif constant_type == "sqrt2":
            N_next = (N_k + (2 / N_k)) / 2

        elif constant_type == "ln2":
            N_next = (
                N_k + (1 / (count + 1)) if count % 2 == 0 else N_k - (1 / (count + 1))
            )

        N_k = N_next

        if count % 1000 == 0:
            print(f"Iteration {count}: Result = {N_k * multiplier}")

    print(f"Final {constant_type} Result:", N_k * multiplier)
    return N_k * multiplier


# Example usage:
print("\nCalculating π:")
compute_tholonic_constant("pi")

print("\nCalculating φ (Golden Ratio):")
compute_tholonic_constant("phi")

print("\nCalculating e (Euler's number):")
compute_tholonic_constant("e")

print("\nCalculating √2:")
compute_tholonic_constant("sqrt2")

print("\nCalculating ln(2):")
compute_tholonic_constant("ln2")

```

This program demonstrates how π can be derived through the tholonic relationships discovered in our analysis of the I Ching. The initial values are taken from the tholonic interpretation of trigrams, particularly the relationships between *Negotiation*, *Definition*, and *Contribution* as mapped to the primary trigram values.

## The 8×8 Grid


Before we go down this seemingly obscure rabbit hole, the reader might be interested in why we are even bothering with this. 

As was mentioned earlier, 2×3=6 is the simplest instance of the most fundamental pattern of interaction. And we saw examples of this at the beginning of this introduction in the form of *F=ma, V=IR, W=Fd, c=f\\&lambda;, E=hf, v = &lambda;\\f, and even E=mc².* These are just a few of hundreds of instances that we can see across all sciences, physics, and even metaphysics.

When we say 2×3, we are describing a function that has two dimensions: 2 and 3, just as saying “1” alone has only one dimension. Likewise, if we say 3×3×2, we are describing something three-dimensional. 2D formulas are very common in physics and mechanics, as well as electricity, but 2×3 is the archetype of that pattern. What would the archetype of a 3D function look like? The most likely candidate is 2×2×3, but the Tholonic model and the I Ching suggest that 3×3×2 is more accurate because 3×3×2 is actually more self-similar than 2×2×3. Here is why, as explained by AI[^26], which does a far better job of explaining than I do:

[^26]: OpenAI, ChatGPT 4.0

##### The 3×3×2 structure is more self-similar than the 2×2×3 structure because it maintains greater uniformity across its dimensions. In a 3×3×2 configuration, the two larger dimensions (3×3) form a square base, which exhibits a repeating pattern, while the smaller third dimension (2) allows for a balanced extension. This preserves a sense of proportionality and symmetry, making it more conducive to recursive self-similarity. In contrast, a 2×2×3 structure lacks this symmetry, as its dominant 3-length dimension disrupts the uniformity between its two smaller, equal sides. Self-similarity often arises from balanced repetition across dimensions, making 3×3×2 a more structurally consistent and recursively extendable form.

In this 3D extended version of the 2D fundamental interactions we see that *18=2×3^2^* is a much closer archetype formulas such as  *E=mc^2^*,  *KE=$\frac{1}{2}$mv^2^* (kinetic energy), *P=(σAT^2^)×T^2^* (radiant power), *kq=Er^2^* (electric field), *P/4πr^2^* (radiant intensity), and more.

We see a pattern that equates the speed of light (c) with 3 and mass with 2. Mapped to the tholon, where 2 equates to *Limitation/Definition* and 3 equates to *Contribution/Integration*, we gain an expanded understanding of what E might represent. This becomes even more profound when we apply the concept of the I Ching, where 2 equates not only to the limits of our environment but also to the laws of reality.

I think we can all agree that mass is an excellent example of the limitation of energy, given that mass is essentially energy "slowed down" by *8.987×10^16^m^2^/s^2^*, and it unquestionably limits the existence of everything.

In the Tholonic spectrum of Awareness and Intention, 2 equates with Awareness, as awareness itself is a defining process, an act of definition or limitation.

This then equates 3 with Intention, suggesting that movement is the contributing and integrating quality, and given that the potential of movement is, by definition, energy, and because the very purpose of radiation (light) is to distribute energy, we can say that the intentions of energy are to distribute itself. The tholonic claim is that energy only exists as a result of the balancing of some imbalance, which suggests that the “intention” of energy is to achieve balance.

With all the above in mind, the formula *E = mc²*, interpreted symbolically through the Tholonic lens, can be mapped as *m* = 2, *c* = 3, yielding *E* = 2 × 3² = 18. Interestingly, 18 corresponds to ***o***22 in base<sub>8</sub>, marking the second full octave of the value of mass. This resonance is not significant because of the number 22 in base<sub>10</sub> (although that is interesting), but because ***o***22 represents the first point at which mass, as an instance of the first duality (2), reaches a new scale of instantiation: an octave of self-similarity within the recursive structure of manifestation, representing a duality of dualities, or rather, a spectrum framed by two distinct dualities. This pattern of 2 pairs as a stable recursive system emerges again and again as a persistent theme in the architecture of existence.

<img src="/home/jw/src/iching_cli/book/intro/Images/8x8.png" style='float:right;width:25%'/>As for the grid itself and the numbers within it, this 8×8 grid emerged from this *2×3^2^* pattern. We began by splitting 18 into two prime numbers: 7 and 11, which provides the most balanced representation from both tholonic and I Ching perspectives. We then further divided 11 into two complementary pairs: 5+6 and 4+7, seeking the most even distributions possible. These numbers, 0 through 7, were then positioned within an 8×8 grid following a pattern where complementary pairs always sum to 7 (0+7, 1+6, 2+5, 3+4). The red numbers (0, 1, 2, 3) occupy positions in the left/upper portion of the grid, while their green complements (7, 6, 5, 4) are positioned in the right/lower portion, creating a visual representation of balance. The exact locations of these numbers are determined by the relationship between the polar chart (which appears to be the parent tholon) and the binary chart (which appears to be a child tholon). This arrangement reflects fundamental principles found in both the Tholonic Model and the I Ching, where opposing yet complementary forces interact to create wholeness. The grid thus represents a two-dimensional manifestation of how the original number 18 can be decomposed into balanced, interrelated elements that maintain specific mathematical relationships while embodying principles of negotiation, limitation, and contribution.

The placement of these numbers and the numbers themselves, in the 8×8 grid emerged from our systematic decomposition of the original number 18 derived from the archetypal pattern of *2×3^2^*. We first split 18 into two prime numbers (7 and 11), then further divided 11 into complementary pairs, ultimately giving us the set of numbers 0 through 7 to place in our grid.

- 

### Why 2×3²=18 and not 2²×3=16, and it Relation to the 8×8 Grid


As briefly as possible, here is the relationship between 2×3² and our 8×8 grid.

2²×3=12 divides into balanced 6+6 and further into 3+3, creating perfect symmetry. 12 divides by 3, giving 4, then by 2, reinforcing balance. No two primes sum to 12 or 6.

Conversely, 2×3² divides by 2 and 3 but also equals prime pairs 5+13, 7+11, 17+1. The most balanced is 7+11. The two most balanced distributions of 11 are 6+5 and 7+4.

This contrast shows 2²×3 produces balanced even numbers while 3²×2 creates imbalanced prime structures, but also suggests that the more balanced and symmetrical patterns precede the dynamic patterns, which we also see in the patterns of the **DESCENDING** and ***Ascending***, suggesting **DESCENDING** precedes ***Ascending***.

Our 8×8 grid shows pairs summing to 7. The set containing the number that form two 11s, which were arrived at by reconstructing 11 as evenly as possible, and 11 was arrived at by deconstructing 18 into its prime numbers as evenly as possible. If we have the set {{6,5},{7,4}}, then we implicitly have the complementary set of {{1,2},{0,3}} necessary to have sums that pair to 7. This makes the {{6,5},{7,4}} set the explicit or defining set, and {{1,2},{0,3}} the implicit or contributing set, as its complement.

Referring back to the polar chart, we notice the order of cardinal pairs differs between their sequential binary values and their positions on the polar star-chart (starting from the top and rotating clockwise). This is because the cardinal polar pairs define the "cardinal" themes, while the 32 paths or pairs define archetypes that can play out in those themes in either an ascending or descending fashion. Hierarchically speaking, the 32 pairs are expressed within the cardinal themes; the cardinal themes are tholons, and the 32 pairs are partons. However, they are also tholons as well, each with two partons of ascending and descending hexagrams, which are tholons that include two partons of trigrams, which are tholons that include three partons of lines, which form a fundamental or primary tholon.

This 8×8 grid shows several interesting relationships between the ascending and descending principles.

You can understand how this 8×8 chart was arrived at by looking at the two lists of cardinal hexagrams below. The list on the left is the first 8 pairs in sequential binary order or the order of the 32 pairs, and the list on the right is in the order of the 8 cardinal points on the polar chart, out of the 64 points in total. Each line is assigned the number of its position, and as each position has an ascending (green) and descending (red) property, each position has two entries. The items are numbered 0–7. The matching descending items are then connected (right image), as are the ascending items (left image).

<center><img src='../Images/pol-seq-xover.png' style='width:100%'/></center>

We can see the connecting pattern for descending hexagrams is perfectly symmetrical, but when we do the same for the ascending hexagrams, it looks radically different. Although not symmetrical, it's still a clear pattern, but a very dynamic one, with two diagonal lines moving up and down inside two parallel lines. Here again, we see the duality of structure and order in the domain of the descending, and that of movement in the domain of the ascending.

However, its true pattern becomes clear when we plot these relationships, as you will soon see.

We end up with the following connecting pairs of descending hexagrams: (0, 0), (1, 4), (2, 2), (3, 6), (4, 1), (5, 5), (6, 3), (7, 7), which are then plotted as shown above and in the image below (right).

When we connect the ascending pairs (left image), we get: (0, 0), (1, 4), (2, 6), (3, 2), (4, 7), (5, 3), (6, 5), (7, 1).

The two 8×8 plots are shown below

<center><img src='../Images/polar-binary.png' style='width:100%'/></center>

There are several fantastic patterns to explore; for example:

<img src="/home/jw/src/iching_cli/book/intro/Images/ad-quark.png" style='float:right;width:15%'/>The change that needs to occur to transform the ascending to the descending is: [1] down 3, [2] down 1, [3] up 1, [5] down 1, [6] up 1, [7] up 3.  [0] and [4] do not change.

The first thing that comes to mind is this is the exact same “pattern” that we see in how quarks form protons and neutrons, because the proton is composed of two *up* quarks and one *down* quark, while the neutron is composed of one *up* quark and two *down* quarks. This correlation tells us that the ascending hexagrams {4,5,6,7} share this property with the imbalanced positively charged proton, and the descending hexagrams {0,1,2,3} share this property with the balanced neutrally charged neutron. Additionally, given that *up* quarks have a charge of +1/3 and *down* quarks have a charge of -1/3, if we apply these values to each *up* or *down* movement, we end up with all the total down movements = 1 and all the total up movements = 1.

Another truly mind-blowing observation (for me, at least) is not only the fractal nature of numbers, but the emergence of perfectly integrated structures composed of static and dynamic patterns that naturally evolve simply by examining the various perspectives that a larger multidimensional structure naturally presents when projected onto two dimensions. We see a perfectly ordered pattern in the Descending Hexagrams 8×8 plot, but a seemingly disordered pattern in the Ascending Hexagrams plot. However, when we combine them, a new pattern emerges that seems to reference the 10 pairs of stable hexagrams and the 22 pairs of dynamic hexagrams. Furthermore, we observe a triad with the exact same color mapping as a tholon, where the yellow 4 represents the child *Negotiated* *N*-state (which is always the opposite of its parent, represented by the blue *N*-state), the green 7 as *Limitation/Definition*, and the red 1 as *Contribution/Integration*. This suggests that 7 is the limiting or defining concept, which would certainly be true in an octal system, which we are using, where any single digit cannot exceed 7. This is why the maximum value of the hexagrams in octal is 77, which equated to 63.

This would make 1, which appears on the point of *Contribution/Integration*, the contributing concept, which is quite intuitive considering that 1 is the fundamental unit, the concept of unification, the source of emergence, and primordial in that it is fundamentally indivisible and necessary for any numerical formation.

<img src="/home/jw/src/iching_cli/book/intro/Images/10-22.png" style='float:right;width:25%'/>This triad also forms two number pyramids: the central and larger pyramid starts with {4} → {3, 4, 5} → {2, 3, 4, 5, 6} → {1, 2, 3, 4, 5, 6, 7}, and the smaller pyramid that emerges from 0 starts with {1} → {1, 2} → {1, 2, 3} → {1, 2, 3, 4}. We know this because all the numbers in both number pyramids perfectly align with the grid numbers.

If we represent the sum of each row as octals, we get ***o***4 + ***o***14 + ***o***24 + ***o***34 = ***o***100 (which equals 64 in decimal), and this only happens if we start with 4. This is remarkable because the total number of hexagrams in octal is ***o***100 (which equals 64 in decimal)!

On the {4, 7} vector, we have a "scope" of 11 by adding 4 + 7, and within that scope there exist two 11s (5+6 two times), or 2 × the value of the scope, making the value of the entire line 11 + (11 + 11) = 3×11

On the {4, 1} vector, there is also a scope of 5 by adding 4 + 1, and within that scope there exist two 5s (2+3 two times), or 2 × the value of the scope, making the value of the entire line 5 + (5 + 5) = 3×5

This establishes a clear pattern for the vector values, with ‘5’ for the left vector and ‘11’ for the right vector, and the vectors themselves divided into three parts. Naturally, 11 + 5 = 16, which matches the number of original hexagrams needed to create the 64 hexagrams.

We also see that the difference between *N* and the points *D* and *C* are positive and negating values for 3;  4-7=-3 and 4-1=3. 

Given that of the 32 pairs of hexagrams, the 10 balanced pairs fall on the {4,1} vector, while the 22 imbalanced or dynamic pairs fall on the {4,7} vector, these two vectors can be described as:

<img src="/home/jw/src/iching_cli/book/intro/Images/left-right.png" style='width:80%'/>

Ironically, the the {4,1} vector that appears to be more *Definition/Limitation* and the {7,7} vector seems more *Contribution/Integration*, but this is easily solved if we simply reverse the arbitrary X-axis order to descend from 7 to 0 rather than ascend from 0 to 7, which I should have done initially knowing that “Descending precedes Ascending”, as we discovered earlier.

In any case, this is a fascinating example of symmetry, self-similarity, and harmonic balance.

Of course, all these amazing patterns and relationships are simply the effect of deterministic mathematics, and there is nothing "special" about them. However, from the Tholonic perspective, this only confirms the idea that such patterns are found in all creations across all scopes and contexts, which is really what we are interested in. What is “special” is how these patterns support the model of the Tholonic I Ching, which is most evident in the only two positions that do not change, the [0] and [4], which are the extreme top and bottom points of 2䷁*~0~* ***Receptive*** ⇔ 1䷀*~63~* **CREATIVE** and 24䷗*~1~* ***Return*** ⇔ 44䷫*~62~* **COMING TO MEET** that define the entire spectrum and the vertical axis. Not only can we map these two sets of four points to a tetrahedron, they can be perfectly mapped to a parent and child tholon and even the two trigrams and six lines of the hexagrams where *NDC* properties and the I Ching archetypes align perfectly.

