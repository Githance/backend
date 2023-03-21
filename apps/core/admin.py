from django.contrib import admin


class AdminSite(admin.AdminSite):
    site_header = "Githance, административная часть"
    site_title = "Githance"

    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been registered.

        The order of apps corresponds to the given app_order. Other apps not present in
        app_order are sorted alphabetically and appended to the end of the list.
        All models in each app are also sorted alphabetically.
        """
        app_order = (
            "projects",
            "participants",
            "users",
            "account",
            "socialaccount",
        )

        app_dict = self._build_app_dict(request)

        app_list = []
        for app_name in app_order:
            if app_dict.get(app_name) is not None:
                app_list.append(app_dict.pop(app_name))

        app_list += sorted(app_dict.values(), key=lambda x: x["name"].lower())

        for app in app_list:
            app["models"].sort(key=lambda x: x["name"])

        return app_list
