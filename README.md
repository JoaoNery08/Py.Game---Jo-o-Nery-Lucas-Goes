# Py.Game---Jo-o-Nery-Lucas-Goes
Desenvolvimento do Py.Game

**Título:** Z-Crusher
**Integrantes:** João Nery Filho e Lucas Góes de Almeida

**Descrição do jogo:**
Z-Crusher é um eletrizante jogo de sobrevivência em meio a um apocalipse zumbi, onde o caos se espalha e apenas os mais determinados conseguem resistir. O jogador deve escolher entre quatro personagens distintos: Nerd - possui disparos rápidos e frequentes, mas pouca vida e curto alcance das balas. Seu corpo é grande, facilitando ser atingido -; Musculoso - tem muita vida, tiros velozes, alto dano e longa duração dos projéteis -; Flash - é o mais rápido, com pouca vida e balas lentas, porém muito dano e bom alcance -; Mendel — é ágil e pequeno, com pouca vida, tiros lentos mas frequentes e boa duração dos disparos -, cada um com suas próprias características e vantagens que influenciam diretamente a forma de encarar os desafios.

O objetivo é simples e implacável: matar o maior número possível de zumbis e sobreviver ao máximo, enfrentando ondas que se tornam progressivamente mais intensas e perigosas. A cada cinco rodadas, um chefe surge para testar seus limites; e a cada dez, um novo aparece ainda mais desafiador, exigindo estratégia, precisão e agilidade.

Durante o jogo, o jogador pode coletar power-ups espalhados pelo cenário para obter vantagens temporárias, como vida extra, aumento de velocidade, explosões que eliminam todos os inimigos em tela, momentos de invulnerabilidade e recuperação total da vida. Usá-los no momento certo pode ser a diferença entre avançar mais uma rodada ou sucumbir à horda.

Não há um fim. O jogo só termina quando o jogador morre. Por isso, é preciso dar tudo de si desde o início, acumulando o máximo de pontos possível para garantir um lugar no topo do ranking. Em Z-Crusher, cada segundo vivo é uma conquista.
**#(Texto 80% gerado por IA generativa)** - https://docs.google.com/document/d/1FBbYNyr63YL5V38gJ3QTaqBrHmdoMhvYkbo1Etg-7W0/edit?usp=sharing

**Como rodar o jogo:**
- Abrir repositório criado no Github, no VsCode;
- Após a abertura do repositório, deve-se baixar todos os arquivos nele presente;
- Depois disso, é necessário entrar em "game", seguido de "jogo.py";
- Por fim, para incializar o jogo, é só pressionar o botão "run", no canto superior direito da tela.

**Como jogar:**
- Ao rodar o jogo, você se deparará com a tela de início. Nela você se depara com o título do jogo, Z-Crusher (centralizado ao topo); um pouco mais abaixo temos o botão "Start"; um pouco mais abaixo do botão "Start", temos a opção de "Select Character"; ainda na tela de ínicio, temos também a opção "ranking".
    - **"Start":** ao ser clicado com o botão esquedro do mouse, você é redirecionado para uma nova tela. Essa tela tem em seu top a frase "ENTER YOUR NAME", um pouco mais abaixo ela conta com um retângulo que permite a escrita do nome do player e, por fim, um pouco mais abaixo ainda, a opção "Start Game", que ao ser selecionada inicia uma nova partida.
    - **Select Character:** ao clicar nessa opção uma nova tela se abre, onde se depara com imagens dos 4 personagens disponíveis para esoclha. Clicando em cima de qualquer um deles com o botão esquerdo do mouse, ele é automaticamente selecionado e já o retorna pra tela de início. Caso não queira trocar de personagem - manter o que já está selecionado - é possível selecinar o botão "back" no canto inferior esquerdo da tela, que o direcionará para tela de início novamente.
    - **Ranking:** ao ser selecionado, abre uma nova tela com as 10 melhores pontuações já registradas e os respectivos nomes dos players que as fizeram. Centralizado bem abaixo, também possui um botão "back" que te redireciona para o menu principal. 
