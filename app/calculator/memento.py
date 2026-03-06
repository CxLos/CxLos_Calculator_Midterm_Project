# =========== Imports =========== #

import datetime
from typing import Any, Dict, List
from dataclasses import dataclass, field
from app.calculator import Calculation

@dataclass
class Memento:
    """
    Undo/ Redo functionality
    """

    history: List[Calculation]
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """
        
        """
        
        return {
            'history': [calc.to_dict() for calc in self.history],
            'timestamp': self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Memento':
        """
        Pull from dictionary
        """

        return cls(
            history = [Calculation.from_dict(calc) for calc in data['history']],
            timestamp=datetime.datetime.fromisoformat(data['timestamp'])
        )
