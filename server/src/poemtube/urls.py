
urls = (
    '/openid', 'web.webopenid.host',

    "/api/v1/poems(.*)", "poemtube.api.v1.Poems",
    "/api/v1/login",     "poemtube.api.v1.LogIn",
    "/api/v1/loginoid",  "poemtube.api.v1.LogInOid",
    "/api/v1/whoami",    "poemtube.api.v1.WhoAmI",

    "/", "poemtube.site.Home",
)

