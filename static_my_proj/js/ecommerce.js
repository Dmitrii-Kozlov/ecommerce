$(document).ready(function () {
  // Contact Form
  let contactForm = $(".contact-form")
  let contactFormMethod = contactForm.attr("method")
  let contactFormEndpoint = contactForm.attr("action")
  contactForm.submit(function (event) {
        event.preventDefault()
      let contactFormData = contactForm.serialize()
      let thisForm =$(this)
      $.ajax({
          method: contactFormMethod,
          url: contactFormEndpoint,
          data: contactFormData,
          success: function (data) {
            thisForm[0].reset()
              $.alert({
                  title: "Thank you!",
                  content: data.success_message,
                  theme: "modern"
              })
          },
          error: function (error) {
              console.log(error)
              let errorData = error.responseJSON
              let msg = ""
              $.each(errorData, function (key, value) {
                msg += key + ": " + value[0].message + "<br>"
              })
            $.alert({
                  title: "Oops!",
                  content: msg,
                  theme: "modern"
              })
          }
      })
  })


  // Add Product to Cart
  let productForm = $(".form-product-ajax")
  productForm.submit(function (event) {
    event.preventDefault()
      let thisForm = $(this)
      let actionEndpoint = thisForm.attr("action")
      let httpMethod = thisForm.attr("method")
      let formData = thisForm.serialize()

      $.ajax({
          url: actionEndpoint,
          method: httpMethod,
          data: formData,
          success: function (data) {
            let submitSpan = thisForm.find(".submit-span")
              if (data.added) {
                  submitSpan.html("<button type=\"submit\" class=\"btn btn-primary\">Remove from cart</button>")
              } else {
                  submitSpan.html("<button type=\"submit\" class=\"btn btn-success\">Add to cart</button>")
              }
            let cartCount = $(".navbar-cart-count")
            cartCount.text(data.navbarCartCount)

            let currentPath = window.location.href
            if (currentPath.indexOf("cart") != -1) {
                updateCart()
            }
          },
          error: function (errorData) {
              $.alert({
                  title: "Oops!",
                  content: "Error",
                  theme: "modern"
              })

          }
      })
  })
function updateCart() {
    console.log("in current cart")
    let cartTable = $(".cart-table")
    let cartBody = cartTable.find(".cart-body")
    let productRows = cartBody.find(".cart-product")
    //cartBody.html("<h1>Changed</h1>")
    let currentUrl = window.location.href
    let updateCartMethod = 'GET'
    let updateCartUrl = '/api/cart'
    let data = {}

    $.ajax({
        url: updateCartUrl,
        method: updateCartMethod,
        data : data,

        success: function (data) {
            let hiddenCartItemRemoveForm = $(".cart-item-remove-form")
            if (data.products.length > 0) {
            productRows.html(" ")
                i = data.products.length
                $.each(data.products, function(index, value){
                    let newCartItemRemove = hiddenCartItemRemoveForm.clone()
                    newCartItemRemove.css("display", "block")
                    newCartItemRemove.find(".cart-item-product-id").val(value.id)
                    cartBody.prepend("<tr><th scope=\"row\">" + i + "</th><td><a href='" + value.url + "'>" + value.title + "</a>"+ newCartItemRemove.html() +"<td>" + value.price +"</td></tr>")

                    i --
                })
                cartBody.find(".cart-subtotal").text(data.subtotal)
                cartBody.find(".cart-total").text(data.total)

            } else {
                window.location.href = currentUrl
            }


        },
        error: function (errorData) {
            $.alert({
                  title: "Oops!",
                  content: "Error",
                  theme: "modern"
              })

        }

    })
}

})