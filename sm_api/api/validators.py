from attr import attrs, attrib, validators


@attrs
class UserRegisterDataValidator:
    login = attrib(validator=[validators.instance_of(str)])
    password = attrib(validator=[validators.instance_of(str)])
    first_name = attrib(validator=[validators.instance_of(str)])
    last_name = attrib(validator=[validators.instance_of(str)])


@attrs
class UserLoginDataValidator:
    login = attrib(validator=[validators.instance_of(str)])
    password = attrib(validator=[validators.instance_of(str)])


@attrs
class AddPostDataValidator:
    title = attrib(validator=[validators.instance_of(str)])
    text = attrib(validator=[validators.instance_of(str)])
