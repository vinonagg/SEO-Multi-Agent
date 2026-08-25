import os
import asyncio
import requests
import streamlit as st

from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

MODEL = "gpt-4.1-mini"


# ============================================================
# WEB SEARCH TOOL
# ============================================================

async def web_search(query: str) -> str:
    """
    Search the web using Tavily API.

    The Research Agent uses this tool to identify:
    - Current trends
    - Recent developments
    - Industry insights
    - Relevant keywords
    - Popular discussions
    """

    if not TAVILY_API_KEY:
        return """
Live web search is currently unavailable because TAVILY_API_KEY
is not configured.

Use your existing knowledge, but do not claim that information
has been verified through live web research.
"""

    try:
        response = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": TAVILY_API_KEY,
                "query": query,
                "search_depth": "advanced",
                "max_results": 7,
                "include_answer": True,
                "include_raw_content": False,
            },
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        results = []

        # Add Tavily-generated summary if available
        if data.get("answer"):
            results.append(
                f"""
SEARCH SUMMARY

{data["answer"]}
"""
            )

        # Add individual search results
        for index, item in enumerate(
            data.get("results", []),
            start=1
        ):

            title = item.get("title", "No title")
            url = item.get("url", "No URL")
            content = item.get("content", "No content")

            results.append(
                f"""
SOURCE {index}

TITLE:
{title}

URL:
{url}

CONTENT:
{content}
"""
            )

        if not results:
            return "No useful search results were found."

        return "\n\n".join(results)

    except Exception as error:

        return f"""
WEB SEARCH FAILED

Error:
{str(error)}

Continue using available knowledge, but do not invent
current statistics, trends, or research findings.
"""


# ============================================================
# CREATE MULTI-AGENT TEAM
# ============================================================

def create_seo_team():

    # IMPORTANT:
    # Do NOT add parallel_tool_calls=False here.
    # Only the Research Agent has tools.
    model_client = OpenAIChatCompletionClient(
        model=MODEL,
        api_key=OPENAI_API_KEY,
    )

    # ========================================================
    # AGENT 1 - RESEARCH AGENT
    # ========================================================

    research_agent = AssistantAgent(
        name="research_agent",

        model_client=model_client,

        tools=[web_search],

        max_tool_iterations=3,

        description=(
            "An SEO research specialist responsible for researching "
            "topics, identifying trends, keywords, search intent, "
            "target audience, and content opportunities."
        ),

        system_message="""
You are the RESEARCH AGENT in an SEO content creation workflow.

Your ONLY responsibility is research.

When you receive a topic:

1. Use the web_search tool to research the topic.
2. Identify current and important trends.
3. Identify major discussions around the topic.
4. Identify the target audience.
5. Identify search intent.
6. Suggest one primary keyword.
7. Suggest relevant secondary keywords.
8. Suggest long-tail keywords.
9. Identify common user questions.
10. Identify content opportunities.
11. Suggest a recommended article angle.

Your final response MUST use this structure:

# RESEARCH BRIEF

## Original Topic

## Trending Angles

## Target Audience

## Search Intent

## Primary Keyword

## Secondary Keywords

## Long-Tail Keywords

## Important Questions To Answer

## Recommended Article Angle

## Suggested Article Structure

## Research Sources

Important rules:

- Use web research when available.
- Do not fabricate statistics.
- Do not invent sources.
- Do not write the complete article.
- Your research will be used by the Content Writer Agent.
"""
    )

    # ========================================================
    # AGENT 2 - CONTENT WRITER
    # ========================================================

    content_agent = AssistantAgent(
        name="content_writer",

        model_client=model_client,

        description=(
            "A professional content writer responsible for converting "
            "research into a high-quality, engaging article."
        ),

        system_message="""
You are the CONTENT WRITER AGENT.

You will receive:

1. The user's original topic.
2. A research brief from the Research Agent.

Your responsibility is to write a complete, engaging article.

Requirements:

- Create an SEO-friendly title.
- Use a single H1 title.
- Write a strong introduction.
- Use clear H2 headings.
- Use H3 headings where appropriate.
- Cover the important trending angles.
- Address the identified search intent.
- Use keywords naturally.
- Avoid keyword stuffing.
- Use clear and professional language.
- Add examples where useful.
- Add a conclusion.
- Add an FAQ section.

Return ONLY the complete article in Markdown format.

Do not:

- Mention agents.
- Mention internal workflow.
- Explain your reasoning.
- Add SEO reports.

Your article will be passed to the SEO Specialist.
"""
    )

    # ========================================================
    # AGENT 3 - SEO SPECIALIST
    # ========================================================

    seo_agent = AssistantAgent(
        name="seo_specialist",

        model_client=model_client,

        description=(
            "An SEO specialist responsible for analyzing and "
            "optimizing articles for search engines and readers."
        ),

        system_message="""
You are the SEO SPECIALIST AGENT.

You will receive the previous agents' outputs.

Your responsibility is to audit and optimize the article.

Check the following:

1. SEO title.
2. Primary keyword usage.
3. Secondary keyword usage.
4. Keyword stuffing.
5. Search intent alignment.
6. H1 structure.
7. H2 structure.
8. H3 structure.
9. Readability.
10. Meta description.
11. URL slug.
12. FAQ optimization.
13. Content completeness.

Then improve the article.

Your final response MUST follow this format:

# SEO OPTIMIZATION REPORT

SEO Score: X/100

## Primary Keyword

## SEO Title

## Meta Description

## Suggested URL Slug

## SEO Improvements Applied

# OPTIMIZED ARTICLE

Write the complete optimized article here.

Important:

- Keep the article natural.
- Avoid keyword stuffing.
- Preserve useful information.
- Do not fabricate facts.
- Do not mention the internal multi-agent workflow.
"""
    )

    # ========================================================
    # AGENT 4 - CONTENT REVIEWER
    # ========================================================

    review_agent = AssistantAgent(
        name="content_reviewer",

        model_client=model_client,

        description=(
            "A senior editor and final reviewer responsible for "
            "producing publication-ready SEO content."
        ),

        system_message="""
You are the FINAL CONTENT REVIEWER.

You are the final quality gate.

Review all previous outputs.

Check:

1. Factual consistency.
2. Logical flow.
3. Grammar.
4. Repetition.
5. Readability.
6. Professional tone.
7. SEO quality.
8. Natural keyword usage.
9. Heading structure.
10. Search intent alignment.
11. Completeness.

Make any necessary improvements.

Your final response MUST follow this exact format:

# FINAL REVIEW

Status: APPROVED

Quality Score: X/100

SEO Score: X/100

## Improvements Made

- Improvement 1
- Improvement 2
- Improvement 3

# FINAL SEO ARTICLE

Write the complete, publication-ready article here.

Important:

- The FINAL SEO ARTICLE must be complete.
- Do not mention agents.
- Do not mention internal workflow.
- Do not add explanations after the final article.
"""
    )

    # ========================================================
    # TERMINATION CONDITION
    # ========================================================

    termination = MaxMessageTermination(
        max_messages=5
    )

    # ========================================================
    # CREATE TEAM
    # ========================================================

    team = RoundRobinGroupChat(
        participants=[
            research_agent,
            content_agent,
            seo_agent,
            review_agent,
        ],

        termination_condition=termination,
    )

    return team, model_client


