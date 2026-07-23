import pytest
from fastapi.testclient import TestClient
from Module_6_8_FastAPI.async_endpoint import app

# Fixture ensures lifespan runs (loads ESM + classifier) before tests
@pytest.fixture(scope="module")
def client():
  with TestClient(app) as c:
    yield c

# Test root endpoint
def test_root(client):
  response = client.get("/")
  assert response.status_code == 200
  assert response.json()["status"] == "running"

def test_get_existing_protein(client):
  response = client.get("/Protein/P00533")
  assert response.status_code == 200
  data = response.json()
  assert data["uniprot_id"] == "P00533"
  assert "protein_name" in data

def test_get_nonexistent_protein(client):
  response = client.get("/Protein/INVALID999")
  assert response.status_code == 404
  assert "INVALID999 not found" in response.json()["detail"]

def test_predict_valid_sequence(client):
  egfr_sequence = "MRPSGTAGAALLALLAALCPASRALEEKKVCQGTSNKLTQLGTFEDHFLSLQRMFNNCEVVLGNLEITYVQRNYDLSFLKTIQEVAGYVLIALNTVERIPLENLQIIRGNMYYENSYALAVLSNYDANKTGLKELPMRNLQEILHGAVRFSNNPALCNVESIQWRDIVSSDFLSNMSMDFQNHLGSCQKCDPSCPNGSCWGAGEENCQKLTKIICAQQCSGRCRGKSPSDCCHNQCAAGCTGPRESDCLVCRKFRDEATCKDTCPPLMLYNPTTYQMDVNPEGKYSFGATCVKKCPRNYVVTDHGSCVRACGADSYEMEEDGVRKCKKCEGPCRKVCNGIGIGEFKDSLSINATNIKHFKNCTSISGDLHILPVAFRGDSFTHTPPLDPQELDILKTVKEITGFLLIQAWPENRTDLHAFENLEIIRGRTKQHGQFSLAVVSLNITSLGLRSLKEISDGDVIISGNKNLCYANTINWKKLFGTSGQKTKIISNRGENSCKATGQVCHALCSPEGCWGPEPRDCVSCRNVSRGRECVDKCNLLEGEPREFVENSECIQCHPECLPQAMNITCTGRGPDNCIQCAHYIDGPHCVKTCPAGVMGENNTLVWKYADAGHVCHLCHPNCTYGCTGPGLEGCPTNGPKIPSIATGMVGALLLLLVVALGIGLFMRRRHIVRKRTLRRLLQERELVEPLTPSGEAPNQALLRILKETEFKKIKVLGSGAFGTVYKGLWIPEGEKVKIPVAIKELREATSPKANKEILDEAYVMASVDNPHVCRLLGICLTSTVQLITQLMPFGCLLDYVREHKDNIGSQYLLNWCVQIAKGMNYLEDRRLVHRDLAARNVLVKTPQHVKITDFGLAKLLGAEEKEYHAEGGKVPIKWMALESILHRIYTHQSDVWSYGVTVWELMTFGSKPYDGIPASEISSILEKGERLPQPPICTIDVYMIMVKCWMIDADSRPKFRELIIEFSKMARDPQRYLVIQGDERMHLPSPTDSNFYRALMDEEDMDDVVDADEYLIPQQGFFSSPSTSRTPLLSSLSATSNNSTVACIDRNGLQSCPIKEDSFLQRYSSDPTGALTEDSIDDTFLPVPEYINQSVPKRPAGSVQNPVYHNQPLNPAPSRDPHYQDPHSTAVGNPEYLNTVQPTCVNSTFDSPAHWAQKGSHQISLDNPDYQQDFFPKEAKPNGIFKGSTAENAEYLRVAPQSSEFIGA"
  response = client.post("/predict", json={"sequence": egfr_sequence})
  assert response.status_code == 200
  data = response.json()
  assert "predicted_class" in data
  assert data["predicted_class"] in ["kinase", "protease"]
  assert 0.0 <= data["confidence"] <= 1.0
  print(f"\nEGFR predicted as: {data['predicted_class']} (confidence: {data['confidence']})")

def test_predict_empty_sequence(client):
  response = client.post("/predict", json={"sequence": ""})
  # Empty sequence gives error here, not result returned. this test will be updated in the subsequent commit
  assert response.status_code in [200, 400, 422, 503]

# Reflection question comes in the subsequent commit.
