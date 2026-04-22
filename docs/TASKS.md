# VideoSong Tasks

Legenda:

* `[ ]` pendente
* `[-]` em andamento
* `[x]` concluido

Regra do projeto:
Cada tarefa relevante deve ser atualizada em tres momentos quando aplicavel:

* `dev`: implementacao realizada
* `test`: validacao executada
* `commit`: pronto para registrar no Git

---

## Sprint 0 - Base do Projeto

Status: Concluido

* [x] Criar repositorio local com remoto GitHub configurado
  dev: repositorio Git local encontrado e remoto `origin` validado
  test: `git remote -v` e `git status --short --branch`
  commit: pronto

* [x] Criar estrutura inicial do projeto
  dev: pastas `docs`, `src/videosong`, `src/videosong/ui` e `tests`
  test: validacao visual da arvore local
  commit: pronto

* [x] Criar documentacao curta de produto e fluxo
  dev: `README.md`, `docs/VIBE_PLAN.md` e `docs/TASKS.md`
  test: revisao manual do conteudo
  commit: pronto

* [x] Criar ambiente virtual `.venv`
  dev: `.venv` criado localmente
  test: interpreter do ambiente validado e pronto para uso
  commit: pronto

* [x] Instalar dependencias do projeto
  dev: `yt-dlp`, `pytest` e `pip` instalados no `.venv`
  test: instalacao validada com `python -m pytest -q` e `python -m pip --version`
  commit: pronto

* [x] Adicionar app inicial em `tkinter`
  dev: `main.py`, `src/videosong/app.py` e `src/videosong/ui/main_window.py`
  test: importacao de `MainWindow` validada no `.venv`
  commit: pronto

* [x] Adicionar teste minimo de importacao/execucao basica
  dev: `tests/test_imports.py`
  test: `python -m pytest -q` executado com sucesso
  commit: pronto

---

## Sprint 1 - Download Minimo Viavel

Status: Concluido

* [x] Definir fluxo de entrada da URL
  dev: interface exibe a etapa de URL e resumo dinamico do fluxo
  test: `python -m pytest -q`
  commit: realizado no historico atual do projeto

* [x] Implementar escolha entre video e audio
  dev: interface permite selecionar entre `video` e `audio` por radio buttons
  test: `python -m pytest -q`
  commit: realizado no historico atual do projeto

* [x] Implementar escolha de pasta de destino
  dev: interface permite escolher uma pasta local e inclui o destino no resumo e na validacao do fluxo
  test: `python -m pytest -q`
  commit: realizado na branch `codex/task-escolha-pasta-destino-atual`

* [x] Integrar `yt-dlp` no servico de download
  dev: `download_service.py` adicionado e integrado a interface para iniciar o download real com `yt-dlp`
  test: `python -m pytest -q`
  commit: realizado na branch `codex/task-integracao-real-yt-dlp-atual`

* [x] Exibir status de sucesso e erro
  dev: interface atualizada para destacar URL, formato e feedback visual de sucesso ou erro
  test: `python -m pytest -q`
  commit: realizado na branch `codex/task-status-sucesso-erro`

* [x] Nome automatico do arquivo
  dev: configurado via `yt-dlp`
  test: validacao manual
  commit: realizado

* [x] Feedback de status (basico)
  dev: mensagens simples na UI
  test: validacao manual
  commit: realizado

---

## Sprint 2 - Qualidade e Entrega

Status: Concluido

* [x] Melhorar mensagens e validacoes
  dev: interface orienta melhor o fluxo de URL e formato, com mensagens distintas para URL vazia, URL invalida e fluxo validado
  test: `python -m pytest -q`
  commit: realizado na branch `codex/task-melhorar-mensagens-e-validacoes`

* [x] Adicionar testes dos modulos centrais
  dev: testes unitarios adicionados para validacao de URL, resumo do fluxo e mensagens/status centrais da interface
  test: `python -m pytest -q`
  commit: realizado na branch `codex/task-testes-modulos-centrais`

* [x] Preparar empacotamento para Windows
  dev: `requirements-dev.txt`, `VideoSong.spec` e `scripts/build_windows.ps1` adicionados com base minima de PyInstaller para gerar `dist\VideoSong.exe`
  test: `python -m pytest -q` e `.\scripts\build_windows.ps1`
  commit: realizado na branch `codex/task-preparar-empacotamento-windows`

* [x] Atualizar empacotamento Windows com build regenerado
  dev: `scripts/build_windows.ps1` ajustado para limpar artefatos antigos e regenerar `dist\VideoSong.exe` a partir do estado atual do projeto
  test: `python -m pytest -q` e `.\scripts\build_windows.ps1`
  commit: aguardando autorizacao

