# Hackathon Pitch Script
**(0:00 - 0:45) The Problem & Solution**
"Hi, I'm the creator of InsightForge. Every day, professionals make decisions worth millions of dollars using scattered data. While generative AI is great at chatting, it's terrible at structured, reliable decision-making. That's why I built InsightForge: an AI Decision Intelligence Platform that computes, compares, and confidently recommends."

**(0:45 - 2:00) Architecture & AI Pipeline**
"Under the hood, this is a production-grade pipeline. A Next.js frontend communicates with a FastAPI back end. The Orchestrator retrieves factual context via RAG, then forces the LLM to generate a strict JSON response using Pydantic validation. If the LLM hallucinates, our engine automatically catches the error and forces a retry."

**(2:00 - 4:00) The Demo**
"Let's look at the demo. I'm going to ask it to compare two cloud providers based on internal requirements. The engine retrieves context, generates the matrix, and validates it. The result is a strict comparison table with a Confidence Score of 88%. This score tells the user exactly how much they can trust the tool."

**(4:00 - 5:00) Reliability & Future Scope**
"What makes InsightForge enterprise-ready is reliability. I built this focusing entirely on one powerful workflow. Because it guarantees valid JSON outputs, it can easily plug into downstream systems. InsightForge brings engineering rigor to AI decision-making. Thank you."
