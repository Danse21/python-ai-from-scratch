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
  # Re-written to follow one status code, one specific message rule
  # assert response.status_code in [200, 400, 422, 503]
  assert response.status_code == 422
  assert "empty" in response.json()["detail"].lower()

"""
Reflection questions:
Q1. Why does TestClient not need a running server — how does it work?
Answer: TestClient wraps FastAPI app using ASGI and calls the app functions directly in-process without HTTP or a running server.
The request goes straight into the FastAPI app's code and returns the response.
Q2. test_predict_empty_sequence accepts multiple status codes (in [200, 400, 422, 503]). Is this good or bad test design, and
what would a better test look like?
Answer: A multiple status codes in one assert is bad test design because the test passes even when things go wrong for the wrong
reason. it should always be one status code, one specific message.
Q3. EGFR (P00533) is a receptor tyrosine kinase — what do you expect the model to predict for it, and why?
Answer: I would expect the model to predict a kinase with igh confidence if the model performs optimally. This is  becuase the
training data almost certainly contained kinases with similar sequences. If it predicts protease, it will indicate that
the 30-protein training set was too small to capture the EGFR's sequence neighbourhood.
"""
