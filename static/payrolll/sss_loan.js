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

            return false;
        }
    });

  
});


// this function is for inserting data

const insert_sss_loan = async () => {

    
    const data = {
        employee_id_id: document.getElementById("employee_id_id").value,
        is_active: document.getElementById("is_active").value,
        amount_deduction: document.getElementById("amount_deduction").value,
    };

    console.log(data)
    
    try {
        const response = await fetch(`/api-insert-sss-loan/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            const responseData = await response.json();
            console.log(responseData);
            // Data saved successfully
            window.alert("Your data has been saved!!!!");
            // Optionally, you can redirect to another page
            window.location.assign("/insert-sss-loan/");
        } else if (response.status === 401) {
            // Unauthorized, session has expired
            window.alert("Session has expired");
        } else if (response.status === 400) {
            // Bad Request, duplicate branch
            const responseData = await response.json();
            window.alert(`Error: ${responseData.detail}`);
        } else {
            // Handle other errors
            window.alert("An unexpected error occurred");
        }
    } catch (error) {
        // Handle unexpected errors
        window.alert("An unexpected error occurred");
        console.log(error);
    }
};


// Attach the event listener to the button
const btn_save_sss_loan_deduction = document.querySelector('#btn_save_sss_loan_deduction');
btn_save_sss_loan_deduction.addEventListener("click", insert_sss_loan);


// this is to display table
$(document).ready(function() {
    // Function to fetch data and populate table
    function populateTable() {
        $.ajax({
            url: '/graphql', // Replace with your GraphQL endpoint
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                query: `
                    query {
                        getSssLoanDeductions {
                            id
                            employeeId
                            firstName
                            lastName
                            amountDeduction
                        }
                    }
                `
            }),
            success: function(response) {
                if (response && response.data && response.data.getSssLoanDeductions && Array.isArray(response.data.getSssLoanDeductions)) {
                    console.log('Data received from server:', response.data.getSssLoanDeductions);
                    var tableBody = $('#table_sss_loan tbody');
                    tableBody.empty(); // Clear table body

                    // Populate table rows with data
                    response.data.getSssLoanDeductions.forEach(function(item) {
                        var row = '<tr>' +
                            '<td>'  + item.id + '</td>' + // Adjust this line to include ID
                            '<td>'  + item.employeeId + '</td>' + // Adjust this line to include Employee ID
                            '<td>' + item.lastName + '</td>' +
                            '<td>' + item.firstName + '</td>' +
                            '<td>' + item.amountDeduction + '</td>' +
                            '</tr>';
                        tableBody.append(row);
                    });
                } else {
                    console.error('Data format error or empty data received from server.');
                }
            },
            error: function(error) {
                console.error('GraphQL request failed:', error);
            }
        });
    }

    // Call populateTable function on document ready
    populateTable();
});


// jQuery code to call the modal for updating the sss loan
$(document).ready(function() {
    
    $('#btn_update_sss_loan').click(function() {
        $('#update_sss_loan_modal').modal('show');
    });
});



// jQuery code to update amount deduction field based on update_id input
$(document).ready(function() {
    $('#update_id').on('keyup', function() {
        fetchData();
    });

    // $('#search_button_update').click(function() {
    //     fetchData();
    // });

    function fetchData() {
        var updateIdValue = $('#update_id').val();

        // Make a GraphQL request to fetch data based on the update ID
        $.ajax({
            url: '/graphql', // Replace with your GraphQL endpoint
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                query: `
                    query getSssLoanById($searchTerm: String!) {
                        getSssLoanById(searchTerm: $searchTerm) {
                            amountDeduction
                        }
                    }
                `,
                variables: {
                    searchTerm: updateIdValue
                }
            }),
            success: function(response) {
                // Check if response has data
                if (response.data && response.data.getSssLoanById) {
                    var amountDeductionValue = response.data.getSssLoanById[0].amountDeduction; // Access the first element of the array
                    console.log(amountDeductionValue)
                    $('#update_amount_deduction').val(amountDeductionValue);
                } else {
                    // Clear amount deduction field if no data found
                    $('#update_amount_deduction').val('');
                }
            },
            error: function(error) {
                console.error('GraphQL request failed:', error);
            }
        });
    }

});

//  this function is to update 
$(document).ready(function() {
    // Bind fetchData function to modal show event
   

    $('#btn_save_changes').click(function() {
        
        updateSSSDeduction();
    });

   

    function updateSSSDeduction() {
        var id = $('#update_id').val();
        var amountDeduction = $('#update_amount_deduction').val();

        // Make an AJAX request to update the cash advance
        $.ajax({
            url: '/api-update-sss-loan/' + id,
            method: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify({
                amount_deduction: amountDeduction
            }),
            success: function(response) {
                // Handle success response
                console.log('Cash advance updated successfully:', response);
                $('#update_cash_advance_modal').modal('hide'); // Close the modal
                window.location.href = '/insert-sss-loan/';
            },
            error: function(error) {
                // Handle error response
                console.error('Error updating cash advance:', error);
                // Display error message to user if needed
            }
        });
    }
});

