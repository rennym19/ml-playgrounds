def create_instance(cls, d):
    cls_instance = cls()
    for k, v in d.items():
        if k == '_id':
            setattr(cls_instance, 'uid', v)
        setattr(cls_instance, k, v)
    return cls_instance

def cast_document(cls, document, many=False):
    if many:
        return [create_instance(cls, d) for d in document]
    return create_instance(cls, document)
