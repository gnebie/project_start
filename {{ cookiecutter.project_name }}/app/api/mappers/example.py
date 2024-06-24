from functools import singledispatch

@singledispatch
def map_to_dto(t):
    raise NotImplementedError("Unsupported type")

@map_to_dto.register
def _(t: UserSchema) -> UserReadDTO:
    return UserReadDTO(id=t.id, name=t.name, email=t.email)


