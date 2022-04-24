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
    def get_poll_model(poll_id, secure=True):
        form = Form.objects.get(pk=poll_id)
        if not secure:
            return form
        try:
            DBManager.__check_close_condition(form)
        except Exception as ex:
            raise Exception(ex)
        return form

    @staticmethod
    def get_user_polls(user_id):
        return Form.objects.filter(owner=user_id)

    @staticmethod
    def __check_close_condition(form):
        if form.is_closed:
            raise Exception("This poll is closed. You can no longer respond to it.")
        if form.close_condition == 'C':
            if form.close_count+1 == int(form.close_value):
                form.is_closed = True
            elif form.close_count >= int(form.close_value):
                form.is_closed = True
                form.save()
                raise Exception("This poll is closed. You can no longer respond to it.")
        elif form.close_condition == 'D':
            if datetime.strptime(datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d") > \
                    datetime.strptime(form.close_value, "%Y-%m-%d"):
                form.is_closed = True
                form.save()
                raise Exception("This poll is closed. You can no longer respond to it.")

    @staticmethod
    def send_poll_response(request, poll_id):
        current_form = Form.objects.get(pk=poll_id)
        try:
            DBManager.__check_close_condition(current_form)
        except Exception as ex:
            raise Exception(ex)

        current_form.close_count = current_form.close_count + 1
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
        response = Response.objects.filter(id_response=poll_id)
        return response[0].responses

    @staticmethod
    def get_public_newest_polls():
        return Form.objects.filter(is_public=True).order_by('created_at')[:10]

    @staticmethod
    def get_polls_by_title(request):
        params = request['search'].split(' ')
        query = "select * from ankiety_form where is_public=true and ("
        for p in range(0, len(params)):
            query += "title like '%%" + params[p] + "%%'"
            if p != len(params) - 1:
                query += " or "
        data = []
        query += ')'
        for p in Form.objects.raw(query):
            data.append(p)
        return data

    @staticmethod
    def get_names(poll_id):
        form = Form.objects.get(pk=poll_id)
        values = []
        for f in form.items['formItems']:
            values.append(f['name'])
        return values

    @staticmethod
    def get_names_types(poll_id):
        form = Form.objects.get(pk=poll_id)
        values = []
        for f in form.items['formItems']:
            values.append({'name': f['name'], 'type': f['type'], 'title': f['description'], 'questions':f['value']})
        return values



