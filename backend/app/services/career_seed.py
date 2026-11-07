import uuid
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import app.models.user  # Ensure User is in metadata
from app.models.career import CareerPath, CareerModule, CareerTopic, CareerSubtopic, TopicLearningContent

def build_topic_content(
    topic_name: str,
    module_name: str,
    career_name: str,
    level: str,
    primary_language: str,
    key_terms: List[str],
    code_snippet: str,
    output_snippet: str
) -> Dict[str, Any]:
    """Generates complete learning content adhering to all 17 master requirements."""
    
    return {
        "topic_name": topic_name,
        "learning_objectives": [
            f"Master core foundational principles and architecture of {topic_name}",
            f"Understand internal working mechanisms, execution lifecycles, and performance tradeoffs",
            f"Write clean, idiomatic, and production-ready code with {primary_language}",
            f"Debug common edge cases, performance bottlenecks, and security vulnerabilities",
            f"Apply concepts to real-world industrial systems and ace technical interviews"
        ],
        "prerequisites": [
            f"Foundations of {career_name}",
            "Basic terminal usage and code editor environment setup",
            "Logical reasoning and algorithmic flow comprehension"
        ],
        "beginner_explanation": (
            f"Imagine you are building a modern skyscraper. {topic_name} is like the foundational framework "
            f"that ensures everything above it stands strong, scales effortlessly, and responds with agility. "
            f"In {career_name}, mastering {topic_name} allows you to break down complex business problems into "
            f"predictable, testable, and reusable building blocks. Whether you are handling high-traffic user requests, "
            f"processing large data streams, or architecting enterprise solutions, {topic_name} gives you the exact tools "
            f"needed to write high-confidence software."
        ),
        "detailed_technical_notes": (
            f"### Technical Architecture & Core Principles: {topic_name}\n\n"
            f"1. **Core Mechanism & Memory Model**:\n"
            f"   In modern runtime environments, {topic_name} executes with strict isolation and performance boundaries. "
            f"   It relies on memory optimization techniques including stack allocation for primitive execution frames and "
            f"   heap management for dynamic reference graph lifecycle. Understanding reference counters and garbage collection cycles "
            f"   prevents memory leaks and latency spikes.\n\n"
            f"2. **Internal Execution Lifecycle**:\n"
            f"   When {topic_name} is invoked, the execution pipeline undergoes compilation/interpretation, AST generation, "
            f"   and bytecode optimization. In production microservices, thread pools and non-blocking I/O multiplexing ensure "
            f"   sub-millisecond latency under concurrent request loads.\n\n"
            f"3. **Concurrency and Thread Safety**:\n"
            f"   State mutation within {topic_name} must adhere to thread-safe contracts. Shared mutable state across worker threads "
            f"   requires explicit synchronization primitives, atomic references, or immutable data structures to prevent race conditions.\n\n"
            f"4. **Enterprise Scalability Best Practices**:\n"
            f"   - Decouple interface specifications from concrete implementations.\n"
            f"   - Apply defensive copying when passing mutable objects across boundaries.\n"
            f"   - Leverage structured logging, tracing spans, and health metrics.\n"
            f"   - Ensure statelessness for horizontal scale-out in containerized clusters."
        ),
        "important_definitions": [
            {
                "term": key_terms[0] if len(key_terms) > 0 else f"{topic_name} Abstraction",
                "definition": f"A structural interface or contract that defines operational behavior without binding to concrete execution logic.",
                "key_concept": "Decoupling specification from runtime implementation."
            },
            {
                "term": key_terms[1] if len(key_terms) > 1 else "State Encapsulation",
                "definition": "The bundling of data with the methods that operate on that data, restricting direct access from external callers.",
                "key_concept": "Data hiding, integrity enforcement, and modular maintenance."
            },
            {
                "term": key_terms[2] if len(key_terms) > 2 else "Runtime Polymorphism",
                "definition": "The mechanism allowing code to invoke behaviors determined dynamically by the underlying concrete instance at runtime.",
                "key_concept": "Open-Closed Principle (OCP) and clean extensibility."
            }
        ],
        "syntax_and_examples": [
            {
                "title": f"Standard Declaration and Usage in {primary_language}",
                "language": primary_language.lower(),
                "syntax": f"// Production structure for {topic_name}\npublic/standard interface/class Component {{\n    // Fields & Behaviors\n}}",
                "example": code_snippet,
                "explanation": f"Demonstrates idiomatic setup, configuration injection, and error-handling wrapping for {topic_name}."
            }
        ],
        "practical_coding_examples": [
            {
                "title": f"Enterprise Implementation: {topic_name}",
                "code": code_snippet,
                "language": primary_language.lower(),
                "explanation": f"This production snippet illustrates clean domain boundaries, input validation, execution error handling, and deterministic output.",
                "output": output_snippet
            }
        ],
        "real_world_applications": [
            {
                "domain": "Fintech & Payments",
                "use_case": "High-Throughput Transaction Ledger",
                "real_example": f"Using {topic_name} to guarantee idempotency, consistency checks, and audit logging across distributed payment gateways."
            },
            {
                "domain": "E-Commerce & Supply Chain",
                "use_case": "Inventory State Synchronization",
                "real_example": f"Applying {topic_name} patterns to manage concurrent stock reservations during high-volume flash sales."
            },
            {
                "domain": "Cloud Infrastructure",
                "use_case": "Microservice Orchestration & Observability",
                "real_example": f"Implementing {topic_name} inside containerized container clusters to handle health-probes and circuit-breaking."
            }
        ],
        "common_mistakes": [
            {
                "mistake": "Ignoring resource cleanup or unclosed connection handles",
                "why_wrong": "Leads to connection pool exhaustion, file descriptor leaks, and memory bloat in long-running services.",
                "how_to_fix": "Always utilize try-with-resources / context managers (with blocks) or defer statements.",
                "corrected_code": "// Always use auto-closing resource handlers\ntry (var client = new Connection()) {\n    client.execute();\n}"
            },
            {
                "mistake": "Catching generic Top-Level Exceptions without logging context",
                "why_wrong": "Swallows critical runtime faults, masking the root cause of failures during production incidents.",
                "how_to_fix": "Catch specific, documented checked/unchecked exceptions and log correlation IDs.",
                "corrected_code": "catch (SpecificDomainException ex) {\n    log.error(\"Context failed id={}\", correlationId, ex);\n    throw ex;\n}"
            }
        ],
        "interview_questions": [
            {
                "question": f"How does {topic_name} behave under high concurrency, and what techniques ensure thread safety?",
                "answer": (
                    f"In {primary_language}, {topic_name} requires careful segregation of mutable state. "
                    f"Techniques include utilizing immutable data objects, thread-local storage, explicit reentrant locks, "
                    f"and concurrent collection wrappers. When horizontal scaling is employed, distributed locks or optimistic "
                    f"locking via version columns in relational databases prevent concurrent update anomalies."
                ),
                "difficulty": "Intermediate",
                "tip": "Always mention both single-node in-memory thread safety and distributed multi-instance locking."
            },
            {
                "question": f"What are the primary performance overheads associated with {topic_name}, and how do you profile them?",
                "answer": (
                    f"Overheads usually stem from frequent heap allocation, reflection/dynamic proxy lookups, or unindexed I/O queries. "
                    f"Profiling involves CPU flame graphs, memory allocation analyzers (e.g. JProfiler, Py-Spy), and APM spans."
                ),
                "difficulty": "Advanced",
                "tip": "Discuss asymptotic time complexity O(1) vs O(N) and I/O wait times."
            }
        ],
        "mcqs": [
            {
                "id": 1,
                "question": f"Which of the following best characterizes {topic_name} in an enterprise system?",
                "options": [
                    "It is only used for small script execution and cannot scale horizontally.",
                    "It provides modular, testable, and decoupled architectural capabilities with deterministic lifecycle management.",
                    "It replaces all relational databases and caching layers entirely.",
                    "It removes the need for type safety and runtime error handling."
                ],
                "correct_option": 1,
                "explanation": f"{topic_name} provides robust, modular architecture with clear separation of concerns, ensuring maintainability."
            },
            {
                "id": 2,
                "question": "What is the recommended approach for managing resource lifecycles?",
                "options": [
                    "Rely solely on finalizers and manual garbage collection triggers.",
                    "Keep handles open globally across application instances.",
                    "Use deterministic resource management constructs (try-with-resources / context managers).",
                    "Suppress all cleanup errors and never close file descriptors."
                ],
                "correct_option": 2,
                "explanation": "Deterministic resource management guarantees that socket, DB, and file handles are released promptly."
            },
            {
                "id": 3,
                "question": "When designing high-throughput APIs, what is the primary benefit of immutability?",
                "options": [
                    "Decreases compilation time by half.",
                    "Eliminates race conditions since state cannot be modified after instantiation.",
                    "Allows direct hardware register manipulation.",
                    "Disables JSON serialization."
                ],
                "correct_option": 1,
                "explanation": "Immutable objects are inherently thread-safe because their state cannot change once published."
            }
        ],
        "coding_exercises": [
            {
                "id": 1,
                "title": f"Exercise 1: Implement Core Logic for {topic_name}",
                "description": f"Write a robust function or class that implements the key workflow for {topic_name}. Validate inputs, handle boundary errors, and return structured output.",
                "starter_code": f"// Starter template for {topic_name}\npublic class Solution {{\n    public String execute(String input) {{\n        // TODO: Implement your logic here\n        return null;\n    }}\n}}",
                "solution_code": f"public class Solution {{\n    public String execute(String input) {{\n        if (input == null || input.isBlank()) throw new IllegalArgumentException(\"Invalid input\");\n        return \"Processed: \" + input.trim().toUpperCase();\n    }}\n}}",
                "test_cases": [
                    {"input": "hello", "expected": "Processed: HELLO"},
                    {"input": "nexora", "expected": "Processed: NEXORA"}
                ]
            }
        ],
        "mini_projects": [
            {
                "title": f"Mini-Project: Production-Ready {topic_name} Service",
                "description": f"Build a modular standalone service that exposes a RESTful endpoint, validates payload schemas, executes {topic_name} operations, and logs execution latency.",
                "requirements": [
                    "Clean domain model separation (Controller -> Service -> Repository)",
                    "Comprehensive unit tests with at least 80% code coverage",
                    "Structured JSON error responses with standard HTTP status codes",
                    "Docker container configuration for reproducible deployments"
                ],
                "steps": [
                    "1. Define domain interfaces and DTOs",
                    "2. Implement business logic and validation rules",
                    "3. Add integration test suite with mock dependencies",
                    "4. Package application with container build script"
                ],
                "deliverables": "Source repository with README, unit test suite, and Dockerfile."
            }
        ],
        "revision_notes": (
            f"### Quick Revision Sheet: {topic_name}\n"
            f"- **Core Concept**: Encapsulates {topic_name} operational logic with high cohesion and low coupling.\n"
            f"- **Performance Rule**: Avoid redundant allocations in hot loops; reuse buffers and connection pools.\n"
            f"- **Safety Rule**: Treat external inputs as untrusted; enforce schema boundaries at ingestion.\n"
            f"- **Testing**: Combine unit tests for edge cases with integration tests for external contracts."
        ),
        "key_takeaways": [
            f"Deep understanding of {topic_name} is essential for senior-level engineering competence.",
            "Always prioritize readability, automated tests, and idiomatic conventions over premature micro-optimizations.",
            "Architect for observable failure modes using structured logging and distributed tracing."
        ],
        "additional_learning_resources": [
            {
                "title": f"Official Documentation: {primary_language} Standards",
                "url": "https://docs.oracle.com/en/java/" if primary_language == "Java" else ("https://docs.python.org/3/" if primary_language == "Python" else "https://pandas.pydata.org/docs/"),
                "type": "Official Documentation",
                "note": "Comprehensive API specifications and language evolution notes."
            },
            {
                "title": "Architectural Patterns & Clean Code",
                "url": "https://martinfowler.com/architecture/",
                "type": "Architecture Guide",
                "note": "Industry-standard design patterns, domain-driven design, and refactoring techniques."
            }
        ],
        "estimated_learning_time_minutes": 120 if level == "Advanced" else (90 if level == "Intermediate" else 60),
        "topic_completion_assessment": {
            "passing_score_percentage": 80,
            "required_tasks": [
                "Answer all 3 MCQs correctly",
                "Submit working solution for coding exercise",
                "Review technical notes and key takeaways"
            ],
            "rubric": "Demonstrates clear understanding of principles, idiomatic syntax, and production error handling."
        }
    }

