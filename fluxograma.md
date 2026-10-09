# Estrutura do Fluxo de Triagem e Atendimento (IA)

## 1. Tipos de Interações (Entradas)
* **Reclamação**
* **Pedido de ajuda (Dúvida)**
* **Conversa normal**
* **Abuso/Spam detectado**

---

## 2. Rotina Base de Mensagens
* **Rotina de Mensagens** -> Humano Responde? 
  * **Sim** -> Análise de Resposta -> Análise de contexto.
  * **Não** -> Regras para nova chamada (A definir) -> Guarda informação pra contexto de forma otimizada.

---

## 3. Fluxo de Reclamações e Anomalias
* **Análise comportamental (Humor/Sentimental) (Antena)**
  * **Objetivo:** Identificar sinais de cansaço, sobrecarga, conflito, desmotivação, vontade de sair ou situações graves.
* **Anomalia de comportamento detectada?**
  * **Não** -> Guarda informação pra contexto de forma otimizada.
  * **Sim** -> Avisar liderança (Resume informações encontradas até agora para justificar o sinal encontrado) -> *Rotina de recebimento de notificações da IA pela diretoria (Em um outro bloco).*
* **Possível Problema Identificado:**
  * Avalia gravidade, urgência e sensibilidade.
  * Tenta consultar mais informações para contexto (Se já não tiver).
  * Se ainda não requer ação, mas é útil pra contexto: Arquiva a situação para contexto futuro.
  * Define o melhor canal: **Gerente Direto** ou **RH/Direção** (Quem é o Alvo e o Tema?).

### 3.1. Rota: Gerente Direto
* **Exemplos de atuação:**
  * *Conflitos Horizontais:* "O cara da fritadeira não me ajuda e sobra tudo pra mim". (O gerente tem o poder de mudar a escala ou advertir o colega).
  * *Sobrecarga e Cansaço Crônico:* "Tô dobrando turno direto, não tô aguentando". (O gerente ajusta o ritmo).
  * *Problemas Estruturais/Sistemas:* "O caixa travou e o cliente me xingou". (O gerente precisa saber que o problema não foi lentidão, mas a máquina).
  * *Desmotivação Padrão:* "Não sei se levo jeito pra isso, erro os lanches toda hora". (O gerente entra como treinador para apoiar).
* **Ação:** Informa o colaborador que a situação que ele informou está sendo passada para o gerente pra ele tomar conhecimento. 
* **Próximo Passo:** *Rotina de recebimento de notificações da IA pela gerência (Em um outro bloco).*

### 3.2. Rota: RH / Direção
* **Exemplos de atuação:**
  * *Assédio e Humilhação:* Qualquer relato de abuso moral (gritos, xingamentos constantes), assédio sexual ou racismo/preconceito. O gerente direto não tem treinamento jurídico para lidar com isso; a empresa precisa assumir.
  * *Furos Trabalhistas Graves:* "Não caiu meu vale-transporte" ou "fizeram eu bater o ponto e continuar limpando a loja". Isso gera processo trabalhista massivo, a direção precisa saber na hora.
* **Ação:** Informa o colaborador que a mensagem dele está sendo direcionada ao RH e que a situação vai ser avaliada o mais breve possível. 
* **Próximo Passo:** *Rotina de recebimento de notificações da IA pela diretoria (Em um outro bloco).*

### 3.3. Preparação do Aviso (Comum às rotas)
* Resume e monta a mensagem que vai ser enviada como aviso (motivo, importância, tempo de contatação).
* Dá pra avisar o colaborador que a situação vai ser tratada com seriedade e perguntar se ele deseja informar mais alguma informação extra ou apenas confirmar que quer prosseguir.
* **Pede confirmação do usuário:**
  * *Aceite do usuário* -> Segue fluxo de notificação.
  * *Usuário não aceita* -> Guarda a informação pra contexto.

---

## 4. Fluxo de Pedido de Ajuda (Dúvidas)
* **Ação:** Verifica a dúvida em um RAG de FAQ da empresa.
* **O RAG trouxe informações relevantes?**
  * **Sim:** Utiliza as informações encontradas para tentar sanar a dúvida.
    * *A dúvida foi sanada?*
      * **Sim:** Que bom (N sei o que colocar). -> Guarda a informação pra contexto (Dúvida).
      * **Não:** Tenta explicar de uma forma diferente -> A dúvida foi sanada? (Loop).
  * **Não:** Informa que não possui informações concretas e sugere que a dúvida seja sanada com algum profissional. (Dá pra criar um aviso disso pro gerente).