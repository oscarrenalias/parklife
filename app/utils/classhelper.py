class ClassHelper:
    
    #
    # Returns a reference to a class given its class path
    #
    @staticmethod
    def get_class( kls ):
        parts = kls.split('.')
        module = ".".join(parts[:-1])
        m = __import__( module )
        for comp in parts[1:]:
            m = getattr(m, comp)            
        return m

#
# This mixin class allows mixed in classes to use some simple introspection to determine
# whether they provide a certain method, and to call any method with a varaible number of arguments
# by using the method name as as tring
#    
class DynamicDispatcherMixin:
    #
    # Returns True if the given object has the given method
    #
    def has_method(self, method):
        return method in self.__class__.__dict__
    
    #
    # Call a method in the given object using its name and the provided parameters
    #
    def call_method(self, method, *params):
        if self.has_method(method):
            return self.__class__.__dict__[method](self, *params)
        else:
            raise NotImplementedError("Method %s in object of class %s is not implemented" % (method, self.__class__.__name__))

#
# Calls a method or retrieves the attribute of an instance by its name, provided
# as a string
# TODO: where to put this?
#
def do_call(obj, attribute):
    v = getattr(obj, attribute)
    if v.__class__.__name__ == "instancemethod":
        return v()
    else:
        return v
        