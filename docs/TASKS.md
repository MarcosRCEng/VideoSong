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
  commit: realizado na branch `codex/task-atualizar-empacotamento-windows`

* [x] Revisar README com instrucoes finais de uso
  dev: `README.md` atualizado com estado atual do app, fluxo de uso, validacao local e empacotamento Windows
  test: revisao manual do conteudo e `python -m pytest -q`
  commit: realizado na branch `codex/task-revisar-readme-uso-final`

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
  commit: realizado na branch `codex/task-formatos-mp4-mp3`

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
  commit: realizado na branch `codex/task-ffmpeg-ffprobe-download`

* [x] Adicionar gravacao simples de logs de erro para diagnostico local
  dev: `src/videosong/services/error_log.py` adicionado para registrar erros em `logs\videosong-errors.log`; falhas de download relevantes e excecoes nao tratadas da aplicacao/interface agora escrevem no log local e devolvem referencia objetiva ao arquivo
  test: validar `python -m pytest -q` cobrindo gravacao do log e mensagens de erro com caminho do arquivo
  commit: realizado na branch `codex/task-logs-erro-e-build-final-exe`

* [x] Adicionar instalador Windows com documentacao de distribuicao
  dev: `scripts\VideoSongInstaller.iss`, `scripts\build_installer.ps1` e `scripts\build_installer.cmd` adicionados para gerar um instalador Windows baseado em Inno Setup a partir de `dist\VideoSong.exe`; `README.md` agora documenta a geracao e o uso do `VideoSong-<release>-setup.exe`
  test: compilacao local validada com `scripts\build_installer.cmd local`, confirmando a geracao de `dist\releases\VideoSong-local-setup.exe`
  commit: realizado na branch `codex/task-doc-installer-windows`

---

## Sprint 3 - Nova Experiencia de Interface (Wizard + Lista)

Objetivo: eliminar a tela unica, evitar corte visual e introduzir fluxo estruturado com suporte a multiplas URLs.

* [x] Refatorar arquitetura da UI para fluxo por etapas
  dev: extrair WizardState e preparar MainWindow para renderizar a etapa ativa com navegacao
  test: navegacao entre etapas e estado central cobertos com pytest
  commit: realizado na branch `codex/task-sprint3-base-wizard`

* [x] Criar etapa de configuracao global
  dev: selecao de formato (video/audio)
  test: persistencia durante fluxo + pytest
  commit: realizado na branch `codex/task-sprint3-etapa-config-destino`

* [x] Criar etapa de pasta de destino
  dev: tela dedicada para escolha de pasta
  test: validacao de selecao + pytest
  commit: realizado na branch `codex/task-sprint3-etapa-config-destino`

* [x] Criar etapa de lista de URLs
  dev: adicionar, remover e listar URLs
  test: validacao de lista e entradas invalidas + pytest
  commit: realizado na branch `codex/task-sprint3-lista-urls`

* [x] Permitir colar multiplas URLs (uma por linha)
  dev: parser testavel para texto multiline com deduplicacao simples, separacao entre URLs validas e invalidas e integracao com a lista existente sem quebrar a adicao manual
  test: validacao de multiplas entradas, duplicidades e integracao da colagem em lote + `python -m pytest -q` via `.venv`
  commit: realizado na branch `codex/task-sprint3-colagem-multipla`

* [x] Criar etapa de revisao e execucao
  dev: resumo final com formato, pasta, quantidade de URLs, estado pronto para execucao e disparo minimo preservando o servico atual pela primeira URL
  test: resumo final, bloqueio de avance sem pasta/URLs obrigatorias + `python -m pytest -q`
  commit: realizado na branch `codex/task-sprint3-revisao-execucao`

* [x] Corrigir responsividade da janela
  dev: reorganizar a shell da janela com `grid`, ajustar `geometry`/`minsize`, distribuir pesos com `columnconfigure`/`rowconfigure` e recalcular `wraplength` no resize para reduzir cortes visuais nas etapas do wizard
  test: cobertura de wrap responsivo + `python -m pytest -q` e validacao manual em tamanhos reduzidos/redimensionamento da janela
  commit: realizado na branch `codex/task-sprint3-responsividade`

---

