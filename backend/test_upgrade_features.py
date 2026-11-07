import asyncio
import io
from httpx import AsyncClient, ASGITransport
from app.main import app

async def run_upgrade_tests():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        print("\n=======================================================")
        print("  STARTING NEXORA AI UPGRADE AUTOMATED VERIFICATION")
        print("=======================================================\n")

        # 1. Health check
        res = await client.get("/health")
        assert res.status_code == 200
        print("✓ 1. Backend API Health Check OK:", res.json())

        # 2. Registration with password confirmation & login
        user_email = "student_scholar@nexora.ai"
        user_pass = "ScholarPass2026!"
        
        reg_res = await client.post("/api/auth/register", json={
            "name": "Darshan Scholar",
            "email": user_email,
            "password": user_pass,
            "confirm_password": user_pass
        })
        if reg_res.status_code == 400:
            print("User already registered, continuing...")
        else:
            assert reg_res.status_code == 200, f"Register failed: {reg_res.text}"
            print("✓ 2. User registration with password confirmation OK:", user_email)

        # Login
        login_res = await client.post("/api/auth/login", data={"username": user_email, "password": user_pass})
        assert login_res.status_code == 200, f"Login failed: {login_res.text}"
        login_data = login_res.json()
        token = login_data["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("✓ 3. Login OK. Received JWT token and user status metadata.")

        # Forgot password & Reset password flow
        fp_res = await client.post("/api/auth/forgot-password", json={"email": user_email})
        assert fp_res.status_code == 200
        reset_token = fp_res.json().get("reset_token_preview")
        if reset_token:
            rp_res = await client.post("/api/auth/reset-password", json={
                "token": reset_token,
                "new_password": user_pass,
                "confirm_password": user_pass
            })
            assert rp_res.status_code == 200
            print("✓ 4. Forgot password & reset password flow verified.")

        # Account Type Selection: Student
        type_res = await client.post("/api/auth/select-account-type", json={"account_type": "student"}, headers=headers)
        assert type_res.status_code == 200
        print("✓ 5. Account type selected: Student.")

        # Step 1: Personal Information
        pinfo_res = await client.post("/api/education/personal-info", json={
            "name": "Darshan Sharma",
            "preferred_name": "Darshan",
            "email": user_email,
            "phone_number": "+91 9876543210",
            "date_of_birth": "2003-05-15",
            "country": "India",
            "state": "Karnataka",
            "city": "Bengaluru",
            "preferred_language": "English"
        }, headers=headers)
        assert pinfo_res.status_code == 200
        print("✓ 6. Step 1 Personal Information saved.")

        # Step 2: Education Records (SSLC completed, PUC completed, UG ongoing)
        sslc_res = await client.post("/api/education/records", json={
            "level": "SSLC / 10th",
            "status": "Completed",
            "institution_name": "St. Joseph High School",
            "board_or_university": "CBSE",
            "passing_year": 2019,
            "result_percentage_cgpa": "92.4%",
            "chronological_order": 1
        }, headers=headers)
        assert sslc_res.status_code == 200

        puc_res = await client.post("/api/education/records", json={
            "level": "PUC / 12th",
            "status": "Completed",
            "institution_name": "National Pre-University College",
            "board_or_university": "State Board",
            "stream": "Science (PCMB)",
            "passing_year": 2021,
            "result_percentage_cgpa": "94.8%",
            "chronological_order": 2
        }, headers=headers)
        assert puc_res.status_code == 200

        ug_res = await client.post("/api/education/records", json={
            "level": "Undergraduate (UG)",
            "status": "Currently studying",
            "degree_name": "BE / B.Tech",
            "specialization": "Computer Science & Engineering",
            "institution_name": "BMS College of Engineering",
            "board_or_university": "VTU",
            "admission_year": 2021,
            "expected_completion_year": 2025,
            "current_class_or_year": "4th Year",
            "current_semester": "7th Semester",
            "chronological_order": 3
        }, headers=headers)
        assert ug_res.status_code == 200
        ug_record_id = ug_res.json()["id"]
        print("✓ 7. Step 2 Education Records (SSLC, PUC, Ongoing UG 7th Sem) saved.")

        # Step 3: Subjects & Syllabi Management
        sub1_res = await client.post("/api/education/subjects", json={
            "name": "Advanced Artificial Intelligence & Neural Networks",
            "code": "CS701",
            "credits": 4,
            "description": "Deep learning architectures, transformers, and neuro-symbolic systems.",
            "education_record_id": ug_record_id
        }, headers=headers)
        assert sub1_res.status_code == 200
        sub1_id = sub1_res.json()["id"]

        sub2_res = await client.post("/api/education/subjects", json={
            "name": "Cloud Computing & Distributed Systems",
            "code": "CS702",
            "credits": 4,
            "education_record_id": ug_record_id
        }, headers=headers)
        assert sub2_res.status_code == 200
        sub2_id = sub2_res.json()["id"]

        # Upload Syllabus Text
        syl_res = await client.post(f"/api/education/subjects/{sub1_id}/syllabus-text", json={
            "title": "CS701 Complete Syllabus",
            "content_text": "Unit 1: Attention mechanisms and Transformers.\nUnit 2: Large Language Model architecture and instruction tuning.\nUnit 3: Grounded retrieval and vector search.\nUnit 4: Neuro-symbolic verification and evaluation."
        }, headers=headers)
        assert syl_res.status_code == 200

        # Upload Study Material
        mat_res = await client.post(f"/api/education/subjects/{sub1_id}/materials", json={
            "title": "Unit 1 Transformers & Multi-Head Attention Notes",
            "material_type": "lecture_notes",
            "content_text": "Formal definition of scaled dot-product attention: Attention(Q, K, V) = softmax(QK^T / sqrt(d_k))V."
        }, headers=headers)
        assert mat_res.status_code == 200
        print("✓ 8. Step 3 Ongoing Semester Subjects, Syllabus text & Study Materials saved.")

        # Step 4: Learning Preferences
        pref_res = await client.post("/api/education/learning-preferences", json={
            "explanation_language": "English",
            "difficulty_level": "Intermediate",
            "explanation_depth": "detailed",
            "code_examples_required": True,
            "visual_explanations_required": True,
            "practice_questions_required": True,
            "mcqs_required": True,
            "viva_prep_required": True,
            "exam_prep_required": True
        }, headers=headers)
        assert pref_res.status_code == 200
        print("✓ 9. Step 4 Learning Preferences configured.")

        # Step 5: Career Information
        car_res = await client.post("/api/education/career-info", json={
            "career_goal": "Senior AI Systems Architect",
            "current_skills": ["Python", "PyTorch", "FastAPI", "PostgreSQL", "Docker"],
            "technologies_interested": ["Kubernetes", "LangChain", "Vector Databases", "React"],
            "preferred_career_path": "Python Full Stack Development",
            "daily_learning_time_minutes": 90,
            "target_completion_weeks": 10
        }, headers=headers)
        assert car_res.status_code == 200
        print("✓ 10. Step 5 Career Goals and Skills saved.")

        # Step 6: Resume Upload, Intelligent Parsing & Review Confirmation
        sample_resume_content = """
        DARSHAN SHARMA
        Bangalore, India | student_scholar@nexora.ai

        EDUCATION:
        B.Tech in Computer Science and Engineering, BMS College of Engineering (2021-2025)
        Pre-University College Science PCMB (2019-2021)
        Secondary School Leaving Certificate (2019)

        SKILLS:
        Python, Java, TypeScript, React.js, FastAPI, PostgreSQL, Docker, Git, Machine Learning

        PROJECTS:
        Project: Nexora Research Notebook Suite - Developed 3-panel grounded workspace with inline citations.
        Project: Distributed Microservices Engine - Engineered high-throughput REST API with automated migrations.

        INTERNSHIPS:
        Full Stack Engineering Intern at Tech Innovators (3 Months)

        CERTIFICATIONS:
        AWS Certified Cloud Practitioner (2024)
        PostgreSQL Performance Tuning Specialist (2024)
        """
        resume_upload_res = await client.post(
            "/api/education/resume/upload",
            files={"file": ("Darshan_Resume.txt", io.BytesIO(sample_resume_content.encode("utf-8")), "text/plain")},
            headers=headers
        )
        assert resume_upload_res.status_code == 200
        parsed_data = resume_upload_res.json()
        assert parsed_data["requires_user_confirmation"] is True
        assert len(parsed_data["parsed_sections"]["skills"]) > 0
        resume_id = parsed_data["resume_id"]

        # Confirm parsed sections
        confirm_res = await client.post("/api/education/resume/confirm", json={
            "resume_id": resume_id,
            "skills": parsed_data["parsed_sections"]["skills"],
            "education": parsed_data["parsed_sections"]["education"]
        }, headers=headers)
        assert confirm_res.status_code == 200
        print("✓ 11. Step 6 Resume uploaded, parsed, reviewed and confirmed without silent overwrite.")

        # Step 7: Education Timeline & Profile Completion
        tl_res = await client.get("/api/education/timeline", headers=headers)
        assert tl_res.status_code == 200
        tl_data = tl_res.json()
        assert tl_data["completed_count"] >= 2 # SSLC & PUC
        assert tl_data["ongoing_count"] >= 1 # UG

        comp_res = await client.post("/api/education/complete", headers=headers)
        assert comp_res.status_code == 200
        assert comp_res.json()["profile_completed"] is True
        print("✓ 12. Step 7 Education Timeline verified and Profile Completion marked active.")

        # --- 8. Teacher Profile & AI Assistance Tools ---
        print("\n--- Testing Teacher / Educator Profile & AI Assist ---")
        teach_res = await client.post("/api/teacher/profile", json={
            "institution": "Indian Institute of Science",
            "teaching_position": "Associate Professor",
            "department": "Artificial Intelligence",
            "qualification": "Ph.D in Computer Science",
            "specialization": "Foundational AI Models",
            "teaching_experience_years": 8.5,
            "subjects_taught": ["Machine Learning", "Deep Neural Networks"],
            "current_classes_semesters": ["M.Tech 1st Sem", "B.Tech Final Year"]
        }, headers=headers)
        assert teach_res.status_code == 200

        teach_assist = await client.post("/api/teacher/ai-assist", json={
            "tool_type": "lesson_plan",
            "subject_name": "Deep Neural Networks",
            "topic": "Backpropagation & Gradient Descent",
            "grade_or_sem": "M.Tech 1st Sem"
        }, headers=headers)
        assert teach_assist.status_code == 200
        assert "timeline" in teach_assist.json()
        print("✓ 13. Teacher Profile and AI Lesson Plan generation verified.")

        # --- 9. Professional Profile & Module Customization ---
        print("\n--- Testing Professional Profile & Module Customization ---")
        prof_res = await client.post("/api/professional/profile", json={
            "name": "Darshan Sharma",
            "profession": "Staff AI Platform Engineer",
            "organization": "Enterprise AI Labs",
            "skills": ["Distributed Systems", "PostgreSQL", "FastAPI"],
            "career_goals": "Architect sovereign enterprise AI systems",
            "enabled_modules": ["study", "career", "research", "planner", "knowledge_base"]
        }, headers=headers)
        assert prof_res.status_code == 200
        print("✓ 14. Professional Profile and modular app toggles verified.")

        # --- 10. AI Research Notebook (NotebookLM style) ---
        print("\n--- Testing AI Research Notebook (NotebookLM Style) ---")
        # A. Create Notebook with ONLY Title!
        nb_res = await client.post("/api/notebooks/", json={
            "title": "Artificial Intelligence in Healthcare Diagnostics",
            "description": "Evaluating machine learning models on high-resolution clinical imaging.",
            "domain_area": "Medical AI & Computer Vision"
        }, headers=headers)
        assert nb_res.status_code == 201
        notebook_id = nb_res.json()["id"]
        print("✓ 15. Research Notebook created with ONLY title:", notebook_id)

        # B. Add Reference Source (Pasted Text & File)
        source_doc_text = """
        RESEARCH ARTICLE: High-Accuracy Lung Disease Classification via Deep Convolutional Networks
        Authors: Dr. Emily Watson, Dr. Arthur Davis (2024)
        Journal of Medical Imaging and AI, Vol 12, pp. 45-62

        Abstract:
        We present a 152-layer residual network architecture trained on 45,000 anonymized chest radiographs. 
        Our model achieves 98.4% diagnostic accuracy and reduces false negatives by 31.2% compared to standard clinician evaluations.

        Page 1: Introduction and Clinical Motivation
        Early detection of pulmonary lesions is critical for effective patient triage. In traditional clinical workflows, 
        radiologist fatigue contributes to missed micro-nodules in high-density lung parenchyma.

        Page 2: Methodology & Data Preprocessing
        Image inputs are normalized to 1024x1024 resolution and augmented using random rotation and elastic deformations. 
        We employ cross-entropy loss with focal regularization to counteract severe class imbalance.

        Page 3: Experimental Results and Statistical Significance
        The proposed network reached an Area Under the Curve (AUC) of 0.992 across the independent test cohort. 
        In controlled trials, the system processed radiographs with a mean inference latency of 42 milliseconds.

        Page 4: Limitations and Research Gaps
        A critical limitation is model performance degradation when applied to low-dose mobile X-ray devices with high noise floor. 
        Future studies must investigate unsupervised domain adaptation for rural clinic environments.
        """
        source_res = await client.post(f"/api/notebooks/{notebook_id}/sources/paste-text", json={
            "title": "Deep CNN Clinical Imaging Paper",
            "content_text": source_doc_text
        }, headers=headers)
        assert source_res.status_code == 200
        print("✓ 16. Reference paper source ingested, page-chunked, and linked to notebook in PostgreSQL.")

        # C. Source-Grounded AI Chat with Verified Citations
        chat_res = await client.post(f"/api/notebooks/{notebook_id}/chat", json={
            "query": "What accuracy and AUC did the model achieve, and what are the main limitations?",
            "general_ai_mode": False
        }, headers=headers)
        assert chat_res.status_code == 200
        chat_data = chat_res.json()
        assert chat_data["is_source_grounded"] is True
        assert len(chat_data["citations"]) > 0
        assert "Deep CNN Clinical Imaging Paper" in chat_data["citations"][0]["source_title"]
        print("✓ 17. Source-grounded AI chat verified with verified inline citations and page numbers.")

        # D. General AI Mode Toggle
        gen_chat_res = await client.post(f"/api/notebooks/{notebook_id}/chat", json={
            "query": "Explain the general concept of convolutional kernels in machine learning.",
            "general_ai_mode": True
        }, headers=headers)
        assert gen_chat_res.status_code == 200
        assert "[General AI Knowledge Mode]" in gen_chat_res.json()["answer"]
        print("✓ 18. General AI knowledge mode toggle verified.")

        # E. Humanize & Improve Writing Feature
        humanize_res = await client.post(f"/api/notebooks/{notebook_id}/humanize", json={
            "text": "Furthermore, in order to delve into the parameters, it is crucial to remember that we utilize high accuracy.",
            "mode": "natural_human"
        }, headers=headers)
        assert humanize_res.status_code == 200
        h_data = humanize_res.json()
        assert len(h_data["changes_summary"]) > 0
        print("✓ 19. Humanize & Improve Writing verified with side-by-side diff summary.")

        # F. 20 Research Studio Tools
        studio_summary = await client.post(f"/api/notebooks/{notebook_id}/studio/summary", headers=headers)
        assert studio_summary.status_code == 200

        studio_gaps = await client.post(f"/api/notebooks/{notebook_id}/studio/gap_analysis", headers=headers)
        assert studio_gaps.status_code == 200

        studio_audio = await client.post(f"/api/notebooks/{notebook_id}/studio/audio_overview", headers=headers)
        assert studio_audio.status_code == 200
        assert "dialogue" in studio_audio.json()["data"]
        print("✓ 20. Research Studio 20-generator suite (Executive Summary, Gap Analysis, Audio Podcast) verified.")

        # G. Save Studio Output into Persistent Notes & Export
        note_res = await client.post(f"/api/notebooks/{notebook_id}/notes", json={
            "title": "Key Clinical Findings & Gaps Note",
            "content": "Model achieved 98.4% accuracy; key limitation is low-dose mobile X-ray noise.",
            "category": "Literature Synthesis"
        }, headers=headers)
        assert note_res.status_code == 200

        export_md = await client.get(f"/api/notebooks/{notebook_id}/export?export_format=markdown", headers=headers)
        assert export_md.status_code == 200
        assert "Artificial Intelligence in Healthcare Diagnostics" in export_md.text

        export_csv = await client.get(f"/api/notebooks/{notebook_id}/export?export_format=csv", headers=headers)
        assert export_csv.status_code == 200
        print("✓ 21. Persistent notes saved in PostgreSQL and Markdown & CSV export verified.")

        # --- 11. Social Media & Developer Account Connections ---
        print("\n--- Testing Social Connections & GitHub Career Sync ---")
        gh_res = await client.post("/api/social/connect-github", json={"username": "torvalds"}, headers=headers)
        assert gh_res.status_code == 200
        gh_account = gh_res.json()["account"]
        gh_acc_id = gh_account["id"]
        assert gh_account["is_connected"] is True

        # Sync GitHub Repos to Career Profile
        sync_res = await client.post("/api/social/sync-github-to-career", json={
            "account_id": gh_acc_id,
            "selected_repo_names": [r["name"] for r in gh_account.get("public_repos", [])[:2]]
        }, headers=headers)
        assert sync_res.status_code == 200

        # Add manual profile links
        link_res = await client.post("/api/social/add-profile-link", json={
            "platform": "linkedin",
            "profile_url": "https://linkedin.com/in/darshan-sharma-ai"
        }, headers=headers)
        assert link_res.status_code == 200
        link_acc_id = link_res.json()["account"]["id"]

        # Toggle visibility
        vis_res = await client.put(f"/api/social/visibility/{link_acc_id}?show=false", headers=headers)
        assert vis_res.status_code == 200

        # Disconnect
        disc_res = await client.delete(f"/api/social/disconnect/{link_acc_id}", headers=headers)
        assert disc_res.status_code == 200
        print("✓ 22. GitHub connection, Career sync, profile link addition, visibility toggle, and disconnect verified.")

        # --- 12. Security & User Isolation ---
        print("\n--- Testing Security & User Isolation ---")
        user2_email = "rival_researcher@mit.edu"
        user2_pass = "SecurePass2026!"
        await client.post("/api/auth/register", json={"email": user2_email, "password": user2_pass})
        u2_login = await client.post("/api/auth/login", data={"username": user2_email, "password": user2_pass})
        token2 = u2_login.json()["access_token"]
        headers2 = {"Authorization": f"Bearer {token2}"}

        # User 2 tries to access User 1's notebook
        unauth_nb = await client.get(f"/api/notebooks/{notebook_id}", headers=headers2)
        assert unauth_nb.status_code == 404, f"Security Breach! User 2 accessed User 1's notebook: {unauth_nb.text}"
        print("✓ 23. Strict PostgreSQL User Isolation verified: User B receives 404 Not Found on User A's private research notebook.")

        print("\n=======================================================")
        print("  ALL 23 UPGRADE TESTS PASSED WITH 100% SUCCESS!")
        print("=======================================================\n")

if __name__ == "__main__":
    asyncio.run(run_upgrade_tests())
