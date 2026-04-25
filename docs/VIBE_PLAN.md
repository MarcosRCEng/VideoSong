# VideoSong Vibe Plan

## North Star

Entregar um aplicativo desktop pequeno, confiavel e facil de manter para baixar uma ou varias URLs localmente, com opcao clara para salvar video completo ou extrair somente audio.

## Produto em Uma Frase

"Escolher formato, montar uma fila de URLs, acompanhar o progresso e salvar sem complicacao."

## Regras de Implementacao

- fazer sempre a menor entrega funcional possivel
- evitar camadas desnecessarias no inicio
- manter nomes e arquivos simples
- preferir implementacoes claras a abstractions prematuras
- cada tarefa deve caber em um contexto curto de conversa
- toda mudanca relevante deve terminar com teste e status atualizado

## Arquitetura Inicial

### Interface

- `tkinter` para janela principal
- wizard em quatro etapas: formato, pasta, lista de URLs e revisao
- fila visivel com status, progresso global e progresso por item
- acoes finais simples: cancelar fila, abrir pasta e limpar itens concluidos

### Aplicacao

- `app.py` para bootstrap
- `ui/main_window.py` para janela, eventos e orquestracao da fila
- modulos pequenos em `ui/` para estado do wizard, mensagens, lista de URLs e resumo da revisao

### Servicos

- `services/download_service.py` encapsula `yt-dlp`, formatos finais, binarios externos e progresso
- `services/download_queue.py` modela os itens da fila
- `services/settings_service.py` salva preferencias locais simples
- `services/error_log.py` grava diagnostico local de falhas relevantes

## Fases

## Fase 1 - Fundacao

- estrutura do repositorio
- ambiente virtual
- dependencias basicas
- janela inicial abrindo corretamente
- arquivo de tarefas e planejamento

## Fase 2 - Download Minimo

- aceitar URL valida
- baixar video em pasta escolhida
- baixar apenas audio
- feedback basico de sucesso e erro

## Fase 3 - Experiencia

- progresso na interface
- validacoes melhores
- bloqueio de clique duplo
- mensagens amigaveis

## Fase 4 - Robustez

- testes dos modulos principais
- configuracoes persistentes simples
- empacotamento para Windows

## Estado Atual do Fluxo

- wizard estruturado em etapas
- suporte a multiplas URLs, incluindo colagem em lote
- fila sequencial com status por item
- execucao em thread separada para manter a UI responsiva
- progresso em tempo real via `progress_hooks` do `yt-dlp`
- tempo, velocidade e ETA quando disponiveis
- cancelamento de fila, abertura da pasta final e limpeza de itens concluidos
- requisitos locais documentados: `Node.js`, `ffmpeg` e `ffprobe`

## Definition of Done

Uma tarefa so deve ser considerada concluida quando:

- a implementacao estiver funcional
- houver validacao minima local
- o status estiver refletido em `docs/TASKS.md`
- a entrega estiver pronta para commit

## Formato de Iteracao

Para economizar contexto e tokens, cada rodada deve responder a quatro perguntas:

1. Qual tarefa vamos atacar agora?
2. Qual e a menor entrega funcional?
3. Como vamos validar?
4. O que precisa ser marcado no checklist?
