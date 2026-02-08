# generator.py
import re


def analyze_skills_for_career_track(skills, user_preferences=None):
    """Analyze skills to determine the most suitable career track, considering user preferences."""
    skills_lower = [skill.lower() for skill in skills]
    
    # Define career tracks and their associated skills
    career_tracks = {
        "Software Development": {
            "keywords": ["python", "java", "javascript", "c++", "c#", "react", "angular", "vue", "node.js", "django", "flask", "spring", "git", "docker", "kubernetes", "aws", "azure", "sql", "mongodb", "redis", "api", "rest", "graphql", "microservices", "agile", "scrum"],
            "description": "Software Development focuses on creating applications, websites, and software solutions."
        },
        "Data Science & Analytics": {
            "keywords": ["python", "r", "sql", "pandas", "numpy", "matplotlib", "seaborn", "scikit-learn", "tensorflow", "pytorch", "keras", "jupyter", "tableau", "powerbi", "excel", "statistics", "machine learning", "deep learning", "data visualization", "etl", "hadoop", "spark"],
            "description": "Data Science involves analyzing data to extract insights and build predictive models."
        },
        "DevOps & Cloud": {
            "keywords": ["docker", "kubernetes", "jenkins", "gitlab", "github", "aws", "azure", "gcp", "terraform", "ansible", "linux", "bash", "python", "shell", "ci/cd", "monitoring", "logging", "prometheus", "grafana", "nginx", "apache"],
            "description": "DevOps focuses on automation, infrastructure management, and cloud services."
        },
        "Cybersecurity": {
            "keywords": ["security", "penetration testing", "ethical hacking", "network security", "firewall", "vulnerability assessment", "siem", "wireshark", "nmap", "metasploit", "kali linux", "compliance", "gdpr", "iso 27001", "nist", "cryptography"],
            "description": "Cybersecurity involves protecting systems, networks, and data from digital attacks."
        },
        "Product Management": {
            "keywords": ["product management", "agile", "scrum", "kanban", "jira", "confluence", "user stories", "roadmap", "market research", "competitive analysis", "stakeholder management", "project management", "prd", "mrr", "user experience", "ux"],
            "description": "Product Management focuses on developing and managing products that meet user needs."
        },
        "UI/UX Design": {
            "keywords": ["figma", "adobe xd", "sketch", "invision", "user experience", "user interface", "wireframing", "prototyping", "user research", "usability testing", "design systems", "responsive design", "accessibility", "photoshop", "illustrator"],
            "description": "UI/UX Design focuses on creating user-friendly and visually appealing interfaces."
        },
        "Artificial Intelligence & Machine Learning": {
            "keywords": ["python", "tensorflow", "pytorch", "keras", "scikit-learn", "deep learning", "machine learning", "neural networks", "nlp", "computer vision", "reinforcement learning", "data science", "statistics", "mathematics", "algorithms"],
            "description": "AI/ML focuses on developing intelligent systems and algorithms that can learn and make decisions."
        },
        "Mobile Development": {
            "keywords": ["swift", "kotlin", "java", "react native", "flutter", "xamarin", "ios", "android", "mobile app", "app development", "mobile ui", "mobile testing", "app store", "google play"],
            "description": "Mobile Development focuses on creating applications for smartphones and tablets."
        },
        "Web Development": {
            "keywords": ["html", "css", "javascript", "react", "angular", "vue", "node.js", "php", "python", "django", "flask", "wordpress", "web design", "frontend", "backend", "full stack"],
            "description": "Web Development focuses on creating websites and web applications."
        },
        "Game Development": {
            "keywords": ["unity", "unreal engine", "c++", "c#", "game design", "3d modeling", "animation", "game physics", "game engine", "opengl", "directx", "game programming"],
            "description": "Game Development focuses on creating interactive games and entertainment software."
        },
        "Blockchain & Web3": {
            "keywords": ["blockchain", "ethereum", "bitcoin", "solidity", "smart contracts", "web3", "defi", "nft", "cryptocurrency", "distributed systems", "cryptography"],
            "description": "Blockchain & Web3 focuses on decentralized applications and cryptocurrency technologies."
        },
        "Business Consulting": {
            "keywords": ["business", "consulting", "strategy", "management", "analysis", "excel", "powerpoint", "presentation", "client", "stakeholder", "project management", "business process", "optimization", "change management", "financial analysis", "market research", "competitive analysis", "business development", "operations", "strategy consulting", "management consulting", "advisory", "business intelligence", "data analysis", "process improvement"],
            "description": "Business Consulting focuses on helping organizations improve performance, solve problems, and achieve strategic objectives through expert advice and analysis."
        }
    }
    
    # If user has specified an area of interest, prioritize it
    if user_preferences and user_preferences.get("area_of_interest"):
        user_interest = user_preferences["area_of_interest"].lower()
        
        # Direct match with career tracks
        for track_name in career_tracks.keys():
            if user_interest in track_name.lower() or track_name.lower() in user_interest:
                return track_name, career_tracks[track_name]["description"]
        
        # Check for business consulting variations
        business_keywords = ["business consultant", "business consulting", "consultant", "consulting", "business advisor", "business advisory"]
        if any(keyword in user_interest for keyword in business_keywords):
            return "Business Consulting", career_tracks["Business Consulting"]["description"]
        
        # Check for other common variations
        if "data science" in user_interest or "data analyst" in user_interest:
            return "Data Science & Analytics", career_tracks["Data Science & Analytics"]["description"]
        elif "product" in user_interest and "management" in user_interest:
            return "Product Management", career_tracks["Product Management"]["description"]
        elif "ui" in user_interest or "ux" in user_interest or "design" in user_interest:
            return "UI/UX Design", career_tracks["UI/UX Design"]["description"]
        elif "ai" in user_interest or "machine learning" in user_interest or "artificial intelligence" in user_interest:
            return "Artificial Intelligence & Machine Learning", career_tracks["Artificial Intelligence & Machine Learning"]["description"]
        elif "mobile" in user_interest or "app" in user_interest:
            return "Mobile Development", career_tracks["Mobile Development"]["description"]
        elif "web" in user_interest:
            return "Web Development", career_tracks["Web Development"]["description"]
        elif "game" in user_interest:
            return "Game Development", career_tracks["Game Development"]["description"]
        elif "blockchain" in user_interest or "web3" in user_interest:
            return "Blockchain & Web3", career_tracks["Blockchain & Web3"]["description"]
        elif "cybersecurity" in user_interest or "security" in user_interest:
            return "Cybersecurity", career_tracks["Cybersecurity"]["description"]
        elif "devops" in user_interest or "cloud" in user_interest:
            return "DevOps & Cloud", career_tracks["DevOps & Cloud"]["description"]
        elif "software" in user_interest or "programming" in user_interest or "developer" in user_interest:
            return "Software Development", career_tracks["Software Development"]["description"]
        
        # If no direct match found, find the closest match based on skills
        best_match = None
        best_score = 0
        for track, info in career_tracks.items():
            score = 0
            for keyword in info["keywords"]:
                for skill in skills_lower:
                    if keyword in skill or skill in keyword:
                        score += 1
            if score > best_score:
                best_score = score
                best_match = track
        
        if best_match:
            return best_match, f"{career_tracks[best_match]['description']} (Closest match to your interest in {user_preferences['area_of_interest']})"
    
    # Calculate scores for each career track
    scores = {}
    for track, info in career_tracks.items():
        score = 0
        for keyword in info["keywords"]:
            for skill in skills_lower:
                if keyword in skill or skill in keyword:
                    score += 1
        scores[track] = score
    
    # Return the track with the highest score, or a default
    if max(scores.values()) > 0:
        best_track = max(scores, key=scores.get)
        return best_track, career_tracks[best_track]["description"]
    else:
        return "General Technology", "A broad technology career path suitable for various roles."


