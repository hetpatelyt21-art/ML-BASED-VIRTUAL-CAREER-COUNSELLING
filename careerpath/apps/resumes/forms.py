from django import forms


class ResumeUploadForm(forms.Form):
    target_role = forms.CharField(max_length=140, required=False)
    resume_file = forms.FileField()

    def clean_resume_file(self):
        resume_file = self.cleaned_data["resume_file"]
        extension = resume_file.name.rsplit(".", 1)[-1].lower()
        if extension not in {"pdf", "docx"}:
            raise forms.ValidationError("Upload a PDF or DOCX resume.")
        if resume_file.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Resume uploads must stay under 5 MB.")
        return resume_file

