# B3 Asset Monitor

O **B3 Asset Monitor** é um sistema projetado para auxiliar os investidores nas suas decisões de comprar ou vender ativos. O sistema rastreia periodicamente a cotação atual de ativos da B3 e notifica o usuário via e-mail quando uma oportunidade de negociação surge.

## Funcionalidades

- **Interface Web**: Permite que o usuário configure os ativos da B3 a serem monitorados, os parâmetros de túnel de preço (valor máximo e mínimo) e a periodicidade da checagem.
- **Monitoramento de Cotações**: O sistema obtém e armazena as cotações dos ativos cadastrados de uma fonte pública.
- **Consulta de Preços**: Os preços armazenados dos ativos cadastrados podem ser consultados através da interface web.
- **Notificações por E-mail**: O sistema envia um e-mail para o investidor sugerindo a compra ou venda de um ativo baseado nos limites do túnel de preço.

## Configuração Rápida

1. Clone o repositório:
   ```bash
   git clone https://github.com/apenasweber/b3_inoa.git
   ```
2. Renomeie o arquivo .env-example para .env e insira as informações necessárias, como servidor de email.
3. Navegue até o diretório do projeto:
   ```bash
   cd b3_inoa
   ```
4. Execute o projeto com:
   ```bash
   make run
   ```
5. Acesse [http://localhost:8000/admin](http://localhost:8000/admin)
6. Logue com user: admin e password: admin
7. Clique em Assets ou Add Assets para inserir o asset desejado para monitoria.

## Testes unitários:

```bash
make test
```

## Base de Dados

### Tabela: Asset

- **ticker**: Código do ativo na B3.
- **lower_limit**: Limite inferior do túnel de preço.
- **upper_limit**: Limite superior do túnel de preço.
- **check_interval**: Intervalo de checagem do preço do ativo.
- **email**: Endereço de e-mail para notificações.
- **email_sent**: Indica se um e-mail de alerta foi enviado.

### Tabela: Quotation

- **asset**: Relaciona-se com a tabela Asset.
- **price**: Preço do ativo.
- **created_at**: Data de criação do registro.
- **updated_at**: Data da última atualização.
- **timestamp**: Data e hora da cotação.

## Observações

- Os tempos de checagem do preço dos tickers inicia em 30 minutos por conta da API escolhida, a **BRAPI**, que atualiza a cada 30mins: [BRAPI Docs](https://brapi.dev/docs)
- O código contém logs e no próprio console conseguimos visualizá-los para entendermos o que está sendo feito.
- Ao invés de construir frontend, usei a própria interface web do Django por atender a todos requisitos de forma mais rápida e eficiente. Afinal, soluções simples e funcionais são as melhores para desafios de código, em minha humilde percepção.