# -------------------------------------------------------------
# Career Path Definitions
# -------------------------------------------------------------

JAVA_PATH_SPEC = {
    "title": "Java Full Stack Development",
    "slug": "java-full-stack",
    "description": (
        "Complete enterprise-grade Java full stack curriculum from programming fundamentals, Core Java, "
        "OOP, Collections, Multithreading, DSA, SQL databases, Spring Boot, Spring Security, React.js frontend, "
        "Docker CI/CD, to production deployment and portfolio engineering."
    ),
    "icon": "Coffee",
    "estimated_weeks": 24,
    "total_hours": 180,
    "modules": [
        {
            "title": "Module 1: Java Foundations & OOP Mastery",
            "description": "Programming fundamentals, Core Java, OOP principles, collections, and modern Java 8+ features.",
            "difficulty": "Beginner",
            "estimated_hours": 35,
            "topics": [
                {
                    "title": "Programming fundamentals and problem-solving",
                    "subtopics": ["Algorithms & Flowcharts", "Pseudocode & Logic", "Variables & Memory layout", "Problem Decomposition"],
                    "terms": ["Algorithm Complexity", "Control Flow", "Stack vs Heap Memory"],
                    "code": "public class Basics {\n    public static void main(String[] args) {\n        int sum = 0;\n        for (int i = 1; i <= 10; i++) sum += i;\n        System.out.println(\"Sum: \" + sum);\n    }\n}",
                    "output": "Sum: 55"
                },
                {
                    "title": "Core Java and OOP",
                    "subtopics": ["JVM, JRE, JDK architecture", "Compilation & Bytecode", "Garbage Collection Basics", "Package Management"],
                    "terms": ["Java Virtual Machine", "Just-In-Time Compiler", "Garbage Collector"],
                    "code": "public class ArchitectureDemo {\n    public static void main(String[] args) {\n        System.out.println(\"Java Version: \" + System.getProperty(\"java.version\"));\n    }\n}",
                    "output": "Java Version: 21.0.2"
                },
                {
                    "title": "Data types, operators, control statements, arrays and strings",
                    "subtopics": ["Primitive vs Reference types", "Bitwise & Logical Operators", "Loops & Pattern printing", "String immutability & StringBuilder", "Multi-dimensional Arrays"],
                    "terms": ["String Constant Pool", "Primitive Boxing", "Array Allocation"],
                    "code": "public class StringDemo {\n    public static void main(String[] args) {\n        StringBuilder sb = new StringBuilder(\"Nexora\");\n        sb.append(\" AI Platform\");\n        System.out.println(sb.toString());\n    }\n}",
                    "output": "Nexora AI Platform"
                },
                {
                    "title": "Classes, objects, inheritance, polymorphism, abstraction and encapsulation",
                    "subtopics": ["Class design & Constructors", "Single & Multi-level Inheritance", "Method Overloading vs Overriding", "Abstract Classes vs Interfaces", "Access Modifiers"],
                    "terms": ["Dynamic Method Dispatch", "Encapsulation Boundary", "Interface Contract"],
                    "code": "abstract class Service {\n    abstract void process();\n}\nclass UserService extends Service {\n    void process() { System.out.println(\"Processing User Account\"); }\n}",
                    "output": "Processing User Account"
                },
                {
                    "title": "Collections Framework, generics and exception handling",
                    "subtopics": ["List, Set, Map hierarchies", "Generics & Type Erasure", "Checked vs Unchecked Exceptions", "Custom Exception Classes", "Fail-Fast vs Fail-Safe Iterators"],
                    "terms": ["HashMap Bucket Collisions", "Bounded Wildcards", "Custom Exception Hierarchy"],
                    "code": "import java.util.*;\npublic class CollectionDemo {\n    public static void main(String[] args) {\n        Map<String, Integer> scores = new HashMap<>();\n        scores.put(\"Java\", 98);\n        System.out.println(scores.getOrDefault(\"Java\", 0));\n    }\n}",
                    "output": "98"
                },
                {
                    "title": "Multithreading, file handling, streams and Java 8+ features",
                    "subtopics": ["Thread Lifecycle & Synchronization", "ExecutorService & Thread Pools", "NIO.2 File Operations", "Lambda expressions & Method references", "Stream API & Optional", "CompletableFuture"],
                    "terms": ["ForkJoinPool", "Stream Pipelines", "Deadlock Prevention"],
                    "code": "import java.util.List;\npublic class StreamDemo {\n    public static void main(String[] args) {\n        List<String> list = List.of(\"react\", \"spring\", \"postgres\");\n        list.stream().filter(s -> s.startsWith(\"s\")).map(String::toUpperCase).forEach(System.out::println);\n    }\n}",
                    "output": "SPRING"
                }
            ]
        },
        {
            "title": "Module 2: DSA & Persistence Layer",
            "description": "Data structures and algorithms in Java, relational databases, SQL optimization, JDBC, and Hibernate ORM.",
            "difficulty": "Intermediate",
            "estimated_hours": 40,
            "topics": [
                {
                    "title": "DSA and coding practice",
                    "subtopics": ["Time & Space Complexity O(N)", "Linked Lists & Trees", "Stacks, Queues & PriorityQueue", "Graphs, BFS & DFS", "Dynamic Programming & Greedy Algorithms"],
                    "terms": ["Binary Search Tree", "Memoization", "Amortized Complexity"],
                    "code": "public class BinarySearch {\n    public static int search(int[] arr, int target) {\n        int l = 0, r = arr.length - 1;\n        while(l <= r) {\n            int mid = l + (r - l) / 2;\n            if (arr[mid] == target) return mid;\n            if (arr[mid] < target) l = mid + 1; else r = mid - 1;\n        }\n        return -1;\n    }\n}",
                    "output": "Index found: 2"
                },
                {
                    "title": "SQL, database design, PostgreSQL and MySQL",
                    "subtopics": ["Database Normalization (1NF to 3NF)", "DDL, DML, DQL Queries", "Complex Joins & Subqueries", "Indexing Strategies (B-Tree, Hash)", "ACID Transactions & Isolation Levels"],
                    "terms": ["ACID Compliance", "Foreign Key Constraints", "Index Scan vs Seq Scan"],
                    "code": "SELECT u.email, COUNT(p.id) as total_projects \nFROM users u \nLEFT JOIN research_projects p ON u.id = p.user_id \nGROUP BY u.email \nHAVING COUNT(p.id) > 0;",
                    "output": "developer@nexora.ai | 4"
                },
                {
                    "title": "JDBC and ORM concepts",
                    "subtopics": ["Connection Pooling (HikariCP)", "PreparedStatement & SQL Injection Prevention", "Transaction Management in JDBC", "Object-Relational Mapping Paradigms"],
                    "terms": ["Connection Pool", "Prepared Statement", "Object-Relational Impedance Mismatch"],
                    "code": "try (Connection conn = dataSource.getConnection();\n     PreparedStatement ps = conn.prepareStatement(\"SELECT * FROM users WHERE email = ?\")) {\n    ps.setString(1, \"test@nexora.ai\");\n    ResultSet rs = ps.executeQuery();\n}",
                    "output": "Database query completed safely"
                }
            ]
        },
        {
            "title": "Module 3: Modern Frontend & Web Architecture",
            "description": "HTML5, CSS3, modern JavaScript, React.js, component architecture, and REST API consumption.",
            "difficulty": "Intermediate",
            "estimated_hours": 35,
            "topics": [
                {
                    "title": "HTML5, CSS3, JavaScript and responsive design",
                    "subtopics": ["Semantic HTML Elements", "CSS Grid & Flexbox", "Tailwind CSS & Utility-first design", "ES6+ Modern JavaScript (Promises, async/await)", "DOM Manipulation & Events"],
                    "terms": ["Event Loop", "Flexbox Axis", "CSS Cascade & Specificity"],
                    "code": "const fetchUserData = async (id) => {\n  try {\n    const response = await fetch(`/api/profile/${id}`);\n    return await response.json();\n  } catch (err) {\n    console.error('Fetch error', err);\n  }\n};",
                    "output": "{ id: 1, name: 'Alex' }"
                },
                {
                    "title": "React.js and frontend development",
                    "subtopics": ["JSX & Component LifeCycle", "React Hooks (useState, useEffect, useMemo, useCallback)", "State Management & Context API", "React Router & Navigation", "Component Design Systems"],
                    "terms": ["Virtual DOM", "Reconciliation Algorithm", "Custom Hooks"],
                    "code": "import React, { useState } from 'react';\nexport function Counter() {\n  const [count, setCount] = useState(0);\n  return <button onClick={() => setCount(c => c + 1)}>Count: {count}</button>;\n}",
                    "output": "Rendered interactive button"
                },
                {
                    "title": "REST APIs and HTTP",
                    "subtopics": ["HTTP Methods (GET, POST, PUT, DELETE, PATCH)", "Status Codes & Headers", "RESTful Architectural Constraints", "CORS & Content Negotiation", "API Versioning"],
                    "terms": ["Idempotence", "HATEOAS", "Preflight OPTIONS request"],
                    "code": "POST /api/v1/projects HTTP/1.1\nHost: api.nexora.ai\nContent-Type: application/json\n\n{\"title\": \"Deep Learning Research\", \"domain\": \"AI\"}",
                    "output": "HTTP/1.1 201 Created"
                }
            ]
        },
        {
            "title": "Module 4: Spring Boot Microservices & Security",
            "description": "Enterprise backend development with Spring Boot, Spring Data JPA, Hibernate, Spring Security, and JWT.",
            "difficulty": "Advanced",
            "estimated_hours": 45,
            "topics": [
                {
                    "title": "Spring Framework, Spring Boot and Spring MVC",
                    "subtopics": ["Inversion of Control (IoC) & Dependency Injection", "Spring Boot Starters & Auto-configuration", "@RestController & Request Mapping", "Validation & Global Exception Handling", "Application Properties & Profiles"],
                    "terms": ["IoC Container", "ApplicationContext", "ControllerAdvice"],
                    "code": "@RestController\n@RequestMapping(\"/api/v1/health\")\npublic class HealthController {\n    @GetMapping\n    public ResponseEntity<Map<String, String>> health() {\n        return ResponseEntity.ok(Map.of(\"status\", \"UP\"));\n    }\n}",
                    "output": "{\"status\": \"UP\"}"
                },
                {
                    "title": "Spring Data JPA and Hibernate",
                    "subtopics": ["Entity Mapping & Annotations (@Entity, @Table, @Id)", "Relationship Mappings (@OneToMany, @ManyToMany)", "Derived Query Methods & JPQL", "Lazy vs Eager Loading & N+1 Problem", "Paging & Sorting"],
                    "terms": ["First-Level vs Second-Level Cache", "N+1 Query Issue", "JPQL Projection"],
                    "code": "public interface ProjectRepository extends JpaRepository<ResearchProject, UUID> {\n    List<ResearchProject> findByUserIdAndStatus(UUID userId, String status);\n}",
                    "output": "Repository query generated dynamically"
                },
                {
                    "title": "Spring Security, JWT and authentication",
                    "subtopics": ["SecurityFilterChain & Filter Architecture", "AuthenticationManager & UserDetailsService", "JWT Token Generation & Validation", "Role-Based Access Control (@PreAuthorize)", "OAuth2 & Social Logins"],
                    "terms": ["Bearer Token", "Security Context Holder", "CSRF Protection"],
                    "code": "@Bean\npublic SecurityFilterChain filterChain(HttpSecurity http) throws Exception {\n    return http.csrf(csrf -> csrf.disable())\n               .authorizeHttpRequests(auth -> auth.requestMatchers(\"/auth/**\").permitAll().anyRequest().authenticated())\n               .build();\n}",
                    "output": "Security configuration loaded"
                },
                {
                    "title": "Unit testing and integration testing",
                    "subtopics": ["JUnit 5 Architecture & Assertions", "Mockito & Mocking Services", "Testcontainers & PostgreSQL integration tests", "WebMvcTest & MockMvc", "Code Coverage Analysis with JaCoCo"],
                    "terms": ["Mock vs Spy", "Test Fixture", "Integration Slice Test"],
                    "code": "@SpringBootTest\nclass ProjectServiceTest {\n    @Test\n    void contextLoads() {\n        assertTrue(true);\n    }\n}",
                    "output": "Tests passed: 100%"
                }
            ]
        },
        {
            "title": "Module 5: DevOps, Cloud & Full Stack Capstone",
            "description": "Git, Maven, Docker, CI/CD pipelines, cloud deployment, and full-stack portfolio projects.",
            "difficulty": "Advanced",
            "estimated_hours": 25,
            "topics": [
                {
                    "title": "Git, GitHub, Maven and build tools",
                    "subtopics": ["Git Branching Strategies (GitFlow, Trunk-based)", "Merge vs Rebase", "Maven Lifecycle & Dependency Management", "Multi-module Maven Projects"],
                    "terms": ["Trunk-Based Development", "POM hierarchy", "Git Cherry-Pick"],
                    "code": "git checkout -b feature/career-roadmap\ngit commit -m \"feat: implement complete topic notes\"\ngit push origin feature/career-roadmap",
                    "output": "Branch pushed to GitHub"
                },
                {
                    "title": "Docker, CI/CD, deployment and cloud fundamentals",
                    "subtopics": ["Dockerfile Multi-stage Builds", "Docker Compose Multi-container orchestration", "GitHub Actions CI/CD workflows", "AWS/Cloud Deployment (ECS, RDS, S3)", "Container Security & Healthchecks"],
                    "terms": ["Multi-stage Docker Build", "Container Layer Caching", "Continuous Delivery"],
                    "code": "FROM eclipse-temurin:21-jre-alpine\nCOPY target/*.jar app.jar\nENTRYPOINT [\"java\", \"-jar\", \"/app.jar\"]",
                    "output": "Container image built successfully"
                },
                {
                    "title": "Full-stack projects, portfolio and interview preparation",
                    "subtopics": ["Architecting an Enterprise Full-Stack SaaS", "System Design Fundamentals (Rate Limiting, Caching, DB Sharding)", "Resume & GitHub Portfolio Polish", "Mock Technical & Behavioral Interviews"],
                    "terms": ["System Design Architecture", "CAP Theorem", "STAR Interview Method"],
                    "code": "// Full Stack Nexora Architecture Architecture Review\nClient (React) -> Gateway -> Spring Boot Services -> PostgreSQL & Redis",
                    "output": "Ready for high-impact production roles"
                }
            ]
        }
    ]
}

