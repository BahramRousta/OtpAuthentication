from rest_framework import throttling


class GetOTPRateThrottle(throttling.AnonRateThrottle):
    scope = 'otp_throttle'

    def allow_request(self, request, view):
        if request.method == "POST":
            return True
        return super().allow_request(request, view)


class LoginRateThrottle(throttling.AnonRateThrottle):
    scope = 'login_throttle'

    def allow_request(self, request, view):
        if request.method == "GET":
            return True
        return super().allow_request(request, view)