* [x] Revisar README com instrucoes finais de uso
  dev: `README.md` atualizado com estado atual do app, fluxo de uso, validacao local e empacotamento Windows
  test: revisao manual do conteudo e `python -m pytest -q`
  commit: aguardando autorizacao

* [x] Tratamento de erros
  dev: try/except com log
  test: simulacao de erro
  commit: realizado

* [x] Logger de erros
  dev: arquivo `error_log.py`
  test: escrita em arquivo
  commit: realizado

* [x] Testes unitarios basicos
  dev: criados testes iniciais
  test: `pytest`
  commit: realizado

* [x] README inicial
  dev: documentacao basica
  test: revisao manual
  commit: realizado

* [x] Build executavel Windows
  dev: PyInstaller configurado
  test: execucao do `.exe`
  commit: realizado

---

## Backlog Pos-Projeto

Status: Parcialmente concluido

* [x] Padronizar formatos finais de download para `.mp4` e `.mp3`
  dev: ajustar o fluxo para salvar video final em `.mp4` e somente audio final em `.mp3`
  test: validar o comportamento do servico de download e atualizar os testes automatizados
  commit: aguardando autorizacao

* [x] Versionar o executavel `.exe` a cada sprint fechada
  dev: `scripts/build_windows.ps1` agora exige `-ReleaseLabel` e, alem de regenerar `dist\VideoSong.exe`, copia um artefato versionado para `dist\releases\VideoSong-<release>.exe`; `README.md` documenta o fluxo minimo de release por sprint
  test: validar `python -m pytest -q` e `.\scripts\build_windows.ps1 -ReleaseLabel sprint-2`, confirmando a presenca de `dist\releases\VideoSong-sprint-2.exe`
  commit: realizado na branch `codex/task-logs-erro-e-build-final-exe`

* [x] Configurar runtime JavaScript compativel com `yt-dlp` para URLs do YouTube
  dev: `download_service.py` passou a validar se `node` esta realmente executavel antes de habilitar `js_runtimes`; quando a URL e do YouTube e nao ha runtime suportado, o app interrompe com orientacao objetiva em vez de deixar o aviso interno do `yt-dlp`; `scripts/setup_windows.ps1` foi adicionado para instalar/verificar `Node.js` LTS no Windows e o `README.md` passou a documentar esse pre-requisito fora do `requirements.txt`
  test: `.\.venv\Scripts\python.exe -m pytest -q`, checagem local confirmando que o `node.exe` encontrado em `WindowsApps` nao esta utilizavel como runtime para o `yt-dlp` e validacao de sintaxe do script `.\scripts\setup_windows.ps1`
  commit: realizado na branch `codex/task-runtime-js-ytdlp`

* [x] Garantir `ffmpeg` e `ffprobe` no fluxo de download de video e audio
  dev: `download_service.py` passou a localizar `ffmpeg` e `ffprobe` no ambiente e tambem nos binarios empacotados pelo PyInstaller; `scripts/setup_windows.ps1` agora instala/verifica `Node.js`, `ffmpeg` e `ffprobe`; `scripts/build_windows.ps1` passou a bloquear build incompleto e `VideoSong.spec` embute `ffmpeg/ffprobe` no pacote final quando encontrados
  test: validacao automatizada do Python e validacao de sintaxe/execucao dos scripts de setup e build no Windows
  commit: pendente

* [x] Adicionar gravacao simples de logs de erro para diagnostico local
  dev: `src/videosong/services/error_log.py` adicionado para registrar erros em `logs\videosong-errors.log`; falhas de download relevantes e excecoes nao tratadas da aplicacao/interface agora escrevem no log local e devolvem referencia objetiva ao arquivo
  test: validar `python -m pytest -q` cobrindo gravacao do log e mensagens de erro com caminho do arquivo
  commit: realizado na branch `codex/task-logs-erro-e-build-final-exe`

---

## Sprint 3 - Nova Experiencia de Interface (Wizard + Lista)

Objetivo: eliminar a tela unica, evitar corte visual e introduzir fluxo estruturado com suporte a multiplas URLs.

* [x] Refatorar arquitetura da UI para fluxo por etapas
  dev: extrair WizardState e preparar MainWindow para renderizar a etapa ativa com navegacao
  test: navegacao entre etapas e estado central cobertos com pytest
  commit: pendente

* [x] Criar etapa de configuracao global
  dev: selecao de formato (video/audio)
  test: persistencia durante fluxo + pytest
  commit: pendente

* [x] Criar etapa de pasta de destino
  dev: tela dedicada para escolha de pasta
  test: validacao de selecao + pytest
  commit: pendente

* [x] Criar etapa de lista de URLs
  dev: adicionar, remover e listar URLs
  test: validacao de lista e entradas invalidas + pytest
  commit: pendente

