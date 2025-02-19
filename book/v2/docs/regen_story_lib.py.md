# regen_story_lib.py

## Story Generation Library for I Ching

### Description
This library provides functions and schemas for generating stories based on I Ching hexagrams. It defines the structure for story generation prompts and responses, ensuring consistent story formats that align with hexagram interpretations.

### Usage
Import and use in other scripts:
```python
from regen_story_lib import make_prompt, stories_schema
```

Example:
```python
prompt = make_prompt(hexagram_number=1, story_idx=0)
```

### Core Components
1. **Story Types:**
   - Man vs. Man
   - Man vs. Nature
   - Man vs. Self

2. **Schema Structure:**
   - Title
   - Theme
   - Short Story (~200 words)
   - Lines in Context (6 lines with interpretations)

3. **Line Interpretations:**
   - Name: Central concept
   - Meaning: Significance in story
   - Changing: Effect when line changes

### Functions
`make_prompt(hexagram_number, story_idx)`
- Generates a complete prompt for story generation using:
  - I Ching primer
  - Tholonic primer
  - Hexagram-specific content
  - Story structure guidelines

### Schema Validation
- Enforces story length limits
- Validates line interpretations
- Ensures complete hexagram coverage
- Maintains consistent structure

### Dependencies
- json
- os
- sys

*Author:* Assistant  
*Last Updated:* 03-21-2024 12:00

---

