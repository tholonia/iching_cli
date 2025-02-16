max_words=200

story_type = [
    "Man vs. Man",
    "Man vs. Nature",
    "Man vs. Self"
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

prompt_reply_structure = {
        "entries": [
            {
                "title": "Generated title of the story.",
                "theme": "The name ONLY of the author whose style this story was written in.",
                "short_story": f"A {max_words} word story that captures the essence of the story's main conflict, themes, and resolution. IMPORTANT: No mention of the I Ching or the hexagrams can be made in the story.",
                "lines_in_context": {
                    "6": {
                        "name": "The central concept of line six in the story.",
                        "meaning": "An explanation of the significance of line six within the context of the story.",
                        "changing": "A description of what occurs when the value of line six changes, indicating a shift in meaning or interpretation."
                    },
                    "5": {
                        "name": "The central concept of line five in the story.",
                        "meaning": "An explanation of the significance of line five within the context of the story.",
                        "changing": "A description of what occurs when the value of line five changes, indicating a shift in meaning or interpretation."
                    },
                    "4": {
                        "name": "The central concept of line four in the story.",
                        "meaning": "An explanation of the significance of line four within the context of the story.",
                        "changing": "A description of what occurs when the value of line four changes, indicating a shift in meaning or interpretation."
                    },
                    "3": {
                        "name": "The central concept of line three in the story.",
                        "meaning": "An explanation of the significance of line three within the context of the story.",
                        "changing": "A description of what occurs when the value of line three changes, indicating a shift in meaning or interpretation."
                    },
                    "2": {
                        "name": "The central concept of line two in the story.",
                        "meaning": "An explanation of the significance of line two within the context of the story.",
                        "changing": "A description of what occurs when the value of line two changes, indicating a shift in meaning or interpretation."
                    },
                    "1": {
                        "name": "The central concept of line one in the story.",
                        "meaning": "An explanation of the significance of line one within the context of the story.",
                        "changing": "A description of what occurs when the value of line one changes, indicating a shift in meaning or interpretation."
                    }
                }
            }
        ]
    }



def make_prompt(hexagram_number, story_idx):

    iching_primer_path = "../includes/iching_primer.md"
    tholonic_primer_path = "../includes/tholonic_primer.md"
    local_hexagram_path = f"../regen/{hexagram_number}.json"

    with open(iching_primer_path, "r", encoding="utf-8") as f:
        iching_primer_content = f.read()

    with open(tholonic_primer_path, "r", encoding="utf-8") as f:
        tholonic_primer_content = f.read()

    with open(local_hexagram_path, "r", encoding="utf-8") as f:
        hexagram_content = f.read()




    prompt = f"""

# Prepare the prompt for the OpenAI API

Tholonic Primer:
{tholonic_primer_content}

I Ching Primer:
{iching_primer_content}

Hexagram {hexagram_number}:
{hexagram_content}

Using the context provided above, generate a short story of approximately {max_words} words that represents the essence and significance of hexagram {hexagram_number} from the I Ching. The story should be engaging and immersive, demonstrating the themes of raw creative force, unrestrained potential, and the process of realization.

### Story Structure:
- The story should have a clear **{story_type[story_idx]}** conflict that embodies the struggle of creative force seeking realization against opposing forces.
- The **title** should capture the essence of the story in a compelling way.
- The story should be written in the style of a well-known author, using a strong and recognizable literary voice.  IMPORTANT: Ensure that the story sounds different from the other stories
- The **short_story** should be a ~500 word version of the story that captures the essence of the story's main conflict, themes, and resolution.

### Hexagram Structure in Story Progression:
The story should be divided into six stages corresponding to the six lines of hexagram {hexagram_number}, with each stage representing a fundamental phase of creative development:

1. **Line 1 - "Emergence"**
   - Meaning: The first stirrings of creation. The protagonist is filled with raw, unshaped potential but lacks direction.
   - Changing Interpretation: If yang changes to yin, it suggests hesitation or failure to act, delaying the creative impulse.

2. **Line 2 - "Formation"**
   - Meaning: The protagonist begins shaping their potential, encountering the first barriers and defining their creative path.
   - Changing Interpretation: If yin changes to yang, it signifies premature action, leading to instability or misalignment with natural flow.

3. **Line 3 - "Conflict"**
   - Meaning: The protagonist meets direct opposition or external challenges that threaten to halt their creation.
   - Changing Interpretation: If yang changes to yin, it indicates retreat or exhaustion before reaching full realization.

4. **Line 4 - "Manifestation"**
   - Meaning: The protagonist refines their vision, aligning their creative work with external reality. They gain momentum.
   - Changing Interpretation: If yin changes to yang, it may indicate overreaching ambition, leading to unsustainable expansion.

5. **Line 5 - "Mastery"**
   - Meaning: The protagonist takes full command of their creation, standing at the peak of their power.
   - Changing Interpretation: If yang changes to yin, it suggests the risk of arrogance or a misjudgment that could undermine success.

6. **Line 6 - "Transcendence"**
   - Meaning: The protagonist's creation is complete, no longer theirs but something that exists beyond them, affecting the world.
   - Changing Interpretation: If yang changes to yin, it signifies clinging to control instead of letting go, preventing evolution.

### Output Format:
The response should be structured as a JSON object replacing the following template values:

```json
{prompt_reply_structure}
    """
    return prompt
