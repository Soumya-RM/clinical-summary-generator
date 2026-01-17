from pathlib import Path
import pandas as pd
from typing import Dict, Any, List

DATA_DIR = Path("data")

FILES = {
    "diagnoses": "diagnoses.csv",
    "medications": "medications.csv",
    "vitals": "vitals.csv",
    "notes": "notes.csv",
    "wounds": "wounds.csv",
    "oasis": "oasis.csv",
}

class DataLoader:
    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = data_dir
        self.tables = self._load_all()

    def _load_all(self) -> Dict[str, pd.DataFrame]:
        tables = {}
        for name, file in FILES.items():
            path = self.data_dir / file
            if not path.exists():
                raise FileNotFoundError(f"Missing required file: {file}")
            tables[name] = pd.read_csv(path)
        return tables

    def get_latest_episode(self, patient_id: str) -> str:
        df = self.tables["diagnoses"]

        patient_rows = df[df["patient_id"] == patient_id]
        if patient_rows.empty:
            raise ValueError(f"No data found for patient_id={patient_id}")

        # Assumption: episode_id increases over time
        latest_episode = patient_rows["episode_id"].max()
        return latest_episode

    def _filter_by_patient_episode(
        self, df: pd.DataFrame, patient_id: str, episode_id: str
    ) -> pd.DataFrame:
        cols = df.columns

        if "episode_id" in cols:
            return df[
                (df["patient_id"] == patient_id) &
                (df["episode_id"] == episode_id)
            ]

        return df[df["patient_id"] == patient_id]

    def get_patient_snapshot(self, patient_id: str) -> Dict[str, Any]:
        episode_id = self.get_latest_episode(patient_id)

        snapshot = {
            "patient_id": patient_id,
            "episode_id": episode_id,
            "diagnoses": self._filter_by_patient_episode(
                self.tables["diagnoses"], patient_id, episode_id
            ).to_dict("records"),

            "medications": self._filter_by_patient_episode(
                self.tables["medications"], patient_id, episode_id
            ).to_dict("records"),

            "vitals": self._filter_by_patient_episode(
                self.tables["vitals"], patient_id, episode_id
            ).to_dict("records"),

            "notes": self._filter_by_patient_episode(
                self.tables["notes"], patient_id, episode_id
            ).to_dict("records"),

            "wounds": self._filter_by_patient_episode(
                self.tables["wounds"], patient_id, episode_id
            ).to_dict("records"),

            "oasis": self._filter_by_patient_episode(
                self.tables["oasis"], patient_id, episode_id
            ).to_dict("records"),
        }

        return snapshot

if __name__ == "__main__":
    loader = DataLoader()
    snapshot = loader.get_patient_snapshot(1001)
    print(snapshot.keys())
    
    print(snapshot["episode_id"])
    
    for k, v in snapshot.items():
        if isinstance(v, list):
            print(k, len(v))


