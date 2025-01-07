
# Action Recorder - Gravação de Ações de Teclado e Mouse

## Descrição

O **Action Recorder** é um aplicativo desenvolvido em Python para gravar e reproduzir ações do teclado e mouse. Ele permite que o usuário grave ações como cliques de mouse e pressionamento de teclas, salve essas ações e depois as reproduza automaticamente. Ele também permite que o usuário remova e reorganize as ações gravadas.

## Funcionalidades

- **Gravação**: Grave ações de teclado e mouse (como cliques e atalhos de teclado) com a capacidade de parar a gravação a qualquer momento pressionando a tecla "Esc".
- **Reprodução**: Reproduza as ações gravadas com o atraso entre as ações definidas.
- **Edição**: Reorganize as ações gravadas através de de mover as ações para cima ou para baixo.
- **Limpeza**: Limpe todas as ações gravadas.
- **Remoção de Ações**: Remova ações específicas da lista de ações.
- **Sleep**: Adicione um tempo de espera (sleep) entre as ações.
  
## Requisitos

Para executar o **Action Recorder**, você precisará instalar as dependências necessárias. Você pode fazer isso utilizando o arquivo `requirements.py`.

### Pacotes necessários:
- **pyautogui**: Para simular eventos do mouse e teclado.
- **keyboard**: Para detectar as teclas pressionadas no teclado.
- **pynput**: Para detectar eventos de clique do mouse.
- **tk**: Biblioteca de interface gráfica para criar a janela e os controles.

### Instalando Dependências

Execute o arquivo `requirements.py` para instalar todos os pacotes necessários:

```sh
python requirements.py
```

Isso garantirá que todos os pacotes necessários sejam instalados automaticamente.

## Como Usar

1. **Iniciar Gravação**:
   - Clique no botão "Gravar" para começar a gravar suas ações de teclado e mouse.
   - Durante a gravação, pressione as teclas ou clique com o mouse como desejar.
   - Para parar a gravação, pressione a tecla "Esc".

2. **Reproduzir Ações**:
   - Após gravar, clique no botão "Reproduzir" para executar as ações gravadas.

3. **Editar Ações**:
   - Você pode mover as ações para cima ou para baixo usando os botões "Subir Ação" ou "Descer Ação".
   - As ações podem ser removidas da lista clicando em "Remover Ação".

4. **Limpar Ações**:
   - Clique no botão "Limpar Ações" para apagar todas as ações gravadas.

## Como Funciona

- O programa grava as ações feitas com o teclado e mouse. Ele armazena essas ações em uma lista que é salva em um arquivo `acoes_gravadas.pkl`.
- As ações incluem pressionamento de teclas, cliques de mouse e até atalhos de teclado como **Ctrl+C** e **Ctrl+V**.
- As ações podem ser reproduzidas, respeitando os tempos de delay entre elas, permitindo simular a interação humana.

## Estrutura do Projeto

- `action_recorder.py`: Código principal que contém a lógica de gravação, reprodução, edição e manipulação das ações.
- `requirements.py`: Script para instalar as dependências necessárias.

## Como Executar o Programa

1. Clone ou baixe o repositório.
2. Instale as dependências usando o comando:

   ```sh
   python requirements.py
   ```

3. Execute o script principal:

   ```sh
   python action_recorder.py
   ```

4. A interface gráfica será aberta, e você poderá começar a gravar, editar e reproduzir as ações de teclado e mouse.

## Contribuições

Sinta-se à vontade para contribuir com o projeto. Você pode melhorar a funcionalidade, adicionar novos recursos ou corrigir bugs. Basta criar um **fork** do projeto e enviar um **pull request** com suas melhorias.
