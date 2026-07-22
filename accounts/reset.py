from django.contrib.auth import views as auth_views



class EduTrackPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'email_and_reset/password_reset_confirm.html'
    success_url = '/reset/done/'

    def form_valid(self, form):
        response = super().form_valid(form)

        # A completed password reset is a strong signal the account owner
        # is back in control — clear any accumulated Axes lockout so they
        # aren't still cooling off from whatever failed attempts (their own
        # forgotten password, or someone else's guesses) led them here.
        from axes.utils import reset

        user = form.user
        reset(username=user.get_username())

        return response