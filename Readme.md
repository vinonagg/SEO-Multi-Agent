# SEO Multi-Agent System

## 🤖 AI-Powered SEO Content Generation Using AutoGen

An AI-powered multi-agent system that automates the SEO content creation workflow using **Microsoft AutoGen**, **OpenAI**, **Tavily**, and **Streamlit**.

The application uses four specialized AI agents that collaborate to transform a user-provided topic into a publication-ready, SEO-optimized article.

---

## 🚀 Features

- 🔍 **Research Agent** — Researches the topic, identifies trends, search intent, keywords, and content opportunities.
- ✍️ **Content Writer Agent** — Creates a structured and engaging article based on the research.
- 📈 **SEO Specialist Agent** — Optimizes keywords, headings, metadata, readability, and SEO structure.
- 🧐 **Content Reviewer Agent** — Performs the final quality review and produces a publication-ready article.
- 🌐 **Live Web Research** — Uses Tavily Search API for current research and trending topics.
- 💬 **Streamlit Frontend** — Provides a simple and interactive user interface.
- 📥 **Article Download** — Download the final SEO article in Markdown format.

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │  Streamlit Frontend │
                    │                     │
                    │   User enters topic │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   🔍 Research Agent │
                    │                     │
                    │ • Topic Research    │
                    │ • Trending Angles   │
                    │ • Search Intent     │
                    │ • Keywords          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ ✍️ Content Writer   │
                    │                     │
                    │ • Article Creation  │
                    │ • Headings          │
                    │ • FAQ               │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  📈 SEO Specialist  │
                    │                     │
                    │ • SEO Optimization  │
                    │ • Meta Description  │
                    │ • URL Slug          │
                    │ • Keyword Analysis  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ 🧐 Content Reviewer │
                    │                     │
                    │ • Quality Review    │
                    │ • Grammar           │
                    │ • Readability       │
                    │ • Final Approval    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ 🚀 Final SEO Article│
                    └─────────────────────┘
```

---

# 🔄 Multi-Agent Workflow

The system follows a sequential agent workflow:

```text
User Topic
    │
    ▼
🔍 Research Agent
    │
    ▼
Research Brief
    │
    ▼
✍️ Content Writer Agent
    │
    ▼
Article Draft
    │
    ▼
📈 SEO Specialist Agent
    │
    ▼
SEO Optimized Article
    │
    ▼
🧐 Content Reviewer Agent
    │
    ▼
🚀 Final Publication-Ready Article
```

---

# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| Microsoft AutoGen | Multi-agent orchestration |
| OpenAI | Large Language Model |
| Tavily API | Live web research |
| Streamlit | User interface |
| python-dotenv | Environment variable management |

---

# 📂 Project Structure

```text
SEO-Multi-Agent/
│
├── seo_multi_agent.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/SEO-Multi-Agent.git
```

Navigate to the project directory:

```bash
cd SEO-Multi-Agent
```

---

## 2. Create a Virtual Environment

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
python -m pip install --upgrade pip
```

Install the required packages:

```bash
python -m pip install streamlit python-dotenv requests
```

Install AutoGen:

```bash
python -m pip install -U "autogen-agentchat" "autogen-ext[openai]"
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root.

```bash
touch .env
```

Add your API keys:

```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

> **Note:** `TAVILY_API_KEY` is optional. Without it, the Research Agent will use available model knowledge instead of live web research.

---

# ▶️ Running the Application

Start the Streamlit application:

```bash
python -m streamlit run seo_multi_agent.py
```

After starting the application, Streamlit will provide a local URL similar to:

```text
http://localhost:8501
```

Open the URL in your browser.

---

# 💡 Example Usage

Enter a topic such as:

```text
AI Agents in Healthcare
```

The system will automatically:

1. Research the topic.
2. Identify important and trending angles.
3. Analyze search intent.
4. Generate relevant keywords.
5. Write a complete article.
6. Optimize the article for SEO.
7. Generate a meta description.
8. Generate a suggested URL slug.
9. Review grammar and readability.
10. Produce a final publication-ready SEO article.

---

# 🤖 Agents

## 🔍 Research Agent

Responsibilities:

