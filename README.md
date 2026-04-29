# 🚀 Enterprise LLM Error Monitor

An automated, event-driven background daemon that monitors application logs, triages errors using a cascading Multi-LLM fallback strategy, and dispatches intelligent, AI-summarized email alerts to engineering teams.

## ✨ Key Features

* **🔄 Cross-Provider LLM Fallback:** Architected to guarantee uptime. If the primary AI provider (Google Gemini) experiences rate limits, the system instantly cascades to secondary providers (Groq/LLaMA 3) and tertiary providers (OpenAI GPT-4o).
* **⚡ Real-Time Event Monitoring:** Utilizes Python's `watchdog` library to sit silently in the background (0% CPU usage) and instantly trigger processing the millisecond a log file is updated.
* **📧 Intelligent Email Routing:** Automatically formats AI insights into readable HTML reports and routes them to designated `TO:` (Engineering) and `CC:` (Management) email lists.
* **🛡️ Concurrency & File-Lock Protection:** Includes built-in safeguards to pause processing if the log database (Excel/CSV) is currently locked or being written to by another user or application.

## 🛠️ Architecture

1. **Ingestion:** A target log file (`error_logs.xlsx`) is monitored for filesystem modification events.
2. **Triage:** New "Pending" errors are extracted and sent via API to the LLM router.
3. **Analysis:** The LLM acts as an expert Site Reliability Engineer, generating a 2-sentence non-technical summary and a technical resolution path.
4. **Dispatch:** The system compiles the data, sends SMTP alerts, and updates the database status to "Processed".

## 🚀 Getting Started

### Prerequisites
* Python 3.9+
* API Keys for Google Gemini, Groq (Optional), and OpenAI (Optional)
* A Gmail account with an "App Password" generated for SMTP delivery.

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YourUsername/enterprise-llm-error-monitor.git](https://github.com/YourUsername/enterprise-llm-error-monitor.git)
   cd enterprise-llm-error-monitor