## Sprint 4 - Persistencia e Conveniencia

Objetivo: reduzir friccao entre usos do aplicativo.

* [x] Criar servico de configuracoes persistentes
  dev: `settings_service.py` criado com API simples para carregar/salvar configuracoes em JSON local, fallback seguro para arquivo ausente e JSON invalido, e exportacao via `services.__init__`
  test: `.\.venv\Scripts\python.exe -m pytest -q tests/test_settings_service.py`
  commit: realizado na branch `codex/task-sprint4-settings-service`

* [x] Memorizar ultima pasta utilizada
  dev: `MainWindow` agora salva automaticamente a pasta escolhida no wizard via `settings_service` e restaura esse destino ao abrir o app; quando nao existe pasta salva, o fluxo preserva a regra da pasta padrao inteligente
  test: `.\.venv\Scripts\python.exe -m pytest -q tests/test_settings_service.py tests/test_wizard_config_steps.py tests/test_imports.py`
  commit: realizado na branch `codex/task-sprint4-settings-service`

* [x] Definir pasta padrao inteligente
  dev: `settings_service.py` agora resolve a pasta padrao com prioridade para `Videos` no modo `video` e `Music` no modo `audio`, com fallback seguro para a `home`; `MainWindow` passa a iniciar com esse destino e troca entre defaults ao mudar o modo enquanto o usuario ainda nao escolheu uma pasta manual
  test: `.\.venv\Scripts\python.exe -m pytest -q tests/test_settings_service.py tests/test_imports.py`
  commit: realizado na branch `codex/task-sprint4-settings-service`

* [x] Memorizar ultimo formato usado
  dev: `MainWindow` agora salva a ultima escolha entre `video` e `audio` no `settings_service` assim que o formato muda e restaura essa preferencia ao abrir a janela, preservando a logica atual da UI e da pasta padrao inteligente por modo
  test: `.\.venv\Scripts\python.exe -m pytest -q tests/test_settings_service.py tests/test_wizard_config_steps.py tests/test_imports.py`
  commit: realizado na branch `codex/task-sprint4-settings-service`

---

## Sprint 5 - Fila de Downloads

Objetivo: suportar multiplas URLs com processamento em lote.

* [x] Criar modelo de item de download
  dev: `download_queue.py` introduz `DownloadItem` com estado e mensagem, `WizardState` expoe a fila derivada de forma nao intrusiva e `MainWindow` ja inicia a execucao a partir do primeiro item dessa fila, sem progresso em tempo real ainda
  test: `.\.venv\Scripts\python.exe -m pytest -q tests/test_imports.py tests/test_wizard_review.py`
  commit: realizado na branch `codex/task-sprint5-download-item-model`

* [x] Implementar execucao sequencial da fila
  dev: `MainWindow` agora percorre `self.state.download_items` em ordem, marca cada item como `running` antes do `start_download()`, atualiza para `completed` ou `error` ao final e continua a fila mesmo quando um item falha; mensagens de revisao/resumo foram ajustadas para refletir o processamento sequencial de toda a lista
  test: `.\.venv\Scripts\python.exe -m pytest -q tests/test_imports.py tests/test_wizard_review.py`
  commit: realizado na branch `codex/task-sprint5-download-item-model`

* [x] Exibir status por item
  dev: etapa de revisao agora mostra uma lista por item com URL curta, status e mensagem; `MainWindow` mantem `self.download_items` como colecao executavel viva e atualiza essa fila durante a rodada de download, preservando os estados ja conhecidos quando o fluxo base nao muda
  test: `.\.venv\Scripts\python.exe -m pytest -q tests/test_wizard_review.py tests/test_imports.py`
  commit: realizado na branch `codex/task-sprint5-status-por-item`

* [x] Exibir resumo global da fila
  dev: etapa de revisao agora mostra um resumo global derivado da fila visivel com total, concluidos, erros e em andamento; os contadores usam a mesma colecao renderizada na lista por item e sao atualizados a cada refresh de estado da fila
  test: `.\.venv\Scripts\python.exe -m pytest -q tests/test_wizard_review.py tests/test_imports.py`
  commit: realizado na branch `codex/task-sprint5-resumo-global-fila`

