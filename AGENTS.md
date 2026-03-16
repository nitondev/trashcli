## Project Guidelines  
  
- Repo: https://github.com/nitondev/trashcli  
- Maintainer: Lord J. Hackwell (@nitondev)  
  
### Tooling  
Use the following tools for code quality and development:  
  
- `black`  
- `isort`  
- `ruff`  
- `uv`  
  
### Project Structure  
  
- `src/` - source code  
- `src/commands` - CLI command modules  
- `tests/` - unit tests 
  
### Commit Messages  
  
This project uses **Conventional Commits**.  
  
Format:  
```
<type>(optional scope): <description>  
```  
Rules:  
  
- Use **lowercase**  
- Maximum **40 characters**  
- Be concise and descriptive  
  
Allowed commit types:  
  
- `build:` – build system or dependencies  
- `chore:` – maintenance tasks  
- `ci:` – CI/CD changes  
- `docs:` – documentation changes  
- `style:` – formatting or style only  
- `refactor:` – code restructuring without behavior changes  
- `perf:` – performance improvements  
- `test:` – adding or updating tests  
- `fix:` – bug fixes  
- `feat:` – new features
### Formatting  
  
Run before committing:  
```shell  
ruff check .  
ruff format .
```