def analyze_skills_and_tech_stack(career_track, current_skills):
    """Analyze required skills, missing skills, and tech stack for a career track."""
    
    # Define comprehensive skill requirements and tech stacks for each career track
    skill_requirements = {
        "Software Development": {
            "core_skills": {
                "Programming Languages": ["Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust"],
                "Web Technologies": ["HTML", "CSS", "React", "Angular", "Vue.js", "Node.js"],
                "Backend Frameworks": ["Django", "Flask", "Spring Boot", "Express.js", "FastAPI"],
                "Databases": ["SQL", "MongoDB", "PostgreSQL", "Redis", "MySQL"],
                "Version Control": ["Git", "GitHub", "GitLab"],
                "Cloud Platforms": ["AWS", "Azure", "Google Cloud", "Heroku"],
                "DevOps Tools": ["Docker", "Kubernetes", "Jenkins", "CI/CD"],
                "Testing": ["JUnit", "PyTest", "Jest", "Selenium"],
                "Architecture": ["Microservices", "REST APIs", "GraphQL", "System Design"]
            },
            "tech_stack": {
                "Frontend": ["React", "Angular", "Vue.js", "TypeScript", "Redux", "Next.js"],
                "Backend": ["Node.js", "Python", "Java", "Spring Boot", "Django", "FastAPI"],
                "Database": ["PostgreSQL", "MongoDB", "Redis", "MySQL", "Elasticsearch"],
                "Cloud": ["AWS", "Azure", "Google Cloud", "Docker", "Kubernetes"],
                "Tools": ["Git", "Jenkins", "Jira", "Postman", "VS Code"]
            }
        },
        "UI/UX Design": {
            "core_skills": {
                "Design Tools": ["Figma", "Adobe XD", "Sketch", "InVision", "Adobe Photoshop", "Adobe Illustrator"],
                "Prototyping": ["Wireframing", "Prototyping", "User Flows", "Information Architecture"],
                "User Research": ["User Interviews", "Usability Testing", "User Personas", "User Journey Mapping"],
                "Design Principles": ["Visual Design", "Typography", "Color Theory", "Layout Design"],
                "Design Systems": ["Component Libraries", "Design Tokens", "Style Guides", "Brand Guidelines"],
                "Accessibility": ["WCAG Guidelines", "Accessibility Testing", "Inclusive Design"],
                "Collaboration": ["Stakeholder Management", "Design Presentations", "Feedback Integration"],
                "Analytics": ["User Analytics", "A/B Testing", "Heatmaps", "Conversion Optimization"]
            },
            "tech_stack": {
                "Design Tools": ["Figma", "Adobe XD", "Sketch", "InVision", "Adobe Creative Suite"],
                "Prototyping": ["Framer", "Principle", "Protopie", "Axure RP"],
                "Research": ["UserTesting", "Hotjar", "FullStory", "Google Analytics"],
                "Collaboration": ["Slack", "Microsoft Teams", "Zoom", "Miro", "Notion"],
                "Development": ["HTML", "CSS", "JavaScript", "React", "Vue.js"]
            }
        },
        "Data Science & Analytics": {
            "core_skills": {
                "Programming": ["Python", "R", "SQL", "Scala", "Julia"],
                "Data Manipulation": ["Pandas", "NumPy", "dplyr", "DataFrames"],
                "Visualization": ["Matplotlib", "Seaborn", "Plotly", "Tableau", "Power BI"],
                "Machine Learning": ["Scikit-learn", "TensorFlow", "PyTorch", "Keras"],
                "Big Data": ["Hadoop", "Spark", "Hive", "Kafka"],
                "Statistics": ["Statistical Analysis", "Hypothesis Testing", "A/B Testing"],
                "Databases": ["SQL", "NoSQL", "Data Warehousing", "ETL"],
                "Tools": ["Jupyter", "RStudio", "Apache Airflow", "MLflow"]
            },
            "tech_stack": {
                "Languages": ["Python", "R", "SQL", "Scala"],
                "Libraries": ["Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch"],
                "Visualization": ["Tableau", "Power BI", "Matplotlib", "Seaborn"],
                "Big Data": ["Apache Spark", "Hadoop", "Kafka", "Airflow"],
                "Cloud": ["AWS SageMaker", "Azure ML", "Google AI Platform", "Databricks"]
            }
        },
        "DevOps & Cloud": {
            "core_skills": {
                "Cloud Platforms": ["AWS", "Azure", "Google Cloud", "DigitalOcean"],
                "Containerization": ["Docker", "Kubernetes", "Rancher", "OpenShift"],
                "CI/CD": ["Jenkins", "GitLab CI", "GitHub Actions", "CircleCI"],
                "Infrastructure as Code": ["Terraform", "CloudFormation", "Ansible", "Chef"],
                "Monitoring": ["Prometheus", "Grafana", "ELK Stack", "Datadog"],
                "Operating Systems": ["Linux", "Windows Server", "Shell Scripting"],
                "Networking": ["TCP/IP", "DNS", "Load Balancing", "VPN"],
                "Security": ["IAM", "Security Groups", "Compliance", "Vulnerability Management"]
            },
            "tech_stack": {
                "Cloud": ["AWS", "Azure", "Google Cloud", "Terraform", "Ansible"],
                "Containers": ["Docker", "Kubernetes", "Helm", "Istio"],
                "CI/CD": ["Jenkins", "GitLab", "GitHub Actions", "ArgoCD"],
                "Monitoring": ["Prometheus", "Grafana", "ELK Stack", "Datadog"],
                "Security": ["Vault", "Secrets Manager", "WAF", "Security Hub"]
            }
        },
        "Cybersecurity": {
            "core_skills": {
                "Security Tools": ["Wireshark", "Nmap", "Metasploit", "Burp Suite", "Kali Linux"],
                "Network Security": ["Firewalls", "IDS/IPS", "VPN", "Network Monitoring"],
                "Application Security": ["OWASP", "Penetration Testing", "Code Review", "SAST/DAST"],
                "Incident Response": ["SIEM", "Forensics", "Threat Hunting", "Malware Analysis"],
                "Compliance": ["GDPR", "ISO 27001", "NIST", "SOC 2"],
                "Cryptography": ["Encryption", "Hashing", "Digital Signatures", "PKI"],
                "Operating Systems": ["Linux", "Windows", "macOS Security"],
                "Programming": ["Python", "Bash", "PowerShell", "C/C++"]
            },
            "tech_stack": {
                "Security Tools": ["Kali Linux", "Metasploit", "Nmap", "Wireshark"],
                "SIEM": ["Splunk", "QRadar", "ELK Stack", "Microsoft Sentinel"],
                "Vulnerability Management": ["Nessus", "Qualys", "OpenVAS", "Nexpose"],
                "Forensics": ["Autopsy", "Volatility", "FTK", "EnCase"],
                "Cloud Security": ["AWS Security Hub", "Azure Security Center", "Prisma Cloud"]
            }
        },
        "Product Management": {
            "core_skills": {
                "Product Strategy": ["Product Vision", "Roadmapping", "Market Analysis", "Competitive Analysis"],
                "User Research": ["User Interviews", "Surveys", "Usability Testing", "Analytics"],
                "Agile Methodologies": ["Scrum", "Kanban", "Sprint Planning", "User Stories"],
                "Data Analysis": ["SQL", "Google Analytics", "A/B Testing", "Metrics"],
                "Communication": ["Stakeholder Management", "Presentation Skills", "Documentation"],
                "Business Acumen": ["Business Models", "Pricing Strategy", "Go-to-Market", "ROI Analysis"],
                "Tools": ["Jira", "Confluence", "Figma", "Mixpanel", "Amplitude"]
            },
            "tech_stack": {
                "Product Management": ["Jira", "Confluence", "Aha!", "Productboard"],
                "Analytics": ["Google Analytics", "Mixpanel", "Amplitude", "Tableau"],
                "Design": ["Figma", "Sketch", "InVision", "Adobe XD"],
                "Communication": ["Slack", "Microsoft Teams", "Zoom", "Loom"],
                "Research": ["SurveyMonkey", "UserTesting", "Hotjar", "FullStory"]
            }
        },
        "Business Consulting": {
            "core_skills": {
                "Analytical Tools": ["Excel", "PowerPoint", "Tableau", "Power BI", "SQL"],
                "Business Analysis": ["Business Process Analysis", "Financial Analysis", "Market Research"],
                "Strategy": ["Strategic Planning", "Competitive Analysis", "Business Model Design"],
                "Project Management": ["Agile", "Scrum", "Kanban", "Project Planning"],
                "Communication": ["Presentation Skills", "Client Management", "Stakeholder Management"],
                "Methodologies": ["Lean Six Sigma", "Change Management", "Process Improvement"],
                "Industry Knowledge": ["Operations Management", "Financial Management", "Marketing"],
                "Tools": ["Microsoft Office", "Visio", "Jira", "Confluence", "Miro"]
            },
            "tech_stack": {
                "Analytics": ["Excel", "Power BI", "Tableau", "SQL", "Python"],
                "Presentation": ["PowerPoint", "Prezi", "Canva", "Adobe Creative Suite"],
                "Project Management": ["Jira", "Confluence", "Monday.com", "Asana"],
                "Collaboration": ["Slack", "Microsoft Teams", "Zoom", "Miro"],
                "CRM": ["Salesforce", "HubSpot", "Microsoft Dynamics"]
            }
        },
        "Artificial Intelligence & Machine Learning": {
            "core_skills": {
                "Programming": ["Python", "R", "Julia", "C++", "Java"],
                "Machine Learning": ["Scikit-learn", "TensorFlow", "PyTorch", "Keras", "XGBoost"],
                "Deep Learning": ["Neural Networks", "CNN", "RNN", "LSTM", "Transformers"],
                "Data Processing": ["Pandas", "NumPy", "Scipy", "DataFrames", "ETL"],
                "Mathematics": ["Linear Algebra", "Calculus", "Statistics", "Probability"],
                "Specializations": ["NLP", "Computer Vision", "Reinforcement Learning", "Time Series"],
                "Tools": ["Jupyter", "Google Colab", "MLflow", "Weights & Biases"],
                "Deployment": ["Docker", "Kubernetes", "AWS SageMaker", "Azure ML"]
            },
            "tech_stack": {
                "Languages": ["Python", "R", "Julia", "C++"],
                "Frameworks": ["TensorFlow", "PyTorch", "Scikit-learn", "Keras"],
                "Cloud": ["AWS SageMaker", "Azure ML", "Google AI Platform", "Databricks"],
                "Tools": ["Jupyter", "MLflow", "Weights & Biases", "DVC"],
                "Deployment": ["Docker", "Kubernetes", "Flask", "FastAPI"]
            }
        },
        "Mobile Development": {
            "core_skills": {
                "Platforms": ["iOS", "Android", "Cross-platform"],
                "Languages": ["Swift", "Kotlin", "Java", "Dart", "JavaScript"],
                "Frameworks": ["React Native", "Flutter", "Xamarin", "Ionic"],
                "Development": ["Mobile UI", "App Lifecycle", "State Management", "Navigation"],
                "Testing": ["Unit Testing", "UI Testing", "Integration Testing"],
                "Deployment": ["App Store", "Google Play", "CI/CD", "Code Signing"],
                "Performance": ["Memory Management", "Battery Optimization", "Network Optimization"],
                "Tools": ["Xcode", "Android Studio", "VS Code", "Firebase"]
            },
            "tech_stack": {
                "Native": ["Swift", "Kotlin", "Xcode", "Android Studio"],
                "Cross-platform": ["React Native", "Flutter", "Xamarin"],
                "Backend": ["Firebase", "AWS Amplify", "Parse Server"],
                "Testing": ["Jest", "Detox", "Espresso", "XCUITest"],
                "Deployment": ["Fastlane", "App Center", "CodePush"]
            }
        },
        "Web Development": {
            "core_skills": {
                "Frontend": ["HTML", "CSS", "JavaScript", "TypeScript"],
                "Frameworks": ["React", "Angular", "Vue.js", "Next.js", "Nuxt.js"],
                "Backend": ["Node.js", "Python", "PHP", "Java", "C#"],
                "Databases": ["MySQL", "PostgreSQL", "MongoDB", "Redis"],
                "APIs": ["REST", "GraphQL", "SOAP", "Microservices"],
                "Performance": ["SEO", "Web Performance", "Caching", "CDN"],
                "Security": ["Web Security", "HTTPS", "Authentication", "Authorization"],
                "Tools": ["Git", "VS Code", "Chrome DevTools", "Postman"]
            },
            "tech_stack": {
                "Frontend": ["React", "Angular", "Vue.js", "TypeScript", "Tailwind CSS"],
                "Backend": ["Node.js", "Express", "Django", "Flask", "Laravel"],
                "Database": ["PostgreSQL", "MongoDB", "Redis", "MySQL"],
                "Cloud": ["AWS", "Vercel", "Netlify", "Heroku"],
                "Tools": ["Git", "Docker", "Jenkins", "VS Code"]
            }
        },
        "Game Development": {
            "core_skills": {
                "Engines": ["Unity", "Unreal Engine", "Godot", "CryEngine"],
                "Programming": ["C#", "C++", "Python", "Lua", "JavaScript"],
                "Game Design": ["Game Mechanics", "Level Design", "Game Balance", "Narrative"],
                "Graphics": ["3D Modeling", "Animation", "Texturing", "Rendering"],
                "Audio": ["Sound Design", "Music Integration", "Audio Programming"],
                "Physics": ["Game Physics", "Collision Detection", "Particle Systems"],
                "Networking": ["Multiplayer", "Networking", "Server Architecture"],
                "Tools": ["Blender", "Maya", "Photoshop", "Audacity"]
            },
            "tech_stack": {
                "Engines": ["Unity", "Unreal Engine", "Godot"],
                "Languages": ["C#", "C++", "Python", "Lua"],
                "Graphics": ["Blender", "Maya", "3ds Max", "Substance Painter"],
                "Audio": ["FMOD", "Wwise", "Audacity"],
                "Platforms": ["PC", "Mobile", "Console", "VR/AR"]
            }
        },
        "Blockchain & Web3": {
            "core_skills": {
                "Blockchain": ["Ethereum", "Bitcoin", "Smart Contracts", "Solidity"],
                "Programming": ["Solidity", "Rust", "JavaScript", "Python", "Go"],
                "DeFi": ["DeFi Protocols", "Yield Farming", "Liquidity Pools", "DEX"],
                "NFTs": ["NFT Standards", "ERC-721", "ERC-1155", "Marketplaces"],
                "Web3": ["Web3.js", "Ethers.js", "MetaMask", "Wallet Integration"],
                "Security": ["Cryptography", "Auditing", "Penetration Testing"],
                "Networks": ["Layer 2", "Polygon", "Solana", "Polkadot"],
                "Tools": ["Hardhat", "Truffle", "Remix", "Ganache"]
            },
            "tech_stack": {
                "Blockchain": ["Ethereum", "Bitcoin", "Polygon", "Solana"],
                "Development": ["Solidity", "Rust", "Hardhat", "Truffle"],
                "Frontend": ["React", "Web3.js", "Ethers.js", "MetaMask"],
                "Tools": ["Remix", "Ganache", "Infura", "Alchemy"],
                "DeFi": ["Uniswap", "Compound", "Aave", "Curve"]
            }
        },
        "DevOps & Cloud": {
            "core_skills": {
                "Cloud Platforms": ["AWS", "Azure", "Google Cloud", "DigitalOcean"],
                "Containerization": ["Docker", "Kubernetes", "Rancher", "OpenShift"],
                "CI/CD": ["Jenkins", "GitLab CI", "GitHub Actions", "CircleCI"],
                "Infrastructure as Code": ["Terraform", "CloudFormation", "Ansible", "Chef"],
                "Monitoring": ["Prometheus", "Grafana", "ELK Stack", "Datadog"],
                "Operating Systems": ["Linux", "Windows Server", "Shell Scripting"],
                "Networking": ["TCP/IP", "DNS", "Load Balancing", "VPN"],
                "Security": ["IAM", "Security Groups", "Compliance", "Vulnerability Management"]
            },
            "tech_stack": {
                "Cloud": ["AWS", "Azure", "Google Cloud", "Terraform", "Ansible"],
                "Containers": ["Docker", "Kubernetes", "Helm", "Istio"],
                "CI/CD": ["Jenkins", "GitLab", "GitHub Actions", "ArgoCD"],
                "Monitoring": ["Prometheus", "Grafana", "ELK Stack", "Datadog"],
                "Security": ["Vault", "Secrets Manager", "WAF", "Security Hub"]
            }
        },
        "Cybersecurity": {
            "core_skills": {
                "Security Tools": ["Wireshark", "Nmap", "Metasploit", "Burp Suite", "Kali Linux"],
                "Network Security": ["Firewalls", "IDS/IPS", "VPN", "Network Monitoring"],
                "Application Security": ["OWASP", "Penetration Testing", "Code Review", "SAST/DAST"],
                "Incident Response": ["SIEM", "Forensics", "Threat Hunting", "Malware Analysis"],
                "Compliance": ["GDPR", "ISO 27001", "NIST", "SOC 2"],
                "Cryptography": ["Encryption", "Hashing", "Digital Signatures", "PKI"],
                "Operating Systems": ["Linux", "Windows", "macOS Security"],
                "Programming": ["Python", "Bash", "PowerShell", "C/C++"]
            },
            "tech_stack": {
                "Security Tools": ["Kali Linux", "Metasploit", "Nmap", "Wireshark"],
                "SIEM": ["Splunk", "QRadar", "ELK Stack", "Microsoft Sentinel"],
                "Vulnerability Management": ["Nessus", "Qualys", "OpenVAS", "Nexpose"],
                "Forensics": ["Autopsy", "Volatility", "FTK", "EnCase"],
                "Cloud Security": ["AWS Security Hub", "Azure Security Center", "Prisma Cloud"]
            }
        },
        "Product Management": {
            "core_skills": {
                "Product Strategy": ["Product Vision", "Roadmapping", "Market Analysis", "Competitive Analysis"],
                "User Research": ["User Interviews", "Surveys", "Usability Testing", "Analytics"],
                "Agile Methodologies": ["Scrum", "Kanban", "Sprint Planning", "User Stories"],
                "Data Analysis": ["SQL", "Google Analytics", "A/B Testing", "Metrics"],
                "Communication": ["Stakeholder Management", "Presentation Skills", "Documentation"],
                "Business Acumen": ["Business Models", "Pricing Strategy", "Go-to-Market", "ROI Analysis"],
                "Tools": ["Jira", "Confluence", "Figma", "Mixpanel", "Amplitude"]
            },
            "tech_stack": {
                "Product Management": ["Jira", "Confluence", "Aha!", "Productboard"],
                "Analytics": ["Google Analytics", "Mixpanel", "Amplitude", "Tableau"],
                "Design": ["Figma", "Sketch", "InVision", "Adobe XD"],
                "Communication": ["Slack", "Microsoft Teams", "Zoom", "Loom"],
                "Research": ["SurveyMonkey", "UserTesting", "Hotjar", "FullStory"]
            }
        }
    }
    
    # Get requirements for the career track
    requirements = skill_requirements.get(career_track, skill_requirements["Software Development"])
    
    # Analyze current skills vs required skills
    current_skills_lower = [skill.lower() for skill in current_skills]
    current_skills_set = set(current_skills_lower)
    
    # Find matching and missing skills
    matching_skills = {}
    missing_skills = {}
    
    for category, skills in requirements["core_skills"].items():
        matching = []
        missing = []
        
        for skill in skills:
            skill_lower = skill.lower()
            # Check for exact or partial matches with better logic
            found_match = False
            for current_skill in current_skills_set:
                # Check for exact match or if current skill contains the required skill
                if (skill_lower == current_skill or 
                    skill_lower in current_skill or 
                    current_skill in skill_lower):
                    # Additional check to avoid false positives
                    if len(skill_lower) > 2:  # Avoid matching very short strings
                        matching.append(skill)
                        found_match = True
                        break
            
            if not found_match:
                missing.append(skill)
        
        if matching:
            matching_skills[category] = matching
        if missing:
            missing_skills[category] = missing
    
    return {
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "tech_stack": requirements["tech_stack"],
        "skill_gap_percentage": calculate_skill_gap_percentage(matching_skills, missing_skills)
    }


