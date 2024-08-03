# I Ching (CLI)

This is a command-line version of the I Ching that uses the original yarrow stick method as the algorithm for determining each line. By default, it uses the python random library but using the "-r" option on the command line makes a call to random.org to get a true random numbers, which, in my experience, makes a significant difference.

The output is sent to the console using ANSI codes and to a markdown file whose file name is determined by the input question. The default question is the string "test mode". To add a custom question you can use the "-q 'your question here' " command-line argument and pass in a question string.

The interpretations for the hexagram come from The Wilhelm Baines version of the I-Ching. Some of the formatting in that text is a little off and there may occasionally be notes that I have added that will probably make no sense to anybody but me.

The original algorithm used for the yarrow stick method was a JavaScript function that comes from https://github.com/Brianfit/I-Ching/blob/master/yarrow-sort.js

Much credit to the author of this function because my attempts to create a python version of the yarrow stick process was far more difficult than I thought it would be, and I never got it working, so I just took the JavaScript code and converted that to python.

### Example

```
./throw.py -q "Is now a time of action or stillness?" -r
./throw.py --question "Is now a time of action or stillness?" --true_random
```

This command outputs to an ANSI terminal and to the file `Q_Is_now_a_time_of.md` (The file name is determined by the first 16 characters of the question)

Porting from JavaScript to python imposed quite a number of design decisions that are less than ideal. On top of that, the rest of the code is a bit primitive as well. Nevertheless it works, so this will be added to my long list of projects that need to be polished and optimized.

