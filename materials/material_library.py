from materials.material import Material

class MaterialLibrary:
    """Biblioteca de materiales predefinidos"""
    
    @staticmethod
    def get_materials():
        return {
            'metal': Material(
                name='Metálico',
                ambient=[0.2, 0.2, 0.22],
                diffuse=[0.7, 0.7, 0.75],
                specular=[1.0, 1.0, 1.0],
                shininess=150.0,
                reflectivity=0.85,
                material_type=0
            ),
            'water': Material(
                name='Agua',
                ambient=[0.08, 0.22, 0.32],
                diffuse=[0.25, 0.55, 0.75],
                specular=[0.85, 0.92, 1.0],
                shininess=80.0,
                reflectivity=0.65,
                material_type=1
            ),
            'matte': Material(
                name='Opaco',
                ambient=[0.35, 0.15, 0.1],
                diffuse=[0.9, 0.35, 0.25],
                specular=[0.15, 0.15, 0.15],
                shininess=8.0,
                reflectivity=0.05,
                material_type=2
            )
        }