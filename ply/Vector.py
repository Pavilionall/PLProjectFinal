class Vector():
    def f(self):
        data = {
            'x': 0,
            '$x': lambda x: data.update({'x': x}),
            'y': 0,
            '$y': lambda x: data.update({'y': x}),
            'z': 0,
            '$z': lambda x: data.update({'z': x}),
            'length': 0,
            '$length': lambda x: data.update({'length': x}),
            'unitVectorX': 0,
            '$unitVectorX': lambda x: data.update({'unitVectorX': x}),
            'unitVectorY': 0,
            '$unitVectorY': lambda x: data.update({'unitVectorY': x}),
            'unitVectorZ': 0,
            '$unitVectorZ': lambda x: data.update({'unitVectorZ': x})
        }
        def cf(self, d):
            if d in data:
                return data[d]
            else:
                return None
        return cf
    run = f(1)
