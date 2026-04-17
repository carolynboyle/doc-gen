# 2026JAN17overview.mmd

**Path:** docs/mermaid/current/2026JAN17overview.mmd
**Syntax:** text
**Generated:** 2026-03-26 19:01:15

```
flowchart TD
    Start([Start])

    subgraph UI["User Interfaces"]
        Menu["menu.py"]
        CLI["cli.py"]
    end

    subgraph Engine["engine.py"]
        Scan["scan_project"]
        BuildManifest["build_manifest"]
        Render["render_docs"]
        Status["status"]
        Reset["reset_runtime"]
    end

    subgraph Core["Core Data"]
        FSTree["Filesystem Tree"]
        Manifest["Manifest for markdown inputs"]
    end

    subgraph Runtime["Runtime"]
        State["Load and save state"]
        Backups["Backups"]
    end

    Start --> Menu
    Start --> CLI

    Menu --> Engine
    CLI --> Engine

    Scan --> FSTree
    FSTree --> BuildManifest
    BuildManifest --> Manifest
    BuildManifest --> State

    Manifest --> Render
    Render --> Backups

    Status --> Manifest
    Reset --> Backups

```
