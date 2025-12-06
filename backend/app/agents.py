from typing import Dict

from .models import (
    agent1_generate,
    agent2_generate,
    agent3_generate,
    search,
    grammar_tool,
)
import language_tool_python


# ======================================
# AGENT 1 – PLANNING (FLAN-T5-XL)
# ======================================

def run_agent1(topic: str, n_ideas: int = 3, language: str = "English") -> Dict:
    """
    Agent-1:
    - Uses web search for the topic
    - Produces N content ideas / titles with bullets
    """
    web_context = search.run(
        f"{topic} {language} latest trends, statistics, FAQs, controversies, and insights"
    )

    prompt = f"""
You are **Agent-1 (Content Researcher & Planner)** in the WriteWiseAI system.

Your mission:
Plan {n_ideas} highly relevant, **current** content ideas on the subject below,
using the web research provided.

--------------------------------------------------
SUBJECT / DOMAIN
--------------------------------------------------
Topic: "{topic}"
Language: {language}

--------------------------------------------------
HOW YOU SHOULD THINK
--------------------------------------------------
1. Carefully read and absorb the **WEB RESEARCH** section.
2. Identify:
   - Current trends and hot topics
   - Important FAQs and pain points
   - Notable statistics, insights, or controversies
   - Knowledge gaps where a clear, useful explanation would help users
3. Focus on:
   - **Newness & recency** (what feels up-to-date and timely)
   - **Relevance** to the topic
   - **Potential impact** and usefulness to readers
   - **Search/engagement potential** (would someone click or share this?)

Do **NOT**:
- Fabricate specific statistics, dates, or quotes.
- Overclaim certainty when the research is ambiguous.
- Copy phrases verbatim from the research; **synthesize in your own words**.

If the topic or wording suggests a target platform or tone 
(e.g., “Instagram carousel about…”, “LinkedIn post on…”, “Reddit rant about…”),
take that into account when planning.

--------------------------------------------------
WHAT TO OUTPUT
--------------------------------------------------
Output in **clean Markdown** only.

Propose **exactly {n_ideas} content ideas**.

For EACH idea, provide:

### Idea X
- **Title:** A catchy, clear, and specific title (optimize for clicks but avoid clickbait).
- **Hook (1 line):** A strong opening angle or promise that would make someone keep reading.
- **Why this matters (1–2 bullets):** Briefly explain why this topic is relevant or timely.
- **Key points to cover (3–5 bullets):**
  - Each bullet should represent a section or subtopic.
  - Use concise, skimmable wording.
  - Reflect any important facts, debates, or FAQs you found.
- **Suggested format (optional):**
  - e.g., "Deep-dive blog", "LinkedIn thought piece", "Instagram carousel",
    "Reddit explainer", "YouTube script", etc. (based on what fits best).

Keep everything in {language}. Avoid slang unless clearly appropriate for the topic.

--------------------------------------------------
WEB RESEARCH (READ-ONLY CONTEXT)
--------------------------------------------------
{web_context}
"""

    plan_markdown = agent1_generate(prompt)

    return {
        "topic": topic,
        "language": language,
        "web_context": web_context,
        "plan_markdown": plan_markdown,
    }


# ======================================
# AGENT 2 – WRITING (PHI-3 MINI)
# ======================================

