"""
Central data store for ThiranPathai.
Extend SKILL_LIST, RESOURCES, PREREQ and QUIZ as your project grows.
In a bigger version, these could move into database tables instead of Python files.
"""

SKILL_LIST = [
    "java", "python", "sql", "html", "css", "javascript", "react", "node.js",
    "spring boot", "rest api", "git", "docker", "kubernetes", "aws", "c++", "c",
    "dsa", "data structures", "machine learning", "excel", "power bi", "tableau",
    "pandas", "numpy", "django", "flask", "mongodb", "mysql", "linux", "php",
    "angular", "typescript", "kotlin", "swift", "android", "figma", "photoshop",
    "communication", "testing", "selenium", "junit", "agile", "jira",
    "tensorflow", "nlp", "statistics",
]

# Skill aliases so slightly different wordings still match (extend this as you find more)
SKILL_ALIASES = {
    "spring boot": ["springboot", "spring-boot"],
    "rest api": ["restful api", "rest apis", "restful services"],
    "node.js": ["nodejs", "node js"],
    "javascript": ["js"],
    "machine learning": ["ml"],
    "data structures": ["dsa", "data structures and algorithms"],
}

RESOURCES = {
    "spring boot": "https://spring.io/guides/gs/spring-boot/",
    "rest api": "https://developer.mozilla.org/en-US/docs/Glossary/REST",
    "git": "https://docs.github.com/en/get-started",
    "docker": "https://docs.docker.com/get-started/",
    "sql": "https://www.w3schools.com/sql/",
    "python": "https://docs.python.org/3/tutorial/",
    "java": "https://docs.oracle.com/javase/tutorial/",
    "react": "https://react.dev/learn",
    "power bi": "https://learn.microsoft.com/en-us/power-bi/",
    "excel": "https://support.microsoft.com/excel",
    "machine learning": "https://www.coursera.org/learn/machine-learning",
    "aws": "https://aws.amazon.com/getting-started/",
    "kubernetes": "https://kubernetes.io/docs/tutorials/",
}

PREREQ = {
    "spring boot": ["java"],
    "rest api": ["java"],
    "docker": ["git"],
    "kubernetes": ["docker"],
    "react": ["javascript"],
    "django": ["python"],
    "flask": ["python"],
    "tensorflow": ["python"],
}

DEFAULT_COMPANIES = [
    {"name": "TCS", "role": "Software Developer", "skills": ["java", "sql", "dsa", "git", "rest api"]},
    {"name": "Infosys", "role": "Backend Engineer", "skills": ["java", "spring boot", "sql", "rest api", "git"]},
    {"name": "Zoho", "role": "Full Stack Developer", "skills": ["javascript", "react", "node.js", "mongodb", "css"]},
    {"name": "Accenture", "role": "Data Analyst", "skills": ["python", "sql", "excel", "power bi", "statistics"]},
    {"name": "Wipro", "role": "Cloud Support Engineer", "skills": ["aws", "linux", "docker", "python", "git"]},
]

QUIZ = {
    "java": [
        {"q": "Which keyword is used to inherit a class in Java?", "o": ["extends", "implements", "inherits", "using"], "a": 0},
        {"q": "Java is primarily:", "o": ["Compiled only", "Interpreted only", "Compiled + interpreted (JVM)", "Neither"], "a": 2},
        {"q": "Which collection does NOT allow duplicates?", "o": ["List", "Set", "Array", "Queue"], "a": 1},
    ],
    "sql": [
        {"q": "Which command removes a table permanently?", "o": ["DELETE", "DROP", "TRUNCATE", "REMOVE"], "a": 1},
        {"q": "JOIN that returns only matching rows from both tables:", "o": ["LEFT JOIN", "RIGHT JOIN", "INNER JOIN", "FULL JOIN"], "a": 2},
        {"q": "Which clause filters grouped results?", "o": ["WHERE", "HAVING", "FILTER", "GROUP"], "a": 1},
    ],
    "python": [
        {"q": "Which is used to define a function?", "o": ["func", "def", "function", "lambda only"], "a": 1},
        {"q": "Python lists are:", "o": ["Immutable", "Mutable", "Fixed-size", "Read-only"], "a": 1},
        {"q": "What does len() return for a string?", "o": ["Byte size", "Character count", "Word count", "Line count"], "a": 1},
    ],
    "git": [
        {"q": "Which command creates a new branch?", "o": ["git branch <name>", "git new <name>", "git create <name>", "git init <name>"], "a": 0},
        {"q": "'git clone' is used to:", "o": ["Delete a repo", "Copy a remote repo locally", "Merge branches", "Revert commits"], "a": 1},
        {"q": "Which command stages changes for commit?", "o": ["git add", "git push", "git stage-only", "git commit -all"], "a": 0},
    ],
    "rest api": [
        {"q": "Which HTTP method is used to update a resource fully?", "o": ["GET", "POST", "PUT", "OPTIONS"], "a": 2},
        {"q": "REST APIs typically exchange data as:", "o": ["Only XML", "JSON (commonly)", "Binary only", "Plain text only"], "a": 1},
        {"q": "Status code 404 means:", "o": ["Server error", "Success", "Not Found", "Unauthorized"], "a": 2},
    ],
    "spring boot": [
        {"q": "Spring Boot mainly helps you:", "o": ["Design UI", "Quickly build Java backend apps", "Write CSS", "Manage DNS"], "a": 1},
        {"q": "Which annotation marks a REST controller?", "o": ["@Entity", "@RestController", "@Repository", "@Bean"], "a": 1},
        {"q": "Spring Boot apps are usually packaged as:", "o": ["EXE", "JAR", "DLL", "ISO"], "a": 1},
    ],
    "docker": [
        {"q": "A Dockerfile is used to:", "o": ["Run tests", "Define how an image is built", "Store logs", "Manage DNS"], "a": 1},
        {"q": "Docker containers share the host's:", "o": ["Kernel", "GPU driver only", "Keyboard", "Monitor"], "a": 0},
        {"q": "Which command lists running containers?", "o": ["docker ps", "docker list", "docker show", "docker active"], "a": 0},
    ],
    "excel": [
        {"q": "Which function adds a range of cells?", "o": ["TOTAL()", "SUM()", "ADD()", "PLUS()"], "a": 1},
        {"q": "VLOOKUP searches in:", "o": ["Rows only", "The first column of a range", "Any random cell", "Only headers"], "a": 1},
        {"q": "Pivot Tables are used to:", "o": ["Format text", "Summarise & analyse data", "Draw shapes", "Send email"], "a": 1},
    ],
}
