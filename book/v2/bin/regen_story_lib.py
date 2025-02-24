#!/usr/bin/env python3

"""
=============================================================================
regen_story_lib.py - Story Generation Library for I Ching
=============================================================================

Description:
  This library provides functions and schemas for generating stories based on
  I Ching hexagrams. It defines the structure for story generation prompts
  and responses, ensuring consistent story formats that align with hexagram
  interpretations.

Usage:
  Import and use in other scripts:
    from regen_story_lib import make_prompt, stories_schema

  Example:
    prompt = make_prompt(hexagram_number=1, story_idx=0)

Core Components:
  1. Story Types:
     - Man vs. Man
     - Man vs. Nature
     - Man vs. Self

  2. Schema Structure:
     - Title
     - Theme
     - Short Story (~200 words)
     - Lines in Context (6 lines with interpretations)

  3. Line Interpretations:
     - Name: Central concept
     - Meaning: Significance in story
     - Changing: Effect when line changes

Functions:
  make_prompt(hexagram_number, story_idx)
    Generates a complete prompt for story generation using:
    - I Ching primer
    - Tholonic primer
    - Hexagram-specific content
    - Story structure guidelines

Schema Validation:
  - Enforces story length limits
  - Validates line interpretations
  - Ensures complete hexagram coverage
  - Maintains consistent structure

Dependencies:
  - json
  - os
  - sys

Author: Assistant
Last Updated: 2024-03-21
=============================================================================
"""

import json
import os
import sys
from colorama import Fore, Style
from dotenv import load_dotenv

load_dotenv()

max_words=200

story_type = [
    ["Man vs. Man", "set in a material, practical, mundane world of human interaction (e.g. business, politics, etc.) where men are pit against men"],
    ["Man vs. Nature", "set in a natural world of plants, animals, and the elements (e.g. mountains, rivers, etc.) where man is pitted against nature"],
    ["Man vs. Self", "set in a world of introspection, self-discovery, and personal growth (e.g. a quest for meaning, a search for truth, etc.) where man is pitted against himself."]
]


stories_schema = {
      "type": "object",
      "properties": {
        "title": {
          "type": "string"
        },
        "entries": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "title": {
                "type": "string"
              },
              "theme": {
                "type": "string"
              },
              "short_story": {
                "type": "string"
              },
              "lines_in_context": {
                "type": "object",
                "properties": {
                  "6": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string"
                      },
                      "meaning": {
                        "type": "string"
                      },
                      "changing": {
                        "type": "string"
                      }
                    },
                    "required": [
                      "name",
                      "meaning",
                      "changing"
                    ]
                  },
                  "5": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string"
                      },
                      "meaning": {
                        "type": "string"
                      },
                      "changing": {
                        "type": "string"
                      }
                    },
                    "required": [
                      "name",
                      "meaning",
                      "changing"
                    ]
                  },
                  "4": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string"
                      },
                      "meaning": {
                        "type": "string"
                      },
                      "changing": {
                        "type": "string"
                      }
                    },
                    "required": [
                      "name",
                      "meaning",
                      "changing"
                    ]
                  },
                  "3": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string"
                      },
                      "meaning": {
                        "type": "string"
                      },
                      "changing": {
                        "type": "string"
                      }
                    },
                    "required": [
                      "name",
                      "meaning",
                      "changing"
                    ]
                  },
                  "2": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string"
                      },
                      "meaning": {
                        "type": "string"
                      },
                      "changing": {
                        "type": "string"
                      }
                    },
                    "required": [
                      "name",
                      "meaning",
                      "changing"
                    ]
                  },
                  "1": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string"
                      },
                      "meaning": {
                        "type": "string"
                      },
                      "changing": {
                        "type": "string"
                      }
                    },
                    "required": [
                      "name",
                      "meaning",
                      "changing"
                    ]
                  }
                },
                "required": [
                  "6",
                  "5",
                  "4",
                  "3",
                  "2",
                  "1"
                ]
              }
            },
            "required": [
              "title",
              "theme",
              "short_story",
              "lines_in_context"
            ]
          }
        }
      },
      "required": [
        "title",
        "entries"
      ]
    }
