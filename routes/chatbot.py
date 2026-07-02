from flask import Blueprint, render_template, request, jsonify, session
from utils.decorators import login_required
import os

chatbot_bp = Blueprint("chatbot", __name__)

DEPARTMENT_CONTEXT = """You are an AI assistant for the Department of Computer Science & Machine Learning at Loyola Academy.
You can help with:
- Machine Learning, Deep Learning, AI concepts
- Python, Java programming
- Database Management Systems (DBMS)
- Computer Networks (CN)
- Operating Systems (OS)
- Design & Analysis of Algorithms (DAA)
- Data Structures
- Interview preparation questions
- Resume writing suggestions
- PPT creation help
- Academic guidance

Always be helpful, accurate, and professional. If you don't know something, say so clearly."""


@chatbot_bp.route("/")
@login_required
def chat():
    return render_template("chatbot/chat.html")


@chatbot_bp.route("/ask", methods=["POST"])
def ask():
    message = request.json.get("message", "").strip()
    if not message:
        return jsonify({"response": "Please enter a message."})

    api_key = os.getenv("GEMINI_API_KEY", "")

    if api_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(
                f"{DEPARTMENT_CONTEXT}\n\nUser: {message}\n\nAssistant:"
            )
            return jsonify({"response": response.text})
        except Exception as e:
            return jsonify({"response": f"AI service error. Using fallback. Error: {str(e)}"})

    # Fallback rule-based responses
    response = _get_fallback_response(message)
    return jsonify({"response": response})


def _get_fallback_response(message):
    msg = message.lower()
    responses = {
        "hello": "Hello! 👋 I'm the Department AI Assistant. Ask me about ML, Python, Java, DBMS, CN, OS, DAA, interview questions, or resume help!",
        "machine learning": "Machine Learning is a subset of AI that enables systems to learn from data. Key topics: Supervised Learning, Unsupervised Learning, Reinforcement Learning, Neural Networks, Decision Trees, SVM, and more.",
        "python": "Python is a versatile programming language widely used in ML, data science, and web development. Key concepts: OOP, data structures, libraries (NumPy, Pandas, Scikit-learn, TensorFlow).",
        "java": "Java is an object-oriented programming language. Key concepts: Classes, Inheritance, Polymorphism, Collections, Multithreading, JDBC.",
        "dbms": "Database Management Systems cover: ER diagrams, Normalization, SQL queries, Transactions, ACID properties, Indexing, and Query Optimization.",
        "computer networks": "Computer Networks topics: OSI Model, TCP/IP, DNS, HTTP/HTTPS, Routing, Subnetting, Network Security.",
        "operating system": "OS concepts: Process Management, Memory Management, File Systems, CPU Scheduling, Deadlocks, Virtual Memory.",
        "daa": "Design & Analysis of Algorithms: Divide & Conquer, Dynamic Programming, Greedy Algorithms, Graph Algorithms, NP-Completeness.",
        "interview": "Interview Tips: Practice Data Structures, Algorithms, System Design. Prepare behavioral questions. Review your projects. Mock interview regularly.",
        "resume": "Resume Tips: Keep it 1-2 pages. Include: Contact Info, Objective, Education, Skills, Projects, Internships, Certifications, Achievements.",
    }

    for keyword, resp in responses.items():
        if keyword in msg:
            return resp

    return "I'm the Department AI Assistant. I can help with ML, Python, Java, DBMS, CN, OS, DAA, interview prep, resume tips, and PPT help. Ask me anything! 🎓"