def calculate_skill_gap_percentage(matching_skills, missing_skills):
    """Calculate the percentage of skills gap."""
    total_matching = sum(len(skills) for skills in matching_skills.values())
    total_missing = sum(len(skills) for skills in missing_skills.values())
    total_skills = total_matching + total_missing
    
    if total_skills == 0:
        return 0
    
    return round((total_missing / total_skills) * 100, 1)


def generate_dynamic_stage_recommendations(career_track, skills, experience, education, user_preferences=None):
    """Dynamically generate personalized recommendations based on user's specific inputs and resume analysis."""
    
    # Analyze current skill gaps and strengths
    skills_lower = [skill.lower() for skill in skills]
    user_interest = user_preferences.get("area_of_interest", "") if user_preferences else ""
    timeline = user_preferences.get("timeline", "") if user_preferences else ""
    future_goals = user_preferences.get("future_goals", []) if user_preferences else []
    
    # Define skill categories for different career tracks
    skill_categories = {
        "Software Development": {
            "core_languages": ["python", "java", "javascript", "c++", "c#", "go", "rust"],
            "frameworks": ["react", "angular", "vue", "django", "flask", "spring", "express", "fastapi"],
            "databases": ["sql", "mongodb", "redis", "postgresql", "mysql"],
            "tools": ["git", "docker", "kubernetes", "jenkins", "aws", "azure"],
            "concepts": ["api", "rest", "graphql", "microservices", "agile", "scrum"]
        },
        "Data Science & Analytics": {
            "languages": ["python", "r", "sql", "scala"],
            "libraries": ["pandas", "numpy", "matplotlib", "seaborn", "scikit-learn", "tensorflow", "pytorch"],
            "tools": ["jupyter", "tableau", "powerbi", "excel", "spark", "hadoop"],
            "concepts": ["statistics", "machine learning", "deep learning", "data visualization", "etl"]
        },
        "DevOps & Cloud": {
            "platforms": ["aws", "azure", "gcp", "digitalocean"],
            "containers": ["docker", "kubernetes", "rancher"],
            "automation": ["jenkins", "gitlab", "github actions", "terraform", "ansible"],
            "monitoring": ["prometheus", "grafana", "elk stack", "datadog"],
            "os": ["linux", "bash", "shell scripting"]
        },
        "Cybersecurity": {
            "tools": ["wireshark", "nmap", "metasploit", "burp suite", "kali linux"],
            "concepts": ["penetration testing", "ethical hacking", "network security", "vulnerability assessment"],
            "frameworks": ["nist", "iso 27001", "gdpr", "compliance"],
            "domains": ["web security", "network security", "application security", "incident response"]
        },
        "Product Management": {
            "methodologies": ["agile", "scrum", "kanban", "lean"],
            "tools": ["jira", "confluence", "figma", "monday.com", "notion"],
            "skills": ["user research", "market research", "competitive analysis", "stakeholder management"],
            "concepts": ["user stories", "roadmap", "prd", "mrr", "user experience"]
        },
        "UI/UX Design": {
            "tools": ["figma", "adobe xd", "sketch", "invision", "photoshop", "illustrator"],
            "skills": ["wireframing", "prototyping", "user research", "usability testing"],
            "concepts": ["design systems", "responsive design", "accessibility", "user experience", "user interface"]
        },
        "Artificial Intelligence & Machine Learning": {
            "languages": ["python", "r", "julia"],
            "libraries": ["tensorflow", "pytorch", "keras", "scikit-learn", "numpy", "pandas"],
            "domains": ["nlp", "computer vision", "reinforcement learning", "deep learning"],
            "concepts": ["neural networks", "statistics", "mathematics", "algorithms", "optimization"]
        },
        "Mobile Development": {
            "platforms": ["ios", "android", "react native", "flutter", "xamarin"],
            "languages": ["swift", "kotlin", "java", "dart", "javascript"],
            "concepts": ["mobile ui", "app lifecycle", "mobile testing", "app store", "google play"]
        },
        "Web Development": {
            "frontend": ["html", "css", "javascript", "react", "angular", "vue"],
            "backend": ["node.js", "php", "python", "django", "flask", "express"],
            "concepts": ["responsive design", "web security", "seo", "performance", "full stack"]
        },
        "Game Development": {
            "engines": ["unity", "unreal engine", "godot"],
            "languages": ["c++", "c#", "python", "lua"],
            "skills": ["game design", "3d modeling", "animation", "game physics"],
            "concepts": ["game mechanics", "level design", "game optimization"]
        },
        "Blockchain & Web3": {
            "platforms": ["ethereum", "bitcoin", "polygon", "solana"],
            "languages": ["solidity", "rust", "javascript", "python"],
            "concepts": ["smart contracts", "defi", "nft", "web3", "cryptography", "distributed systems"]
        },
        "Business Consulting": {
            "analytical_tools": ["excel", "powerpoint", "tableau", "powerbi", "sql", "python", "r"],
            "methodologies": ["business process improvement", "change management", "strategic planning", "lean six sigma", "agile"],
            "skills": ["business analysis", "financial analysis", "market research", "competitive analysis", "stakeholder management"],
            "concepts": ["business strategy", "operations management", "organizational development", "performance optimization", "risk management"],
            "domains": ["strategy consulting", "management consulting", "operations consulting", "financial consulting", "technology consulting"]
        }
    }
    
    # Get relevant skills for the career track
    track_skills = skill_categories.get(career_track, skill_categories["Software Development"])
    
    # Analyze current skills vs required skills
    current_skills = set()
    missing_skills = set()
    
    for category, skill_list in track_skills.items():
        for skill in skill_list:
            if any(skill.lower() in existing_skill.lower() or existing_skill.lower() in skill.lower() 
                   for existing_skill in skills):
                current_skills.add(skill)
            else:
                missing_skills.add(skill)
    
    # Generate dynamic stage recommendations
    stage1_recs = []
    stage2_recs = []
    stage3_recs = []
    
    # Stage 1: Entry Level (0-2 years) - Focus on foundational skills
    if missing_skills:
        # Prioritize missing core skills
        core_missing = list(missing_skills)[:5]  # Top 5 missing skills
        for skill in core_missing:
            if skill in track_skills.get("languages", []) + track_skills.get("core_languages", []) + track_skills.get("analytical_tools", []):
                stage1_recs.append(f"Master {skill} fundamentals and best practices")
            elif skill in track_skills.get("tools", []) + track_skills.get("platforms", []) + track_skills.get("methodologies", []):
                stage1_recs.append(f"Learn {skill} and gain hands-on experience")
            elif skill in track_skills.get("concepts", []) + track_skills.get("skills", []) + track_skills.get("domains", []):
                stage1_recs.append(f"Understand {skill} principles and applications")
    
    # Add general foundational recommendations based on career track
    if career_track == "Business Consulting":
        stage1_recs.extend([
            "Develop strong business analysis and problem-solving skills",
            "Master Excel, PowerPoint, and other business tools",
            "Learn business process improvement methodologies",
            "Build client relationship and communication skills",
            "Gain experience in data analysis and market research"
        ])
    else:
        # Technical track foundational skills
        if len(stage1_recs) < 5:
            stage1_recs.extend([
                "Build a strong portfolio of projects showcasing your skills",
                "Practice problem-solving and algorithmic thinking",
                "Learn version control and collaboration tools",
                "Develop strong communication and teamwork abilities",
                "Gain practical experience through internships or entry-level positions"
            ])
    
    # Stage 2: Mid-Level (2-5 years) - Focus on specialization and leadership
    if current_skills:
        # Build on existing strengths
        existing_strengths = list(current_skills)[:3]
        for skill in existing_strengths:
            stage2_recs.append(f"Deepen expertise in {skill} and related areas")
    
    # Add specialization recommendations based on career track
    if career_track == "Business Consulting":
        stage2_recs.extend([
            "Specialize in specific consulting domains (strategy, operations, technology)",
            "Lead client engagements and project teams",
            "Develop expertise in industry-specific business challenges",
            "Build a network of clients and industry professionals",
            "Master advanced business analysis and presentation skills"
        ])
    else:
        # Technical track specialization
        stage2_recs.extend([
            "Specialize in a specific domain within your field",
            "Take on project leadership and mentorship responsibilities",
            "Contribute to open source projects and communities",
            "Develop advanced problem-solving and system design skills",
            "Build a professional network and personal brand"
        ])
    
    # Stage 3: Senior Level (5+ years) - Focus on strategic leadership
    if career_track == "Business Consulting":
        stage3_recs = [
            "Lead major consulting engagements and strategic initiatives",
            "Mentor junior consultants and develop consulting teams",
            "Drive business transformation and organizational change",
            "Establish thought leadership in business consulting",
            "Develop strategic partnerships and business development skills",
            "Lead cross-functional teams and organizational initiatives",
            "Publish research, write books, or create educational content"
        ]
    else:
        # Technical track leadership
        stage3_recs = [
            "Lead major projects and architectural decisions",
            "Mentor and guide teams of professionals",
            "Drive innovation and best practices in your organization",
            "Contribute to industry standards and thought leadership",
            "Develop strategic vision and business acumen"
        ]
    
    # Customize based on user preferences
    if user_preferences:
        # Timeline adjustments
        if "Fast-track" in timeline:
            stage1_recs = stage1_recs[:4]  # Focus on fewer, critical skills
            stage2_recs = stage2_recs[:4]
            stage3_recs = stage3_recs[:4]
            stage1_recs.append("Accelerate learning through intensive bootcamps or courses")
            stage2_recs.append("Seek rapid advancement opportunities and challenging projects")
        
        # Goal-specific additions
        if "Become a technical leader/architect" in future_goals:
            if career_track == "Business Consulting":
                stage1_recs.append("Study business architecture and strategic frameworks")
                stage2_recs.append("Lead business transformation and change initiatives")
                stage3_recs.append("Define business strategy and organizational standards")
            else:
                stage1_recs.append("Study system design and architecture patterns")
                stage2_recs.append("Lead technical design discussions and decisions")
                stage3_recs.append("Define technical strategy and standards for organizations")
        
        if "Move into management/leadership" in future_goals:
            stage1_recs.append("Develop leadership and communication skills")
            stage2_recs.append("Take on team lead and project management roles")
            stage3_recs.append("Lead cross-functional teams and organizational initiatives")
        
        if "Start my own company/entrepreneurship" in future_goals:
            stage1_recs.append("Learn business fundamentals and startup methodologies")
            stage2_recs.append("Build a network of potential co-founders and investors")
            stage3_recs.append("Develop business strategy and fundraising skills")
        
        if "Work for top tech companies (FAANG)" in future_goals:
            if career_track == "Business Consulting":
                stage1_recs.append("Study business strategy and competitive analysis")
                stage2_recs.append("Build expertise in technology consulting and digital transformation")
                stage3_recs.append("Lead strategic initiatives for major technology companies")
            else:
                stage1_recs.append("Practice coding interviews and system design problems")
                stage2_recs.append("Build projects that demonstrate scalability and complexity")
                stage3_recs.append("Contribute to large-scale systems and high-impact projects")
        
        if "Work remotely/freelance" in future_goals:
            stage1_recs.append("Build a strong online presence and portfolio")
            stage2_recs.append("Develop client management and project delivery skills")
            stage3_recs.append("Establish thought leadership and personal brand")
        
        if "Become a subject matter expert" in future_goals:
            stage1_recs.append("Deep dive into specific technologies or business domains")
            stage2_recs.append("Contribute to professional communities and conferences")
            stage3_recs.append("Publish research, write books, or create educational content")
        
        if "Achieve work-life balance" in future_goals:
            stage1_recs.append("Develop time management and prioritization skills")
            stage2_recs.append("Establish boundaries and sustainable work practices")
            stage3_recs.append("Create flexible work arrangements and team policies")
    
    # Ensure we have enough recommendations
    while len(stage1_recs) < 5:
        stage1_recs.append("Continuously learn and adapt to new technologies and methodologies")
    while len(stage2_recs) < 5:
        stage2_recs.append("Expand your professional network and industry connections")
    while len(stage3_recs) < 5:
        stage3_recs.append("Stay updated with emerging trends and technologies")
    
    return stage1_recs[:7], stage2_recs[:7], stage3_recs[:7]


