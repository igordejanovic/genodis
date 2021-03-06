from lang.validators import TextValidator, DecimalValidator, BaseValidator

__author__ = 'Alen Suljkanovic'


def action_processor(action):
    """
    Action processor
    """
    print(str(action.expression.second_operand.first_operand.name))


def property_processor(property):
    """
    Property processor
    """
    def resolve_date(args):
        for arg in args:
            if arg.name == "format":
                print("format value %s" % arg.value)

    def _validate(prop):
        validator = None
        if prop.type == "string" or prop.type == "combo":
            validator = TextValidator(prop)
        elif prop.type == "decimal":
            validator = DecimalValidator(prop)
        else:
            validator = BaseValidator(prop)

        validator.validate()

    _validate(property)

    if not hasattr(property, "django_field"):
        setattr(property, "django_field", None)

    django_mappings = {
        "string": "CharField",
        "text": "TextField",
        "int": "IntegerField",
        "float": "FloatField",
        "decimal": "DecimalField",
        "date": "DateField",
        "datetime": "DateTimeField",
        "combo": "CharField"
    }

    if property.type == "combo":
        choices = property.args_dict["choices"]
        choices_data = choices.value.split(",")
        # value for 'choices' argumet is string, so create list of tupples
        new_value = []
        for data in choices_data:
            short_name, long_name = data.split(":")
            new_value.append((short_name, long_name))

        choices.value = tuple(new_value)
        # Dynamically add max length if it's not declared
        if "max_length" not in property.args_dict:
            from lang.meta import PropertyArgument
            arg = PropertyArgument(property, "max_length", len(new_value))
            property.arguments.insert(0, arg)

    if property.type in django_mappings:
        property.django_field = django_mappings[property.type]


def property_argument_processor(prop_argument):
    """
    Property argument processor.
    """
    if prop_argument.name == "unique":
        if not prop_argument.value:
            prop_argument.value = True


def class_processor(_class):
    """
    Class processor
    """
    # print(_class)
    pass


def model_processor(model):
    """
    Model processor
    """
    # Dictionary of all classes in model
    all_classes = {c.name: c for c in model.classes}

    for c in model.classes:
        for p in c.properties:
            if p.type in all_classes and not c.session:
                if p.list:
                    ref_class = all_classes[p.type]
                    ref_class.foreign_key = c