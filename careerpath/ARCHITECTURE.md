# Mentoraa Architecture

Mentoraa is organized around the career progression pipeline:

assessment -> roadmap -> skills -> projects -> resume -> internships/jobs

## Current App Map

- `website`: existing authentication, profile, feedback, assessments, prediction result capture.
- `builder`: existing resume builder.
- `apps.roadmap`: 3-month career roadmap, monthly milestones, weekly tasks, completion tracking.
- `apps.skills`: role skill requirements, user skills, readiness scoring, skill gap reports.
- `apps.resumes`: PDF/DOCX resume analysis, ATS score history, keyword and bullet feedback.
- `apps.analytics`: user progress dashboard and weekly summary model.
- `apps.ai_mentor`: AI mentor conversation storage.
- `apps.interviews`: role-based mock interview history and scoring.
- `apps.jobs`: internship/fresher/remote opportunity matching.
- `apps.portfolio`: project ideas, README output, project tracking.
- `apps.payments`: Stripe/Razorpay-ready subscription state.
- `apps.community`: role-specific communities and project showcases only.
- `services.ai`: OpenAI/Claude provider abstraction, ready for RAG and vector storage later.

## Production Runtime

- Web: Django + Gunicorn.
- Database: PostgreSQL through `DATABASE_URL`, SQLite fallback for local development.
- Queue: Celery with Redis broker/result backend.
- Cache: Redis through `REDIS_URL`, local memory fallback for development.
- Static files: collected into `STATIC_ROOT`.
- Deployment targets: Render, Railway, AWS, DigitalOcean, or any Docker host.

## Required Environment

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DATABASE_URL`
- `REDIS_URL`
- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `AI_PROVIDER`
- `GOOGLE_OAUTH_CLIENT_ID`
- `GOOGLE_OAUTH_CLIENT_SECRET`
- SMTP variables from `.env.example`

## Next Engineering Priorities

1. Add authenticated CRUD for `UserSkill` evidence and levels.
2. Add AI mentor UI with message streaming and quota checks.
3. Add role-specific mock interview generation through `services.ai`.
4. Add job feed importers behind provider interfaces.
5. Add production observability: structured logs, Sentry, uptime checks, and database backups.
