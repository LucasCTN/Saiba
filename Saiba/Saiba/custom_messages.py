# -*- coding: utf-8 -*-

def get_all_error_messages( fields, labels ):
    messages = {}

    messages_types = ['required', 'invalid_image']

    for field in fields:
        label_name = labels[field]

        errors = {}

        for message_type in messages_types:
            errors[message_type] = get_error_message( labels[field], message_type )

        messages[message_type] = errors

    return messages

def get_error_message( label_name, message_type ):
    messages = {    'required' : "O campo '" + label_name + "' é obrigatório.",
                    'invalid_image' : u'Envie uma imagem válida. O arquivo que você enviou não é uma imagem ou é uma imagem corrompida.' }

    return messages[message_type]

def get_custom_error_message( message_type ):
    custom_messages = { 'duplicated_entry' : "Já existe uma entrada com este título.",
                        'invalid_date' : "A data inserida é inválida." }

    return custom_messages[message_type]