PYTHON_PATH_SPEC = {
    "title": "Python Full Stack Development",
    "slug": "python-full-stack",
    "description": (
        "Comprehensive Python full-stack engineering path from Python core syntax, OOP, DSA, "
        "PostgreSQL database architecture, modern web frontend, Django, Flask, FastAPI microservices, "
        "REST APIs, JWT security, Docker CI/CD, and portfolio projects."
    ),
    "icon": "Terminal",
    "estimated_weeks": 22,
    "total_hours": 160,
    "modules": [
        {
            "title": "Module 1: Python Core & Advanced Paradigms",
            "description": "Python fundamentals, data structures, OOP, file handling, iterators, generators, and decorators.",
            "difficulty": "Beginner",
            "estimated_hours": 35,
            "topics": [
                {
                    "title": "Python fundamentals and problem-solving",
                    "subtopics": ["Python Interpreter & Bytecode", "Variables, Dynamic Typing, and Memory", "Input/Output & String Formatting", "Algorithmic Problem-Solving"],
                    "terms": ["GIL (Global Interpreter Lock)", "Dynamic Typing", "CPython Execution"],
                    "code": "def solve(n: int) -> int:\n    return sum(i for i in range(1, n + 1) if i % 2 == 0)\nprint(solve(10))",
                    "output": "30"
                },
                {
                    "title": "Data types, operators, conditions, loops and functions",
                    "subtopics": ["Numeric types, booleans, and None", "Bitwise, Comparison, and Identity Operators", "Conditional branching (if/elif/else, match-case)", "While and For loops with else clause", "Functions (*args, **kwargs, default params)"],
                    "terms": ["Scope Resolution (LEGB)", "First-Class Functions", "Short-Circuit Evaluation"],
                    "code": "def calculate_stats(*values, factor=1.0):\n    return sum(values) * factor\nprint(calculate_stats(10, 20, 30, factor=1.5))",
                    "output": "90.0"
                },
                {
                    "title": "Lists, tuples, sets and dictionaries",
                    "subtopics": ["List comprehensions & Slicing", "Tuples & NamedTuples", "Set theory operations (union, intersection)", "Dictionary hashing, views, and comprehension", "collections module (deque, Counter, defaultdict)"],
                    "terms": ["Hash Table Under the Hood", "Mutable vs Immutable", "Dictionary Key Invariants"],
                    "code": "from collections import Counter\ncounts = Counter([\"java\", \"python\", \"python\", \"react\"])\nprint(counts.most_common(1))",
                    "output": "[('python', 2)]"
                },
                {
                    "title": "OOP, modules, packages and exception handling",
                    "subtopics": ["Classes, instances, and self", "Inheritance and MRO (Method Resolution Order)", "Dunder/Magic methods (__init__, __str__, __repr__)", "Creating and publishing packages", "Try/Except/Else/Finally blocks"],
                    "terms": ["Method Resolution Order (MRO)", "Duck Typing", "Context Manager Protocol"],
                    "code": "class Model:\n    def __init__(self, name: str):\n        self.name = name\n    def __repr__(self):\n        return f\"Model(name='{self.name}')\"\nprint(repr(Model('Nexora')))",
                    "output": "Model(name='Nexora')"
                },
                {
                    "title": "File handling, iterators, generators and decorators",
                    "subtopics": ["Context managers (with statement)", "Custom iterators (__iter__, __next__)", "Generators and yield keyword", "Function decorators with arguments", "functools (lru_cache, wraps)"],
                    "terms": ["Generator Memory Efficiency", "Closure Scope", "Memoization Cache"],
                    "code": "import functools\ndef timed(func):\n    @functools.wraps(func)\n    def wrapper(*args, **kwargs):\n        return func(*args, **kwargs)\n    return wrapper",
                    "output": "Decorator initialized"
                }
            ]
        },
        {
            "title": "Module 2: DSA, Databases & Relational Modeling",
            "description": "Data structures and algorithms in Python, SQL fundamentals, PostgreSQL database design, and ORM.",
            "difficulty": "Intermediate",
            "estimated_hours": 35,
            "topics": [
                {
                    "title": "DSA and coding practice",
                    "subtopics": ["Big-O Complexity in Python", "Arrays, Linked Lists, and Stacks", "Trees, Graphs, and Hash Maps", "Sorting & Searching Algorithms", "Dynamic Programming & Recursion"],
                    "terms": ["Timsort Algorithm", "Graph Traversal", "Recursion Depth Limit"],
                    "code": "def fib(n: int, memo={}) -> int:\n    if n in memo: return memo[n]\n    if n <= 1: return n\n    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)\n    return memo[n]\nprint(fib(10))",
                    "output": "55"
                },
                {
                    "title": "SQL, PostgreSQL and database design",
                    "subtopics": ["PostgreSQL Schema Architecture", "Table constraints & Foreign keys", "Complex Joins, Aggregations, and Window functions", "Indexes (B-tree, GIN for JSONB)", "Database Transactions and Isolation"],
                    "terms": ["PostgreSQL MVCC", "Window Functions (OVER, PARTITION BY)", "GIN Indexing"],
                    "code": "SELECT project_id, metric_name, AVG(metric_value) OVER(PARTITION BY project_id) \nFROM research_results;",
                    "output": "Query executed with window aggregates"
                },
                {
                    "title": "ORM and database integration",
                    "subtopics": ["SQLAlchemy 2.0 Core & ORM", "Async SQLAlchemy with asyncpg", "Alembic Migrations", "Relationship loading strategies", "Session Lifecycle and Transactions"],
                    "terms": ["Unit of Work Pattern", "Async Engine Connection Pool", "Identity Map"],
                    "code": "async with AsyncSessionLocal() as session:\n    result = await session.execute(select(User).filter_by(email='user@nexora.ai'))\n    user = result.scalars().first()",
                    "output": "Retrieved user asynchronously"
                }
            ]
        },
        {
            "title": "Module 3: Frontend & REST API Integration",
            "description": "HTML, CSS, JavaScript, React.js, and REST API development with FastAPI and Flask.",
            "difficulty": "Intermediate",
            "estimated_hours": 35,
            "topics": [
                {
                    "title": "HTML, CSS, JavaScript and React.js",
                    "subtopics": ["Responsive layout with Tailwind CSS", "Modern JS (ES Modules, Async/Await)", "React Functional Components and Hooks", "API Integration with Axios", "State Management in React"],
                    "terms": ["React Reconciliation", "State Immutability", "CSS Responsive Breakpoints"],
                    "code": "import { useEffect, useState } from 'react';\nimport axios from 'axios';\n// Fetch career roadmaps from FastAPI backend\nexport const useRoadmaps = () => {\n  const [data, setData] = useState([]);\n  useEffect(() => { axios.get('/api/career/paths').then(res => setData(res.data)); }, []);\n  return data;\n};",
                    "output": "Hook connected to backend"
                },
                {
                    "title": "Backend development using Django, Flask and FastAPI",
                    "subtopics": ["FastAPI ASGI architecture & Starlette", "Pydantic v2 schemas and validation", "Flask WSGI application design", "Django Batteries-Included framework", "Async route handlers & background tasks"],
                    "terms": ["ASGI vs WSGI", "Pydantic Data Parsing", "Dependency Injection in FastAPI"],
                    "code": "from fastapi import FastAPI, Depends\napp = FastAPI(title='Nexora API')\n@app.get('/health')\nasync def health():\n    return {'status': 'healthy'}",
                    "output": "{\"status\": \"healthy\"}"
                },
                {
                    "title": "REST API development",
                    "subtopics": ["RESTful Resource Design & Status Codes", "Request validation with Pydantic", "Error handling and custom HTTPExceptions", "Pagination, filtering, and sorting", "OpenAPI (Swagger) auto-documentation"],
                    "terms": ["OpenAPI 3.0", "Idempotent HTTP methods", "Content Negotiation"],
                    "code": "@router.get('/papers', response_model=List[PaperResponse])\nasync def get_papers(skip: int = 0, limit: int = 20, db = Depends(get_db)):\n    return await fetch_papers(db, skip, limit)",
                    "output": "Documented Swagger endpoint"
                }
            ]
        },
        {
            "title": "Module 4: Security, Testing & DevOps",
            "description": "Authentication, JWT tokens, testing, CI/CD, Docker containerization, and cloud deployment.",
            "difficulty": "Advanced",
            "estimated_hours": 35,
            "topics": [
                {
                    "title": "Authentication, authorization and security",
                    "subtopics": ["Password hashing with bcrypt / passlib", "JWT access & refresh tokens", "OAuth2 Password Flow with Bearer token", "Role-Based Access Control (RBAC)", "CORS, Rate Limiting, and SQL Injection Prevention"],
                    "terms": ["Bcrypt Salt Rounds", "JWT Claims & Expiration", "OWASP Top 10 Mitigation"],
                    "code": "from jose import jwt\nfrom datetime import datetime, timedelta\ntoken = jwt.encode({'sub': user.email, 'exp': datetime.utcnow() + timedelta(hours=24)}, 'SECRET', algorithm='HS256')",
                    "output": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                },
                {
                    "title": "Testing and debugging",
                    "subtopics": ["pytest test runner & fixtures", "httpx AsyncClient for API testing", "Mocking with unittest.mock", "Code coverage reporting with pytest-cov", "Debugging with pdb and rich tracebacks"],
                    "terms": ["Pytest Fixtures", "Test Isolation", "Async Test Client"],
                    "code": "import pytest\nfrom httpx import AsyncClient\n@pytest.mark.asyncio\nasync def test_health(app_client: AsyncClient):\n    response = await app_client.get('/health')\n    assert response.status_code == 200",
                    "output": "1 passed in 0.04s"
                },
                {
                    "title": "Git, GitHub and project management",
                    "subtopics": ["Git branching, pull requests, and code reviews", "GitHub Actions workflows", "Pre-commit hooks (black, flake8, ruff)", "Semantic versioning and changelogs"],
                    "terms": ["Branch Protection Rules", "Semantic Versioning", "CI Pipeline"],
                    "code": "# .github/workflows/ci.yml\nname: Python CI\non: [push, pull_request]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v3\n      - run: pytest",
                    "output": "Automated checks green"
                },
                {
                    "title": "Docker, CI/CD and deployment",
                    "subtopics": ["Multi-stage Dockerfile for FastAPI", "Docker Compose multi-container setup", "Gunicorn / Uvicorn worker process management", "Cloud deployment on Render / AWS ECS", "SSL configuration & NGINX reverse proxy"],
                    "terms": ["Container Layer Optimization", "Uvicorn Worker Scaling", "Reverse Proxy"],
                    "code": "FROM python:3.12-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY . .\nCMD [\"uvicorn\", \"app.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]",
                    "output": "Production container ready"
                },
                {
                    "title": "Full-stack projects, portfolio and interview preparation",
                    "subtopics": ["End-to-End SaaS application architecture", "System Design for High-Throughput Python Backends", "Live Coding Interview Techniques (LeetCode Patterns)", "Showcase Portfolio Website & Resume Review"],
                    "terms": ["System Design Scalability", "Caching Strategies (Redis)", "Behavioral Interview Prep"],
                    "code": "# Production Architecture\nFrontend: React + Tailwind | Backend: FastAPI Async | Database: PostgreSQL 17",
                    "output": "Ready for top-tier full-stack roles"
                }
            ]
        }
    ]
}

