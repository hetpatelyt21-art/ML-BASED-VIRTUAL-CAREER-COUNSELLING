from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ResumeUploadForm
from .models import ResumeAnalysis
from .services import analyze_resume


@login_required
def resume_analyzer(request):
    latest_role = request.user.assessment_results.first().career_name if request.user.assessment_results.exists() else ""
    form = ResumeUploadForm(request.POST or None, request.FILES or None, initial={"target_role": latest_role})
    if form.is_valid():
        analysis = analyze_resume(
            request.user,
            form.cleaned_data["resume_file"],
            form.cleaned_data["target_role"] or latest_role,
        )
        messages.success(request, "Resume analysis complete.")
        return redirect("resume_analyzer")
    analyses = ResumeAnalysis.objects.filter(user=request.user)[:5]
    return render(request, "resumes/analyzer.html", {"form": form, "analyses": analyses})