history_schema = {
      "type": "object",
      "properties": {
        "title": {
          "type": "string"
        },
        "subtitle": {
          "type": "string"
        },
        "summary": {
          "type": "string"
        },
        "source": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "lines_in_history": {
          "type": "object",
          "properties": {
            "6": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string"
                },
                "meaning": {
                  "type": "string"
                },
                "changing": {
                  "type": "string"
                }
              },
              "required": [
                "name",
                "meaning",
                "changing"
              ]
            },
            "5": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string"
                },
                "meaning": {
                  "type": "string"
                },
                "changing": {
                  "type": "string"
                }
              },
              "required": [
                "name",
                "meaning",
                "changing"
              ]
            },
            "4": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string"
                },
                "meaning": {
                  "type": "string"
                },
                "changing": {
                  "type": "string"
                }
              },
              "required": [
                "name",
                "meaning",
                "changing"
              ]
            },
            "3": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string"
                },
                "meaning": {
                  "type": "string"
                },
                "changing": {
                  "type": "string"
                }
              },
              "required": [
                "name",
                "meaning",
                "changing"
              ]
            },
            "2": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string"
                },
                "meaning": {
                  "type": "string"
                },
                "changing": {
                  "type": "string"
                }
              },
              "required": [
                "name",
                "meaning",
                "changing"
              ]
            },
            "1": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string"
                },
                "meaning": {
                  "type": "string"
                },
                "changing": {
                  "type": "string"
                }
              },
              "required": [
                "name",
                "meaning",
                "changing"
              ]
            }
          },
          "required": [
            "6",
            "5",
            "4",
            "3",
            "2",
            "1"
          ]
        }
      },
      "required": [
        "title",
        "subtitle",
        "short_story",
        "source",
        "lines_in_history"
      ]
    }

