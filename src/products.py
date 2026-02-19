"""Product catalog for Mirra Cookies"""

PRODUCTS = {
    "c1": {
        "nome": "Ouro Belga",
        "preco": 18.0,
        "img": "https://images.pexels.com/photos/312418/pexels-photo-312418.jpeg?w=600&q=80",
        "desc": "Chocolate belga 54% cacau com massa amanteigada. Textura crocante perfeita.",
        "ingredientes": "Farinha integral, Manteiga premium, Chocolate Belga 54%, Açúcar demerara, Ovos caipiras",
        "alergênios": "Glúten, Leite, Ovos",
        "rating": 4.9,
        "categoria": "Clássicos",
        "tamanho": "50g"
    },
    "c2": {
        "nome": "Veludo Rubro",
        "preco": 20.0,
        "img": "https://images.pexels.com/photos/461198/pexels-photo-461198.jpeg?w=600&q=80",
        "desc": "Massa Red Velvet com recheio de cream cheese vanilla. Sabor único e sofisticado.",
        "ingredientes": "Farinha, Corante natural de beterraba, Cream Cheese, Baunilha Bourbon, Manteiga",
        "alergênios": "Glúten, Leite, Ovos, Corante natural",
        "rating": 4.8,
        "categoria": "Especial",
        "tamanho": "55g"
    },
    "c3": {
        "nome": "Pistache Imperial",
        "preco": 24.0,
        "img": "https://images.pexels.com/photos/1092730/pexels-photo-1092730.jpeg?w=600&q=80",
        "desc": "Pistaches iranianos premium com chocolate branco. Exclusivo e irresistível.",
        "ingredientes": "Farinha, Pistache Iraniano, Chocolate Branco Belga, Manteiga clarificada, Açúcar de coco",
        "alergênios": "Glúten, Leite, Frutos secos, Amêndoa, Iódo",
        "rating": 5.0,
        "categoria": "Premium",
        "tamanho": "60g"
    },
    "c4": {
        "nome": "Double Dark Salt",
        "preco": 19.0,
        "img": "https://images.pexels.com/photos/821365/pexels-photo-821365.jpeg?w=600&q=80",
        "desc": "Cacau black, chocolate 70% com Flor de Sal. Intenso e equilibrado.",
        "ingredientes": "Farinha, Chocolate 70% Belga, Cacau em pó, Flor de Sal Himalaia, Manteiga",
        "alergênios": "Glúten, Leite",
        "rating": 4.7,
        "categoria": "Clássicos",
        "tamanho": "50g"
    },
    "c5": {
        "nome": "Brûlée Real",
        "preco": 21.0,
        "img": "https://images.pexels.com/photos/1410235/pexels-photo-1410235.jpeg?w=600&q=80",
        "desc": "Massa de baunilha com casquinha de açúcar maçaricada. Sofisticado e delicioso.",
        "ingredientes": "Farinha, Baunilha Bourbon, Açúcar cristal, Manteiga francesa, Ovos, Caramelo",
        "alergênios": "Glúten, Leite, Ovos",
        "rating": 4.9,
        "categoria": "Especial",
        "tamanho": "55g"
    },
    "c6": {
        "nome": "Nutella Supreme",
        "preco": 22.0,
        "img": "https://images.pexels.com/photos/1092730/pexels-photo-1092730.jpeg?w=600&q=80",
        "desc": "Massa clássica recheada com Nutella pura. Irresistível para os amantes de chocolate.",
        "ingredientes": "Farinha, Nutella 100%, Manteiga premium, Ovos caipiras, Açúcar",
        "alergênios": "Glúten, Leite, Ovos, Amêndoa, Avelã",
        "rating": 4.6,
        "categoria": "Clássicos",
        "tamanho": "55g"
    },
    "combo1": {
        "nome": "Combo Imperial (4 un)",
        "preco": 70.0,
        "img": "https://images.pexels.com/photos/1085730/pexels-photo-1085730.jpeg?w=600&q=80",
        "desc": "4 cookies premium à sua escolha com 15% de desconto especial.",
        "ingredientes": "Variado - Escolha seus sabores favoritos",
        "alergênios": "Consulte os produtos individuais",
        "rating": 4.8,
        "categoria": "Promoção",
        "tamanho": "200g total"
    },
    "combo2": {
        "nome": "Combo Perfeito (6 un)",
        "preco": 100.0,
        "img": "https://images.pexels.com/photos/1085730/pexels-photo-1085730.jpeg?w=600&q=80",
        "desc": "6 cookies premium à sua escolha com 20% de desconto e embalagem premium.",
        "ingredientes": "Variado - Escolha seus sabores favoritos",
        "alergênios": "Consulte os produtos individuais",
        "rating": 4.9,
        "categoria": "Promoção",
        "tamanho": "300g total"
    }
}