# ============================================================
# RUN MULTI-AGENT WORKFLOW
# ============================================================

async def run_seo_workflow(topic: str):

    team, model_client = create_seo_team()

    task = f"""
Create a complete SEO-optimized article using the following topic.

USER TOPIC:

{topic}

The agents must execute in this order:

1. Research Agent
2. Content Writer
3. SEO Specialist
4. Content Reviewer

Each agent should use the previous agent's output.

The Content Reviewer must provide the final publication-ready article.
"""

    try:

        result = await team.run(
            task=task
        )

        research_output = ""
        content_output = ""
        seo_output = ""
        final_output = ""

        messages = []

        for message in result.messages:

            source = getattr(message, "source", "")
            content = getattr(message, "content", "")

            if not content:
                continue

            content_text = str(content)

            messages.append(
                {
                    "agent": source,
                    "content": content_text,
                }
            )

            if source == "research_agent":

                research_output = content_text

            elif source == "content_writer":

                content_output = content_text

            elif source == "seo_specialist":

                seo_output = content_text

            elif source == "content_reviewer":

                final_output = content_text

        return {
            "research": research_output,
            "content": content_output,
            "seo": seo_output,
            "final": final_output,
            "messages": messages,
            "stop_reason": result.stop_reason,
        }

    finally:

        await model_client.close()


# ============================================================
# STREAMLIT APPLICATION
# ============================================================

