# -*- coding: utf-8 -*-

def custom_error_messages( fields ):
    messages = {}

    for field in fields:
        messages[field] = {   'required' : u'Esse campo é obrigatório.',
                            'invalid_image' : u'Envie uma imagem válida. O arquivo que você enviou não é uma imagem ou é uma imagem corrompida.' }

    return messages