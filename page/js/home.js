
fetch('http://127.0.0.1:8005/')
  .then(response => response.json()) // Convert response to JSON
  .then(funkos => {

    const container = document.querySelector('.product-grid');
    console.log(container)
    for (let i = 0; i < Math.min(8, funkos.length); i++) {
      const funko = funkos[i];
      const div = document.createElement('div');
      div.className = 'product-card';
      div.innerHTML = `
        <a href="/item?item=${funko.id}">
          <img src="${funko.link_image}" alt="${funko.name}" class="product-image" />
        </a>
        <h3>${funko.name}</h3>
        <p>$${funko.cost}</p>
        <form method="POST" action="/add_to_cart/${funko.id}">
          <!-- CSRF token handling is needed if you actually use this with Django -->
          <button class="add-to-cart">Add to Cart</button>
        </form>
      `;
      container.appendChild(div);
    }

  })
  .catch(error => {
    console.error('Error fetching data:', error);
  });
