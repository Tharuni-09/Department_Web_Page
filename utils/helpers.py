from datetime import datetime

def format_date(dt):
    """Format datetime for display."""
    if isinstance(dt, datetime):
        return dt.strftime("%d %b %Y")
    return str(dt) if dt else ""

def format_datetime(dt):
    """Format datetime with time."""
    if isinstance(dt, datetime):
        return dt.strftime("%d %b %Y, %I:%M %p")
    return str(dt) if dt else ""

def get_semester_list():
    """Return list of semesters."""
    return list(range(1, 9))

def get_regulation_list():
    """Return list of regulations."""
    return ["R20", "R21", "R22", "R23", "R24", "R25"]

def get_subject_list():
    """Return common CS & ML subjects."""
    return [
        "Machine Learning", "Deep Learning", "Data Structures",
        "Algorithms", "Database Management", "Computer Networks",
        "Operating Systems", "Python Programming", "Java Programming",
        "Web Technologies", "Software Engineering", "Artificial Intelligence",
        "Data Mining", "Cloud Computing", "Cyber Security",
        "Design & Analysis of Algorithms", "Discrete Mathematics",
        "Computer Architecture", "Theory of Computation", "Compiler Design",
        "Natural Language Processing", "Computer Vision", "Big Data Analytics",
        "Internet of Things", "Mobile Computing", "Other"
    ]

def get_category_list():
    """Return outreach event categories."""
    return [
        "Workshop", "Seminar", "Hackathon", "Guest Lecture",
        "Industrial Visit", "Conference", "Cultural Event",
        "Sports Event", "Community Service", "Other"
    ]
