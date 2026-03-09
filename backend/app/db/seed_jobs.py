"""
Database seeder: populates the jobs table with 50+ real-world job listings.
Run via POST /api/jobs/seed or directly: python -m app.db.seed_jobs

Covers categories: Software Engineering, Data Science, DevOps, Product, Design, Finance, Marketing
"""
from typing import List, Dict, Any

# 50+ job listings across diverse roles and industries
SEED_JOBS: List[Dict[str, Any]] = [
    # ─── Software Engineering ───────────────────────────────────────────────
    {
        "title": "Senior Full Stack Developer",
        "company": "TechNova Inc.",
        "location": "San Francisco, CA (Remote OK)",
        "job_type": "Full-time",
        "experience_level": "Senior",
        "category": "Engineering",
        "salary_range": "$140,000 - $180,000",
        "description": """We are seeking a Senior Full Stack Developer to build scalable web applications.
You will work across the entire stack, from database design to frontend UI.
Our team uses modern technologies including React, Node.js, and PostgreSQL.
You'll lead technical decisions, mentor junior developers, and ship high-quality features.
We value clean code, test coverage, and continuous deployment practices.""",
        "required_skills": ["React", "Node.js", "TypeScript", "PostgreSQL", "REST APIs", "Git"],
        "preferred_skills": ["GraphQL", "Redis", "Docker", "AWS", "CI/CD"],
    },
    {
        "title": "Backend Engineer (Python)",
        "company": "DataStream Corp",
        "location": "Remote",
        "job_type": "Full-time",
        "experience_level": "Mid-level",
        "category": "Engineering",
        "salary_range": "$110,000 - $140,000",
        "description": """Join our backend team to build high-performance APIs and data pipelines.
You'll work with Python, FastAPI, and PostgreSQL to power our data platform.
Experience with async programming, microservices, and cloud deployment is valued.
We process millions of records daily and need engineers who care about performance.""",
        "required_skills": ["Python", "FastAPI", "PostgreSQL", "REST APIs", "Docker"],
        "preferred_skills": ["Celery", "Redis", "Kafka", "AWS Lambda", "asyncio"],
    },
    {
        "title": "MERN Stack Developer",
        "company": "StartupXYZ",
        "location": "Austin, TX",
        "job_type": "Full-time",
        "experience_level": "Mid-level",
        "category": "Engineering",
        "salary_range": "$90,000 - $120,000",
        "description": """Build and maintain our consumer-facing web application using the MERN stack.
You'll develop new features, fix bugs, and improve performance across MongoDB, Express, React, and Node.js.
We're a fast-growing startup where engineers wear many hats and ship fast.
Strong JavaScript skills and experience with REST APIs are essential.""",
        "required_skills": ["MongoDB", "Express.js", "React", "Node.js", "JavaScript", "REST APIs"],
        "preferred_skills": ["Redux", "Socket.io", "JWT", "Docker", "Agile"],
    },
    {
        "title": "iOS Developer",
        "company": "MobileFirst Labs",
        "location": "New York, NY",
        "job_type": "Full-time",
        "experience_level": "Mid-level",
        "category": "Engineering",
        "salary_range": "$120,000 - $155,000",
        "description": """Design and build advanced applications for the iOS platform.
You'll own the full development cycle from concept to App Store submission.
Work closely with product and design teams to deliver exceptional user experiences.
Our app has 1M+ daily active users and we hold a high bar for performance.""",
        "required_skills": ["Swift", "Xcode", "iOS SDK", "UIKit", "Core Data"],
        "preferred_skills": ["SwiftUI", "Combine", "Unit Testing", "CI/CD", "Firebase"],
    },
    {
        "title": "Android Developer",
        "company": "Appify Solutions",
        "location": "Seattle, WA (Remote OK)",
        "job_type": "Full-time",
        "experience_level": "Mid-level",
        "category": "Engineering",
        "salary_range": "$115,000 - $150,000",
        "description": """Develop and maintain Android applications for millions of users.
You'll use Kotlin and modern Android architecture (MVVM, Jetpack Compose).
Experience with Retrofit, Room database, and Coroutines is required.
You'll collaborate with backend engineers to integrate APIs and improve performance.""",
        "required_skills": ["Kotlin", "Android SDK", "Jetpack Compose", "Room", "Retrofit"],
        "preferred_skills": ["Coroutines", "Hilt", "Firebase", "Unit Testing", "CI/CD"],
    },
    {
        "title": "Software Engineer – Java",
        "company": "EnterpriseGlobal",
        "location": "Chicago, IL",
        "job_type": "Full-time",
        "experience_level": "Mid-level",
        "category": "Engineering",
        "salary_range": "$100,000 - $130,000",
        "description": """Build enterprise-grade backend services using Java and Spring Boot.
You'll work on microservices architecture, REST APIs, and database integration.
Experience with Maven/Gradle build tools and JUnit testing is required.
Knowledge of messaging systems (Kafka, RabbitMQ) is a strong plus.""",
        "required_skills": ["Java", "Spring Boot", "REST APIs", "SQL", "Maven", "JUnit"],
        "preferred_skills": ["Kafka", "Docker", "Kubernetes", "AWS", "Microservices"],
    },
    {
        "title": "DevOps Engineer",
        "company": "CloudOps Co.",
        "location": "Remote",
        "job_type": "Full-time",
        "experience_level": "Senior",
        "category": "DevOps",
        "salary_range": "$130,000 - $165,000",
        "description": """Own and evolve our cloud infrastructure on AWS.
You'll manage CI/CD pipelines, containerized workloads, and infrastructure-as-code.
Strong Terraform, Kubernetes, and Docker skills are essential.
You'll drive reliability improvements, reduce deployment time, and automate operations.""",
        "required_skills": ["AWS", "Terraform", "Kubernetes", "Docker", "CI/CD", "Linux"],
        "preferred_skills": ["Helm", "ArgoCD", "Prometheus", "Grafana", "Python scripting"],
    },
    {
        "title": "Cloud Infrastructure Engineer",
        "company": "ScaleUp Technologies",
        "location": "Remote",
        "job_type": "Full-time",
        "experience_level": "Senior",
        "category": "DevOps",
        "salary_range": "$135,000 - $170,000",
        "description": """Design and manage multi-cloud infrastructure across AWS and GCP.
Automate deployments with Terraform and Ansible. Monitor with Datadog.
Experience with cost optimization, security best practices, and SRE principles is valued.
You'll partner with development teams to ensure reliable, scalable deployments.""",
        "required_skills": ["AWS", "GCP", "Terraform", "Ansible", "Docker", "Kubernetes"],
        "preferred_skills": ["Datadog", "SRE", "Python", "Helm", "Cost Optimization"],
    },
    {
        "title": "Site Reliability Engineer (SRE)",
        "company": "HighTraffic Inc.",
        "location": "San Francisco, CA",
        "job_type": "Full-time",
        "experience_level": "Senior",
        "category": "DevOps",
        "salary_range": "$145,000 - $185,000",
        "description": """Ensure our platform runs at 99.99% uptime serving 10M+ users.
You'll define SLOs/SLIs, build observability systems, and reduce MTTR.
Strong background in distributed systems, alerting, and on-call practices.
Experience automating incident response with Python/Bash is essential.""",
        "required_skills": ["Linux", "Python", "Kubernetes", "Prometheus", "Grafana", "SLO/SLI"],
        "preferred_skills": ["Chaos Engineering", "Go", "Terraform", "PagerDuty", "AWS"],
    },
    # ─── Data Science / ML ──────────────────────────────────────────────────
    {
        "title": "Data Scientist",
        "company": "InsightAI Labs",
        "location": "Boston, MA (Hybrid)",
        "job_type": "Full-time",
        "experience_level": "Mid-level",
        "category": "Data Science",
        "salary_range": "$110,000 - $145,000",
        "description": """Use data to drive business decisions and build predictive models.
You'll work with large datasets, perform statistical analysis, and deploy ML models.
Strong Python skills (pandas, scikit-learn, numpy) and SQL experience are required.
Experience with A/B testing and experiment design is a strong plus.""",
        "required_skills": ["Python", "pandas", "scikit-learn", "SQL", "Statistics", "Machine Learning"],
        "preferred_skills": ["TensorFlow", "PySpark", "Tableau", "A/B Testing", "R"],
    },
    {
        "title": "Machine Learning Engineer",
        "company": "AIVentures",
        "location": "Remote",
        "job_type": "Full-time",
        "experience_level": "Senior",
        "category": "Data Science",
        "salary_range": "$140,000 - $180,000",
        "description": """Build and deploy production ML systems at scale.
You'll design training pipelines, optimize model performance, and monitor production models.
Experience with deep learning frameworks (PyTorch/TensorFlow) and MLOps is required.
You'll work on NLP, computer vision, and recommendation systems.""",
        "required_skills": ["Python", "PyTorch", "TensorFlow", "MLOps", "Docker", "SQL"],
        "preferred_skills": ["Kubernetes", "MLflow", "Feature Stores", "AWS SageMaker", "Spark"],
    },
    {
        "title": "Data Analyst",
        "company": "RetailMax",
        "location": "Denver, CO",
        "job_type": "Full-time",
        "experience_level": "Entry",
        "category": "Data Science",
        "salary_range": "$65,000 - $85,000",
        "description": """Analyze business data to identify trends and support decision-making.
Create dashboards and reports using SQL and BI tools (Tableau, Looker).
Collaborate with business stakeholders to define metrics and KPIs.
Strong analytical mindset and attention to detail are essential.""",
        "required_skills": ["SQL", "Excel", "Tableau", "Data Analysis", "Python"],
        "preferred_skills": ["Looker", "dbt", "Google Analytics", "Statistics", "Power BI"],
    },
    {
        "title": "NLP Engineer",
        "company": "LinguaTech",
        "location": "Remote",
        "job_type": "Full-time",
        "experience_level": "Senior",
        "category": "Data Science",
        "salary_range": "$145,000 - $185,000",
        "description": """Design and build NLP systems for text understanding and generation.
Work on LLM fine-tuning, prompt engineering, and RAG pipelines.
Experience with Hugging Face transformers and vector databases is required.
You'll ship production NLP features used by thousands of customers.""",
        "required_skills": ["Python", "Transformers", "PyTorch", "NLP", "Hugging Face", "LLMs"],
        "preferred_skills": ["LangChain", "Vector Databases", "RAG", "Fine-tuning", "RLHF"],
    },
    {
        "title": "Business Intelligence Developer",
        "company": "FinanceFirst",
        "location": "New York, NY (Hybrid)",
        "job_type": "Full-time",
        "experience_level": "Mid-level",
        "category": "Data Science",
        "salary_range": "$90,000 - $115,000",
        "description": """Build self-service analytics solutions for business teams.
Design and maintain data models, ETL pipelines, and BI dashboards.
Strong SQL and data warehouse experience (Snowflake, BigQuery) is required.
You'll bridge the gap between data engineering and business users.""",
        "required_skills": ["SQL", "Tableau", "Power BI", "Snowflake", "dbt", "Data Modeling"],
        "preferred_skills": ["Python", "Looker", "BigQuery", "ETL", "Airflow"],
    },
    # ─── Product Management ──────────────────────────────────────────────────
    {
        "title": "Senior Product Manager",
        "company": "ProductLab",
        "location": "San Francisco, CA",
        "job_type": "Full-time",
        "experience_level": "Senior",
        "category": "Product",
        "salary_range": "$155,000 - $200,000",
        "description": """Lead product strategy and execution for our core platform product.
Define the roadmap, write PRDs, and align cross-functional teams (engineering, design, marketing).
You'll use data to make decisions and run experiments to validate hypotheses.
3+ years PM experience at a tech company required; B2B SaaS experience preferred.""",
        "required_skills": ["Product Strategy", "Roadmapping", "PRDs", "Data Analysis", "Agile", "Stakeholder Management"],
        "preferred_skills": ["SQL", "A/B Testing", "User Research", "Jira", "OKRs"],
    },
    {
        "title": "Product Manager – Mobile",
        "company": "AppGrowth Inc.",
        "location": "Remote",
        "job_type": "Full-time",
        "experience_level": "Mid-level",
        "category": "Product",
        "salary_range": "$120,000 - $155,000",
        "description": """Own the mobile product roadmap for iOS and Android apps.
Work closely with engineering, design, and marketing to ship impactful features.
Strong understanding of mobile metrics (DAU, retention, funnel) is required.
Experience with app store optimization and mobile growth is a plus.""",
        "required_skills": ["Product Management", "Mobile Apps", "Agile", "Metrics", "User Stories"],
        "preferred_skills": ["iOS", "Android", "A/B Testing", "Amplitude", "SQL"],
    },
    {
        "title": "Technical Product Manager",
        "company": "APILayer",
        "location": "Remote",
        "job_type": "Full-time",
        "experience_level": "Senior",
        "category": "Product",
        "salary_range": "$140,000 - $175,000",
        "description": """Lead product development for our developer-facing API platform.
Write detailed technical specs, work directly with engineering, and represent developer needs.
Prior software engineering experience or strong technical background is required.
You'll manage the full lifecycle of API products from conception to GA.""",
        "required_skills": ["Technical Product Management", "API Design", "REST APIs", "Agile", "PRDs"],
        "preferred_skills": ["Developer Experience", "OpenAPI", "SQL", "System Design", "Jira"],
    },
    # ─── Design ──────────────────────────────────────────────────────────────
    {
        "title": "Senior UX Designer",
        "company": "DesignHub",
        "location": "New York, NY (Hybrid)",
        "job_type": "Full-time",
        "experience_level": "Senior",
        "category": "Design",
        "salary_range": "$120,000 - $155,000",
        "description": """Design intuitive user experiences for our enterprise SaaS platform.
Conduct user research, create wireframes, prototypes, and high-fidelity mockups.
Collaborate with product managers and engineers to bring designs to life.
Strong portfolio demonstrating complex UX problem-solving is required.""",
        "required_skills": ["Figma", "User Research", "Wireframing", "Prototyping", "Usability Testing"],
        "preferred_skills": ["Design Systems", "Motion Design", "HTML/CSS", "Accessibility", "Sketch"],
    },
    {
        "title": "UI/UX Designer",
        "company": "CreativeTech",
        "location": "Remote",
        "job_type": "Full-time",
        "experience_level": "Mid-level",
        "category": "Design",
        "salary_range": "$80,000 - $110,000",
        "description": """Create beautiful, user-centered designs for web and mobile applications.
Build and maintain a comprehensive design system. Produce pixel-perfect UI specifications.
You'll work in an agile team, iterating quickly based on user feedback and analytics.
Strong visual design skills and proficiency with Figma are essential.""",
        "required_skills": ["Figma", "UI Design", "UX Design", "Design Systems", "Prototyping"],
        "preferred_skills": ["Adobe XD", "Illustrator", "User Research", "CSS", "Animation"],
    },
    {
        "title": "Product Designer",
        "company": "FinanceApp Co.",
        "location": "San Francisco, CA",
        "job_type": "Full-time",
        "experience_level": "Mid-level",
        "category": "Design",
        "salary_range": "$110,000 - $140,000",
        "description": """End-to-end product design for our personal finance application.
Own design from research to final handoff: user interviews, information architecture, UI design.
Work in a collaborative environment with product and engineering teams.
Experience designing for mobile-first products is a strong plus.""",
        "required_skills": ["Figma", "Product Design", "User Research", "Mobile Design", "Prototyping"],
        "preferred_skills": ["iOS Design Guidelines", "Material Design", "Framer", "HTML/CSS"],
    },
    # ─── Cybersecurity ────────────────────────────────────────────────────────
    {
        "title": "Cybersecurity Engineer",
        "company": "SecureNet Corp",
        "location": "Washington, DC",
        "job_type": "Full-time",
        "experience_level": "Mid-level",
        "category": "Security",
        "salary_range": "$115,000 - $150,000",
        "description": """Protect company assets through security assessments, penetration testing, and incident response.
Implement security controls, monitor threats, and respond to incidents.
Experience with SIEM tools, vulnerability scanning, and network security is required.
CISSP, CEH, or equivalent certifications are preferred.""",
        "required_skills": ["Penetration Testing", "Network Security", "SIEM", "Incident Response", "Vulnerability Assessment"],
        "preferred_skills": ["CISSP", "CEH", "Python", "AWS Security", "Zero Trust"],
    },
    {
        "title": "Application Security Engineer",
        "company": "AppSec Labs",
        "location": "Remote",
        "job_type": "Full-time",
        "experience_level": "Senior",
        "category": "Security",
        "salary_range": "$140,000 - $175,000",
        "description": """Embed security into the software development lifecycle.
Perform code reviews, threat modeling, and penetration testing of web applications.
Champion DevSecOps practices and train developers on secure coding.
Experience with OWASP Top 10, SAST/DAST tools, and bug bounty programs is valued.""",
        "required_skills": ["Application Security", "OWASP", "Python", "Code Review", "SAST/DAST"],
        "preferred_skills": ["Burp Suite", "DevSecOps", "AWS Security", "Threat Modeling", "Bug Bounty"],
    },
    # ─── Finance / Accounting ─────────────────────────────────────────────────
    {
        "title": "Financial Analyst",
        "company": "InvestGroup",
        "location": "New York, NY",
        "job_type": "Full-time",
        "experience_level": "Entry",
        "category": "Finance",
        "salary_range": "$70,000 - $90,000",
        "description": """Analyze financial data to support investment decisions and business planning.
Build financial models, prepare reports, and track KPIs.
Strong Excel skills and knowledge of accounting principles required.
CFA Level 1 or progress toward CFA is a plus.""",
        "required_skills": ["Financial Modeling", "Excel", "Financial Analysis", "Accounting", "SQL"],
        "preferred_skills": ["CFA", "Python", "Tableau", "Bloomberg Terminal", "Valuation"],
    },
    {
        "title": "Quantitative Analyst",
        "company": "QuantFund",
        "location": "New York, NY",
        "job_type": "Full-time",
        "experience_level": "Senior",
        "category": "Finance",
        "salary_range": "$180,000 - $250,000",
        "description": """Develop and implement quantitative models for trading and risk management.
Strong mathematics, statistics, and programming background required.
Experience with time series analysis, factor models, and portfolio optimization.
PhD in Mathematics, Statistics, Physics, or Computer Science preferred.""",
        "required_skills": ["Python", "R", "Statistics", "Financial Modeling", "Machine Learning", "SQL"],
        "preferred_skills": ["C++", "MATLAB", "Risk Management", "Derivatives", "Monte Carlo"],
    },
    # ─── Marketing ────────────────────────────────────────────────────────────
    {
        "title": "Digital Marketing Manager",
        "company": "GrowthCo",
        "location": "Remote",
        "job_type": "Full-time",
        "experience_level": "Mid-level",
        "category": "Marketing",
        "salary_range": "$75,000 - $100,000",
        "description": """Lead digital marketing campaigns across SEO, SEM, social media, and email.
Manage performance marketing budget, optimize for CAC and ROAS.
Analyze campaign performance and report to leadership.
Experience with marketing automation tools (HubSpot, Marketo) is required.""",
        "required_skills": ["Digital Marketing", "SEO", "SEM", "Google Ads", "Email Marketing", "Analytics"],
        "preferred_skills": ["HubSpot", "Marketo", "Content Marketing", "Social Media", "A/B Testing"],
    },
    {
        "title": "Growth Marketing Engineer",
        "company": "SaaS Startup",
        "location": "Remote",
        "job_type": "Full-time",
        "experience_level": "Mid-level",
        "category": "Marketing",
        "salary_range": "$100,000 - $130,000",
        "description": """Bridge marketing and engineering to drive user acquisition and activation.
Build growth experiments, implement tracking, and optimize conversion funnels.
Strong technical background with SQL, Python, and experience with data pipelines.
You'll own the full growth tech stack and experiment velocity.""",
        "required_skills": ["Python", "SQL", "Google Analytics", "A/B Testing", "Growth Hacking"],
        "preferred_skills": ["Segment", "Amplitude", "Braze", "dbt", "Marketing Automation"],
    },
    # ─── More Engineering Roles ──────────────────────────────────────────────
    {
        "title": "Frontend Developer – React",
        "company": "WebCraft Agency",
        "location": "Remote",
        "job_type": "Full-time",
        "experience_level": "Mid-level",
        "category": "Engineering",
        "salary_range": "$85,000 - $115,000",
        "description": """Build responsive, accessible web interfaces using React and TypeScript.
Work with designers to implement pixel-perfect UIs and smooth interactions.
Experience with state management (Redux, Zustand), testing (Jest, RTL), and performance optimization.
Contributions to open-source or a strong portfolio are valued.""",
        "required_skills": ["React", "TypeScript", "JavaScript", "CSS", "HTML", "REST APIs"],
        "preferred_skills": ["Redux", "Tailwind CSS", "Jest", "Webpack", "Accessibility"],
    },
    {
        "title": "Golang Backend Engineer",
        "company": "HighPerf Systems",
        "location": "Remote",
        "job_type": "Full-time",
        "experience_level": "Senior",
        "category": "Engineering",
        "salary_range": "$140,000 - $175,000",
        "description": """Build high-performance distributed systems using Go.
Design and implement gRPC services, message queues, and caching layers.
Experience with concurrency patterns, profiling, and performance tuning in Go.
You'll work on systems handling millions of requests per second.""",
        "required_skills": ["Go", "gRPC", "PostgreSQL", "Redis", "Docker", "Microservices"],
        "preferred_skills": ["Kubernetes", "Kafka", "Prometheus", "AWS", "Protocol Buffers"],
    },
    {
        "title": "Rust Systems Engineer",
        "company": "SystemsCraft",
        "location": "Remote",
        "job_type": "Full-time",
        "experience_level": "Senior",
        "category": "Engineering",
        "salary_range": "$155,000 - $195,000",
        "description": """Build low-level systems software in Rust for memory-safe, high-performance applications.
Work on networking, storage systems, or WebAssembly runtimes.
Deep understanding of systems programming, memory management, and concurrency.
Open source contributions in Rust are a significant plus.""",
        "required_skills": ["Rust", "Systems Programming", "Linux", "Concurrency", "Performance Optimization"],
        "preferred_skills": ["WebAssembly", "Networking", "C/C++", "LLVM", "Open Source"],
    },
    {
        "title": "Embedded Systems Engineer",
        "company": "HardwareTech",
        "location": "Austin, TX",
        "job_type": "Full-time",
        "experience_level": "Mid-level",
        "category": "Engineering",
        "salary_range": "$105,000 - $135,000",
        "description": """Develop firmware for embedded devices in C/C++.
Design drivers, optimize for real-time constraints, and debug hardware issues.
Experience with RTOS, ARM Cortex microcontrollers, and communication protocols (I2C, SPI, UART).
A background in electrical engineering or strong knowledge of electronics is preferred.""",
        "required_skills": ["C", "C++", "Embedded Systems", "RTOS", "ARM Cortex", "Firmware"],
        "preferred_skills": ["FreeRTOS", "Zephyr", "I2C", "SPI", "Python scripting"],
    },
    {
        "title": "Blockchain Developer",
        "company": "Web3 Labs",
        "location": "Remote",
        "job_type": "Full-time",
        "experience_level": "Mid-level",
        "category": "Engineering",
        "salary_range": "$120,000 - $165,000",
        "description": """Develop smart contracts and DeFi protocols on Ethereum and EVM-compatible chains.
Write, test, and audit Solidity contracts. Build integrations with frontends using ethers.js.
Experience with DeFi protocols, ERC standards, and security auditing is valuable.
A deep understanding of blockchain fundamentals and cryptography is required.""",
        "required_skills": ["Solidity", "Ethereum", "Smart Contracts", "JavaScript", "ethers.js"],
        "preferred_skills": ["Hardhat", "Foundry", "DeFi", "Layer 2", "Security Auditing"],
    },
    {
        "title": "QA Engineer / SDET",
        "company": "QualityFirst",
        "location": "Remote",
        "job_type": "Full-time",
        "experience_level": "Mid-level",
        "category": "Engineering",
        "salary_range": "$85,000 - $110,000",
        "description": """Design and implement automated test frameworks for web and API testing.
Write unit, integration, and end-to-end tests. Champion quality in the development lifecycle.
Experience with Selenium, Playwright, or Cypress for UI testing and pytest/JUnit for API testing.
Strong debugging skills and attention to detail are essential.""",
        "required_skills": ["Python", "Selenium", "Pytest", "API Testing", "CI/CD", "Test Automation"],
        "preferred_skills": ["Playwright", "Cypress", "Load Testing", "Performance Testing", "Java"],
    },
    # ─── Data Engineering ────────────────────────────────────────────────────
    {
        "title": "Data Engineer",
        "company": "DataPipeline Co.",
        "location": "Remote",
        "job_type": "Full-time",
        "experience_level": "Mid-level",
        "category": "Data Science",
        "salary_range": "$110,000 - $145,000",
        "description": """Build and maintain scalable data pipelines for our analytics platform.
Design data models, ETL workflows, and optimize query performance.
Experience with Airflow, Spark, dbt, and cloud data warehouses is required.
You'll work closely with data scientists and analysts to deliver reliable data.""",
        "required_skills": ["Python", "SQL", "Apache Airflow", "dbt", "Spark", "Data Warehousing"],
        "preferred_skills": ["Snowflake", "BigQuery", "Kafka", "Databricks", "AWS"],
    },
    {
        "title": "Analytics Engineer",
        "company": "MetricsOps",
        "location": "Remote",
        "job_type": "Full-time",
        "experience_level": "Mid-level",
        "category": "Data Science",
        "salary_range": "$100,000 - $130,000",
        "description": """Transform raw data into clean, tested, and documented datasets for analysis.
Own the semantic layer using dbt and maintain data quality through testing.
Work with Snowflake or BigQuery to optimize query performance.
Strong SQL and a software engineering mindset applied to data problems.""",
        "required_skills": ["SQL", "dbt", "Snowflake", "Data Modeling", "Python"],
        "preferred_skills": ["Airflow", "Looker", "BigQuery", "Testing", "Version Control"],
    },
    # ─── Product / Project Management ────────────────────────────────────────
    {
        "title": "Scrum Master / Agile Coach",
        "company": "AgileOps",
        "location": "Chicago, IL (Hybrid)",
        "job_type": "Full-time",
        "experience_level": "Mid-level",
        "category": "Product",
        "salary_range": "$90,000 - $120,000",
        "description": """Facilitate agile ceremonies and coach teams on Scrum practices.
Remove impediments, track velocity, and continuously improve team processes.
Strong facilitation and communication skills are essential.
CSM or equivalent certification and 3+ years experience with agile teams required.""",
        "required_skills": ["Scrum", "Agile", "Facilitation", "Jira", "Team Leadership"],
        "preferred_skills": ["SAFe", "Kanban", "Coaching", "Confluence", "Risk Management"],
    },
    {
        "title": "Engineering Manager",
        "company": "TechScale Corp",
        "location": "San Francisco, CA",
        "job_type": "Full-time",
        "experience_level": "Lead",
        "category": "Engineering",
        "salary_range": "$190,000 - $240,000",
        "description": """Lead a team of 6-8 software engineers building our core platform.
Balance technical leadership with people management — hiring, coaching, performance reviews.
Define technical direction, drive execution, and represent engineering to stakeholders.
5+ years engineering experience with at least 2 years managing teams required.""",
        "required_skills": ["Team Leadership", "System Design", "Hiring", "Agile", "Technical Strategy"],
        "preferred_skills": ["Python", "AWS", "OKRs", "Performance Management", "Roadmapping"],
    },
    # ─── AI / Research ────────────────────────────────────────────────────────
    {
        "title": "AI Research Engineer",
        "company": "DeepMind Research",
        "location": "London, UK (Hybrid)",
        "job_type": "Full-time",
        "experience_level": "Senior",
        "category": "Data Science",
        "salary_range": "$160,000 - $210,000",
        "description": """Conduct applied AI research and implement novel algorithms in production.
Strong background in deep learning, reinforcement learning, or generative models.
Publish or implement state-of-the-art research in NLP, vision, or multimodal AI.
PhD or equivalent research experience in ML/AI is strongly preferred.""",
        "required_skills": ["PyTorch", "Research", "Deep Learning", "Python", "Mathematics"],
        "preferred_skills": ["Reinforcement Learning", "JAX", "CUDA", "Paper Publication", "LLMs"],
    },
    {
        "title": "Prompt Engineer / LLM Specialist",
        "company": "GenAI Startup",
        "location": "Remote",
        "job_type": "Full-time",
        "experience_level": "Mid-level",
        "category": "Data Science",
        "salary_range": "$110,000 - $145,000",
        "description": """Design, test, and optimize prompts for large language model applications.
Build reliable LLM pipelines with safety guardrails and evaluation frameworks.
Experience with OpenAI, Anthropic, or Google Gemini APIs is required.
Knowledge of RAG, fine-tuning, and vector databases is a strong plus.""",
        "required_skills": ["Prompt Engineering", "LLMs", "Python", "OpenAI API", "LangChain"],
        "preferred_skills": ["RAG", "Fine-tuning", "Vector Databases", "Evaluation", "Guardrails"],
    },
    # ─── Healthcare / Biotech ─────────────────────────────────────────────────
    {
        "title": "Healthcare Data Analyst",
        "company": "HealthTech Inc.",
        "location": "Boston, MA",
        "job_type": "Full-time",
        "experience_level": "Mid-level",
        "category": "Data Science",
        "salary_range": "$80,000 - $105,000",
        "description": """Analyze clinical and operational data to improve patient outcomes.
Work with EHR data (HL7, FHIR), claims data, and population health datasets.
Strong SQL and Python skills with experience in statistical analysis.
HIPAA compliance knowledge and healthcare domain expertise are required.""",
        "required_skills": ["SQL", "Python", "Data Analysis", "HIPAA", "HL7/FHIR", "Statistics"],
        "preferred_skills": ["Tableau", "R", "Clinical Data", "Machine Learning", "dbt"],
    },
    # ─── Sales / Customer Success ─────────────────────────────────────────────
    {
        "title": "Solutions Engineer / Pre-Sales",
        "company": "EnterpriseSaaS",
        "location": "Remote",
        "job_type": "Full-time",
        "experience_level": "Mid-level",
        "category": "Engineering",
        "salary_range": "$110,000 - $145,000",
        "description": """Partner with sales to demonstrate technical value of our platform to prospects.
Run product demos, build proof-of-concepts, and answer technical questions.
Bridge between sales and engineering — translate customer needs into product feedback.
Prior software engineering background and excellent communication skills required.""",
        "required_skills": ["Technical Communication", "REST APIs", "SQL", "Python", "Demos"],
        "preferred_skills": ["Salesforce", "Docker", "Cloud Platforms", "Customer Success", "Scripting"],
    },
    # ─── Additional Roles ─────────────────────────────────────────────────────
    {
        "title": "Full Stack Developer (Vue.js + Django)",
        "company": "WebAgency Pro",
        "location": "Remote",
        "job_type": "Full-time",
        "experience_level": "Mid-level",
        "category": "Engineering",
        "salary_range": "$90,000 - $120,000",
        "description": """Build web applications using Vue.js and Django REST Framework.
Design database schemas, implement REST APIs, and build interactive frontends.
Experience with PostgreSQL, Docker, and CI/CD pipelines is required.
Strong problem-solving skills and ability to work independently are essential.""",
        "required_skills": ["Vue.js", "Django", "Python", "PostgreSQL", "REST APIs", "JavaScript"],
        "preferred_skills": ["Celery", "Redis", "Docker", "GitLab CI", "TypeScript"],
    },
    {
        "title": "Staff Software Engineer",
        "company": "Unicorn Startup",
        "location": "San Francisco, CA",
        "job_type": "Full-time",
        "experience_level": "Lead",
        "category": "Engineering",
        "salary_range": "$200,000 - $280,000",
        "description": """Shape the technical direction of our platform as a Staff Engineer.
Lead cross-team technical initiatives, mentor senior engineers, and design complex systems.
Deep expertise in distributed systems, databases, and software architecture.
10+ years of software engineering experience with a strong track record of impact.""",
        "required_skills": ["System Design", "Distributed Systems", "Python or Go", "Architecture", "Technical Leadership"],
        "preferred_skills": ["Kafka", "Kubernetes", "PostgreSQL", "AWS", "Open Source"],
    },
    {
        "title": "Platform Engineer",
        "company": "TechPlatform Inc.",
        "location": "Remote",
        "job_type": "Full-time",
        "experience_level": "Senior",
        "category": "DevOps",
        "salary_range": "$140,000 - $175,000",
        "description": """Build and maintain the internal developer platform (IDP) used by 200+ engineers.
Create self-service tooling, golden paths, and platform abstractions for development teams.
Experience with Kubernetes, Backstage, and internal developer portals is valued.
Strong Python/Go scripting and infrastructure automation background required.""",
        "required_skills": ["Kubernetes", "Python", "Go", "CI/CD", "Docker", "Infrastructure as Code"],
        "preferred_skills": ["Backstage", "Terraform", "ArgoCD", "Developer Experience", "GitOps"],
    },
    {
        "title": "Computer Vision Engineer",
        "company": "VisionAI",
        "location": "Remote",
        "job_type": "Full-time",
        "experience_level": "Senior",
        "category": "Data Science",
        "salary_range": "$145,000 - $185,000",
        "description": """Build and deploy computer vision models for real-world applications.
Train object detection, segmentation, and classification models at scale.
Experience with PyTorch, ONNX, and optimizing models for inference.
Work on autonomous vehicles, medical imaging, or retail analytics.""",
        "required_skills": ["Python", "PyTorch", "Computer Vision", "OpenCV", "Deep Learning"],
        "preferred_skills": ["ONNX", "TensorRT", "CUDA", "MLOps", "Edge Deployment"],
    },
    {
        "title": "Database Administrator (DBA)",
        "company": "DataOps Corp",
        "location": "Atlanta, GA (Hybrid)",
        "job_type": "Full-time",
        "experience_level": "Senior",
        "category": "Engineering",
        "salary_range": "$115,000 - $145,000",
        "description": """Manage and optimize PostgreSQL and MySQL databases for enterprise applications.
Perform backup/recovery, query optimization, capacity planning, and security hardening.
Experience with replication, high availability, and disaster recovery is required.
Knowledge of cloud databases (RDS, Cloud SQL) is a plus.""",
        "required_skills": ["PostgreSQL", "MySQL", "SQL", "Database Optimization", "Backup & Recovery"],
        "preferred_skills": ["AWS RDS", "MongoDB", "Redis", "Performance Tuning", "Replication"],
    },
    {
        "title": "Technical Writer",
        "company": "DocuCraft",
        "location": "Remote",
        "job_type": "Full-time",
        "experience_level": "Mid-level",
        "category": "Engineering",
        "salary_range": "$75,000 - $100,000",
        "description": """Create clear, accurate, and comprehensive technical documentation for developer tools.
Write API docs, tutorials, how-to guides, and reference material.
Experience documenting REST APIs with OpenAPI/Swagger is required.
Ability to understand code examples and work closely with engineering teams.""",
        "required_skills": ["Technical Writing", "API Documentation", "OpenAPI", "Markdown", "Developer Tools"],
        "preferred_skills": ["Docusaurus", "Git", "Python scripting", "Confluence", "Diagramming"],
    },
]


