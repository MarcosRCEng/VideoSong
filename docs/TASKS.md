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
  commit: aguardando autorizacao

- [x] Implementar escolha entre video e audio
  dev: interface permite selecionar entre `video` e `audio` por radio buttons
  test: `python -m pytest -q`
  commit: aguardando autorizacao

- [ ] Implementar escolha de pasta de destino
- [ ] Integrar `yt-dlp` no servico de download
- [x] Exibir status de sucesso e erro
  dev: interface atualizada para destacar URL, formato e feedback visual de sucesso ou erro
  test: `python -m pytest -q`
  commit: aguardando autorizacao

## Sprint 2 - Qualidade e Entrega

- [ ] Melhorar mensagens e validacoes
- [ ] Adicionar testes dos modulos centrais
- [ ] Preparar empacotamento para Windows
- [ ] Revisar README com instrucoes finais de uso
