from allauth.socialaccount.providers.google.provider import GoogleProvider as DjRestAuthGoogleProvider


# class GoogleProvider(DjRestAuthGoogleProvider):
#     id = "google"
#
#     def extract_common_fields(self, data):
#         first_name = data.get("given_name", "")
#         last_name = data.get("family_name", "")
#         name = " ".join((first_name, last_name)).strip()
#         return {
#             "email": data.get("email"),
#             "name": name,
#         }


# provider_classes = (GoogleProvider,)
