# Requisitos — UrbanInventory

## Requisitos Funcionais

| Código | Descrição | Implementação |
|--------|-----------|---------------|
| RF01 | Cadastrar ativo |  |
| RF02 | Cadastrar localização |  |
| RF03 | Cadastrar usuário | |
| RF04 | Cadastrar papel | |
| RF05 | Cadastrar permissão | |
| RF06 | Associar ativo à jurisdição | |
| RF07 | Consultar ativos por conjunto |  |
| RF08 | Consultar relações |  |
| RF09 | Validar mapeamentos |  |
| RF10 | Validar acesso |  |
| RF11 | Produzir relatório |  |

## Requisitos Não Funcionais

- Python 3.10+
- Arquitetura em camadas (Interface → Aplicação → Núcleo → Dados)
- Testes com pytest
- Análise Big-O documentada
- Profiling com cProfile

## Casos de Teste Obrigatórios

- Usuário inexistente
- Papel inexistente
- Permissão inválida
- Ativo sem jurisdição
- Usuário com múltiplas permissões
- Acesso autorizado / negado
- Conjunto vazio, disjuntos, interseção, união, diferença
