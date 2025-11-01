
class Material:
    """Define las propiedades de un material"""
    
    def __init__(self, name, ambient, diffuse, specular, shininess, reflectivity, material_type):
        self.name = name
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.reflectivity = reflectivity
        self.material_type = material_type  # 0: metal, 1: water, 2: matte