* [x] Bloquear edicao durante execucao
  dev: `MainWindow` agora usa `is_downloading` para desabilitar navegacao e controles editaveis da etapa atual, alem de ignorar handlers de formato, pasta e lista de URLs enquanto a fila estiver em execucao
  test: `.\.venv\Scripts\python.exe -m pytest -q tests/test_imports.py tests/test_wizard_url_list.py tests/test_wizard_review.py`
  commit: realizado na branch `codex/task-sprint5-bloquear-edicao-execucao`

---

## Sprint 6 - Progresso em Tempo Real e Assincronia

Objetivo: UI responsiva e feedback completo de download.

* [x] Executar downloads em thread separada
  dev: `MainWindow` agora inicia a fila em uma `Thread` daemon e aplica atualizacoes na UI por uma fila de eventos consumida com `after()`, mantendo a rodada fora da thread principal do Tk
  test: `.\.venv\Scripts\python.exe -m pytest -q`
  commit: realizado na branch `codex/task-sprint6-thread-separada` (`618168c`)

* [x] Integrar progress_hooks do yt-dlp
  dev: `download_service.py` agora registra `progress_hooks`, normaliza eventos do `yt-dlp` em percentual, velocidade e ETA, e repassa esses dados por item para a fila executada pela UI
  test: `.\.venv\Scripts\python.exe -m pytest -q`
  commit: realizado na branch `codex/task-sprint6-progress-hooks` (`e57b31b`)

* [x] Exibir progresso por item
  dev: etapa de revisao renderiza uma barra individual por item da fila usando o percentual recebido pelos eventos de progresso do download
  test: `.\.venv\Scripts\python.exe -m pytest -q`
  commit: realizado na branch `codex/task-sprint6-progresso-por-item` (`687fda2`)

* [x] Exibir progresso global
  dev: etapa de revisao agora exibe uma barra e um texto de progresso global calculados a partir dos itens visiveis da fila; itens concluidos ou com erro contam como processados, itens em execucao usam o percentual atual e pendentes contam como 0
  test: calculo agregado coberto em pytest e validado com `.\.venv\Scripts\python.exe -m pytest -q`
  commit: realizado na branch `codex/task-sprint6-progresso-global` (`f0ce236`)

* [x] Exibir tempo, velocidade e ETA
  dev: UI de revisao agora exibe tempo decorrido, velocidade e ETA do item atual usando dados normalizados dos `progress_hooks` do `yt-dlp`
  test: exibicao e formatacao cobertas por pytest; `.\.venv\Scripts\python.exe -m pytest -q`
  commit: realizado na branch `codex/task-sprint6-tempo-velocidade-eta` (`5349c02`)

---

## Sprint 7 - Polimento Final

Objetivo: melhorar controle e experiencia final.

* [x] Botao abrir pasta ao final
  dev: botao simples exibido ao final da execucao para abrir a pasta de destino no Explorer sem alterar o fluxo principal de download
  test: `.\.venv\Scripts\python.exe -m pytest -q tests/test_imports.py tests/test_wizard_review.py`
  commit: pronto, aguardando autorizacao

* [x] Melhorar mensagens de erro por item
  dev: mensagens de falha por item revisadas para orientar a acao do usuario sem expor detalhes tecnicos brutos
  test: `.\.venv\Scripts\python.exe -m pytest -q tests/test_imports.py tests/test_wizard_review.py`
  commit: pronto, aguardando autorizacao

* [x] Limpar fila apos execucao
  dev: botao para limpar da interface os itens concluidos apos a execucao, mantendo itens com erro na fila e sem apagar arquivos baixados
  test: `.\.venv\Scripts\python.exe -m pytest -q tests/test_imports.py tests/test_wizard_review.py` e `.\.venv\Scripts\python.exe -m pytest -q`
  commit: pronto, aguardando autorizacao

* [x] Cancelar downloads em execucao
  dev: botao simples para solicitar cancelamento da fila em execucao; o item atual termina com seguranca e os proximos itens sao marcados como cancelados sem iniciar novos downloads
  test: validacao automatizada do cancelamento da fila e `.\.venv\Scripts\python.exe -m pytest -q`
  commit: pronto, aguardando autorizacao

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
