$(document).ready(function() {
    $("#name").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/api-acutocomplte-employee/",
                data: { term: request.term },
                dataType: "json",
                success: function(data) {
                    response(data);
                },
                error: function(err) {
                    console.error("Error fetching autocomplete data:", err);
                    // Optionally, provide user feedback about the error
                }
            });
        },
        minLength: 0,  // Minimum length of the input before triggering autocomplete
        select: function(event, ui) {
            $("#name").val(ui.item.value); 
            $("#employee_id_id").val(ui.item.id);
            $("#basic_pay").val(ui.item.basic_monthly_pay / 2);
            // Get the value of the input field with id 'name'
            var nameValue = $("#name").val();
            // console.log(nameValue)
            // $("#name_for").val(ui.item.value);
            $("#name_for_ca").autocomplete("search", ui.item.value);
           
            $("#name_for_ca2").autocomplete("search", ui.item.value);
           

            return false;
        }
    });

  
});






// this  function is for autocomplete for cash advances

$(function() {
    $("#name_for_ca").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/graphql",
                method: "POST",
                contentType: "application/json",
                data: JSON.stringify({
                    query: `
                        query($searchTerm: String!) {
                            getSssByTerm(searchTerm: $searchTerm)
                        }
                    `,
                    variables: {
                        searchTerm: request.term
                    }
                }),
                success: function(result) {
                    // Extract the autocomplete results from the GraphQL response
                    var autocompleteResults = result.data.getSssByTerm;
                    // Display the autocomplete results in the 'name' input field
                    $("#sss_loan").val(autocompleteResults);
                }
            });
        },
        minLength: 2 // Minimum characters before autocomplete starts
    });
});


$(function() {
    $("#name_for_ca2").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/graphql",
                method: "POST",
                contentType: "application/json",
                data: JSON.stringify({
                    query: `
                        query GetCashAdvance($searchTerm: String!) {
                            getCashAdvanceByTerm(searchTerm: $searchTerm)
                        }
                    `,
                    variables: {
                        searchTerm: request.term
                    }
                }),
                success: function(result) {
                    // Extract the autocomplete results from the GraphQL response
                    var autocompleteResults = result.data.getCashAdvanceByTerm;
                   
                    // Pass the results array to the response callback function
                    response(autocompleteResults);
                },
                error: function(xhr, status, error) {
                    console.error("Error fetching autocomplete data:", error);
                    response([]); // Provide an empty response in case of an error
                }
            });
        },
        minLength: 2, // Minimum characters before autocomplete starts
        select: function(event, ui) {
            // Handle the selection event if needed
        }
    });
});




// Define a function for the second code
// function setupSecondAutocomplete() {
//     $("#name").autocomplete({
//         source: function(request, response) {
//             $.ajax({
//                 url: "/graphql",
//                 method: "POST",
//                 contentType: "application/json",
//                 data: JSON.stringify({
//                     query: `
//                         query($searchTerm: String!) {
//                             getCashAdvanceByTerm(searchTerm: $searchTerm)
//                         }
//                     `,
//                     variables: {
//                         searchTerm: request.term
//                     }
//                 }),
//                 success: function(result) {
//                     // Extract the autocomplete results from the GraphQL response
//                     var autocompleteResults = result.data.getCashAdvanceByTerm;
//                     // Display the autocomplete results in the 'name' input field
//                     $("#general_loan").val(autocompleteResults);
//                 }
//             });
//         },
//         minLength: 2 // Minimum characters before autocomplete starts
//     });
// }






// this is for computation of gross payroll

$(document).ready(function() {
    $('#basic_pay,#late,#absent,#under_time,#normal_working_day_ot, \
        #holiday_ot,#basic_pay_adjustment').on('input', function() {
        calculatetotalGross();
    });
    });

    function calculatetotalGross() {
    
    let basic_pay;
    let late;
    let absent;
    let under_time;
    let normal_working_day_ot;
    let holiday_ot;
    let basic_pay_adjustment;
   


    basic_pay = $('#basic_pay').val() || 0;
    late = $('#late').val() || 0;
    absent = $('#absent').val() || 0;
    under_time = $('#under_time').val() || 0;
    normal_working_day_ot = $('#normal_working_day_ot').val() || 0;
    holiday_ot = $('#holiday_ot').val() || 0;
    basic_pay_adjustment = $('#basic_pay_adjustment').val() || 0;
    
    
    let product;
    let product2
    product = (parseFloat(basic_pay) + parseFloat(late)
                    + parseFloat(absent) + parseFloat(under_time)
                    + parseFloat(normal_working_day_ot) + parseFloat(holiday_ot)
                    + parseFloat(basic_pay_adjustment));

    product2 = product.toFixed(2);
    const stringNumber = product.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
    $('#gross_pay').val(stringNumber);
    $('#gross_pay2').val(product2);
    
    calculatetotalDeduction()
    calculatetotalNetpay()

    }


// this is for computation of total deduction

$(document).ready(function() {
    $('#housing_loan,#sss_loan,#hdmf_loan,#general_loan,#company_loan').on('input', function() {
        calculatetotalDeduction();
    });
    });

    function calculatetotalDeduction() {
    
    let housing_loan;
    let sss_loan;
    let hdmf_loan;
    let general_loan;
    let company_loan;
   
   


    housing_loan = $('#housing_loan').val() || 0;
    sss_loan = $('#sss_loan').val() || 0;
    hdmf_loan = $('#hdmf_loan').val() || 0;
    general_loan = $('#general_loan').val() || 0;
    company_loan = $('#company_loan').val() || 0;
    
    
    
    let product;
    let product2
    product = (parseFloat(housing_loan) + parseFloat(sss_loan)
                    + parseFloat(hdmf_loan) + parseFloat(general_loan)
                    + parseFloat(company_loan)
                    );

    product2 = product.toFixed(2);
    const stringNumber = product.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
    $('#total_deduction').val(stringNumber);
    $('#total_deduction2').val(product2);
    calculatetotalNetpay()
    }


// this is for computation of NET PAY

    $(document).ready(function() {
        $('#gross_pay2,#total_deduction2').on('input', function() {
            calculatetotalNetpay();
        });
        });

        function calculatetotalNetpay() {
        
        let gross_pay2;
        let total_deduction2;
        
    
    


        gross_pay2 = $('#gross_pay2').val() || 0;
        total_deduction2 = $('#total_deduction2').val() || 0;
       
        
        
        
        let product;
        let product2
        product = (parseFloat(gross_pay2) - parseFloat(total_deduction2)
                        );

        product2 = product.toFixed(2);
        const stringNumber = product.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
        $('#net_pay').val(stringNumber);
        $('#total_deduction2').val(product2);
        }