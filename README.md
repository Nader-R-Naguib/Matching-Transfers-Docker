# 🏦 AI-Powered Transfer Reconciliation System

An automated, containerized backend system that uses vision AI (SuryaOCR) and Large Language Models (Llama-3 via Groq) to extract transaction data from user-uploaded bank transfer screenshots and strictly reconcile them against official bank statements.

## 🧠 How the System Works (Architecture)

This system is built using a **Separation of Concerns** architecture to ensure the API never slows down or crashes during heavy auditing.

* **Phase 1: Real-Time Ingestion (The API)**
    * Powered by FastAPI. Users or front-end clients upload receipt screenshots.
    * The system immediately runs AI OCR, extracts the exact amount and phone number, runs pixel-level confidence checks, saves the record to the `user_transfers` database table, and deletes the temporary image.
* **Phase 2: The Batch Auditor (The Matching Engine)**
    * A separate batch process (`main.py`) that ingests official bank statements (CSV/Excel).
    * It sweeps the database to cross-reference user claims against the actual bank records.
    * Successful matches are pushed to `matched_transactions`, and discrepancies are flagged in the `anomaly` tables.

---

## 🚀 Prerequisites & System Requirements

Because this system runs state-of-the-art AI vision models locally, Docker requires sufficient memory allocated to it. 

1. **Install Docker Desktop** & Docker Compose.
2. **Increase Docker Memory (Windows/WSL2 Only):** If you are on Windows, you must allocate at least 8GB of RAM to Docker, or the AI model will silently crash during processing.
   * Go to `C:\Users\<YourUsername>`
   * Create a file named exactly `.wslconfig`
   * Add the following text and save:
     ```text
     [wsl2]
     memory=8GB
     ```
   * Open a terminal and run `wsl --shutdown`, then restart Docker Desktop.

---

## 🛠️ Initial Setup

**1. Clone the Repository**
```bash
git clone [https://github.com/](https://github.com/)<YourUsername>/Matching-Transfers-Docker.git
cd Matching-Transfers-Docker
