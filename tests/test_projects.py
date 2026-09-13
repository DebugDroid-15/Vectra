import pytest
import os
from kheramat.projects import VectraProject

def test_project_save_load(tmp_path):
    proj_dir = tmp_path / "MyECEProject"
    proj = VectraProject("MyECEProject", str(proj_dir), "main.m")
    proj.save()

    config_file = proj_dir / "project.vectra"
    assert config_file.exists()

    loaded = VectraProject.load(str(config_file))
    assert loaded.name == "MyECEProject"
    assert loaded.entry_script == "main.m"

