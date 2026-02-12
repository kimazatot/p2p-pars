logo = 'logo/4148781.png'
mini_logo = 'logo/4148781.png'

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Админпанель Парсинга",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Управление сайтом",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Админ панель",

    # static to use for your site, must be present in static files, used for brand on top left
    "site_logo": "",

    # static to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": "",

    # static to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": None,

    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,

    # Welcome text on the login screen
    "welcome_sign": "Welcome to the Admin",

    # Copyright on the footer
    "copyright": "GeekPro © 2025",

    # List of model admins to search from the search bar, search bar omitted if excluded
    # If you want to use a single search field you dont need to use a list, you can use a simple string
    # "search_model": ["user.User"],
    "search_model": ["user.User"],

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,

    ############
    # Top Menu #
    ############

    # Links to put along the top menu

    "topmenu_links": [
        {"name": "Главная", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Site", "url": "https://dezis-group.vercel.app/", "permissions": ["auth.view_user"]},
        # Уберите лишние ссылки, чтобы оставить только главную
    ],

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
        {"model": "auth.user"}
    ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["auth", "books", "books.author", "books.book"],

    # Custom links to append to app groups, keyed on app name
    "custom_links": {
        "books": [{
            "name": "Make Messages",
            "url": "make_messages",
            "icon": "fas fa-comments",
            "permissions": ["books.view_book"]
        }]
    },

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.group": "fas fa-users",
        "auth.user": "fas fa-user",

        "content.docs": "fas fa-file-alt",
        "content.documents": "fas fa-file",
        "content.events": "fas fa-calendar",
        "content.news": "fas fa-newspaper",
        "content.aec_partners": "fas fa-handshake",
        "content.Facts_and_figures": "fas fa-chart-bar",
        "content.AEC_members": "fas fa-users",

        "about_company.History": "fas fa-history",
        "about_company.Value": "fas fa-heart",
        "about_company.About": "fas fa-info-circle",
        "about_company.Management": "fas fa-user-tie",

        "education.Videos": "fas fa-video",
        "education.Our_services": "fas fa-concierge-bell",
        "education.Education": "fas fa-graduation-cap",

        "support.FAQ": "fas fa-question-circle",
        "support.Footer": "fas fa-solid fa-download",
        "support.JoinRequest": "fas fa-comment",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": True,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"}
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,

    "brand_colour": "navbar-indigo",
    "accent": "accent-indigo",

    "navbar": "navbar-white navbar-light",
    "navbar_fixed": False,

    "layout_boxed": False,          # 🔥 ВАЖНО
    "footer_fixed": False,

    "sidebar_fixed": False,         # 🔥 ВАЖНО
    "sidebar": "sidebar-dark-indigo",

    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,

    "sidebar_nav_compact_style": False,   # 🔥 ВАЖНО
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,

    "theme": "litera",
    "dark_mode_theme": None,

    "actions_sticky_top": True,

    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
