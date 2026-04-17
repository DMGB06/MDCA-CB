from app.services.knowledge_service import search_knowledge


def test_search_knowledge_tramite():
    result = search_knowledge("licencia de funcionamiento")
    assert "Licencia de Funcionamiento" in result
    assert "S/150" in result


def test_search_knowledge_horario():
    result = search_knowledge("horario caja")
    assert "Caja" in result
    assert "8:30 am" in result


def test_search_knowledge_contacto():
    result = search_knowledge("teléfono atención")
    assert "(01) 876-5432" in result


def test_search_knowledge_faq():
    result = search_knowledge("impuestos")
    assert "Caja Municipal" in result
