# Mentoraa Frontend Blueprint

## Product Positioning

Mentoraa is an AI-powered career progression operating system for students and early professionals.

Core journey:

assessment -> roadmap -> skills -> projects -> resume -> internships/jobs

Do not design it like a generic quiz site, LinkedIn clone, blog, or social feed.

## Working Backend Features

### Authentication

- Register
- Login/logout
- Email OTP verification
- Google OAuth configuration support
- User profile with avatar, headline, bio, interests, target role

### Career Assessment

- Basic career assessment
- Advanced assessment
- Career prediction result
- Match score, confidence, advanced score
- Saved assessment history
- Learning resources shown on result page

### Roadmap

- Auto-generated after assessment result is saved
- 3-month roadmap
- Monthly focus areas
- Weekly tasks
- Task types: learning, project, certification, internship prep, resume
- Completion checkbox/toggle
- Roadmap progress percentage

Routes:

- `/roadmap/`
- `/roadmap/tasks/<id>/toggle/`

### Skill Gap

- Auto-generated after assessment result is saved
- Target role requirements
- Missing skills
- Readiness percentage
- Priority ranking
- Improvement suggestions

Route:

- `/skills/`

### Resume Builder

- Resume profile
- Education items
- Experience items
- Resume preview
- DOCX export
- PDF export

Routes:

- `/builder/resume/`
- `/builder/resume/preview/`
- `/builder/resume/download/docx/`
- `/builder/resume/download/pdf/`
- `/builder/resume/education/add/`
- `/builder/resume/experience/add/`

### Resume Analyzer

- PDF upload
- DOCX upload
- Extracted resume text
- ATS score
- Matched role keywords
- Missing role keywords
- Weak bullet detection
- Formatting issue detection
- Improvement suggestions
- Score history

Route:

- `/resumes/analyzer/`

### Analytics Dashboard

- Roadmap progress
- Skill readiness
- Latest resume score
- Resume score change
- Current incomplete roadmap tasks

Route:

- `/dashboard/`

### AI-Ready Foundations

- AI provider abstraction for OpenAI and Claude
- Context builder includes target role, assessment match, roadmap progress, skill gaps, resume score
- Mentor conversation/message storage
- Mock interview models
- Job matching models
- Portfolio project models
- Subscription models
- Role community/project showcase models

## Recommended Frontend Information Architecture

Primary navigation:

- Dashboard
- Assessment
- Roadmap
- Skills
- Resume
- Jobs
- Mentor
- Profile

Mobile bottom navigation:

- Dashboard
- Roadmap
- Skills
- Resume
- Profile

## Key Screens

### 1. Dashboard

Purpose: command center.

Show:

- Career target card
- Roadmap progress ring/bar
- Skill readiness bar
- Resume ATS score
- Weekly tasks
- Suggested next action
- Quick actions: Continue Roadmap, Analyze Resume, Update Skills, Build Resume

UX:

- Dense but calm
- Use progress widgets, not marketing cards
- Always show one clear next action

### 2. Assessment Flow

Purpose: capture signal.

Show:

- Step indicator
- One question group at a time on mobile
- Progress state
- Result page with career match and next-step CTA

Primary CTA after result:

- Generate/Open Roadmap

### 3. Roadmap

Purpose: retention loop.

Show:

- 3 month columns/cards
- Week-by-week tasks
- Completion checkboxes
- Month progress
- Overall progress
- Task tags: Learn, Project, Certification, Resume, Internship

UX:

- Make tasks feel actionable and small
- Completed tasks should be visually calm but still readable
- Mobile should stack months vertically

### 4. Skills

Purpose: readiness truth.

Show:

- Readiness percentage
- Missing skills
- Current vs required level
- Priority labels
- Evidence field in future frontend
- Recommended learning resources

UX:

- Avoid shaming language
- Use “next skill to improve” framing

### 5. Resume Builder

Purpose: create career artifact.

Show:

- Contact/profile section
- Education
- Experience
- Export buttons: DOCX, PDF
- CTA to Analyze Resume

UX:

- Use forms with clear sections
- Keep preview and edit close together

### 6. Resume Analyzer

Purpose: improve employability.

Show:

- Upload PDF/DOCX
- Target role input
- ATS score
- Keyword matches
- Missing keywords
- Weak bullets
- Formatting issues
- Improvement suggestions
- Score history

UX:

- Score is useful, not judgmental
- Put top 3 fixes above detailed findings

### 7. AI Mentor

Purpose: context-aware guidance.

Show:

- Chat interface
- Context chips: target role, roadmap progress, resume score, weak skills
- Prompt starters: “What should I do this week?”, “Improve my resume”, “Prepare me for interview”

UX:

- Mentor should sound tactical and specific
- Do not present it as a generic chatbot

### 8. Jobs/Internships

Purpose: outcome matching.

Show:

- Opportunity cards
- Skill match %
- Resume match %
- Missing skills
- Apply/source link

UX:

- Filter by internship, fresher job, remote
- Sort by match percentage

## Visual Direction

Keep current Mentoraa style cues:

- Dark navy/charcoal base
- Teal accent
- White/light gray surfaces
- Professional student-friendly tone

Suggested palette:

- Primary: `#1e2a38`
- Background dark: `#0d1117`
- Accent: `#4db6ac`
- Accent soft: `#d2f1ee`
- Surface: `#ffffff`
- Muted surface: `#f3f6f8`
- Text muted: `#51606e`

Component style:

- Border radius: 8-14px
- Buttons: pill or soft rounded
- Progress bars: teal/navy gradient
- Cards: only for actual items or panels
- Avoid decorative social-feed layouts

## Data Objects For Lovable

Use these frontend entities:

- UserProfile
- AssessmentResult
- CareerRoadmap
- RoadmapMonth
- WeeklyTask
- UserProgress
- Skill
- CareerSkillRequirement
- UserSkill
- SkillGapReport
- ResumeProfile
- ResumeEducation
- ResumeExperience
- ResumeAnalysis
- MentorConversation
- MentorMessage
- MockInterview
- InterviewQuestion
- Opportunity
- MatchScore
- PortfolioProject
- Subscription

## API Direction

The current app is server-rendered Django. For a new frontend, create JSON endpoints around the existing services rather than duplicating logic.

Recommended API groups:

- `/api/auth/`
- `/api/assessments/`
- `/api/roadmap/`
- `/api/skills/`
- `/api/resumes/`
- `/api/analytics/`
- `/api/mentor/`
- `/api/interviews/`
- `/api/jobs/`
- `/api/portfolio/`

## Lovable Prompt Summary

Build a mobile-first SaaS dashboard for Mentoraa, an AI-powered career progression operating system. The UX should center on the pipeline assessment -> roadmap -> skills -> projects -> resume -> internships/jobs. Use a dark navy and teal brand, clean white panels, progress widgets, task checklists, skill readiness bars, resume score cards, and role-specific guidance. Avoid social feed, blog, LinkedIn clone patterns, and marketing-heavy landing pages. First screen after login should be a dashboard with roadmap progress, skill readiness, resume score, weekly tasks, and a clear next action.
