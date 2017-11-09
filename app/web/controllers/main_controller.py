
import app.device
from .controller import Controller


class MainController(Controller):

    @Controller.require()
    async def show_index(self, request):

        devices = app.device.manager.get_devices()

        return await self.render('index.tmpl.html', request, {
            'devices': devices
        })
