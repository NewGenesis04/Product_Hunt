import pytest
from app.memory.service import MemoryService
from app.schemas.memory import Preference, Heuristic


@pytest.fixture
def memory_service(tmp_path):
    # Use a temporary directory for the test database
    db_path = tmp_path / "test_memory.json"
    service = MemoryService(str(db_path))
    yield service
    service.db.close()

def test_episode_creation_and_retrieval(memory_service):
    """Test creating an episode and retrieving it as the active one."""
    ep = memory_service.create_episode(category="Monitors", initial_query="Looking for a 27 inch monitor")
    
    assert ep.status.state == "active"
    assert ep.category == "Monitors"
    
    active = memory_service.get_active_episode()
    assert active is not None
    assert active.id == ep.id

def test_episode_transition_logic(memory_service):
    """Test that starting a new episode pauses the existing active one."""
    # Phase 1: Start Monitors episode
    ep1 = memory_service.create_episode(category="Monitors", initial_query="Looking for a 27 inch monitor")
    
    # Phase 2: Drift to Inverters (Start new episode)
    ep2 = memory_service.create_episode(category="Inverters", initial_query="How much for a 3kVA inverter?")
    
    # Verify ep2 is active
    active = memory_service.get_active_episode()
    assert active.id == ep2.id
    assert active.category == "Inverters"
    
    # Verify ep1 is paused
    ep1_doc = memory_service.get_episode_by_id(ep1.id)

    assert ep1_doc.status.state == "paused"
    assert ep1_doc.status.last_transition_reason == "New episode started"

def test_preference_upsert_logic(memory_service):
    """Test that adding the same preference twice updates evidence count and confidence."""
    pref = Preference(category="Monitors", feature="brand", value="LG", preference_type="like")
    
    # First insert
    memory_service.upsert_preference(pref)
    prefs_initial = memory_service.get_preferences("Monitors")
    assert len(prefs_initial) == 1
    assert prefs_initial[0].evidence_count == 1
    
    initial_confidence = prefs_initial[0].confidence
    
    # Second insert (Reinforcement)
    memory_service.upsert_preference(pref)
    prefs_updated = memory_service.get_preferences("Monitors")
    
    assert len(prefs_updated) == 1
    assert prefs_updated[0].evidence_count == 2
    assert prefs_updated[0].confidence > initial_confidence
    assert prefs_updated[0].confidence <= 1.0

def test_heuristic_storage_and_retrieval(memory_service):
    """Test adding and retrieving heuristics based on applicability."""
    h = Heuristic(
        name="Lagos Delivery Premium",
        rule="Lagos vendors usually have 24hr delivery but higher base price",
        applicability={"category": "electronics"},
        logic_hint="Factor in delivery speed when comparing Lagos vs Abuja vendors"
    )
    memory_service.add_heuristic(h)
    
    # Retrieve using the category logic implemented in get_heuristics
    results = memory_service.get_heuristics("electronics")
    
    assert len(results) == 1
    assert results[0].name == "Lagos Delivery Premium"
    
    # Verify non-matching category returns empty
    empty_results = memory_service.get_heuristics("furniture")
    assert len(empty_results) == 0