DATA_ANALYSIS_PATH_SPEC = {
    "title": "Data Analysis",
    "slug": "data-analysis",
    "description": (
        "Complete modern data analyst path from Excel mastery, data cleaning, advanced SQL, PostgreSQL, "
        "Python data analysis (NumPy, Pandas), EDA, statistical probability, Matplotlib & Seaborn visualization, "
        "Power BI, Power Query, DAX, business storytelling, real-world case studies, and portfolio engineering."
    ),
    "icon": "BarChart3",
    "estimated_weeks": 20,
    "total_hours": 140,
    "modules": [
        {
            "title": "Module 1: Excel & Data Preparation Foundations",
            "description": "Excel mastery, formula architecture, advanced data cleaning, and validation workflows.",
            "difficulty": "Beginner",
            "estimated_hours": 25,
            "topics": [
                {
                    "title": "Excel fundamentals and advanced Excel",
                    "subtopics": ["Formulas (XLOOKUP, INDEX/MATCH, SUMIFS)", "Pivot Tables & Slicers", "Conditional Formatting & Data Validation", "What-If Analysis & Goal Seek", "Dynamic Array Formulas"],
                    "terms": ["XLOOKUP Matrix", "Pivot Cache", "Dynamic Array Spill Range"],
                    "code": "=XLOOKUP(A2, Customers!A:A, Customers!D:D, \"Not Found\", 0)",
                    "output": "Returned matched customer revenue"
                },
                {
                    "title": "Data cleaning and data preparation",
                    "subtopics": ["Handling Missing Values & Null Imputation", "Deduplication & String Standardization", "Outlier Detection using IQR & Z-score", "Data Type Conversions & Date Parsing", "Data Profiling & Quality Auditing"],
                    "terms": ["Interquartile Range (IQR)", "Data Quality Dimensions", "Type Casting"],
                    "code": "=TRIM(CLEAN(PROPER(A2)))",
                    "output": "Cleaned formatted name string"
                }
            ]
        },
        {
            "title": "Module 2: Advanced SQL & Database Querying",
            "description": "SQL fundamentals, complex queries, window functions, and PostgreSQL analytical querying.",
            "difficulty": "Intermediate",
            "estimated_hours": 30,
            "topics": [
                {
                    "title": "SQL fundamentals and advanced SQL",
                    "subtopics": ["SELECT, WHERE, GROUP BY, HAVING, ORDER BY", "Inner, Left, Right, and Full Outer Joins", "Subqueries and Common Table Expressions (CTEs)", "Window Functions (ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD)", "Query Execution Plans & Indexing"],
                    "terms": ["Common Table Expression (CTE)", "Window Framing (ROWS BETWEEN)", "Query Cost Analysis"],
                    "code": "WITH MonthlyRevenue AS (\n    SELECT DATE_TRUNC('month', created_at) as month, SUM(metric_value) as revenue\n    FROM research_results\n    GROUP BY 1\n)\nSELECT month, revenue, LAG(revenue) OVER(ORDER BY month) as prev_month\nFROM MonthlyRevenue;",
                    "output": "Month | Revenue | Prev Month"
                },
                {
                    "title": "PostgreSQL and database querying",
                    "subtopics": ["PostgreSQL Advanced Aggregate Functions", "JSONB Querying and Indexing", "Date/Time and Timestamp Math", "Full-Text Search (tsvector, tsquery)", "Analytical Views & Materialized Views"],
                    "terms": ["Materialized View Refresh", "JSONB Path Queries", "Full-Text Search GIN Index"],
                    "code": "SELECT id, title, abstract \nFROM research_papers \nWHERE to_tsvector('english', title || ' ' || abstract) @@ to_tsquery('english', 'machine & learning');",
                    "output": "Top matched research papers returned"
                }
            ]
        },
        {
            "title": "Module 3: Python for Data Analysis & Exploratory Analytics",
            "description": "Python syntax for analysts, NumPy numerical arrays, Pandas dataframes, and exploratory data analysis.",
            "difficulty": "Intermediate",
            "estimated_hours": 35,
            "topics": [
                {
                    "title": "Python fundamentals for analysis",
                    "subtopics": ["Python Data Types & Collections for Analysts", "List & Dictionary Comprehensions", "Functions, Lambda, and Map/Filter", "Jupyter Notebooks Environment & Best Practices"],
                    "terms": ["Vectorized Operations", "Jupyter Kernel Lifecycle", "Lambda Mapping"],
                    "code": "revenue = [12000, 15400, 18900, 22100]\ngrowth = [(revenue[i] - revenue[i-1]) / revenue[i-1] * 100 for i in range(1, len(revenue))]\nprint([round(g, 1) for g in growth])",
                    "output": "[28.3, 22.7, 16.9]"
                },
                {
                    "title": "NumPy and Pandas",
                    "subtopics": ["NumPy N-dimensional Arrays & Broadcasting", "Vectorized Array Math & Slicing", "Pandas Series & DataFrames", "Data Ingestion (CSV, Excel, SQL, JSON)", "Boolean Indexing and loc/iloc selection"],
                    "terms": ["Broadcasting Rules", "DataFrame Memory Layout", "Vectorized Boolean Masking"],
                    "code": "import pandas as pd\ndf = pd.DataFrame({'user_id': [1, 2], 'score': [85, 92]})\nprint(df[df['score'] >= 90])",
                    "output": "   user_id  score\n1        2     92"
                },
                {
                    "title": "Data manipulation and exploratory data analysis",
                    "subtopics": ["GroupBy Aggregations & Pivot Tables in Pandas", "Handling Missing Values (fillna, dropna, interpolate)", "Merging, Joining, and Concatenating DataFrames", "Datetime Resampling and Rolling Window Metrics", "EDA Checklist and Descriptive Summaries"],
                    "terms": ["Split-Apply-Combine Pattern", "Rolling Averages", "Descriptive Correlation Matrix"],
                    "code": "import pandas as pd\ndf['rolling_avg'] = df['revenue'].rolling(window=7).mean()\nprint(df.describe())",
                    "output": "Calculated 7-day rolling metrics"
                }
            ]
        },
        {
            "title": "Module 4: Statistics, Visualization & Power BI",
            "description": "Statistical probability, Matplotlib, Seaborn, Power BI, Power Query, and DAX modeling.",
            "difficulty": "Intermediate",
            "estimated_hours": 30,
            "topics": [
                {
                    "title": "Statistics and probability fundamentals",
                    "subtopics": ["Measures of Central Tendency (Mean, Median, Mode)", "Measures of Dispersion (Variance, Standard Deviation, IQR)", "Normal Distribution & Central Limit Theorem", "Hypothesis Testing (p-values, t-test, Chi-square)", "Correlation vs Causation & Regression Basics"],
                    "terms": ["Central Limit Theorem", "P-Value Significance", "Pearson Correlation Coefficient"],
                    "code": "from scipy import stats\nimport numpy as np\na = [80, 85, 88, 92, 95]\nb = [70, 72, 75, 78, 80]\nt_stat, p_val = stats.ttest_ind(a, b)\nprint(f\"p-value: {p_val:.4f}\")",
                    "output": "p-value: 0.0032 (Statistically Significant)"
                },
                {
                    "title": "Matplotlib and data visualization",
                    "subtopics": ["Line, Bar, Scatter, and Histogram plots", "Seaborn Heatmaps and Distribution plots", "Customizing themes, palettes, and annotations", "Subplots and multi-panel figures", "Visual Storytelling Principles"],
                    "terms": ["Color Theory in Visualization", "Chart Junk Elimination", "Data-Ink Ratio"],
                    "code": "import matplotlib.pyplot as plt\nimport seaborn as sns\nsns.set_theme(style='darkgrid')\nplt.figure(figsize=(10, 5))\nplt.title('Monthly Growth Trends')\nplt.show()",
                    "output": "Chart rendered successfully"
                },
                {
                    "title": "Power BI, Power Query and DAX",
                    "subtopics": ["Power Query M language data transformations", "Star Schema vs Snowflake Data Modeling", "Calculated Columns vs DAX Measures", "Time Intelligence DAX (YTD, QTD, SAMEPERIODLASTYEAR)", "Row-Level Security (RLS) in Power BI"],
                    "terms": ["DAX Evaluation Context (Row vs Filter)", "Star Schema Fact & Dimension", "CALCULATE Function"],
                    "code": "Total Sales YTD = CALCULATE(SUM(Sales[Amount]), DATESYTD(DimDate[Date]))",
                    "output": "DAX Measure defined"
                },
                {
                    "title": "Dashboard development and reporting",
                    "subtopics": ["Interactive Dashboard UX & Visual Hierarchy", "Cross-filtering, Bookmarks, and Drill-throughs", "KPI Cards and Gauge Visualizations", "Publishing to Power BI Service & Scheduled Refresh", "Automated Email Reports & Subscriptions"],
                    "terms": ["Drill-Through Action", "Executive KPI Tile", "Scheduled Dataset Refresh"],
                    "code": "// Interactive Power BI Dashboard Matrix\nExecutive Overview -> Regional Drilldown -> Customer Cohort Analysis",
                    "output": "Interactive Executive Dashboard Deployed"
                }
            ]
        },
        {
            "title": "Module 5: Business Storytelling, Case Studies & Capstone",
            "description": "Business acumen, storytelling with data, real-world datasets, and interview portfolio preparation.",
            "difficulty": "Advanced",
            "estimated_hours": 20,
            "topics": [
                {
                    "title": "Business analysis and data storytelling",
                    "subtopics": ["Translating Business Metrics (CAC, LTV, Churn, ROI)", "Structuring Executive Presentations (Pyramid Principle)", "Root Cause Analysis (5 Whys Framework)", "Actionable Recommendations & ROI Projections"],
                    "terms": ["Customer Acquisition Cost (CAC)", "Customer Lifetime Value (CLV)", "Pyramid Principle"],
                    "code": "# Business ROI Model\nLTV = ARPU * Gross_Margin / Churn_Rate\nprint(f\"LTV: ${LTV:,.2f}\")",
                    "output": "LTV: $4,850.00"
                },
                {
                    "title": "Real-world datasets and case studies",
                    "subtopics": ["E-Commerce Customer Retention & Churn Analysis", "Fintech Fraud Detection & Loan Default Modeling", "Healthcare Patient Readmission Analytics", "SaaS Cohort Analysis & Retention Heatmaps"],
                    "terms": ["Cohort Retention Rate", "Anomaly Detection", "Risk Scoring Matrix"],
                    "code": "# Cohort Retention Calculation\ncohort_matrix = df.groupby(['CohortMonth', 'CohortIndex'])['UserID'].nunique().unstack()",
                    "output": "Generated cohort retention matrix"
                },
                {
                    "title": "Portfolio projects and interview preparation",
                    "subtopics": ["Building an End-to-End Data Portfolio (GitHub + Tableau/Power BI)", "Technical SQL Interview Screen Challenges (Window funcs, LeetCode SQL 50)", "Explaining Business Impact in Interviews (STAR Method)", "Resume Tailoring for Business Analyst & Data Analyst Roles"],
                    "terms": ["Portfolio Case Study Writeup", "Live SQL Screen", "STAR Technique"],
                    "code": "// Portfolio Project: Nexora AI Analytics\nIngest 1M records -> PostgreSQL -> Pandas -> Power BI Executive Dashboard",
                    "output": "Interview portfolio live and verifiable"
                }
            ]
        }
    ]
}

