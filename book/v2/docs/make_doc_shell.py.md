To convert the shell script's documentation comment into markdown format using the specified template, you'll first need to extract the relevant docstring content from the script. Here's an example based on a hypothetical shell script docstring:

Assuming the shell script docstring is:

```shell
: '
# MyScript

## This script is a demo program for processing data.

### Description
This script processes data from specified input files and generates a summary.

### Usage
./myscript.sh [options] inputfile

### Options
-h, --help     Display help message
-v, --version  Display program version
'
```

The corresponding markdown document would be:

```markdown
# MyScript

## This script is a demo program for processing data.

### Description
This script processes data from specified input files and generates a summary.

### Usage
./myscript.sh [options] inputfile

### Options
-h, --help     Display help message
-v, --version  Display program version

*Last Updated:* MM-DD-YYYY HH:MM
```

Replace `MM-DD-YYYY HH:MM` with the actual date and time when you generate the markdown document. For example, if the document was generated on October 10th, 2023 at 15:30, you'll write it as `10-10-2023 15:30`.

---