def make_history_prompt(hexagram_number):
    iching_primer_path = "../includes/iching_primer.md"
    tholonic_primer_path = "../includes/tholonic_primer.md"
    local_hexagram_path = f"../regen/{hexagram_number}.json"

    opposite_line_type = {
        "yang": "yin",
        "yin": "yang"
    }

    with open(iching_primer_path, "r", encoding="utf-8") as f:
        iching_primer_content = f.read()

    with open(tholonic_primer_path, "r", encoding="utf-8") as f:
        tholonic_primer_content = f.read()

    with open(local_hexagram_path, "r", encoding="utf-8") as f:
        hexagram_content = json.load(f)

    # Define the expected JSON response structure
    prompt_reply_structure = {

        "title": "Title of historical story",
        "subtitle": f"\"{hexagram_content['name']}\" in History",
        "short_story": f"Describe historical event in approx. {max_words} words",
        "source": [ "list sources 1", "list sources 2","etc..." ],
        "lines_in_history": {
            "6": {
                "name": "Line 6 name",
                "meaning": "Line 6 meaning",
                "changing": f"Describe both challenges (disruptions, imbalances, or lessons that arise from the change) and potential benefits (new insights, opportunities, or higher-order growth made possible by the transformation) resulting from line 6  {hexagram_content['line_type'][0]} changing to {opposite_line_type[hexagram_content['line_type'][0]]} in the context of Transcendence and this story.  DO NOT describe the effects {opposite_line_type[hexagram_content['line_type'][0]]} changing to {hexagram_content['line_type'][0]}  because that is impossible given that line 6 is {hexagram_content['line_type'][0]}.",
            },
            "5": {
                "name": "Line 5 ",
                "meaning": "Line 5 meaning",
                "changing": f"Describe both challenges (disruptions, imbalances, or lessons that arise from the change) and potential benefits (new insights, opportunities, or higher-order growth made possible by the transformation) resulting from line 5  {hexagram_content['line_type'][1]} changing to {opposite_line_type[hexagram_content['line_type'][1]]} in the context of Mastery and this story.  DO NOT describe the effects {opposite_line_type[hexagram_content['line_type'][1]]} changing to {hexagram_content['line_type'][1]}  because that is impossible given that line 5 is {hexagram_content['line_type'][1]}.",
            },
            "4": {
                "name": "Line 4 ",
                "meaning": "Line 4 meaning",
                "changing": f"Describe both challenges (disruptions, imbalances, or lessons that arise from the change) and potential benefits (new insights, opportunities, or higher-order growth made possible by the transformation) resulting from line 4  {hexagram_content['line_type'][2]} changing to {opposite_line_type[hexagram_content['line_type'][2]]} in the context of Manifestation and this story.  DO NOT describe the effects {opposite_line_type[hexagram_content['line_type'][2]]} changing to {hexagram_content['line_type'][2]}  because that is impossible given that line 4 is {hexagram_content['line_type'][2]}.",
            },
            "3": {
                "name": "Line 3 ",
                "meaning": "Line 3 meaning",
                "changing": f"Describe both challenges (disruptions, imbalances, or lessons that arise from the change) and potential benefits (new insights, opportunities, or higher-order growth made possible by the transformation) resulting from line 3  {hexagram_content['line_type'][3]} changing to {opposite_line_type[hexagram_content['line_type'][3]]} in the context of Conflict and this story.  DO NOT describe the effects {opposite_line_type[hexagram_content['line_type'][3]]} changing to {hexagram_content['line_type'][3]}  because that is impossible given that line 3 is {hexagram_content['line_type'][3]}.",
            },
            "2": {
                "name": "Line 2 ",
                "meaning": "Line 2 meaning",
                "changing": f"Describe both challenges (disruptions, imbalances, or lessons that arise from the change) and potential benefits (new insights, opportunities, or higher-order growth made possible by the transformation) resulting from line 2  {hexagram_content['line_type'][4]} changing to {opposite_line_type[hexagram_content['line_type'][4]]} in the context of Formation and this story.  DO NOT describe the effects {opposite_line_type[hexagram_content['line_type'][4]]} changing to {hexagram_content['line_type'][4]}  because that is impossible given that line 2 is {hexagram_content['line_type'][4]}.",
            },
            "1": {
                "name": "Line 1",
                "meaning": "Line 1 meaning",
                "changing": f"Describe both challenges (disruptions, imbalances, or lessons that arise from the change) and potential benefits (new insights, opportunities, or higher-order growth made possible by the transformation) resulting from line 1  {hexagram_content['line_type'][5]} changing to {opposite_line_type[hexagram_content['line_type'][5]]} in the context of Emergence and this story.  DO NOT describe the effects {opposite_line_type[hexagram_content['line_type'][5]]} changing to {hexagram_content['line_type'][5]}  because that is impossible given that line 1 is {hexagram_content['line_type'][5]}.",
            }
        }
    }



    prompt = f"""
# Prepare the prompt for the OpenAI API

Tholonic Primer:
{tholonic_primer_content}

I Ching Primer:
{iching_primer_content}

Hexagram {hexagram_number}:
{json.dumps(hexagram_content, indent=2)}

Using the context provided above, identify a historical event that is relevant to hexagram {hexagram_number} from the I Ching.  Then generate a short story of approximately {max_words} words that represents the essence and significance of the historical event. The story should be engaging and immersive, demonstrating the themes of raw creative force, unrestrained potential, and the process of realization.

For the given I Ching hexagram, provide a comprehensive interpretation of each of its six lines. In your analysis, consider the line's position within the hexagram, its natural Yin (⚋) or Yang (⚊) state, and its relationship with adjacent lines. Discuss how deviations from the natural Yin-Yang sequence influence the line's meaning, and explain the interplay between the inner (lines 1-3) and outer (lines 4-6) trigrams. Highlight how these interactions reflect the principles of negotiation (balance), limitation (definition), and contribution (integration)."

Explanation:

Line Position and Natural State: Each line in a hexagram has a designated position (1 through 6) and an associated natural state—either Yin (⚋) or Yang (⚊). Understanding this helps in interpreting the line's role and influence within the hexagram.

Adjacent Line Relationships: Lines influence and are influenced by their neighboring lines. Analyzing these relationships provides insight into the dynamics and potential tensions within the hexagram.

Deviations from Natural Sequence: A line that deviates from its expected Yin or Yang state can indicate imbalance or transformation, affecting the overall interpretation.

Inner and Outer Trigrams: The lower trigram (lines 1-3) represents internal conditions, while the upper trigram (lines 4-6) reflects external manifestations. Exploring their interplay offers a deeper understanding of the hexagram's message.

Principles of Negotiation, Limitation, and Contribution: These principles relate to balance, definition, and integration within the hexagram. Incorporating them into the analysis provides a holistic view of the forces at play.

### Story Structure:
- The event should have a clear message that embodies the six stages of creation, conflict, manifestation, mastery, conflict, and transcendence.
- The **title** should capture the essence of the story in a compelling way.
- The story should be written in the style of historians, such as Joan Evans, Dorothy Mills, C.W Ceram, Bernard Cornwell, and Alison Weir, using a strong and recognizable literary voice.  IMPORTANT: Ensure that the story sounds different from the other stories
- The **short_story** should be approximatly {max_words} words and that captures the essence of the story's main conflict, themes, and resolution.

### Hexagram Structure in Story Progression:
The story should be divided into six stages corresponding to the six lines of hexagram {hexagram_number}. For each line:
- The current line type is specified in hexagram_content['line_type']
- Only describe what happens when the CURRENT line changes to its OPPOSITE
- For a yang line (─), describe only yang→yin changes
- For a yin line (--), describe only yin→yang changes

1. **Line 1 name should reflect the essential quality of Emergence as it appears in this story"**
   - Meaning: a description of how this quality of Emergence is instantiated."
   - Changing: Decribe both challenges (disruptions, imbalances, or lessons that arise from the change) and potential benefits (new insights, opportunities, or higher-order growth made possible by the transformation) resulting from line 1  {hexagram_content['line_type'][5]} changing to {opposite_line_type[hexagram_content['line_type'][5]]} in the context of Emergence and this story.  DO NOT describe the effects {opposite_line_type[hexagram_content['line_type'][5]]} changing to {hexagram_content['line_type'][5]}  because that is impossible given that line 1 is {hexagram_content['line_type'][5]}. "

2. **Line 2 name should reflect the essential quality of Formation as it appears in this story"**
   - Meaning: a description of how this quality of Formation is instantiated."
   - Changing: Decribe both challenges (disruptions, imbalances, or lessons that arise from the change) and potential benefits (new insights, opportunities, or higher-order growth made possible by the transformation) resulting from line 2  {hexagram_content['line_type'][4]} changing to {opposite_line_type[hexagram_content['line_type'][4]]} in the context of Formation and this story.  DO NOT describe the effects {opposite_line_type[hexagram_content['line_type'][4]]} changing to {hexagram_content['line_type'][4]}  because that is impossible given that line 2 is {hexagram_content['line_type'][4]}. "

3. **Line 3 name should reflect the essential quality of Conflict as it appears in this story"**
   - Meaning: a description of how this quality of Conflict is instantiated."
   - Changing: Decribe both challenges (disruptions, imbalances, or lessons that arise from the change) and potential benefits (new insights, opportunities, or higher-order growth made possible by the transformation) resulting from line 3  {hexagram_content['line_type'][3]} changing to {opposite_line_type[hexagram_content['line_type'][3]]} in the context of Conflict and this story.  DO NOT describe the effects {opposite_line_type[hexagram_content['line_type'][3]]} changing to {hexagram_content['line_type'][3]}  because that is impossible given that line 3 is {hexagram_content['line_type'][3]}. "

4. **Line 4 name should reflect the essential quality of Manifestation as it appears in this story"**
   - Meaning: a description of how this quality of Manifestation is instantiated."
   - Changing: Decribe both challenges (disruptions, imbalances, or lessons that arise from the change) and potential benefits (new insights, opportunities, or higher-order growth made possible by the transformation) resulting from line 4  {hexagram_content['line_type'][2]} changing to {opposite_line_type[hexagram_content['line_type'][2]]} in the context of Manifestation and this story.  DO NOT describe the effects {opposite_line_type[hexagram_content['line_type'][2]]} changing to {hexagram_content['line_type'][2]}  because that is impossible given that line 4 is {hexagram_content['line_type'][2]}.",

5. **Line 5 name should reflect the essential quality of Mastery as it appears in this story"**
   - Meaning: a description of how this quality of Mastery is instantiated."
   - Changing: Decribe both challenges (disruptions, imbalances, or lessons that arise from the change) and potential benefits (new insights, opportunities, or higher-order growth made possible by the transformation) resulting from line 5  {hexagram_content['line_type'][1]} changing to {opposite_line_type[hexagram_content['line_type'][1]]} in the context of Mastery and this story.  DO NOT describe the effects {opposite_line_type[hexagram_content['line_type'][1]]} changing to {hexagram_content['line_type'][1]}  because that is impossible given that line 5 is {hexagram_content['line_type'][1]}. "

6. **Line 6 name should reflect the essential quality of Transcendence as it appears in this story"**
   - Meaning: a description of how this quality of Transcendence is instantiated."
   - Changing: Decribe both challenges (disruptions, imbalances, or lessons that arise from the change) and potential benefits (new insights, opportunities, or higher-order growth made possible by the transformation) resulting from line 6  {hexagram_content['line_type'][0]} changing to {opposite_line_type[hexagram_content['line_type'][0]]} in the context of Transcendence and this story.  DO NOT describe the effects {opposite_line_type[hexagram_content['line_type'][0]]} changing to {hexagram_content['line_type'][0]}  because that is impossible given that line 6 is {hexagram_content['line_type'][0]}. "

IMPORTANT: For each line's "Moving Line" description:
- If the current line is yang (─), only describe what happens when it changes to yin (--)
- If the current line is yin (--), only describe what happens when it changes to yang (─)
- Never describe a yin→yang change for a yang line
- Never describe a yang→yin change for a yin line

### Output Format:
The response should be structured as a JSON object following this template:

```json
{json.dumps(prompt_reply_structure, indent=2)}
```
"""

    # print(Fore.GREEN + prompt + Style.RESET_ALL)
    return prompt

