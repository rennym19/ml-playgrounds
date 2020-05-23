def get_instance(cls, single_document):
    cls_instance = cls()
    for k, v in single_document.items():
        setattr(cls_instance, k, v)
    return cls_instance

def cast_document(cls, document, many=False):
    if many:
        return [get_instance(cls, d) for d in document]
    return get_instance(cls, document)
