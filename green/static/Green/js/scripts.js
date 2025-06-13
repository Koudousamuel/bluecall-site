
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
                        <div class="col-md-2 gy-9 gx-0">
                            <div class="card">
                                <img src="${product.image_url}" alt="" class="card-img-top" height="280">
                                <div class="card-body">
                                    <div class="card-title" id="aa${product.id}">${product.title}</div>
                                    <div class="card-text"><span id="price${product.id}"  class="text-danger">${product.price} FCFA</span></div>
                                    <a href="/${product.id}/" class="btn btn-warning">Voir</a>   
                                    <button 
                                    class="btn ted btn-custom" 
                                    data-id="${ product.id }" 
                                    data-nom="${product.title}">

                                    Ajouter
                                    </button>
              
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




