"""
Vectra Native Project Management & Session Recovery Subsystem
"""

import os
import json
from typing import List, Dict, Any, Optional

class VectraProject:
    def __init__(self, name: str, root_path: str, entry_script: str = "main.m"):
        self.name = name
        self.root_path = os.path.abspath(root_path)
        self.entry_script = entry_script
        self.version = "0.1.0"
        self.config_file = os.path.join(self.root_path, "project.vectra")

    def save(self):
        os.makedirs(self.root_path, exist_ok=True)
        data = {
            "name": self.name,
            "version": self.version,
            "entry_script": self.entry_script,
            "created_by": "Vectra Desktop 0.1.0"
        }
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def load(cls, config_path: str) -> 'VectraProject':
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Project configuration file not found: {config_path}")
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        root = os.path.dirname(config_path)
        proj = cls(data.get("name", "Untitled"), root, data.get("entry_script", "main.m"))
        proj.version = data.get("version", "0.1.0")
        return proj

