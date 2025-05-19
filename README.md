# AI Psychologist Chatbot

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture & Tech Stack](#architecture--tech-stack)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview
This project is an **AI Psychologist Chatbot** that allows users to communicate with a virtual psychologist via text or voice. The chatbot processes user input, responds in text and voice, and analyzes emotional and sentimental content. Each session is summarized and visualized on a dashboard for a human psychologist to review emotional fluctuations and session insights.

Key functionalities:
- Voice & text communication with the chatbot
- Emotion & sentiment analysis of conversation
- Session summarization
- Interactive dashboard for psychologists to select patients and view sessions

---

## Features
- **Multimodal Chat**:  
  Users can interact through text or voice; the chatbot responds in both formats.
- **Hybrid NLP Engine**:  
  - Primary chatbot powered by Rasa.  
  - Fallback to O‑Llama when Rasa confidence < 0.8 for nuanced responses.
- **Emotion & Sentiment Analysis**:  
  - Lexical and sentiment scoring on user input.  
  - Summarization of sessions highlighting emotional peaks and troughs.
- **Psychologist Dashboard**:  
  - List of patients and their sessions.  
  - Interactive charts showing emotional fluctuations over time.  
  - Session summaries and transcript view.

---

## Architecture & Tech Stack
- **Frontend**: React  
- **Backend**: Flask (Python)  
- **Database**: MongoDB  
- **Chatbot**:  
  - **Rasa** for intent recognition and dialogue management  
  - **O‑Llama** for fallback responses when confidence is low  
- **Analysis**: Custom Python modules for emotion/sentiment lexicons and summarization  
- **Visualization**: React charting libraries (e.g., Recharts or Chart.js)

---

## Installation
1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/ai-psychologist-chatbot.git
   cd ai-psychologist-chatbot
   ```

2. **Frontend Setup**
  ```bash
     cd ../frontend
  npm install
  ```
3.***backend setup***
  ```bash
  cd backend
  source venv/bin/activate
  flask run
  ```

4. MongoDB

Ensure MongoDB is running locally or configure MONGO_URI in backend/.env


## Usage

1. **User Interaction**  
   - Open the frontend application.  
   - Login/register (if implemented) or start a new session.  
   - Chat via text or use the microphone button for voice input.

2. **Session Analysis**  
   - Finish the conversation.  
   - The backend processes the transcript for emotion, sentiment, and summarization.

3. **Psychologist Dashboard**  
   - Login as psychologist.  
   - Select a patient and session from the list.  
   - View interactive charts and session summary.

---

## Screenshots

_Add screenshots by pasting or linking them below:_

1. **Chat Interface**  
   ![Chat Interface](![WhatsApp Image 2025-05-19 at 13 19 25_894dff11](https://github.com/user-attachments/assets/7a1555b8-f897-4a1c-b3e9-064e1a5dfb90)
)

2. **Session Analysis Dashboard**  
   ![Session Dashboard – View 1](![WhatsApp Image 2025-05-19 at 13 01 58_24613076](https://github.com/user-attachments/assets/0e1a82ba-94d6-4340-8ad9-e6475ab2d6d8)
)

   ![Session Dashboard – View 2](![WhatsApp Image 2025-05-19 at 13 02 29_5b00fb7e](https://github.com/user-attachments/assets/d4271393-e7d4-4508-97d5-f522109a86f0)
)
   ![Session Dashboard – View 3](![WhatsApp Image 2025-05-19 at 13 02 59_67319213](https://github.com/user-attachments/assets/2850dce6-efea-4bcd-8a7f-c18de97c60da)
)
   ![Session Dashboard – View 5](![WhatsApp Image 2025-05-19 at 13 04 01_dcde4351](https://github.com/user-attachments/assets/2df7bdef-8eb4-40ac-9ec8-94bc79d84800)
)

4. **Session Summary View**  
   ![Session Summary](![WhatsApp Image 2025-05-19 at 13 03 32_68e04159](https://github.com/user-attachments/assets/71cb2f5e-74bc-4a8d-b106-b3a711d0962b)
)
