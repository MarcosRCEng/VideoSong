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
  dev: interface reorganizada em etapas claras para URL e revisao do fluxo antes do download
  test: `python -m pytest -q`
  commit: pronto para registrar

- [x] Implementar escolha entre video e audio
  dev: selecao entre `video` e `audio` com resumo dinamico e status coerente com a escolha
  test: `python -m pytest -q`
  commit: pronto para registrar

- [x] Implementar escolha de pasta de destino
  dev: etapa visual de pasta adicionada na interface com seletor e resumo atualizado com o destino escolhido
  test: `python -m pytest -q`
  commit: pronto para registrar
- [x] Integrar `yt-dlp` no servico de download
  dev: `download_service.py` passou a iniciar downloads reais com `yt-dlp` para video e audio, e a interface passou a acionar esse fluxo diretamente
  test: `.venv\Scripts\python.exe -m pytest -q`
  commit: pronto para registrar
- [x] Exibir status de sucesso e erro
  dev: mensagens de revisao centralizadas no servico e exibidas na interface com estados visuais de sucesso e erro
  test: `.venv\Scripts\python.exe -m pytest -q`
  commit: pronto para registrar

## Sprint 2 - Qualidade e Entrega

- [ ] Melhorar mensagens e validacoes
- [ ] Adicionar testes dos modulos centrais
- [ ] Preparar empacotamento para Windows
- [ ] Revisar README com instrucoes finais de uso
