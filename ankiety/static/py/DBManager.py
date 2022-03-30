from django.contrib.auth.models import User
from ankiety.models import Form


class DBManager:

    @staticmethod
    def convert_to_json(request, user_id):
        print(request)
        request._mutable = True
        title_poll = request['title']
        description_poll = request['description']

        del request['csrfmiddlewaretoken']
        del request['title']
        del request['description']

        poll_json = {'formItems': []}
        index = 0
        dict_ = {k: request.getlist(k) if len(request.getlist(k)) > 1 else v for k, v in request.items()}

        for key, value in dict_.items():
            item_symbol = key[0]
            description = value[0]
            value.pop(0)
            name = value[0]
            value.pop(0)
            placeholder = ''
            if item_symbol == 't' or item_symbol == 'n':  # possibility of placeholder
                placeholder = value[-1]
                value.pop(-1)
            is_req = 'T'  # add in future
            poll_json['formItems'].append({'id': index, 'type': item_symbol, 'description': description, 'value': value,
                                           'name': name, 'placeholder': placeholder, 'is_req': is_req})
            index += 1
        print(poll_json)
        user = User.objects.get(pk=user_id)  # owner
        Form.objects.create(owner=user,
                            close_condition='N',
                            close_value='',
                            is_closed=False,
                            title=title_poll,
                            description=description_poll,
                            items=poll_json
                            )
