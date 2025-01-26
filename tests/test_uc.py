from unitycatalog_migrate import uc

def test_get_host_url(monkeypatch):
    monkeypatch.setenv("UC_HOST_URL", "http://testhost:8080/api/2.1/unity-catalog")
    assert uc.get_host_url() == "http://testhost:8080/api/2.1/unity-catalog"



def test_get_host_url_not_set(monkeypatch):
    monkeypatch.setenv("UC_HOST_URL", "")
    assert uc.get_host_url() == "http://localhost:8080/api/2.1/unity-catalog"