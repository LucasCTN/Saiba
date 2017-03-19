# -*- coding: utf-8 -*-

def custom_error_messages( fields, labels ):
    messages = {}

    for field in fields:
        label_name = labels[field]

        required = "O campo '" + label_name + "' é obrigatório."

        messages[field] = {   'required' : required,
                            'invalid_image' : u'Envie uma imagem válida. O arquivo que você enviou não é uma imagem ou é uma imagem corrompida.' }

    return messages