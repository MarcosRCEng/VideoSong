# 🤖 AGENTS.md — Diretrizes para uso com Codex

Este arquivo define regras obrigatórias para qualquer agente automatizado (ex: Codex) que execute tarefas neste repositório.

---

# 📌 REGRAS CRÍTICAS (OBRIGATÓRIO)

## 🌿 Branching

* Sempre usar a branch `main` como base.
* Toda nova tarefa deve criar uma nova branch a partir da `main`.
* Nunca trabalhar diretamente na `main`.
* Nunca criar branch sem ancestral comum com `main`.
* Nunca usar `--orphan` ou iniciar repositório separado.

## 🔄 Fluxo de trabalho

1. Atualizar a `main` local (pull)
2. Criar nova branch:

   * `feature/...`
   * `fix/...`
   * `refactor/...`
3. Implementar a solução
4. Garantir que a branch ainda possui ancestral comum com `main`
5. Entregar código pronto para Pull Request

## 🚫 PROIBIDO

* ❌ `git push --force` na `main`
* ❌ reescrever histórico da `main`
* ❌ criar branches desconectadas
* ❌ alterar configuração do repositório sem necessidade
* ❌ commitar segredos ou credenciais

---

# 🧪 QUALIDADE DE CÓDIGO

## 📦 Estrutura

* Respeitar a arquitetura existente do projeto
* Não misturar responsabilidades (ex: lógica de negócio no controller)

## ✍️ Código

* Código deve ser legível e consistente
* Evitar duplicação
* Seguir princípios SOLID quando aplicável

## 🧪 Testes

* Sempre que possível, adicionar ou atualizar testes
* Garantir que nada quebra funcionalidades existentes

---

# 🔐 SEGURANÇA

* Nunca expor:

  * senhas
  * tokens
  * chaves de API
* Usar variáveis de ambiente para configurações sensíveis

---

# 🔧 PULL REQUEST

## 📌 Regras

* Toda alteração deve ser entregue via Pull Request
* Nunca fazer merge automático sem revisão

## 📝 Formato do título

* `feat: descrição`
* `fix: descrição`
* `refactor: descrição`
* `docs: descrição`

## 📄 Descrição deve conter:

* Objetivo da alteração
* O que foi modificado
* Como testar
* Possíveis impactos

---

# ⚠️ VALIDAÇÃO ANTES DE FINALIZAR

Antes de concluir a tarefa, o agente DEVE verificar:

* [ ] Branch foi criada a partir da `main`
* [ ] Não há divergência de histórico
* [ ] Código compila/roda corretamente
* [ ] Não existem arquivos desnecessários
* [ ] Não há credenciais no código
* [ ] Alteração está isolada e clara

---

# 🧠 COMPORTAMENTO DO AGENTE

Se qualquer uma das condições abaixo ocorrer:

* histórico da branch diferente da `main`
* conflitos não resolvidos
* dúvidas sobre arquitetura

👉 O agente deve PARAR e reportar o problema
👉 NÃO deve tentar resolver de forma destrutiva (force push, reset, etc)

---

# 🚀 OBJETIVO

Garantir:

* consistência de histórico Git
* qualidade de código
* segurança
* fluxo profissional de desenvolvimento

---

# 📌 RESUMO PARA O AGENTE

* Sempre partir da `main`
* Sempre criar branch nova
* Nunca quebrar o histórico
* Sempre entregar via PR