- Ao seleconar o botão de "Start", ser redirecionado para tela de entrar com o nome do player e clicar na opção "Start Game", um novo jogo é criado, dando inicio à uma nova tela (tela padrão de todas partidas).
- Uma vez nessa tela da partida em si, nós temos: uma barra de vida no canto superior esquerdo; os powerups coletados no canto inferior esquerdo; e no rastante da tela o player, os zumbis e chefes.
- Para conseguir jogar o jogo efetivamente os comandos são: W (para andar para frente); A (para andar para esquerda); S (para andar para trás); D (para andar para direita); botão esquerdo do mouse/espaço no teclado (para atirar - você pode, tanto clicar tiro por tiro, quanto apenas segurá-lo-).
- Para conseguir pegar os powerups, basta ir em direção dele e deixar que ele enconste no seu personagem. Imediatamnete o powerup já será ativado/armazenado.
- Toda vez quem um zumbi enconstar em você uma baixa de vida será sofrida. Com os chefes o mesmo acontece, com a diferença que o dano é maior. Quando a barra de vida se esgotar e, em caso de você não possuir nenhum powerup de vida extra, você morre e o jogo acaba, o redirecionando para tela de "Game Over".
- A tela de 'Game Over" possui uma breve mensagem, assim como a sua pontuação final naquela partida (caso ela esteja entre as 10 maiores já feitas, seu nome e quantidade de pontos serão automaticmante armazenados no ranking). Para sair dessa tela e voltar a tela incial, bastar apertar qualquer botão do seu teclado.

**Instalação de Bibliotecas:**
    **Pygame:**
        - Pré-requisitos: ter o VsCode e o Anaconda Prompt instalados;
        - Abrir Anaconda Prompt e digitar: "pip install pygame"
        - Abrir arquivo no VsCode e dar: "import pygame".
    **Demais:**
        - Todas as outras bibliotecas ultilizadas na produção desse jogo, já são proveninetes da biblioteca padrão do Python, logo, basta dar um import "nome da biblioteca" para ter acesso a elas.

**Uso de IA Generativa no Código:**
- Linhas 125 há 146 (com as funções: load_ranking, save_ranking e adding_to_ranking) foram 100% realizadas por IA Generativa. O histórico do ChatGPT se encontra no link:https://docs.google.com/document/d/19HFALhbeaHI2hEhRt5IAAw_nQO3Ci-Fmpe_L_ACSwSw/edit?usp=sharing
    - **Explicação material gerado por IA:** As linhas geradas pelo ChatGPt implementa um sistema de ranking que armazena os nomes e pontuações dos jogadores em um arquivo JSON. Primeiramente, define-se o nome do arquivo onde o ranking será salvo (ranking.json). A função load_ranking(), por sua vez, verifica se esse arquivo existe; caso seja constatado a não existência do arquivo, uma lista vazia é retornada. Se o arquivo existir, ele é aberto e carregado usando json.load(). Caso ocorra algum erro durante essa leitura, uma lista vazia também é retornada. Já a função save_ranking(ranking) recebe uma lista de rankings e a grava no arquivo JSON, escrevendo seu conteúdo com dados atualizados sob antigos. Por fim, a função add_to_ranking(name, score) serve para adicionar uma nova entrada ao ranking: ela carrega o ranking atual, insere um novo dicionário com o nome e a pontuação do jogador, ordena a lista de forma decrescente pelo valor da pontuação (lambda x: x[score]), mantém apenas os 10 melhores colocados e salva o ranking atualizado de volta no arquivo. Ela também retorna a nova lista de ranking após a atualização.
- Todas as imagens sendo ultilizadas no jogo, também são provenientes da IA generativa ChatGPT.

**Endereço Vídeo do Jogo:** 
https://youtu.be/5BNZLFjUSAM

