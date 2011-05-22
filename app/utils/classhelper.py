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