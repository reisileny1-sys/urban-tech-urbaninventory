def mostrar_menu():
    print("------------------ URBANINVENTORY ------------------")
    print("1. Cadastrar ativo")
    print("2. Cadastrar localização")
    print("3. Cadastrar usuário")
    print("4. Cadastrar papel")
    print("5. Cadastrar permissão")
    print("6. Consultar ativos")
    print("7. Consultar conjuntos (U, n, -, disjuntos)")
    print("8. Consultar relações")
    print("9. Validar acesso (RBAC)")
    print("10. Generar relatório")
    print("11. Associar ativo à jurisdição")
    print("12. Matriz de pertencimento")
    print("13. Exportar ativos para CSV")
    print("0. Sair")
    print("----------------------------------------------------")

def main():
    while True:
        mostrar_menu()
        opcao = input("Escolha: ")
        
        if opcao == "1":
            print("\n-> Executando: Cadastrar ativo...\n")
        elif opcao == "0":
            print("\nEncerrando o sistema...")
            break
        else:
            print("\nOpção inválida! Tente novamente.\n")

if __name__ == "__main__":
    main()