const form = document.getElementById("checkout-form")
var reqyested_data = {}
 
form.addEventListener('submit' , (e) => {
    e.preventDefault()
    document.getElementById("checkout-now-btn").classList.add("hiddenarea")
    document.getElementById("paypal-button-container").classList.remove("hiddenarea")

})

paypal.Buttons({
    // Set up the transaction
    createOrder: function(data, actions) {
        return actions.order.create({
            purchase_units: [{
                amount: {
                    value: total
                }
            }]
        });
    },

    onApprove: function(data, actions) {
        return actions.order.capture().then(function(details) {
            createShipping(
                {
                address : document.getElementById('address').value,
                state : document.getElementById('state').value,
                city : document.getElementById('city').value,
                zip : document.getElementById('postalcode').value,
                total : total
                }
            )
            alert("Transaction Completed")
            location.reload()

        });
    }
}).render('#paypal-button-container');


var createShipping = (dataonHold) => {
    var url = '/processorder/'
    fetch(
        url,
        {
            method : 'POST',
            body : JSON.stringify({ dataonHold }),
            headers :{
                'Content-Type' : 'application/json',
                'X-CSRFToken' : csrftoken,
            }
        }
    )
    .then( response => response.json() )
    .then( data => console.log(data) )
}

