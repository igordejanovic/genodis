import os
from textx.metamodel import metamodel_from_file
from lang.obj_processors import model_processor, class_processor, \
    property_processor, action_processor, property_argument_processor

__author__ = 'Alen Suljkanovic'


class Model(object):
    """
    Python representation of model defined in grammar.
    """

    def __init__(self, name, classes, actions=None, bindings=None):
        """
        Initialization of model
        """
        self.name = name
        self.classes = classes
        self.actions = actions if actions else []
        self.bindings = bindings if bindings else []

    def __str__(self):
        return "Model(%s), entities: %s, actions %s" % (self.name,
                                                        self.classes,
                                                        self.actions)


class Class(object):
    """
    Python representation of entity defined in grammar.
    """

    def __init__(self, parent, name, properties, session, actions=None,
                 bindings=None):
        """
        Initialization of entity.
        """
        self.parent = parent
        self.name = name
        self.properties = properties
        self.actions = actions if actions else []
        self.session = True if session else False
        self.bindings = bindings if bindings else []

        # Dictionary that describes relationship of one class with others.
        # Key is name of referenced class and value shows how many times
        # given class has been referenced.
        self.references = {}

        self.foreign_key = None

    def __str__(self):
        return self.name


class Property(object):
    """
    Python representation of property defined in grammar.
    """
    def __init__(self, parent, name, type, list=None, arguments=None):
        """
        Initialization of property.
        """
        self.parent = parent
        self.name = name
        self.type = type
        self.list = True if list else False
        self.arguments = arguments if arguments else []

    def __str__(self):
        return self.name

    @property
    def args_dict(self):
        args = {arg.name: arg for arg in self.arguments}
        return args


class PropertyArgument(object):
    """
    Python representation of property argument defined in grammar.
    """
    def __init__(self, parent, name, value):
        self.parent = parent
        self.name = name
        self.value = value

    def __str__(self):
        return "%s=%s" % (self.name, self.value)


class Action(object):
    """
    Python representation of action defined in grammar.
    """
    def __init__(self, parent, name, expression):
        self.parent = parent
        self.name = name
        self.expression = expression

    def __str__(self):
        return self.name


class ActionExpression(object):
    """

    """
    def __init__(self, parent, first_operand, operator, second_operand):
        self.parent = parent
        self.first_operand = first_operand
        self.operator = operator
        self.second_operand = second_operand

# classes to instantiate via textX
_classes = (Model, Class, Property, PropertyArgument, Action, ActionExpression)

obj_processors = {
    "Model": model_processor,
    "Class": class_processor,
    "Property": property_processor,
    "Action": action_processor,
    "PropertyArgument": property_argument_processor,
}

_model_meta = None


def get_model_meta():
    """
    Gets model meta-model.
    """
    global _model_meta
    _model_meta = metamodel_from_file(os.path.join(os.path.dirname(__file__),
                                                   "model.tx"),
                                      classes=_classes)
    _model_meta.register_obj_processors(obj_processors)
    return _model_meta