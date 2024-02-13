function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie!='') {
        const cookies = document.cookie.split(';');
        for (let i=0; i<cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length +1)) {
                cookieValue = decodeURIComponent(cookie.substring(name.length+1));
                break;
            }
        }
    }

    return cookieValue
}
const csrfToken = getCookie('csrftoken');




let add2cartBtns = document.querySelectorAll(".product-action-2 button")
console.log("Add to cart button Tally: "+ add2cartBtns)
add2cartBtns.forEach(btn =>{
    btn.addEventListener("click", addToCart)
})



function addToCart(e){
    let product_id = e.target.value
    let url = "/add_to_cart"
    let data = {id:product_id}

    fetch(url, {
        method : "POST",
        headers: {
            "Content-Type":"application/json", 
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(data => {
        console.log(data.tally)
        console.log(data.cart_items)

        document.getElementById("tally").innerHTML = data.tally
        document.getElementById("tally2").innerHTML = data.tally
        document.getElementById("tally-hover").innerHTML = data.tally
        if (data.success_message) {
            // Create the success message div
            let successMessageDiv = document.createElement('div');
            successMessageDiv.classList.add('alert', 'alert-success', 'alert-dismissible', 'fade', 'show', 'mx-5', 'my-1');
            successMessageDiv.setAttribute('role', 'alert');
            successMessageDiv.innerHTML = `
                <strong>Success!</strong> ${data.success_message}
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            `;

            // Append the success message div as the first item in the product-area section
            let productArea = document.querySelector('.product-area');
            productArea.insertBefore(successMessageDiv, productArea.firstChild);
            // Scroll to the top of the page
            window.scrollTo({
                top: 0,
                behavior: 'smooth'  // Optional smooth scrolling
            });

            // update cart items
            updateCartItems(data.cart_items);
        }
    })
    .catch(err => {
        console.log(err)
    })


}

function updateCartItems(cartItems) {
    let shoppingList = document.querySelector(".shopping-list");
    shoppingList.innerHTML = ""; // Clear existing cart items
    let totalAmount = 0;

    cartItems.forEach(cartItem => {
        // Fetch photo object using the photo_id
        fetch(`api/v1/photos/${cartItem.photo_id}`) 
            .then(response => response.json())
            .then(photo => {
                let listItem = document.createElement("li");
                listItem.innerHTML = `
                    <a href="#" class="remove" title="Remove this item"><i class="fa fa-remove"></i></a>
                    <a class="cart-img" href="#"><img src="https://res.cloudinary.com/thinc/${photo.webp_image}" style="width: 70px; height: auto" alt="${photo.title}"></a>
                    <h4><a href="#">${photo.title}</a></h4>
                    <p class="quantity">${cartItem.quantity}x - <span class="amount">Sh. ${photo.price}</span></p>
                `;
                shoppingList.appendChild(listItem);
                console.log('QTY: '+cartItem.quantity)
                console.log('PRICE: '+photo.price)

                let subTotal = parseInt(cartItem.quantity)*parseInt(photo.price);
                console.log('SUBTOTAL: '+subTotal)
                totalAmount += subTotal
                console.log('TOTAL: '+totalAmount)

                let totalAmountElement = document.querySelector(".total-amount");
                if (totalAmountElement) {
                    totalAmountElement.textContent = `Sh. ${Number(totalAmount).toFixed(2)}`;
                }
            })  

        
            .catch(error => {
                console.error('Error fetching photo:', error);
            });
    });
    console.log('TOTAL From outside the loop: '+totalAmount)

}