
from .controller import Controller


class MainController(Controller):

    @Controller.require()
    async def show_index(self, request):
        return await self.render('index.tmpl.html', request)
