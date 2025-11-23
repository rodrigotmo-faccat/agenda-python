from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from bson.objectid import ObjectId
import os

class SistemaAgenda:
    def __init__(self):
        uri = "mongodb+srv://admin:admin@agenda-python.620snvg.mongodb.net/?appName=agenda-python"
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client['agenda']
        self.compromissos = self.db['compromissos']
        try:
            self.client.admin.command('ping')
            print("Sucesso!")
        except Exception as e:
            print(e)
    
    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def pausar(self):
        input("\nPressione ENTER para continuar...")
    
    def validar_data_hora(self, data_str, hora_str):
        """Valida e converte data e hora para datetime"""
        try:
            data_hora_str = f"{data_str} {hora_str}"
            data_hora = datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M")
            return data_hora
        except ValueError:
            return None
    
    def listar_compromissos(self):
        """Lista todos os compromissos cadastrados"""
        self.limpar_tela()
        print("=" * 60)
        print("LISTA DE COMPROMISSOS".center(60))
        print("=" * 60)
        
        compromissos = list(self.compromissos.find().sort("data_hora", 1))
        
        if not compromissos:
            print("\nNenhum compromisso cadastrado.")
        else:
            for i, comp in enumerate(compromissos, 1):
                data_hora = comp['data_hora'].strftime("%d/%m/%Y %H:%M")
                pessoas = ", ".join(comp['pessoas']) if comp['pessoas'] else "Nenhuma"
                
                print(f"\n[{i}] ID: {comp['_id']}")
                print(f"    Data/Hora: {data_hora}")
                print(f"    Título: {comp['titulo']}")
                print(f"    Descrição: {comp['descricao']}")
                print(f"    Pessoas: {pessoas}")
                print("-" * 60)
        
        self.pausar()
    
    def cadastrar_compromisso(self):
        """Cadastra um novo compromisso"""
        self.limpar_tela()
        print("=" * 60)
        print("CADASTRAR NOVO COMPROMISSO".center(60))
        print("=" * 60)
        
        # Coleta de dados
        data = input("\nData (dd/mm/aaaa): ")
        hora = input("Hora (hh:mm): ")
        
        data_hora = self.validar_data_hora(data, hora)
        if not data_hora:
            print("\nData ou hora inválida! Use o formato correto.")
            self.pausar()
            return
        
        titulo = input("Título: ")
        if not titulo:
            print("\nO título não pode estar vazio!")
            self.pausar()
            return
        
        descricao = input("Descrição: ")
        
        pessoas = []
        print("\n--- Pessoas Envolvidas ---")
        print("(Digite o nome de cada pessoa e pressione ENTER)")
        print("(Deixe em branco e pressione ENTER para finalizar)")
        
        while True:
            pessoa = input(f"Pessoa {len(pessoas) + 1}: ").strip()
            if not pessoa:
                break
            pessoas.append(pessoa)
        
        compromisso = {
            "data_hora": data_hora,
            "titulo": titulo,
            "descricao": descricao,
            "pessoas": pessoas
        }
        
        resultado = self.compromissos.insert_one(compromisso)
        print(f"\nCompromisso cadastrado com sucesso! ID: {resultado.inserted_id}")
        self.pausar()
    
    def alterar_titulo_descricao(self):
        """Altera título e descrição de um compromisso"""
        self.limpar_tela()
        print("=" * 60)
        print("ALTERAR TÍTULO E DESCRIÇÃO".center(60))
        print("=" * 60)
        
        comp_id = input("\nDigite o ID do compromisso: ").strip()
        
        try:
            compromisso = self.compromissos.find_one({"_id": ObjectId(comp_id)})
            
            if not compromisso:
                print("\nCompromisso não encontrado!")
                self.pausar()
                return
            
            print(f"\nTítulo atual: {compromisso['titulo']}")
            novo_titulo = input("Novo título (deixe em branco para manter): ").strip()
            
            print(f"\nDescrição atual: {compromisso['descricao']}")
            nova_descricao = input("Nova descrição (deixe em branco para manter): ").strip()
            
            update_data = {}
            if novo_titulo:
                update_data["titulo"] = novo_titulo
            if nova_descricao:
                update_data["descricao"] = nova_descricao
            
            if update_data:
                self.compromissos.update_one(
                    {"_id": ObjectId(comp_id)},
                    {"$set": update_data}
                )
                print("\nCompromisso atualizado com sucesso!")
            else:
                print("\nNenhuma alteração realizada.")
            
        except Exception as e:
            print(f"\nErro: {e}")
        
        self.pausar()
    
    def alterar_pessoas(self):
        """Altera as pessoas envolvidas em um compromisso"""
        self.limpar_tela()
        print("=" * 60)
        print("ALTERAR PESSOAS ENVOLVIDAS".center(60))
        print("=" * 60)
        
        comp_id = input("\nDigite o ID do compromisso: ").strip()
        
        try:
            compromisso = self.compromissos.find_one({"_id": ObjectId(comp_id)})
            
            if not compromisso:
                print("\nCompromisso não encontrado!")
                self.pausar()
                return
            
            print(f"\nPessoas atuais: {', '.join(compromisso['pessoas']) if compromisso['pessoas'] else 'Nenhuma'}")
            print("\n--- Nova Lista de Pessoas ---")
            print("(Digite o nome de cada pessoa e pressione ENTER)")
            print("(Deixe em branco e pressione ENTER para finalizar)")
            
            novas_pessoas = []
            while True:
                pessoa = input(f"Pessoa {len(novas_pessoas) + 1}: ").strip()
                if not pessoa:
                    break
                novas_pessoas.append(pessoa)
            
            self.compromissos.update_one(
                {"_id": ObjectId(comp_id)},
                {"$set": {"pessoas": novas_pessoas}}
            )
            print("\nLista de pessoas atualizada com sucesso!")
            
        except Exception as e:
            print(f"\nErro: {e}")
        
        self.pausar()
    
    def excluir_pessoa(self):
        """Exclui uma pessoa de um compromisso"""
        self.limpar_tela()
        print("=" * 60)
        print("EXCLUIR PESSOA DE UM COMPROMISSO".center(60))
        print("=" * 60)
        
        comp_id = input("\nDigite o ID do compromisso: ").strip()
        
        try:
            compromisso = self.compromissos.find_one({"_id": ObjectId(comp_id)})
            
            if not compromisso:
                print("\nCompromisso não encontrado!")
                self.pausar()
                return
            
            if not compromisso['pessoas']:
                print("\nEste compromisso não possui pessoas cadastradas.")
                self.pausar()
                return
            
            print("\nPessoas cadastradas:")
            for i, pessoa in enumerate(compromisso['pessoas'], 1):
                print(f"  [{i}] {pessoa}")
            
            nome_pessoa = input("\nDigite o nome da pessoa a excluir: ").strip()
            
            if nome_pessoa in compromisso['pessoas']:
                self.compromissos.update_one(
                    {"_id": ObjectId(comp_id)},
                    {"$pull": {"pessoas": nome_pessoa}}
                )
                print(f"\nPessoa '{nome_pessoa}' excluída com sucesso!")
            else:
                print(f"\nPessoa '{nome_pessoa}' não encontrada neste compromisso.")
            
        except Exception as e:
            print(f"\nErro: {e}")
        
        self.pausar()
    
    def excluir_compromisso(self):
        """Exclui um compromisso completo"""
        self.limpar_tela()
        print("=" * 60)
        print("EXCLUIR COMPROMISSO".center(60))
        print("=" * 60)
        
        comp_id = input("\nDigite o ID do compromisso: ").strip()
        
        try:
            compromisso = self.compromissos.find_one({"_id": ObjectId(comp_id)})
            
            if not compromisso:
                print("\nCompromisso não encontrado!")
                self.pausar()
                return
            
            print(f"\nTítulo: {compromisso['titulo']}")
            print(f"Data/Hora: {compromisso['data_hora'].strftime('%d/%m/%Y %H:%M')}")
            
            confirmacao = input("\nConfirma a exclusão? (S/N): ").strip().upper()
            
            if confirmacao == 'S':
                self.compromissos.delete_one({"_id": ObjectId(comp_id)})
                print("\nCompromisso excluído com sucesso!")
            else:
                print("\nExclusão cancelada.")
            
        except Exception as e:
            print(f"\nErro: {e}")
        
        self.pausar()
    
    def menu_principal(self):
        """Exibe o menu principal"""
        while True:
            self.limpar_tela()
            print("=" * 60)
            print("SISTEMA DE AGENDA - MONGODB".center(60))
            print("=" * 60)
            print("\n[1] Listar compromissos")
            print("[2] Cadastrar novo compromisso")
            print("[3] Alterar título e descrição")
            print("[4] Alterar pessoas envolvidas")
            print("[5] Excluir pessoa de um compromisso")
            print("[6] Excluir compromisso")
            print("[0] Sair")
            print("\n" + "=" * 60)
            
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == '1':
                self.listar_compromissos()
            elif opcao == '2':
                self.cadastrar_compromisso()
            elif opcao == '3':
                self.alterar_titulo_descricao()
            elif opcao == '4':
                self.alterar_pessoas()
            elif opcao == '5':
                self.excluir_pessoa()
            elif opcao == '6':
                self.excluir_compromisso()
            elif opcao == '0':
                print("\nEncerrando o sistema...")
                break
            else:
                print("\nOpção inválida!")
                self.pausar()

if __name__ == "__main__":
    try:
        sistema = SistemaAgenda()
        sistema.menu_principal()
    except Exception as e:
        print(f"\nErro ao conectar ao MongoDB: {e}")
        print("Certifique-se de que o MongoDB está rodando!")