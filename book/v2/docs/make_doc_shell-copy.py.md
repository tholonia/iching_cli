# make_doc_sh.py

## Shell Script Documentation Collector

### Description
This script scans the current directory for shell script files (*.sh), extracts their documentation comments, and compiles them into a single markdown file with an index of script usages at the top.

### Usage
```bash
./make_doc_sh.py
```

### Process
1. Scans the current directory for *.sh files
2. For each shell script file:
   - Extracts the comment block at the top of the file
   - Extracts usage information
   - Converts to markdown format
3. Creates a script list and usage index
4. Combines all sections into `doc_sh.md`

### Output
- `doc_sh.md`: Combined markdown documentation with script list and usage index

### Author
Assistant

*Last Updated:* 10-11-2023 14:30
```
(Note: You can set the current date and time in MM-DD-YYYY HH:MM format as appropriate for *Last Updated:* at the end of the markdown.)

---

