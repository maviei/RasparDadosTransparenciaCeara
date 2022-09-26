from time import sleep
import sys
import pandas as pd
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import Playwright, sync_playwright, expect
from datetime import datetime


def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=True)
    context = browser.new_context()
    page2 = context.new_page()#segunda guia 
    context.set_default_navigation_timeout(100000000)
    
    # Open new page 
    page = context.new_page()
    context.set_default_navigation_timeout(100000000)
    
    pag = 1 #Iniciar na páginação 1
    #Link da página com filtro
    page.goto(f"https://cearatransparente.ce.gov.br/portal-da-transparencia/servidores?cod_orgao=221&functional_status=+&integration_supports_server_role_id=246&locale=&month_year=08%2F2022&page={pag}&search=&sort_column=&sort_direction=&__=__")  
    page.locator('xpath=/html/body/div[5]/div[2]/div/div/div[1]/button/span').click() #fechar popup 1
    page.locator('body > div.card.privacy_statement.text-justify > div:nth-child(4) > div > a').click() #fechar popup 2 aceita termos
    

    
    
    df = pd.DataFrame()
    for r in range(10000):
        l = 1
        k = 1
        for i in range(10):
            nomes = page.locator(f"xpath=//html/body/div[5]/div[6]/div/div/div[2]/div/div[2]/div/div[2]/div[3]/table/tbody/tr[{l}]/td")
            for k in range(5):
                nome = nomes.nth(0).text_content().strip()
                sb = nomes.nth(4).text_content().strip()
                sl = nomes.nth(5).text_content().strip()

            nomes.nth(k).click() #abrir link nome nova página com mais informações do servidor
            dados = page.locator("p.content-value")
            matricula = len(page.query_selector_all('xpath=/html/body/div[5]/div[4]/div/nav/a'))
            for j in range(1):
                    orgao1 = dados.nth(0).inner_text().strip()
                    data_adm1 = dados.nth(2).inner_text().strip()
                    cargo1 = dados.nth(1).inner_text().strip()
                    situacao1 = dados.nth(3).inner_text().strip()
                    ch1 = dados.nth(4).inner_text().strip()
                    if(situacao1 == "Aposentado"):
                        vsp = page.query_selector('//div[2]/div/div/div[1]/div[2]/table/tbody/tr[2]/td[2]').inner_html().strip()
                    if(situacao1 == "Ativo"):
                        vsp = page.query_selector('//div[2]/div/div/div[1]/div[2]/table/tbody/tr[1]/td[2]').inner_html().strip()
                    orgao2 = ''
                    data_adm2 = ''
                    cargo2 = ''
                    situacao2 = ''
                    ch2 = ''
                    if(matricula >= 2):
                        orgao2 = dados.nth(5).inner_text().strip()
                        data_adm2 = dados.nth(7).inner_text().strip()
                        cargo2 = dados.nth(6).inner_text().strip()
                        situacao2 = dados.nth(8).inner_text().strip()
                        ch2 = dados.nth(9).inner_text().strip()
            page.go_back()
            
            
            now = datetime.now() #data atual
            ano = now.strftime("%Y")
            mes = now.strftime("%m")
            dia = now.strftime("%d")
            horas = now.strftime("%H:%M:%S")

            date_time = now.strftime("%d/%m/%Y %H:%M:%S")

            dadossave = {
            'Nome':nome,
            'Salario bruto':sb,
            'Salario liquido':sl,
            'Vencimento/Salario/Provento':vsp,
            'Orgão1':orgao1, 
            'Data admição1':data_adm1, 
            'Cargo1':cargo1,
            'Situação1':situacao1,
            'Carga horaria1':ch1,
            'Orgão2':orgao2,
            'Data admição2':data_adm2,
            'Cargo2': cargo2,
            'Situação2':situacao2,
            'Carga horaria2':ch2,
            'TimeStamp':date_time
             }

            df = df.append(dadossave,ignore_index=True)
            df.to_csv('dados.csv', index=False, encoding="utf-8") #salvar arquivos em CSV.
             
            #Salvar arquivo em um fomulário do Google
            #Essa opção é limitada pelo número de requisição, se for acima de 100 não recomendo
            #sleep(2)
            # page2.goto("https://docs.google.com/forms/d/e/IDFOMULARIO/viewform")
            # page2.locator("text=NomeSua resposta >> input[type=\"text\"]").fill(nome)
            # page2.locator("text=Vencimento/Salario/ProventoSua resposta >> input[type=\"text\"]").fill(vsp)
            # page2.locator("text=Salário brutoSua resposta >> input[type=\"text\"]").fill(sb)
            # page2.locator("text=Salário líquidoSua resposta >> input[type=\"text\"]").fill(sl)
            # page2.locator("text=Órgão1Sua resposta >> input[type=\"text\"]").fill(orgao1)
            # page2.locator("text=Situação1Sua resposta >> input[type=\"text\"]").fill(situacao1)
            # page2.locator("text=Cargo/Função/Emprego1Sua resposta >> input[type=\"text\"]").fill(cargo1)
            # page2.locator("text=Data de admissão1Sua resposta >> input[type=\"text\"]").fill(str(data_adm1))
            # page2.locator("text=Carga horária1Sua resposta >> input[type=\"text\"]").fill(ch1)
            # if(matricula >= 2):
            #     page2.locator("text=Órgão2Sua resposta >> input[type=\"text\"]").fill(orgao2)
            #     page2.locator("text=Situação2Sua resposta >> input[type=\"text\"]").fill(situacao2)
            #     page2.locator("text=Cargo/Função/Emprego2Sua resposta >> input[type=\"text\"]").fill(cargo2)
            #     page2.locator("text=Data de admissão2Sua resposta >> input[type=\"text\"]").fill(str(data_adm2))
            #     page2.locator("text=Carga horária2Sua resposta >> input[type=\"text\"]").fill(ch2)
            # page2.locator("div[role=\"button\"]:has-text(\"Enviar\")").click()
            # page2.wait_for_url("https://docs.google.com/forms/d/e/IDFORMULARIO/formResponse")
            # # Click text=Enviar outra resposta
            # page2.locator("text=Enviar outra resposta").click()
            # page2.wait_for_url("https://docs.google.com/forms/d/e/IDFORMULARIO/viewform")        
            
            l += 1 
        page.locator("text=Próxima").click()    
        #sleep(1)
        
    context.close() 
    browser.close() 
with sync_playwright() as playwright: 
    run(playwright) 
