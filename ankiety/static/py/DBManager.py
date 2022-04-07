from django.contrib.auth.models import User
from ankiety.models import Form,Response
import re


class DBManager:

    @staticmethod
    def is_required(is_req):
        if is_req == '1':
            return 'Y'
        else:
            return 'F'

    @staticmethod
    def close_condition_mark(close_value):
        if re.match(r"^\d{4}-\d{2}-\d{2}$", close_value) is not None:
            return 'D'
        elif re.match(r"^[1-9]\d*$", close_value) is not None:
            return 'C'
        else:
            return 'N'

    @staticmethod
    def insert_poll_model(request, user_id):
        print(request)
        request._mutable = True
        title_poll = request['title']
        description_poll = request['description']
        end_condition_poll = request['end_condition']
        del request['csrfmiddlewaretoken']
        del request['title']
        del request['description']
        del request['end_condition']

        poll_json = {'formItems': []}
        index = 0
        dict_ = {k: request.getlist(k) if len(request.getlist(k)) > 1 else v for k, v in request.items()}

        for key, value in dict_.items():
            item_symbol = key[0]
            description = value[0]
            value.pop(0)
            name = value[0]
            value.pop(0)
            is_req = value[0]
            value.pop(0)
            placeholder = ''
            if item_symbol == 't' or item_symbol == 'n':  # possibility of placeholder
                placeholder = value[-1]
                value.pop(-1)
            poll_json['formItems'].append({'id': index, 'type': item_symbol, 'description': description, 'value': value,
                                           'name': name, 'is_req': DBManager.is_required(is_req)})
            index += 1
        print(poll_json)
        user = User.objects.get(pk=user_id)  # owner
        Form.objects.create(owner=user,
                            close_condition=DBManager.close_condition_mark(end_condition_poll),
                            close_value=end_condition_poll,
                            title=title_poll,
                            description=description_poll,
                            items=poll_json
                            )

    @staticmethod
    def get_poll_model(poll_id):
        form = Form.objects.get(pk=poll_id)
        if form.is_closed:
            return Exception("This poll is closed. You can no longer respond to it.")
        else:
            return form

    @staticmethod
    def get_user_polls(user_id):
        return Form.objects.filter(owner=user_id)

    @staticmethod
    def send_poll_response(request, poll_id):
        return 5

    @staticmethod
    def get_responses(poll_id):
        return Response.objects.filter(id_response=poll_id)