def generate_career_path(summary: dict) -> str:
    """Generate a comprehensive career path recommendation based on resume analysis and user preferences."""
    
    # Extract data from summary
    skills = summary.get("skills", [])
    job_titles = summary.get("job_titles", [])
    companies = summary.get("companies", [])
    education = summary.get("education", [])
    projects = summary.get("projects", [])
    certifications = summary.get("certifications", [])
    achievements = summary.get("achievements", [])
    user_preferences = summary.get("user_preferences", {})
    
    # Analyze career track considering user preferences
    career_track, track_description = analyze_skills_for_career_track(skills, user_preferences)
    
    # Analyze skills and tech stack
    skills_analysis = analyze_skills_and_tech_stack(career_track, skills)
    
    # Generate dynamic stage recommendations
    stage1_recs, stage2_recs, stage3_recs = generate_dynamic_stage_recommendations(
        career_track, skills, job_titles, education, user_preferences
    )
    
    # Build the career path response
    response = f"""
# 🎯 Personalized Career Path Recommendation

## 📊 Resume Analysis Summary
- **Skills Identified:** {', '.join(skills[:10])}{'...' if len(skills) > 10 else ''}
- **Experience:** {', '.join(job_titles[:5])}{'...' if len(job_titles) > 5 else ''}
- **Education:** {', '.join(education[:3])}{'...' if len(education) > 3 else ''}
- **Projects:** {', '.join(projects[:3])}{'...' if len(projects) > 3 else ''}
- **Certifications:** {', '.join(certifications[:3])}{'...' if len(certifications) > 3 else ''}
- **Achievements:** {', '.join(achievements[:3])}{'...' if len(achievements) > 3 else ''}

## 🚀 Recommended Career Track: {career_track}
{track_description}

## ⚙️ Your Preferences
- **Area of Interest:** {user_preferences.get('area_of_interest', 'Not specified')}
- **Timeline:** {user_preferences.get('timeline', 'Not specified')}
- **Future Goals:** {', '.join(user_preferences.get('future_goals', ['Not specified']))}
{f"- **Additional Goals:** {user_preferences.get('additional_goals', '')}" if user_preferences.get('additional_goals') else ''}

---

## 🔍 Skills Analysis & Tech Stack

### 📈 Skills Gap Analysis
**Current Skills Gap:** {skills_analysis['skill_gap_percentage']}% of required skills are missing

### ✅ Skills You Already Have
"""
    
    # Add matching skills
    if skills_analysis['matching_skills']:
        for category, skills_list in skills_analysis['matching_skills'].items():
            response += f"\n**{category}:**\n"
            for skill in skills_list:
                response += f"- ✅ {skill}\n"
    else:
        response += "\n*No specific skills from your resume match the required skills for this career track.*\n"
    
    response += f"""

### ❌ Critical Missing Skills
"""
    
    # Add missing skills
    if skills_analysis['missing_skills']:
        for category, skills_list in skills_analysis['missing_skills'].items():
            response += f"\n**{category}:**\n"
            for skill in skills_list:
                response += f"- ❌ {skill}\n"
    else:
        response += "\n*Great! You have all the required skills for this career track.*\n"
    
    response += f"""

### 🛠️ Recommended Tech Stack
"""
    
    # Add tech stack recommendations
    for category, tools in skills_analysis['tech_stack'].items():
        response += f"\n**{category}:**\n"
        for tool in tools:
            response += f"- 🛠️ {tool}\n"
    
    response += f"""

---

## 📈 3-Stage Career Development Plan

### Stage 1: Entry Level (0-2 years)
**Focus:** Building foundational skills and gaining practical experience

"""
    
    for i, rec in enumerate(stage1_recs, 1):
        response += f"{i}. {rec}\n"
    
    response += f"""

### Stage 2: Mid-Level (2-5 years)
**Focus:** Specialization and leadership development

"""
    
    for i, rec in enumerate(stage2_recs, 1):
        response += f"{i}. {rec}\n"
    
    response += f"""

### Stage 3: Senior Level (5+ years)
**Focus:** Strategic leadership and innovation

"""
    
    for i, rec in enumerate(stage3_recs, 1):
        response += f"{i}. {rec}\n"
    
    response += f"""

---

## 💡 Personalized Recommendations

### Immediate Next Steps (Next 3-6 months):
"""
    
    # Personalized immediate steps based on preferences
    if user_preferences.get("timeline") == "Fast-track (aim for rapid advancement)":
        response += """
1. **Accelerated Learning:** Focus intensively on the top 3 missing skills from the analysis above
2. **Project Portfolio:** Build 2-3 impressive projects showcasing your target skills
3. **Networking:** Attend industry events and connect with professionals in your target field
4. **Certification:** Pursue relevant certifications to validate your skills quickly
5. **Mentorship:** Find a mentor who can guide your rapid career progression
"""
    else:
        response += """
1. **Skill Enhancement:** Focus on the top 2-3 missing skills from the skills analysis
2. **Project Building:** Create portfolio projects showcasing your target skills
3. **Networking:** Connect with professionals in your target career track
4. **Certification:** Consider relevant certifications for your chosen path
5. **Mentorship:** Seek guidance from experienced professionals in your field
"""
    
    # Add goal-specific recommendations
    future_goals = user_preferences.get("future_goals", [])
    if "Work for top tech companies (FAANG)" in future_goals:
        if career_track == "Business Consulting":
            response += """
6. **Business Strategy:** Study business models and competitive landscapes
7. **Technology Consulting:** Learn about digital transformation and technology strategy
"""
        else:
            response += """
6. **Interview Preparation:** Start practicing coding interviews and system design
7. **Company Research:** Study the specific technologies and practices used at target companies
"""
    
    if "Start my own company/entrepreneurship" in future_goals:
        response += """
6. **Business Skills:** Learn about business models, market research, and customer development
7. **Idea Validation:** Start validating business ideas and building prototypes
"""
    
    if "Achieve work-life balance" in future_goals:
        response += """
6. **Time Management:** Develop effective scheduling and prioritization techniques
7. **Wellness Practices:** Establish healthy work habits and stress management strategies
"""
    
    response += f"""

### Long-term Strategy (1-3 years):
- Continuously update skills based on industry trends and your specific goals
- Build a strong professional network and personal brand aligned with your aspirations
- Seek opportunities that align with your timeline and career objectives
- Stay updated with emerging technologies and methodologies in your chosen field
- Consider advanced education or specialized training based on your goals
{f"- Focus on {user_preferences.get('area_of_interest', 'your chosen field')} specialization and expertise" if user_preferences.get('area_of_interest') else ""}

---

## 🎯 Goal Alignment

Your career path has been customized based on:
- **Skills Analysis:** {len(skills)} skills identified from your resume
- **Interest Alignment:** {user_preferences.get('area_of_interest', 'General technology')} focus
- **Timeline Preference:** {user_preferences.get('timeline', 'Balanced approach')}
- **Future Aspirations:** {len(future_goals)} specific goals identified
- **Skills Gap:** {skills_analysis['skill_gap_percentage']}% of required skills need development

---

*This career path is tailored specifically to your resume, interests, and goals. Consider your personal circumstances, work-life balance preferences, and market conditions when following these recommendations.*
"""
    
    return response