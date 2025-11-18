# Programa de automação de entrada de dados e extração de informações para SharePoint

> Este programa foi criado para atender a um layout específico e não se destina a outras finalidades!

## Instalação

O programa não requer um procedimento de instalação específico. Basta extrair o arquivo criado na seção de versões para qualquer pasta, de preferência na área de trabalho para facilitar o acesso.

## Configuração

Preencha o arquivo de configuração `mos_bot.conf` com as informações necessárias. Há instruções em português para cada configuração dentro do próprio arquivo. Todos os caminhos inseridos devem ser absolutos.

## Uso

O programa funciona em dois modos: `INSERIR` ou `EXTRAIR`, de acordo com a configuração `OPERACAO` no arquivo `mos_bot.conf`.

### Modo de Inserção (INSERIR)

Neste modo, o programa recupera informações do arquivo `consulta_medicao_completa.xlsx`, que deve estar atualizado na pasta de instalação do programa. Ele usará este arquivo para recuperar as informações necessárias para preencher o SharePoint.

Após carregar a planilha na memória, o programa verificará a existência de arquivos e pastas na pasta indicada na configuração `UPOPATH`. Ele navegará até encontrar a hierarquia de pastas que corresponda à profundidade definida na configuração `PROFUNDIDADE`.

O nome da pasta/arquivo será usado para recuperar as informações relacionadas ao(s) documento(s). Se o programa encontrar as informações, ele as exibirá no SharePoint; caso contrário, ignorará a pasta/arquivo e buscará o próximo.

### Modo de Extração (EXTRAIR)

Neste modo, basta iniciar o programa, que se autenticará, carregará a página de medições e exportará um relatório para a pasta indicada na configuração `ODLPATH`.

O relatório é exportado como um arquivo CSV e, para visualização correta no Excel, deve ser importado usando ferramentas de análise de dados (Microsoft Power Query).

## Solução de problemas

### Problema com atualização do ChromeDriver

O problema com a atualização do ChromeDriver, se deve a alteração do certificado de segurança, causada pela conexão com o NetSkope.

1. Quando o programa tentar realizar a atualização, se estiver na rede do NetSkope ele falhará;
    > Não será possível utilizar o programa enquanto o ChromeDriver não for atualizado;
2. Para atualizar será necessário desabilitar a rede NetSkope e iniciar o programa;
3. Com a rede NetSkope desabilitada, ele conseguirá atualizar, mas falhará na operação;
4. Depois da atualização realizada, reabilite o NetSkope e inicie o programa normalmente.

> Essa atualização é necessária a cada atualização do navegador Google Chrome, geralmente uma vez por mês.
> Fonte: <https://www.oficinadanet.com.br/google/34694-com-que-frequencia-o-google-atualiza-o-chrome>

## Desenvolvimento

Para criar um executável, siga os passos abaixo:

1. Verifique a instalação e as versões dos requisitos:

    ```sh
    # Verifica a instalação e a versão do Python
    # Versão 3.13.7 ou superior
    python --version
    # Verifica a instalação e a versão do Pip
    # Versão 25.2 ou superior
    pip --version
    ```

    > O sistema operacional alvo para este projeto é o Windows.

2. Recomenda-se criar e ativar o ambiente virtual para instalar as dependências:

    ```sh
    # Cria o ambiente virtual
    python -m venv venv
    # Ativa o ambiente virtual
    source venv/Scripts/activate
    # Instala as dependências
    pip install -r requirements.txt
    ```

## Distribuição

1. Use o `PyInstaller` para criar um executável:

    ```sh
    pyinstaller --icon appicon.ico --hidden-import lxml --onefile src/mos_bot.py
    ```

    > O executável será salvo na pasta `dist`, no diretório raiz do projeto.

2. Compacte todos os arquivos relacionados em um arquivo zip:

    ```sh
    zip -j dist/mos_bot.zip readme.md dist/mos_bot.exe src/mos_bot.conf src/mos_bot.path
    cd src && zip -r ../dist/mos_bot.zip chromedriver-win64 && cd ..
    ```
