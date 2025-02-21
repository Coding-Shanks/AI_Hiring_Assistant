### **📝 TalentScout Hiring Assistant – AI-Powered Resume Screening & Chatbot**  

![Streamlit](https://img.shields.io/badge/Streamlit-%23FF4B4B.svg?style=for-the-badge&logo=Streamlit&logoColor=white)  
An AI-powered hiring assistant that helps recruiters screen candidates efficiently. Built using **Streamlit, Google Gemini AI, and Pandas**, this application features an AI chatbot, candidate screening, admin dashboard, and user authentication.

---

## **🚀 Features**
✅ **User Authentication:** Candidates & Admins can log in securely.  
✅ **Candidate Screening:** Candidates fill out a form & upload resumes.  
✅ **Resume Upload & Storage:** Resumes are saved in the `data/resumes/` directory.  
✅ **Admin Dashboard:** Admins can view the total number of candidates and login count.  
✅ **AI Suitability Score:** Automatically assigns a score based on input.  
✅ **AI Chatbot:** Integrated with **Google Gemini AI** for hiring assistance.  
✅ **Duplicate Handling:** Ensures each email can only submit one form; new data updates the existing entry.  
✅ **Access Control:** Only admins can see stored candidates.  

---

## **💁️ Project Structure**
```
📚 ai_hiring_assistant/
│── 📚 data/                  # Stores users, candidates, and login count
│   ├── users.json            # Stores user credentials
│   ├── candidates.json       # Stores candidate details
│   ├── login_count.json      # Stores login count
│   └── resumes/              # Stores uploaded resumes
│── 📄 app.py                 # Main Streamlit app
│── 📄 requirements.txt       # Required dependencies
│── 📄 README.md              # Project documentation
│── 📄 .streamlit/secrets.toml # (If using secrets for API keys)
```

---

## **🔧 Installation & Setup**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/Coding-Shanks/AI_Hiring_Assistant.git
cd ai_hiring_assistant
```

### **2️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3️⃣ Run the Streamlit App**
```bash
streamlit run app.py
```

---

## **🌍 Deploy on Streamlit Community Cloud**
1. Push your code to **GitHub**.
2. Go to **[Streamlit Cloud](https://share.streamlit.io/)**.
3. Click **New App** → Select your GitHub repo.
4. Set the main file as `app.py` & Click **Deploy**.
5. Add **API keys** under Streamlit **Secrets**:
   ```json
   {
       "GOOGLE_GEMINI_API_KEY": "your-api-key-here"
   }
   ```

## 🌐 Live Demo  
[View Live Demo](https://aihiringassistant-hcwz2z676tm7b9wr48myhr.streamlit.app/) *(Host on GitHub Pages or Netlify)*  

## **🛠 Tech Stack**
- **Frontend & UI**: Streamlit  
- **Backend**: Python  
- **Database**: JSON files  
- **AI Model**: Google Gemini AI  
- **File Storage**: Local storage (resumes)  

---

## **🤝 Contributing**
Feel free to contribute! Fork the repo, create a feature branch, and submit a **pull request**.

---

## **🐝 License**
MIT License

---

## **📝 Contact**
For queries or suggestions, reach out to **Coding-Shanks** via GitHub. 🚀

---