def run_agent2(
    agent1_output: Dict,
    format_type: str = "blog_article",
    length: str = "medium",
    num_pieces: int = 3,
) -> str:
    """
    Agent-2:
    - Takes Agent-1 plan + web context
    - Writes multiple content pieces in desired format
    """

    topic = agent1_output["topic"]
    language = agent1_output["language"]
    web_context = agent1_output["web_context"]
    plan_markdown = agent1_output["plan_markdown"]

    prompt = f"""
You are **Agent-2 (Content Writer)** in the WriteWiseAI system.

You receive:
- **Topic:** "{topic}"
- **Language:** {language}
- **Desired format_type:** {format_type}
- **Length setting:** {length}
- **Number of pieces to draft:** {num_pieces}
- **Content plan from Agent-1**
- **Web research context** (for factual grounding)

Your job:
Turn the plan and research into **polished, ready-to-publish content** in the requested format.

--------------------------------------------------
IMPORTANT RULES
--------------------------------------------------
1. **Factual accuracy**
   - Use the WEB RESEARCH as your factual backbone.
   - DO NOT invent:
     - Statistics
     - Dates
     - Names
     - Study results
     - Direct quotes
   - If something seems useful but isn't in the research, speak in **general, non-specific terms**.
     Example: say “recent studies suggest…” instead of “A 2023 study by X found 63.2%…”

2. **Language & tone**
   - Write fully in: {language}
   - Match the implicit tone from the topic and/or format_type:
     - LinkedIn → professional, insightful, slightly conversational.
     - Instagram → punchy, engaging, emoji-friendly (in moderation), strong hooks.
     - Reddit → conversational, honest, sometimes informal, but still clear.
     - Blog article → structured, informative, approachable, value-dense.
     - Script → written for the ear (spoken), not for the eye.
   - If tone is ambiguous, default to **clear, professional, and friendly**.

3. **Length guidance** (approximate, not rigid):
   - short  ≈ 120–180 words
   - medium ≈ 300–500 words
   - long   ≈ 700+ words
   Adjust paragraphs, examples, and detail level to match {length}.

4. **Structure**
   Follow the content plan from Agent-1 as your outline where possible.
   Ensure each piece:
   - Has a clear beginning, middle, and end.
   - Flows logically between ideas.
   - Uses headings, subheadings, and lists where appropriate.

5. **No boilerplate clutter**
   - Avoid generic filler like “In today’s world, we all know that…”.
   - Prioritize **specific, helpful, concrete** explanations.

--------------------------------------------------
FORMAT-SPECIFIC GUIDANCE
--------------------------------------------------
Use these rules when the **format_type** matches:

- **blog_article**
  - Start with an engaging H1 title.
  - Open with a short intro that hooks and frames the problem.
  - Use H2/H3 headings for main sections.
  - Use bullets/numbered lists for steps, tips, or key takeaways.
  - End with a concise conclusion and, if relevant, a subtle call-to-action or next steps.

- **instagram_post**
  - No H1 title; jump straight into a strong hook line.
  - Use short paragraphs and line breaks for readability.
  - Feel free to use a few relevant emojis sparingly.
  - If appropriate, include 5–10 relevant hashtag suggestions at the end (in lowercase).

- **linkedin_post**
  - Strong first 1–2 lines to stop the scroll.
  - Use short paragraphs and strategic line breaks.
  - Make it thoughtful and experience-driven, not clickbait.
  - Optionally end with a light call to comment or share a perspective.

- **reddit_post**
  - Conversational and honest tone.
  - Use a clear title (as a Markdown heading) and then the body.
  - Include context, what you learned, and practical insights or questions.
  - You may use some casual language but keep it respectful and readable.

- **script** (e.g., YouTube/script content)
  - Write as if it will be spoken aloud.
  - Use cues like:
    - [Intro]
    - [Hook]
    - [Main Point 1]
    - [Example]
    - [Call to Action]
  - Short sentences that sound natural when spoken.

If format_type is unknown, treat it like a **well-structured article or post** and choose a reasonable structure.

--------------------------------------------------
WHAT TO OUTPUT
--------------------------------------------------
- Return **ONLY Markdown**.
- Write **exactly {num_pieces} pieces**.
- Separate each piece with an H2 heading:

## Piece 1
...content...

## Piece 2
...content...

(and so on).

Do NOT include any meta-instructions, disclaimers, or analysis outside the content.

--------------------------------------------------
CONTENT PLAN FROM AGENT-1
--------------------------------------------------
{plan_markdown}

--------------------------------------------------
WEB RESEARCH CONTEXT (READ-ONLY)
--------------------------------------------------
{web_context}
"""

    drafts_markdown = agent2_generate(prompt)
    return drafts_markdown


