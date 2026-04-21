# VideoSong Tasks

Legenda:

- `[ ]` pendente
- `[-]` em andamento
- `[x]` concluido

Regra do projeto:

Cada tarefa relevante deve ser atualizada em tres momentos quando aplicavel:

- `dev`: implementacao realizada
- `test`: validacao executada
- `commit`: pronto para registrar no Git

## Sprint 0 - Base do Projeto

- [x] Criar repositorio local com remoto GitHub configurado
  dev: repositorio Git local encontrado e remoto `origin` validado
  test: `git remote -v` e `git status --short --branch`
  commit: pronto

- [x] Criar estrutura inicial do projeto
  dev: pastas `docs`, `src/videosong`, `src/videosong/ui` e `tests`
  test: validacao visual da arvore local
  commit: pronto

- [x] Criar documentacao curta de produto e fluxo
  dev: `README.md`, `docs/VIBE_PLAN.md` e `docs/TASKS.md`
  test: revisao manual do conteudo
  commit: pronto

- [x] Criar ambiente virtual `.venv`
  dev: `.venv` criado localmente
  test: interpreter do ambiente validado e pronto para uso
  commit: pronto

- [x] Instalar dependencias do projeto
  dev: `yt-dlp`, `pytest` e `pip` instalados no `.venv`
  test: instalacao validada com `python -m pytest -q` e `python -m pip --version`
  commit: pronto

- [x] Adicionar app inicial em `tkinter`
  dev: `main.py`, `src/videosong/app.py` e `src/videosong/ui/main_window.py`
  test: importacao de `MainWindow` validada no `.venv`
  commit: pronto

- [x] Adicionar teste minimo de importacao/execucao basica
  dev: `tests/test_imports.py`
  test: `python -m pytest -q` executado com sucesso
  commit: pronto

## Sprint 1 - Download Minimo Viavel

- [x] Definir fluxo de entrada da URL
  dev: interface exibe a etapa de URL e resumo dinamico do fluxo
  test: `python -m pytest -q`
  commit: realizado no historico atual do projeto

- [x] Implementar escolha entre video e audio
  dev: interface permite selecionar entre `video` e `audio` por radio buttons
  test: `python -m pytest -q`
  commit: realizado no historico atual do projeto

- [x] Implementar escolha de pasta de destino
  dev: interface permite escolher uma pasta local e inclui o destino no resumo e na validacao do fluxo
  test: `python -m pytest -q`
  commit: aguardando autorizacao
- [ ] Integrar `yt-dlp` no servico de download
- [x] Exibir status de sucesso e erro
  dev: interface atualizada para destacar URL, formato e feedback visual de sucesso ou erro
  test: `python -m pytest -q`
  commit: realizado na branch `codex/task-status-sucesso-erro`

## Sprint 2 - Qualidade e Entrega

- [x] Melhorar mensagens e validacoes
  dev: interface orienta melhor o fluxo de URL e formato, com mensagens distintas para URL vazia, URL invalida e fluxo validado
  test: `python -m pytest -q`
  commit: realizado na branch `codex/task-melhorar-mensagens-e-validacoes`
- [x] Adicionar testes dos modulos centrais
  dev: testes unitarios adicionados para validacao de URL, resumo do fluxo e mensagens/status centrais da interface
  test: `python -m pytest -q`
  commit: realizado na branch `codex/task-testes-modulos-centrais`
- [x] Preparar empacotamento para Windows
  dev: `requirements-dev.txt`, `VideoSong.spec` e `scripts/build_windows.ps1` adicionados com base minima de PyInstaller para gerar `dist\VideoSong.exe`
  test: `python -m pytest -q` e `.\scripts\build_windows.ps1`
  commit: realizado na branch `codex/task-preparar-empacotamento-windows`
- [ ] Revisar README com instrucoes finais de uso
