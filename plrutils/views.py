# Create your views here.
from django.http import HttpResponse
from django.db import connections
from psycopg2 import DataError, ProgrammingError
from models import GraphFunction
from django.core.exceptions import MultipleObjectsReturned
from utils import check_types, TypeNotSupported, draw_message, draw_legend


def functions_list(request):
    # robadiroberto (suona anche bene)
    pass


def execute(request, func_args):
    args = [arg for arg in func_args.split('/') if arg]
    func_name = args[0]  # first arg is function name
    args = args[1:]  # second to last args are parameters

    try:
        func = GraphFunction.objects.get(name=func_name)
    except GraphFunction.DoesNotExist:
        response = draw_message('Error! "{0}" is not a valid function!'
                              .format(func_name))
        response.status_code = 500
        return response
    except MultipleObjectsReturned:
        # This should not happen, since the "name" field
        # has the "unique=True" attribute
        response = draw_message('Error! Something REALLY wrong happened.')
        response.status_code = 500
        return response

    # A TypeNotSupported exception will be raised if
    # an expected_type is not valid.
    # I won't cover this possibility (I trust you, admin)
    args = check_types(func.params, args)
    if args is None:
        response = draw_message('Error! Invalid params type.')
        response.status_code = 500
        return response

    cursor = connections[func.database.name].cursor()
    cursor.callproc('plr_set_display', [':5.0'])  # some preliminary stuff
    res = cursor.fetchall()
    if not res[0][0].upper() == 'OK':
        response = draw_message('Error! Something wrong happened.')
        response.status_code = 500
        return response

    try:
        cursor.callproc(func_name, args)
        buff = cursor.fetchall()[0][0]
    except DataError:
        response = draw_message('Error! Invalid data.')
        response.status_code = 500
        return response
    except ProgrammingError:
        response = draw_message(
            'Error! No function matches the given name and argument types.')
        response.status_code = 500
        return response

    response = HttpResponse(buff[22:], mimetype="image/png", status=200)
    return response


def legend(request, legend_args):
    args = [arg for arg in legend_args.split('/') if arg]
    response = draw_legend(args)
    return response
