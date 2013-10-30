
from api.v1 import Poem
from site import Home

urls = (
	"/api/v1/poems/.*", "Poem",
	"/.*", "Home",
	)