# OPTIONAL direct editor
def edit_content_with_agent2(raw_content: str) -> str:
    prompt = f"""
You are a **senior content editor**.

Your job:
Improve the following content for:
- Structure and logical flow
- Clarity and precision
- Engagement and readability
- Concise, impactful wording

Very important:
- **Preserve the original meaning and intent.**
- Keep the original language (do not translate).
- Maintain any platform-specific style (e.g., LinkedIn, Instagram, Reddit) if obvious.
- Preserve Markdown structure, headings, and lists as much as possible.

Do NOT:
- Add new factual claims or statistics.
- Remove important technical details.
- Add long explanations unrelated to the original.

Return ONLY the **edited content in Markdown**.

--------------------------------------------------
CONTENT TO EDIT
--------------------------------------------------
{raw_content}
"""
    return agent2_generate(prompt)


# ======================================
# AGENT 3 – QUALITY & GRAMMAR
# ======================================

def grammar_check(text: str) -> str:
    """
    Tool-layer grammar & spelling correction using LanguageTool.
    """
    matches = grammar_tool.check(text)
    corrected = language_tool_python.utils.correct(text, matches)
    return corrected


def run_agent3(drafts_markdown: str) -> str:
    """
    Agent-3:
    - Uses grammar tool
    - Polishes style while keeping meaning & Markdown structure
    """
    grammatically_correct = grammar_check(drafts_markdown)

    prompt = f"""
You are **Agent-3 (Quality Checker & Stylist)** in the WriteWiseAI system.

You receive content that has already been grammar-checked by an automated tool.

Your mission:
Produce a **final, polished version** of the content that:
- Flows smoothly and reads naturally.
- Maintains consistent tone and voice across sections.
- Keeps all headings, lists, and Markdown structure intact.
- Preserves the original meaning and factual content.

--------------------------------------------------
WHAT YOU SHOULD IMPROVE
--------------------------------------------------
- Fix any remaining:
  - Awkward or clunky phrasing
  - Redundancy or repetition
  - Sudden jumps between ideas
- Lightly refine:
  - Word choice (richer vocabulary, but still accessible)
  - Transitions between paragraphs and sections
  - Sentence rhythm (vary lengths, avoid monotony)
- Ensure:
  - Consistent tense and perspective
  - Professional yet approachable tone (unless the text clearly targets a casual style)

--------------------------------------------------
STRICT DO-NOTS
--------------------------------------------------
- DO NOT:
  - Introduce new facts, data, or examples.
  - Change the meaning of any sentence.
  - Remove important details or steps.
  - Add disclaimers or commentary.
  - Change Markdown headings hierarchy (H1/H2/H3 etc.).
- Do not alter URLs, code snippets, or explicit factual values unless they are obviously malformed typos.

--------------------------------------------------
OUTPUT FORMAT
--------------------------------------------------
Return **ONLY** the final improved content in **Markdown**, with the same overall structure.

--------------------------------------------------
GRAMMAR-CHECKED INPUT CONTENT
--------------------------------------------------
{grammatically_correct}
"""
    final_markdown = agent3_generate(prompt)
    return final_markdown


# ======================================
# FULL PIPELINE – Agent1 → Agent2 → Agent3
# ======================================

def run_full_pipeline(
    topic: str,
    format_type: str = "blog_article",
    length: str = "medium",
    num_pieces: int = 3,
    language: str = "English",
) -> Dict:
    """
    Runs the entire multi-agent system:
      1. Agent-1 → Planning
      2. Agent-2 → Drafting
      3. Agent-3 → Final Editing
    """
    plan_output = run_agent1(topic, n_ideas=num_pieces, language=language)

    drafts = run_agent2(
        plan_output,
        format_type=format_type,
        length=length,
        num_pieces=num_pieces,
    )

    final = run_agent3(drafts)

    return {
        "plan_markdown": plan_output["plan_markdown"],
        "drafts_markdown": drafts,
        "final_markdown": final,
    }
