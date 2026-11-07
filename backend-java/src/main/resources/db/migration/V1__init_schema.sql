-- Nexora AI Flyway Initial Schema Migration

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    account_type VARCHAR(50),
    is_verified BOOLEAN DEFAULT TRUE,
    verification_token VARCHAR(255),
    reset_password_token VARCHAR(255),
    reset_token_expiry TIMESTAMP,
    profile_completed BOOLEAN DEFAULT FALSE,
    first_time_login BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- 2. User Profiles Table
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID PRIMARY KEY,
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    preferred_name VARCHAR(255),
    native_language VARCHAR(100) DEFAULT 'English',
    english_level VARCHAR(50) DEFAULT 'Intermediate',
    learning_goal VARCHAR(500),
    timezone VARCHAR(100),
    phone_number VARCHAR(50),
    date_of_birth VARCHAR(50),
    country VARCHAR(100) DEFAULT 'India',
    state VARCHAR(100),
    city VARCHAR(100),
    avatar_url VARCHAR(1000),
    profession VARCHAR(100),
    organization VARCHAR(255),
    enabled_modules JSONB DEFAULT '["study", "career", "research", "creator", "planner", "knowledge_base"]'::jsonb,
    career_skills JSONB DEFAULT '[]'::jsonb,
    research_interests JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Education Records Table
CREATE TABLE IF NOT EXISTS education_records (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    level VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Completed',
    institution_name VARCHAR(255),
    board_or_university VARCHAR(255),
    stream VARCHAR(100),
    degree_name VARCHAR(100),
    specialization VARCHAR(255),
    course_duration VARCHAR(50),
    admission_year INT,
    passing_year INT,
    expected_completion_year INT,
    current_class_or_year VARCHAR(50),
    current_semester VARCHAR(50),
    result_percentage_cgpa VARCHAR(50),
    research_title VARCHAR(500),
    research_guide VARCHAR(255),
    research_status VARCHAR(100),
    chronological_order INT DEFAULT 1,
    extra_metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_education_user ON education_records(user_id);

-- 4. User Subjects Table
CREATE TABLE IF NOT EXISTS user_subjects (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    education_record_id UUID REFERENCES education_records(id) ON DELETE SET NULL,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50),
    credits INT,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_user_subjects_user ON user_subjects(user_id);

-- 5. Syllabi Table
CREATE TABLE IF NOT EXISTS syllabi (
    id UUID PRIMARY KEY,
    user_subject_id UUID NOT NULL REFERENCES user_subjects(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    source_type VARCHAR(50) DEFAULT 'file_upload',
    file_name VARCHAR(255),
    file_path VARCHAR(500),
    content_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Research Notebooks Table
CREATE TABLE IF NOT EXISTS research_notebooks (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    domain_area VARCHAR(255),
    keywords JSONB DEFAULT '[]'::jsonb,
    category VARCHAR(100) DEFAULT 'General',
    is_pinned BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_notebooks_user ON research_notebooks(user_id);

-- 7. Social Accounts Table
CREATE TABLE IF NOT EXISTS social_accounts (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL,
    platform_user_id VARCHAR(255),
    username VARCHAR(255),
    profile_url VARCHAR(1000) NOT NULL,
    display_name VARCHAR(255),
    avatar_url VARCHAR(1000),
    connection_type VARCHAR(50) DEFAULT 'profile_link',
    is_connected BOOLEAN DEFAULT FALSE,
    show_on_public_profile BOOLEAN DEFAULT TRUE,
    public_repos JSONB DEFAULT '[]'::jsonb,
    platform_metadata JSONB DEFAULT '{}'::jsonb,
    encrypted_token TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_social_accounts_user ON social_accounts(user_id);
