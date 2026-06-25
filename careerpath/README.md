# Mentoraa Django MVP

Mentoraa is a focused career guidance MVP with authentication, email OTP verification, Google OAuth support, assessments, result recommendations, feedback, profile management, and a resume builder.

## Active structure

- `careerpath/` project settings, root URLs, ASGI/WSGI entrypoints
- `website/` home, auth, OTP verification, profile, assessment, results, feedback, static assets, and templates
- `builder/` resume profile, education, experience, and preview flows
- `ml/BasicTestQue.csv` local assessment dataset used by `website/predictor.py`
- `media/` uploaded profile media
- `db.sqlite3` local development database

Removed modules: `journey`, `coach`, `community`, and portfolio builder.

## Install

```powershell
C:\Users\ASUS\AppData\Local\Programs\Python\Python312\python.exe -m pip install -r requirements.txt
```

## Migrate

```powershell
C:\Users\ASUS\AppData\Local\Programs\Python\Python312\python.exe manage.py migrate
```

## Run

```powershell
C:\Users\ASUS\AppData\Local\Programs\Python\Python312\python.exe manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Environment variables

```text
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=Mentoraa <your-email@gmail.com>

GOOGLE_OAUTH_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret
```

Without SMTP variables, Mentoraa uses Django's console email backend for local OTP testing.

## Google OAuth setup

1. Create OAuth credentials in Google Cloud Console.
2. Add redirect URI: `http://127.0.0.1:8000/accounts/google/login/callback/`.
3. Set `GOOGLE_OAUTH_CLIENT_ID` and `GOOGLE_OAUTH_CLIENT_SECRET`.
4. Ensure Django Site id `1` is set to domain `127.0.0.1:8000`.
5. Restart the server.

## Active routes

- `/`
- `/register/`
- `/verify-email/<user_id>/`
- `/verify-email/<user_id>/resend/`
- `/login/`
- `/logout/`
- `/profile/`
- `/basic-test/`
- `/advanced-test/`
- `/results/`
- `/builder/resume/`
- `/builder/resume/preview/`
- `/builder/resume/education/add/`
- `/builder/resume/experience/add/`
