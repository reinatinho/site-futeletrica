# Futeletrica 2013 - Landing Page

Landing page oficial do time de futebol Futeletrica 2013, desenvolvida em Django.

## Características

- **Design responsivo** com cores do time (preto, amarelo e branco)
- **Página principal** com história, regras e informações do time
- **Página de dashboard** com Power BI embeddado
- **Galeria de fotos** (preparada para adicionar imagens)
- **Informações sobre parceiros** (Chinelinho FC)
- **Links para redes sociais** (@futeletrica2013)

## Tecnologias Utilizadas

- Django 5.2.6
- HTML5, CSS3, JavaScript
- Font Awesome (ícones)
- Google Fonts (Roboto)

## Instalação e Execução

### 1. Ativação do ambiente virtual
```bash
source /home/trevizan/Documents/.venv/bin/activate
```

### 2. Instalação das dependências
```bash
pip install -r requirements.txt
```

### 3. Executar migrações
```bash
python manage.py migrate
```

### 4. Executar o servidor
```bash
python manage.py runserver
```

### 5. Acessar o site
Abra o navegador e acesse: `http://127.0.0.1:8000`

## Estrutura do Projeto

```
site-futeletrica/
├── futeletrica_site/          # Configurações do Django
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── main/                      # App principal
│   ├── views.py              # Views do site
│   ├── urls.py               # URLs do app
│   └── templatetags/         # Filtros customizados
├── templates/                 # Templates HTML
│   ├── base.html             # Template base
│   └── main/
│       ├── home.html         # Página principal
│       └── dashboard.html    # Página do dashboard
├── static/                   # Arquivos estáticos
│   ├── css/
│   │   └── style.css         # Estilos principais
│   ├── js/
│   │   └── script.js         # JavaScript
│   └── images/
│       └── logo.png          # Logo do time
├── manage.py
└── requirements.txt
```

## Funcionalidades

### Página Principal (/)
- Hero section com logo e estatísticas
- História do time
- Galeria de fotos (placeholder)
- Regras do grupo
- Informações sobre o parceiro Chinelinho FC
- Link para Instagram

### Dashboard (/dashboard/)
- Power BI embeddado
- Botão para tela cheia
- Link para abrir no Power BI
- Informações sobre as funcionalidades

## Personalização

### Adicionar Fotos à Galeria
1. Adicione as imagens na pasta `static/images/galeria/`
2. Modifique o template `templates/main/home.html` na seção `.galeria-grid`
3. Substitua os placeholders por elementos `<img>`

### Adicionar Logo do Chinelinho FC
1. Adicione a logo na pasta `static/images/`
2. Modifique o template em `.logo-placeholder` substituindo o ícone

### Modificar Cores
As cores podem ser alteradas no arquivo `static/css/style.css` nas variáveis CSS:
```css
:root {
    --primary-yellow: #FFD700;
    --secondary-yellow: #FFC107;
    --black: #000000;
    --white: #ffffff;
    --gray-dark: #333333;
    --gray-light: #666666;
}
```

## URLs Disponíveis

- `/` - Página principal
- `/dashboard/` - Dashboard com Power BI
- `/admin/` - Painel administrativo do Django

## Melhorias Futuras

- [ ] Sistema de upload de fotos via admin
- [ ] Blog/notícias do time
- [ ] Calendário de jogos
- [ ] Sistema de cadastro de jogadores
- [ ] Galeria dinâmica com categorias
- [ ] Integração com WhatsApp para contato

## Suporte

Para dúvidas ou melhorias, entre em contato através do Instagram @futeletrica2013 ou email futeletrica2013@gmail.com.

---

**Futeletrica 2013** - Mais que um time, uma família! ⚽🟡⚫