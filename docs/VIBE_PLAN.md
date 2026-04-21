# VideoSong Vibe Plan

## North Star

Entregar um aplicativo desktop pequeno, confiavel e facil de manter para baixar videos da internet localmente, com opcao clara para extrair somente audio.

## Produto em Uma Frase

"Colar URL, escolher formato, clicar e salvar sem complicacao."

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
- componentes simples: URL, tipo de download, pasta, botao, status

### Aplicacao

- `app.py` para bootstrap
- `ui/main_window.py` para a janela e eventos

### Servicos

- futuro `services/download_service.py` para encapsular `yt-dlp`
- futuro `services/file_service.py` para paths, nomes e pasta destino

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
