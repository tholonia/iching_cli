# I Ching (CLI)

This is a command-line version of the I Ching that uses the original yarrow stick method as the algorithm for determining each line. By default, it uses the python random library but using the "-r" option on the command line makes a call to random.org to get a true random numbers, which, in my experience, makes a significant difference.

The output is sent to the console using ANSI codes and to a markdown file whose file name is determined by the input question. The default question is the string "test mode". To add a custom question you can use the "-q|--question 'your question here' " command-line argument and pass in a question string.

The interpretations for the hexagram come from The Wilhelm Baines version of the I-Ching, which uses the King Wen sequence of hexagrams. Some of the formatting in the text is a little off and there may occasionally be notes that I have added that will probably make no sense to anybody but me, as this data was ported from a previous web-based versions that was far more comprehensive and interactive.

The original algorithm used for the yarrow stick method was a JavaScript function that comes from https://github.com/Brianfit/I-Ching/blob/master/yarrow-sort.js

Much credit to the author of this function because my attempts to create a python version of the yarrow stick process was far more difficult than I thought it would be, and I never got it working, so I just took the JavaScript code and converted that to python.

Porting from JavaScript to python imposed quite a number of design decisions that are less than ideal. On top of that, the rest of the code is a bit primitive as well. Nevertheless it works, so this will be added to my long list of projects that need to be polished and optimized.

---

## ```throw.py``` examples

#### View a hexagram by binary value 0

```bash
./throw.py --binary 0
```
> Binary value range from 0 (000000) to 63 (111111)

#### View a hexagram by classic value 1 (not yet implemented)

```bash
./throw.py --classic 1
```
> Classic arrangements of hexagrams (King Wen order) ranges from 1 to 64

#### Ask a question using true random data from [RANDOM.ORG](random.org) (slow)

```bash
# obfuscated... ./throw.py --question "Should I?" --true_random
./throw.py --question "Should I?"
```
> Questions can be as long as necessary.  The first 16 character of the question are used to create a filename of the output, for example "Q_should_I.txt".  In my experience true random numbers are far more effective that pseudo-random numbers, but are slightly slower, and requires an Internet connection.  By default, pseudo-random numbers are used.


## ```update.py``` examples

```bash
./update.py --bin 0 --comment
```
> Commens can be added to a hexagram by selecting the bunary valus of the hexagram (`--bin 0`) and setting the the comment prefix value to some text.  An example os setting comments is:
```bash
./update.py -b 33 --comment '#1 "cause" of the pair b33:b35 (c27:b41) "CORNERS OF THE MOUTH (PROVIDING NOURISHMENT)" ⮕ "DECREASE"'
./update.py -b 33 --comment '#2 "effect" of the pair b33:b35 (c27:b41) "CORNERS OF THE MOUTH (PROVIDING NOURISHMENT)" ⮕ "DECREASE"'
```
> In this example, we create two comment, one for the first hexagram and one for the second.  The binary sequence values are preceeded by 'b' and the classical sequence values are preceeded by 's'.  If only one hexagram was prodcued with no moving lines, the comment command would be...
```bash
./update.py -b 0 --comment 'Non-moving hexagram of b0 (c2) "The Receptive"'
```

