from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import UserProfile
from .predictor import QUESTION_ORDER, QUESTION_TEXT, predict_basic_assessment


LIKERT_CHOICES = [(str(value), str(value)) for value in range(1, 6)]


# ================= LOGIN =================
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        profile, _ = UserProfile.objects.get_or_create(user=user)
        if not profile.email_verified:
            raise forms.ValidationError(
                "Please verify your email before logging in.",
                code="email_not_verified",
            )


# ================= REGISTER =================
class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "First name"}),
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Last name"}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Email address"})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Create a password"})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm password"})
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Username"}),
            "first_name": forms.TextInput(attrs={"placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email address"}),
        }

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("That username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("That email is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            self.add_error("password2", "Passwords do not match.")
        password = cleaned_data.get("password1")
        if password:
            temp_user = User(
                username=cleaned_data.get("username", ""),
                email=cleaned_data.get("email", ""),
                first_name=cleaned_data.get("first_name", ""),
                last_name=cleaned_data.get("last_name", ""),
            )
            try:
                validate_password(password, temp_user)
            except ValidationError as exc:
                self.add_error("password1", exc)
        return cleaned_data


class OTPVerificationForm(forms.Form):
    otp = forms.CharField(
        label="Verification code",
        min_length=6,
        max_length=6,
        widget=forms.TextInput(attrs={"placeholder": "6-digit OTP", "inputmode": "numeric"}),
    )

    def clean_otp(self):
        otp = self.cleaned_data["otp"].strip()
        if not otp.isdigit():
            raise forms.ValidationError("Enter the 6-digit code sent to your email.")
        return otp

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# ================= CONTACT =================
class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Your Name"}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Your Email"})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Your Message", "rows": 5})
    )


# ================= USER UPDATE =================
class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get("instance")
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError("That email is already in use.")
        return email


# ================= PROFILE =================
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["headline", "bio", "interests", "target_role"]
        widgets = {
            "headline": forms.TextInput(attrs={"placeholder": "Headline"}),
            "bio": forms.Textarea(attrs={"rows": 4, "placeholder": "Short bio"}),
            "interests": forms.TextInput(attrs={"placeholder": "Interests"}),
            "target_role": forms.TextInput(attrs={"placeholder": "Target role"}),
        }


# ================= BASIC ASSESSMENT =================
class BasicAssessmentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for question_id in QUESTION_ORDER:
            self.fields[question_id] = forms.ChoiceField(
                choices=LIKERT_CHOICES,
                widget=forms.RadioSelect,
                label=QUESTION_TEXT[question_id],
                required=True,
            )

    def get_answer_map(self):
        return {
            field_name: int(value)
            for field_name, value in self.cleaned_data.items()
        }

    def get_prediction(self):
        return predict_basic_assessment(self.get_answer_map())


# ================= ADVANCED ASSESSMENT (FIXED) =================
class AdvancedAssessmentForm(forms.Form):
    def __init__(self, questions, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔒 CRITICAL FIX: prevent NoneType crash
        if not questions or not isinstance(questions, (list, tuple)):
            questions = []

        for index, question in enumerate(questions, start=1):
            self.fields[f"q{index}"] = forms.ChoiceField(
                choices=LIKERT_CHOICES,
                widget=forms.RadioSelect,
                label=question,
                required=True,
            )

    def total_score(self):
        return sum(int(value) for value in self.cleaned_data.values())
