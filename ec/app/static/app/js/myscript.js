$(document).ready(function() {
    $('.plus-cart').click(function(){
        var id = $(this).attr("pid"); // Get the product ID from the button attribute
        var eml = $(this).siblings('#quantity'); // Get the quantity element
        console.log("pid=", id);
        $.ajax({
            type: "GET",
            url: "/pluscart",
            data: {
                prod_id: id
            },
            success: function(data) {
                console.log("data = ", data);
                eml.text(data.quantity); // Update the quantity in the HTML
                $('#amount').text(data.amount); // Update the amount
                $('#totalamount').text(data.totalamount); // Update the total amount
            }
        });
    });

    $('.minus-cart').click(function(){
        var id = $(this).attr("pid"); // Get the product ID from the button attribute
        var eml = $(this).siblings('#quantity'); // Get the quantity element
        console.log("pid=", id);
        $.ajax({
            type: "GET",
            url: "/minuscart",
            data: {
                prod_id: id
            },
            success: function(data) {
                console.log("data = ", data);
                eml.text(data.quantity); // Update the quantity in the HTML
                $('#amount').text(data.amount); // Update the amount
                $('#totalamount').text(data.totalamount); // Update the total amount
            }
        });
    });

    $('.remove-cart').click(function(){
        var id = $(this).attr("pid"); // Get the product ID from the button attribute
        var row = $(this).closest('.row'); // Get the parent row of the button
        console.log("pid=", id);
        $.ajax({
            type: "GET",
            url: "/removecart",
            data: {
                prod_id: id
            },
            success: function(data) {
                $('#amount').text(data.amount); // Update the amount
                $('#totalamount').text(data.totalamount); // Update the total amount
                row.remove(); // Remove the entire row containing the product
            }
        });
    });
});
