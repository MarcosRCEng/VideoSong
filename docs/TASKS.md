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

* [x] Criar estrutura de pastas
  dev: estrutura criada em `src/videosong/` com `ui/`, `services/`, `utils/`
  test: `python -m pytest -q`
  commit: realizado

* [x] Criar janela principal com tkinter
  dev: `MainWindow` implementada com layout inicial
  test: execucao manual
  commit: realizado

* [x] Configurar entrada principal do app
  dev: `main.py` com bootstrap
  test: execucao direta
  commit: realizado

---

## Sprint 1 - Download Minimo Viavel

Status: Concluido

* [x] Campo para inserir URL
  dev: implementado na UI
  test: validacao manual
  commit: realizado

* [x] Validar URL basica
  dev: funcao simples de validacao
  test: testes unitarios
  commit: realizado

* [x] Opcao de formato (video/audio)
  dev: radio buttons implementados
  test: validacao manual
  commit: realizado

* [x] Seletor de pasta
  dev: integrado com dialog do sistema
  test: validacao manual
  commit: realizado

* [x] Integrar yt-dlp
  dev: download funcional
  test: execucao real
  commit: realizado

* [x] Nome automatico do arquivo
  dev: configurado via yt-dlp
  test: validacao manual
  commit: realizado

* [x] Feedback de status (basico)
  dev: mensagens simples na UI
  test: validacao manual
  commit: realizado

---

## Sprint 2 - Qualidade e Entrega

Status: Concluido

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

## Sprint 3 - Nova Experiencia de Interface (Wizard + Lista)

Objetivo: eliminar a tela unica, evitar corte visual e introduzir fluxo estruturado com suporte a multiplas URLs.

* [ ] Refatorar arquitetura da UI para fluxo por etapas
  dev: separar a interface em etapas controladas pela janela principal
  test: navegacao entre etapas + pytest
  commit: pendente

* [ ] Criar etapa de configuracao global
  dev: selecao de formato (video/audio)
  test: persistencia durante fluxo + pytest
  commit: pendente

* [ ] Criar etapa de pasta de destino
  dev: tela dedicada para escolha de pasta
  test: validacao de selecao + pytest
  commit: pendente

* [ ] Criar etapa de lista de URLs
  dev: adicionar, remover e listar URLs
  test: validacao de lista e entradas invalidas + pytest
  commit: pendente

* [ ] Permitir colar multiplas URLs (uma por linha)
  dev: parser de texto para lista automatica
  test: validacao de multiplas entradas + pytest
  commit: pendente

* [ ] Criar etapa de revisao e execucao
  dev: resumo da configuracao e quantidade de itens
  test: validacao do resumo + pytest
  commit: pendente

* [ ] Corrigir responsividade da janela
  dev: ajustar layout (grid), dimensoes e comportamento de resize
  test: execucao em diferentes resolucoes + pytest
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
