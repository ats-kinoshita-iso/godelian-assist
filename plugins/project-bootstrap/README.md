# project-bootstrap

Initialize a new Godot 4.x game project with the full godelian-assist structure in one guided session.

## Skills

| Skill | Invocation | Description |
|---|---|---|
| new-project | `/new-project` | Run all 7 initialization steps |
| configure-quality | `/configure-quality` | Install gdtoolkit, create .gdlintrc, set up GdUnit4 |
| setup-autoloads | `/setup-autoloads` | Create EventBus, GameManager, SaveManager singletons |
| setup-directories | `/setup-directories` | Create the standard src/assets/scenes/plans layout |

## Typical Flow

```
/new-project      → runs steps 1–7, calling sub-skills as needed
/configure-quality → adds linting and test infrastructure
/brief            → start designing your first feature
```
