
const form = document.getElementById("checkout-form")

form.addEventListener('submit' , (e) => {
    e.preventDefault()
    document.getElementById("checkout-now-btn").classList.add("hiddenarea")
    document.getElementById("paypal-button-container").classList.remove("hiddenarea")
    const reqyested_data = {
        address : document.getElementById('address').value,
        state : document.getElementById('state').value,
        city : document.getElementById('city').value,
        zip : document.getElementById('postalcode').value

    }
    createShipping(reqyested_data)
   
})


const createShipping = (dataonHold) => {
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


paypal.Buttons({
    // Set up the transaction
    createOrder: function(data, actions) {
        return actions.order.create({
            purchase_units: [{
                amount: {
                    value: '88.44'
                }
            }]
        });
    },

    // Finalize the transaction
    onApprove: function(data, actions) {
        return actions.order.capture().then(function(details) {
            // Show a success message to the buyer
            alert('Transaction completed by ' + details.payer.name.given_name + '!');
        });
    }


}).render('#paypal-button-container');