> The text is perpended to the content of the file `latest_comment.txt`, which needs to be filled out before running this command.  If teh contents of `latest_comment.txt` is `As I had just won lotto, I interpreted this as message to be careful on how I spent my new-found fotrune", then the comment saved for the hexagrams respectively woudl be:

```
#1 "cause" of the pair b33:b35 (c27:b41) "CORNERS OF THE MOUTH (PROVIDING NOURISHMENT) :: As I had just won lotto, I interpreted this as message to be careful on how I spent my new-found fortune
```
> saved as a comment to hexagram b33
```
#2 "effect" of the pair b33:b35 (c27:b41) "CORNERS OF THE MOUTH (PROVIDING NOURISHMENT)" ⮕ "DECREASE" :: As I had just won lotto, I interpreted this as message to be careful on how I spent my new-found fortune
```
> saved as a comment to hexagram b35
```
Non-moving hexagram of b0 (c2) "The Receptive" :: As I had just won lotto, I interpreted this as message to be careful on how I spent my new-found fortune
```
> saved as a comment to hexagram b0

#### Make dump backups of all databases (`hexagrams.db` and `trigrams.db`)

```bash
./update.py --dump
```
> this saves a dated SQL dump oif each database, for example:
```bash
hexagrams_08_12_2024.sql
trigrams_08_12_2024.sql
```

#### Reload database from specific backup

```bash
./update.py --reload hexagrams_08_12_2024.sql
```
> This deletes the database and creates a new instance

# Example output

---

# Question: test mode

```
━━━━━━━━━×
───   ─── 
━━━   ━━━∘
───────── 
━━━━━━━━━×
───   ─── 
```

**TITLE**:    Ku 
**TRANS**:    WORK ON WHAT HAS BEEN SPOILED [ DECAY ]
**SEQUENCE**: 38 (100110)
**ORDER**:    18 (I-Ching order)

**UPPER_TRIGRAM**: The Gentle (SUN), Wind & Wood, Feminine Understanding, Mercury
**LOWER_TRIGRAM**: Keeping Still (KeN), Mountain, Feminine Creative, Earth

**EXPLANATION**:

> The Chinese character ku represents a bowl in whose contents worms are breeding. This means decay. IT is come about because the gentle indifference in the lower trigram has come together with the rigid inertia of the upper,and the result is stagnation. Since this implies guilt, the conditions embody a demand for removal of the cause. Hence the meaning of the hexagram is not simply "what has been spoiled" but "work on what has been spoiled".

**JUDGMENT**:

> WORK ON WHAT HAS BEEN SPOILED Has supreme success.
> It furthers one to cross the great water.
> Before the starting point, three days.
> After the starting point, three days.

**JUDGMENT EXPLANATION**:

> What has been spoiled through man's fault can be made good again through man's work. IT is not immutable fate, as in the time of STANDSTILL, that has caused the state of corruption, but rather the abuse of human freedom. Work Toward improving conditions promises well, because it accords the possibilities of the time. We must not recoil from work and danger-symbolized by crossing of the great water-but must take hold energetically. Success depends, however, on proper deliberation. This is expressed by the lines,"Before the starting point, three days. After the starting point, three days."We must first know the cause of corruption before we can do away with them;hence it is necessary to be cautious during the time before the start. Then we must see to it that the new way is safely entered upon, so that a relapse maybe avoided; therefore we must pay attention to the time after the start.Decisiveness and energy must take the place of inertia and indifference that have led to decay, in order that the ending may be followed by a new beginning.

**COMMENTS**:

> None




**MOVING LINES**
**Nine in the second place means:**

>*Setting right what has been spoiled by the mother,
>One must not be too persevering.*
>This refers to mistakes that as a result of weakness have brought about decay-hence the symbol, "what has been spoiled by the mother. " In setting things right in such a case, a certain gentle consideration is called for. In order not to wound, one should not attempt to proceed too drastically.

**Six in the fourth place means:**

>*Tolerating what has been spoiled by the father.
>In continuing one sees humiliation.*
>This shows the situation of someone too weak to take measures against decay that has its roots in the past and is just beginning to manifest itself. It is allowed to run its course. If this continues, humiliation will result.

**Nine at the top means:**

>*He does not serve kings and princes,
>Sets himself higher goals.*
>Not every man has an obligation to mingle in the affairs of the world. There are some who are developed to such a degree that they are justified in letting the world go its own way and refusing to enter public life with a view to reforming it. But this does not imply a right to remain idle or to sit back and merely criticize. Such withdrawal is justified only when we strive to realize in ourselves the higher aims of mankind. For although the sage remains distant from the turmoil of daily life, he creates incomparable human values for the future.

```
───   ─── 
───   ─── 
───────── 
───────── 
───   ─── 
───   ─── 
```

**TITLE**:    Hsiao Kuo 
**TRANS**:    Preponderance of the Small
**SEQUENCE**: 12 (100110)
**ORDER**:    62 (I-Ching order)

**UPPER_TRIGRAM**: Keeping Still (KeN), Mountain, Feminine Creative, Earth
**LOWER_TRIGRAM**: The Arousing (CHeN), Thunder, Masculine Expanding, Mars

**EXPLANATION**:

> While in the hexagram Ta Kuo, PREPONDERANCE OF THE GREAT 

|28, the strong lines preponderate and are within, inclosed between weak lines at the top and bottom, the present hexagram has weak lines preponderating, though here again they are on the outside, the strong lines being within. This indeed is the basis of the exceptional situation indicated by the hexagram. When strong lines are outside, we have the hexagram I,PROVIDING NOURISHMENT 

|27, or Chung Fu, INNER TRUTH, 

|61; neither represents an exceptional state. When strong elements within preponderate, they necessarily enforce their will. This creates struggle and exceptional conditions in general. But in the present hexagram it is the weak element that perforce must mediate with the outside world. If a man occupies a position of authority for which he is by nature really inadequate,extraordinary prudence is necessary.

**JUDGMENT**:

> PREPONDERANCE OF THE SMALL.
> Success.
> Perseverance furthers.
> Small things may be done; great things should not be done.

**JUDGMENT EXPLANATION**:

> The flying bird brings the message: It is not well to strive upward, It is well to remain below. Great good fortune. 

|Exceptional modesty and conscientiousness are sure to be rewarded with success; however, if a man is not to throw himself away, it is important that they should not become empty form and subservience but be combined always with a correct dignity in personal behavior. We must understand the demands of the time in order to find the necessary offset for its deficiencies and damages.In any event we must not count on great success, since the requisite strength is lacking. In this lies the importance of the message that one should not strive after lofty things but hold to lowly things. The structure of the hexagram gives rise to the idea that this message is brought by a bird. In Ta Kuo, PREPONDERANCE OF THE GREAT 

|28, the four strong, heavy lines within, supported only by two weak lines without, give the image of a sagging ridgepole. Here the supporting weak lines are both outside and preponderant; this gives the image of a soaring bird. But a bird should not try to surpass itself and fly into the sun; it should descend to the earth, where its nest is. In this way it gives the message conveyed by the hexagram.

**COMMENTS**:

> None

---



# Install

This was written in Python 3.10.14, but it should run on any 3.x version.

The only modules needed are `colorama` and `sqlite3`

```bash
pip install colorama sqlite3
```
On Linux, make the scripts executable 
```bash
chmod 755 *py
# then run 
./throw.py <args>
./update.py <args>
```
On Windows, as there is no `shebang` expressions, you need to run
```bash
python ./throw.py <args>
python ./update.py <args>
```
[Download Python for Windows](https://www.python.org/downloads/windows/) (includes pip)


# About

This is part of the Tholonia Project, which has an interest in the I-Ching as it is attempting to reinterpret the I-Ching by reverse-engineering and reconstructing the original reasoning behind its creation and use.  The draft of this effort is available in a book form at https://tholonia.com/material/book_ICHING_THE_BOOK.html.
