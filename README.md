# Sistema-Fuzzy
Trabalho apresentado para a disciplina de Sistemas Fuzzy com objetivo de implementar um sistema capaz de fornecer um diagnósitco sobre a qualidade da água do rio Castelo Novo.
## Tabela de Conteúdos 
- [Descrição](#descrição)
- [Instalação](#instalação)
- [Uso](#uso)
- [Autor](#autor) 
- [Agradecimentos](#agradecimentos)
  
## Descrição
Uma grave crise hídrica afetou a região sul da Bahia, devido a isto, a busca por possíveis soluções que sejam capazes de reduzir esse problema de abastecimento fez com
que o rio Castelo Novo, fosse escolhido por uma empresa de captação de água. No entanto, as águas pertencentes a esse rio possuem altos índices de cloreto de sódio, as deixando
salobra que pode ser prejudicial a saúde. Por esse motivo, o principal objetivo desse modelo é fornecer previsões confiáveis sobre a variação da salinidade, auxiliando a empresa na tomada de decisões e garantindo que a água distribuída esteja dentro dos padrões considerados aceitáveis para consumo.

## Instalação
### Clonar o Repositório: 
  ```bash
     git clone https://github.com/diegomarcelin/Sistema-Fuzzy.git
     cd Sistema-Fuzzy
  ```
## Uso
No final do código existe uma função principal, ela é a responsável por chamar a função de inferência que é a parte mais desafiadora do projeto. Alguns gráficos das funções pertinências plotados pelas informações fornecidas das coletas não estão com o maior grau em 1, isso ocorre devido a um problema da função de plotagem ao usar números float, como ocorre em alguns intervalos das variáveis linguísticas, por exemplos, nos valores 25.5 e 19.25.

## Autor
- [Diêgo Marcelino]