def make_stories_prompt(hexagram_number, story_idx):
    iching_primer_path = "../includes/iching_primer.md"
    tholonic_primer_path = "../includes/tholonic_primer.md"
    local_hexagram_path = f"../regen/{hexagram_number}.json"

    opposite_line_type = {
        "yang": "yin",
        "yin": "yang"
    }

    with open(iching_primer_path, "r", encoding="utf-8") as f:
        iching_primer_content = f.read()

    with open(tholonic_primer_path, "r", encoding="utf-8") as f:
        tholonic_primer_content = f.read()

    with open(local_hexagram_path, "r", encoding="utf-8") as f:
        hexagram_content = json.load(f)

    # Define reusable line template with required fields
    line_template = {
        "name": "Line Name",
        "meaning": "Line Meaning",
        "changing": ""  # Will be populated with specific changing instructions
    }

    # Define changing line instructions for each position
    changing_instructions = {
        "6": f"Describe as concisely as possible both challenges and benefits resulting from line 6 {hexagram_content['line_type'][0]} changing to {opposite_line_type[hexagram_content['line_type'][0]]} in the context of Transcendence and this story.",
        "5": f"Describe as concisely as possible both challenges and benefits resulting from line 5 {hexagram_content['line_type'][1]} changing to {opposite_line_type[hexagram_content['line_type'][1]]} in the context of Mastery and this story.",
        "4": f"Describe as concisely as possible both challenges and benefits resulting from line 4 {hexagram_content['line_type'][2]} changing to {opposite_line_type[hexagram_content['line_type'][2]]} in the context of Manifestation and this story.",
        "3": f"Describe as concisely as possible both challenges and benefits resulting from line 3 {hexagram_content['line_type'][3]} changing to {opposite_line_type[hexagram_content['line_type'][3]]} in the context of Conflict and this story.",
        "2": f"Describe as concisely as possible both challenges and benefits resulting from line 2 {hexagram_content['line_type'][4]} changing to {opposite_line_type[hexagram_content['line_type'][4]]} in the context of Formation and this story.",
        "1": f"Describe as concisely as possible both challenges and benefits resulting from line 1 {hexagram_content['line_type'][5]} changing to {opposite_line_type[hexagram_content['line_type'][5]]} in the context of Emergence and this story."
    }

    # Create lines_in_context structure
    lines_in_context = {}
    for line_num in ["6", "5", "4", "3", "2", "1"]:
        line_data = line_template.copy()
        line_data["changing"] = changing_instructions[line_num]
        lines_in_context[line_num] = line_data

    # Define the expected JSON response structure
    prompt_reply_structure = {
        "title": "Story Title",
        "entries": [{
            "title": "Story Title",
            "theme": "Author's Style",
            "short_story": f"The story text in properly constructed paragraphs (~{max_words} words).",
            "lines_in_context": lines_in_context
        }]
    }

    # Create story requirements section
    story_requirements = f"""
Story Requirements:
- Type: {story_type[story_idx][0]} conflict {story_type[story_idx][1]}
- Length: Approximately {max_words} words
- Structure: Clear progression through six stages
- Format: Properly constructed paragraphs
- Style: Strong literary voice distinct from other stories
- Content: No direct references to hexagrams or lines
"""

    # Create line analysis template
    line_analysis_template = """
Line {num} - {context}:
- Name: Essential quality as it appears in story
- Meaning: How this quality is instantiated
- Changing: Effects when {line_type} changes to {opposite} in context of {context}
"""

    # Generate line analysis sections
    contexts = ["Transcendence", "Mastery", "Manifestation", "Conflict", "Formation", "Emergence"]
    line_analyses = []
    for i, context in enumerate(contexts):
        line_num = 6 - i
        line_type = hexagram_content['line_type'][i]
        opposite = opposite_line_type[line_type]
        line_analyses.append(line_analysis_template.format(
            num=line_num,
            context=context,
            line_type=line_type,
            opposite=opposite
        ))

    # Construct the complete prompt
    prompt = f"""
# Story Generation for Hexagram {hexagram_number}

Tholonic Primer:
{tholonic_primer_content}

I Ching Primer:
{iching_primer_content}

Hexagram {hexagram_number}:
{json.dumps(hexagram_content, indent=2)}

{story_requirements}

Line Analysis:
{''.join(line_analyses)}

IMPORTANT: For each line's "Moving Line" description:
- If the current line is yang (─), only describe what happens when it changes to yin (--)
- If the current line is yin (--), only describe what happens when it changes to yang (─)
- Never describe a yin→yang change for a yang line
- Never describe a yang→yin change for a yin line

Response Format:
```json
{json.dumps(prompt_reply_structure, indent=2)}
```
"""

    return prompt