- Research the user topic.
- Identify current trends.
- Analyze the target audience.
- Identify search intent.
- Generate primary keywords.
- Generate secondary keywords.
- Generate long-tail keywords.
- Identify frequently asked questions.
- Suggest content opportunities.

### Output

```text
Research Brief
├── Original Topic
├── Trending Angles
├── Target Audience
├── Search Intent
├── Primary Keyword
├── Secondary Keywords
├── Long-Tail Keywords
├── Important Questions
├── Recommended Article Angle
├── Suggested Article Structure
└── Research Sources
```

---

## ✍️ Content Writer Agent

Responsibilities:

- Create an SEO-friendly title.
- Write an engaging introduction.
- Structure the article using H1, H2, and H3 headings.
- Cover trending topics from the research.
- Use keywords naturally.
- Add examples where appropriate.
- Write a conclusion.
- Generate an FAQ section.

### Output

A complete Markdown article ready for SEO optimization.

---

## 📈 SEO Specialist Agent

The SEO Specialist analyzes:

- SEO title
- Primary keyword usage
- Secondary keyword usage
- Keyword stuffing
- Search intent alignment
- Heading hierarchy
- Readability
- Meta description
- URL slug
- FAQ optimization
- Content completeness

### Example Output

```text
SEO Score: 92/100

Primary Keyword:
AI Agents in Healthcare

SEO Title:
AI Agents in Healthcare: How Intelligent AI Is Transforming Patient Care

Meta Description:
Discover how AI agents are transforming healthcare operations,
patient care, clinical workflows, and the future of healthcare.

Suggested URL Slug:
ai-agents-in-healthcare
```

---

## 🧐 Content Reviewer Agent

The final reviewer checks:

- Factual consistency
- Logical flow
- Grammar
- Repetitive content
- Readability
- Professional tone
- SEO quality
- Natural keyword usage
- Heading structure
- Search intent alignment

### Final Output

```text
FINAL REVIEW

Status: APPROVED

Quality Score: 95/100

SEO Score: 93/100

FINAL SEO ARTICLE
```

---

# 📊 Streamlit Interface

The Streamlit application provides:

- Topic input
- Multi-agent processing status
- Final SEO article
- Research Agent output
- Content Writer output
- SEO optimization report
- Final review output
- Markdown article download
- Workflow debugging information

---

# 🔐 Security

API keys should never be committed to GitHub.

The `.gitignore` file should contain:

```text
# Environment variables
.env

# Virtual environments
venv/
.venv/

# Python cache
__pycache__/
*.py[cod]

# Streamlit secrets
.streamlit/secrets.toml

# macOS
.DS_Store

# IDE
.vscode/
.idea/

# Streamlit agent skills
.agents/skills/
```

---

# 🔮 Future Improvements

Potential improvements for future versions:

- Google Trends integration
- Google Search Console integration
- SERP analysis
- Keyword difficulty analysis
- Competitor content analysis
- Multiple LLM provider support
- Human approval workflow
- Agent memory
- Article generation in multiple languages
- Word count selection
- Content tone selection
- WordPress publishing integration
- Docker containerization
- VPS deployment
- LangSmith observability
- Automated SEO scoring dashboard

---

# 🐳 Future Deployment Architecture

```text
                    Internet
                       │
                       ▼
                ┌───────────────┐
                │     Nginx     │
                │ Reverse Proxy │
                └───────┬───────┘
                        │
                        ▼
              ┌───────────────────┐
              │ Docker Container  │
              │                   │
              │    Streamlit      │
              │    Application    │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │ AutoGen Agents    │
              │                   │
              │ Research          │
              │ Content           │
              │ SEO               │
              │ Review            │
              └───────────────────┘
```

---

# 📸 Application Screenshot

Add a screenshot of your application here after running it:

```markdown
![SEO Multi-Agent System](images/seo-multi-agent.png)
```

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Commit your changes.
5. Push the branch.
6. Create a Pull Request.

---

# 📄 License

This project is currently intended for educational and portfolio purposes.

---

# 👨‍💻 Author

**Vinoth Nagarajan**

AI | Generative AI | Multi-Agent Systems | Automation | RAG | AI Program & Project Management

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

It helps others discover the project and supports continued development.