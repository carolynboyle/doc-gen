# modules.mmd

**Path:** docs/mermaid/current/modules.mmd
**Syntax:** text
**Generated:** 2026-03-26 19:01:15

```
flowchart TD
    DocGen["doc_gen package"]

    DocGen --> CLI["cli.py"]
    DocGen --> Menu["menu.py"]
    DocGen --> Engine["engine.py"]

    CLI --> CLI_Main["main"]
    Menu --> Menu_Run["run_menu"]
    Engine --> DGE["DocGenEngine"]
    Engine --> ME["MenuEngine"]

    %% Click targets
    click CLI "../planned/cli-flow.mmd" "CLI execution flow"
    click Menu "../planned/menu-flow.mmd" "Menu execution flow"
    click Engine "../planned/engine-flow.mmd" "Engine internals"

    click DGE "../planned/docgenengine-api.mmd" "DocGenEngine API"
    click ME "../planned/menuengine-flow.mmd" "MenuEngine behavior"

```
