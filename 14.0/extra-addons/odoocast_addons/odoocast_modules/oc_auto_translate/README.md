# OdooCast Auto Translate

## Descrição
O módulo OdooCast Auto Translate é uma extensão para o Odoo que simplifica o processo de tradução de termos não traduzidos em sua instalação do Odoo. Ele permite que você execute ações de servidor para gerar traduções automaticamente com base no idioma da sessão dos termos selecionados na tabela `ir.translation`. Além disso, facilita a exportação e substituição de traduções por meio da interface do Odoo.

## Recursos

- Executar ação de servidor "Traduzir Texto(s) Selecionado(s)" para gerar traduções em termos não traduzidos com base no idioma da sessão dos termos selecionados na tabela `ir.translation`.
- Exportar traduções por meio de Definições > Traduções > Exportar Tradução, escolhendo idioma, formato PO e nome técnico do módulo.
- Substituir o arquivo na pasta `i18n` do módulo traduzido de forma eficiente.

## Instalação
1. Faça o download do módulo para a sua instalação do Odoo.
2. Execute `pip install mtranslate` para instalar a dependência pip necessária para rodar as traduções.
4. Procure por `oc_auto_translate` na barra de pesquisa dentro do módulo de apps.
5. Vá para o painel de administração do Odoo.
6. Acesse Configurações Técnicas > Ações > Atualizar Lista de Módulos.
7. Procure "OdooCast Auto Translate" e clique em `Criar Ação Contextual`.

## Como Usar
1. No painel de administração do Odoo, acesse a tabela `ir.translation`.
2. Selecione os termos que deseja traduzir.
3. Execute a ação de servidor "Traduzir Texto(s) Selecionado(s)" para gerar traduções em termos não traduzidos com base no idioma da sessão.
4. Para exportar traduções:
   - Vá para Definições > Traduções > Exportar Tradução.
   - Escolha o idioma, formato PO e nome técnico do módulo.
   - Exporte o arquivo de tradução.
5. Substitua o arquivo na pasta `i18n` do módulo traduzido.

## Contribuição
Contribuições são bem-vindas! Se você deseja melhorar este módulo, sinta-se à vontade para criar um pull request.

## Licença
Este módulo é distribuído sob a [AGPL3](LICENSE).

---

*Outras informações:* O nome do módulo é "OdooCast Auto Translate".
