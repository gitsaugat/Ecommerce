const add_btns = document.querySelectorAll('#add-to-cart-btn')
console.log(add_btns)

for( let i = 0; i < add_btns.length; i++ )
{
    add_btns[i].addEventListener('click' , ()=>{
        let id = add_btns[i].dataset.product
        let action = add_btns[i].dataset.action
        if( user === "AnonymousUser" )
        {
            console.log("not logged in")
        }
        else{
            updateOrder(id , action)
        }
    })

}

const updateOrder = (pk , action) => {

    var url = '/updateitem/'
    fetch(
        url ,
        {
        method: 'POST',
        headers : {
            'Content-Type' : 'application/json',
            'X-CSRFToken' : csrftoken

        },
        body : JSON.stringify({ productId : pk , action : action })
        }

        )
        .then(response => response.json())
        .then( data => location.reload() )
}

