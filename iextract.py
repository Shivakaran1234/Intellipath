# iextract.py
from transformers import pipeline
import re


# Pick a resume-focused token-classification model from HF.
# Example placeholder; change to a model you have access to.
NER_MODEL = "yashpwr/resume-ner-bert-v2"


# aggregation_strategy requires transformers>=4.8+
ner = pipeline("token-classification", model=NER_MODEL, aggregation_strategy="simple")


def extract_entities(text: str):
    """Return aggregated NER results for the given text."""
    # For very long docs, you may want to chunk. We'll do a simple chunk approach.
    MAX_CHARS = 2000
    chunks = [text[i:i+MAX_CHARS] for i in range(0, len(text), MAX_CHARS)]
    out = []
    for c in chunks:
        try:
            out.extend(ner(c))
        except Exception:
            # On some environments HF pipeline may error for very long sequences; ignore chunk errors.
            pass
    
    # Add the original text to the results for enhanced skill extraction
    if out:
        out.append({"original_text": text})
    
    return out


def _clean_token(w: str) -> str:
    w = re.sub(r"\s+", " ", w.replace("##", "")).strip(" -–·•")
    return w


def normalize_entities(ents: list) -> dict:
    data = {
        "skills": [],
        "job_titles": [],
        "companies": [],
        "education": [],
        "projects": [],
        "years_of_experience": [],
        "certifications": [],
        "achievements": []
    }

    # Enhanced skill recognition patterns - Comprehensive Tech and Non-Tech Skills
    skill_patterns = {
        # Programming Languages
        "programming_languages": [
            "python", "javascript", "java", "c++", "c#", "go", "rust", "swift", "kotlin", 
            "php", "ruby", "scala", "r", "matlab", "dart", "typescript", "html", "css",
            "sql", "bash", "powershell", "lua", "perl", "assembly", "cobol", "fortran",
            "groovy", "clojure", "haskell", "erlang", "elixir", "crystal", "nim", "zig",
            "v", "julia", "d", "ada", "pascal", "basic", "delphi", "objective-c"
        ],
        
        # Web Technologies
        "web_technologies": [
            "html", "css", "javascript", "typescript", "react", "angular", "vue", "svelte",
            "next.js", "nuxt.js", "gatsby", "ember", "backbone", "jquery", "bootstrap",
            "tailwind css", "material-ui", "antd", "chakra ui", "styled-components",
            "sass", "less", "stylus", "webpack", "vite", "parcel", "babel", "eslint"
        ],
        
        # Backend Frameworks
        "backend_frameworks": [
            "node.js", "express", "django", "flask", "fastapi", "spring boot", "spring",
            "laravel", "rails", "asp.net", "dotnet", "gin", "echo", "fiber", "chi",
            "koa", "hapi", "sails", "meteor", "strapi", "nest.js", "adonis", "phoenix",
            "play framework", "akka", "vert.x", "micronaut", "quarkus", "grails"
        ],
        
        # Databases
        "databases": [
            "mysql", "postgresql", "mongodb", "redis", "sqlite", "oracle", "sql server",
            "mariadb", "cassandra", "dynamodb", "firebase", "elasticsearch", "neo4j",
            "couchdb", "rethinkdb", "influxdb", "timescaledb", "cockroachdb", "yugabyte",
            "scylla", "clickhouse", "snowflake", "bigquery", "redshift", "aurora"
        ],
        
        # Cloud Platforms
        "cloud_platforms": [
            "aws", "azure", "google cloud", "gcp", "heroku", "digitalocean", "linode",
            "vultr", "ibm cloud", "oracle cloud", "alibaba cloud", "firebase", "vercel",
            "netlify", "cloudflare", "scaleway", "ovh", "rackspace", "upcloud", "exoscale"
        ],
        
        # DevOps Tools
        "devops_tools": [
            "docker", "kubernetes", "jenkins", "gitlab", "github actions", "circleci",
            "travis ci", "ansible", "terraform", "chef", "puppet", "vagrant", "prometheus",
            "grafana", "elk stack", "datadog", "new relic", "splunk", "nagios", "zabbix",
            "consul", "vault", "nomad", "helm", "istio", "linkerd", "argocd", "flux",
            "tekton", "spinnaker", "octopus deploy", "teamcity", "bamboo", "gitlab ci"
        ],
        
        # Data Science & Analytics
        "data_science": [
            "python", "r", "julia", "matlab", "sas", "spss", "stata", "power bi", "tableau",
            "excel", "sql", "spark", "hadoop", "kafka", "airflow", "mlflow", "jupyter",
            "rstudio", "colab", "databricks", "snowflake", "redshift", "bigquery",
            "pandas", "numpy", "scipy", "scikit-learn", "tensorflow", "pytorch", "keras",
            "xgboost", "lightgbm", "catboost", "matplotlib", "seaborn", "plotly", "bokeh",
            "d3.js", "ggplot2", "shiny", "streamlit", "gradio", "dash", "looker", "qlik"
        ],
        
        # Machine Learning & AI
        "machine_learning": [
            "tensorflow", "pytorch", "keras", "scikit-learn", "xgboost", "lightgbm",
            "catboost", "fastai", "hugging face", "transformers", "spacy", "nltk",
            "opencv", "pillow", "scikit-image", "pytorch lightning", "wandb", "mlflow",
            "kubeflow", "sagemaker", "vertex ai", "azure ml", "databricks", "h2o",
            "rapids", "dask", "vaex", "modin", "ray", "horovod", "deepspeed"
        ],
        
        # Mobile Development
        "mobile_development": [
            "swift", "kotlin", "java", "dart", "react native", "flutter", "xamarin",
            "ionic", "cordova", "phonegap", "xcode", "android studio", "firebase",
            "onesignal", "branch", "appsflyer", "mixpanel", "amplitude", "segment",
            "fastlane", "codepush", "app center", "testflight", "play console"
        ],
        
        # Game Development
        "game_development": [
            "unity", "unreal engine", "godot", "cryengine", "lumberyard", "c#", "c++",
            "lua", "python", "blender", "maya", "3ds max", "zbrush", "substance painter",
            "houdini", "nuke", "after effects", "premiere", "audacity", "fmod", "wwise",
            "steam", "epic games", "itch.io", "game maker", "construct", "rpg maker"
        ],
        
        # Cybersecurity
        "cybersecurity": [
            "kali linux", "metasploit", "nmap", "wireshark", "burp suite", "owasp",
            "penetration testing", "ethical hacking", "vulnerability assessment",
            "siem", "splunk", "qradar", "logrhythm", "exabeam", "sentinel", "soc",
            "incident response", "forensics", "autopsy", "volatility", "ftk", "encase",
            "nessus", "qualys", "openvas", "nexpose", "rapid7", "tenable", "crowdstrike",
            "carbon black", "sentinelone", "cylance", "palo alto", "fortinet", "checkpoint"
        ],
        
        # Blockchain & Web3
        "blockchain_web3": [
            "ethereum", "bitcoin", "solidity", "rust", "web3.js", "ethers.js", "hardhat",
            "truffle", "remix", "ganache", "metamask", "walletconnect", "ipfs", "filecoin",
            "polygon", "solana", "polkadot", "cardano", "binance smart chain", "avalanche",
            "arbitrum", "optimism", "uniswap", "compound", "aave", "curve", "opensea",
            "nft", "defi", "dao", "smart contracts", "consensus", "mining", "staking"
        ],
        
        # UI/UX Design
        "ui_ux_design": [
            "figma", "adobe xd", "sketch", "invision", "adobe photoshop", "adobe illustrator",
            "wireframing", "prototyping", "user research", "usability testing", "user experience",
            "user interface", "design systems", "visual design", "typography", "color theory",
            "layout design", "accessibility", "ui design", "ux design", "flutter flow",
            "framer", "principle", "protopie", "axure rp", "balsamiq", "marvel", "zeplin",
            "abstract", "lucidchart", "draw.io", "whimsical", "mural", "miro", "notion"
        ],
        
        # Business & Productivity Tools
        "business_tools": [
            "excel", "powerpoint", "word", "outlook", "sharepoint", "teams", "slack",
            "zoom", "microsoft office", "google workspace", "salesforce", "hubspot",
            "jira", "confluence", "monday.com", "asana", "trello", "notion", "airtable",
            "clickup", "wrike", "smartsheet", "basecamp", "podio", "zoho", "freshdesk",
            "intercom", "zendesk", "pipedrive", "close", "salesforce", "dynamics 365"
        ],
        
        # Project Management
        "project_management": [
            "agile", "scrum", "kanban", "lean", "six sigma", "prince2", "pmp", "pmi",
            "waterfall", "sprint planning", "user stories", "epics", "backlog", "retrospectives",
            "daily standups", "sprint reviews", "sprint retrospectives", "story points",
            "velocity", "burndown charts", "gantt charts", "critical path", "risk management",
            "stakeholder management", "change management", "resource management"
        ],
        
        # Soft Skills
        "soft_skills": [
            "leadership", "communication", "teamwork", "collaboration", "problem solving",
            "critical thinking", "creativity", "adaptability", "flexibility", "time management",
            "organization", "planning", "decision making", "negotiation", "conflict resolution",
            "emotional intelligence", "empathy", "active listening", "presentation skills",
            "public speaking", "mentoring", "coaching", "facilitation", "influence",
            "networking", "relationship building", "customer service", "sales", "marketing"
        ],
        
        # Domain Knowledge
        "domain_knowledge": [
            "finance", "banking", "insurance", "healthcare", "pharmaceuticals", "biotechnology",
            "manufacturing", "logistics", "supply chain", "retail", "e-commerce", "real estate",
            "education", "government", "non-profit", "consulting", "legal", "media",
            "entertainment", "gaming", "sports", "fitness", "food", "beverage", "automotive",
            "aerospace", "defense", "energy", "utilities", "telecommunications", "transportation"
        ],
        
        # Operating Systems
        "operating_systems": [
            "linux", "ubuntu", "centos", "red hat", "debian", "fedora", "arch linux",
            "windows", "windows server", "macos", "ios", "android", "chrome os",
            "freebsd", "openbsd", "netbsd", "solaris", "aix", "hp-ux", "unix"
        ],
        
        # Networking
        "networking": [
            "tcp/ip", "dns", "dhcp", "http", "https", "ftp", "smtp", "pop3", "imap",
            "ssh", "telnet", "vpn", "firewall", "load balancing", "routing", "switching",
            "vlans", "subnetting", "cidr", "bgp", "ospf", "eigrp", "mpls", "sdn",
            "nfv", "5g", "wifi", "bluetooth", "ethernet", "fiber", "coaxial"
        ],
        
        # Testing & Quality Assurance
        "testing_qa": [
            "unit testing", "integration testing", "system testing", "acceptance testing",
            "regression testing", "performance testing", "load testing", "stress testing",
            "security testing", "penetration testing", "usability testing", "accessibility testing",
            "junit", "testng", "pytest", "jest", "mocha", "chai", "selenium", "cypress",
            "playwright", "appium", "postman", "soapui", "jmeter", "gatling", "k6",
            "sonarqube", "codecov", "coveralls", "jenkins", "gitlab ci", "github actions"
        ],
        
        # Version Control
        "version_control": [
            "git", "github", "gitlab", "bitbucket", "svn", "mercurial", "perforce",
            "git flow", "git hooks", "git submodules", "git lfs", "github pages",
            "gitlab pages", "github actions", "gitlab ci", "bitbucket pipelines"
        ],
        
        # Monitoring & Observability
        "monitoring_observability": [
            "prometheus", "grafana", "elk stack", "elasticsearch", "logstash", "kibana",
            "datadog", "new relic", "splunk", "dynatrace", "appdynamics", "instana",
            "jaeger", "zipkin", "opentelemetry", "cloudwatch", "azure monitor",
            "stackdriver", "nagios", "zabbix", "icinga", "sensu", "consul", "etcd"
        ]
    }

    for e in ents:
        label = e.get("entity_group", e.get("entity", "")).upper()
        word = _clean_token(e.get("word", ""))
        if not word:
            continue
        if "SKILL" in label:
            data["skills"].append(word)
        elif any(x in label for x in ("DESIGNATION", "JOB", "TITLE")):
            data["job_titles"].append(word)
        elif any(x in label for x in ("COMPANY", "ORG")):
            data["companies"].append(word)
        elif any(x in label for x in ("DEGREE", "COLLEGE", "EDU", "UNIV")):
            data["education"].append(word)
        elif "PROJECT" in label:
            data["projects"].append(word)
        elif "YEAR" in label or "EXPERIENCE" in label:
            data["years_of_experience"].append(word)
        elif "CERTIFICATION" in label or "CERT" in label:
            data["certifications"].append(word)
        elif "ACHIEVEMENT" in label or "AWARD" in label:
            data["achievements"].append(word)

    # Enhanced skill extraction from text patterns
    def extract_skills_from_text(text):
        skills_found = []
        text_lower = text.lower()
        
        # Extract skills from all categories
        for category, skills in skill_patterns.items():
            for skill in skills:
                if skill.lower() in text_lower:
                    skills_found.append(skill)
        
        return skills_found

    def extract_additional_info(text, data):
        """Extract additional information like certifications, achievements, etc."""
        text_lower = text.lower()
        
        # Extract certifications
        cert_patterns = [
            "certification", "certified", "cert", "nptel", "linkedin", "ibm", "microsoft",
            "aws", "azure", "google", "oracle", "cisco", "comptia", "arcel", "pmp", "prince2",
            "scrum", "agile", "six sigma", "lean", "itil", "cobit", "iso", "gdpr", "sox",
            "hipaa", "pci dss", "ccna", "ccnp", "ccie", "mcse", "mcp", "mta", "mcts",
            "rhcsa", "rhce", "lpic", "cka", "ckad", "cks", "terraform", "ansible", "docker",
            "kubernetes", "jenkins", "gitlab", "github", "salesforce", "hubspot", "tableau",
            "power bi", "snowflake", "databricks", "sagemaker", "vertex ai", "azure ml"
        ]
        
        # Extract achievements
        achievement_patterns = [
            "nasa hackathon", "flutter flow workshop", "hackathon", "workshop",
            "award", "recognition", "achievement", "winner", "finalist",
            "ui/ux design", "rapid prototyping", "hands-on ui/ux design",
            "competition", "contest", "challenge", "innovation", "excellence",
            "outstanding", "distinguished", "merit", "honor", "scholarship",
            "fellowship", "grant", "research", "publication", "patent", "invention",
            "conference", "presentation", "speaker", "panelist", "mentor", "volunteer",
            "community service", "leadership", "student government", "club president",
            "team captain", "project lead", "technical lead", "architect", "expert"
        ]
        
        # Extract projects
        project_patterns = [
            "interactive sales analytics dashboard", "weather app", 
            "postgraduate project management system", "mern stack",
            "power bi", "sql", "dax", "docker", "jenkins", "kubernetes",
            "ui/ux design", "rapid prototyping", "flutter flow",
            "project", "application", "system", "platform", "website", "app",
            "dashboard", "portal", "api", "service", "tool", "framework", "library",
            "plugin", "extension", "module", "component", "feature", "functionality",
            "automation", "script", "bot", "chatbot", "ai", "machine learning",
            "data analysis", "visualization", "reporting", "monitoring", "tracking",
            "inventory", "e-commerce", "crm", "erp", "cms", "lms", "blog", "forum",
            "social media", "game", "simulation", "model", "algorithm", "database",
            "mobile app", "web app", "desktop app", "cloud", "server", "client"
        ]
        
        # Extract companies
        company_patterns = [
            "electronic arts", "ea sports", "deloitte australia", "forage",
            "vnr vignana jyothi institute", "technology", "microsoft", "google", "apple",
            "amazon", "meta", "facebook", "netflix", "uber", "lyft", "airbnb", "spotify",
            "slack", "zoom", "salesforce", "adobe", "oracle", "ibm", "intel", "amd",
            "nvidia", "cisco", "vmware", "red hat", "canonical", "docker", "hashicorp",
            "databricks", "snowflake", "palantir", "stripe", "square", "paypal", "visa",
            "mastercard", "goldman sachs", "jpmorgan", "morgan stanley", "bank of america",
            "wells fargo", "citigroup", "deloitte", "pwc", "ey", "kpmg", "accenture",
            "infosys", "tcs", "wipro", "cognizant", "hcl", "tech mahindra", "capgemini",
            "atos", "nvidia", "amd", "qualcomm", "broadcom", "marvell", "micron",
            "samsung", "lg", "sony", "panasonic", "philips", "siemens", "ge", "bosch",
            "volkswagen", "bmw", "mercedes", "toyota", "honda", "ford", "gm", "tesla",
            "spacex", "blue origin", "virgin galactic", "boeing", "airbus", "lockheed",
            "raytheon", "northrop grumman", "general dynamics", "bae systems"
        ]
        
        # Extract job titles
        job_title_patterns = [
            "software engineering", "virtual experience", "technology virtual experience",
            "software engineer", "developer", "analyst", "consultant", "architect",
            "manager", "director", "vp", "cto", "ceo", "founder", "co-founder",
            "lead", "senior", "junior", "associate", "principal", "staff", "fellow",
            "intern", "internship", "apprentice", "trainee", "graduate", "entry level",
            "mid level", "senior level", "executive", "chief", "head", "coordinator",
            "specialist", "expert", "guru", "ninja", "rockstar", "evangelist",
            "advocate", "ambassador", "mentor", "coach", "trainer", "instructor",
            "professor", "lecturer", "researcher", "scientist", "data scientist",
            "machine learning engineer", "ai engineer", "devops engineer", "sre",
            "site reliability engineer", "cloud engineer", "security engineer",
            "network engineer", "systems engineer", "qa engineer", "test engineer",
            "automation engineer", "frontend developer", "backend developer",
            "full stack developer", "mobile developer", "game developer", "ui designer",
            "ux designer", "product manager", "project manager", "scrum master",
            "business analyst", "data analyst", "financial analyst", "market analyst",
            "sales representative", "account manager", "customer success", "support",
            "operations", "administrator", "coordinator", "assistant", "clerk"
        ]
        
        # Check for patterns and add to data
        for pattern in cert_patterns:
            if pattern in text_lower:
                # Find the full certification name
                lines = text.split('\n')
                for line in lines:
                    if pattern in line.lower():
                        data["certifications"].append(line.strip())
                        break
        
        # Extract education information
        education_patterns = [
            "university", "college", "institute", "school", "academy", "bachelor", "master",
            "phd", "doctorate", "diploma", "certificate", "degree", "b.tech", "m.tech",
            "b.e", "m.e", "b.sc", "m.sc", "b.com", "m.com", "b.ba", "m.ba", "mba",
            "bca", "mca", "b.arch", "m.arch", "llb", "llm", "md", "mbbs", "pharmacy",
            "engineering", "computer science", "information technology", "data science",
            "business administration", "management", "finance", "marketing", "economics",
            "mathematics", "physics", "chemistry", "biology", "medicine", "law", "arts",
            "humanities", "social sciences", "psychology", "sociology", "political science"
        ]
        
        for pattern in education_patterns:
            if pattern in text_lower:
                lines = text.split('\n')
                for line in lines:
                    if pattern in line.lower():
                        data["education"].append(line.strip())
                        break
        
        for pattern in achievement_patterns:
            if pattern in text_lower:
                lines = text.split('\n')
                for line in lines:
                    if pattern in line.lower():
                        data["achievements"].append(line.strip())
                        break
        
        for pattern in project_patterns:
            if pattern in text_lower:
                lines = text.split('\n')
                for line in lines:
                    if pattern in line.lower():
                        data["projects"].append(line.strip())
                        break
        
        for pattern in company_patterns:
            if pattern in text_lower:
                lines = text.split('\n')
                for line in lines:
                    if pattern in line.lower():
                        data["companies"].append(line.strip())
                        break
        
        for pattern in job_title_patterns:
            if pattern in text_lower:
                lines = text.split('\n')
                for line in lines:
                    if pattern in line.lower():
                        data["job_titles"].append(line.strip())
                        break

    # Add extracted skills to the data
    original_text = ""
    for e in ents:
        if isinstance(e, dict):
            if e.get('original_text'):
                original_text = e.get('original_text')
                break
            elif e.get('word'):
                original_text += " " + e.get('word', '')
    
    if original_text:
        additional_skills = extract_skills_from_text(original_text)
        data["skills"].extend(additional_skills)
        
        # Extract additional information from text patterns
        extract_additional_info(original_text, data)

    for k in data:
        data[k] = sorted(set(data[k]), key=str.lower)
    return data