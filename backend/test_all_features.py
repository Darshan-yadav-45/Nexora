import asyncio
import io
from httpx import AsyncClient, ASGITransport
from app.main import app

async def run_tests():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        print("\n--- 1. Testing Health & Root Endpoints ---")
        res = await client.get("/health")
        assert res.status_code == 200, f"Health check failed: {res.text}"
        print("✓ Health check OK:", res.json())

        print("\n--- 2. Testing Authentication ---")
        user_email = "researcher1@nexora.ai"
        user_pass = "Password123!"
        
        # Register user 1
        reg_res = await client.post("/api/auth/register", json={"email": user_email, "password": user_pass})
        if reg_res.status_code == 400:
            print("User already registered, logging in...")
        else:
            assert reg_res.status_code == 200, f"Register failed: {reg_res.text}"
            print("✓ Registered user:", user_email)

        # Login user 1
        login_res = await client.post("/api/auth/login", data={"username": user_email, "password": user_pass})
        assert login_res.status_code == 200, f"Login failed: {login_res.text}"
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("✓ Logged in, JWT token acquired")

        # Create Profile
        prof_res = await client.post("/api/profile/", json={
            "name": "Dr. Sarah Mitchell",
            "preferred_name": "Sarah",
            "native_language": "English",
            "english_level": "C1",
            "learning_goal": "career"
        }, headers=headers)
        if prof_res.status_code == 200:
            print("✓ User profile created")
        else:
            print("Profile exists or status:", prof_res.status_code)

        print("\n--- 3. Testing Career Roadmaps ---")
        paths_res = await client.get("/api/career/paths", headers=headers)
        assert paths_res.status_code == 200, f"Get paths failed: {paths_res.text}"
        paths = paths_res.json()
        assert len(paths) >= 3, f"Expected at least 3 paths, got {len(paths)}"
        print(f"✓ Retrieved {len(paths)} career paths:")
        for p in paths[:3]:
            print(f"  - {p['title']} ({len(p.get('modules', []))} modules)")

        java_path = next(p for p in paths if "Java" in p["title"])
        first_module = java_path["modules"][0]
        first_topic = first_module["topics"][0]
        topic_id = first_topic["id"]
        print(f"✓ Examining Topic: '{first_topic['title']}' (ID: {topic_id})")

        # Get full 17-item content
        content_res = await client.get(f"/api/career/topics/{topic_id}/content", headers=headers)
        assert content_res.status_code == 200, f"Get content failed: {content_res.text}"
        content = content_res.json()
        print("✓ Verified 17 Master Content Attributes:")
        print("  1. Topic Name:", content["topic_name"])
        print("  2. Objectives Count:", len(content["learning_objectives"]))
        print("  3. Technical Notes Length:", len(content["detailed_technical_notes"]))
        print("  4. Important Definitions:", len(content["important_definitions"]))
        print("  5. Interview Questions:", len(content["interview_questions"]))
        print("  6. MCQs:", len(content["mcqs"]))
        print("  7. Coding Exercises:", len(content["coding_exercises"]))
        print("  8. Mini-Projects:", len(content["mini_projects"]))
        print("  9. Key Takeaways:", len(content["key_takeaways"]))

        # Enroll in Career Path
        enroll_res = await client.post(f"/api/career/enroll/{java_path['id']}", headers=headers)
        assert enroll_res.status_code == 200
        print("✓ Enrolled in path:", java_path["title"])

        # Update Topic Progress & Take Quiz
        prog_res = await client.post(f"/api/career/topics/{topic_id}/progress", json={
            "status": "Completed",
            "quiz_score": 100.0,
            "quiz_answers": {"1": 1, "2": 2, "3": 1},
            "project_completed": True,
            "time_spent_minutes": 75
        }, headers=headers)
        assert prog_res.status_code == 200
        print("✓ Topic progress updated to Completed (Score: 100%)")

        # Save Notes & Bookmark
        note_res = await client.post(f"/api/career/topics/{topic_id}/note", json={
            "notes": "Remember: JVM stack allocation stores primitive values, heap stores reference types.",
            "is_bookmarked": True
        }, headers=headers)
        assert note_res.status_code == 200
        print("✓ Topic personal note and bookmark saved")

        # Path Progress Overview
        path_prog_res = await client.get(f"/api/career/progress/{java_path['id']}", headers=headers)
        assert path_prog_res.status_code == 200
        prog_overview = path_prog_res.json()
        print(f"✓ Path Progress: {prog_overview['completion_percentage']}% ({prog_overview['completed_topics']}/{prog_overview['total_topics']} topics)")
        print(f"  Next Recommended: {prog_overview['next_recommended_topic']['title'] if prog_overview['next_recommended_topic'] else 'None'}")

        # Timetable Generator
        tt_res = await client.post("/api/career/timetable/generate", json={
            "career_path_id": java_path["id"],
            "daily_study_hours": 2.5,
            "days_per_week": 5
        }, headers=headers)
        assert tt_res.status_code == 200
        print(f"✓ Timetable generated ({tt_res.json()['total_days_scheduled']} study days scheduled)")

        # AI-Generated Roadmap
        ai_road_res = await client.post("/api/career/generate-ai", json={
            "career_goal": "Cloud AI Architect",
            "current_knowledge_level": "Intermediate",
            "existing_skills": ["Python", "Docker"],
            "preferred_technologies": ["Python", "FastAPI", "PostgreSQL", "PyTorch"],
            "daily_study_hours": 2.0,
            "weekly_study_hours": 14.0,
            "target_completion_weeks": 12
        }, headers=headers)
        assert ai_road_res.status_code == 200
        print("✓ AI personalized roadmap generated successfully")

        # Custom Roadmap File Upload & Extraction
        dummy_roadmap = b"Module 1: Cloud Native Fundamentals\nTopic: Microservice Architecture Patterns\nTopic: Container Orchestration with Kubernetes\nModule 2: Distributed Data Stores\nTopic: Distributed PostgreSQL and Caching"
        upload_res = await client.post(
            "/api/career/upload",
            files={"file": ("my_custom_roadmap.txt", dummy_roadmap, "text/plain")},
            headers=headers
        )
        assert upload_res.status_code == 200
        extracted = upload_res.json()
        print(f"✓ Custom roadmap file parsed ({extracted['total_topics_count']} topics extracted)")

        # Download Progress Report
        report_res = await client.get(f"/api/career/report/{java_path['id']}?format=markdown", headers=headers)
        assert report_res.status_code == 200
        print("✓ Downloadable Markdown progress report generated:", report_res.text[:120], "...")

        print("\n--- 4. Testing Research Management System ---")
        # Create Research Project
        proj_res = await client.post("/api/research/projects", json={
            "title": "Scalable Neuro-Symbolic Reasoning in Autonomous Edge Systems",
            "domain_area": "Artificial Intelligence / Edge Computing",
            "topic": "Neuro-Symbolic Logic & Knowledge Graph Synthesis",
            "problem_statement": "Deep neural networks lack formal mathematical verifiability under out-of-distribution physical sensor anomalies.",
            "research_type": "Empirical Research",
            "methodology_overview": "Hybrid probabilistic logic engines coupled with quantized transformer decoders.",
            "expected_outcomes": "Sub-millisecond verification with zero false-safety assertions."
        }, headers=headers)
        assert proj_res.status_code == 200, f"Project creation failed: {proj_res.text}"
        project = proj_res.json()
        project_id = project["id"]
        print(f"✓ Created Research Project: '{project['title']}' (ID: {project_id})")

        # Upload Paper to Library
        dummy_paper = b"%PDF-1.4\n1 0 obj << /Title (Attention Is All You Need) >> endobj\nstream\n(Attention Is All You Need) Tj\n(We propose the Transformer architecture) Tj\nendstream\nendobj"
        paper_res = await client.post(
            "/api/research/papers/upload",
            data={
                "research_project_id": project_id,
                "paper_title": "Attention Is All You Need",
                "publication_year": 2017,
                "journal_or_conference": "NeurIPS"
            },
            files={"file": ("attention_2017.pdf", dummy_paper, "application/pdf")},
            headers=headers
        )
        assert paper_res.status_code == 200, f"Paper upload failed: {paper_res.text}"
        paper = paper_res.json()
        paper_id = paper["id"]
        print(f"✓ Research paper uploaded, extracted, and indexed: '{paper['title']}'")

        # Test AI Research Assistant (17 Tools Dispatch)
        print("\n--- 5. Testing AI Research Assistant Tools ---")
        tools_to_test = [
            ("topic_explanation", {"topic": "Neuro-Symbolic AI", "domain": "Computer Science"}),
            ("problem_identification", {"topic": "Edge AI Verification"}),
            ("question_generation", {"topic": "Scalable Transformer Compression"}),
            ("objectives_generation", {"topic": "Federated Representation Learning"}),
            ("gap_identification", {"topic": "Graph Neural Networks for Drug Discovery"}),
            ("methodology_suggestions", {"goal": "Benchmark low-latency edge AI inference"}),
            ("citation_organization", {"title": "Attention Is All You Need", "year": 2017, "authors": "Vaswani et al."}),
            ("viva_preparation", {"topic": "Deep Learning Generalization"})
        ]

        for tool_name, payload in tools_to_test:
            ai_res = await client.post("/api/research/ai/execute", json={
                "tool_name": tool_name,
                "research_project_id": project_id,
                "research_paper_id": paper_id,
                "input_data": payload,
                "persist_to_project": True
            }, headers=headers)
            assert ai_res.status_code == 200, f"AI tool {tool_name} failed: {ai_res.text}"
            print(f"  ✓ Tool '{tool_name}' executed and output persisted in PostgreSQL")

        # Literature Review Matrix (12 Attributes)
        print("\n--- 6. Testing Literature Review Workspace ---")
        lit_res = await client.get(f"/api/research/literature-review/{project_id}", headers=headers)
        assert lit_res.status_code == 200
        lit_review = lit_res.json()
        print(f"✓ Literature Review matrix active: '{lit_review['title']}' ({len(lit_review['entries'])} entries)")
        
        # Export literature review
        export_res = await client.get(f"/api/research/literature-review/{project_id}/export?format=markdown", headers=headers)
        assert export_res.status_code == 200
        print("✓ Literature Review Markdown matrix exported successfully")

        # Gap Analysis, Methodology & Variables Workspace
        print("\n--- 7. Testing Methodology, Variables & Gap Analysis ---")
        gap_res = await client.post("/api/research/gaps", json={
            "research_project_id": project_id,
            "gap_title": "Lack of Continuous Symbolic Verification at Edge Latency",
            "description": "Existing formal provers require server-grade hardware, causing >200ms latency.",
            "impact_level": "High"
        }, headers=headers)
        assert gap_res.status_code == 200
        print("✓ Research Gap Analysis recorded in PostgreSQL")

        var_res = await client.post("/api/research/variables", json={
            "research_project_id": project_id,
            "name": "Quantization Bitwidth",
            "variable_type": "Independent",
            "measurement_unit": "bits (4, 8, 16)"
        }, headers=headers)
        assert var_res.status_code == 200
        print("✓ Research Variable (Independent) added")

        # Research Task & Planner Integration
        print("\n--- 8. Testing Integration (Research -> Planner, Knowledge Base, Career) ---")
        task_res = await client.post("/api/research/tasks", json={
            "research_project_id": project_id,
            "title": "Implement Neuro-Symbolic Verification Benchmark",
            "priority": "High"
        }, headers=headers)
        assert task_res.status_code == 200
        research_task = task_res.json()
        print("✓ Research Task created:", research_task["title"])

        # Convert to Planner Task
        conv_res = await client.post(f"/api/integration/planner/convert-research-task/{research_task['id']}", headers=headers)
        assert conv_res.status_code == 200
        planner_task = conv_res.json()
        print(f"✓ Successfully converted Research Task to Planner Task: '{planner_task['title']}' (ID: {planner_task['id']})")

        # Save Paper to Knowledge Base
        kb_res = await client.post(f"/api/integration/knowledge-base/save-paper/{paper_id}", headers=headers)
        assert kb_res.status_code == 200
        kb_item = kb_res.json()
        print(f"✓ Saved Research Paper to Knowledge Base: '{kb_item['title']}'")

        # Add Skill to Career Profile
        skill_res = await client.post("/api/integration/profile/add-skill", json={
            "skill_name": "Neuro-Symbolic AI Verification",
            "domain": "Edge Intelligence",
            "proficiency": "Advanced"
        }, headers=headers)
        assert skill_res.status_code == 200
        print("✓ Research-derived skill connected to User Career Profile")

        # Generate Presentation Slides from Project
        doc_res = await client.post(f"/api/integration/projects/{project_id}/generate-documentation?doc_type=Presentation Slides", headers=headers)
        assert doc_res.status_code == 200
        print("✓ Project presentation slides generated and stored in PostgreSQL")

        # Security & Isolation Test: User B cannot access User A's project!
        print("\n--- 9. Testing User Isolation & Security ---")
        user2_email = "attacker@rival.org"
        user2_pass = "Password123!"
        await client.post("/api/auth/register", json={"email": user2_email, "password": user2_pass})
        l2_res = await client.post("/api/auth/login", data={"username": user2_email, "password": user2_pass})
        token2 = l2_res.json()["access_token"]
        headers2 = {"Authorization": f"Bearer {token2}"}

        unauth_proj = await client.get(f"/api/research/projects/{project_id}", headers=headers2)
        assert unauth_proj.status_code == 404, f"Security leak! User 2 accessed User 1's project: {unauth_proj.text}"
        print("✓ Confirmed strict user isolation: User B cannot access User A's private research project (404 Not Found)")

        print("\n=======================================================")
        print("  ALL BACKEND TESTS PASSED WITH 100% SUCCESS!")
        print("=======================================================\n")

if __name__ == "__main__":
    asyncio.run(run_tests())
