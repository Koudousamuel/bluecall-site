function filtrerProduits(categorie) {
    let data = {};

    if (categorie.toLowerCase() !== 'tout') {
        data = { category: categorie };
    }

    $.ajax({
        url: '/filtrer-produits/',
        type: 'GET',
        data: data,
        success: function(data) {
            let container = $("#produits-container");
            container.html("");

            if (data.error) {
                container.html(`<p>${data.error}</p>`);
            } else {
                data.forEach(product => {
                    container.append(`
                        <div class="col-6 col-sm-4 col-md-2 mb-2">
                            <div class="card h-100">
                                <img src="${product.image_url}" alt="" class="card-img-top" style="height: 180px; object-fit: cover;">
                                <div class="card-body p-2">
                                    <div class="card-title text-truncate" id="aa${product.id}" title="${product.title}">
                                        ${product.title}
                                    </div>
                                    <div class="card-text">
                                        <span id="price${product.id}" class="text-danger">${product.price} FCFA</span>
                                    </div>
                                    <div class="mt-2 d-flex flex-wrap gap-1">
                                        <a href="/${product.id}/" class="btn btn-warning btn-sm flex-fill">Voir</a>   
                                        <button 
                                            class="btn ted btn-custom btn-sm flex-fill" 
                                            data-id="${product.id}" 
                                            data-nom="${product.title}">
                                            Ajouter
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `);
                });
            }
        },
        error: function() {
            console.log("Erreur lors de la récupération des produits.");
        }
    });
}




