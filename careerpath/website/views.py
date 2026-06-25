from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from .career_data import CAREER_RESULTS, QUESTION_SETS
from .career_resources import get_career_resource
from .forms import (
    AdvancedAssessmentForm,
    BasicAssessmentForm,
    ContactForm,
    OTPVerificationForm,
    ProfileUpdateForm,
    RegistrationForm,
    UserLoginForm,
    UserUpdateForm,
)
from .models import AssessmentResult, EmailVerification, Feedback, UserProfile


def _build_progression_system(result):
    from apps.roadmap.services import generate_roadmap_for_result
    from apps.skills.services import generate_skill_gap_report

    roadmap = generate_roadmap_for_result(result)
    skill_report = generate_skill_gap_report(result)
    return roadmap, skill_report


def _get_basic_prediction(request):
    return request.session.get("basic_prediction") or {}


def _get_predicted_domain(request):
    basic_prediction = _get_basic_prediction(request)
    return basic_prediction.get("top_domain") or request.session.get("selected_domain")


def _get_question_domain(request):
    predicted_domain = _get_predicted_domain(request)
    if predicted_domain in QUESTION_SETS:
        return predicted_domain

    return "Engineering & Technology"


def _send_verification_email(user):
    verification, otp = EmailVerification.create_for_user(user)
    send_mail(
        subject="Your Mentoraa verification code",
        message=(
            f"Your Mentoraa verification code is {otp}. "
            "It expires in 10 minutes."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
    return verification


def home(request):
    initial = {}
    if request.user.is_authenticated:
        initial = {
            "name": request.user.get_full_name() or request.user.username,
            "email": request.user.email,
        }

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            Feedback.objects.create(
                user=request.user if request.user.is_authenticated else None,
                **form.cleaned_data,
            )
            messages.success(request, "Thanks for the feedback.")
            return redirect("home")
    else:
        form = ContactForm(initial=initial)

    return render(request, "website/home.html", {"contact_form": form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        UserProfile.objects.get_or_create(user=user)
        _send_verification_email(user)
        messages.success(request, "We sent a verification code to your email.")
        return redirect("verify_email", user_id=user.pk)

    return render(request, "website/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = UserLoginForm(request, data=request.POST or None)
    if form.is_valid():
        login(request, form.get_user())
        messages.success(request, "Welcome back.")
        return redirect("home")

    return render(
        request,
        "website/login.html",
        {
            "form": form,
            "google_oauth_enabled": bool(settings.GOOGLE_OAUTH_CLIENT_ID and settings.GOOGLE_OAUTH_CLIENT_SECRET),
        },
    )


def verify_email_view(request, user_id):
    if request.user.is_authenticated:
        return redirect("home")
    user = get_object_or_404(User, pk=user_id)
    verification, _ = EmailVerification.objects.get_or_create(
        user=user,
        defaults={
            "otp_hash": "",
            "expires_at": timezone.now(),
        },
    )
    if not verification.otp_hash:
        _send_verification_email(user)
        verification = user.email_verification

    form = OTPVerificationForm(request.POST or None)
    if form.is_valid():
        if verification.verify(form.cleaned_data["otp"]):
            messages.success(request, "Email verified. You can now log in.")
            return redirect("login")
        messages.error(request, "Invalid or expired verification code.")

    return render(
        request,
        "website/verify_email.html",
        {"form": form, "verification": verification, "user_to_verify": user},
    )


def resend_otp_view(request, user_id):
    if request.method != "POST":
        return redirect("verify_email", user_id=user_id)
    user = get_object_or_404(User, pk=user_id)
    profile, _ = UserProfile.objects.get_or_create(user=user)
    if profile.email_verified:
        messages.info(request, "This email is already verified.")
        return redirect("login")
    _send_verification_email(user)
    messages.success(request, "A new verification code has been sent.")
    return redirect("verify_email", user_id=user.pk)


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")


@login_required
def basic_test(request):
    form = BasicAssessmentForm(request.POST or None)

    if form.is_valid():
        prediction = form.get_prediction()
        request.session["basic_prediction"] = prediction.as_session_payload()
        request.session["selected_domain"] = prediction.top_domain
        request.session["result_domain"] = prediction.top_domain
        request.session["advanced_score"] = None
        request.session["result_saved"] = False
        request.session.pop("latest_result_id", None)
        return redirect(f"{reverse('advanced_test')}?domain={prediction.top_domain}")

    return render(request, "website/basic_test.html", {"form": form})


@login_required
def advanced_test(request):
    if not _get_basic_prediction(request):
        messages.info(request, "Complete the basic test first.")
        return redirect("basic_test")
    domain = _get_question_domain(request)
    questions = QUESTION_SETS.get(domain) or QUESTION_SETS["Engineering & Technology"]
    form = AdvancedAssessmentForm(questions, request.POST or None)

    if form.is_valid():
        predicted_domain = _get_predicted_domain(request) or domain
        request.session["advanced_score"] = form.total_score()
        request.session["selected_domain"] = predicted_domain
        request.session["result_domain"] = predicted_domain
        request.session["result_saved"] = False
        return redirect("results")

    return render(
        request,
        "website/advanced_test.html",
        {"form": form, "domain": domain},
    )


def _build_result_context(request):
    basic_prediction = _get_basic_prediction(request)
    if not basic_prediction:
        return {
            "has_result_data": False,
            "domain": "Unknown",
            "career_name": "Assessment not completed",
            "career_description": "Take the basic and advanced assessments to unlock your roadmap and saved progress.",
            "match_score": 0,
            "advanced_score": 0,
            "model_confidence": 0,
            "top_traits": [],
            "top_matches": [],
            "salary_text": "",
            "outlook_text": "",
            "facts_source": "",
            "learning_sources": [],
            "resources": [],
            "roadmap_summary": "",
            "required_skills": [],
            "top_industries": [],
            "courses": [],
            "videos": [],
        }

    domain = basic_prediction.get("top_domain")
    if domain not in CAREER_RESULTS:
        domain = "Engineering & Technology"

    result = CAREER_RESULTS.get(domain, CAREER_RESULTS["Engineering & Technology"])
    resource_pack = get_career_resource(
        basic_prediction.get("recommended_role", result["career"])
    )
    score = int(request.session.get("advanced_score") or 0)
    advanced_percentage = min(99, 60 + round((score / 25) * 39))
    model_confidence = int(basic_prediction.get("confidence", advanced_percentage))
    percentage = round((advanced_percentage * 0.6) + (model_confidence * 0.4))
    sorted_matches = sorted(
        basic_prediction.get("probabilities", {}).items(),
        key=lambda item: item[1],
        reverse=True,
    )[:3]

    return {
        "has_result_data": True,
        "domain": domain,
        "career_name": basic_prediction.get("recommended_role", result["career"]),
        "career_description": result["description"],
        "match_score": percentage,
        "advanced_score": advanced_percentage,
        "model_confidence": model_confidence,
        "top_traits": basic_prediction.get("top_traits", []),
        "top_matches": sorted_matches,
        "salary_text": result["salary"],
        "outlook_text": result["outlook"],
        "facts_source": result["facts_source"],
        "learning_sources": result["sources"],
        "roadmap_summary": resource_pack["roadmap_summary"],
        "required_skills": resource_pack["required_skills"],
        "top_industries": resource_pack["top_industries"],
        "resources": resource_pack["resources"],
        "courses": resource_pack["courses"],
        "videos": resource_pack["videos"],
    }


def _build_saved_result_context(result):
    resource_pack = get_career_resource(result.career_name)
    return {
        "has_result_data": True,
        "domain": result.domain,
        "career_name": result.career_name,
        "career_description": result.career_description,
        "match_score": result.match_score,
        "advanced_score": result.advanced_score,
        "model_confidence": result.model_confidence,
        "top_traits": result.top_traits,
        "top_matches": result.top_matches,
        "salary_text": result.salary_text,
        "outlook_text": result.outlook_text,
        "facts_source": "Saved Mentoraa result",
        "learning_sources": result.learning_sources,
        "roadmap_summary": resource_pack["roadmap_summary"],
        "required_skills": resource_pack["required_skills"],
        "top_industries": resource_pack["top_industries"],
        "resources": resource_pack["resources"],
        "courses": resource_pack["courses"],
        "videos": resource_pack["videos"],
    }


@login_required
def results(request):
    saved_result = None
    latest_saved_result = request.user.assessment_results.first()
    context = _build_result_context(request)

    if not context["has_result_data"] and latest_saved_result:
        context = _build_saved_result_context(latest_saved_result)
    elif not context["has_result_data"]:
        messages.info(request, "Complete the assessment to view your result.")
        return redirect("basic_test")

    if (
        context["has_result_data"]
        and _get_basic_prediction(request)
        and not request.session.get("result_saved")
    ):
        saved_result = AssessmentResult.objects.create(
            user=request.user,
            domain=context["domain"],
            career_name=context["career_name"],
            career_description=context["career_description"],
            match_score=context["match_score"],
            advanced_score=context["advanced_score"],
            model_confidence=context["model_confidence"],
            salary_text=context["salary_text"],
            outlook_text=context["outlook_text"],
            top_traits=context["top_traits"],
            top_matches=context["top_matches"],
            learning_sources=context["learning_sources"],
        )
        request.session["result_saved"] = True
        request.session["latest_result_id"] = saved_result.pk
        latest_saved_result = saved_result
        _build_progression_system(saved_result)

    context["saved_result"] = saved_result
    context["latest_saved_result"] = latest_saved_result
    context["active_result"] = saved_result or latest_saved_result
    return render(request, "website/results.html", context)


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    latest_result = request.user.assessment_results.first()
    recent_results = request.user.assessment_results.all()[:5]
    feedback_count = request.user.feedback_entries.count()

    user_form = UserUpdateForm(request.POST or None, instance=request.user)
    profile_form = ProfileUpdateForm(request.POST or None, instance=profile)

    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        messages.success(request, "Your profile has been updated.")
        return redirect("profile")

    return render(
        request,
        "website/profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "latest_result": latest_result,
            "recent_results": recent_results,
            "feedback_count": feedback_count,
        },
    )


def feedback_view(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        Feedback.objects.create(
            user=request.user if request.user.is_authenticated else None,
            **form.cleaned_data,
        )
        messages.success(request, "Feedback submitted.")

    return redirect(f"{reverse('home')}#contact")
