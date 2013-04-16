import ast
import os
import pkg_resources
from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse
import textwrap


class TypeNotSupported(Exception):
    pass


def check_type(expected_type, value):
    """
    Return None if the expected type does not match with the given value,
    otherwise return the value expressed as python type.
    """

    def is_char(val):
        if len(val) != 1:
            return None
        return val

    def is_array(array_type, val):
        try:
            # try to evaluate as python list
            # note that this is a SAFE evaluation.
            res = list(ast.literal_eval('[' + val + ']'))
        except (SyntaxError, ValueError):
            return None

        res = map(lambda v: check_type(array_type, v), res)
        return None if None in res else res

    type_dict = {'int': int, 'float': float, 'string': lambda s: s,
                 'char': is_char,
                 'string_array': lambda v: is_array('string', v),
                 'char_array': lambda v: is_array('char', v),
                 'int_array': lambda v: is_array('int', v),
                 'float_array': lambda v: is_array('float', v)}

    try:
        res = type_dict[expected_type](value)
    except ValueError:
        return None
    except KeyError:
        raise TypeNotSupported('{0} is not a valid type!'.format(expected_type))
    return res


def check_types(func_params, args):
    """
    Return None if the parameters given to a function are not correct,
    otherwise return the list of parameters.
    """
    # Build a list of types from the csv
    # e.g.:
    # name1;type1;name2;type2 --> [type1, type2]
    types = [arg_type for (i, arg_type) in enumerate(func_params.split(';'))
             if i % 2 != 0]

    _args = [check_type(expected_type, value)
             for expected_type, value in zip(types, args)]

    if None in _args:
        return None
    return _args


def get_truetype_font(name='verdana.ttf', size=20):
    dist = pkg_resources.get_distribution('plrutils')
    font_path = os.path.join(dist.location, 'plrutils', 'fonts', name)
    assert os.path.exists(font_path)  # asserts ftw!
    return ImageFont.truetype(font_path, size=size)


def draw_message(text, color='#000000', bg_color='#ffffff', size=(400, 400)):
    """ A View that returns a PNG image generated using PIL """

    im = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(im)

    font = get_truetype_font('verdana.ttf', 25)

    # wrap the text to fill it in the image
    # (unfortunately pil can't handle multi-line text automagically)
    wrapped_text = textwrap.wrap(text, 20)

    # draw the text at the center of the image
    w = max([draw.textsize(line, font=font)[0] for line in wrapped_text])
    left = (size[0] - w) / 2  # left margin

    v_spacing = 15  # vertical spacing
    h = sum([draw.textsize(line, font=font)[1] for line in wrapped_text]) + \
        v_spacing * (len(wrapped_text) - 1)
    top = (size[1] - h) / 2  # top margin

    # write the text, one line at a time
    for line in wrapped_text:
        draw.text((left, top), line, font=font, fill=color)
        top += draw.textsize(line, font=font)[1] + v_spacing

    response = HttpResponse(mimetype="image/png")
    im.save(response, 'PNG')

    return response  # and we're done!


def draw_legend(legend_args, margin_top=30, padding=(20, 20), rect_dim=20,
                middle_spacing=None):
    """ Draw a simple legend """

    # check whether legend_args list is valid
    expected_types = \
        'width;int;height;int;colors;string_array;label;string_array'
    args = check_types(expected_types, legend_args)
    if args is None:
        response = draw_message('Error! Invalid params type.')
        response.status_code = 500
        return response

    # retrieve parameters
    img_width, img_height = args[0], args[1]
    colors, labels = args[2], args[3]

    # make it a bit responsive
    if middle_spacing is None:
        if img_width <= 300:
            margin_top = 10
            middle_spacing = 30
        elif img_width <= 400:
            middle_spacing = 70
        else:
            middle_spacing = 100

    font = get_truetype_font('verdana.ttf', 17)

    img = Image.new('RGB', (img_width, img_height), '#FFFFFF')
    draw = ImageDraw.Draw(img)

    # calculate horizontal margin
    h_margin = img_width - (2 * padding[1] + (middle_spacing + rect_dim))
    h_margin -= max([draw.textsize(label, font=font)[0] for label in labels])
    if h_margin <= 3:
        h_margin = 4

    # margin => (top/bottom, right/left) - as in CSS
    margin = (margin_top, h_margin / 2)

    # draw outline
    draw.rectangle([(margin[1], margin[0]),
                    (img_width - margin[1], img_height - margin[0])],
                   outline='black')

    # first of all, calculate the vertical space between labels
    # to fit the labels in the legend correctly
    v_spacing = img_height - (2 * margin[0]) - (2 * padding[0])
    v_spacing -= (sum([draw.textsize(label, font=font)[1] for label in labels]))
    v_spacing /= (len(labels) - 1)

    top = margin[0] + padding[0]
    left = margin[1] + padding[1]

    # draw the items, one item at a time
    for idx, label in enumerate(labels):
        # --- rectangle on the left ---
        # calculate a top-padding for the rectangle, to correctly align it
        # to the text.
        rect_top_padding = (draw.textsize(label, font=font)[1] - rect_dim) / 2
        rect_top = top + rect_top_padding
        try:
            draw.rectangle([(left, rect_top),
                            (left + rect_dim, rect_top + rect_dim)],
                           outline='black', fill=colors[idx % len(colors)])
        except ValueError, e:
            # the specified color is not valid
            response = draw_message('Error! {}'.format(str(e)))
            response.status_code = 500
            return response

        # --- label ---
        label_left = img_width - left - draw.textsize(label, font=font)[0]
        draw.text((label_left, top), label, font=font, fill='#000000')

        top += draw.textsize(label, font=font)[1] + v_spacing

    response = HttpResponse(mimetype='image/png')
    img.save(response, 'PNG')
    return response

