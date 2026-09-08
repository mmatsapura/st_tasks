# Демо 6. pydantic.BaseModel
#
# dataclass доверяет полям. BaseModel проверяет типы и ограничения
# в момент создания: "10" станет 10, а age=-1 не пройдёт.
#
# Нужен пакет: pip install pydantic
# API ниже — для pydantic v2.


from pydantic import BaseModel, Field, ValidationError, field_validator


class User(BaseModel):
    name: str = Field(min_length=1)
    age: int = Field(ge=0, le=120)
    email: str

    @classmethod
    def email_must_have_at(cls, value):
        if "@" not in value:
            raise ValueError("email must contain @")
        return value


user = User(name="Ira", age="20", email="ira@mail.com")
print(user)                    # age уже int, не строка
print(user.model_dump())       # обычный dict — удобно отдать в JSON

try:
    User(name="", age=-1, email="ira.mail.com")
except ValidationError as error:
    print(error)
