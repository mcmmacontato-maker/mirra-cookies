# Mirra Cookies

Frontend de uma loja de cookies artesanais em Recife, com foco em sabores autorais, promoções e combos para compartilhar.

## Funcionalidades

- Vitrine responsiva com sabores clássicos, recheados e veganos
- Filtros por categoria
- Carrinho lateral com subtotal e itens adicionados
- Combo promocional com desconto
- Toast de confirmação ao adicionar produtos
- Layout adaptado para desktop e mobile

## Como executar

O projeto é estático e não precisa de instalação de dependências. Na raiz do projeto, execute:

```bash
python3 -m http.server 4173
```

Depois, abra [http://localhost:4173](http://localhost:4173) no navegador.

## Estrutura

- [index.html](index.html): estrutura da página e conteúdo da loja
- [styles.css](styles.css): identidade visual, layout e responsividade
- [app.js](app.js): filtros, carrinho e interações da interface
- [flavors.css](flavors.css): imagens e tratamentos visuais específicos de cada sabor

As imagens dos produtos são carregadas via URLs do Unsplash e os ícones usam Lucide via CDN.