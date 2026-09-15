from material import Material


def test_creacion_y_getters():
    material = Material("AL-01", "Aluminio AL-01", "kg", 10)

    assert material.get_id() == "AL-01"
    assert material.get_nombre() == "Aluminio AL-01"
    assert material.get_unidad_medida() == "kg"
    assert material.get_punto_reposicion() == 10


def test_set_punto_reposicion_actualiza_valor():
    material = Material("AL-01", "Aluminio AL-01", "kg", 10)

    material.set_punto_reposicion(20)

    assert material.get_punto_reposicion() == 20


def test_requiere_reposicion_true_cuando_existencia_menor():
    material = Material("AL-01", "Aluminio AL-01", "kg", 10)

    assert material.requiere_reposicion(5) is True


def test_requiere_reposicion_false_cuando_existencia_mayor_o_igual():
    material = Material("AL-01", "Aluminio AL-01", "kg", 10)

    assert material.requiere_reposicion(10) is False
    assert material.requiere_reposicion(15) is False


def test_total_materiales_aumenta_al_crear_instancia():
    assert Material.total_materiales() == 0

    Material("AL-01", "Aluminio AL-01", "kg", 10)

    assert Material.total_materiales() == 1