def main():

    st.set_page_config(
        page_title="AI SEO Multi-Agent System",
        page_icon="🤖",
        layout="wide",
    )

    # ========================================================
    # HEADER
    # ========================================================

    st.title("🤖 AI SEO Multi-Agent System")

    st.markdown(
        """
**Research → Content → SEO → Review**

Enter any topic and let four specialized AI agents
collaboratively create a publication-ready SEO article.
"""
    )

    st.divider()

    # ========================================================
    # API KEY VALIDATION
    # ========================================================

    if not OPENAI_API_KEY:

        st.error(
            "OPENAI_API_KEY is missing."
        )

        st.info(
            "Add your OpenAI API key to the .env file."
        )

        st.code(
            """
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
"""
        )

        st.stop()

    # ========================================================
    # SIDEBAR
    # ========================================================

    with st.sidebar:

        st.header("⚙️ Configuration")

        st.success(
            f"Model: {MODEL}"
        )

        if TAVILY_API_KEY:

            st.success(
                "Live Web Research: Enabled"
            )

        else:

            st.warning(
                "Live Web Research: Disabled"
            )

            st.caption(
                "Add TAVILY_API_KEY to enable live "
                "web research and trend discovery."
            )

        st.divider()

        st.subheader(
            "🤖 Agent Workflow"
        )

        st.markdown(
            """
### 1. 🔍 Research Agent

Researches:

- Trends
- Keywords
- Search intent
- Audience
- Content opportunities

### 2. ✍️ Content Agent

Creates:

- SEO article
- Headings
- Introduction
- Conclusion
- FAQ

### 3. 📈 SEO Agent

Optimizes:

- Keywords
- Meta description
- URL slug
- Heading structure
- Readability

### 4. 🧐 Review Agent

Checks:

- Quality
- Grammar
- SEO
- Readability
- Final publication readiness
"""
        )

    # ========================================================
    # USER INPUT
    # ========================================================

    topic = st.chat_input(
        "Enter a topic... Example: AI Agents in Healthcare"
    )

    # ========================================================
    # PROCESS USER REQUEST
    # ========================================================

    if topic:

        with st.chat_message("user"):

            st.write(topic)

        try:

            with st.status(
                "🤖 Multi-Agent System is working...",
                expanded=True,
            ) as status:

                st.write(
                    "🔍 Research Agent is researching the topic..."
                )

                result = asyncio.run(
                    run_seo_workflow(topic)
                )

                st.write(
                    "✍️ Content Writer Agent completed the article."
                )

                st.write(
                    "📈 SEO Specialist optimized the article."
                )

                st.write(
                    "🧐 Content Reviewer completed the final review."
                )

                status.update(
                    label="✅ SEO content generation completed!",
                    state="complete",
                    expanded=False,
                )

        except Exception as error:

            st.error(
                "The multi-agent workflow encountered an error."
            )

            st.exception(error)

            return

        # ====================================================
        # FINAL OUTPUT
        # ====================================================

        st.divider()

        st.header(
            "🚀 Final SEO Content"
        )

        if result["final"]:

            st.markdown(
                result["final"]
            )

        else:

            st.warning(
                "Final reviewer output was not captured."
            )

        # ====================================================
        # DOWNLOAD BUTTON
        # ====================================================

        if result["final"]:

            st.download_button(
                label="⬇️ Download Final Article",
                data=result["final"],
                file_name="seo_article.md",
                mime="text/markdown",
            )

        # ====================================================
        # AGENT OUTPUT DETAILS
        # ====================================================

        st.divider()

        st.header(
            "🔍 Agent Workflow Details"
        )

        tab1, tab2, tab3, tab4 = st.tabs(
            [
                "🔍 Research",
                "✍️ Content",
                "📈 SEO",
                "🧐 Final Review",
            ]
        )

        # ----------------------------------------------------
        # RESEARCH TAB
        # ----------------------------------------------------

        with tab1:

            if result["research"]:

                st.markdown(
                    result["research"]
                )

            else:

                st.info(
                    "Research output was not captured."
                )

        # ----------------------------------------------------
        # CONTENT TAB
        # ----------------------------------------------------

        with tab2:

            if result["content"]:

                st.markdown(
                    result["content"]
                )

            else:

                st.info(
                    "Content output was not captured."
                )

        # ----------------------------------------------------
        # SEO TAB
        # ----------------------------------------------------

        with tab3:

            if result["seo"]:

                st.markdown(
                    result["seo"]
                )

            else:

                st.info(
                    "SEO output was not captured."
                )

        # ----------------------------------------------------
        # FINAL REVIEW TAB
        # ----------------------------------------------------

        with tab4:

            if result["final"]:

                st.markdown(
                    result["final"]
                )

            else:

                st.info(
                    "Final review output was not captured."
                )

        # ====================================================
        # DEBUG INFORMATION
        # ====================================================

        with st.expander(
            "🔧 Workflow Debug Information"
        ):

            st.write(
                f"Stop Reason: {result['stop_reason']}"
            )

            st.write(
                "Agents executed:"
            )

            for message in result["messages"]:

                st.write(
                    f"• {message['agent']}"
                )


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()