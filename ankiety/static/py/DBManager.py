from django.contrib.auth.models import User
from ankiety.models import Form, Response
from .RequestParser import RequestParser
from django.db import connection
from datetime import datetime


class DBManager:

    @staticmethod
    def insert_poll_model(request, user_id):
        print(request)
        request._mutable = True
        title_poll = request['title']
        description_poll = request['description']
        end_condition_poll = request['end_condition']
        is_public = request['public']
        del request['csrfmiddlewaretoken']
        del request['title']
        del request['description']
        del request['end_condition']
        del request['public']

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

            poll_json['formItems'].append({'id': index, 'type': item_symbol, 'description': description, 'value': value,
                                           'name': name, 'is_req': RequestParser.is_required(is_req)})
            index += 1
        print(poll_json)
        user = User.objects.get(pk=user_id)  # owner
        Form.objects.create(owner=user,
                            close_condition=RequestParser.close_condition_mark(end_condition_poll),
                            close_value=end_condition_poll,
                            is_public=is_public,
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
        current_form = Form.objects.get(pk=poll_id)
        if current_form.is_closed:
            return Exception("This poll is closed. You can no longer respond to it.")
        if current_form.close_condition == 'C':
            if current_form.close_count >= int(current_form.close_value):
                current_form.is_closed = True
        """
        elif current_form.close_condition == 'D':
            if datetime.now().strftime("%Y-%m-%d") > datetime.strptime(current_form.close_value, "%Y-%m-%d"):
                current_form.is_closed = True
        """

        current_form.close_count += current_form.close_count + 1
        current_form.save()

        request._mutable = True
        dict_ = {k: request.getlist(k) if len(request.getlist(k)) > 1 else v for k, v in request.items()}
        del request['csrfmiddlewaretoken']
        poll_json = {}

        for key, value in dict_.items():
            if key == 'csrfmiddlewaretoken':
                continue
            params = key.split('-')
            key = params[1]
            poll_json[key] = value

        # print(poll_json)

        if Response.objects.filter(pk=poll_id).exists():
            with connection.cursor() as cursor:
                cursor.execute("UPDATE ankiety_response SET responses = JSON_ARRAY_APPEND(responses, '$', %s) WHERE id_response_id = %s", [poll_json, poll_id])
        else:
            Response.objects.create(id_response=current_form, responses=poll_json)
        # Response.objects.filter(id_response=poll_id).update(responses=Response('responses',poll_json ))


    @staticmethod
    def get_responses(poll_id):
        return Response.objects.filter(id_response=poll_id)

    @staticmethod
    def get_public_newest_polls():
        return Form.objects.filter(is_public=True).order_by('created_at')