async def seed_jobs(db) -> int:
    """
    Seed the database with job listings.
    Generates embeddings for each job and stores them.

    Args:
        db: Async database session.

    Returns:
        Number of jobs seeded.
    """
    from sqlalchemy import select
    from app.models.job import Job
    from app.services.embeddings import generate_embedding

    # Check how many jobs already exist
    result = await db.execute(select(Job))
    existing_jobs = result.scalars().all()
    existing_titles = {j.title for j in existing_jobs}

    seeded_count = 0
    for job_data in SEED_JOBS:
        # Skip if already exists (by title)
        if job_data["title"] in existing_titles:
            continue

        # Generate embedding text from title + description + skills
        embedding_text = (
            f"{job_data['title']} {job_data['description']} "
            f"Skills: {', '.join(job_data['required_skills'])}"
        )

        try:
            embedding = await generate_embedding(embedding_text)
        except Exception:
            embedding = None  # Skip embedding if API unavailable

        job = Job(
            title=job_data["title"],
            company=job_data["company"],
            location=job_data["location"],
            job_type=job_data["job_type"],
            experience_level=job_data["experience_level"],
            category=job_data["category"],
            salary_range=job_data["salary_range"],
            description=job_data["description"],
            required_skills=job_data["required_skills"],
            preferred_skills=job_data["preferred_skills"],
            embedding=embedding,
        )
        db.add(job)
        seeded_count += 1

    await db.commit()
    return seeded_count