# Categorias disponíveis
CATEGORIES = {
    "Clássicos": "Sabores tradicionais e deliciosos",
    "Especial": "Criações exclusivas e sofisticadas",
    "Premium": "Ingredientes raros e importados",
    "Promoção": "Combos com desconto especial"
}

# FAQs
FAQS = [
    ("Quanto tempo duram os cookies?", 
     "Os cookies têm validade de 7 dias em ambiente fresco e seco. Recomendamos consumir nos primeiros 3 dias para máximo frescor."),
    
    ("Vocês fazem delivery?",
     "Sim! Fazemos entregas em até 48 horas na região metropolitana. Frete calculado no checkout."),
    
    ("Qual é a política de devolução?",
     "Oferecemos garantia de 7 dias. Se o produto chegar com defeito, fazemos a troca sem perguntas."),
    
    ("Como fazer cookies personalizados?",
     "Sim! Aceitamos pedidos personalizados. Solicite com mínimo 10 dias de antecedência via WhatsApp: (11) 99999-8888"),
    
    ("Como armazenar corretamente?",
     "Guarde em local fresco, seco e longe de umidade. NUNCA refrigere! Prefira potes de vidro com vedação."),
    
    ("Posso combinar cupons?",
     "Não. Apenas um cupom por pedido. Se tiver múltiplos cupons, use o de maior desconto."),
    
    ("Qual é a origem dos ingredientes?",
     "Usamos chocolate belga importado, manteiga francesa e ingredientes premium de fornecedores certificados."),
    
    ("Vocês entregam em todo o Brasil?",
     "Atualmente fazemos entrega na região metropolitana. Para outros locais, entre em contato via WhatsApp para cotação."),
    
    ("Qual é o valor mínimo para entrega?",
     "Não há mínimo! Entregamos desde um único cookie. O frete varia conforme localização."),
    
    ("Como é feito o cálculo do frete?",
     "O frete é calculado via CEP na região de cobertura. Oferecemos frete grátis para compras acima de R$ 100.")
]

# Informações de contato
CONTACT_INFO = {
    "address": "Rua Imperial, 123 - São Paulo, SP 01310-100",
    "email": "contato@mirracookies.com.br",
    "whatsapp": "(11) 99999-8888",
    "instagram": "@mirracookies",
    "facebook": "mirracookiesoficial",
    "hours": {
        "segunda_sexta": "9:00 - 18:00",
        "sabado": "10:00 - 14:00",
        "domingo": "Fechado"
    }
}

# Sobre a empresa
ABOUT_TEXT = """
**Mirra Cookies** é uma empresa artesanal especializada em cookies premium, criada em 2022 com paixão 
por qualidade e excelência.

Utilizamos apenas ingredientes de qualidade excepcional - chocolate belga importado, manteiga francesa, 
e frutas selecionadas - combinados com técnicas artesanais que honram tradições autênticas.

Cada cookie é feito à mão, com cuidado e dedicação, para oferecer uma experiência única de sabor. 
Somos comprometidos com sustentabilidade, usando embalagens eco-friendly e práticas responsáveis.
"""

# Políticas
POLICIES = {
    "termos": """
    <h3>📋 Termos de Serviço</h3>
    <ul>
        <li><b>Entrega:</b> Até 48 horas úteis na região de cobertura</li>
        <li><b>Devolução:</b> 7 dias para defeitos de fabricação</li>
        <li><b>Alergênios:</b> Consulte sempre os ingredientes antes de consumir</li>
        <li><b>Privacidade:</b> Seus dados não são compartilhados com terceiros</li>
        <li><b>Garantia:</b> 100% da qualidade garantida</li>
    </ul>
    """,
    
    "privacidade": """
    <h3>🔐 Política de Privacidade</h3>
    <p>Seu endereço de e-mail e dados pessoais são protegidos e nunca compartilhados. 
    Usamos encriptação SSL para proteger suas informações de pagamento.</p>
    
    <h4>Como usamos seus dados:</h4>
    <ul>
        <li>Processamento de pedidos</li>
        <li>Envio de códigos de recuperação de senha</li>
        <li>Atualizações sobre seu pedido</li>
        <li>Melhorias no serviço (com sua autorização)</li>
    </ul>
    """,
    
    "garantia": """
    <h3>✨ Garantia de Qualidade</h3>
    <p>Se receber um cookie com defeito, defeito de sabor ou fora do esperado, 
    faremos a reposição ou devolução do dinheiro, sem perguntas.</p>
    
    <p><b>Como solicitar:</b> Mande foto do produto e descreva o problema via WhatsApp 
    em até 24 horas após receber o pedido.</p>
    """
}
