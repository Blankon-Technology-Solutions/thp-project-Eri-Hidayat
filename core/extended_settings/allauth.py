import os

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APPS": [
            {
                "client_id": os.environ.get("GOOGLE_OAUTH2_KEY"),
                "secret": os.environ.get("GOOGLE_OAUTH2_SECRET"),
                "key": "",
            },
        ],
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    },
    "linkedin_oauth2": {
        "SCOPE": ["r_liteprofile", "r_emailaddress"],
        "PROFILE_FIELDS": [
            "id",
            "first-name",
            "last-name",
            "email-address",
            "picture-url",
            "public-profile-url",
        ],
        "APP": {
            "client_id": os.environ.get("LINKEDIN_OAUTH2_KEY"),
            "secret": os.environ.get("LINKEDIN_OAUTH2_SECRET"),
            "key": "",
        },
    },
}
