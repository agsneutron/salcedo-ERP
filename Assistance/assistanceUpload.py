from django.views.generic import View

class uploadAssistance(View):

    def handle_uploaded_file(self, archivo):
        route = 'AssistanceUploads/tmp/' + str(datetime.datetime.now()) + '.csv'
        with open(ruta, 'wb+') as destination:
            for chunk in archivo.chunks():
                destination.write(chunk)
        return ruta

    def post(self, request, *args, **kwargs):

        pass