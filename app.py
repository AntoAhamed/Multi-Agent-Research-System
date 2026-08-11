import streamlit as st

from src.pipelines.pipeline import run_research_pipeline


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #777;
        margin-bottom: 30px;
    }

    .result-box {
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #ddd;
        background-color: #fafafa;
    }

    .step-title {
        font-size: 20px;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🔎 AI Research Agent</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">Search → Read → Write → Critic</div>',
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Research Settings")

    topic = st.text_area(
        "Research Topic",
        placeholder=(
            "Example:\n"
            "The impact of artificial intelligence on software development"
        ),
        height=150,
    )

    run_button = st.button(
        "🚀 Start Research",
        use_container_width=True,
        type="primary",
    )

    st.divider()

    st.markdown("### Pipeline")

    st.markdown(
        """
        **1. 🔎 Search Agent**  
        Finds recent and reliable information.

        **2. 📖 Reader Agent**  
        Selects and scrapes a relevant source.

        **3. ✍️ Writer**  
        Creates the research report.

        **4. 🧐 Critic**  
        Reviews and critiques the report.
        """
    )


# ============================================================
# HELPER FUNCTION
# ============================================================

def get_content(value):
    """
    Converts different LangChain response formats
    into text that Streamlit can display.
    """

    if value is None:
        return ""

    # AIMessage / message-like object
    if hasattr(value, "content"):
        value = value.content

    # Gemini / LangChain structured content
    if isinstance(value, list):

        text_parts = []

        for item in value:

            if isinstance(item, dict):

                if item.get("type") == "text":
                    text_parts.append(item.get("text", ""))

                elif "text" in item:
                    text_parts.append(item["text"])

            else:
                text_parts.append(str(item))

        return "\n".join(text_parts)

    return str(value)


# ============================================================
# RUN RESEARCH
# ============================================================

if run_button:

    if not topic.strip():

        st.warning("⚠️ Please enter a research topic first.")

    else:

        st.session_state["research_result"] = None

        st.markdown("## 🔬 Researching...")

        progress = st.progress(0)

        status = st.empty()

        try:

            # ------------------------------------------------
            # RUN COMPLETE RESEARCH PIPELINE
            # ------------------------------------------------

            status.info(
                "🔎 Running Search → Reader → Writer → Critic..."
            )

            progress.progress(10)

            result = run_research_pipeline(topic.strip())

            progress.progress(100)

            status.success(
                "✅ Research completed successfully!"
            )

            st.session_state["research_result"] = result

        except Exception as e:

            progress.empty()
            status.empty()

            st.error("❌ Something went wrong.")

            st.exception(e)


# ============================================================
# DISPLAY RESULTS
# ============================================================

if st.session_state.get("research_result"):

    result = st.session_state["research_result"]

    # --------------------------------------------------------
    # EXTRACT RESULTS
    # --------------------------------------------------------

    search_results = get_content(
        result.get("search_results")
    )

    scraped_content = get_content(
        result.get("scraped_content")
    )

    report = get_content(
        result.get("report")
    )

    feedback = get_content(
        result.get("feedback")
    )

    # --------------------------------------------------------
    # RESULTS HEADER
    # --------------------------------------------------------

    st.divider()

    st.markdown("## 📊 Research Results")

    # --------------------------------------------------------
    # TABS
    # --------------------------------------------------------

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "🔎 Search Results",
            "📖 Scraped Content",
            "📄 Final Report",
            "🧐 Critic Review",
        ]
    )

    # ========================================================
    # TAB 1 — SEARCH RESULTS
    # ========================================================

    with tab1:

        st.subheader("Search Agent Results")

        if search_results:

            st.markdown(search_results)

        else:

            st.info("No search results returned.")

    # ========================================================
    # TAB 2 — SCRAPED CONTENT
    # ========================================================

    with tab2:

        st.subheader("Reader Agent Results")

        if scraped_content:

            st.markdown(scraped_content)

        else:

            st.info("No scraped content returned.")

    # ========================================================
    # TAB 3 — FINAL REPORT
    # ========================================================

    with tab3:

        st.subheader("Research Report")

        if report:

            st.markdown(report)

            st.divider()

            st.download_button(
                label="⬇️ Download Report",
                data=report,
                file_name="research_report.md",
                mime="text/markdown",
            )

        else:

            st.info("No report generated.")

    # ========================================================
    # TAB 4 — CRITIC
    # ========================================================

    with tab4:

        st.subheader("Critic Review")

        if feedback:

            st.markdown(feedback)

        else:

            st.info("No critic feedback returned.")


# ============================================================
# INITIAL SCREEN
# ============================================================

else:

    st.info(
        "👈 Enter a research topic in the sidebar and click "
        "**Start Research** to begin."
    )

    st.markdown(
        """
        ### How it works

        Your research agent follows four steps:

        **🔎 Search**  
        Finds recent and reliable information.

        ↓

        **📖 Reader**  
        Scrapes the most relevant source.

        ↓

        **✍️ Writer**  
        Combines the research into a report.

        ↓

        **🧐 Critic**  
        Reviews the generated report.
        """
    )
