# Customer Support Bot

A simple AI-powered customer support chatbot built in Python.

This project demonstrates a lightweight support assistant that:
- loads FAQ data from local files
- detects whether the user question is in Bengali or English
- returns answers in the same language as the question
- uses Gemini API for response generation
- includes a web frontend and a command-line test mode

## Features
- Bengali and English language detection
- FAQ-based answer guidance
- Friendly and helpful support-style responses
- Short, clear replies with optional emoji

## Getting Started
1. Install dependencies from `requirements.txt` or manually install needed packages.
2. Create a `.env` file with `GEMINI_API_KEY`.
3. Run the FastAPI backend in `app/main.py` or test the bot interactively using `app/chatbot.py`.

