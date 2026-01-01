from tinydb import TinyDB, Query
from datetime import datetime
from typing import List
from app.schemas.memory import Episode, Preference, Heuristic

class MemoryService:
    def __init__(self, db_path: str = "../database/memory.json"):
        self.db = TinyDB(db_path)
        self.episodes_table = self.db.table("episodes")
        self.preferences_table = self.db.table("preferences")
        self.heuristics_table = self.db.table("heuristics")

    # --- Episodic Memory ---

    def get_active_episode(self, category: str | None = None) -> Episode | None:
        """Finds the current active episode. Optionally filters by category."""
        E = Query()
        if category:
            result = self.episodes_table.get((E.status.state == "active") & (E.category == category))
        else:
            result = self.episodes_table.get(E.status.state == "active")
        
        return Episode(**result) if result else None

    def create_episode(self, category: str, initial_query: str) -> Episode:
        """Creates a new episode and marks any other active episodes as paused."""
        # Pause any existing active episode
        self.pause_all_active_episodes()
        
        episode = Episode(
            category=category,
            initial_query=initial_query
        )
        self.episodes_table.insert(episode.model_dump(mode="json"))
        return episode

    def get_episodes_by_category(self, category: str) -> List[Episode]:
        """Retrieve all episodes for a given category."""
        E = Query()
        results = self.episodes_table.search(E.category == category)
        return [Episode(**r) for r in results]
    
    def get_episode_by_id(self, episode_id: str) -> Episode | None:
        """Retrieve an episode by its unique ID."""
        E = Query()
        result = self.episodes_table.get(E.id == episode_id)
        return Episode(**result) if result else None

    def pause_all_active_episodes(self):
        """Pauses all currently active episodes."""
        E = Query()
        self.episodes_table.update(
            {"status": {"state": "paused", "last_transition_reason": "New episode started"}},
            E.status.state == "active"
        )

    def update_episode(self, episode: Episode):
        E = Query()
        episode.updated_at = datetime.now()
        self.episodes_table.update(episode.model_dump(mode="json"), E.id == episode.id)

    # --- Preference Memory ---

    def upsert_preference(self, pref: Preference):
        """
        Updates preference if it exists (increasing confidence/evidence),
        otherwise inserts new preference.
        """
        P = Query()
        existing = self.preferences_table.get(
            (P.category == pref.category) & 
            (P.feature == pref.feature) & 
            (P.value == pref.value)
        )

        if existing:
            # Update logic: increase evidence, bump confidence slightly
            new_evidence_count = existing['evidence_count'] + 1
            # Simple asymptotic confidence boost: 1 - (1-old)*0.9
            new_confidence = min(1.0, existing['confidence'] + (1.0 - existing['confidence']) * 0.1)
            
            self.preferences_table.update({
                "evidence_count": new_evidence_count,
                "confidence": new_confidence,
                "last_updated": datetime.now().isoformat()
            }, doc_ids=[existing.doc_id])
        else:
            self.preferences_table.insert(pref.model_dump(mode="json"))

    def get_preferences(self, category: str) -> List[Preference]:
        P = Query()
        results = self.preferences_table.search((P.category == category) | (P.category == "global"))
        return [Preference(**r) for r in results]

    # --- Heuristic Memory ---

    def get_heuristics(self, category: str) -> List[Heuristic]:
        H = Query()
        
        results = self.heuristics_table.search(H.applicability.category == category)
        return [Heuristic(**r) for r in results]

    def add_heuristic(self, heuristic: Heuristic):
        """Seed heuristics (usually manual or system-level)"""
        self.heuristics_table.insert(heuristic.model_dump(mode="json"))