* [x] Permitir colar multiplas URLs (uma por linha)
  dev: parser testavel para texto multiline com deduplicacao simples, separacao entre URLs validas e invalidas e integracao com a lista existente sem quebrar a adicao manual
  test: validacao de multiplas entradas, duplicidades e integracao da colagem em lote + `python -m pytest -q` via `.venv`
  commit: pendente

* [x] Criar etapa de revisao e execucao
  dev: resumo final com formato, pasta, quantidade de URLs, estado pronto para execucao e disparo minimo preservando o servico atual pela primeira URL
  test: resumo final, bloqueio de avance sem pasta/URLs obrigatorias + `python -m pytest -q`
  commit: pendente

* [x] Corrigir responsividade da janela
  dev: reorganizar a shell da janela com `grid`, ajustar `geometry`/`minsize`, distribuir pesos com `columnconfigure`/`rowconfigure` e recalcular `wraplength` no resize para reduzir cortes visuais nas etapas do wizard
  test: cobertura de wrap responsivo + `python -m pytest -q` e validacao manual em tamanhos reduzidos/redimensionamento da janela
  commit: pendente

---

## Sprint 4 - Persistencia e Conveniencia

Objetivo: reduzir friccao entre usos do aplicativo.

* [ ] Criar servico de configuracoes persistentes
  dev: `settings_service.py` com armazenamento local (JSON)
  test: leitura/escrita + pytest
  commit: pendente

* [ ] Memorizar ultima pasta utilizada
  dev: salvar e restaurar automaticamente
  test: persistencia entre execucoes + pytest
  commit: pendente

* [ ] Definir pasta padrao inteligente
  dev: Videos (video) / Music (audio)
  test: validacao de fallback + pytest
  commit: pendente

* [ ] Memorizar ultimo formato usado
  dev: restaurar configuracao anterior
  test: persistencia + pytest
  commit: pendente

---

## Sprint 5 - Fila de Downloads

Objetivo: suportar multiplas URLs com processamento em lote.

* [ ] Criar modelo de item de download
  dev: estrutura com estado, progresso e mensagem
  test: validacao de estados + pytest
  commit: pendente

* [ ] Implementar execucao sequencial da fila
  dev: processar URLs uma a uma
  test: multiplos downloads + pytest
  commit: pendente

* [ ] Exibir status por item
  dev: aguardando, baixando, concluido, erro
  test: transicoes de estado + pytest
  commit: pendente

* [ ] Exibir resumo global da fila
  dev: total, concluidos, erros
  test: consistencia de contadores + pytest
  commit: pendente

* [ ] Bloquear edicao durante execucao
  dev: desabilitar controles ativos
  test: validacao de bloqueio + pytest
  commit: pendente

---

## Sprint 6 - Progresso em Tempo Real e Assincronia

Objetivo: UI responsiva e feedback completo de download.

* [ ] Executar downloads em thread separada
  dev: uso de threading + fila de eventos
  test: UI responsiva + pytest
  commit: pendente

* [ ] Integrar progress_hooks do yt-dlp
  dev: capturar percentual, velocidade e ETA
  test: validacao de eventos + pytest
  commit: pendente

* [ ] Exibir progresso por item
  dev: barra individual por download
  test: atualizacao dinamica + pytest
  commit: pendente

* [ ] Exibir progresso global
  dev: percentual total da fila
  test: calculo agregado + pytest
  commit: pendente

* [ ] Exibir tempo, velocidade e ETA
  dev: indicadores em tempo real
  test: validacao de exibicao + pytest
  commit: pendente

---

## Sprint 7 - Polimento Final

Objetivo: melhorar controle e experiencia final.

* [ ] Botao abrir pasta ao final
  dev: abrir explorer automaticamente
  test: validacao manual + pytest
  commit: pendente

* [ ] Melhorar mensagens de erro por item
  dev: feedback claro por URL
  test: simulacao de erro + pytest
  commit: pendente

* [ ] Limpar fila apos execucao
  dev: remover itens concluidos
  test: validacao da lista + pytest
  commit: pendente

* [ ] Cancelar downloads em execucao
  dev: interromper fila com seguranca
  test: validacao de cancelamento + pytest
  commit: pendente

* [ ] Atualizar README e documentacao
  dev: refletir nova arquitetura e fluxo
  test: revisao manual
  commit: pendente

---

## Backlog Futuro (Nao Prioritario)

* [ ] Downloads paralelos configuraveis
* [ ] Formato por item (nao global)
* [ ] Reordenacao de fila (drag and drop)
* [ ] Historico de downloads
* [ ] Drag and drop de URLs
* [ ] Retry automatico em falhas