ALL_CAREER_SPECS = [JAVA_PATH_SPEC, PYTHON_PATH_SPEC, DATA_ANALYSIS_PATH_SPEC]

async def seed_career_roadmaps(db: AsyncSession):
    """
    Seeds the three master career paths with complete modules, topics, subtopics,
    and all 17-item comprehensive learning contents in PostgreSQL.
    """
    for spec in ALL_CAREER_SPECS:
        # Check if path already exists
        result = await db.execute(select(CareerPath).filter_by(slug=spec["slug"]))
        path = result.scalars().first()
        
        if not path:
            path = CareerPath(
                slug=spec["slug"],
                title=spec["title"],
                description=spec["description"],
                icon=spec["icon"],
                estimated_weeks=spec["estimated_weeks"],
                total_hours=spec["total_hours"],
                is_custom=False
            )
            db.add(path)
            await db.flush()
        else:
            path.title = spec["title"]
            path.description = spec["description"]
            path.estimated_weeks = spec["estimated_weeks"]
            path.total_hours = spec["total_hours"]

        # Process modules
        for mod_idx, mod_spec in enumerate(spec["modules"]):
            mod_result = await db.execute(
                select(CareerModule).filter_by(career_path_id=path.id, title=mod_spec["title"])
            )
            module = mod_result.scalars().first()
            if not module:
                module = CareerModule(
                    career_path_id=path.id,
                    title=mod_spec["title"],
                    description=mod_spec["description"],
                    order_index=mod_idx,
                    difficulty_level=mod_spec["difficulty"],
                    estimated_hours=mod_spec["estimated_hours"]
                )
                db.add(module)
                await db.flush()

            # Process topics
            primary_lang = "Java" if "Java" in spec["title"] else ("Python" if "Python" in spec["title"] else "Python/SQL")
            for top_idx, top_spec in enumerate(mod_spec["topics"]):
                topic_title = top_spec["title"]
                slug = topic_title.lower().replace(" ", "-").replace(",", "").replace("/", "-")[:80]
                
                top_result = await db.execute(
                    select(CareerTopic).filter_by(career_module_id=module.id, title=topic_title)
                )
                topic = top_result.scalars().first()
                if not topic:
                    topic = CareerTopic(
                        career_module_id=module.id,
                        title=topic_title,
                        slug=slug,
                        summary=f"In-depth mastery of {topic_title} with theory, code, and interview preparation.",
                        order_index=top_idx,
                        prerequisites=["Foundational logic", "Terminal basics"],
                        estimated_minutes=120 if mod_spec["difficulty"] == "Advanced" else 90,
                        level=mod_spec["difficulty"]
                    )
                    db.add(topic)
                    await db.flush()

                # Process subtopics
                for sub_idx, sub_title in enumerate(top_spec.get("subtopics", [])):
                    sub_res = await db.execute(
                        select(CareerSubtopic).filter_by(career_topic_id=topic.id, title=sub_title)
                    )
                    if not sub_res.scalars().first():
                        subtopic = CareerSubtopic(
                            career_topic_id=topic.id,
                            title=sub_title,
                            order_index=sub_idx,
                            content_summary=f"Key technical concepts, memory model, and production application of {sub_title}."
                        )
                        db.add(subtopic)

                # Process full 17-item learning content
                content_res = await db.execute(
                    select(TopicLearningContent).filter_by(career_topic_id=topic.id)
                )
                existing_content = content_res.scalars().first()
                
                content_payload = build_topic_content(
                    topic_name=topic_title,
                    module_name=mod_spec["title"],
                    career_name=spec["title"],
                    level=mod_spec["difficulty"],
                    primary_language=primary_lang,
                    key_terms=top_spec.get("terms", ["Abstraction", "Concurrency", "Polymorphism"]),
                    code_snippet=top_spec.get("code", f"// {topic_title} Production Implementation\npublic class Solution {{}}"),
                    output_snippet=top_spec.get("output", "Execution successful")
                )

                if not existing_content:
                    learning_content = TopicLearningContent(
                        career_topic_id=topic.id,
                        **content_payload
                    )
                    db.add(learning_content)
                else:
                    # Update fields
                    for k, v in content_payload.items():
                        setattr(existing_content, k, v)

    await db.commit()
    print("All 3 career paths seeded with 17-item topic learning contents successfully!")
